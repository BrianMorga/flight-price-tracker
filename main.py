import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def start_chrome():
    # Set up Chrome options (without --headless to see the browser)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up the Chrome driver with webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Navigate to Google Flights
    driver.get('https://www.google.com/flights')
    
    # Print the title of the page to confirm it's working
    print(driver.title)  # This should print something like "Google Flights"
    
    # Wait a few seconds to ensure the page loads and you can see the browser
    time.sleep(5)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    start_chrome()
