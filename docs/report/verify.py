"""Visual and interaction smoke check for the standalone V17 report."""

from pathlib import Path
from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parent
PREVIEWS = ROOT / "previews"
PREVIEWS.mkdir(exist_ok=True)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1050}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri(), wait_until="load")
    assert page.locator(".slide").count() == 20
    assert page.locator(".slide-link").count() == 20
    assert "V13" not in page.locator(".top").inner_text()
    assert all("V13" not in text for text in page.locator(".slide").all_inner_texts())
    reports = []
    for i in range(20):
        page.locator(".slide-link").nth(i).click()
        slide = page.locator(".slide.active")
        assert slide.count() == 1
        assert page.locator("#count").inner_text() == f"{i+1:02d} / 20"
        image_count = slide.locator("img").count()
        broken = slide.locator("img").evaluate_all("images => images.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src'))")
        geometry = slide.evaluate("""s => {
          const bounds = [...s.querySelectorAll('.body > *, .body > * > *, .body > * > * > *')]
            .filter(e => e.getClientRects().length)
            .map(e => ({tag:e.tagName, className:e.className, bottom:e.offsetTop+e.offsetHeight}));
          const body=s.querySelector('.body');
          return {bodyScroll:body?.scrollHeight ?? 0, bodyClient:body?.clientHeight ?? 0,
            slideScroll:s.scrollHeight, slideClient:s.clientHeight,
            maximumChildBottom:Math.max(0,...bounds.map(x=>x.bottom))};
        }""")
        slide.screenshot(path=str(PREVIEWS / f"slide-{i+1:02d}.png"))
        reports.append((i+1, slide.get_attribute("data-title"), image_count, broken, geometry))
    page.locator('[data-mode="doc"]').click()
    assert page.locator(".article h1").count() >= 1
    assert page.locator(".article h2").count() >= 5
    assert page.locator(".article").is_visible()
    assert "完整文稿汇总" in page.locator(".article h1").inner_text()
    assert "V13" not in page.locator(".article").inner_text()
    assert all("V13" not in title for _, title, *_ in reports)
    assert page.locator('.article a[href="references/03-PRD.pdf"]').count() >= 1
    assert not page.locator(".layout > aside").is_visible()
    assert page.locator(".main").bounding_box()["x"] == 0
    page.screenshot(path=str(PREVIEWS / "document-desktop.png"))
    page.locator('[data-mode="demo"]').click()
    assert page.locator(".demo-frame").is_visible()
    assert not page.locator(".layout > aside").is_visible()
    assert page.locator(".main").bounding_box()["x"] == 0
    page.screenshot(path=str(PREVIEWS / "demo-desktop.png"))
    iframe = page.frame_locator(".demo-frame")
    assert page.locator(".demo-frame").get_attribute("src").endswith("autoclaw_presentation_v15/index.html#task2")
    assert page.locator("#demo-open").get_attribute("href").endswith("autoclaw_presentation_v15/index.html#task2")
    iframe.locator("#presentation").wait_for(state="visible")
    expect(iframe.locator("#path-title")).to_have_text("测试2 · 设计产物与协作评审")
    task2 = iframe.frame_locator("#task2-frame")
    task2.locator("#task-files").wait_for(state="attached")
    assert "产物版本" in task2.locator("#task-files").inner_text()
    assert iframe.locator("#svg-gallery").get_attribute("href").endswith("autoclaw_task2_v15/designs.html")
    task2.locator('a[href="../autoclaw_presentation_v15/index.html"]').first.click()
    expect(iframe.locator("main")).to_be_visible()
    page.locator('[data-demo="task1"]').click()
    assert page.locator(".demo-frame").get_attribute("src").endswith("autoclaw_presentation_v15/index.html#task1")
    iframe.locator("#presentation").wait_for(state="visible")
    expect(iframe.locator("#path-title")).to_have_text("测试1 · 设计产物链路")
    task1 = iframe.frame_locator("#task1-frame")
    task1.locator('[data-action="start-example"]').wait_for()
    task1.locator('[data-action="start-example"]').click()
    task1.locator('[data-action="confirm"]').click()
    task1.locator('[data-target="composer"]').wait_for(timeout=8000)
    assert iframe.locator("#svg-gallery").get_attribute("href").endswith("autoclaw_task1_v15/designs.html")
    page.locator('[data-demo="task2"]').click()
    iframe.locator("#presentation").wait_for(state="visible")
    task2.locator("#task-files").wait_for(state="attached")
    page.locator('[data-mode="deck"]').click()
    assert page.locator(".layout > aside").is_visible()
    assert page.locator(".main").bounding_box()["x"] > 0
    page.locator("#overview-btn").click()
    assert page.locator(".overview.open .overview-item").count() == 20
    page.locator("#close-overview").click()
    assert not page.locator(".overview").is_visible()
    mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    mobile.goto((ROOT / "index.html").as_uri(), wait_until="load")
    mobile_width = mobile.evaluate("({scroll:document.documentElement.scrollWidth, client:document.documentElement.clientWidth})")
    mobile.locator(".mobile-select").select_option("19")
    assert mobile.locator("#count").inner_text() == "20 / 20"
    mobile.screenshot(path=str(PREVIEWS / "mobile-slide-20.png"), full_page=True)
    mobile.locator('[data-mode="doc"]').click()
    mobile_doc_width = mobile.evaluate("({scroll:document.documentElement.scrollWidth, client:document.documentElement.clientWidth})")
    assert mobile_doc_width["scroll"] <= mobile_doc_width["client"] + 1, "Mobile document horizontal overflow"
    mobile.screenshot(path=str(PREVIEWS / "mobile-document.png"))
    print("SLIDES", len(reports))
    for report in reports:
        print("SLIDE", *report)
    print("MOBILE", mobile_width)
    print("PAGE_ERRORS", errors)
    assert not errors, errors
    assert all(not report[3] for report in reports), "Broken slide images"
    assert mobile_width["scroll"] <= mobile_width["client"] + 1, "Mobile horizontal overflow"
    template = browser.new_page()
    template.goto((ROOT / "index.template.html").as_uri() + "#document", wait_until="load")
    assert template.url.endswith("index.html#document")
    assert "@@ARTICLE@@" not in template.locator("body").inner_text()
    assert template.locator(".article h1").is_visible()
    template.goto((ROOT / "index.template.html").as_uri() + "#slide-20", wait_until="load")
    assert template.url.endswith("index.html#slide-20")
    assert template.locator("#count").inner_text() == "20 / 20"
    browser.close()
