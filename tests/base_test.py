import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.utils import take_screenshot
from utils.logger import Logger
from utils.driver import ChromeDriver

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(__name__)
        cls.logger.info("Setting up WebDriver")
        cls.driver = ChromeDriver(implicit_wait=10)
        cls.driver_wait = WebDriverWait(cls.driver, 20)

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("Tearing down WebDriver")
        cls.driver.quit()

    def tearDown(self):
        # Get the current test case result
        test_result = self._outcome.result if hasattr(self, '_outcome') else None
        
        if test_result:
            # Check for failures or errors
            if test_result.failures or test_result.errors:
                for test, error in test_result.failures + test_result.errors:
                    self.logger.error(f"Test failed: {test.id()}")
                    # Use driver directly since it is now the WebDriver instance
                    take_screenshot(self.driver, test.id())
                    self.logger.info(f"Screenshot taken for failed test: {test.id()}")