import unittest
from time import sleep
from tests.base_test import BaseTest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.jobs_entrance_page import JobsEntrancePage
from pages.filter_jobs_page import FilterJobsPage
from utils.utils import wait_for_load, check_tab_url, switch_to_new_window
from utils.logger import Logger

class TestInsider(BaseTest):
    def setUp(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.logger.info("Initializing test class and page objects")
        self.home_page = HomePage(self.driver)
        self.careers_page = CareersPage(self.driver)
        self.jobs_page = JobsEntrancePage(self.driver)
        self.filter_page = FilterJobsPage(self.driver)

    """
    def test_network_tests(self):
        driver = self.driver
        driver.start_network_logging()

        driver.get("https://useinsider.com/careers/open-positions/?department=qualityassurance")

        requests = driver.get_network_requests()
        for request in requests:
            print(f"URL: {request['url']}")
            print(f"Method: {request['method']}")
            print(f"Type: {request['type']}")
            print("---")

        driver.stop_network_logging()"""
    

    def test_1_homepage_and_click_careers(self):
        self.logger.info("Starting homepage and careers navigation test")
        self.home_page.open_homepage()
        self.assertTrue(self.home_page.is_home_page(), "Home page is not loaded correctly")
        self.home_page.nav_bar.init_dropdown_elements()
        self.home_page.nav_bar.click_company()
        self.home_page.nav_bar.init_sub_dropdown_elements()
        self.home_page.nav_bar.click_careers()
        self.assertTrue(self.careers_page.is_locations_visible(), "Locations section is not visible")
        self.assertTrue(self.careers_page.is_life_at_insider_visible(), "Life at Insider section is not visible")
        self.assertTrue(self.careers_page.is_teams_visible(), "Teams section is not visible")
        self.logger.info("Homepage and careers navigation test completed successfully")
  

    def test_2_job_positions(self):
        self.jobs_page.open_page()
        self.jobs_page.accept_cookies()
        self.jobs_page.click_all_jobs(self.driver_wait)
        wait_for_load(self.driver_wait)
        sleep(5)
        self.filter_page.click_location_selector()
        sleep(5)
        self.filter_page.click_location_selector()
        sleep(5)
        self.filter_page.click_location_selector()
        self.filter_page.click_location("Istanbul, Turkiye")
        self.filter_page.click_department_selector()
        self.filter_page.click_department("Quality Assurance")
        wait_for_load(self.driver_wait)
        self.filter_page.is_all_jobs_correct()
        self.filter_page.click_view_role_button()
        self.assertTrue(check_tab_url(self.driver, 1, "https://jobs.lever.co/useinsider"))
        switch_to_new_window(self.driver)


if __name__ == '__main__':
    unittest.main(verbosity=0)
