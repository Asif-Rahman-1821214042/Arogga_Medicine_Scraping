from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time,json
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
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

# page loadout time
driver.set_page_load_timeout(40) 

# Move mouse to the button and click
actions = ActionChains(driver)

#Main Storage
count=1
Med_Link_Details_List=[]

# Meta Data
Company_NameX="//div[contains(@class,'product_product_info__5eX6G')]//div[contains(@class,'d-flex items-center hover-text-primary justify-space-between gap-10 w-full')]//div[contains(@class,'text-primary')]"
GenericX="//div[@id='generic_modal_desktop']/span"
QuantityX="//div[contains(@class,'product_product_info__5eX6G')]//div[contains(@class,'items-center px-20 product_price_container__58Ku0')]//div[contains(@class,'d-flex flex-column gap-8')]//div//span[contains(@class,'d-flex text-16 text-grey900 fw-500')]//div//span"

# Safety Advice
Safety_Advice_HeadingX="//div[contains(@class,'py-5')]/div[1]"
Safety_Advice_DefinationX="//div[contains(@class,'py-5')]/div[2]"


# Introduction
IntroductionX="//div[@id='introduction']"

# Medicine Overview
OverviewsHeadX="//div[contains(@class,'d-flex flex-column mb-10 focus')]/div[1]"
OverviewsDefX="//div[contains(@class,'d-flex flex-column mb-10 focus')]/div[2]"

# Quick Tips
QuickTipsTitleX="//div[@class='d-flex flex-column mb-10 p-10 px-20']/div"
QuickTipsUlX="//div[@class='d-flex flex-column mb-10 p-10 px-20']/ul"


#upload df
df=pd.read_csv('JSON_output_CSV.csv')

for iLink in df['Med Link']:
    # Open the webpage
    try:
        driver.get(iLink)
        time.sleep(2)
    except:
        print("Page load timed out. Stopping load.")
        driver.execute_script("window.stop();") 

    # Company Extract
    try:
        Company_Name=driver.find_element(By.XPATH,Company_NameX).text
    except:
        Company_Name=''
    

    # Generic Extract
    try:
        Generic=driver.find_element(By.XPATH,GenericX).text
    except:
        Generic=''
    
    # Quantity Extract
    try:
        Quantity=driver.find_element(By.XPATH,QuantityX).text
    except:
        Quantity=''
    

    # Safety List Storage Meomory
    Safety_Advices_List=[]
    try:
        Safety_Advice_Heading=driver.find_elements(By.XPATH,Safety_Advice_HeadingX)
        Safety_Advice_Defination=driver.find_elements(By.XPATH,Safety_Advice_DefinationX)
        for H,D in zip(Safety_Advice_Heading,Safety_Advice_Defination):
            Safety_Advices_List.append({
            H.text:D.text
        })
    except:
        pass

    #click all see more
    # time.sleep(1)
    button_len = driver.find_elements(By.XPATH, "//b[contains(text(), 'Show more')]")
    for i in range(0,len(button_len)+1):
        try:
            button = driver.find_element(By.XPATH, "//b[contains(text(), 'Show more')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)
            actions.move_to_element(button).click().perform()
        except:
            pass


    # Overview Part
    Overviews_List=[]
    try:
        OverviewsHead=driver.find_elements(By.XPATH,OverviewsHeadX)
        OverviewsDef=driver.find_elements(By.XPATH,OverviewsDefX)
        for H,D in zip(OverviewsHead,OverviewsDef):
            # Mouse Option Click
            # time.sleep(1)
            # Overview Text Extraction
            Title=H.text
            Def=D.text
            Overviews_List.append({
                Title:Def
            })
    except:
        pass



    # Quick Tips
    QuickTips_List=[]
    QuickTips_LI=[]
    try:
        QuickTipsTitle=driver.find_element(By.XPATH,QuickTipsTitleX).text
        QuickTipsUl=driver.find_elements(By.XPATH,QuickTipsUlX)
        QuickTips_List.append({"Heading":QuickTipsTitle})
        for ul in QuickTipsUl:
            QuickTips_LI.append(ul.text)
        QuickTips_List.append({"List":QuickTips_LI})
    except:
        QuickTips_List.append({"Heading":""})
        QuickTips_List.append({"List":QuickTips_LI})

    # Quick Tips Part



    Med_Link_Details_List.append({
        "Link":iLink,
        "Company Name":Company_Name,
        "Generic": Generic,
        "Quantity":Quantity,
        "Safety Advices":Safety_Advices_List,
        "Overviews List":Overviews_List,
        "Quick Tips":QuickTips_List
    })

    print({
        "Count":count,
        "Link":iLink,
        "Company Name":Company_Name,
        "Generic": Generic,
        "Quantity":Quantity,
        "Safety Advices":Safety_Advices_List,
        "Overviews List":Overviews_List,
        "Quick Tips":QuickTips_List
    })
    print('\n')
    count=count+1

    if count%200==0:
        print("Done")
        with open(f"Arogga_Medicine_Details_{count}.json", "w", encoding="utf-8") as m:
            json.dump(Med_Link_Details_List, m, indent=4, ensure_ascii=False)


with open("Arogga_Medicine_Detail_Data.json", "w", encoding="utf-8") as m:
    json.dump(Med_Link_Details_List, m, indent=4, ensure_ascii=False)


