from playwright.sync_api import sync_playwright, Playwright
from base import *
from pprint import pprint

SAVE_DIR: str = '/tmp/crawl'
XPATH: dict = {
    # 検索ページ
    '入札執行課所option内容': '//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select/option',
    '入札執行課所': '//html/body/div/form/table[3]/tbody/tr[2]/td/table/tbody/tr[8]/td[2]/select',
    '検索ボタン': '//html/body/div/form/table[3]/tbody/tr[2]/td/a/img',
    # 検索結果
    'ヒット件数': '//html/body/div/form/table[4]/tbody/tr[1]/td/table/tbody/tr/td[1]',
    '検索結果テーブル行': '//html/body/div/form/table[4]/tbody/tr[2]/td/table/tbody/tr',
}


def main(play_wright: Playwright):
    browser = BaseBrowser(browser=play_wright.chromium.launch(headless=False), options={})
    page = browser.new_page()
    page.navigate('http://cals05.pref.akita.lg.jp/ecydeen/do/PPI/koukoku')

    # NOTE: 普通に一括検索できるけど、勉強なので入札執行課所毎に検索していく。
    options: list[str] = page.fetch_option_values(XPATH['入札執行課所option内容'])
    options.remove('')  # 入札執行課所が「指定しない」は今回対象外
    options = [options[2]]  # NOTE: 開発のため一つだけに絞って動かしてる
    for option in options:
        page.select(XPATH['入札執行課所'], option)
        page.click_to_navigate(XPATH['検索ボタン'])
        crawl_search_list(browser, page)


def crawl_search_list(browser: BaseBrowser, page: BasePage):
    """
    検索ページのリストを抽出するための処理
    :param browser:
    :param page:
    :return:
    """
    result_label: str = page.find_all(XPATH['ヒット件数']).text()
    if 'ヒットしました' not in result_label:
        print('データなし')
        return

    rows: BaseLocator = page.find_all(XPATH['検索結果テーブル行'])
    crawled_data: list = []
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

        detail_page: BasePage = row.click_to_navigate_new_tab('//td[3]/a', browser)
        detail_data = crawl_detail_page(browser, detail_page)
        main_data['detail'] = detail_data
        crawled_data.append(main_data)
        detail_page.close()

    pprint(crawled_data)

    page._wait()


def crawl_detail_page(browser: BaseBrowser, page: BasePage):
    file_name = page.click_to_download('//html/body/form/div/table[2]/tbody/tr[4]/td/a[1]', SAVE_DIR)
    return {
        'title': page.find_all('//html/body/form/div/table[2]/tbody/tr[2]/th/font').text(),
        'file_name': file_name
    }


if __name__ == '__main__':
    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)
    with sync_playwright() as p:
        main(p)
