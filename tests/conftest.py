import pytest
import logging
from selenium import webdriver
import os
from tests.UI.pages.login_page import LoginPage
from tests.UI.pages.product_page import ProductPage
from tests.UI.pages.checkout_page import CheckoutPage
from tests.UI.pages.shopping_cart_page import ShoppingCartPage
from tests.UI.pages.overview_page import OverviewPage
from tests.config_loader import load_config
'''
UI Fixtures
'''
@pytest.fixture
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=True")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    driver = webdriver.Chrome(options=options)
    logging.info("Browser initialized")
    os.makedirs('screenshots', exist_ok=True)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture
def login_page(browser):
    """Fixture to provide a ProductPage object."""
    return LoginPage(browser)

@pytest.fixture
def product_page(browser):
    """Fixture to provide a ProductPage object."""
    return ProductPage(browser)

@pytest.fixture
def checkout_page(browser):
    """Fixture to provide an instance of the CheckoutPage."""
    return CheckoutPage(browser)

@pytest.fixture
def shopping_cart_page(browser):
    """Fixture to provide an instance of the CheckoutPage."""
    return ShoppingCartPage(browser)

@pytest.fixture
def overview_page(browser):
    """Fixture to provide an instance of the OverviewPage."""
    return OverviewPage(browser)

'''
API Fixtures
'''
@pytest.fixture
def context():
    """Provides a shared context dictionary to pass data between steps."""
    return {}

@pytest.fixture(scope="session")
def base_url():
    """Returns the API base URL."""
    return "https://petstore.swagger.io/v2"
