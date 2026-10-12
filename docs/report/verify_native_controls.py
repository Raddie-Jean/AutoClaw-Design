from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 for n in [1,2]:
  page=b.new_page(viewport={'width':1512,'height':945});errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  page.goto(f'http://127.0.0.1:8771/report_v17/demo/autoclaw_task{n}_v18/index.html');page.wait_for_timeout(500)
  if n==2:page.locator('[data-tab=canvas]').first.click()
  assert page.get_by_label('拖动画布').count()==1
  page.locator('.reading-menu summary').first.click();page.locator('[data-native=read-phone]').click();page.wait_for_timeout(100)
  page.locator('.reading-menu summary').first.click();page.locator('[data-native=read-desktop]').click()
  page.locator('.reading-menu summary').nth(2).click()
  with page.expect_download() as dl:page.locator('[data-native=html]').click()
  assert dl.value.suggested_filename.endswith('.html')
  page.get_by_label('拖动画布').click();assert page.locator('body').evaluate('(e)=>e.classList.contains("pan-mode")')
  page.screenshot(path=f'output/report_v17/previews/V18_测试{n}_原生工具栏.png')
  assert not errs,errs
  print('task',n,'passed menus, HTML download, hand tool, no page errors')
 b.close()
