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
    """
    検索ページのリストを抽出するための処理
    :param browser:
    :param page:
    :return:
    """
    result_label: str = page.find_all(
        '//html/body/div/form/table[4]/tbody/tr[1]/td/table/tbody/tr/td[1]').text()
    if 'ヒットしました' not in result_label:
        print('データなし')  # TODO dictとかで返して呼び出し元に表示させたい
        return

    rows: BaseLocator = page.find_all('//html/body/div/form/table[4]/tbody/tr[2]/td/table/tbody/tr')
    for i in range(1, rows.count()):  # 1行目はヘッダなので除外
        row: BaseLocator = rows.nth(i)
        main_data: dict = {
            '公開日': row.text(**{'xpath': '//td[1]'}),
            '入札方式': row.text(**{'xpath': '//td[2]'}),
            '名称': row.text(**{'xpath': '//td[3]'}),
            '場所': row.text(**{'xpath': '//td[4]'}),
            '種別': row.text(**{'xpath': '//td[5]'}),
            '等級': row.text(**{'xpath': '//td[6]'}),
            '概要': row.text(**{'xpath': '//td[7]'}),
            '予定価格': row.text(**{'xpath': '//td[8]'}),
            '課所': row.text(**{'xpath': '//td[9]'}),
            '区分': row.text(**{'xpath': '//td[10]'}),
        }
        print(main_data)

    # row: BaseLocator = rows.nth(1)
    # row.click('//td[3]/a')
    # page.wait()


def crawl_detail_page(browser: BaseBrowser, page: BasePage):
    pass


if __name__ == '__main__':
    with sync_playwright() as p:
        main(p)
