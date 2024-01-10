from selenium import webdriver
from selenium.webdriver.common.by import By

list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+15+5Gjusit'
# list_link = 'https://www.jusit.ch/fr/smartphones.html?brand=Apple&model=iPhone+14jusit'

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("headless")
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(30)

browser.get(list_link)

items = browser.find_elements(By.CSS_SELECTOR, 'a.item-panel')
if len(items) == 0:
    raise Exception('No iPhone 15 item')
if len(items) == 2:
    raise Exception('Multiple iPhone 15 item')

link_from_list = items[0]
detail_link = link_from_list.get_attribute('href')
print(detail_link)
if detail_link in ['https://www.jusit.ch/#', '#']:
    raise Exception('Detail link not fetch properly')
browser.get(detail_link)
not_found_titles = browser.find_elements(By.CSS_SELECTOR, 'h4')
for not_found in not_found_titles:
    text = not_found.get_attribute('innerText')
    if text not in ['Dommage.', "La page n'a pas été trouvée."]:
        raise Exception('Check page')    
print('Detail page not available yet...')
