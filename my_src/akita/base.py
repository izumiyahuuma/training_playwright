import os.path
from uuid import uuid4

from playwright.sync_api import Browser, Page, Locator, Download


class BaseLocator:
    """
    playwrightのLocatorのラッパー
    """
    __locator: Locator

    def __init__(self, locator: Locator):
        self.__locator = locator

    def text(self, **kwargs) -> str:
        xpath: str = kwargs.get('xpath')
        if xpath:
            return self.__locator.locator(xpath).inner_text()
        return self.__locator.inner_text()

    def count(self) -> int:
        return self.__locator.count()

    def nth(self, i: int) -> 'BaseLocator':
        return BaseLocator(self.__locator.nth(i))

    def click_to_navigate_new_tab(self, xpath: str, browser: 'BaseBrowser') -> 'BasePage':
        contexts = browser.contexts()
        with contexts[0].expect_page() as new_page_info:
            self.__locator.locator(xpath).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state()
        return browser.new_page(**{'page': new_page})


class BasePage:
    """
    playwrightのPageのラッパー
    """

    __page: Page
    __options: dict  # HACK: クラス化してあげるといいよね

    def __init__(self, page: Page, options: dict):
        self.__page = page
        self.__options = options

    def navigate(self, url: str):
        self.__page.goto(url)
        self.__page.wait_for_load_state()
        self._wait()

    def click_to_navigate(self, xpath: str):
        self.click(xpath)
        self.__page.wait_for_load_state()
        self._wait()

    def fetch_option_values(self, xpath: str) -> list[str]:
        options: Locator = self.__page.locator(xpath)
        values: list[str] = [options.nth(i).get_attribute('value') for i in range(options.count())]
        return values

    def select(self, xpath: str, option_value: str):
        self.__page.locator(xpath).select_option(value=option_value)

    def click_to_download(self, xpath: str, save_dir: str):
        with self.__page.expect_download() as download_info:
            self.__page.click(xpath)
        download: Download = download_info.value
        file_name = download.suggested_filename
        uuid = uuid4()
        # ファイル名に変更加えない方が本来のクローリング的には正しい気がしつつ、ディレクトリきるのめんどいからファイル名にくっつけちゃう
        save_path = f'{save_dir}/{uuid}_{file_name}'
        download.save_as(save_path)
        self._wait()
        return save_path

    def click(self, xpath: str):
        self.__page.click(xpath)

    def find_all(self, xpath: str) -> BaseLocator:
        locator = BaseLocator(self.__page.locator(xpath))
        return locator

    def close(self):
        self.__page.close()

    def _wait(self):
        self.__page.wait_for_timeout(self.__options.get('timeout', 1000))


class BaseBrowser:
    """
    playwrightのBrowserのラッパー
    """
    __browser: Browser
    __options: dict  # HACK: クラス化してあげるといいよね

    def __init__(self, browser: Browser, options: dict):
        self.__browser = browser
        self.__options = options

    def new_page(self, **kwargs) -> BasePage:
        if isinstance(kwargs.get('page'), Page):
            return BasePage(kwargs.get('page'), self.__options)
        return BasePage(self.__browser.new_page(), self.__options)

    def contexts(self):
        return self.__browser.contexts
