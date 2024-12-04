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

def get_user_input():
    # Prompt the user for input: origin, destination, and vacation length
    origin = input("Enter origin airport code (e.g., JFK): ")
    destination = input("Enter destination airport code (e.g., LAX): ")
    vacation_days = int(input("Enter number of days for your vacation: "))
    
    return origin, destination, vacation_days

if __name__ == "__main__":
    # Get user input
    origin, destination, vacation_days = get_user_input()
    
    # Print the user input to confirm
    print(f"\nUser Input: Origin: {origin}, Destination: {destination}, Vacation Length: {vacation_days} days")
    
    # Start Chrome and navigate to Google Flights (still here for testing purposes)
    start_chrome()
