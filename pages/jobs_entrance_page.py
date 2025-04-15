from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC

class JobsEntrancePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://useinsider.com/careers/quality-assurance/"

    def open_page(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        try:
            self.driver.find_element(By.ID, "wt-cli-accept-all-btn").click()
        except ElementNotInteractableException:
            print("Çerezler zaten onaylanmiş")

    def click_all_jobs(self, wait):
        element = self.driver.find_element(By.LINK_TEXT, "See all QA jobs")
        wait.until(EC.element_to_be_clickable(element))
        element.click()
