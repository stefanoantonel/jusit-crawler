#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# from selenium.webdriver.firefox.service import Service as Service
# from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


# In[2]:


# get_ipython().system('rm -f ./*.png')


# In[3]:


# !venv/bin/pip install webdriver-manager


# In[4]:


# driver = webdriver.Chrome(ChromeDriverManager().install())


# In[5]:


list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'


# In[6]:


options = Options()
options.headless = True
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("headless")
options.add_argument("--headless")
# options.add_argument("--incognito")
# options.add_argument("--disable-javascript")
# options.set_preference('javascript.enabled', False)
# options.add_argument("--window-size=800,600")
# options.add_experimental_option(
#   "prefs",
#   {
#     'profile.managed_default_content_settings.javascript':2
#   }
# )
browser = webdriver.Chrome(options=options)
# browser.implicitly_wait(5)
# browser.delete_all_cookies()


# In[7]:


# browser.set_network_conditions(
#     offline=False,
#     latency=5000,  # additional latency (ms)
#     download_throughput=100 * 1024,  # maximal throughput
#     upload_throughput=500 * 1024  # maximal throughput
# )


# In[8]:


browser.get(list_link)
print('Got the link')
browser.get_screenshot_as_file("after got link.png")


# In[9]:


# Accept cookies parameters
def remove_cookie_banner():
    # try:
    #     browser.get_screenshot_as_file("cookies.png")
    #     focus = browser.find_element(By.ID, 'focus-lock-id')
    #     print(focus.get_attribute('innerText'))
    
    #     # btn = browser.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
    #     # print(btn.get_attribute('innerText'))
    # except Exception as e:
    #     # print(e)
    #     print('Error cookies acceptance')
    #     raise SystemExit("Stop right there!")


    print('looking')
    sleep(5)
    banner_container = browser.find_element(By.ID, "usercentrics-root")
    print(banner_container)
    
    browser.execute_script("""
       var l = document.getElementById("usercentrics-root");
       if (!l) return;
       l.parentNode.removeChild(l);
    """)
    
    browser.get_screenshot_as_file("after removing cookie banner.png")


# In[10]:


remove_cookie_banner()


# In[11]:


items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel')
print(items)


# In[12]:


if len(items) == 0:
    raise Exception('No iPhone item')
if len(items) == 2:
    raise Exception('Multiple iPhone items')


# In[13]:


link_from_list = items[0]
print(link_from_list)

browser.get_screenshot_as_file("before detail link.png")
# remove_cookie_banner()

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


# In[ ]:





# In[ ]:




