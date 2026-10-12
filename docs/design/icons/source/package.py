from pathlib import Path
import json,xml.etree.ElementTree as E,html,zipfile
from PIL import Image,ImageDraw,ImageFont
P=Path('output/autoclaw_native_icons_v06');m=json.load(open(P/'manifest.json'));font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',12)
for group in sorted(set(x['file'].split('/')[0] for x in m)):
 items=[x for x in m if x['file'].startswith(group+'/')];w=1000;h=((len(items)+7)//8)*110;im=Image.new('RGB',(w,h),'#fafafa');d=ImageDraw.Draw(im);parts=[]
 for i,x in enumerate(items):
  cx=(i%8)*125;cy=(i//8)*110;r=E.parse(P/x['file']).getroot();assert not r.findall('.//{http://www.w3.org/2000/svg}image');raw=(P/x['file']).read_text();assert 'currentColor' not in raw;assert '<script' not in raw
  r.set('x',str(cx+43));r.set('y',str(cy+18));r.set('width','40');r.set('height','40');parts.append('<g id="'+html.escape(x['name'])+'">'+E.tostring(r,encoding='unicode')+f'<text x="{cx+62}" y="{cy+85}" font-family="Arial" font-size="9" text-anchor="middle" fill="#666">{html.escape(x["name"])}</text></g>')
  png=Image.open(P/'previews'/(group+'--'+x['name']+'.png')).convert('RGBA').resize((48,48));im.paste(png,(cx+38,cy+14),png);name=x['name'];d.text((cx+4,cy+78),name[:22],font=font,fill='#555')
 (P/(group+'_图标总览.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+''.join(parts)+'</svg>');im.save(P/(group+'_图标总览.png'))
(P/'validation.json').write_text(json.dumps({'count':len(m),'all_xml_valid':True,'all_vector_only':True,'all_rendered':True,'currentColor_resolved':True,'figma_import_tested':False},indent=2))
zp=P.parent/'2026-10-12_AutoClaw_原生SVG图标库_V06.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
 for f in P.rglob('*'):
  if f.is_file() and 'source' not in f.relative_to(P).parts:z.write(f,f.relative_to(P))
assert zipfile.ZipFile(zp).testzip() is None;print(zp.resolve())
