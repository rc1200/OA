import pandas as pd
import requests
from bs4 import BeautifulSoup


'''
# store entire object into a variable
page = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=41.8843&lon=-87.6324#.XIRQYFNKgUE'
)

# lets the object know we are passing an HTML and to pars it as that
soup = BeautifulSoup(page.content, 'html.parser')

# grabbing all the code inside the div based on the ID
week = soup.find(id='seven-day-forecast-body')
print(week)



# store everything within the container
# NOTE since we are using Class container instead of a tag we use "class_" since class is reserved
items = week.find_all(class_='tombstone-container')

# storing the text into a list using list comprehension
period_names = [item.find(class_='period-name').get_text() for item in items]
short_descriptions = [item.find(class_='short-desc').get_text() for item in items]
temperatures = [item.find(class_='temp').get_text() for item in items]

# passing a dictionary using Pandas Dataframe ... has the Key and List
weather_stuff = pd.DataFrame(
    {
        'period': period_names,
        'short_descriptions': short_descriptions,
        'temperatures': temperatures,
    })

print(weather_stuff)

# export the data into a csv file
weather_stuff.to_csv('exported_to_csv.csv')

'''

# store entire object into a variable


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get('https://www.amazon.ca/gp/offer-listing/007738248X', headers=headers)
# page = requests.get('https://www.amazon.ca/gp/offer-listing/007738248X')  NOTE: you might get this if you don't add headers 503 Server Error: Service Unavailable for url: https://www.amazon.ca/gp/offer-listing/007738248X


try:
    page.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(e)


# lets the object know we are passing an HTML and to pars it as that
soup = BeautifulSoup(page.content, 'html.parser')

# print(page)
# print(soup)


Alloffers = soup.find(id='olpRefinements')
print(Alloffers)

# store everything within the Offers
# NOTE since we are using Class container instead of a tag we use "class_" since class is reserved


# items = Alloffers.find_all(class_='a-size-large a-color-price olpOfferPrice a-text-bold')
# print(items)
# print(items[0])


# storing the text into a list using list comprehension
# uisng .text.strip() vs .get_text() to strip out the spaces


# price = [item.find(class_='a-size-large a-color-price olpOfferPrice a-text-bold').text.strip() for item in items] seems only for big price, not accurate as it doesn't include shipping

# price = [item.find(class_='a-row a-spacing-mini olpOffer').get_text() for item in items]

# print(price)


'''
# Class for entire row... but need to filter based on specific columns
'a-row a-spacing-mini olpOffer'

# Class Filter for Price n.b. there could be 2 prices for shipping, maybe use regex to get total amokunt /d
'a-column a-span2 olpPriceColumn'

# Class Filter for Condition
'a-column a-span3 olpConditionColumn'

# Class Filter for Seller Information
'a-column a-span2 olpSellerColumn'

# Class Filter for Delivery
'a-column a-span3 olpDeliveryColumn'
'''

# ------------------------------


def getAmazonPrice(productUrl):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    res = requests.get(productUrl, headers=headers)
    # res = requests.get(productUrl)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)

    soup = BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('#newOfferAccordionRow .header-price')
    return elems[0].text.strip()


# price = getAmazonPrice('http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=&sr=')
# print('The price is ' + price)
