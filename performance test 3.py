import subprocess
import time
import os
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from urllib.parse import quote_plus  # Add this import for URL encoding

# Define the URLs
login_url = "https://vlearnv.herovired.com/"
dashboard_url = "https://vlearnv.herovired.com/"

# Login credentials
username = "nitisha.piplani@herovired.com"
password = "Hero@123"

# Path to Chrome executable
chrome_executable_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Path to reports folder
reports_folder = ""

# Create the reports folder if it doesn't exist
if not os.path.exists(reports_folder):
    os.makedirs(reports_folder)

# Configure Chrome options for Lighthouse
lighthouse_options = ['--disable-device-emulation', '--disable-network-throttling', '--disable-cpu-throttling', '--output=json']

# Set up ChromeDriver using chromedriver_manager
service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # Remove headless mode
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Login to the website
    driver.get(login_url)
    print("Logging in...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button[2]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/input[1]"))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/input[2]"))).send_keys(password)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button"))).click()
    print("Logged in successfully.")

    # Wait for the dashboard page to load
    WebDriverWait(driver, 60).until(EC.url_to_be(dashboard_url))
    print("Dashboard page loaded.")

    # Extract all the URLs to navigate
    all_links = driver.find_elements(By.XPATH, "//a[@href]")
    all_urls = [link.get_attribute("href") for link in all_links]

    # Remove None and duplicate URLs
    all_urls = list(filter(None, all_urls))
    all_urls = list(set(all_urls))

    # Run Lighthouse for each page
    for url in all_urls:
        encoded_url = quote_plus(url)  # Encode the URL
        output_file = os.path.join(reports_folder, f"report_{encoded_url.replace('/', '_')}.json")
        lighthouse_command = f'"{chrome_executable_path}" --remote-debugging-port=9222 --no-first-run --no-default-browser-check {encoded_url} {" ".join(lighthouse_options)} --output-path="{output_file}"'
        subprocess.run(lighthouse_command, shell=True)
        print(f"Lighthouse report for page {url} saved.")

    # Combine reports into a single DataFrame
    combined_df = pd.DataFrame()
    for file in os.listdir(reports_folder):
        if file.endswith(".json"):
            file_path = os.path.join(reports_folder, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
                df = pd.json_normalize(data)
                combined_df = combined_df.append(df, ignore_index=True)

    # Convert DataFrame to Excel
    excel_output_path = "combined_report.xlsx"
    combined_df.to_excel(excel_output_path, index=False)
    print(f"Combined report saved as {excel_output_path}")

except TimeoutException:
    print("Timeout occurred while waiting for the dashboard page to load.")
except NoSuchElementException:
    print("Element not found.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()