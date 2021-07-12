import base64
import inspect
import logging
import unittest
import yaml
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from page_objects import HomePage, AuthenticationPanel

logger = logging.getLogger(__name__)
logger.propagate = False
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


# noinspection PyArgumentList,PyTypeChecker
def decode_auth(encoded_value):
    return base64.b64decode(encoded_value).decode("utf-8")


class PortalLogin(unittest.TestCase, HomePage, AuthenticationPanel):
    # Initializing browser and driver.
    def setUp(self):
        chrome_driver_path = Path.cwd() / "drivers/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    # Wait until clickable element is present
    def get_element_clickable(self, xpath, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            err = 'Element with xpath {} could not be found!'
            raise Exception(err.format(xpath))

    # Wait until text is present in the element
    def get_text_present(self, xpath, text, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(ec.text_to_be_present_in_element((By.XPATH, xpath), text))
        except TimeoutException:
            err = 'Element with xpath {} could not be found!'
            raise Exception(err.format(xpath))

    # Click action using Java script
    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    # Scroll to the element view using Java script
    def js_scroll(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def read_test_prop(self, func_name):
        class_path = str(self.__class__).split("'")[1].split(".")
        file_name = class_path[0]
        class_name = class_path[1]
        filepath = Path.cwd() / f"data/{file_name.replace('test_', '')}.yml"
        if filepath is not None:
            with open(filepath, "r") as prop:
                return yaml.safe_load(prop)[class_name][func_name]

    def validate_home_page(self):
        self.get_text_present(HomePage.login_signup_lbl, "Login / Sign Up")
        logger.info("Portal launched successfully")

    def goto_login_panel(self):
        self.get_element_clickable(HomePage.login_signup_btn).click()
        self.get_text_present(AuthenticationPanel.login_create_header, "Log in / Create account to manage orders")
        logger.info("Login Panel launched successfully")

    def login_with_password(self, username, password):
        self.get_element_clickable(AuthenticationPanel.password_login_lbl).click()
        self.get_text_present(AuthenticationPanel.login_header, "Login")
        self.driver.find_element_by_id(AuthenticationPanel.username_edit).send_keys(decode_auth(username))
        self.driver.find_element_by_id(AuthenticationPanel.password_edit).send_keys(decode_auth(password))
        self.driver.find_element_by_id(AuthenticationPanel.submit_btn).click()
        if self.driver.find_element_by_xpath(AuthenticationPanel.success_mesg).is_displayed():
            logger.info("User logged in successfully")
        else:
            logger.info("User logged in NOT success")

    # Main validation
    def test_portal_login(self):
        prop = self.read_test_prop(inspect.stack()[0][3])
        self.driver.get(prop['url'])
        self.validate_home_page()
        self.goto_login_panel()
        self.login_with_password(prop['username'], prop['password'])

    def tearDown(self):
        self.driver.quit()

# if __name__ == '__main__':
#     unittest.main()
