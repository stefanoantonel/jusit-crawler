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


# In[2]:


# get_ipython().system('rm -f ./*.png')


# In[3]:


list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'


# In[4]:


options = Options()
options.headless = True
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("headless")
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--window-size=800,600")
browser = webdriver.Chrome(options=options)
# browser.implicitly_wait(5)
browser.delete_all_cookies()


# In[5]:


# browser.set_network_conditions(
#     offline=False,
#     latency=5000,  # additional latency (ms)
#     download_throughput=100 * 1024,  # maximal throughput
#     upload_throughput=500 * 1024  # maximal throughput
# )


# In[6]:


browser.get(list_link)
browser.get_screenshot_as_file("after got link.png")


# In[7]:


def remove_cookie_banner():
    delay = 5
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


items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel')
print('items', items)


# In[10]:


if len(items) == 0:
    raise Exception('No iPhone 15 item')
if len(items) == 2:
    raise Exception('Multiple iPhone 15 item')


# In[11]:


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
        raise Exception('Check page')    
print('Detail page not available yet...')
browser.get_screenshot_as_file("details.png")
browser.quit()

