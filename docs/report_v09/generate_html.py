from pathlib import Path
from html import escape
from markdown import Markdown

ROOT = Path(__file__).parent
OUT = ROOT / "2026-10-05_AutoClaw_Design工作区_方案汇报_V09.html"
MD = ROOT / "2026-10-05_AutoClaw_Design工作区_方案汇报_V09.md"
PROTO = ROOT.parent / "prototype_v08"
slides = sorted(ROOT.glob("[0-9][0-9]_*.svg"))
assert len(slides) == 12, f"Expected 12 SVG slides, found {len(slides)}"

titles = [
    "封面", "思路演化", "研究证据", "共创旅程", "草图三态", "痛点排序",
    "界面定域修订", "评审节奏", "信息架构", "原型链路", "MVP 边界", "验证计划",
]
svg_sections = []
sidebar_items = []
for i, (path, title) in enumerate(zip(slides, titles), 1):
    svg = path.read_text(encoding="utf-8")
    svg_sections.append(
        f'<section class="slide{(" active" if i == 1 else "")}" data-slide="{i}" '
        f'aria-label="第 {i} 页：{escape(title)}">{svg}</section>'
    )
    sidebar_items.append(
        f'<button class="slide-link{(" active" if i == 1 else "")}" data-goto="{i}" '
        f'aria-label="查看第 {i} 页 {escape(title)}"><span class="number">{i:02d}</span>'
        f'<span>{escape(title)}</span></button>'
    )

md = Markdown(extensions=["tables", "fenced_code", "toc"])
article_html = md.convert(MD.read_text(encoding="utf-8"))
toc_html = md.toc
prototype_html = (PROTO / "index.html").read_text(encoding="utf-8")
prototype_css = (PROTO / "styles.css").read_text(encoding="utf-8")
prototype_css += """
#mobile-design-entry{display:none}
@media(max-width:780px){
  .top-actions{display:none}
  .breadcrumbs{margin-top:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .workspace{padding:0 15px 24px}
  .workspace-tabs{gap:20px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}
  .workspace-tabs button{flex:none;font-size:13px}
  .page-head{display:block;margin:20px 0 15px}
  .page-head h1{font-size:22px}
  .page-head>.pill{display:inline-block;margin-top:12px}
  .pills{flex-wrap:wrap}
  .app-main:has(.home) #mobile-design-entry{display:block;position:absolute;top:77px;left:20px;z-index:5;border:1px solid #a6d5cb;background:#e5f4f0;color:#167b72;border-radius:8px;padding:10px 14px;font-size:13px;font-weight:600}
}
"""
prototype_js = (PROTO / "app.js").read_text(encoding="utf-8")
prototype_html = prototype_html.replace('<main id="main" tabindex="-1"></main>', '<button id="mobile-design-entry" data-action="overview">打开「邀请成员流程」设计任务 →</button><main id="main" tabindex="-1"></main>')
prototype_html = prototype_html.replace('<link rel="stylesheet" href="./styles.css">', f'<style>{prototype_css}</style>')
prototype_html = prototype_html.replace('<script src="./app.js"></script>', f'<script>{prototype_js}</script>')
assert './styles.css' not in prototype_html and './app.js' not in prototype_html

html = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>AutoClaw Design 工作区 · 方案汇报 V09</title>
  <style>
    :root{--ink:#17383b;--muted:#60716f;--teal:#12877d;--line:#dbe5e0;--surface:#fff;--bg:#eef3f0;--shadow:0 15px 50px rgba(18,45,49,.10)}
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;background:var(--bg);color:var(--ink);font-family:"PingFang SC","Noto Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    button{font:inherit;cursor:pointer}
    .app{min-height:100vh;display:grid;grid-template-rows:64px minmax(0,1fr)}
    .topbar{background:var(--surface);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:24px;padding:0 24px;position:sticky;top:0;z-index:20}
    .brand{display:flex;align-items:center;gap:12px;min-width:310px;font-size:15px;font-weight:700;white-space:nowrap}
    .brand-mark{width:28px;height:28px;background:var(--teal);color:#fff;display:grid;place-items:center;border-radius:7px;font-weight:800}
    .brand small{font-size:11px;font-weight:600;color:var(--muted);padding:4px 7px;border:1px solid var(--line);border-radius:5px}
    .view-tabs{display:flex;align-items:center;background:#f0f4f2;border:1px solid var(--line);padding:3px;border-radius:8px;gap:3px}
    .view-tabs button{border:0;background:none;padding:7px 13px;border-radius:5px;font-size:13px;color:var(--muted);font-weight:600}
    .view-tabs button.active{background:#fff;color:var(--ink);box-shadow:0 1px 4px rgba(0,0,0,.08)}
    .top-spacer{flex:1}
    .top-hint{font-size:12px;color:var(--muted);white-space:nowrap}
    .layout{display:grid;grid-template-columns:230px minmax(0,1fr);min-height:calc(100vh - 64px)}
    aside{background:var(--surface);border-right:1px solid var(--line);position:sticky;top:64px;align-self:start;height:calc(100vh - 64px);overflow:auto;padding:23px 13px 25px}
    .side-heading{font-size:11px;letter-spacing:.06em;color:#82918d;font-weight:700;padding:0 12px;margin-bottom:12px}
    .slide-list,.doc-list{display:flex;flex-direction:column;gap:3px}
    .slide-link{display:flex;align-items:center;width:100%;text-align:left;border:0;background:transparent;border-radius:6px;padding:10px 12px;color:#445b58;font-size:13px;gap:12px}
    .slide-link:hover,.slide-link.active{background:#e7f3ef;color:#0e7069}
    .slide-link.active{font-weight:700}
    .number{font-variant-numeric:tabular-nums;font-size:11px;color:#83a6a0;width:22px}
    .doc-list{font-size:12px;line-height:1.55}
    .doc-list ul{list-style:none;padding-left:0;margin:0}
    .doc-list ul ul{padding-left:14px}
    .doc-list a{display:block;text-decoration:none;color:#4d6461;padding:7px 12px;border-radius:5px}
    .doc-list a:hover{background:#e7f3ef;color:#0e7069}
    .demo-guide{display:none;padding:4px 12px;color:#4d6461;font-size:12px;line-height:1.75}
    .demo-guide p{margin:8px 0 14px}
    .demo-guide ol{padding-left:18px;margin:0 0 18px}
    .demo-guide li{margin-bottom:9px}
    .demo-guide a{color:#087b72;text-underline-offset:3px}
    .side-note{border-top:1px solid var(--line);margin:22px 9px 0;padding-top:15px;font-size:11px;line-height:1.7;color:#83918e}
    .main{min-width:0;padding:19px 28px 26px}
    .toolbar{max-width:1380px;margin:0 auto 15px;display:flex;align-items:center;gap:10px;min-height:38px}
    .eyebrow{font-size:13px;font-weight:700;color:var(--ink)}
    .count{font-size:12px;color:var(--muted);margin-left:8px}
    .toolbar-spacer{flex:1}
    .toolbar button,.bottom-nav button{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:6px;padding:8px 12px;font-size:12px;font-weight:600}
    .toolbar button:hover,.bottom-nav button:hover{border-color:#9fc8be;background:#f6fbf9}
    .toolbar button:disabled,.bottom-nav button:disabled{opacity:.35;cursor:default}
    .mobile-select{display:none;border:1px solid var(--line);padding:7px;border-radius:6px;background:#fff;color:var(--ink);max-width:180px}
    .slide-stage{max-width:1380px;margin:auto;background:#fff;box-shadow:var(--shadow);border:1px solid #dce5e1;overflow:auto}
    .slide-stage.zoomed .slide svg{width:max(100%,min(1600px,220vw));max-width:none}
    .slide{display:none}
    .slide.active{display:block}
    .slide svg{display:block;width:100%;height:auto;aspect-ratio:16/9}
    .bottom-nav{max-width:1380px;margin:15px auto 0;display:flex;align-items:center;gap:10px}
    .progress{height:4px;background:#d8e5df;flex:1;max-width:250px;border-radius:3px;overflow:hidden;margin-left:auto}
    .progress span{display:block;height:100%;background:var(--teal);width:8.333%;transition:width .2s}
    .keyboard-tip{font-size:11px;color:#7b8c88}
    .doc-view{display:none;max-width:1080px;margin:0 auto;padding:14px 18px 90px;background:#fff;box-shadow:var(--shadow);border:1px solid var(--line)}
    .article{padding:25px 50px 55px;line-height:1.85;font-size:15px;color:#324b48}
    .article h1{font-size:34px;line-height:1.3;letter-spacing:0;margin:0 0 22px;color:var(--ink)}
    .article h2{font-size:23px;color:var(--ink);border-top:1px solid var(--line);padding-top:36px;margin-top:42px;line-height:1.4}
    .article h3{font-size:18px;color:var(--ink);margin-top:30px}
    .article p{margin:12px 0 17px}
    .article a{color:#087b72;text-underline-offset:3px}
    .article table{border-collapse:collapse;display:block;overflow-x:auto;width:100%;margin:22px 0;font-size:13px;line-height:1.65}
    .article th,.article td{min-width:130px;border:1px solid var(--line);padding:10px 13px;vertical-align:top}
    .article th{background:#eaf4f0;color:var(--ink);font-weight:700}
    .article tr:nth-child(even) td{background:#f8fbf9}
    .article blockquote{border-left:3px solid var(--teal);padding:4px 20px;margin-left:0;background:#f5faf8;color:#4f6562}
    .article code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef4f1;padding:1px 4px;border-radius:3px;font-size:.92em}
    .article ul{padding-left:22px}
    .demo-view{display:none;max-width:1430px;margin:0 auto;padding-bottom:48px}
    .demo-heading{display:flex;align-items:flex-start;gap:24px;justify-content:space-between;margin:3px 0 20px}
    .demo-heading h1{font-size:27px;line-height:1.3;margin:0 0 8px}
    .demo-heading p{font-size:13px;color:var(--muted);line-height:1.65;margin:0;max-width:670px}
    .demo-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}
    .demo-actions button,.demo-actions a{border:1px solid var(--line);background:#fff;color:var(--ink);text-decoration:none;border-radius:6px;padding:9px 12px;font-size:12px;font-weight:600;white-space:nowrap}
    .demo-actions button:hover,.demo-actions a:hover{border-color:#9fc8be;background:#f6fbf9}
    .demo-actions button.active{border-color:#80bfb2;background:#e3f3ed;color:#0e7069}
    .demo-shell{background:#dfe8e3;border:1px solid #cbdad3;padding:17px;display:flex;justify-content:center;overflow:auto;box-shadow:var(--shadow)}
    .demo-shell iframe{display:block;width:1365px;max-width:100%;height:851px;flex:none;border:1px solid #c7d5cf;background:#fff;box-shadow:0 5px 25px rgba(18,45,49,.14)}
    .demo-note{font-size:12px;color:#6d7e79;line-height:1.7;margin-top:11px}
    body.doc-mode .deck-view{display:none}
    body.doc-mode .doc-view{display:block}
    body.doc-mode .slide-list{display:none}
    body:not(.doc-mode) .doc-list{display:none}
    body.demo-mode .deck-view,body.demo-mode .doc-view{display:none}
    body.demo-mode .demo-view{display:block}
    body.demo-mode .slide-list,body.demo-mode .doc-list{display:none}
    body.demo-mode .demo-guide{display:block}
    .overview{position:fixed;inset:0;background:rgba(12,35,38,.84);z-index:40;display:none;overflow:auto;padding:55px 35px}
    .overview.open{display:block}
    .overview-head{max-width:1300px;margin:0 auto 20px;display:flex;align-items:center;color:#fff;justify-content:space-between}
    .overview-head h2{margin:0;font-size:22px}
    .overview-head button{border:1px solid #678481;background:transparent;color:#fff;border-radius:6px;padding:8px 12px}
    .thumb-grid{max-width:1300px;margin:auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
    .thumb{background:#fff;border:0;padding:0;text-align:left;border-radius:5px;overflow:hidden;box-shadow:0 10px 28px rgba(0,0,0,.2)}
    .thumb:hover{outline:3px solid #65c8b7}
    .thumb svg{display:block;width:100%;height:auto}
    .thumb-label{display:block;padding:8px 11px;font-size:12px;color:var(--ink);font-weight:700}
    :focus-visible{outline:2px solid var(--teal)!important;outline-offset:2px}
    @media(max-width:1050px){.brand{min-width:0}.top-hint{display:none}.layout{grid-template-columns:190px minmax(0,1fr)}.main{padding:16px}.article{padding:20px 30px}}
    @media(max-width:760px){.topbar{gap:10px;padding:0 12px}.brand{font-size:12px;gap:6px}.brand span:nth-child(2),.brand small{display:none}.view-tabs{margin-left:auto}.view-tabs button{padding:7px 8px;font-size:11px}.layout{display:block}aside{display:none}.main{padding:12px}.toolbar{gap:7px}.toolbar .eyebrow,.toolbar .count{display:none}.toolbar button{padding:7px 9px}.mobile-select{display:block}.slide-stage{border-radius:2px}.bottom-nav .keyboard-tip{display:none}.doc-view{border:0;padding:4px}.article{padding:16px;font-size:14px}.article h1{font-size:26px}.thumb-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.overview{padding:30px 12px}.demo-heading{display:block}.demo-heading h1{font-size:22px}.demo-actions{justify-content:flex-start;margin-top:13px}.demo-shell{padding:7px}.demo-shell iframe{height:760px}}
    @media print{.topbar,aside,.toolbar,.bottom-nav,.overview{display:none!important}.app,.layout{display:block}.main{padding:0}.slide-stage{border:0;box-shadow:none;max-width:none}.slide{display:block!important;break-after:page}.slide svg,.slide-stage.zoomed .slide svg{width:100%;height:auto}.doc-view{box-shadow:none;border:0;max-width:none;padding:0}.article{padding:0}body.doc-mode .deck-view{display:none!important}body:not(.doc-mode) .doc-view{display:none!important}}
  </style>
</head>
<body>
<div class="app">
  <header class="topbar">
    <div class="brand"><span class="brand-mark">A</span><span>AutoClaw · Design Agent</span><small>方案汇报 V09</small></div>
    <nav class="view-tabs" aria-label="阅读模式"><button id="tab-deck" class="active" data-mode="deck" aria-current="page">画板</button><button id="tab-doc" data-mode="doc">完整文稿</button><button id="tab-demo" data-mode="demo">设计稿 Demo</button></nav>
    <div class="top-spacer"></div><span class="top-hint">单文件 · 离线可查看</span>
  </header>
  <div class="layout">
    <aside aria-label="内容目录">
      <div class="side-heading" id="side-label">汇报画板 · 12 页</div>
      <div class="slide-list">__SIDEBAR__</div>
      <nav class="doc-list" aria-label="文稿目录">__TOC__</nav>
      <div class="demo-guide"><strong>交互演示路径</strong><p>当前采用 AutoClaw Design 工作区 V08 原型，设计源稿是同一 Figma 文件中的「03 · Design 工作区原型」。</p><ol><li>打开「邀请成员流程」</li><li>选择方向 B 并预览</li><li>文字、智能编辑或画笔圈选</li><li>比较候选并采纳</li><li>完成 G1 / G2 评审后查看交付</li></ol><a href="https://www.figma.com/design/XytIsXg4S2lL45NriFX69i/%E6%99%BA%E8%B0%B1%E6%B5%8B%E8%AF%95%E9%A2%98-2026?node-id=100-3" target="_blank" rel="noopener">打开 Figma 设计源稿 ↗</a></div>
      <div class="side-note">画板可用 ← → 翻页；按 O 打开总览。完整文稿含证据口径与来源。</div>
    </aside>
    <main class="main">
      <div class="deck-view">
        <div class="toolbar">
          <span class="eyebrow">__FIRST_TITLE__</span><span class="count" id="count">01 / 12</span>
          <select class="mobile-select" id="mobile-select" aria-label="选择汇报页">__OPTIONS__</select>
          <span class="toolbar-spacer"></span>
          <button id="overview-btn" title="查看全部页面">总览</button>
          <button id="zoom-btn" title="放大画板后可横向拖动查看">放大</button>
          <button id="fullscreen-btn" title="全屏查看画板">全屏</button>
          <button id="print-btn" title="打印或保存为 PDF">打印</button>
        </div>
        <div class="slide-stage" id="stage">__SLIDES__</div>
        <div class="bottom-nav"><button id="prev" aria-label="上一页">← 上一页</button><button id="next" aria-label="下一页">下一页 →</button><div class="progress" aria-hidden="true"><span id="progress"></span></div><span class="keyboard-tip">键盘 ← → 翻页</span></div>
      </div>
      <div class="doc-view"><article class="article">__ARTICLE__</article></div>
      <div class="demo-view">
        <div class="demo-heading"><div><h1>设计稿 Demo · AutoClaw Design 工作区</h1><p>按真实操作顺序体验一条从 AI 初稿、局部修订、概念与 Demo 评审到交付的路径。当前为可点击交互模拟，后续新增设计内容可继续接入此处。</p></div><div class="demo-actions"><button class="active" data-device="desktop">桌面</button><button data-device="mobile">手机</button><button id="reset-demo">重置演示</button><button id="fullscreen-demo">全屏体验</button><a href="https://www.figma.com/design/XytIsXg4S2lL45NriFX69i/%E6%99%BA%E8%B0%B1%E6%B5%8B%E8%AF%95%E9%A2%98-2026?node-id=100-3" target="_blank" rel="noopener">Figma 源稿 ↗</a></div></div>
        <div class="demo-shell"><iframe id="demo-frame" title="AutoClaw Design 工作区可点击原型" srcdoc="__DEMO_SRCDOC__"></iframe></div>
        <p class="demo-note">演示基于 V08 原型。局部生成、状态回归与开发交付为模拟内容；Figma 源稿新增画面不会自动同步到此演示。</p>
      </div>
    </main>
  </div>
</div>
<div class="overview" id="overview" role="dialog" aria-modal="true" aria-label="汇报画板总览">
  <div class="overview-head"><h2>汇报画板 · 12 页</h2><button id="close-overview">关闭 ×</button></div>
  <div class="thumb-grid" id="thumb-grid"></div>
</div>
<script>
(()=>{
  const titles=__TITLES_JSON__;
  const slides=[...document.querySelectorAll('.slide')];
  const links=[...document.querySelectorAll('.slide-link')];
  const overview=document.getElementById('overview');
  const grid=document.getElementById('thumb-grid');
  let current=0;
  let mode='deck';
  function go(index, hash=true){
    current=Math.max(0,Math.min(slides.length-1,index));
    slides.forEach((el,i)=>el.classList.toggle('active',i===current));
    links.forEach((el,i)=>{el.classList.toggle('active',i===current);if(i===current)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current')});
    document.querySelector('.toolbar .eyebrow').textContent=titles[current];
    document.getElementById('count').textContent=String(current+1).padStart(2,'0')+' / 12';
    document.getElementById('mobile-select').value=String(current);
    document.getElementById('prev').disabled=current===0;
    document.getElementById('next').disabled=current===slides.length-1;
    document.getElementById('progress').style.width=((current+1)/slides.length*100)+'%';
    links[current]?.scrollIntoView({block:'nearest'});
    if(hash)history.replaceState(null,'','#slide-'+String(current+1).padStart(2,'0'));
  }
  function setMode(next,hash=true){
    mode=next;
    document.body.classList.toggle('doc-mode',mode==='doc');
    document.body.classList.toggle('demo-mode',mode==='demo');
    for(const view of ['deck','doc','demo']){
      const tab=document.getElementById('tab-'+view);
      tab.classList.toggle('active',mode===view);
      tab.setAttribute('aria-current',mode===view?'page':'false');
    }
    document.getElementById('side-label').textContent=mode==='doc'?'完整文稿目录':mode==='demo'?'设计稿 Demo':'汇报画板 · 12 页';
    if(hash)history.replaceState(null,'',mode==='doc'?'#document':mode==='demo'?'#demo':'#slide-'+String(current+1).padStart(2,'0'));
    window.scrollTo({top:0,behavior:'instant'});
  }
  function openOverview(){overview.classList.add('open');document.getElementById('close-overview').focus()}
  function closeOverview(){overview.classList.remove('open');document.getElementById('overview-btn').focus()}
  slides.forEach((slide,i)=>{
    const btn=document.createElement('button');btn.className='thumb';btn.setAttribute('aria-label','查看第 '+(i+1)+' 页 '+titles[i]);
    btn.appendChild(slide.querySelector('svg').cloneNode(true));
    const label=document.createElement('span');label.className='thumb-label';label.textContent=String(i+1).padStart(2,'0')+'  '+titles[i];btn.appendChild(label);
    btn.addEventListener('click',()=>{go(i);closeOverview()});grid.appendChild(btn);
  });
  links.forEach((button,i)=>button.addEventListener('click',()=>go(i)));
  document.getElementById('prev').addEventListener('click',()=>go(current-1));
  document.getElementById('next').addEventListener('click',()=>go(current+1));
  document.getElementById('mobile-select').addEventListener('change',e=>go(Number(e.target.value)));
  document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
  document.getElementById('overview-btn').addEventListener('click',openOverview);
  document.getElementById('close-overview').addEventListener('click',closeOverview);
  overview.addEventListener('click',e=>{if(e.target===overview)closeOverview()});
  document.getElementById('zoom-btn').addEventListener('click',()=>{const stage=document.getElementById('stage');const on=stage.classList.toggle('zoomed');document.getElementById('zoom-btn').textContent=on?'还原':'放大';stage.scrollTo({left:0,top:0,behavior:'instant'})});
  document.getElementById('fullscreen-btn').addEventListener('click',async()=>{if(document.fullscreenElement)await document.exitFullscreen();else await document.getElementById('stage').requestFullscreen()});
  document.getElementById('print-btn').addEventListener('click',()=>window.print());
  const demoFrame=document.getElementById('demo-frame');
  document.querySelectorAll('[data-device]').forEach(button=>button.addEventListener('click',()=>{
    const isMobile=button.dataset.device==='mobile';
    demoFrame.style.width=isMobile?'390px':'1365px';
    document.querySelectorAll('[data-device]').forEach(b=>b.classList.toggle('active',b===button));
  }));
  document.getElementById('reset-demo').addEventListener('click',()=>{demoFrame.srcdoc=demoFrame.getAttribute('srcdoc')});
  document.getElementById('fullscreen-demo').addEventListener('click',async()=>{if(document.fullscreenElement)await document.exitFullscreen();else await demoFrame.requestFullscreen()});
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'&&overview.classList.contains('open')){closeOverview();return}
    if(e.target.matches('input,textarea,select'))return;
    if(mode!=='deck'||overview.classList.contains('open'))return;
    if(e.key==='ArrowRight'){e.preventDefault();go(current+1)}
    if(e.key==='ArrowLeft'){e.preventDefault();go(current-1)}
    if(e.key.toLowerCase()==='o'){e.preventDefault();openOverview()}
  });
  const initial=location.hash.match(/^#slide-(\d{1,2})$/);
  if(location.hash==='#document')setMode('doc',false);else if(location.hash==='#demo')setMode('demo',false);else go(initial?Number(initial[1])-1:0,false);
})();
</script>
</body>
</html>'''
html = html.replace("__SIDEBAR__", "".join(sidebar_items))
html = html.replace("__TOC__", toc_html)
html = html.replace("__SLIDES__", "".join(svg_sections))
html = html.replace("__ARTICLE__", article_html)
html = html.replace("__DEMO_SRCDOC__", escape(prototype_html, quote=True))
html = html.replace("__FIRST_TITLE__", titles[0])
html = html.replace("__OPTIONS__", "".join(f'<option value="{i}">{i+1:02d} · {escape(t)}</option>' for i, t in enumerate(titles)))
import json
html = html.replace("__TITLES_JSON__", json.dumps(titles, ensure_ascii=False))
OUT.write_text(html, encoding="utf-8")
((ROOT / "index.html")).write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
