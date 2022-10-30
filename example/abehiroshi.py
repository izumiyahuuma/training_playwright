"""
http://abehiroshi.la.coocan.jp/
出演映画の表データを取得する
"""

from playwright.sync_api import sync_playwright, Browser, Page

with sync_playwright() as p:
    browser: Browser = p.chromium.launch(headless=False)
    page: Page = browser.new_page()
    page.goto('http://abehiroshi.la.coocan.jp/')
    page.frame_locator("frame[name=\"left\"]").get_by_role("link", name="映画出演").click()

    page.close()
    browser.close()
