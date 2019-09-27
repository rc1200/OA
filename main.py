import pandas as pd
import re
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

url = 'https://www.amazon.ca/gp/offer-listing/{}'.format('007738248X')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
# response = requests.get('https://www.amazon.ca/gp/offer-listing/007738248X')  NOTE: you might get this if you don't add headers 503 Server Error: Service Unavailable for url: https://www.amazon.ca/gp/offer-listing/007738248X

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(e)


# lets the object know we are passing an HTML and to pars it as that
soup = BeautifulSoup(response.content, 'lxml')  # note for some reason html.parser was not getting all the data


# backup method if we needed to put a delay and actually open the page
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# browser = webdriver.Chrome()  # ensure the chrome driver is install in the same directory or explictly specify path
# browser.get(url)
# soup = browser.page_source


# all the offers for each ROW is stored in this Div class
# creates a list of bojects which we will further parse out
Alloffers = soup.find_all(attrs={'class': 'olpOffer'})


# safeguad when fetching data if type is NONE ie. there is no text (ie. Shipping olpShippingPrice class)
def getText(mainDiv, className):
    if mainDiv.find(attrs={'class': className}) is not None:
        return mainDiv.find(attrs={'class': className}).text.strip()
    else:
        return '0'


def getPriceOnly(priceString):
    return(float(re.sub('[^0-9.]', "", priceString)))


def getData(offer_list_index):

    price = getPriceOnly(getText(offer_list_index, 'olpOfferPrice'))
    priceShipping = getPriceOnly(getText(offer_list_index, 'olpShippingPrice'))
    sellerData = {
        'price': getPriceOnly(getText(offer_list_index, 'olpOfferPrice')),
        'priceShipping': getPriceOnly(getText(offer_list_index, 'olpShippingPrice')),
        'priceTotal': price + priceShipping,
        'condition': getText(offer_list_index, 'olpConditionColumn'),
        'seller': getText(offer_list_index, 'olpSellerColumn'),
        'delivery': getText(offer_list_index, 'olpDeliveryColumn')
    }

    for k, v in sellerData.items():
        print('{} \t\t:----> {}'.format(k, v))

    return sellerData


print('\n\n\n')
print('all offers {}'.format(len(Alloffers)))

myPanda = pd.DataFrame()
for i in Alloffers:   # for i in range(len(Alloffers)):
    if getData(i):
        myPanda = myPanda.append(getData(i), ignore_index=True)


# myPanda = myPanda.append(getData(Alloffers[2]), ignore_index=True)
# myPanda = pd.DataFrame(getData(Alloffers[1]), index=[0])

print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  my Panda ???????????????')
print(myPanda)
print(myPanda[['price', 'condition']])

# export the data into a csv file
myPanda.to_csv('exported_to_csv.csv')
