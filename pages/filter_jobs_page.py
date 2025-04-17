from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage
from utils.utils import simplify_text

class FilterJobsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.current_location = ""
        self.current_department = ""

    def click_location_selector(self):
        self.click((By.ID, "select2-filter-by-location-container"))

    def click_department_selector(self):
        self.click((By.ID, "select2-filter-by-department-container"))

    def click_location(self, location):
        options = self.driver.find_elements(By.CLASS_NAME, "select2-results__option")
        for e in options:
            if location in e.text:
                e.click()
                self.current_location = simplify_text(self.driver.find_element(By.ID, "select2-filter-by-location-container").get_attribute("title"))
                return
        raise NoSuchElementException("Lokasyon bulunamadı")

    def click_department(self, department):
        options = self.driver.find_elements(By.CLASS_NAME, "select2-results__option")
        for e in options:
            if department in e.text:
                e.click()
                self.current_department = simplify_text(self.driver.find_element(By.ID, "select2-filter-by-department-container").get_attribute("title"))
                return
        raise NoSuchElementException("Departman bulunamadı")

    def click_view_role_button(self):
        button = self.driver.find_element(By.XPATH, "//*[@id=\"jobs-list\"]/div[1]/div/a")
        self.driver.execute_script("arguments[0].click();", button)

    def is_all_jobs_correct(self):
        jobs = self.driver.find_elements(By.XPATH, "//*[@id='jobs-list']/div")
        self.scroll_to_element(jobs[0])
        self.wait_for_element_visible((By.XPATH, "//*[@id='jobs-list']/div"))
        for job in jobs:
            location = simplify_text(job.get_attribute("data-location"))
            department = simplify_text(job.get_attribute("data-team"))
            if location != self.current_location or department != self.current_department:
                return False
        return True
