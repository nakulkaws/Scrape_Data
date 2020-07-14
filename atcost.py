from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
import re

now = datetime.now()
dt_string = now.strftime("%d%m%Y-%H%M%S")


driver = webdriver.Chrome("/users/nitipuri/Downloads/ScrapeData/chromedriver") #Edit path of chromedriver accordingly
products=[]
prices=[]
quantities=[]
nonBreakSpace = u'\xa0'
nameregx=re.compile(r'(.*?)(\d.*|small.*|per.*|one.*|two.*|three.*|four.*)', re.I)
pagecountregex=re.compile(r'\((\d*)(\s*\w*\))', re.I)

def extract_data(soup):
    for div in soup.findAll('div', attrs={'class':'item product-layout'}):
        name=div.find('div', attrs={'class':'name'})
        name=name.findChildren()[0]

        price=div.find('span', attrs={'class':'price-new'})

        namelist=nameregx.findall(name.text.replace(nonBreakSpace, ' '))
        if namelist:
            names=re.sub(r'[-\s\(]*$','',namelist[0][0])
            qty=re.sub(r'[-\s\)]*$','',namelist[0][1])
            qty=re.sub(r'[\(\)]*','',qty)

        products.append(names)
        quantities.append(qty)
        prices.append(price.text[1:])
        #availabilities.append(avbl.text)

# AtCost
atcost="https://www.atcost.in/index.php?route=product/category&path=59"
driver.get(atcost)
time.sleep(3)
content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")
extract_data(soup)
time.sleep(2)
try:
    nextpage=driver.find_element_by_css_selector('#content > div > div.bottom_buttons.pagination_holder > div > div.col-sm-6.text-left > ul > li:nth-child(3) > a')
    checkpagecount=driver.find_element_by_css_selector('#content > div > div.bottom_buttons.pagination_holder > div > div.col-sm-6.text-right')
    pages=pagecountregex.findall(checkpagecount.text)
except:
    nextpage=None
pagecount=1

while nextpage:
    ActionChains(driver).click(nextpage).perform()
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    extract_data(soup)
    pagecount+=1
    if pagecount<int(pages[0][0]):
        try:
            nextpage=driver.find_element_by_css_selector('#content > div > div.bottom_buttons.pagination_holder > div > div.col-sm-6.text-left > ul > li:nth-child(3) > a')
        except:
            nextpage=None
    else:
        break


df = pd.DataFrame({'name':products, 'qty':quantities, 'price':prices})
file_name="atcost-"+dt_string+".csv"
df.to_csv(file_name, index=False, encoding='utf-8')

driver.quit()
