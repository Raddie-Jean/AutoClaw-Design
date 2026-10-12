from pathlib import Path
import json,xml.etree.ElementTree as E,re,hashlib,shutil
P=Path('output/autoclaw_native_icons_v06');old=Path('output/autoclaw_line_icons_v04');A=Path('/Applications/AutoClaw2.app/Contents/Resources/app/dist/renderer/assets');ns='http://www.w3.org/2000/svg';E.register_namespace('',ns)
for d in ['01_AutoClaw自定义','02_应用内Lucide','03_原始SVG资源','previews']:(P/d).mkdir(exist_ok=True)
manifest=[]
def save(r,folder,name,origin):
 if 'viewBox' not in r.attrib:r.set('viewBox',f'0 0 {r.get("width","24")} {r.get("height","24")}')
 r.set('width','24');r.set('height','24');r.attrib.pop('color',None)
 for e in r.iter():
  for k,v in list(e.attrib.items()):
   if v=='currentColor':e.set(k,'#333333')
   if k in ['class','className','focusable','role','aria-hidden']:e.attrib.pop(k,None)
 # Root defaults are preserved: omitting fill=none would turn line icons solid.
 path=P/folder/(name+'.svg');E.ElementTree(r).write(path,encoding='unicode');manifest.append({'file':str(path.relative_to(P)),'name':name,'source':origin,'viewBox':r.get('viewBox')})
known={x['source_identifier']:x['name'] for x in json.load(open(old/'manifest.json')) if x.get('source_identifier') and x['method']=='原始矢量'}
for i,x in enumerate(json.load(open(old/'source/extracted.json'))):
 if x['name']=='K5e':continue # animated spinner requires runtime props; do not export an incorrect static circle
 f=old/'source-originals'/(x['name']+'.svg');r=E.parse(f).getroot();name=known.get(x['name'],f'custom-{i+1:03d}-{x["name"].replace("$","s")}');save(r,'01_AutoClaw自定义',name,'AutoClaw installed JSX: '+x['name'])
seen=set()
for x in json.load(open(P/'source/factory-icons.json')):
 name=x['name']
 if name in seen:continue
 seen.add(name);r=E.Element('{'+ns+'}svg',{'viewBox':'0 0 24 24','fill':'none','stroke':'#333333','stroke-width':'2','stroke-linecap':'round','stroke-linejoin':'round'})
 for tag,props in x['data']:E.SubElement(r,'{'+ns+'}'+tag,{k:str(v) for k,v in props.items() if k!='key' and v is not None})
 save(r,'02_应用内Lucide',name,x['file']+' @ '+str(x['start']))
for f in A.glob('*.svg'):
 if f.name.startswith(('hero-','zwork-login-')):continue
 save(E.parse(f).getroot(),'03_原始SVG资源',re.sub(r'-[A-Za-z0-9_-]{8}$','',f.stem),str(f))
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(P/'README.md').write_text(f'''# AutoClaw 原生 SVG 图标库 V06\n\n共 {len(manifest)} 个文件，直接从本机 AutoClaw 2.0.1 安装资源提取。未使用截图描摹、PNG自动描边或凭印象重绘图标。\n\n01 为应用自定义 SVG，保留原始路径、viewBox、描边与填充规则。未确认用途的文件用 custom 编号，未猜测命名。\n02 为应用程序实际内置的 Lucide 图标，不是网上近似替代版。保持原始 24×24、2px 描边。\n03 为应用独立 SVG 资源，包含品牌、渠道和场景素材；它们不全是线性图标。\n\n## 导入 Figma\n\n把所需 SVG 拖入画布。也可导入各分类的“图标总览.svg”，每枚图标独立成组，名称完整显示。均为24×24显示尺寸，保留原始坐标系。单色已将 currentColor 固定为 #333333，无外部CSS或字体依赖。\n\n自定义图标部分是原稿扩展描边的填充路径，调整粗细需编辑路径；Lucide 是真实stroke描边，可直接调整粗细。不要给全部图标统一叠加描边。\n\n应用原生不同图标族的设计尺寸和线宽本来就不同，未强行统一路径以免改变原稿。动态加载图标因依赖运行时参数未纳入。截图中的个别场景图标原生是PNG，也未假装SVG收录。\n\n每枚文件来源见manifest.json。此包未进行真实Figma导入验证；已进行SVG解析、无位图和无外部依赖检查，以及渲染检查。\n''')
print('Native SVG files:',len(manifest))
