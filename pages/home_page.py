
from pages.elements.nav_bar import NavBar

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_page_url = "https://useinsider.com/"
        self.nav_bar = NavBar(driver)

    def open_homepage(self):
        self.driver.get(self.home_page_url)

    def is_home_page(self):
        return self.driver.title == "#1 Leader in Individualized, Cross-Channel CX — Insider"


# Directory: pages/careers_page.py

from selenium.webdriver.common.by import By

class CareersPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            'locations': (By.ID, "career-our-location"),
            'teams': (By.ID, "career-find-our-calling"),
            'life': (By.XPATH, "/html/body/div[1]/section[4]/div/div"),
            'life_header': (By.XPATH, "/html/body/div[1]/section[4]/div/div/div/div[1]/div/h2")
        }

    def is_locations_visible(self):
        return self.driver.find_element(*self.locators['locations']).is_displayed()

    def is_teams_visible(self):
        return self.driver.find_element(*self.locators['teams']).is_displayed()

    def is_life_at_insider_visible(self):
        try:
            return self.driver.find_element(*self.locators['life_header']).text == "Life at Insider"
        except:
            return False
