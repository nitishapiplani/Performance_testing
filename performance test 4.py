import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Define the URL
url = "https://vlearnv.herovired.com/"

# Login credentials
username = "nitisha.piplani@herovired.com"
password = "Hero@123"

# Set up ChromeDriver using chromedriver_manager
service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Uncomment to run headlessly
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Login to the website
    driver.get(url)
    print("Logging in...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button[2]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/input[1]"))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/input[2]"))).send_keys(password)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button"))).click()
    print("Logged in successfully.")

    # Wait for the dashboard page to load after login
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]")))
    print("Dashboard page loaded.")

    # Run Lighthouse
    # You can use Selenium to interact with the Chrome DevTools Protocol directly to run Lighthouse,
    # or you can use a separate library like lighthouse-python (https://github.com/GoogleChrome/lighthouse/tree/master/py)
    # for simplicity, I'll omit this part here since it requires additional setup and code.

except TimeoutException:
    print("Timeout occurred while waiting for the dashboard page to load.")
except NoSuchElementException:
    print("Element not found.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()
