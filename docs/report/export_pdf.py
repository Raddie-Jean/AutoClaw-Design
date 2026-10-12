"""Export the presentation slides to a print-ready PDF."""

from pathlib import Path
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "pdf" / "AutoClaw_DesignAgent_方案汇报_V17.pdf"
OUT.parent.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    page.goto((ROOT / "index.html").as_uri(), wait_until="load")
    page.add_style_tag(content="@media print {.slide:last-of-type{break-after:auto;page-break-after:auto}.stage{height:auto!important}}")
    page.pdf(path=str(OUT), print_background=True, prefer_css_page_size=True)
    browser.close()
print(OUT)
