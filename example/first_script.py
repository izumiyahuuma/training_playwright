"""
https://playwright.dev/python/docs/library#first-script
の写経
"""
from playwright.sync_api import sync_playwright, Browser, Page

with sync_playwright() as p:
    browser: Browser = p.webkit.launch()
    page: Page = browser.new_page()
    page.goto('http://whatsmyuseragent.org/')
    page.screenshot(path="example.png")
    browser.close()
