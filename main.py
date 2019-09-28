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

# https://www.amazon.ca/gp/offer-listing/0143105426

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


def extractViaRegex(strSample, regExPattern, groupNumber, NoneReplacementVal):
    returnRegEx = re.search(regExPattern, strSample)
    if returnRegEx is None:
        returnRegEx = NoneReplacementVal
    else:
        returnRegEx = returnRegEx.group(groupNumber).strip()

    return returnRegEx


def getData(offer_list_index):

    price = getPriceOnly(getText(offer_list_index, 'olpOfferPrice'))
    # price = float(extractViaRegex(getText(offer_list_index, 'olpOfferPrice'), '(\d+\.?\d+)', '0'))
    priceShipping = getPriceOnly(getText(offer_list_index, 'olpShippingPrice'))
    allSellerInfo = getText(offer_list_index, 'olpSellerColumn')
    sellerName = extractViaRegex(allSellerInfo, '^(.*)\n.*', 1, 'Amazon')
    sellerPositive = int(extractViaRegex(allSellerInfo, '(\d\d)%', 1, '0'))
    # sellerRating = extractViaRegex(allSellerInfo, '(\d+,?\d+)\stotal ratings', 1, '0')
    sellerRating = int(extractViaRegex(allSellerInfo, '(\d+,?\d+)\stotal ratings', 1, '0').replace(',', ''))

    sellerData = {
        'price': getPriceOnly(getText(offer_list_index, 'olpOfferPrice')),
        'priceShipping': getPriceOnly(getText(offer_list_index, 'olpShippingPrice')),
        'priceTotal': price + priceShipping,
        'condition': re.sub(r'([^a-zA-Z0-9\-]+|(\n))', ' ', getText(offer_list_index, 'olpCondition').strip()),
        'sellerName': sellerName,
        'sellerPositive': sellerPositive,
        'sellerRating': sellerRating,
        'seller': getText(offer_list_index, 'olpSellerColumn'),
        'delivery': getText(offer_list_index, 'olpDeliveryColumn')
    }

    # for k, v in sellerData.items():
    #     print('{} \t\t:----> {}'.format(k, v))

    return sellerData


# ************************************

def storeToPandas(offers):
    tempPandas = pd.DataFrame()
    for i in offers:   # for i in range(len(Alloffers)):
        if getData(i):
            tempPandas = tempPandas.append(getData(i), ignore_index=True)

    return tempPandas


myPanda = storeToPandas(Alloffers)
# export the data into a csv file
myPanda.to_csv('exported_to_csv.csv')


# ************************************


def storeToNestedDict(sellerObject):
    nestedDict = {}
    boolPutInDict = True

    conditoinTextIncludeList = 'New, Used - Acceptable, Used - Like New, Used - Good'
    conditoinIncludeList = [x.strip() for x in conditoinTextIncludeList.split(',')]

    deliveryTextExcludeList = 'xUnited, xStates, Canada, Japan'
    deliveryExcludeSet = [x.strip() for x in deliveryTextExcludeList.split(',')]

    for i in sellerObject:
        boolPutInDict = True
        sellerName = getData(i)['sellerName']

        if getData(i)['priceTotal'] != 150.46:
            boolPutInDict = False

        if getData(i)['condition'] not in conditoinIncludeList:
            boolPutInDict = False

        if getData(i)['sellerPositive'] < 8:
            boolPutInDict = False

        if getData(i)['sellerRating'] < 0:
            boolPutInDict = False

        print(sellerName + '   zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz' + getData(i)['delivery'])
        deliveryStrippedSet = set(re.split('(\.|\s|\,)', getData(i)['delivery']))

        print(deliveryStrippedSet)
        print(deliveryExcludeSet)

        if deliveryStrippedSet.intersection(deliveryExcludeSet):
            boolPutInDict = False

        if boolPutInDict == True:
            nestedDict[sellerName] = getData(i)

    # print(nestedDict)
    return(nestedDict)


storeToNestedDict(Alloffers)
