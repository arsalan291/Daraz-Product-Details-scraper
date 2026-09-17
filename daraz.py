import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import re

options = Options()
options.add_argument("--headless=new")  # the new headless mode
options.add_argument("--window-size=1920,1080") # set screen size, otherwise screenshots will be small
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver=webdriver.Chrome(options=options)



#open the website
driver.get("https://www.daraz.pk/")

all_products = driver.find_elements(By.CSS_SELECTOR, "div.fs-card-text")

data=[] 

for card in all_products:
    try:
        title = card.find_element(By.CSS_SELECTOR, "p.fs-card-title").text
        price = card.find_element(By.CSS_SELECTOR, ".fs-card-price span.price").text
        currency = card.find_element(By.CSS_SELECTOR, "div.fs-card-price span.currency").text

        try:
            origin_price = card.find_element(By.CSS_SELECTOR, "div.fs-card-origin-price").text
        except:
            origin_price = "No discount"

      
        try:
            sold = card.find_element(By.CSS_SELECTOR, "div.fs-card-sold").text
        except:
            sold = "0"

        print(f"{title} | {currency}{price}| Origin: {origin_price} | {sold}")

        data.append([title, currency + price, origin_price, sold])

        with open('daraz_products.csv', 'w', newline='', encoding='utf-8-sig') as f:
                 writer = csv.writer(f, quoting=csv.QUOTE_ALL) # QUOTE_ALL keeps commas inside title safe
                 writer.writerow(["Title", "Current_Price", "Original_Price", "Sold"])
                 writer.writerows(data)
        
        print(f"Saved {len(data)} products to daraz_products.csv")

    except Exception as e:
        continue

driver.quit()
