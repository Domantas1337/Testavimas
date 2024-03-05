import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options




def read_file_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return lines  # Assuming the first line is email, the second line is password

# Here you specify the paths to your data files
credentials_files = [
    'data1.txt',
    'data2.txt'
]

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(options=options)
    driver.get('https://demowebshop.tricentis.com/')
    yield driver 
    driver.quit()

# Parametrize decorator to run the test function for each credentials file
@pytest.mark.parametrize("file_path", credentials_files)
def test_webshop_login(driver, file_path):
    
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/login']"))
    )
    login_link.click()

    email_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Email"))
    )
    email_form.clear()
    email_form.send_keys("last@mail.com")

    password_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Password"))
    )
    password_form.clear()
    password_form.send_keys("password")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Log in']"))
    )
    login_button.click()

    digital_downloads_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/digital-downloads']"))
    )
    digital_downloads_link.click()

    items_to_buy = read_file_data(file_path)
    
    expected_quantity = 0
    for item in items_to_buy:
        

        print(item)

        item_title_xpath = f"//h2[contains(@class, 'product-title')]/a[text()='{item}']"
        
        title_element = driver.find_element(By.XPATH, item_title_xpath)

        add_to_cart_button = title_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'details')]//input[@value='Add to cart']")
        add_to_cart_button.click()

        cart_quantity_updated = WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.CLASS_NAME, 'cart-qty').text != ("(" + str(expected_quantity) +")")
        )

        
    shopping_cart_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/cart']"))
    )
    shopping_cart_link.click()

    print("neeee")

    terms_check_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='termsofservice']"))
    )
    terms_check_box.click()

    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='checkout']"))
    )
    checkout_button.click()

    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BillingNewAddress_CountryId"))
        )
        select = Select(dropdown)
        select.select_by_visible_text("Canada")

        city_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BillingNewAddress_City"))
        )
        city_form.clear()
        city_form.send_keys("city")

        city_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BillingNewAddress_Address1"))
        )
        city_form.clear()
        city_form.send_keys("address")

        city_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BillingNewAddress_ZipPostalCode"))
        )
        city_form.clear()
        city_form.send_keys("12345")

        city_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BillingNewAddress_PhoneNumber"))
        )
        city_form.clear()
        city_form.send_keys("+12345678912")
    except (ElementNotInteractableException, NoSuchElementException, TimeoutException):
        pass

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='billing-buttons-container']//input[@title='Continue']"))
    )
    continue_button.click()

    payment_continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='payment-method-buttons-container']//input[@value='Continue']"))
    )
    payment_continue_button.click()

    payment_info_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='payment-info-buttons-container']//input[@value='Continue']"))
    )
    payment_info_button.click()

    confirm_order = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='confirm-order-buttons-container']//input[@value='Confirm']"))
    )
    confirm_order.click()

    section_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'section order-completed')]"))
    )

    order_success_text = section_div.find_element(By.XPATH, ".//strong").text
    print(order_success_text)

    assert "Your order has been successfully processed!" == order_success_text



