import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# my website to test
URL = "https://www.saucedemo.com"

# users i will use for testing
correct_username = "standard_user"
correct_password = "secret_sauce"
locked_username = "locked_out_user"


# this runs before every test, it opens the browser
# and closes it when the test is done
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# ====================================================
# helper functions i made so i dont repeat myself
# ====================================================

# this function opens the website
def open_website(driver):
    driver.get(URL)
    time.sleep(1)


# this function does the login for me
def do_login(driver, username, password):
    open_website(driver)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)


# this function logs in with the correct user
def login_with_correct_user(driver):
    do_login(driver, correct_username, correct_password)


# this function adds the first product to the cart
def add_first_product_to_cart(driver):
    first_button = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
    first_button.click()
    time.sleep(1)


# this function goes to the cart page
def go_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)


# this function fills the checkout form
def fill_checkout_form(driver, first, last, zipcode):
    driver.find_element(By.ID, "first-name").send_keys(first)
    driver.find_element(By.ID, "last-name").send_keys(last)
    driver.find_element(By.ID, "postal-code").send_keys(zipcode)
    driver.find_element(By.ID, "continue").click()
    time.sleep(1)


# ====================================================
# LOGIN TESTS
# ====================================================

# TC-01
def test_login_with_correct_username_and_password(driver):
    do_login(driver, correct_username, correct_password)
    # after login i should be on the inventory page
    assert "inventory" in driver.current_url


# TC-02
def test_login_with_wrong_password(driver):
    do_login(driver, correct_username, "wrongpassword")
    # there should be an error message on the page
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-03
def test_login_with_wrong_username(driver):
    do_login(driver, "wronguser", correct_password)
    # there should be an error message on the page
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-04
def test_login_with_empty_fields(driver):
    open_website(driver)
    # i click login without typing anything
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-05
def test_locked_user_cannot_login(driver):
    do_login(driver, locked_username, correct_password)
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    # the error should say something about locked out
    assert "locked out" in error.text.lower()


# TC-06
def test_login_page_has_all_elements(driver):
    open_website(driver)
    # just checking everything is there when i open the page
    assert driver.find_element(By.ID, "user-name").is_displayed()
    assert driver.find_element(By.ID, "password").is_displayed()
    assert driver.find_element(By.ID, "login-button").is_displayed()


# ====================================================
# PRODUCT PAGE TESTS
# ====================================================

# TC-07
def test_there_are_6_products_on_the_page(driver):
    login_with_correct_user(driver)
    all_products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    # there should be exactly 6 products
    assert len(all_products) == 6


# TC-08
def test_every_product_has_name_price_and_button(driver):
    login_with_correct_user(driver)
    all_products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    for product in all_products:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name")
        price = product.find_element(By.CLASS_NAME, "inventory_item_price")
        button = product.find_element(By.TAG_NAME, "button")
        assert name.is_displayed()
        assert price.is_displayed()
        assert button.is_displayed()


# TC-09
def test_sort_by_price_low_to_high(driver):
    login_with_correct_user(driver)
    # i click the sort dropdown and pick low to high
    dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    Select(dropdown).select_by_value("lohi")
    time.sleep(1)
    # now i get all prices and check they are in order
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(p.text.replace("$", "")) for p in price_elements]
    assert prices == sorted(prices)


# TC-10
def test_sort_by_price_high_to_low(driver):
    login_with_correct_user(driver)
    dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    Select(dropdown).select_by_value("hilo")
    time.sleep(1)
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(p.text.replace("$", "")) for p in price_elements]
    assert prices == sorted(prices, reverse=True)


# TC-11
def test_sort_by_name_a_to_z(driver):
    login_with_correct_user(driver)
    dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    Select(dropdown).select_by_value("az")
    time.sleep(1)
    name_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names = [n.text for n in name_elements]
    assert names == sorted(names)


# TC-12
def test_clicking_product_opens_detail_page(driver):
    login_with_correct_user(driver)
    # i click the first product name
    driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].click()
    time.sleep(1)
    assert "inventory-item" in driver.current_url


# TC-13
def test_product_detail_page_has_all_info(driver):
    login_with_correct_user(driver)
    driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].click()
    time.sleep(1)
    # checking all the things are there on the detail page
    assert driver.find_element(By.CLASS_NAME, "inventory_details_name").is_displayed()
    assert driver.find_element(By.CLASS_NAME, "inventory_details_desc").is_displayed()
    assert driver.find_element(By.CLASS_NAME, "inventory_details_price").is_displayed()
    assert driver.find_element(By.CLASS_NAME, "btn_primary").is_displayed()


# ====================================================
# CART TESTS
# ====================================================

# TC-14
def test_adding_item_shows_badge_on_cart(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"


# TC-15
def test_button_changes_to_remove_after_adding(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    # the button should now say remove
    remove_btn = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
    assert "remove" in remove_btn.text.lower()


# TC-16
def test_removing_item_hides_the_badge(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    # now i remove it
    driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()
    time.sleep(1)
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0


# TC-17
def test_added_item_shows_in_cart_page(driver):
    login_with_correct_user(driver)
    # i save the product name before adding
    product_name = driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert cart_item.text == product_name


# TC-18
def test_cart_is_empty_if_nothing_added(driver):
    login_with_correct_user(driver)
    go_to_cart(driver)
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 0


# TC-19
def test_continue_shopping_goes_back_to_products(driver):
    login_with_correct_user(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "continue-shopping").click()
    time.sleep(1)
    assert "inventory" in driver.current_url


# ====================================================
# CHECKOUT TESTS
# ====================================================

# TC-20
def test_full_checkout_works(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    fill_checkout_form(driver, "Ahmad", "Khalil", "12345")
    driver.find_element(By.ID, "finish").click()
    time.sleep(1)
    # after finishing there should be a thank you message
    confirmation = driver.find_element(By.CLASS_NAME, "complete-header")
    assert confirmation.is_displayed()


# TC-21
def test_checkout_fails_if_first_name_is_empty(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    # i leave first name empty on purpose
    fill_checkout_form(driver, "", "Khalil", "12345")
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-22
def test_checkout_fails_if_last_name_is_empty(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    fill_checkout_form(driver, "Ahmad", "", "12345")
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-23
def test_checkout_fails_if_zip_is_empty(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    fill_checkout_form(driver, "Ahmad", "Khalil", "")
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed()


# TC-24
def test_order_summary_shows_price_and_tax(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    fill_checkout_form(driver, "Ahmad", "Khalil", "12345")
    # now i should be on the summary page
    subtotal = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
    tax = driver.find_element(By.CLASS_NAME, "summary_tax_label")
    total = driver.find_element(By.CLASS_NAME, "summary_total_label")
    assert subtotal.is_displayed()
    assert tax.is_displayed()
    assert total.is_displayed()


# TC-25
def test_cancel_checkout_goes_back_to_cart(driver):
    login_with_correct_user(driver)
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    # i click cancel instead of continuing
    driver.find_element(By.ID, "cancel").click()
    time.sleep(1)
    assert "cart" in driver.current_url


# ====================================================
# LOGOUT TESTS
# ====================================================

# TC-26
def test_logout_works_from_burger_menu(driver):
    login_with_correct_user(driver)
    # open the menu on the top left
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(1)
    # after logout i should be back on the login page
    assert driver.current_url == URL + "/"


# TC-27
def test_logged_out_user_cannot_access_inventory(driver):
    open_website(driver)
    # i try to go to inventory without logging in
    driver.get(URL + "/inventory.html")
    time.sleep(1)
    # it should redirect me back to login
    assert "inventory" not in driver.current_url
