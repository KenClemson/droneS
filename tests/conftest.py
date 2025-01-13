import pytest
import logging
from selenium import webdriver

@pytest.fixture
def browser(request):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode in Docker
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    logging.info("Browser initialized")

    yield driver

    # Teardown: Capture screenshot on failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    if failed:
        test_name = request.node.name
        screenshot_path = f"screenshots/{test_name}.png"
        driver.save_screenshot(screenshot_path)
        logging.error(f"Test failed: Screenshot saved to {screenshot_path}")

    driver.quit()
    logging.info("Browser closed")


# ------------------------------------
# Fixtures for API Tests
# ------------------------------------

@pytest.fixture
def context():
    """Provides a shared context dictionary to pass data between steps."""
    return {}

@pytest.fixture(scope="session")
def base_url():
    """Returns the API base URL."""
    return "https://petstore.swagger.io/v2"
