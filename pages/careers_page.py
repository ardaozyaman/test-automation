from selenium.webdriver.common.by import By
from utils.logger import Logger
from pages.base_page import BasePage

class CareersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.locators = {
            'locations': (By.ID, "career-our-location"),
            'teams': (By.ID, "career-find-our-calling"),
            'life': (By.XPATH, "/html/body/div[1]/section[4]/div/div"),
            'life_header': (By.XPATH, "/html/body/div[1]/section[4]/div/div/div/div[1]/div/h2")
        }

    def is_locations_visible(self):
        self.logger.info("Checking if locations section is visible")
        return self.driver.find_element(*self.locators['locations']).is_displayed()

    def is_teams_visible(self):
        self.logger.info("Checking if teams section is visible")
        return self.driver.find_element(*self.locators['teams']).is_displayed()

    def is_life_at_insider_visible(self):
        self.logger.info("Checking if 'Life at Insider' section is visible")
        try:
            result = self.driver.find_element(*self.locators['life_header']).text == "Life at Insider"
            if not result:
                self.logger.warning("'Life at Insider' header text doesn't match expected value")
            return result
        except Exception as e:
            self.logger.error(f"Error while checking 'Life at Insider' section: {str(e)}")
            return False