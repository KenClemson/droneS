from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logger = logging.getLogger(__name__)


class CheckoutPage:
    """Page Object for the checkout page."""

    def __init__(self, driver):
        self.driver = driver

    # Locators
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[data-test="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[data-test="lastName"]')
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, 'input[data-test="postalCode"]')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, 'input[data-test="continue"]')
    CHECKOUT_URL = "checkout-step-one.html"
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container h3")


    def verify_checkout_page_url(self, config):
        """Verify that the current URL is the checkout page URL."""
        current_url = self.driver.current_url
        assert current_url == f"{config['BASE_URL']}{self.CHECKOUT_URL}", f"Expected URL: {config['BASE_URL']}{self.CHECKOUT_URL}, but got: {current_url}"
        logger.info(f"Verified that the current URL is: {current_url}")

    def fill_order_form(self, first_name, last_name, postal_code):
        """Fill the order form with the given details."""
        logger.info(
            f"Filling out the order form with First Name: {first_name}, Last Name: {last_name}, Zip: {postal_code}"
        )

        # Fill first name
        first_name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        )
        first_name_input.clear()  # Clear existing text
        first_name_input.send_keys(first_name)

        # Fill last name
        last_name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        )
        last_name_input.clear()  # Clear existing text
        last_name_input.send_keys(last_name)

        # Fill postal code
        postal_code_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.POSTAL_CODE_INPUT)
        )
        postal_code_input.clear()  # Clear existing text
        postal_code_input.send_keys(postal_code)

        logger.info("Order form filled successfully.")

    def fill_field(self, field_name, value):
        field_map = {
            "First Name": self.FIRST_NAME,
            "Last Name": self.LAST_NAME,
            "Zip/Postal Code": self.POSTAL_CODE
        }
        field_locator = field_map[field_name]
        field_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(field_locator)
        )
        field_element.clear()
        field_element.send_keys(value)

    def get_error_message(self):
        error_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ERROR_MESSAGE)
        )
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.driver.save_screenshot(f'screenshots/expected_checkout{str(timestamp)}.png')
        return error_element.text


    def click_continue(self):
        """Click the continue button."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CONTINUE_BUTTON)).click()
        logger.info("Clicked the continue button to proceed.")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.driver.save_screenshot(f'screenshots/clicker_checkout_continue{str(timestamp)}.png')