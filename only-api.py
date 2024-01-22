#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import sys


# In[ ]:


query = 'https://www.jusit.ch/jusit-search?filter%5Bbrand%5D=Apple&filter%5Bmodel%5D=iPhone%2015%205Gjusit&filter%5BpriceMin%5D=200&filter%5BpriceMax%5D=1100'
headers = {
    'authority': 'www.jusit.ch',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'de-CH',
}
r = requests.get(query, headers=headers)


# In[ ]:


items = r.json()['data']


# In[ ]:


if len(items) != 1:
    print(items)
    raise Exception('Multiple items were found')


# In[ ]:


iphone_url = items[0]['url']
api_link = url = f"https://www.jusit.ch/device-details/{iphone_url.split('/').pop()}"
print('api_link', api_link)


# In[ ]:


PRICE_LIMIT = 640
def check_prices(url):
    lowest_price = 10000
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




