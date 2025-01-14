from pytest_bdd import given, when, parsers
from selenium.common.exceptions import NoSuchElementException
import logging


logger = logging.getLogger(__name__)

@given("I am on the login page")
def go_to_login_page(browser, config):
    """Navigate to the login page."""
    browser.get( f"{config['BASE_URL']}")
    logger.info("Navigated to the login page")

@when(parsers.parse('I enter {username} and {password}'))
def enter_credentials(login_page, username, password):
    """Enter the username and password."""

    try:
        logger.info(f"Entering credentials - Username: '{username}', Password: '{password}'")
        if username:
            login_page.enter_username(username)
        if password:
            login_page.enter_password(password)
    except NoSuchElementException as e:
        logger.error(f"Element not found: {e}")
        raise

@when("I click the login button")
def click_login_button(login_page):
    """Click the login button."""

    login_page.click_login_button()
    logger.info("Login button clicked")