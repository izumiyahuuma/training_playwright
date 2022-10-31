"""
http://abehiroshi.la.coocan.jp/
出演映画の表データを取得する
"""

from playwright.sync_api import sync_playwright, Browser, Page
from pprint import pprint

with sync_playwright() as p:
    browser: Browser = p.chromium.launch(headless=False)
    page: Page = browser.new_page()
    page.goto('http://abehiroshi.la.coocan.jp/')
    page.frame_locator("frame[name=\"left\"]").get_by_role("link", name="映画出演").click()

    # tableが出現しない状態でrow取得すると0件になる時があるので待つ
    page.frame_locator('frame[name=\"right\"]').locator('//html/body/center[2]/table').wait_for()

    rows = page.frame_locator('frame[name=\"right\"]').locator('//html/body/center[2]/table/tbody/tr')
    for i in range(rows.count()):
        release_day = rows.nth(i).locator('//td[1]').text_content().replace('\n', " ")
        title = rows.nth(i).locator('//td[2]').text_content().replace('\n', " ")
        print(f'{release_day} : {title}')

    page.close()
    browser.close()
