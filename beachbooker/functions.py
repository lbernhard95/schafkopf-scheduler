from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options


import time
import random

from core.log import logger


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def close_driver(driver):
    driver.close()


def login(driver, username, password):
    driver.get("https://ssl.forumedia.eu/zhs-courtbuchung.de/reservations.php?action=showRevervations&type_id=2")

    logger.info("Logging in")
    driver.find_element(By.ID, "login_block").click()
    driver.find_element(By.ID, "login").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Anmelden']").send_keys(Keys.RETURN)
    time.sleep(5)  # Wait a bit for page to be loaded

    try:
        driver.find_element(By.CLASS_NAME, "outlogin")
        logger.info("Login successful!")
    except Exception as e:
        logger.error("Something went wrong.")
        logger.error(e)


def find_and_book_slots(driver, booking_date, booking_times):
    """
    Returns True if an available slot for each time in booking_times on booking_date on one field was found
    """
    logger.info(f"Looking for {booking_times} on {booking_date}")

    for page in [1, 2]:
        # Go through each page
        driver.get(
            f"https://zhs-courtbuchung.de/reservations.php?action=showRevervations&type_id=2&date={booking_date}&page={page}"
        )
        fields = driver.find_elements(By.XPATH, "//form[@action='reservation_order.php']")

        slot_collection = []

        for field in fields:
            # Go through each field
            field_name = field.find_element(By.XPATH, ".//th").text
            logger.info(f"Searching through {field_name}")

            available_slots = field.find_elements(By.XPATH, ".//input[@type='checkbox']")
            for slot in available_slots:
                if any(booking_time in slot.get_attribute("name") for booking_time in booking_times):
                    # If current slot time is in desired booking times
                    logger.info(f"Slot found: {slot.get_attribute('name')} on field {field_name}")

                    slot_collection.append(slot)

                    if len(slot_collection) == len(booking_times):
                        # If there is a slot on current field for each requried time

                        # Mark slots found
                        for slot in slot_collection:
                            time.sleep(random.uniform(0.2, 0.9))  # Wait a bit to fool captcha
                            driver.execute_script("arguments[0].click();", slot)

                        try:
                            # Book slots
                            logger.info("Booking...")
                            button_book = field.find_element(By.XPATH, ".//input[@type='submit'][@value='Buchung']")
                            driver.execute_script("arguments[0].click();", button_book)

                            # print(driver.page_source)

                            time.sleep(random.uniform(2.5, 3.5))  # Wait a bit for the next page to be loaded
                            button_confirm = driver.find_element(By.XPATH, "//input[@type='submit'][@value='Bestätigen']")
                            driver.execute_script("arguments[0].click();", button_confirm)

                            # Check if booking was successful
                            time.sleep(random.uniform(2.5, 3.5))  # Wait a bit for the next page to be loaded
                            try:
                                driver.find_element(By.XPATH, "//h2[text()='Vielen Dank']")
                                return "success"
                            except Exception as e:
                                if "captcha" in driver.page_source:
                                    return "captcha"
                                else:
                                    logger.error("Something unforeseen went wrong.")
                                    logger.error(e)
                                    logger.error("SOURCE:")
                                    logger.error(driver.page_source)
                                    return "error"

                        except Exception as e:
                            if "Mindestbuchungszeit" in driver.page_source:
                                return "mindestbuchungszeit"
                            else:
                                logger.error(e)
                                logger.error(driver.page_source)
                                return "error"

            if len(slot_collection) == len(booking_times):
                # If all required slots were found (break field loop)
                break
            else:
                if len(slot_collection) > 0:
                    logger.error("However, no slots available for all required times")

        if len(slot_collection) == len(booking_times):
            # If all required slots were found (break page loop)
            break

    if len(slot_collection) < len(booking_times):
        return "not_enough_slots"
