from pathlib import Path
import xml.etree.ElementTree as E,json,re,shutil
O=Path(__file__).resolve().parents[1];NS='{http://www.w3.org/2000/svg}'
E.register_namespace('',NS[1:-1]);(O/'Figma原生图层').mkdir(exist_ok=True)
def num(e,k,d=0):return float(e.get(k,str(d)))
def convert(e,ox=0,oy=0,s=1,root=False):
 t=e.tag.split('}')[-1];name=e.get('id',t)
 if t in ['title','defs','filter','clipPath']:return None
 if t=='svg' and not root:
  x=ox+num(e,'x')*s;y=oy+num(e,'y')*s;w=num(e,'width',24)*s;h=num(e,'height',24)*s
  if not any(n.tag==NS+'text' for n in e.iter()):
   e.attrib.pop('x',None);e.attrib.pop('y',None)
   return dict(type='svg',name=name,x=x,y=y,w=w,h=h,svg=E.tostring(e,encoding='unicode'))
  vb=e.get('viewBox','0 0 1512 945').split();ox=x;oy=y;s=w/float(vb[2])
 if t in ['g','svg']:
  a=[convert(c,ox,oy,s) for c in e];return dict(type='group',name=name,children=[c for c in a if c])
 a=dict(type=t,name=name,x=ox+num(e,'x')*s,y=oy+num(e,'y')*s,fill=e.get('fill','#000000'),stroke=e.get('stroke'),strokeWidth=num(e,'stroke-width',1)*s)
 if t=='text':a.update(text=''.join(e.itertext()),size=num(e,'font-size',14)*s,weight=num(e,'font-weight',400));a['name']=a['text'][:40]
 elif t=='rect':a.update(w=num(e,'width')*s,h=num(e,'height')*s,r=num(e,'rx')*s)
 elif t=='circle':a.update(x=ox+(num(e,'cx')-num(e,'r'))*s,y=oy+(num(e,'cy')-num(e,'r'))*s,w=num(e,'r')*2*s,h=num(e,'r')*2*s)
 elif t=='image':a.update(w=num(e,'width')*s,h=num(e,'height')*s,src=e.get('href',e.get('{http://www.w3.org/1999/xlink}href','')))
 elif t=='path':
  d=e.get('d','');n=[float(v) for v in re.findall(r'-?\d*\.?\d+',d)]
  if re.fullmatch(r'M[\d .,-]+[HLV][\d .,-]+',d) and len(n) in [3,4]:
   x,y=n[:2];end=(n[2],n[3]) if 'L' in d else (n[2],y) if 'H' in d else (x,n[2]);a.update(type='line',x=ox+x*s,y=oy+y*s,x2=ox+end[0]*s,y2=oy+end[1]*s)
  else:
   return dict(type='svg',name=name,x=ox,y=oy,w=1512*s,h=945*s,svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1512" height="945" viewBox="0 0 1512 945">{E.tostring(e,encoding="unicode")}</svg>')
 else:return None
 return a
for p in O.glob('*.svg'):
 data=convert(E.parse(p).getroot(),root=True);data.update(name=p.stem,width=1512,height=945,schema='autoclaw-native-v2')
 (O/'Figma原生图层'/(p.stem+'.json')).write_text(json.dumps(data,ensure_ascii=False))
print('native JSON ready')
