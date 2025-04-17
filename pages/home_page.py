from pages.elements.nav_bar import NavBar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.home_page_url = "https://useinsider.com/"
        self.unique_element = (By.ID, "home_logo_reel")
        self.nav_bar = NavBar(self.driver)

    def open_homepage(self):
        self.driver.get(self.home_page_url)

    def is_home_page(self):
        return self.is_element_present(self.unique_element)
        

