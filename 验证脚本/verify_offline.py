from pathlib import Path
from playwright.sync_api import sync_playwright
import shutil,json,tempfile
from datetime import date
source=Path(__file__).resolve().parent.parent;T=Path(tempfile.mkdtemp(prefix='AutoClaw 其他设备 解压验证 '));D=T/'交付文件';shutil.copytree(source,D);results=[];errors=[];blocked=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 ctx=b.new_context(viewport={'width':1512,'height':945},accept_downloads=True)
 ctx.route('http://**/*',lambda r:(blocked.append(r.request.url),r.abort()));ctx.route('https://**/*',lambda r:(blocked.append(r.request.url),r.abort()))
 page=ctx.new_page();page.set_default_timeout(8000);page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((D/'index.html').as_uri());page.locator('.slide.active').wait_for();assert page.locator('.slide').count()==20;results.append('解压至不同路径后，断网直接打开汇报首页')
 page.goto((D/'docs/report/index.html').as_uri());assert page.locator('.slide').count()==20
 for i in range(20):
  page.locator('#slide-select').select_option(str(i)) if page.locator('#slide-select').count() else page.locator('#next').click() if i else None
 page.wait_for_timeout(200)
 assert page.locator('img').evaluate_all('(xs)=>xs.filter(x=>x.offsetWidth).every(x=>x.complete&&x.naturalWidth>0)');results.append('20页汇报及图片可离线加载')
 page.goto((D/'docs/report/index.html').as_uri()+'#demo');page.locator('[data-mode=demo]').click();page.locator('[data-demo=task1]').click();f=page.frame_locator('.demo-frame').frame_locator('#task1-frame');f.locator('.product-frame').wait_for()
 f.locator('[data-target=composer]').first.click();f.locator('#prop-radius').fill('12');f.locator('[data-action=apply-params]').click();f.locator('[data-action=diff]').click();f.locator('[data-action=accept-modal]').click();assert 'v2' in f.locator('#features').inner_text()
 f.locator('[data-action=final]').click();f.locator('[data-action=confirm-final]').click();f.locator('.work-tabs [data-tab=versions]').click();f.locator('#main [data-action=export]').click()
 with page.expect_download() as dl:f.locator('[data-action=download]').click()
 assert dl.value.suggested_filename.endswith('.svg');results.append('测试1：圆角修改→候选对比→采纳v2→定稿→真实SVG下载')
 page.locator('[data-demo=task2]').click();g=page.frame_locator('.demo-frame').frame_locator('#task2-frame');g.locator('[data-action=start-review]').first.click();g.locator('[data-action=confirm-review]').click();g.locator('.review-record').first.click();assert g.locator('.review-bubble').is_visible();g.locator('[data-action=comment-candidate]').click();g.locator('[data-action=compare]').first.click();g.locator('#review-modal [data-action=accept]').click();g.locator('.review-record').first.click();g.locator('#reply-text').fill('已修改，请复核');g.locator('[data-action=reply]').click();g.locator('[data-action=resolve]').click();assert '已解决' in g.locator('#features').inner_text();results.append('测试2：发起评审→头像气泡→候选对比→采纳→回复→解决')
 page.locator('[data-demo=task1]').click();assert 'v2' in f.locator('#features').inner_text();page.locator('[data-demo=task2]').click();assert '已解决' in g.locator('#features').inner_text();results.append('双任务切换，独立状态保留')
 g.locator('.work-top > [data-action=manager-open]').click();assert g.locator('.asset-manager').is_visible();g.locator('[data-manager-close]').click();g.locator('[data-tab=canvas]').first.click();assert g.locator('.canvas-top-tools').evaluate('(e)=>e.getBoundingClientRect().height')<65;results.append('产物管理入口、顶部图标工具栏与底部工具栏可用，无挤压换行')
 page.screenshot(path=str(source/'离线演示验收.png'))
 page.goto((D/'docs/report/design-spec/index.html').as_uri());assert page.locator('img').count()==7;assert page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)');results.append('7章设计规范全部离线加载')
 for filename in ['AutoClaw录屏.mp4','Lovart录屏.mp4']:
  page.set_content('<video controls src="'+(D/'docs/research-media'/filename).as_uri()+'"></video>');page.wait_for_function('document.querySelector("video").readyState>=1');assert page.locator('video').evaluate('(e)=>e.duration')>20
 results.append('两份录屏可加载并读取时长')
 mobile=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);m=mobile.new_page();m.goto((D/'docs/report/demo/autoclaw_task2_v18/index.html').as_uri());m.locator('[data-mobile=work]').click();assert m.locator('.workspace').is_visible();results.append('390px移动视口可进入工作区（模拟，非真实手机实测）')
 assert not errors,errors;assert not blocked,blocked;results.append('演示运行无外网请求、无页面脚本报错')
 b.close()
(source/'跨设备离线验收.json').write_text(json.dumps({'date':date.today().isoformat(),'browser':'Chrome Chromium macOS headless','isolated_path':str(T),'network':'HTTP/HTTPS请求全部阻断','passed':results,'errors':errors,'external_runtime_requests':blocked,'limitations':['未在真实Windows/iOS/Android硬件验证','WebKit运行环境未安装，不宣称Safari实测','外部Figma链接需要网络与权限']},ensure_ascii=False,indent=2));print('\n'.join(results))
