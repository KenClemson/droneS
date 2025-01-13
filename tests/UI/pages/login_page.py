# pages/login_page.py

from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class LoginPage:
    """Page Object for the Swag Labs login page."""

    def __init__(self, driver):
        self.driver = driver

    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CLASS_NAME, "error-message-container")

    def enter_username(self, username):
        try:
            username_input = self.driver.find_element(*self.USERNAME_FIELD)
            username_input.clear()
            username_input.send_keys(username)
            logger.info(f"Entered username: {username}")
        except Exception as e:
            logger.error(f"Error entering username: {e}")
            raise

    def enter_password(self, password):
        try:
            password_input = self.driver.find_element(*self.PASSWORD_FIELD)
            password_input.clear()
            password_input.send_keys(password)
            logger.info("Entered password")
        except Exception as e:
            logger.error(f"Error entering password: {e}")
            raise

    def click_login_button(self):
        try:
            login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
            login_btn.click()
            logger.info("Login button clicked")
        except Exception as e:
            logger.error(f"Error clicking login button: {e}")
            raise

    def get_error_message(self):
        try:
            error_message = self.driver.find_element(*self.ERROR_CONTAINER).text
            logger.info(f"Retrieved error message: {error_message}")
            return error_message
        except Exception:
            logger.warning("No error message found")
            return None
