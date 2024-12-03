import requests
import json

# >>>>>>>>>> Check model available
query = 'https://www.jusit.ch/jusit-search?filter%5Bbrand%5D=Samsung'
headers = {
    'authority': 'www.jusit.ch',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'de-CH',
    'cache': 'no-cache'
}
r = requests.get(query, headers=headers)


items = r.json()['data']

for item in items:
    print(item["name"])
    if item["name"] == 'Galaxy S23 +' or item["name"] == 'Galaxy S23+':
        raise Exception('S23+ found')

# with open('./data.json', 'w+') as f:
#     f.write(json.dumps(items))

# >>>>>>>>>> Check specific model price

# iphone 13 pro
# query = 'https://www.jusit.ch/jusit-search?filter%5Bbrand%5D=Apple&filter%5Bmodel%5D=iPhone13Prjusit&filter%5BpriceMin%5D=100&filter%5BpriceMax%5D=1030'
# headers = {
#     'authority': 'www.jusit.ch',
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'de-CH',
# }
# r = requests.get(query, headers=headers)


# items = r.json()['data']


# if len(items) != 1:
#     print(items)
#     raise Exception('Multiple items were found')


# iphone_url = items[0]['url']
# api_link = url = f"https://www.jusit.ch/device-details/{iphone_url.split('/').pop()}"
# print('api_link', api_link)


# PRICE_LIMIT = 520

# def is_sehr_gut(iphone):
#     for attribute_group in iphone['attributeGroups']:
#         for attribute in attribute_group['attributes']:
#             if attribute['key'] == '991_Zustand' and attribute['value'] == 'sehr gut':
#                 return True
#     return False

# def check_prices(url):
#     lowest_price = 10000
#     r = requests.get(url)
#     payload = r.json()
#     iphones = payload['data']['articles']
#     for iphone in iphones:
#         if is_sehr_gut(iphone):
#             for category in ['salesPrice', 'salesPriceDiscounted']:
#                 if category in iphone['price']:
#                     price = iphone['price'][category]
#                     if lowest_price > price:
#                         lowest_price = price
#                     if price < PRICE_LIMIT:
#                         print('Lowest price', price)
#                         raise Exception('iPhone found')

#     print('Lowest price', lowest_price)


# check_prices(api_link)
