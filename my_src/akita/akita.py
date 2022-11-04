from playwright.sync_api import sync_playwright, Playwright
from base import *


def main(play_wright: Playwright):
    browser = BaseBrowser(browser=play_wright.chromium.launch(headless=False))
    page = browser.new_page(options={})
    page.navigate('http://cals05.pref.akita.lg.jp/ecydeen/do/PPI/koukoku')

    # NOTE: 普通に一括検索できるけど、勉強なので入札執行課所毎に検索していく。
    options: list[str] = page.fetch_option_values(
        '//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select/option')
    options.remove('')  # 入札執行課所が「指定しない」は今回対象外
    for option in options:
        page.select('//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select', option)
        page.click_to_navigate('//html/body/div/form/table[3]/tbody/tr[2]/td/a/img')
        crawl_search_list(browser, page)


def crawl_search_list(browser: BaseBrowser, page: BasePage):
    pass


if __name__ == '__main__':
    with sync_playwright() as p:
        main(p)
