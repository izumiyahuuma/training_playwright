from playwright.sync_api import Browser, Page, Locator


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
        self.__page.wait_for_timeout(self.__options.get('timeout', 1000))

    def click_to_navigate(self, xpath: str):
        self.click(xpath)
        self.__page.wait_for_load_state()
        self.__page.wait_for_timeout(self.__options.get('timeout', 1000))

    def fetch_option_values(self, xpath: str) -> list[str]:
        options: Locator = self.__page.locator(xpath)
        values: list[str] = [options.nth(i).get_attribute('value') for i in range(options.count())]
        return values

    def select(self, xpath: str, option_value: str):
        self.__page.locator(xpath).select_option(value=option_value)

    def click(self, xpath: str):
        self.__page.click(xpath)

    def find_all(self, xpath: str) -> BaseLocator:
        locator = BaseLocator(self.__page.locator(xpath))
        return locator


class BaseBrowser:
    """
    playwrightのBrowserのラッパー
    """
    __browser: Browser

    def __init__(self, browser: Browser):
        self.__browser = browser

    def new_page(self, options: dict) -> BasePage:
        return BasePage(self.__browser.new_page(), options)
