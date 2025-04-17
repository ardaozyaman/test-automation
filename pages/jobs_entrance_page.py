from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class JobsEntrancePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com/careers/quality-assurance/"

    def open_page(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        return self.click((By.ID, "wt-cli-accept-all-btn"))


    def click_all_jobs(self, wait):
        return self.click((By.LINK_TEXT, "See all QA jobs"))
