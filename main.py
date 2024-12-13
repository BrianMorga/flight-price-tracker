import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def generate_date_ranges(vacation_days: int):
    start_date = datetime(2025, 1, 1)  # Start from January 1, 2025
    end_date = start_date + timedelta(days=365)  # One year from the starting date
    date_ranges = []

    current_departure = start_date
    while current_departure <= end_date:
        return_date = current_departure + timedelta(days=vacation_days)
        if return_date <= end_date:
            date_ranges.append((current_departure.strftime("%m-%d-%Y"), return_date.strftime("%m-%d-%Y")))
        current_departure += timedelta(days=1)  # Move to the next possible departure date

    return date_ranges


# Get user inputs
departure_city = input("Enter the departure city (e.g., LAX): ")
destination_city = input("Enter the destination city (e.g., JFK): ")
vacation_days = int(input("Enter the number of days for vacation: "))

# Generate date ranges
date_ranges = generate_date_ranges(vacation_days)

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Google Flights
driver.get("https://www.google.com/flights")
time.sleep(2)

# Input departure location
departure_location = driver.find_element(By.XPATH, "//div[@id='i23']/div/div/div/div/div/div/input")
departure_location.clear()
departure_location.send_keys(departure_city)

# Wait for suggestions to load
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab

# Input destination location
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(destination_city).perform()
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab
time.sleep(1)
# Input date range (taking the first range as an example)
departure_date, return_date = date_ranges[0]
webdriver.ActionChains(driver).send_keys(departure_date).perform()
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(return_date).perform()
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Press Tab
webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()  # Press ENTER

# Submit the search
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Move to the search button
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()  # Press Enter
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
time.sleep(.5)
webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
time.sleep(.5)

for departure_date, return_date in date_ranges:
    # Click the departure date box
    new_departure_date = driver.find_element(By.CSS_SELECTOR,
                                             "#yDmH0d > c-wiz.zQTmif.SSPGKf > div > div:nth-child(2) > c-wiz > div.cKvRXe > c-wiz > div.PSZ8D.EA71Tc > div.Ep1EJd > div > div.rIZzse > div.bgJkKe.K0Tsu > div > div > div.cQnuXe.k0gFV > div > div > div:nth-child(1) > div > div.GYgkab.YICvqf.kStSsc.ieVaIb > div > input")
    new_departure_date.click()
    time.sleep(.5)

    # Enter the departure date
    webdriver.ActionChains(driver).send_keys(departure_date).perform()
    time.sleep(.5)
    webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Move to the return date field
    time.sleep(.5)

    # Enter the return date
    webdriver.ActionChains(driver).send_keys(return_date).perform()
    time.sleep(.5)
    webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()  # Update the page
    time.sleep(.5)
    webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(1)

# Keep the browser open for further actions
time.sleep(30)

# Close the browser
# driver.quit()
