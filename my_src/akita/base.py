from playwright.sync_api import Browser, Page, Locator


class BasePage:
    """
    playwrightのPageクラスのラッパー
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

    def click_to_navigate(self, selector: str):
        self.click(selector)
        self.__page.wait_for_load_state()
        self.__page.wait_for_timeout(self.__options.get('timeout', 1000))

    def fetch_option_values(self, selector: str) -> list[str]:
        options: Locator = self.__page.locator(selector)
        values: list[str] = [options.nth(i).get_attribute('value') for i in range(options.count())]
        values.remove('')
        return values

    def select(self, select_box_selector: str, option_value: str):
        self.__page.locator(select_box_selector).select_option(value=option_value)

    def click(self, selector: str):
        self.__page.click(selector)


class BaseBrowser:
    """
    playwrightのBrowserクラスのラッパー
    """
    __browser: Browser

    def __init__(self, browser: Browser):
        self.__browser = browser

    def new_page(self, options: dict) -> BasePage:
        return BasePage(self.__browser.new_page(), options)
