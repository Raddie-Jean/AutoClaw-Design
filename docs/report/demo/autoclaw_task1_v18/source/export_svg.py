from pathlib import Path
import json,html,re,xml.etree.ElementTree as ET,shutil,base64
P=Path('output/autoclaw_task1_v15'); N='http://www.w3.org/2000/svg';ET.register_namespace('',N);(P/'figma-editable-import').mkdir(exist_ok=True)
def esc(t):return html.escape(str(t),quote=True)
def color(c):
 if not c or c=='rgba(0, 0, 0, 0)':return 'none'
 if c.startswith('rgb'):
  a=re.findall(r'[\d.]+',c);return '#'+''.join(f'{int(float(v)):02x}' for v in a[:3])
 return c
def opacity(c):
 a=re.findall(r'[\d.]+',c or '')
 return a[3] if (c or '').startswith('rgba') and len(a)>3 else '1'
for f in sorted((P/'screens').glob('*.layout.json')):
 d=json.loads(f.read_text());w,h=d['width'],d['height'];a=[];texts=[];defs=[]
 for i,o in enumerate(d['items']):
  c=o.get('clip'); cid=f'clip-{i}'
  if isinstance(c,dict):defs.append(f'<clipPath id="{cid}"><rect x="{c["x"]}" y="{c["y"]}" width="{max(0,c["right"]-c["x"])}" height="{max(0,c["bottom"]-c["y"])}"/></clipPath>');a.append(f'<g clip-path="url(#{cid})">')
  x,y=o['x'],o['y'];typ=o['type']
  if typ=='rect':
   a.append(f'<rect x="{x}" y="{y}" width="{o["w"]}" height="{o["h"]}" rx="{o["radius"]}" fill="{color(o["fill"])}" fill-opacity="{opacity(o["fill"])}" stroke="{color(o["border"]) if o["bw"] and o["bottom"] else "none"}" stroke-width="{o["bw"]}"/>')
   if o['bw'] and not o['bottom']:a.append(f'<path d="M{x} {y}h{o["w"]}" stroke="{color(o["border"])}" stroke-width="{o["bw"]}"/>')
   if o['bottom'] and not o['bw']:a.append(f'<path d="M{x} {y+o["h"]}h{o["w"]}" stroke="{color(o["bottomColor"])}" stroke-width="{o["bottom"]}"/>')
  elif typ=='grid':
   for xx in range(int(x),int(x+o['w']),32):a.append(f'<path d="M{xx} {y}v{o["h"]}" stroke="#eee" stroke-width=".7"/>')
   for yy in range(int(y),int(y+o['h']),32):a.append(f'<path d="M{x} {yy}h{o["w"]}" stroke="#eee" stroke-width=".7"/>')
  elif typ=='image':
   root=ET.fromstring(o['src'][7:]) if o['src'].startswith('inline:') else ET.fromstring(base64.b64decode(o['src'].split(',',1)[1])) if o['src'].startswith('data:') else ET.parse(P/o['src']).getroot()
   if o['src'].startswith('inline:'):
    bg=next((color(q.get('fill')) for q in reversed(d['items'][:i]) if q['type']=='rect' and color(q.get('fill'))!='none' and q['x']<=x and q['y']<=y and q['x']+q['w']>=x+o['w'] and q['y']+q['h']>=y+o['h']), '#fff')
    root.set('color', '#fff' if bg.lower() in ['#292929','#333333','#000000'] else '#333')
   vb=[float(v) for v in root.get('viewBox','0 0 1512 945').split()];sx=o['w']/vb[2];sy=o['h']/vb[3]
   for t in root.iter('{'+N+'}text'):
    tx=float(t.get('x','0'));ty=float(t.get('y','0'));tc=t.get('fill','#333333');tc='#'+''.join(c*2 for c in tc[1:]) if len(tc)==4 and tc.startswith('#') else tc
    texts.append(dict(x=x+tx*sx,y=y+ty*sy,text=''.join(t.itertext()),size=float(t.get('font-size','14'))*sx,color=color(tc),weight=int(t.get('font-weight','400')),font='PingFang SC'))
   root.set('x',str(x));root.set('y',str(y));root.set('width',str(o['w']));root.set('height',str(o['h']));a.append(ET.tostring(root,encoding='unicode'))
  elif typ=='text':
   lines=[o['text']]
   if 'w' in o:
    lines=[];line='';width=0
    for ch in o['text']:
     cw=o['size']*(1 if ord(ch)>255 else .55)
     if ch=='\n' or width+cw>o['w']-20:
      lines.append(line);line='';width=0
     if ch!='\n':line+=ch;width+=cw
    if line:lines.append(line)
   for j,t in enumerate(lines):
    yy=y+j*o['size']*1.65
    a.append(f'<text x="{x}" y="{yy}" fill="{color(o["color"])}" font-size="{o["size"]}" font-family="PingFang SC" font-weight="{o["weight"]}">{esc(t)}</text>');texts.append(dict(x=x,y=yy,text=t,size=o['size'],color=color(o['color']),weight=int(o['weight']) if str(o['weight']).isdigit() else 400,font='PingFang SC'))
  elif typ=='slider':
   cy=y+o['h']/2; end=x+o['w']*o['value']/o['max']
   a.append(f'<path d="M{x} {cy}H{x+o["w"]}" stroke="#ddd" stroke-width="4" stroke-linecap="round"/><path d="M{x} {cy}H{end}" stroke="#333" stroke-width="4" stroke-linecap="round"/><circle cx="{end}" cy="{cy}" r="7" fill="#333"/>')
  elif typ=='control':
   a.append(f'<rect x="{x}" y="{y}" width="{o["w"]}" height="{o["h"]}" rx="3" fill="{color(o["color"]) if o["kind"]=="color" else "#1677ff" if o["checked"] else "#fff"}" stroke="#ccc"/>')
   if o['checked']:a.append(f'<path d="M{x+3} {y+6}l3 3 5-6" fill="none" stroke="#fff" stroke-width="1.5"/>')
  if isinstance(c,dict):a.append('</g>')
 name=f.name.replace('.layout.json','');svg=f'<svg xmlns="{N}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{name}</title><defs>'+''.join(defs)+'</defs>'+''.join(a)+'</svg>';ET.fromstring(svg);(P/'screens'/f'{name}.svg').write_text(svg)
 root=ET.fromstring(svg)
 for par in root.iter():
  for ch in list(par):
   if ch.tag=='{'+N+'}text':par.remove(ch)
 (P/'figma-editable-import'/f'{name}.json').write_text(json.dumps(dict(name=name,width=w,height=h,svg=ET.tostring(root,encoding='unicode'),texts=texts),ensure_ascii=False))
plugin=Path('output/autoclaw_collaboration_draft_v11/figma-plugin');shutil.copytree(plugin,P/'figma-plugin',dirs_exist_ok=True)
items=sorted((P/'screens').glob('*.svg'))
gallery=''.join(f'<article><a href="screens/{esc(f.name)}"><img src="screens/{esc(f.name)}"></a><h2>{esc(f.stem)}</h2><a href="screens/{esc(f.name)}" download>下载 SVG</a></article>' for f in items)
(P/'designs.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>测试1 · 设计产物链路 · 设计稿</title><style>body{font:14px "PingFang SC",sans-serif;background:#f7f7f7;color:#333;margin:40px}h1{font-size:26px}p{color:#777}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}article{background:#fff;padding:16px;border:1px solid #e9e9e9;border-radius:12px}img{width:100%;border:1px solid #eee}h2{font-size:16px}a{color:#1677ff}nav{margin:24px 0}@media(max-width:800px){main{grid-template-columns:1fr}body{margin:20px}}</style><h1>测试1 · 设计产物链路 · V14</h1><p>发起需求 → 约束澄清 → 生成产物 → 预览 → 局部修改 → 候选版本 → 定稿 → SVG交付。测试2通过独立任务入口演示。</p><nav><a href="index.html">打开交互 Demo ↗</a>　 ·　 SVG 可拖入 Figma，原生文字导入见配套插件。</nav><main>'+gallery+'</main></html>')
print('Exported',len(items),'SVG screens')
