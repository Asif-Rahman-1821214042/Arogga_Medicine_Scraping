from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time,json
# === Setup Chrome Options ===
chrome_options = Options()

# Set up WebDriver (example with Chrome)
service=Service("/usr/bin/chromedriver")

# Disable popups, ads, and notifications
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # Block notifications
    "profile.default_content_setting_values.popups": 0,         # Disable popups
    "profile.default_content_setting_values.ads": 2,            # Block ads
    "profile.managed_default_content_settings.javascript": 1    # Allow JS if needed
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")

# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options,service=service)  # Make sure chromedriver is in PATH

count=1
med_list=[]

product_cardX="//*[@class='col-md-2 col-sm-3 mb-10']"
product_imgT="img"
Product_LinkT="a"
Med_NameX=".//*[contains(@class,'product-card_product_title')]/a/div"
First_priceX=".//div[contains(@class,'product-card_price')]/del"
Second_priceT="p"



# Open the webpage
driver.get("https://www.arogga.com/category/medicine/6322/medicine")
time.sleep(10)
meds=driver.find_elements(By.XPATH,product_cardX)
print(len(meds))

while True:
    try:
        i=driver.find_element(By.XPATH,f"//*[@class='col-md-2 col-sm-3 mb-10'][{count}]")
    except:
        break
    
    #scroll to specific element
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", i)
    
    try:
        Med_Item=i.find_element(By.TAG_NAME,product_imgT)
    except:
        Med_Item=""

    try:
        Med_Name=i.find_element(By.XPATH,Med_NameX).text
    except:
        Med_Name=""

    try:
        Brand_Name=Med_Item.get_attribute("alt")
    except:
        Brand_Name=""

    try:
        Med_IMG=Med_Item.get_attribute("src")
    except:
        Med_IMG=""

    try:
        Med_Anchor=i.find_element(By.TAG_NAME,Product_LinkT).get_attribute("href")
    except:
        Med_Anchor=""
    
    try:
        Med_Prv_Price=i.find_element(By.XPATH,First_priceX).text
    except:
        Med_Prv_Price=""

    try:
        Med_Curr_Price=i.find_element(By.TAG_NAME,Second_priceT).text
    except:
        Med_Curr_Price=""
    
    med_list.append(
        {
        "Count":count,
        "Medicine Name":Med_Name,
        "Brand Name": Brand_Name,
        "Med IMG":Med_IMG,
        "Med Link":Med_Anchor,
        "Previous Price,":Med_Prv_Price,
        "Current Price,":Med_Curr_Price
        }
        )
    print({
        "Count":count,
        "Medicine Name":Med_Name,
        "Brand Name": Brand_Name,
        "Med IMG":Med_IMG,
        "Med Link":Med_Anchor,
        "Previous Price,":Med_Prv_Price,
        "Current Price,":Med_Curr_Price
        })
    count=count+1



with open("Arogga_Medicine_Data.json", "w", encoding="utf-8") as m:
    json.dump(med_list, m, indent=4, ensure_ascii=False)