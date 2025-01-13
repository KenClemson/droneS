import logging
from pytest_bdd import given, when, then, scenarios, parsers
from selenium.common.exceptions import NoSuchElementException
from tests.UI.pages.login_page import LoginPage

# Load the feature file
scenarios("/app/tests/UI/features/login.feature")

LOGIN_URL = "https://www.saucedemo.com/"
logger = logging.getLogger(__name__)

# Step definitions
@given("I am on the login page")
def go_to_login_page(browser):
    """Navigate to the login page."""
    browser.get(LOGIN_URL)
    logger.info("Navigated to the login page")

@when(parsers.parse('I enter {username} and {password}'))
def enter_credentials(browser, username, password):
    """Enter the username and password."""
    login_page = LoginPage(browser)
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
def click_login_button(browser):
    """Click the login button."""
    login_page = LoginPage(browser)
    login_page.click_login_button()
    logger.info("Login button clicked")

@then(parsers.parse('I should see {expected_outcome}'))
def verify_login_outcome(browser, expected_outcome):
    """Verify the login outcome."""
    login_page = LoginPage(browser)
    error_msg = login_page.get_error_message()

    if expected_outcome == "successful login":
        assert "inventory" in browser.current_url, f"Expected inventory page, but got: {browser.current_url}"
        logger.info("Login successful")
    elif expected_outcome == "locked out error":
        assert "locked out" in error_msg.lower(), f"Expected locked-out error, but got: {error_msg}"
    elif expected_outcome == "missing username error":
        assert "Username is required" in error_msg, "Expected missing username error"
    elif expected_outcome == "missing password error":
        assert "Password is required" in error_msg, "Expected missing password error"
    elif expected_outcome == "login failed":
        assert "Epic sadface" in error_msg, f"Expected login failure, but got: {error_msg}"
    else:
        raise AssertionError(f"Unknown outcome: {expected_outcome}")
