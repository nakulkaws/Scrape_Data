import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import re

now = datetime.now()
dt_string = now.strftime("%d%m%Y-%H%M%S")

products=[] #List to store name of the product
prices=[] #List to store price of the product
quantities=[]

priceregex=re.compile(r'\d*\.\d*')
nameregx=re.compile(r'(.*?)(\d.*|each.*|whole.*|box.*|tp.*|per.*|kg.*|one.*|two.*|three.*|four.*)', re.I)

def extract_data(soup):

    for div in soup.findAll('div', attrs={'class':'col-md-3 p-0'}): # cat-item
        name=div.find('span', attrs={'class':'clsgetname'})
        price=div.find('span', attrs={'id':'final_price'})

        namelist=nameregx.findall(name.text)
        if namelist:
            # names=re.sub(r'[-\s]*$','',namelist[0][0])
            names=re.sub(r'[-\s\(]*$','',namelist[0][0])
            # qty=re.sub(r'^[-\s]*','',namelist[0][1])

            qty=re.sub(r'[-\s\)]*$','',namelist[0][1])
            qty=re.sub(r'[\(\)]*','',qty)

        cleanprice=priceregex.findall(price.text)

        products.append(names)
        prices.append(cleanprice[0])
        quantities.append(qty)
        # prices.append(re.sub(r'^\‚\Ç\π\s','',price.text))

def jio():
    url ="https://www.jiomart.com/category/groceries/fruits-vegetables"
    # old url
    # "https://www.jiomart.com/category/fruits-vegetables"
    driver = webdriver.Chrome("/users/nitipuri/Downloads/ScrapeData/chromedriver") #Edit path of chromedriver accordingly
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    # Set Pincode
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rel_pin_msg")))
    csssel="#rel_pincode"
    pincode=driver.find_element_by_css_selector(csssel)
    pincode.send_keys("122018")
    time.sleep(2)

    # Click Button
    # Button Changed on 11 Jun 2020
    # csssel="#rel_pincode_form > div.lblock > button"
    csssel="#rel_pincode_form > div.pin_detail > button.apply_btn"
    shop=driver.find_element_by_css_selector(csssel)
    shop.click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "delivering_to")))
    time.sleep(2)

    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    extract_data(soup)

    try:
        nextpage=driver.find_element_by_xpath("//*[@id=\"mstar_box\"]/div/div/div/div[22]/ul/li/a")

    except:
        nextpage=False

    while nextpage:
        nextpage.click()
        # ActionChains(driver).click(nextpage).perform()
        time.sleep(2)
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")
        extract_data(soup)

        try:
            nextpage=driver.find_element_by_xpath("//*[@id=\"mstar_box\"]/div/div/div/div[22]/ul/li[2]/a")
        except:
            nextpage=False
            break

    df = pd.DataFrame({'name':products, 'qty':quantities, 'price':prices})
    file_name="jio-"+dt_string+".csv"
    df.to_csv(file_name, index=False, encoding='utf-8')
    driver.quit()

jio()
