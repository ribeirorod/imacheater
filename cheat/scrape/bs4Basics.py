# BeautifulSoup basics on scraping product information from Amazon.com 

from bs4 import BeautifulSoup
import requests
import os 

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
DOMAIN = 'http://amazon.de/'
PRODUCT = 'B089HGT839'

url = os.path.join(DOMAIN,'dp', PRODUCT)
res = requests.get(url, headers=HEADERS, allow_redirects=True)

# html.parser is used for parsing HTML documents. 
# soup is a general variable name that is used for source code definition.
soup = BeautifulSoup(res.text, 'html.parser')

# get product name and description
pdname = soup.select("#productTitle")[0].getText().strip()

# get product features and generate list
details = soup.select("#feature-bullets .a-list-item")
pddetail = [details[i].getText().strip() for i in range(0, len(details))]

# Check for Amazon's Choice badge
amzchoice = True if soup.select(".ac-badge-rectangle") else False

# Find is an inbuilt function of the library that is used to fetch the content from the source. 
# It finds the first occurrence of the element or selector. 
# Find is mainly used for extracting headings, titles, product names, etc. from the web page.

print(soup.find('title').text)
## returns title
print(soup.find('h1').text)
## return the text of first heading(h1) 
print(soup.find('div', {'class': 'tags'}))
## returns the first div tag with the class `tags`
print(soup.find('a',{'class':'tag'}).text) 
# returns the text from the anchor tag with class `tag`

# Find_ALL finds all the occurrences of the element or selector. 
# It is mainly used to scrape data from the tables, product reviews, details, 
# and listed products on a web page. It returns the output in the form of a list.

print(soup.find_all('div', {'class': 'productname'}))

# Return all the div with the class productname in a list:
productnames = soup.find_all('div', {'class': 'productname'})
for name in productnames:
    print(name.text)


from typing import List, Optional, Dict, Boolean as Bool

from collections import defaultdict, namedtuple

Query = defaultdict(str)

# 
# class Query(str):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__ (*args, **kwargs)

# Basic query compiler for DBT:
class BasicQuerySelector:

    defaults = {'limit': 500, 'all':'*'}
    
    def __init__(self, table_name: str,  preview:Bool = True)-> None:
        self.table_name= table_name
        self.preview= preview



#def selelctor ()-> Query:
#declare input fields as optional