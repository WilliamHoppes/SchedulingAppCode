
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#https://scrapingant.com/blog/selenium-python-find-element
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

output_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppTestingGround/01RawWebsiteSnapshots"

#https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver
def capture_website_screenshot(url, output_path):
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    service = Service(executable_path="C:/Users/hoppe/Documents/SchedulingApp/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    browser=webdriver.Chrome(service=service, options=chrome_options)

    try:
        browser.get(url)
        time.sleep(3)
        el=browser.find_element(By.TAG_NAME, "body")
        el.screenshot(output_path)
        print(url+" done")
    finally:
        browser.quit()

capture_website_screenshot("https://continentalclub.com/houston", output_path=output_path+"/ContinentalClub.png")
capture_website_screenshot("https://iondistrict.com/events/month/2025-04/", output_path=output_path+"/IonDistrict.png")

