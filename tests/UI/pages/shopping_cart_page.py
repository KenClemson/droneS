from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class ShoppingCartPage:
    """Page Object for the shopping cart page."""

    def __init__(self, driver):
        self.driver = driver

    # Locators
    CART_ICON = (By.CSS_SELECTOR, 'a[data-test="shopping-cart-link"]')
    ITEM_PRICE = (By.CSS_SELECTOR, 'div[data-test="inventory-item-price"]')
    TOTAL_PRICE = (By.CSS_SELECTOR, 'div[class*="summary_total_label"]')
    CART_LIST = (By.CSS_SELECTOR, 'div[data-test="cart-list"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, 'button[id="checkout"]')

    def open_cart(self):
        """Open the shopping cart."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CART_ICON)).click()
        logger.info("Opened the shopping cart.")
        self.driver.save_screenshot(f'screenshots/selected_cart_icon.png')

    def get_item_price_elements(self):
        """Return list of price elements in the cart."""
        return self.driver.find_elements(*self.ITEM_PRICE)

    def get_cart_item_prices(self):
        """Iterate over cart items in the cart list, get their prices, and sum them."""
        try:
            # Locate the cart list
            cart_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CART_LIST)
            )
            # Find all items within the cart list
            cart_items = cart_list.find_elements(By.CSS_SELECTOR, 'div.cart_item')

            logger.info(f"Number of items in the cart: {len(cart_items)}")

            # Iterate through items and sum their prices
            total_price = 0.0
            for item in cart_items:
                # Find the price element for each item (unpack the locator tuple)
                price_element = item.find_element(*self.ITEM_PRICE)
                price_text = price_element.text.replace("$", "").strip()
                price = float(price_text)
                logger.info(f"Item price: ${str(price)}")
                total_price += price

            logger.info(f"Calculated total price of all items in the cart: ${str(total_price)}")
            return total_price

        except Exception as e:
            self.driver.save_screenshot(f'screenshots/error_calculating_total_price.png')
            logger.error(f"An error occurred while calculating total price: {str(e)}")
            raise

    def click_checkout_button(self):
        try:
            checkout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
            )
            checkout_button.click()
            logger.info("Clicked the checkout button.")
            self.driver.save_screenshot(f'screenshots/clicking_checkout_btn.png')
        except Exception as e:
            self.driver.save_screenshot(f'screenshots/error_clicking_checkout_btn.png')
            logger.error(f"Error clicking checkout button: {e}")
            raise
