from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class OverviewPage:
    """Page object for the checkout overview page."""

    # Locators
    ITEM_PRICE_LOCATOR = (By.CSS_SELECTOR, 'div.inventory_item_price')
    SUBTOTAL_LOCATOR = (By.CSS_SELECTOR, 'div.summary_subtotal_label')
    TAX_LOCATOR = (By.CSS_SELECTOR, 'div.summary_tax_label')
    TOTAL_LOCATOR = (By.CSS_SELECTOR, 'div.summary_total_label')
    OVERVIEW_URL = "checkout-step-two.html"

    def __init__(self, driver):
        self.driver = driver

    def verify_overview_page_url(self, config):
        """Verify that the current URL is the checkout page URL."""
        current_url = self.driver.current_url
        assert current_url == f"{config['BASE_URL']}{self.OVERVIEW_URL}", f"Expected URL: {config['BASE_URL']}{self.OVERVIEW_URL}, but got: {current_url}"
        logger.info(f"Verified that the current URL is: {current_url}")
        self.driver.save_screenshot("screenshots/correct_overview_url.png")
        return True  # Explicitly return True if the assertion passes

    def get_item_prices(self):
        """Fetch the prices of all items on the overview page."""
        logger.info("Waiting for item prices to appear...")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.ITEM_PRICE_LOCATOR)
            )
            price_elements = self.driver.find_elements(*self.ITEM_PRICE_LOCATOR)
            prices = [float(element.text.replace("$", "").strip()) for element in price_elements]

            if not prices:
                logger.warning("No prices found. Possible locator issue or page not fully loaded.")
                self.driver.save_screenshot("screenshots/no_item_prices.png")

            logger.info(f"Fetched item prices: {prices}")
            return prices
        except Exception as e:
            logger.error(f"Failed to fetch item prices: {e}")
            self.driver.save_screenshot("item_prices_error.png")
            raise

    def get_subtotal_price(self):
        """Get the subtotal displayed on the overview page."""
        subtotal_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SUBTOTAL_LOCATOR)
        )
        subtotal_price = float(subtotal_element.text.replace("Item total: $", "").strip())
        logger.info(f"Subtotal on overview page: {subtotal_price}")
        return subtotal_price

    def verify_overview_total(self):
        """Verify that the sum of item prices matches the subtotal."""
        logger.info("Verifying overview page totals...")
        item_prices = self.get_item_prices()
        logger.info(f"Item prices fetched: {item_prices}")

        calculated_total = sum(item_prices)
        logger.info(f"Calculated item total: ${calculated_total}")

        displayed_subtotal = self.get_subtotal_price()
        logger.info(f"Displayed subtotal fetched: ${displayed_subtotal}")

        assert calculated_total == displayed_subtotal, (
            f"Mismatch in item totals! Calculated: ${calculated_total}, Displayed: ${displayed_subtotal}"
        )
        logger.info(f"Verified overview page subtotal matches: ${displayed_subtotal}")
        return calculated_total
