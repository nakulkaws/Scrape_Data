from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
from requests import get
from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains

now = datetime.now()
dt_string = now.strftime("%d%m%Y-%H%M%S")

url = "https://www.bigbasket.com/"

driver = webdriver.Chrome("/users/nitipuri/Downloads/ScrapeData/chromedriver") #Edit path of chromedriver accordingly
driver.get(url)
driver.maximize_window()
time.sleep(3)

# Set location
xpath='//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/a'
dropdown=driver.find_element_by_xpath(xpath)
dropdown.click()
time.sleep(1)

cssselector='#headerControllerId > header > div > div > div > div > ul > li:nth-child(2) > div > div > div:nth-child(2) > form > div.form-group.area-autocomplete.city-select > div'
location=driver.find_element_by_css_selector(cssselector)
location.click()

time.sleep(3)
xpath="//*[@id=\"headerControllerId\"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[1]/div/input[1]"
city=driver.find_element_by_xpath(xpath)
city.send_keys("Gurgaon")
city.send_keys(Keys.RETURN)
time.sleep(2)

xpath="//*[@id=\"areaselect\"]"
pincode=driver.find_element_by_xpath(xpath)
pincode.send_keys("122018")
time.sleep(1)
pincode.send_keys(Keys.RETURN)
time.sleep(2)

xpath='//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[3]/button'
btn=driver.find_element_by_xpath(xpath)
btn.click()
time.sleep(1)

# Load Vegetable Section
bigbasket="https://www.bigbasket.com/cl/fruits-vegetables/?nc=nb"
driver.get(bigbasket)
time.sleep(2)


show_more="#dynamicDirective > product-deck > section > div.col-md-9.wid-fix.clearfix.pl-wrap > div.col-xs-12.product-deck-container.pad-0 > div.show-more > button"
showmore=driver.find_element_by_css_selector(show_more)

#scroll down to last page
last_height=0
while showmore:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    if last_height==driver.execute_script("return document.body.scrollHeight"):
        showmore=None
    else:
        last_height = driver.execute_script("return document.body.scrollHeight")

time.sleep(2)

showmore=driver.find_element_by_css_selector(show_more)
while showmore.size['width'] != 0:
    ActionChains(driver).click(showmore).perform()
    time.sleep(2)


content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")


# BigBasket vegetable list
brands=[]
products=[] #List to store name of the product
prices=[] #List to store price of the product
quantities=[] #List to store rating of the product
packs=[]
availability=[]

for div in soup.findAll('div', attrs={'qa':'product'}):
    brand=div.find('h6', attrs={'class':'ng-binding'})
    name=div.find('a', attrs={'class':'ng-binding'})
    qty=div.find('span', attrs={'ng-bind':'vm.selectedProduct.w'})
    pack=div.find('span', attrs={'ng-bind':'vm.selectedProduct.pack_desc'})
    price=div.find('span', attrs={'ng-bind':'vm.selectedProduct.sp.replace(\'.00\', \'\')'})
    # avbl=div.find('button', attrs={'class':'btn btn-add col-xs-9'})
    # if avbl.text=="ADD":
    #     availability.append("Available")
    # else:
    #     availability.append("Out of Stock")
    products.append(name.text)
    brands.append(brand.text)
    quantities.append(qty.text)
    prices.append(price.text)
    packs.append(pack.text)



    #availabilities.append(avbl.text)
df = pd.DataFrame({'name':products,  'qty':quantities, 'Pack':packs, 'price':prices,'Brand':brands}) #, 'Available':availability })
file_name="bb-"+dt_string+".csv"
df.to_csv(file_name, index=False, encoding='utf-8')
driver.quit()
