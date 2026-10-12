from pathlib import Path
from markdown import Markdown
ROOT=Path(__file__).resolve().parent
src=(ROOT/'index.template.html').read_text(encoding='utf-8')
md=(ROOT/'2026-10-12_AutoClaw_DesignAgent_完整文稿汇总_V17.md').read_text(encoding='utf-8')
article=Markdown(extensions=['tables','fenced_code']).convert(md)
assert src.count('@@ARTICLE@@')==1
out=src.replace('@@ARTICLE@@',article)
assert out.count('<section class="slide')==20
(ROOT/'index.html').write_text(out,encoding='utf-8')
print(f'Wrote {ROOT/"index.html"}')
