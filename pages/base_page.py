from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import Logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
        self.logger = Logger.get_logger(self.__class__.__name__)

    # Wait Methods
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            self.logger.info(f"Waiting for element {locator} to be visible")
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element {locator} not visible after {timeout} seconds")
            return None

    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for element to be clickable"""
        try:
            self.logger.info(f"Waiting for element {locator} to be clickable")
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element {locator} not clickable after {timeout} seconds")
            return None

    # Element Interaction Methods
    def click(self, locator):
        """Click on element"""
        try:
            self.logger.info(f"Clicking element {locator}")
            element = self.wait_for_element_clickable(locator)
            element.click()
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            return False

    def input_text(self, locator, text):
        """Input text into element"""
        try:
            self.logger.info(f"Entering text '{text}' into element {locator}")
            element = self.wait_for_element_visible(locator)
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            self.logger.error(f"Failed to input text into element {locator}: {str(e)}")
            return False

    # JavaScript Methods
    def execute_script(self, script, element=None):
        """Execute JavaScript on element or page"""
        try:
            self.logger.info(f"Executing script: {script}")
            if element:
                return self.driver.execute_script(script, element)
            return self.driver.execute_script(script)
        except Exception as e:
            self.logger.error(f"Failed to execute script: {str(e)}")
            return None

    def scroll_to_element(self, element):
        """Scroll element into view"""
        try:
            self.logger.info("Scrolling to element")
            self.execute_script("arguments[0].scrollIntoView(true);", element)
            return True
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            return False

    # Action Chains Methods
    def hover(self, locator):
        """Hover over element"""
        try:
            self.logger.info(f"Hovering over element {locator}")
            element = self.wait_for_element_visible(locator)
            self.actions.move_to_element(element).perform()
            return True
        except Exception as e:
            self.logger.error(f"Failed to hover over element {locator}: {str(e)}")
            return False

    def drag_and_drop(self, source_locator, target_locator):
        """Drag and drop element"""
        try:
            self.logger.info(f"Dragging element {source_locator} to {target_locator}")
            source = self.wait_for_element_visible(source_locator)
            target = self.wait_for_element_visible(target_locator)
            self.actions.drag_and_drop(source, target).perform()
            return True
        except Exception as e:
            self.logger.error(f"Failed to perform drag and drop: {str(e)}")
            return False

    # Element State Methods
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    # Window/Frame Handling Methods
    def switch_to_frame(self, frame_reference):
        """Switch to iframe"""
        try:
            self.logger.info(f"Switching to frame: {frame_reference}")
            self.driver.switch_to.frame(frame_reference)
            return True
        except Exception as e:
            self.logger.error(f"Failed to switch to frame: {str(e)}")
            return False

    def switch_to_default_content(self):
        """Switch back to default content"""
        try:
            self.logger.info("Switching to default content")
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            self.logger.error(f"Failed to switch to default content: {str(e)}")
            return False

    # Navigation Methods
    def navigate_to(self, url):
        """Navigate to URL"""
        try:
            self.logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to URL: {str(e)}")
            return False

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def refresh_page(self):
        """Refresh current page"""
        self.logger.info("Refreshing page")
        self.driver.refresh()