from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException

import time
import random

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def close_driver(driver):
    driver.close()


def login(driver, username, userpassword):
  driver.get(f"https://ssl.forumedia.eu/zhs-courtbuchung.de/reservations.php?action=showRevervations&type_id=2")

  print("Logging in")
  driver.find_element(By.ID, "login_block").click()
  driver.find_element(By.ID, "login").send_keys(username)
  driver.find_element(By.ID, "password").send_keys(userpassword)
  driver.find_element(By.XPATH, "//input[@value='Anmelden']").send_keys(Keys.RETURN)
  time.sleep(2) # Wait a bit for page to be loaded

  try:
    driver.find_element(By.CLASS_NAME, "outlogin")
    print("Login successful!")
  except  Exception as e:
    print("Something went wrong.")
    print(e)


def find_and_book_slots(driver, booking_date, booking_times):
  """
  Returns True if an available slot for each time in booking_times on booking_date on one field was found
  """
  print(f"\nLooking for {booking_times} on {booking_date}" )

  for page in [1,2]:
    # Go through each page
    driver.get(f"https://zhs-courtbuchung.de/reservations.php?action=showRevervations&type_id=2&date={booking_date}&page={page}")
    fields = driver.find_elements(By.XPATH, "//form[@action='reservation_order.php']")

    slot_collection = []

    for field in fields:
      # Go through each field
      field_name = field.find_element(By.XPATH, './/th').text
      print(f"Searching through {field_name}")

      available_slots = field.find_elements(By.XPATH, ".//input[@type='checkbox']")
      for slot in available_slots:
        if any(booking_time in slot.get_attribute('name') for booking_time in booking_times):
          # If current slot time is in desired booking times
          print(f"Slot found: {slot.get_attribute('name')} on field {field_name}")

          slot_collection.append(slot)

          if len(slot_collection) == len(booking_times):
            # If there is a slot on current field for each requried time
            
            # Mark slots found
            for slot in slot_collection:
              time.sleep(random.uniform(0.2,0.9)) # Wait a bit to fool captcha
              driver.execute_script("arguments[0].click();", slot)

            try:
              # Book slots
              print(f"Booking...")
              button_book = field.find_element(By.XPATH, ".//input[@type='submit'][@value='Buchung']")
              driver.execute_script("arguments[0].click();", button_book)
              
              # print(driver.page_source)
  
              time.sleep(random.uniform(2.5,3.5)) # Wait a bit for the next page to be loaded
              button_confirm = driver.find_element(By.XPATH, "//input[@type='submit'][@value='Bestätigen']")
              driver.execute_script("arguments[0].click();", button_confirm)
  
              # Check if booking was successful
              time.sleep(random.uniform(2.5,3.5)) # Wait a bit for the next page to be loaded
              try:
                driver.find_element(By.XPATH, "//h2[text()='Vielen Dank']")
                return "success"
              except  Exception as e:
                if "captcha" in driver.page_source:
                  return "captcha"
                else:
                  print("Something unforeseen went wrong.")
                  print(e)
                  print("SOURCE:")
                  print(driver.page_source)
                  return "error"
                
            except Exception as e:
              if "Mindestbuchungszeit" in driver.page_source:
                return "mindestbuchungszeit"
              else:
                print(e)
                print(driver.page_source)
                return "error"

      if len(slot_collection) == len(booking_times):
        # If all required slots were found (break field loop)
        break
      else:
        if len(slot_collection) > 0:
          print("However, no slots available for all required times")

    if len(slot_collection) == len(booking_times):
      # If all required slots were found (break page loop)
      break

  if len(slot_collection) < len(booking_times):
    return "not_enough_slots"