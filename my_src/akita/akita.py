from playwright.sync_api import sync_playwright, Browser
from base import *

with sync_playwright() as p:
    browser = BaseBrowser(browser=p.chromium.launch(headless=False))
    page = browser.new_page(options={})
    page.navigate('http://cals05.pref.akita.lg.jp/ecydeen/do/PPI/koukoku')
    options: list[str] = page.fetch_option_values(
        '//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select/option')

    for option in options:
        page.select('//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select', option)
        page.click_to_navigate('//html/body/div/form/table[3]/tbody/tr[2]/td/a/img')
