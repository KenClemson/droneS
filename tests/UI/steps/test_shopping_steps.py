import logging
from pytest_bdd import given, when, then, scenarios, parsers
from tests.UI.steps.common_steps import *

scenarios("/app/tests/UI/features/shopping_cart.feature")
logger = logging.getLogger(__name__)

'''
Product Steps
'''
@given("I am on the products page")
def open_products_page(browser):
    """Navigate to the products page."""
    browser.get("https://www.saucedemo.com/inventory.html")
    logger.info("Navigated to the products page.")

@when(parsers.parse('I add "{item_name}" to the cart'))
def add_item_to_cart(context, product_page, item_name):
    logger.info(f"Adding item '{item_name}' to the cart.")
    price = product_page.add_item_to_cart(item_name)
    context['product_page_prices'] = context.get('product_page_prices', {})
    context['product_page_prices'][item_name] = price

'''
Shopping cart Steps
'''
@when("I open the shopping cart")
def open_cart(shopping_cart_page):
    """Open the shopping cart."""
    shopping_cart_page.open_cart()

@then("The prices in the cart match the product prices")
def verify_prices_match(shopping_cart_page, context):

    product_page_prices = context.get('product_page_prices', {})
    assert product_page_prices, "No items were added to the cart from the product page!"
    cart_page_prices = shopping_cart_page.get_cart_item_prices()
    product_price = 0.0
    for item in product_page_prices:
        product_price += product_page_prices[item]

    logger.info(f"Total Product page prices: {str(product_price)}")
    logger.info(f"Total Cart page prices: {str(cart_page_prices)}")
    assert product_price == cart_page_prices, f"Product page prices do not match cart page prices!"
    logger.info("Verified product page prices match cart page prices.")

@when("I click on the cart checkout button")
def click_checkout_button(shopping_cart_page):
    """Click the checkout button."""
    shopping_cart_page.click_checkout_button()

'''
Checkout Steps
'''
@then("I should be directed to the checkout step 1 page")
def verify_checkout_step_1(checkout_page):
    assert checkout_page.verify_checkout_page_url, "Checkout step 1 page not loaded!"
    logger.info("Verified checkout step 1 page loaded.")

@when(parsers.parse("I fill in {field_name} with {value}"))
def fill_checkout_field(checkout_page, field_name, value):
    checkout_page.fill_field(field_name, value)

@when(parsers.parse("I leave {field_name} empty"))
def leave_checkout_field_empty(checkout_page, field_name):
    checkout_page.fill_field(field_name, "")

@then(parsers.parse("I should see the error message {error_message}"))
def verify_error_message(checkout_page, error_message):
    actual_message = checkout_page.get_error_message()
    assert actual_message == error_message, f"Expected {error_message}, but got {actual_message}"

@when(parsers.parse("I fill the order form with {first_name} {last_name} and {postal_code}"))
def fill_order_form(checkout_page, first_name, last_name, postal_code):
    checkout_page.fill_order_form(first_name, last_name, postal_code)

@when('I click continue')
def click_continue(checkout_page):
    checkout_page.click_continue()

'''
Overview Steps
'''
@then("I should be directed to the checkout step 2 page")
def verify_checkout_step_2(overview_page, config):
    assert overview_page.verify_overview_page_url(config), "Checkout step 1 page not loaded!"
    logger.info("Verified checkout step 2 page loaded.")

@then("the order amount should be correct on the overview page")
def calculate_overview_items(overview_page, context):
    total_overview_price = overview_page.verify_overview_total()

    product_page_prices = context.get('product_page_prices', {})
    assert product_page_prices, "No items were added to the cart from the product page!"

    product_price = 0.0
    for item in product_page_prices:
        product_price += product_page_prices[item]

    logger.info(f"Total Product page prices: {str(product_price)}")
    logger.info(f"Total Overview page prices: {str(total_overview_price)}")
    assert product_price == total_overview_price, f"Product page prices do not match overview page prices!"
