from pathlib import Path
import xml.etree.ElementTree as E
from copy import deepcopy
from html import escape
import zipfile
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'output/autoclaw_main_screens_v17'; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
def tag(n):return '{'+NS+'}'+n
def el(n,**a):return E.Element(tag(n),{k.replace('_','-'):str(v) for k,v in a.items()})
def rect(g,x,y,w,h,fill='#fff',r=0,stroke=None):
 a=dict(x=x,y=y,width=w,height=h,fill=fill,rx=r)
 if stroke:a.update(stroke=stroke,stroke_width=.8)
 g.append(el('rect',**a))
def txt(g,x,y,s,size=14,color='#333',weight=400):
 t=el('text',x=x,y=y,font_family='PingFang SC, sans-serif',font_size=size,fill=color,font_weight=weight);t.text=s;g.append(t)
def line(g,x,y,x2,y2,c='#eee'):g.append(el('path',d=f'M{x} {y}H{x2}' if y==y2 else f'M{x} {y}L{x2} {y2}',stroke=c,stroke_width=.8))
def icon(g,name,x,y,size=18,color='#777'):
 p=ROOT/'output/autoclaw_native_icons_v06/02_应用内Lucide'/f'{name}.svg'
 if not p.exists():
  aliases={'folder-closed':'folder','code-xml':'file-code','list':'task-list','sliders-horizontal':'sliders','download':'export'}
  name=aliases.get(name,name)
  p=ROOT/'output/autoclaw_native_icons_v06/01_AutoClaw自定义'/f'{name}.svg'
 if not p.exists():
  paths={'file-code':'M8 6 3 12l5 6m8-12 5 6-5 6M14 3l-4 18','task-list':'M9 6h12M9 18h12M3 5h2v2H3zM3 17h2v2H3z','export':'M12 3v12m-4-4 4 4 4-4M4 10v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9','mouse-pointer-2':'m4 3 7 18 2-8 8-2Z','type':'M4 4h16M12 4v16M8 20h8','hand':'M8 12V5a2 2 0 0 1 4 0v7-8a2 2 0 0 1 4 0v8-5a2 2 0 0 1 4 0v8c0 4-3 7-7 7-3 0-5-2-7-5L3 13a2 2 0 0 1 3-2l2 2','scan':'M8 3H3v5m13-5h5v5M3 16v5h5m8 0h5v-5'}
  if name not in paths:return
  v=el('svg',viewBox='0 0 24 24',fill='none',stroke=color,stroke_width=1.6,stroke_linecap='round',stroke_linejoin='round');v.append(el('path',d=paths[name]))
 else:v=E.parse(p).getroot()
 v.attrib.update(x=str(x),y=str(y),width=str(size),height=str(size),color=color)
 for q in v.iter():
  for k,val in list(q.attrib.items()):
   if val=='currentColor' or (k=='stroke' and val!='none'):q.set(k,color)
 g.append(v)
def button(g,x,y,w,label,dark=False):
 rect(g,x,y,w,30,'#292929' if dark else '#fff',7,None if dark else '#e7e7e7');txt(g,x+12,y+20,label,12,'#fff' if dark else '#333')
def group(g,name):q=el('g',id=name);g.append(q);return q
base=E.parse(ROOT/'output/autoclaw_unified_v08/screens/02_任务执行_代码与项目文件_统一规范.svg').getroot()
def shell(task):
 r=el('svg',width=1512,height=945,viewBox='0 0 1512 945');t=el('title');t.text=f'测试{task} · 保留AutoClaw产品结构';r.append(t)
 rect(r,0,0,1512,945,'#f7f7f7');rect(r,280,0,1232,945,'#fff',16)
 s=deepcopy(base.find("{*}g[@id='Sidebar']"))
 for t in s.iter(tag('text')):
  if t.text=='矢量界面设计':t.text='AutoClaw 首页设计' if task==1 else 'AutoClaw 首页评审'
 r.append(s);line(r,700,0,700,945,'#e8e8e8')
 q=group(r,'任务对话_保留原产品结构');icon(q,'folder-closed',306,23);txt(q,330,35,'AutoClaw 设计...' if task==1 else 'AutoClaw 评审...',14,weight=600)
 q.append(el('circle',cx=488,cy=28,r=6,fill='#ffc333'));txt(q,485,31,'Z',7,'#fff',600);txt(q,501,34,'7,415',12);txt(q,552,34,'去购买',12,'#ff5927');rect(q,603,17,48,22,'#f7f7f7',5);txt(q,609,33,'非会员',12,'#777');icon(q,'list',674,21,17)
 txt(q,457,128,'今天 · 设计稿 v1 已生成' if task==1 else '今天 · 首页 v1 评审中',12,'#aaa')
 rect(q,340,155,336,88,'#f0f0ee',22)
 lines=['按现有 AutoClaw 规范生成任务首页，','保留矢量与文字，后续继续局部修改。'] if task==1 else ['邀请产品与前端评审 AutoClaw 首页 v1，','建议固定到版本与对象，由我确认采纳。']
 for i,s in enumerate(lines):txt(q,357,184+i*24,s,14)
 rect(q,304,283,28,28,'#f0f6ff',8);txt(q,312,303,'A',16,'#1677ff',600);txt(q,344,303,'Design Agent',14,weight=600)
 ls=['已按现有规范生成首页 SVG 设计稿 v1。','在画布选中输入卡片，调整参数后生成候选。'] if task==1 else ['已固定首页 v1，收到产品与前端的建议。','点击头像查阅，创建候选并对比后确认采纳。']
 for i,s in enumerate(ls):txt(q,304,348+i*24,s,14)
 checks=['已确认视觉规范与画布尺寸','已生成 SVG 与独立文字层','已打开画布 · 选中输入卡片'] if task==1 else ['已固定评审版本 v1','已邀请产品经理、前端工程师','已收到 2 条协作建议']
 for i,s in enumerate(checks):icon(q,'check',305,407+i*31,15,'#35a764');txt(q,331,419+i*31,s,13,'#888')
 rect(q,304,512,372,156,'#fff',12,'#e7e7e7');icon(q,'code-xml',322,533,20,'#1677ff');txt(q,355,550,'AutoClaw 首页 · 设计产物',14,weight=500)
 txt(q,322,582,'工作版 v1' if task==1 else '评审版本 v1',13,'#888');txt(q,322,607,'SVG · 1512 × 945 · 可继续修改' if task==1 else 'SVG · 2 条建议 · 版本固定 v1',12,'#999');line(q,322,622,658,622)
 txt(q,322,647,'打开 Design 工作区',13,'#1677ff');icon(q,'arrow-up-right',468,634,16,'#1677ff');txt(q,546,647,'查看 SVG',12,'#888')
 txt(q,304,704,'当前：选中修改 → 候选对比 → 采纳 → 定稿' if task==1 else '当前：查阅建议 → 修改候选 → 采纳 → 解决',12,'#999')
 cp=group(r,'原生输入框');rect(cp,304,802,372,106,'#fff',26,'#e7e7e7');txt(cp,320,836,'输入“/”使用技能',13,'#aaa');icon(cp,'plus',320,873,17);icon(cp,'shield-check',363,873,17);txt(cp,385,887,'默认权限',12,'#888');icon(cp,'chevron-down',441,878,12);icon(cp,'git-fork',482,875,15);txt(cp,502,887,'Agent',12,'#888');txt(cp,566,887,'Auto',12);icon(cp,'chevron-down',597,878,12);cp.append(el('circle',cx=648,cy=881,r=16,fill='#bfbfbf'));icon(cp,'arrow-up',638,871,20,'#fff');txt(cp,401,930,'内容由 AI 生成，请核实关键信息',11,'#999')
 q=group(r,'产物窗口_原生顶部');rect(q,710,15,240,28,'#f7f7f7',8);icon(q,'code-xml',721,21,17);txt(q,745,34,'AutoClaw 首页 · Design 工作区',13,weight=500);icon(q,'plus',968,21,18);icon(q,'maximize-2',1445,22,16);icon(q,'x',1480,21,17)
 tabs=[(724,'成果',False),(801,'预览与编辑',task==1),(917,'版本与交付',False),(1034,'协作建议',task==2)]
 for x,s,on in tabs:
  txt(q,x,78,s,13,'#1677ff' if on else '#777')
  if on:line(q,x,89,x+len(s)*13,89,'#1677ff')
 rect(q,755,62,18,17,'#f5f5f5',8);txt(q,761,74,'1',10,'#999');rect(q,1092,62,18,17,'#f0f6ff',8);txt(q,1098,74,'2',10,'#1677ff')
 txt(q,1340,77,'桌面',12,'#888');icon(q,'chevron-down',1371,65,13);txt(q,1400,77,'打开',12,'#777');icon(q,'chevron-down',1431,65,13);icon(q,'download',1468,63,18);icon(q,'folder-closed',1493,65,15);line(q,700,90,1512,90)
 return r

def canvas(r,task):
 q=group(r,'产物内画布');rect(q,700,91,812,814,'#fafafa')
 rect(q,700,91,812,47,'#fff');txt(q,720,120,'AutoClaw任务首页.svg',13,weight=500);rect(q,862,103,49,22,'#f5f5f5',5);txt(q,872,118,'v1',11,'#777')
 txt(q,929,120,'画布',12,'#1677ff');txt(q,974,120,'代码',12,'#888');icon(q,'zoom-out',1188,107,17);txt(q,1216,120,'42%',12,'#777');icon(q,'zoom-in',1251,107,17);icon(q,'scan',1280,107,17);line(q,700,138,1512,138)
 # preview artboard remains entirely editable vector
 art=E.parse(ROOT/'output/autoclaw_unified_v08/screens/01_任务首页_统一规范.svg').getroot();art.attrib.update(x='720',y='264',width='556',height='347.5');art.set('id','首页设计稿_独立图层与文字');q.append(art)
 txt(q,720,247,'Desktop · 1512 × 945',11,'#aaa')
 if task==1:
  # selected composer on scaled homepage
  rect(q,908,404,282,52,'none',10,'#1677ff')
  for x,y in [(908,404),(1190,404),(908,456),(1190,456)]:rect(q,x-2,y-2,4,4,'#fff',0,'#1677ff')
 else:
  for x,y,name,c in [(1003,367,'P','#7184a9'),(1179,440,'F','#a282b2')]:
   q.append(el('circle',cx=x,cy=y,r=15,fill=c,stroke='#fff',stroke_width=3));txt(q,x-4,y+5,name,12,'#fff',600)
 tool=group(r,'画布底部工具栏');rect(tool,875,845,230,42,'#fff',12,'#e5e5e5');rect(tool,881,851,30,30,'#292929',8);icon(tool,'mouse-pointer-2',887,857,18,'#fff');icon(tool,'chevron-down',920,860,13);icon(tool,'type',949,856,21);icon(tool,'message-square-plus',990,856,21,'#1677ff' if task==2 else '#333');line(tool,1027,854,1027,878);icon(tool,'plus',1046,856,21);icon(tool,'hand',1077,857,19)
 q=group(r,'原生底部版本入口');rect(q,700,905,812,40,'#fff');line(q,724,905,1488,905);txt(q,724,930,'当前查看 v1',11,'#999');txt(q,1360,930,'查看版本记录',11,'#888');icon(q,'arrow-up-right',1470,918,14)

def panel(r,task):
 q=group(r,'对象参数' if task==1 else '修改与产物版本记录');rect(q,1300,138,212,767,'#fff');line(q,1300,138,1300,905,'#e9e9e9')
 if task==1:
  txt(q,1318,169,'Intelligent UI',14,weight=600);txt(q,1318,195,'输入卡片',12,'#999');line(q,1318,211,1494,211)
  txt(q,1318,241,'布局',12,'#888');txt(q,1318,270,'宽度',12);rect(q,1398,249,96,30,'#fafafa',6,'#e9e9e9');txt(q,1410,269,'768',12);txt(q,1472,269,'px',11,'#aaa')
  txt(q,1318,309,'圆角',12);rect(q,1398,289,96,30,'#fafafa',6,'#e9e9e9');txt(q,1410,309,'26',12);txt(q,1472,309,'px',11,'#aaa')
  txt(q,1318,348,'内边距',12);rect(q,1398,328,96,30,'#fafafa',6,'#e9e9e9');txt(q,1410,348,'20',12);txt(q,1472,348,'px',11,'#aaa');line(q,1318,381,1494,381)
  txt(q,1318,412,'外观',12,'#888');rect(q,1318,433,16,16,'#fff',4,'#ddd');txt(q,1345,446,'FFFFFF',12);txt(q,1318,483,'边框',12);txt(q,1422,483,'1 px',12,'#888')
  button(q,1318,522,176,'生成局部候选',True);txt(q,1318,574,'修改记录',12,'#888');txt(q,1318,603,'暂无修改',12,'#aaa');line(q,1318,625,1494,625);txt(q,1318,656,'产物版本',12,'#888');rect(q,1310,673,194,58,'#f7f7f7',8);txt(q,1322,695,'v1 · 工作版',12);txt(q,1322,716,'任务首页初稿',11,'#aaa')
 else:
  txt(q,1318,170,'记录',13,weight=600);txt(q,1384,170,'参数',13,'#999');icon(q,'sliders-horizontal',1475,155,17);line(q,1318,188,1494,188)
  txt(q,1318,219,'修改记录',12,'#888');txt(q,1318,249,'2 条建议待处理',12);txt(q,1318,273,'尚未采纳修改',11,'#aaa');line(q,1318,296,1494,296)
  txt(q,1318,328,'产物版本',12,'#888');rect(q,1310,345,194,66,'#f7f7f7',8);txt(q,1322,369,'v1 · 工作版',12);txt(q,1322,392,'当前评审版本',11,'#aaa');txt(q,1318,448,'评审活动',12,'#888');txt(q,1318,478,'产品经理添加了建议',11);txt(q,1318,499,'10 分钟前 · 首屏标题',10,'#aaa');txt(q,1318,534,'前端工程师添加了建议',11);txt(q,1318,555,'5 分钟前 · 输入卡片',10,'#aaa');button(q,1318,602,176,'邀请协作')
  # contextual bubble, only place long review copy here
  b=group(r,'头像展开的评审气泡');rect(b,997,391,286,242,'#fff',12,'#e0e0e0');b.append(el('circle',cx=1024,cy=418,r=12,fill='#7184a9'));txt(b,1020,423,'P',11,'#fff');txt(b,1045,422,'产品经理',13,weight=500);txt(b,1215,422,'待处理',11,'#999');txt(b,1014,449,'v1 · 首页 · 首屏标题',11,'#aaa');line(b,1014,462,1266,462)
  for i,s in enumerate(['建议将首页标题改为：','“和 AutoClaw 一起高效工作”，','让任务入口的用途更清晰。']):txt(b,1014,486+i*21,s,13)
  txt(b,1014,558,'10 分钟前',10,'#aaa');line(b,1014,573,1266,573);button(b,1014,588,112,'创建修改候选',True);txt(b,1150,608,'回复',12,'#888');icon(b,'ellipsis',1240,592,18)
for task in [1,2]:
 r=shell(task);canvas(r,task);panel(r,task)
 name=f'测试{task}_'+('预览与编辑主界面' if task==1 else '协作评审主界面')+'_V17.svg';E.ElementTree(r).write(OUT/name,encoding='unicode')
(OUT/'README.md').write_text('''# AutoClaw 两张主任务界面 V16

以用户提供的 Figma 530:12283 和截图为结构基准。保留 280px 侧栏、420px 任务对话、812px 产物窗口。侧栏导航与底部账户、任务输入框、原生窗口标题及「桌面 / 打开 / 下载 / 项目文件」入口保持原产品构成。新增设计链路仅放入右侧产物窗口。

- 测试1：预览与编辑，画布选中输入卡片，右侧 Intelligent UI 参数；生成局部候选后走对比、采纳与版本链路。
- 测试2：协作建议，画布头像与展开气泡；右侧只展示简要修改记录、版本记录及参数入口。对应独立评审任务。

两张为静态设计稿，不改动 V15 交互演示。新增链路状态尚未同步到 HTML，待用户调整确认后再同步。

1512 × 945；独立文字和矢量分组；原用户头像为嵌入位图，其余界面为矢量。SVG 导入 Figma 可能将文字转为路径；不含原生组件/自动布局语义。

Figma 首次读取返回结构信息，后续读取触发 Starter 调用额度限制；最终依据附图及现有规范完成。
''')
print(OUT)
