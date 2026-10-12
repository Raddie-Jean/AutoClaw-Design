from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
D=Path(__file__).resolve().parent.parent;broken=[];local=[];external=set()
class P(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ['src','href','poster'] or not v:continue
   if v.startswith(('data:','blob:','mailto:','javascript:','#')):continue
   u=urlsplit(v)
   if u.scheme in ['http','https']:
    external.add(v)
    if u.hostname in ['localhost','127.0.0.1']:local.append([str(self.file.relative_to(D)),v])
    continue
   if u.scheme:continue
   target=(self.file.parent/unquote(u.path)).resolve()
   if not target.exists():broken.append([str(self.file.relative_to(D)),v])
for f in D.rglob('*.html'):
 p=P();p.file=f
 try:p.feed(f.read_text())
 except Exception as e:broken.append([str(f),str(e)])
print('broken',len(broken),'local',len(local));print(json.dumps(broken[:60],ensure_ascii=False,indent=2));(D/'静态链接检查.json').write_text(json.dumps({'broken':broken,'machine_links':local,'external':sorted(external)},ensure_ascii=False,indent=2))
