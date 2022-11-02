from playwright.sync_api import sync_playwright, Browser
from base import *

with sync_playwright() as p:
    browser = BaseBrowser(browser=p.chromium.launch(headless=False))
    page = browser.new_page(options={})
    page.navigate('http://cals05.pref.akita.lg.jp/')
    page.click('//html/body/div[2]/ul/li[2]/a')
    page.click_to_navigate('//html/body/div[3]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/a')
    
