
# Basic Webscraping with Selenium
import os
from selenium import webdriver

# keys module from the library that helps send keys to the web page: enter key, some text, etc.
# from selenium.webdriver.common.keys import keys
from selenium.webdriver.common.by import By

domain = 'http://amazon.de/'
product = 'B089HGT839'
url = os.path.join(domain,'dp', product)

PATH = os.path.join(os.path.dirname(__file__),'chromedriver') ##Same Directory as Python Program
driver = webdriver.Chrome(executable_path=PATH)
driver.get(url)

# Important Methods For Locating Elements
# find_element_by_id
# find_element_by_name
# find_element_by_xpath
# find_element_by_link_text
# find_element_by_partial_link_text
# find_element_by_tag_name
# find_element_by_class_name
# find_element_by_css_selector

def login(id,password):
    email = driver.find_element_by_id("email")
    email.send_keys(id)
    Password = driver.find_element_by_id("pass")
    Password.send_keys(password)
    button = driver.find_element_by_name("login").click()

login("YOUR_LOGIN_ID","YOUR_LOGIN_PASSWORD")

# accept cookies

try:
    cookies = driver.find_element_by_id("sp-cc-accept")
    cookies.click()
except:
    pass
# get product name and description
# pdname = driver.find_element_by_id("productTitle") - deprecated
pdname = driver.find_element(By.ID, "productTitle").text

# get product features and generate list
# details = driver.find_element_by_css_selector("#feature-bullets") - deprecated
details = driver.find_element(By.CSS_SELECTOR, "#feature-bullets")
pddetail = details.text.split("\n")[1:]

# Check for Amazon's Choice badge
amzchoice = True if driver.find_element_by_id('acBadge_feature_div') else False

driver.close()
#driver.quit()

#context manager approach to webdriver
# with webdriver.Chrome(executable_path=PATH) as driver:
#     driver.get(url)