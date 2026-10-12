from pathlib import Path
import re,xml.etree.ElementTree as E,json
P=Path('output/autoclaw_task1_v13');N='http://www.w3.org/2000/svg';E.register_namespace('',N)
r=E.parse('output/autoclaw_unified_v08/screens/01_任务首页_统一规范.svg').getroot()
lib=Path('output/autoclaw_native_icons_v06')
for par in r.iter():
 for el in list(par):
  if el.tag!='{'+N+'}image':continue
  id=el.get('id','');x=float(el.get('x',0));y=float(el.get('y',0));w=float(el.get('width',20));h=float(el.get('height',20));index=list(par).index(el)
  if 'avatar' in id.lower():new=E.Element('{'+N+'}circle',dict(cx=str(x+w/2),cy=str(y+h/2),r=str(min(w,h)/2),fill='#ebebeb'))
  elif 'Credits' in id:new=E.Element('{'+N+'}circle',dict(cx=str(x+w/2),cy=str(y+h/2),r=str(min(w,h)/2),fill='#ffc02b'))
  else:
   name='office' if 'office' in id else 'code-terminal' if 'code' in id else 'law' if 'law' in id else 'skills'
   f=lib/'01_AutoClaw自定义'/f'{name}.svg'
   if not f.exists():f=lib/'02_应用内Lucide/scale.svg'
   new=E.parse(f).getroot();new.set('x',str(x));new.set('y',str(y));new.set('width',str(w));new.set('height',str(h))
  par.remove(el);par.insert(index,new)
(P/'assets/base-artifact.svg').write_text(E.tostring(r,encoding='unicode'))
s=Path('output/autoclaw_design_flow_v12/index.html').read_text();s=re.sub(r'<script>[\s\S]*?</script>','<script src="task1.js"></script>',s,count=1)
s=s.replace('app.css','base.css').replace('</head>','<link rel="stylesheet" href="task1.css"></head>').replace('AutoClaw · 设计链路交互 Demo V12','测试1 · AutoClaw 设计产物链路')
s=s.replace('AI 产品官网设计','测试1 · 矢量界面设计').replace('Design Agent 测试题','Design Agent 测试题').replace('<button class="nav-item" data-action="nav-info">创业融资方案</button>','<a class="nav-item task-path" href="../autoclaw_design_flow_v12/index.html">测试2 · 协作建议（独立任务）</a>')
s=s.replace('<button class="nav-item" data-action="nav-info">红色蝴蝶结</button>','<a class="nav-item task-path" href="../autoclaw_presentation_v13/index.html">返回演示目录</a>')
s=s.replace('<button class="text-btn" data-action="open-overview">产物 <span class="count">5</span></button>','<span>设计产物</span>')
s=s.replace('data-action="send-message"','data-action="send"').replace('aria-label="向 Agent 描述修改要求"','aria-label="描述设计需求或局部修改"')
a=s.index('  <section class="workspace"');b=s.index('  <div class="mobile-switch"',a)
s=s[:a]+'''<section class="workspace" aria-label="测试1设计产物工作区"><div class="artifact-top"><span class="artifact-tab"><img class="ui-icon" src="assets/file-code.svg" alt="">AutoClaw界面_设计产物.svg</span><span class="spacer"></span><span class="local-label">测试1 · 本地模拟</span><button class="icon-btn" data-action="reset" aria-label="重置测试1"><img class="ui-icon" src="assets/refresh-cw.svg" alt=""></button></div><div class="work-top"><div class="work-tabs" role="tablist"><button data-tab="canvas">画布</button><button data-tab="code">代码</button><button data-tab="layers">图层</button><button data-tab="versions">版本</button></div><span class="spacer"></span><button class="text-btn export" data-action="export"><img class="ui-icon" src="assets/custom-063-gtn.svg" alt="">导出</button></div><div class="guide-row"><span id="step-count"></span><strong id="step-name"></strong><span class="spacer"></span><button class="outline" data-action="next" id="next-step"></button></div><div class="task1-body"><div class="work-main" id="main"></div><aside class="feature-panel" id="features" aria-label="设计功能"></aside></div></section>\n'''+s[b:]
s=s.replace('data-action="open-overview"','data-action="reset"');s=s.replace('../autoclaw_design_flow_v12/index.html','../autoclaw_task2_v13/index.html')
s=s.replace('<script src="task1.js"></script>','<script id="artifact-source" type="application/json">'+json.dumps((P/'assets/base-artifact.svg').read_text()).replace('</','<\\/')+'</script><script src="task1.js"></script>')
s=s.replace('</body>','<script src="nav-route.js"></script></body>')
(P/'index.html').write_text(s)
