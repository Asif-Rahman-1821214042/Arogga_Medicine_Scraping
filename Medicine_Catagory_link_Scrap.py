from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time,json
import csv
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

Med_Link_Catagory_List=[]

# Meta Data
Catagory_X="//body/div[@class='d-flex']/div[@class='sidebar_position_style']/div[@class='sidebar_wrap']/div[@class='sidebar']/div[@class='sidebar-menu_menu_wrapper__JZutP']/div[@class='sidebar-menu_group__7xPbx']/div[@class='sidebar-menu_group_items__elc7Q sidebar-menu_group_items_animation__9gY96']/div"


# Open the webpage
driver.get("https://www.arogga.com/category/medicine/6322/medicine")
time.sleep(5)

anchor_div=driver.find_elements(By.XPATH,Catagory_X)

for i in anchor_div:
    # Med_Link_Catagory_List.append(i.find_element(By.TAG_NAME,"a").get_attribute("href"))
    i.click()
    time.sleep(5)
    sub_catagorys=driver.find_elements(By.XPATH,"//body/div[@class='d-flex']/div[@class='sidebar_position_style']/div[@class='sidebar_wrap']/div[@class='sidebar']/div[@class='sidebar-menu_menu_wrapper__JZutP']/div[@class='sidebar-menu_group__7xPbx']/div[@class='sidebar-menu_group_items__elc7Q sidebar-menu_group_items_animation__9gY96']/div/div[2]/div")
    for z in sub_catagorys:
        Med_Link_Catagory_List.append(z.find_element(By.TAG_NAME,"a").get_attribute("href"))
    print("Done")

print(Med_Link_Catagory_List)

with open("catagory_condom.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Catagory_Link"])
    for item in Med_Link_Catagory_List:
        writer.writerow([item])