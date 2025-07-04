import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime

output_path = "C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/01Raw_Website_Snapshots/"

file_df=pd.read_csv("C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppCode/List_of_Event_Locations.csv")

for f in os.listdir(output_path):
    print(output_path+f)

def capture_website_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
#    service = Service(executable_path="C:/Users/hoppe/Documents/SchedulingApp/chromedriver-win64/chromedriver-win64/chromedriver.exe") #This broke functionality when Chrome updated, don't know why

    browser = webdriver.Chrome(options=chrome_options)

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

current_year=str(datetime.today().year)
current_month=str(datetime.today().month)
current_month_fixed=""
if len(current_month)==1:
    current_month_fixed+="0"+current_month
else:
    current_month_fixed=current_month
current_date_yearmonth=current_year+"-"+current_month

file_urls=file_df['URL'].values.tolist()
file_names=file_df['Name'].values.tolist()
file_special=file_df['SpecialStyle'].values.tolist()

for i in range(len(file_urls)):
    if file_special[i]==0:
        capture_website_screenshot(file_urls[i], output_path=output_path+file_names[i]+".png")
    elif file_special[i]==1:
        capture_website_screenshot(file_urls[i]+current_year+"-"+current_month_fixed+"/", output_path=output_path+file_names[i]+".png")
    time.sleep(5)

