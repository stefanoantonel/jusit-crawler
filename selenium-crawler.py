#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
import requests


# In[2]:


# !rm -f ./*.png


# In[3]:


list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'


# In[4]:


options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--window-size=800,600")
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(5)
browser.delete_all_cookies()
delay = 5


# In[5]:


# browser.set_network_conditions(
#     offline=False,
#     latency=1000,  # additional latency (ms)
#     download_throughput=300 * 1024,  # maximal throughput
#     upload_throughput=500 * 1024  # maximal throughput
# )


# In[6]:


browser.get(list_link)
browser.get_screenshot_as_file("after got link.png")


# In[7]:


def remove_cookie_banner():
    try:
        wrapper = WebDriverWait(browser, delay).until(
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

browser.get_screenshot_as_file("after removing cookie banner.png")


# In[8]:


remove_cookie_banner()


# In[9]:


wrapper = WebDriverWait(browser, delay).until(
  EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item-panel__title'))
)
items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel')
print('items', items)


# In[10]:


if len(items) != 1:
    browser.get_screenshot_as_file("list issue with items.png")
    raise Exception('List has an issue')


# In[11]:


PRICE_LIMIT = 640
def check_prices(iphone_id):
    lowest_price = 10000
    r = requests.get(f"https://www.jusit.ch/device-details/{iphone_id}")
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


# In[12]:


link_from_list = items[0]
browser.get_screenshot_as_file("before detail link.png")

detail_link = link_from_list.get_attribute('href')
print(detail_link)

if detail_link in ['https://www.jusit.ch/#', '#']:
    print('Detail link not fetch properly')
    raise Exception('Detail link not fetch properly')

browser.get(detail_link)
not_found_titles = browser.find_elements(By.CSS_SELECTOR, 'h4')
for not_found in not_found_titles:
    text = not_found.get_attribute('innerText')
    if text not in ['Dommage.', "La page n'a pas été trouvée."]:
        discount_found = check_prices(detail_link.split('/').pop())
        if discount_found:
            raise Exception('Check page')    
print('Detail page not available yet...')
browser.get_screenshot_as_file("details.png")
browser.quit()


# In[ ]:




