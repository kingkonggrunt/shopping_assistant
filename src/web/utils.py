from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class FirefoxDriver:
    """A context manager for the Selenium Firefox Webdriver"""

    def __init__(self, driver_path: str, *, headless: bool=True):
        """
        Args:
            driver_path (str): path of webdriver file
            headless (bool, optional): Run the Selenium Webdriver in headless mode. Defaults to True.
        """
        self.options = Options()
        self.options.headless = headless
        self.driver = None
        self.driver_path = driver_path

    def __enter__(self):
        self.driver = webdriver.Firefox(options=self.options,
                                        executable_path=rf"{self.driver_path}")
        return self.driver

    def __exit__(self, exc_type, exc_value, exe_traceback):
        self.driver.quit()