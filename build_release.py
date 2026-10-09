"""Sync the selected case-study sources and render Markdown for static browsing.

Run from this folder with: python3 build_release.py
The original files under ../ remain untouched. Existing files in docs/ with the
same names are refreshed, so keep edits to source documents in ../output dirs.
"""

from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path

import markdown


PACKAGE = Path(__file__).resolve().parent
DOCS = PACKAGE / "docs"
SELECTED = (
    "input",
    "md",
    "pdf",
    "mvp_v03",
    "journey_v04",
    "co_creation_v05",
    "sketch_v06",
    "feature_v07",
    "prototype_v08",
    "report_v09",
    "architecture_v10",
)


def ignored(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {".DS_Store", "__pycache__"} or name.endswith((".zip", ".pyc"))}


def rewrite_md_links(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "data:")):
            return match.group(0)
        return 'href="' + target[:-3] + '.html' + (match.group(2) or '') + '"'

    return re.sub(r'href="([^"]+\.md)(#[^"]*)?"', replace, html)


def reading_page(title: str, body: str, prefix: str) -> str:
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · AutoClaw Design Agent</title><link rel="stylesheet" href="{prefix}styles.css"></head>
<body><header class="sitebar"><a class="sitebrand" href="{prefix}index.html"><span>A</span>AutoClaw · Design Agent</a><nav><a href="{prefix}index.html">资料首页</a><a href="{prefix}process.html">研究过程</a><a href="{prefix}report_v09/index.html">方案汇报</a><a href="{prefix}architecture_v10/index.html">功能架构</a></nav></header>
<article class="reading">{body}</article><footer class="foot" style="max-width:1000px;margin:30px auto 70px;padding:20px"><a href="{prefix}process.html">← 过程资料</a> · <a href="{prefix}index.html">资料首页</a></footer></body></html>'''


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    # In the original working folder, sync from sibling output directories.
    # After this package becomes its own repository, docs/ is the source.
    source_root = PACKAGE.parent if all((PACKAGE.parent / name).is_dir() for name in SELECTED) else DOCS
    for name in SELECTED:
        source = source_root / name
        if not source.exists():
            raise FileNotFoundError(source)
        if source.resolve() != (DOCS / name).resolve():
            shutil.copytree(source, DOCS / name, dirs_exist_ok=True, ignore=ignored)

    evidence = DOCS / "mvp_v03" / "evidence"
    gallery_items = []
    for image in sorted(evidence.glob("*.png")):
        name = escape(image.name)
        gallery_items.append(f'<a class="card" href="{name}"><img src="{name}" alt="{name}"><span style="padding:13px 16px;font-size:14px;color:#193438">{name}</span></a>')
    (evidence / "index.html").write_text(
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>录屏观察截图 · AutoClaw Design Agent</title><link rel="stylesheet" href="../../styles.css"></head><body>'
        '<header class="sitebar"><a class="sitebrand" href="../../index.html"><span>A</span>AutoClaw · Design Agent</a><nav><a href="../2026-10-04_AutoClaw_Design工作区_MVP初稿_V03.html">返回 V03 观察记录</a></nav></header>'
        '<main class="wrap"><div class="eyebrow">Evidence</div><h1>录屏观察截图</h1><p style="color:#607572">AutoClaw 与 Lovart 的界面观察截帧；点击可查看原图。</p><div class="cards" style="margin-top:30px">'
        + ''.join(gallery_items) + '</div></main></body></html>', encoding="utf-8")

    count = 0
    for source in sorted(DOCS.rglob("*.md")):
        if source.name == "README.md":
            # The per-version README files still remain readable on GitHub.
            continue
        raw = source.read_text(encoding="utf-8")
        body = markdown.markdown(raw, extensions=["extra", "tables", "fenced_code", "toc"])
        body = rewrite_md_links(body)
        title = next((line.lstrip("# ").strip() for line in raw.splitlines() if line.startswith("# ")), source.stem)
        target = source.with_suffix(".html")
        target.write_text(reading_page(title, body, "../"), encoding="utf-8")
        count += 1

    # In the existing standalone viewers, point document links at the rendered
    # Pages copies. Their original source Markdown files remain alongside them.
    for name in ("report_v09", "architecture_v10"):
        for page in (DOCS / name).glob("*.html"):
            if page.name == "index.html" or page.name.startswith("2026-"):
                page.write_text(rewrite_md_links(page.read_text(encoding="utf-8")), encoding="utf-8")

    readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
    body = markdown.markdown(readme, extensions=["extra", "tables", "fenced_code"])
    body = body.replace('href="docs/', 'href="')
    (DOCS / "about.html").write_text(reading_page("资料包说明", body, ""), encoding="utf-8")
    print(f"Prepared {len(SELECTED)} source folders; rendered {count} Markdown documents.")


if __name__ == "__main__":
    main()
