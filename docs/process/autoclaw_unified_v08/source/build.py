from pathlib import Path
import xml.etree.ElementTree as E,base64,html,json,io,zipfile
from PIL import Image
P=Path('output/autoclaw_unified_v08');L=Path('output/autoclaw_native_icons_v06');V4=Path('output/autoclaw_line_icons_v04');N='http://www.w3.org/2000/svg';E.register_namespace('',N)
for d in ['screens','previews','figma-editable-import']:(P/d).mkdir(exist_ok=True)
refs=[Image.open('/var/folders/9z/bdrtng4j073554bq2s5wrbb00000gn/T/codex-clipboard-1b7b6411-09a6-44ed-896a-f4820f39b35d.png').resize((1512,945)),Image.open('/var/folders/9z/bdrtng4j073554bq2s5wrbb00000gn/T/codex-clipboard-82a8b9a3-b787-48b4-aae5-ebaa528a9fa0.png').resize((1512,945))]
custom={'task':'task','agent':'agent','sidebar':'sidebar','view':'view','search':'search','new':'new-task','skills':'skills','folder-add':'folder-add','edit':'edit','folder':'custom-066-d7e','cluster':'cluster','platform':'platform','close':'close','chevron':'chevron-down','right':'chevron-right','file':'custom-061-XJt','export':'custom-063-gtn'}
class S:
 def __init__(self,name,ref):self.name=name;self.ref=ref;self.a=[];self.texts=[];self.a.append('<defs><filter id="soft" x="-20%" y="-70%" width="140%" height="240%"><feDropShadow dx="0" dy="10" stdDeviation="20" flood-color="#1f1f1f" flood-opacity=".055"/></filter></defs>');self.rect(0,0,1512,945,'#f7f7f7');self.rect(280,0,1232,945,'#fff',16)
 def group(self,n):self.a.append('<g id="'+n+'">')
 def end(self):self.a.append('</g>')
 def rect(self,x,y,w,h,c='#fff',r=0,stroke=None,shadow=False):self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"'+(f' stroke="{stroke}" stroke-width=".7"' if stroke else '')+(' filter="url(#soft)"' if shadow else '')+'/>')
 def line(self,x,y,x2,y2,c='#eee'):self.a.append(f'<path d="M{x} {y}L{x2} {y2}" stroke="{c}" stroke-width=".7"/>')
 def text(self,x,y,t,size=14,c='#333333',weight=400,font='PingFang SC'):
  self.a.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{c}">{html.escape(t)}</text>');self.texts.append(dict(x=x,y=y,text=t,size=size,color=c,weight=weight,font=font))
 def icon(self,name,x,y,w=20,h=None,c='#666'):
  if name=='file':f=V4/'svg/file-code.svg'
  elif name=='maximize-2':f=V4/'svg/fullscreen.svg'
  elif name in custom:f=L/'01_AutoClaw自定义'/(custom[name]+'.svg')
  else:f=L/'02_应用内Lucide'/(name+'.svg')
  r=E.parse(f).getroot();r.set('x',str(x));r.set('y',str(y));r.set('width',str(w));r.set('height',str(h or w))
  for el in r.iter():
   for k in ['fill','stroke']:
    if el.get(k)=='#333333':el.set(k,c)
  self.a.append('<g id="icon-'+name+'-'+str(len(self.a))+'">'+E.tostring(r,encoding='unicode')+'</g>')
 def image(self,im,x,y,w,h,label):
  b=io.BytesIO();im.save(b,format='PNG');self.a.append(f'<image id="{label}" x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
 def arrow(self,x,y,c='#fff'):self.a.append(f'<path d="M{x+8} {y+15}V{y+1}m-5 5 5-5 5 5" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
 def save(self):
  head='<svg xmlns="http://www.w3.org/2000/svg" width="1512" height="945" viewBox="0 0 1512 945">';svg=head+''.join(self.a)+'</svg>';f=P/'screens'/(self.name+'.svg');f.write_text(svg);E.fromstring(svg)
  # Native-text import companion removes SVG text so Figma gets real text nodes.
  r=E.fromstring(svg)
  for parent in r.iter():
   for child in list(parent):
    if child.tag=='{'+N+'}text':parent.remove(child)
  (P/'figma-editable-import'/(self.name+'.json')).write_text(json.dumps({'name':self.name,'width':1512,'height':945,'svg':E.tostring(r,encoding='unicode'),'texts':self.texts},ensure_ascii=False))
def sidebar(s,selected=False):
 s.group('Sidebar');s.icon('sidebar',86,19,20);s.rect(14,56,66,32,'#ebebeb',16);s.icon('task',20,62,20);s.text(44,77,'任务');s.icon('agent',86,62,20);s.text(112,77,'智能体');s.icon('view',218,62,20);s.icon('search',244,62,20)
 s.rect(10,110,260,34,'#ebebeb',8);s.icon('new',18,117,20);s.text(44,131,'新建任务');s.text(226,130,'⌘',11,'#888');s.text(249,130,'N',10,'#888');s.icon('skills',18,153,20);s.text(44,167,'Skill & 连接器')
 s.text(18,214,'项目',13,'#888');s.icon('right',48,201,18,c='#999');s.icon('folder-add',242,200,20,c='#888');s.text(18,255,'任务',13,'#888');s.icon('chevron',44,238,24,c='#888');s.icon('edit',242,240,20,c='#888')
 if selected:s.rect(10,271,260,30,'#ebebeb',8)
 for y,t in [(291,'矢量界面设计'),(323,'创业融资方案'),(355,'红色蝴蝶结')]:s.text(18,y,t)
 if selected:s.icon('loader-circle',245,280,14,c='#bfbfbf')
 s.image(s.ref.crop((17,903,43,931)),17,903,26,28,'User-avatar');s.text(50,922,'182****89...');s.text(146,922,'Coding Plan');s.rect(230,909,30,17,'#555',3);s.text(233,922,'1.5X',11,'#fff');s.end()
def credits(s,x,value):
 # Original token artwork from screenshot, kept as a small embedded asset.
 s.image(refs[0].crop((1303,19,1320,36)),x,20,15,15,'Credits-token');s.text(x+23,34,value);s.text(x+77,34,'去购买',14,'#ff5927');s.rect(x+128,17,48,22,'#f7f7f7',5);s.text(x+134,33,'非会员',13,'#777')
def composer(s,x,y,w,h,home=False):
 s.group('Composer')
 if home:s.rect(x+16,y+h-5,w-32,51,'#f6f6f6',20);s.icon('folder',x+35,y+h+13,17);s.text(x+60,y+h+28,'默认项目',14,'#666');s.icon('chevron',x+116,y+h+10,24)
 s.rect(x,y,w,h,'#fff',25,'#e9e9e9',True);s.text(x+16,y+34,'输入“/”使用技能',14,'#a3a3a3');by=y+h-34
 s.icon('plus',x+18,by+2,15,c='#333');s.icon('shield-check',x+60,by+1,15,c='#8b8b8b');s.text(x+78,by+14,'默认权限',14,'#999');s.icon('chevron',x+132,by-2,24,c='#999');s.icon('cluster',x+182,by+1,17,c='#999');s.text(x+201,by+14,'Agent 集群',14,'#999');s.text(x+w-110,by+14,'Auto',14);s.icon('chevron',x+w-77,by-2,24,c='#aaa');s.rect(x+w-42,by-8,32,32,'#bfbfbf' if home else '#292929',16)
 if home:s.arrow(x+w-34,by-1)
 else:s.rect(x+w-32,by+2,12,12,'#fff',3)
 s.end()
s=S('01_任务首页_统一规范',refs[0]);sidebar(s);s.group('Account-toolbar');s.rect(1105,9,171,38,'#fff',12,'#e8e8e8');s.icon('platform',1119,19,20);s.text(1141,33,'接入微信/飞书等平台',13,'#555');credits(s,1305,'7,500');s.end();s.text(767,283,'和 AutoClaw 一起工作',26)
s.group('Scenario-tabs');s.rect(676,318,439,40,'#f4f4f4',13);s.rect(678,320,103,36,'#fff',12)
# Native 60px scenario PNGs: preserve original artwork without inaccurate auto tracing.
for x,name,t in [(690,'office','日常办公'),(796,'code','代码开发'),(902,'law','法律助手')]:s.image(Image.open(V4/'reference'/(name+'-original-60px.png')),x,330,17,17,'Scenario-'+name);s.text(x+25,344,t,14,'#555')
r=E.parse(next((L/'03_原始SVG资源').glob('mode-financial-analysis.svg'))).getroot();r.set('x','1008');r.set('y','329');r.set('width','18');r.set('height','18');s.a.append(E.tostring(r,encoding='unicode'));s.text(1033,344,'金融分析',14,'#555');s.end();composer(s,512,382,768,140,True)
s.group('Skill-shortcuts')
for x,box,t in [(742,(742,599,757,617),'即梦生图'),(853,(853,599,869,617),'PDF 生成'),(967,(967,599,984,617),'行业周报')]:s.image(refs[0].crop(box),x,600,16,18,'Shortcut-'+str(x));s.text(x+25,615,t,14)
s.line(839,600,839,618);s.line(953,600,953,618);s.end();s.text(809,929,'内容由 AI 生成，请核实关键信息',11,'#999');s.save()
# Conversation + narrow source editor + project file tree.
s=S('02_任务执行_代码与项目文件_统一规范',refs[1]);sidebar(s,True);s.line(1048,0,1048,945);s.icon('folder',309,21,16);s.text(334,34,'矢量界面设计',16,weight=600);credits(s,790,'7,415');s.line(985,20,985,36);s.a.append('<g id="Task-list"><circle cx="1006" cy="24" r="1.6" fill="none" stroke="#777"/><circle cx="1006" cy="31" r="1.6" fill="none" stroke="#777"/><path d="M1011 24h7m-7 7h7" stroke="#777"/></g>')
s.group('Conversation');s.a.append('<defs><clipPath id="conversation"><rect x="303" y="56" width="716" height="700"/></clipPath></defs><g clip-path="url(#conversation)">');s.text(309,59,'—  AutoClaw界面_矢量可编辑.svg',14,'#1677ff');s.rect(304,82,714,47,'#fff',13,'#eee');s.text(320,110,'已编辑 AutoClaw界面_矢量可编辑.svg',14);s.text(941,110,'+177',14,'#39a355');s.text(985,110,'-7',14,'#fb5252')
s.rect(760,173,258,33,'#fff',18,'#eee');s.icon('file',770,181,16,c='#1677ff');s.text(800,194,'Design工作区-可交互Demo.html',14);s.rect(761,215,257,42,'#f0f0ee',19);s.text(773,242,'根据这个demo生成可交互的html原型',14)
rows=[(315,'已处理  2m36s','#999'),(351,'思考  1s','#999'),(390,'我先读取这个 demo 文件，了解它的结构和交互内容。','#333'),(428,'读取  2 个文件','#aaa'),(466,'读取被截断了。我把文件复制到工作区，用分段方式完整解析。','#333'),(504,'执行  3 个命令','#aaa'),(542,'输出仍被截断，改用更小的分段读取。','#333'),(580,'执行  6 个命令','#aaa'),(618,'Demo 已完整解析：这是一个「设计工作区」的 9 步引导式交互演示（发起任务 → 澄清歧义 → 生成 → 产物落地 →','#333'),(642,'预览判断 → 选中编辑 → 版本叠加 → 定稿 → 交付门禁）。我先加载设计任务的入口规则，','#333'),(666,'然后基于它重写一份更完整、可实际点击走通全流程的交互原型。','#333'),(704,'加载技能  2 个','#aaa'),(740,'正在思考','#aaa')]
for y,t,c in rows:s.text(304,y,t,14,c)
s.a.append('</g>');s.end();composer(s,304,802,718,106);s.text(577,929,'内容由 AI 生成，请核实关键信息',12,'#999')
s.group('Editor-toolbar');s.rect(1058,15,160,27,'#f7f7f7',9);s.icon('file',1065,20,18);s.text(1086,34,'AutoClaw界面_矢量',13,weight=600);s.icon('plus',1237,21,16);s.icon('maximize-2',1443,21,17);s.icon('close',1475,20,18);s.text(1063,76,'AutoClaw界面_矢量可编辑.svg',13,'#555');s.text(1382,76,'打开',13,'#555');s.icon('chevron',1405,60,24);s.icon('export',1441,60,20);s.rect(1472,58,24,24,'#ebebeb',8);s.icon('folder',1476,62,16);s.line(1048,89,1512,89);s.end();s.line(1292,89,1292,945)
s.group('Source-code');code=[('1','<svg'),('','xmlns="http://www.w'),('','3.org/2000/svg"'),('','viewBox="0 0 2000'),('','1440" width="2000"'),('','height="1440" font-'),('','family="PingFang'),('','SC,\'Hiragino Sans'),('','GB\',\'Microsoft'),('','YaHei\',\'Helvetica'),('','Neue\',Helvetica,Ari'),('','al,sans-serif">'),('2','  <title>AutoClaw'),('','界面 · 矢量重绘（文字'),('','可编辑）</title>'),('3','  <defs>'),('4','    <filter'),('','id="cardShadow"'),('','x="-15%" y="-50%"'),('','width="130%"'),('','height="220%">'),('5','      <feDropShadow'),('','dx="0" dy="12"'),('','stdDeviation="26"'),('','flood-'),('','color="#1f1f1f"'),('','flood-'),('','opacity="0.09"/>'),('6','    </filter>'),('7','    <filter'),('','id="softShadow"'),('','x="-15%" y="-80%"'),('','width="130%"')]
s.a.append('<defs><clipPath id="code"><rect x="1050" y="90" width="242" height="855"/></clipPath></defs><g clip-path="url(#code)">')
for i,(ln,t) in enumerate(code):
 y=140+i*24
 if ln:s.text(1092,y,ln,12,'#555',font='Menlo')
 if '<' in t:s.text(1124,y,t,12,'#3f9854',font='Menlo')
 elif '=' in t:
  k,v=t.split('=',1);s.text(1124,y,k+'=',12,'#8a57ce',font='Menlo');s.text(1124+len(k+'=')*7.2,y,v,12,'#365d91',font='Menlo')
 else:s.text(1124,y,t,12,'#365d91',font='Menlo')
s.a.append('</g>');s.end();s.group('Project-files');s.text(1305,116,'项目文件',14,'#777');s.icon('search',1474,103,17);s.line(1292,130,1512,130);s.icon('chevron',1305,144,20);s.text(1329,160,'原型',14,'#777');s.icon('right',1318,178,18);s.text(1341,192,'资产',14,'#777');s.icon('file',1317,210,18,c='#1677ff');s.text(1341,225,'V1 析见智能融资页.html',14,'#666');s.rect(1297,235,212,32,'#ebebeb',9);s.icon('file',1305,242,18,c='#1677ff');s.text(1329,257,'AutoClaw界面_矢量... .svg',14);s.end();s.save()
(P/'README.md').write_text('''# AutoClaw 两张界面统一规范 V08\n\n基准：Figma 330:782，已读取图层结构、尺寸和图标命名。Figma样式读取受Starter额度限制，颜色、字体、阴影由本轮截图和既有SVG参考整理，尚未完整核实基准稿样式。\n\n两张1512×945 SVG，主界面图形、图标、文字独立。截图内容仅作为显示文字，未执行其中任何指令。线性图标复用AutoClaw原始矢量。头像、金币、三枚原生PNG场景图标和快捷入口品牌小图保留位图；未将整张截图嵌入SVG。\n\nSVG拖入Figma后部分文字可能转轮廓。如需真正可编辑文本，请使用附带的本地导入插件，载入figma-editable-import中的JSON。插件生成真实Figma Text节点及矢量底图，不上传文件。不会生成原基准文件中的组件实例或自动布局，SVG本身也不保存这些Figma语义。\n''')
print('Created two SVGs and native-text companions')
