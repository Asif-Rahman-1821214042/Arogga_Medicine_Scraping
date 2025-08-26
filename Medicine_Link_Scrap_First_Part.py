from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, json
import pandas as pd

# === Load Category CSV ===
df = pd.read_csv('catagory_condom.csv')

# === Setup Chrome Options ===
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.popups": 0,
    "profile.default_content_setting_values.ads": 2,
    "profile.managed_default_content_settings.javascript": 1
})
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # Uncomment for headless operation

# === WebDriver Setup ===
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(options=chrome_options, service=service)

# === XPATH / TAG Constants ===
PRODUCT_CARD_XPATH = "//*[@class='col-md-2 col-sm-3 mb-10']"
PRODUCT_IMG_TAG = "img"
PRODUCT_LINK_TAG = "a"
MED_NAME_XPATH = ".//*[contains(@class,'product-card_product_title')]/a/div"
FIRST_PRICE_XPATH = ".//div[contains(@class,'product-card_price')]/del"
# SECOND_PRICE_TAG = "p"
SECOND_PRICE_TAG = ".//p[contains(@class,'product-card_price')]"

med_list = []
total_count = 1

# === Start Scraping Loop ===
for cLink in df['Catagory_Link']:
    driver.get(cLink)
    time.sleep(15)  # Wait for full page load

    count = 1
    load_track = 1

    while True:
        try:
            product_element = driver.find_element(By.XPATH, f"{PRODUCT_CARD_XPATH}[{count}]")
        except NoSuchElementException:
            break

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product_element)
        time.sleep(0.5)

        # Load more elements when needed
        if count == load_track:
            for _ in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(6)
            load_track += 200

        try:
            img_elem = product_element.find_element(By.TAG_NAME, PRODUCT_IMG_TAG)
            brand_name = img_elem.get_attribute("alt")
            med_img = img_elem.get_attribute("src")
        except NoSuchElementException:
            brand_name = ""
            med_img = ""

        try:
            med_name = product_element.find_element(By.XPATH, MED_NAME_XPATH).text
        except NoSuchElementException:
            med_name = ""

        try:
            med_anchor = product_element.find_element(By.TAG_NAME, PRODUCT_LINK_TAG).get_attribute("href")
        except NoSuchElementException:
            med_anchor = ""

        try:
            med_prev_price = product_element.find_element(By.XPATH, FIRST_PRICE_XPATH).text
        except NoSuchElementException:
            med_prev_price = ""

        try:
            # med_curr_price = product_element.find_element(By.TAG_NAME, SECOND_PRICE_TAG).text
            med_curr_price = product_element.find_element(By.XPATH, SECOND_PRICE_TAG).text
        except NoSuchElementException:
            med_curr_price = ""

        med_info = {
            "Count": total_count,
            "Medicine Name": med_name,
            "Brand Name": brand_name,
            "Med IMG": med_img,
            "Med Link": med_anchor,
            "Previous Price": med_prev_price,
            "Current Price": med_curr_price
        }
        med_list.append(med_info)
        print(med_info)

        count += 1
        total_count += 1

        # Save checkpoint every 200 products
        if total_count % 200 == 0:
            print(f"Saving checkpoint at {total_count}...")
            with open(f"Arogga_Medicine_Data_{total_count}.json", "w", encoding="utf-8") as f:
                json.dump(med_list, f, indent=4, ensure_ascii=False)

# === Save Full Dataset ===
with open("Arogga_Medicine_Data_Full_Dataset.json", "w", encoding="utf-8") as f:
    json.dump(med_list, f, indent=4, ensure_ascii=False)

# === Close Driver ===
driver.quit()
