from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

output_path = "C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppTestingGround/01RawWebsiteSnapshots"

for f in os.listdir(output_path):
    print(f)

def capture_website_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    service = Service(executable_path="C:/Users/hoppe/Documents/SchedulingApp/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        browser.get(url)
        time.sleep(15)  # Give the page time to load
        
        # Get the full height of the page
        total_height = browser.execute_script("return document.body.parentNode.scrollHeight")
        total_width = browser.execute_script("return document.body.parentNode.scrollWidth")
        
        # Set the browser size to capture everything
        browser.set_window_size(total_width, total_height)
        
        # Wait for the resize to take effect
        time.sleep(10)
        
        # Take a screenshot of the entire page
        browser.save_screenshot(output_path)
        print(url + " done")
    finally:
        browser.quit()

capture_website_screenshot("https://continentalclub.com/houston", output_path=output_path+"/ContinentalClub.png")
capture_website_screenshot("https://iondistrict.com/events/month/2025-04/", output_path=output_path+"/IonDistrict.png")
capture_website_screenshot("https://www.threads.net/@sbchoustoncentral", output_path=output_path+"/SilentReadingGroup.png")