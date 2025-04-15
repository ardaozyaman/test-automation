import os
import time
import locale
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def simplify_text(text):
    return ''.join(filter(str.isalpha, text)).lower()

def get_tab_url(driver, tab):
    handles = driver.window_handles
    try:
        driver.switch_to.window(handles[tab])
    except IndexError:
        raise NoSuchWindowException("Bu sekme mevcut değil")
    return driver.current_url

def check_tab_url(driver, tab, url):
    return get_tab_url(driver, tab).startswith(url)

def wait_for_load(driver_wait):
    driver_wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

def switch_to_new_window(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    driver.close()
    driver.switch_to.window(handles[0])

def take_screenshot(driver, test_name):
    path = "./screenshots/"
    os.makedirs(path, exist_ok=True)
    driver.save_screenshot(os.path.join(path, f"{test_name}.png"))
