import time
import sqlite3
import re
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

def setup_database():
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_date TEXT,
            return_date TEXT,
            airline TEXT,
            price INT,
            flight_duration TEXT,
            departure_time TEXT,
            arrival_time TEXT
        )
    """)
    conn.commit()
    return conn

def insert_into_db(conn, departure_date, return_date, airline, price,flight_duration, dep_time, arr_time):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO flights (departure_date, return_date, airline, price, flight_duration,departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (departure_date, return_date, airline, price, flight_duration, dep_time, arr_time))
    conn.commit()

def extract_airline_name(flight_text):
    major_airlines = ["Delta", "United", "Spirit", "Frontier", "American", "Southwest", "WestJet",
                      "Alaska", "JetBlue", "Hawaiian", "Allegiant", "Air Europa", "Emirates", "Key Lime Air",
                      "Qatar Airways", "Royal Air Maroc", "Sun Country Airlines"]
    for airline in major_airlines:
        if airline.lower() in flight_text.lower():
            return airline
    return "Unknown"

def scrape_top_flights(driver, departure_date, return_date, conn):
    # List of alternative XPaths to locate the flights section
    xpaths = [
        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div[2]/div[1]/ul',
        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div[2]/div[1]/ul'
    ]

    flights_section = None

    # Try each XPath until the element is found
    for xpath in xpaths:
        try:
            flights_section = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            print(f"Successfully found flights section with XPath: {xpath}")
            break  # Exit the loop once the element is found
        except Exception as e:
            print(f"XPath failed: {xpath} - {e}")

    if not flights_section:
        print(f"Failed to locate the flights section for {departure_date} - {return_date}")
        return  # Exit the function if no valid XPath works

    # Locate the <ul> containing the flight information
    try:
        list_items = flights_section.find_elements(By.TAG_NAME, "li")

        print(f"Flight details for {departure_date} to {return_date}:")
        for idx, item in enumerate(list_items, start=1):
            flight_text = item.text.strip()
            print(f"{idx}. {flight_text}")

            # Extract key flight details
            try:
                dep_time = re.search(r"(\d{1,2}:\d{2} [APM]{2})", flight_text).group(1)  # Departure time
                arr_time = re.findall(r"(\d{1,2}:\d{2} [APM]{2})", flight_text)[-1]  # Arrival time
                airline_name = extract_airline_name(flight_text)  # Extract airline name
                flight_duration = re.search(r"(\d+ hr \d+ min|\d+ hr|\d+ min)", flight_text).group(1)  # Duration
                # Extract price and remove commas
                price_match = re.search(r"\$([\d,]+)", flight_text)
                if price_match:
                    price = int(price_match.group(1).replace(",", ""))  # Remove commas and convert to INT
                else:
                    price = None  # Handle cases where price is not found

                # Insert into the database
                insert_into_db(conn, departure_date, return_date, airline_name, price, flight_duration, dep_time, arr_time)
                print(f"Inserted: {airline_name}, {dep_time} - {arr_time}, {flight_duration}, ${price}")

            except AttributeError:
                print(f"Could not parse flight details for item {idx}: {flight_text}")

    except Exception as e:
        print(f"Error parsing flight details: {e}")

# Get user inputs
departure_city = input("Enter the departure city (e.g., LAX): ")
destination_city = input("Enter the destination city (e.g., JFK): ")
vacation_days = int(input("Enter the number of days for vacation: "))

# Generate date ranges
date_ranges = generate_date_ranges(vacation_days)

# Setup database
conn = setup_database()

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
    scrape_top_flights(driver, departure_date, return_date, conn)

# Keep the browser open for further actions
time.sleep(30)

# Close the browser
# driver.quit()
