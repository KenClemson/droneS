from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class ProductPage:
    """Page Object for the product listing page."""

    def __init__(self, driver):
        self.driver = driver

    # Locators
    PRODUCT_LIST = (By.CSS_SELECTOR, 'div[data-test="inventory-list"]')
    ITEM_PRICE_LOCATOR = (By.CSS_SELECTOR, 'div.inventory_item_price')

    def add_item_to_cart(self, item_name):
        try:
            """Click the 'Add to cart' button for the given item and get the price"""
            product_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//div[text()="{item_name}"]/ancestor::div[@class="inventory_item"]'))
            )

            price_element = product_element.find_element(*self.ITEM_PRICE_LOCATOR)
            price_text = price_element.text.replace("$", "").strip()
            item_price = float(price_text)

            logger.info(f"Captured price for '{item_name}': ${item_price}")

            add_to_cart_button = WebDriverWait(product_element, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'button[data-test="add-to-cart-{item_name.lower().replace(" ", "-")}"]'))
            )
            add_to_cart_button.click()

            # Screenshot and log
            self.driver.save_screenshot(f'screenshots/selected_{item_name}.png')
            logger.info(f"Added '{item_name}' to the cart.")
            return item_price

        except Exception as e:
            self.driver.save_screenshot(f'screenshots/error_selecting_product.png')
            logger.error(f"An error occurred while selecting a product: {str(e)}")
            raise RuntimeError(f"Error encountered: {e}") from e
