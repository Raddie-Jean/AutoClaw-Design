from playwright.sync_api import sync_playwright
from pathlib import Path
import json,xml.etree.ElementTree as E
O=Path(__file__).resolve().parent;P=O/'previews';downloads=O/'demo/delivery_v18';downloads.mkdir(exist_ok=True)
results=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=b.new_page(viewport={'width':1600,'height':1120},accept_downloads=True);page.set_default_timeout(8000);page.on('pageerror',lambda e:errors.append(str(e)));page.on('download',lambda d:d.save_as(downloads/d.suggested_filename))
 page.goto('http://127.0.0.1:8771/report_v17/index.html#demo');page.locator('[data-demo="task1"]').click()
 f=page.frame_locator('.demo-frame').frame_locator('#task1-frame');f.locator('.product-frame').wait_for();assert f.locator('.product-frame').count()==1
 assert f.locator('.work-tabs').get_by_text('协作建议').count()==0
 f.locator('.work-tabs [data-action="manager-open"]').click();f.locator('.manager-content [data-folder="设计产物"]').click();assert f.locator('.manager-file-row').count()==1
 page.screenshot(path=str(P/'V18_测试1_产物管理.png'))
 f.locator('[data-edit="composer"]').click();assert not f.locator('.asset-manager').is_visible();assert f.locator('.hit.selected').count()==1
 f.locator('#prop-radius').fill('12');f.locator('[data-action="apply-params"]').click();f.locator('[data-action="diff"]').click();f.locator('[data-action="accept-modal"]').click();assert 'v2' in f.locator('#features').inner_text()
 f.locator('[data-action="final"]').click();f.locator('[data-action="confirm-final"]').click();f.locator('.work-top [data-action="export"]').click();f.locator('[data-action="download"]').click();page.wait_for_timeout(200)
 results.append('测试1：产物文件夹→选中输入卡片→圆角12→候选对比→采纳v2→定稿→真实SVG与manifest下载')
 f.locator('.work-tabs [data-action="manager-open"]').click();f.locator('.manager-tree [data-folder="最终文件"]').click();assert '定稿_v2' in f.locator('.manager-content').inner_text();f.locator('[data-manager-close]').click()
 page.locator('[data-demo="task2"]').click();g=page.frame_locator('.demo-frame').frame_locator('#task2-frame');g.locator('.work-top > .icon-btn[data-action="manager-open"]').click();g.locator('.manager-filter').fill('任务首页');assert g.locator('.tree-file').count()>=2
 page.screenshot(path=str(P/'V18_测试2_产物文件夹.png'))
 g.locator('[data-manager-close]').click();g.locator('[data-action="start-review"]').first.click();g.locator('[data-action="confirm-review"]').click();g.locator('.review-record').first.click();assert g.locator('.review-bubble').is_visible()
 page.screenshot(path=str(P/'V18_测试2_头像评审.png'))
 g.locator('[data-action="comment-candidate"]').click();g.locator('[data-action="compare"]').first.click();g.locator('#review-modal [data-action="accept"]').click();g.locator('.review-record').first.click();g.locator('#reply-text').fill('已在 v2 更新标题，请复核。');g.locator('[data-action="reply"]').click();g.locator('[data-action="resolve"]').click();assert '已解决' in g.locator('#features').inner_text()
 g.locator('.work-top [data-action="export"]').click();g.locator('[data-action="download-report"]').click();g.locator('[data-action="download-svg"]').click();g.locator('#review-modal [data-action="close"]').click();page.wait_for_timeout(200)
 results.append('测试2：文件筛选→发起评审→头像气泡→修改候选→对比采纳v2→回复与解决→真实JSON与SVG下载')
 page.locator('[data-demo="task1"]').click();assert 'v2' in f.locator('#features').inner_text();page.locator('[data-demo="task2"]').click();assert '已解决' in g.locator('#features').inner_text();results.append('双任务切换后独立状态保留')
 for frame in page.frames:
  broken=frame.locator('img').evaluate_all('(xs)=>xs.filter(x=>x.offsetWidth&&(!x.complete||!x.naturalWidth)).map(x=>x.src)');assert not broken,broken
 assert not errors,errors
 # Restart flow demonstrates original demand and generation steps.
 restart=b.new_page(viewport={'width':1512,'height':945});restart.goto('http://127.0.0.1:8771/report_v17/demo/autoclaw_task1_v18/index.html?start=1');restart.locator('[data-action="start-example"]').click();restart.locator('[data-action="confirm"]').click();restart.locator('.product-frame').wait_for();assert 'v1' in restart.locator('#features').inner_text();results.append('测试1重新演示：发起需求→确认→模拟生成→首版产物')
 # narrow viewport remains usable through task/work switching
 mobile=b.new_page(viewport={'width':390,'height':844});mobile.goto('http://127.0.0.1:8771/report_v17/demo/autoclaw_task2_v18/index.html');mobile.locator('[data-mobile="work"]').click();assert mobile.locator('.workspace').is_visible();mobile.locator('.work-top > .icon-btn[data-action="manager-open"]').click();assert mobile.locator('.asset-manager').is_visible();mobile.screenshot(path=str(P/'V18_窄屏产物管理.png'));results.append('390px窄屏：任务/工作区切换与文件树可操作')
 b.close()
for p in downloads.glob('*.svg'):E.parse(p)
report=json.loads((downloads/'测试2_协作评审记录.json').read_text());assert report['version']==2 and report['comments'][0]['status']=='已解决'
manifest=json.loads((downloads/'manifest_v2.json').read_text());assert manifest['version']==2
(O/'V18_交互验证.json').write_text(json.dumps({'passed':results,'page_errors':errors,'downloads':[p.name for p in downloads.iterdir()]},ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False))
