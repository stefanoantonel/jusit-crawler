#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
import requests
import sys


# In[ ]:


# !rm -f ./*.png


# In[ ]:


# only for iphone 15
api_link = 'https://www.jusit.ch/device-details/100013812'


# In[ ]:


PRICE_LIMIT = 640
def check_prices(url):
    lowest_price = 10000
    print(url)
    r = requests.get(url)
    payload = r.json()
    iphones = payload['data']['articles']
    for iphone in iphones:
        for category in ['salesPrice', 'salesPriceDiscounted']:
            if category in iphone['price']:
                price = iphone['price'][category]
                if lowest_price > price:
                    lowest_price = price
                if price < PRICE_LIMIT:
                    raise Exception('iPhone found')
    print('Lowest price', lowest_price)


# In[ ]:


try:
    check_prices(api_link)
    sys.exit(0)
except Exception as e:
    print(e)
    print('Issue with the API. Fetching whole page ....')


# In[ ]:


list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'


# In[ ]:


options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--window-size=800,600")
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(5)
browser.delete_all_cookies()
delay = 5


# In[ ]:


# browser.set_network_conditions(
#     offline=False,
#     latency=500,  # additional latency (ms)
#     download_throughput=300 * 1024,  # maximal throughput
#     upload_throughput=500 * 1024  # maximal throughput
# )


# In[ ]:


browser.get(list_link)
browser.get_screenshot_as_file("after got link.png")


# In[ ]:


def remove_cookie_banner():
    try:
        WebDriverWait(browser, delay).until(
          EC.presence_of_element_located((By.ID, 'usercentrics-root'))
        )
        banner_container = browser.find_element(By.ID, "usercentrics-root")
        print('banner_container', banner_container)
        browser.execute_script("""
           var l = document.getElementById("usercentrics-root");
           if (!l) return;
           l.parentNode.removeChild(l);
        """)
    except TimeoutException:
        print("Cookie banner did not show up")


# In[ ]:


remove_cookie_banner()
browser.get_screenshot_as_file("after removing cookie banner.png")


# In[ ]:


WebDriverWait(browser, delay).until(
  EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item-panel__title'))
)
WebDriverWait(browser, delay).until(
  EC.presence_of_element_located((By.CSS_SELECTOR, 'a.item-panel[href]'))
)
items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel[href]')
print('items', items)
for i in items:
    print(i.get_attribute('href'))


# In[ ]:


if len(items) != 1:
    browser.get_screenshot_as_file("list issue with items.png")
    raise Exception('List has an issue')


# In[ ]:


link_from_list = browser.find_element(By.CSS_SELECTOR, 'a.item-panel[href]')
browser.get_screenshot_as_file("before detail link.png")
detail_link = link_from_list.get_attribute('href')
print(detail_link)


# In[ ]:


if detail_link in ['https://www.jusit.ch/#', '#']:
    print('Detail link not fetch properly')
    raise Exception('Detail link not fetch properly')


# In[ ]:


browser.get(detail_link)
remove_cookie_banner()


# In[ ]:


not_found_titles = browser.find_elements(By.CSS_SELECTOR, 'h4')
for not_found in not_found_titles:
    text = not_found.get_attribute('innerText')
    if text not in ['Dommage.', "La page n'a pas été trouvée."]:
        url = f"https://www.jusit.ch/device-details/{detail_link.split('/').pop()}"
        discount_found = check_prices(url)
        if discount_found:
            raise Exception('Check page')    
print('Detail page not available yet...')
browser.get_screenshot_as_file("details.png")
browser.quit()


# In[ ]:




