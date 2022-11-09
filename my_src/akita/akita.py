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
    options = [options[2]]  # TODO 開発のため一つだけに絞って動かしてるのであとで消す
    for option in options:
        page.select('//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select', option)
        page.click_to_navigate('//html/body/div/form/table[3]/tbody/tr[2]/td/a/img')
        crawl_search_list(browser, page)


def crawl_search_list(browser: BaseBrowser, page: BasePage):
    result_label: str = page.find_all(
        '//html/body/div/form/table[4]/tbody/tr[1]/td/table/tbody/tr/td[1]').text()
    if 'ヒットしました' not in result_label:
        print('データなし')  # TODO dictとかで返して呼び出し元に表示させたい
        return

    rows: BaseLocator = page.find_all('//html/body/div/form/table[4]/tbody/tr[2]/td/table/tbody/tr')
    for i in range(1, rows.count()):  # 1行目はヘッダなので除外
        row = rows.nth(i)
        print(row.text(**{'xpath': '//td[1]'}))


if __name__ == '__main__':
    with sync_playwright() as p:
        main(p)
