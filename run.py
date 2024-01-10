#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import time

# # list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit&priceMin=100&priceMax=1100'
list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit&priceMin=100&priceMax=1100'

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(10)
browser.get(list_link)
html = browser.page_source
list_soup = BeautifulSoup(html, features="html.parser")
browser.quit()

print(list_link)
anchors = list_soup.findAll('a')
for a in anchors:
    print(a.get('href'))

# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# browser = webdriver.Chrome(options=options)
# browser.get(list_link)
# html = browser.page_source
# list_soup = BeautifulSoup(html, features="html.parser")

# items = list_soup.findAll('ul', attrs={'class': 'product-listing__list'})
# print('items', items)

# if len(items) == 0:
#     raise Exception('No iPhone 15 item')
# if len(items) == 2:
#     raise Exception('Multiple iPhone 15 item')

# item = items[0]
# print('items', item)

# detail_page = item.find('a').get('href')
# print('detail_page', detail_page)

# browser.get(detail_page)
# html = browser.page_source
# detail_soup = BeautifulSoup(html, features="html.parser")
# browser.quit()

# detail_titles = detail_soup.findAll('h4', attrs={'class': 'headline'})

# no_detail_information = (
#     detail_titles[0].get_text().replace('\n','').strip() == 'Dommage.' and
#     detail_titles[1].get_text().replace('\n','').strip() == "La page n'a pas été trouvée."
# )
# if no_detail_information == False:
#     raise Exception('Detail page found. Check it out')
