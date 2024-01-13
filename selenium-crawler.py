#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service as Service
# from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# !venv/bin/pip install webdriver-manager


# In[3]:


# driver = webdriver.Chrome(ChromeDriverManager().install())


# In[4]:


# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'


# In[5]:


options = Options()
options.headless = True
# options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("headless")
options.add_argument("--headless")
options.add_argument("--incognito")
browser = webdriver.Firefox(options=options)
# browser.implicitly_wait(100)


# In[6]:


browser.get(list_link)


# In[7]:


# Accept cookies parameters
try:
    browser.get_screenshot_as_file("cookies.png")
    btn = browser.find_elements(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
    browser.find_element(By.CSS_SELECTOR, '#focus-lock-id')
except:
    print('Error cookies acceptance')


# In[8]:


items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel')


# In[9]:


if len(items) == 0:
    raise Exception('No iPhone 15 item')
if len(items) == 2:
    raise Exception('Multiple iPhone 15 item')


# In[10]:


link_from_list = items[0]
browser.get_screenshot_as_file("test_failure.png")
print(link_from_list)
detail_link = link_from_list.get_attribute('href')
print(detail_link)
exit()
if detail_link in ['https://www.jusit.ch/#', '#']:
    # raise Exception('Detail link not fetch properly')
    print('Detail link not fetch properly')
    exit()
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




