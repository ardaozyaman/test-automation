from selenium.webdriver.common.by import By
from pages.base_page import BasePage
class NavBar(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.navigation_bar = None
        self.drop_down_elements = []
        self.sub_dropdown_elements = []

    def init_dropdown_elements(self):
        self.navigation_bar = self.driver.find_element(By.ID, "navbarNavDropdown")
        self.drop_down_elements = self.navigation_bar.find_elements(By.ID, "navbarDropdownMenuLink")
        self._set_dropdown_elements()

    def init_sub_dropdown_elements(self):
        self.sub_dropdown_elements = self.navigation_bar.find_elements(By.CLASS_NAME, "dropdown-sub")
        self._set_sub_dropdown_elements()

    def _set_dropdown_elements(self):
        for e in self.drop_down_elements:
            text = e.text
            if text == "Company": self.company_element = e
            elif text == "Resources": self.resources_element = e
            elif text == "Customers": self.customers_element = e
            elif text == "Solutions": self.solutions_element = e
            elif text == "Platform": self.platform_element = e
            elif text == "Why Insider": self.why_insider_element = e

    def _set_sub_dropdown_elements(self):
        for e in self.sub_dropdown_elements:
            text = e.text
            if text == "Careers": self.careers_element = e
            elif text == "Integrations": self.integrations_element = e
            elif text == "Contact Us": self.contact_us_element = e

    def click_company(self): self.company_element.click()
    def click_careers(self): self.careers_element.click()
