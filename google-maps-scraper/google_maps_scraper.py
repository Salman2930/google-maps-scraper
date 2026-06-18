from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as DS
import time
import pandas as pd
import requests
import re

# set driver path

path = r"C:\webdrivers\chromedriver.exe"

options = Options()
options.add_argument("--start-maximized")

service = Service(path)
driver = webdriver.Chrome(service=service, options=options)
#define base url
driver.get("https://www.google.com/maps")
time.sleep(5)
search_box = driver.find_element(By.NAME, "q")

search_box.clear()

search_box.send_keys("Hospitals in Chennai")

search_box.send_keys(Keys.ENTER)

time.sleep(8)

scroll_panel = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

last_count = 0

for i in range(15):

    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight",
        scroll_panel
    )

    time.sleep(3)

    cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")

    current_count = len(cards)

    print(f"Scroll {i+1} -> {current_count} cards")

    if current_count == last_count:
        print("No new cards loaded")
        break

    last_count = current_count

print("Final Cards:", last_count)
data = []

for card in cards[:2]:
    name = None
    rating = None
    reviews = None
    phone = None
    maps_url = None
    website = None

    try:
        name = card.find_element(By.CSS_SELECTOR, "div.qBF1Pd").text
    except:
        pass

    try:
        rating = card.find_element(By.CSS_SELECTOR, "span.MW4etd").text
    except:
        pass

    try:
        reviews = card.find_element(By.CSS_SELECTOR, "span.UY7F9").text
    except:
        pass

    try:
        phone = card.find_element(By.CSS_SELECTOR, "span.UsdlK").text
    except:
        pass

    try:
        maps_url = card.find_element(By.CSS_SELECTOR, "a.hfpxzc").get_attribute("href")
    except:
        pass

    try:
        website = card.find_element(By.CSS_SELECTOR, "a[data-value='Website']").get_attribute("href")
    except:
        pass

    print({
        "name": name,
        "rating": rating,
        "reviews": reviews,
        "phone": phone,
        "website": website,
        "maps_url": maps_url
    })
    


cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
print("Loaded cards:", len(cards))

for index, card in enumerate(cards, start=1):

    def get_text(selector):
        try:
            return card.find_element(By.CSS_SELECTOR, selector).text
        except:
            return None

    def get_href(selector):
        try:
            return card.find_element(By.CSS_SELECTOR, selector).get_attribute("href")
        except:
            return None

    item = {
        "name": get_text("div.qBF1Pd"),
        "rating": get_text("span.MW4etd"),
        "reviews": get_text("span.UY7F9"),
        "phone": get_text("span.UsdlK"),
        "website": get_href("a[data-value='Website']"),
        "maps_url": get_href("a.hfpxzc")
    }

    data.append(item)
    print(index, "done:", item["name"])

df = pd.DataFrame(data)

df = df.drop_duplicates(subset=["maps_url"])

print(df.shape)
print(df.head())

df.to_csv(
    "google_maps_hospitals_chennai_100+_plus.csv",
    index=False,
    encoding="utf-8-sig"
)