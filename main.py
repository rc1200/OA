import pandas as pd
import re
# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject


ItemNumber = '007738248X'
myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')


soup = myAmazonObj.soupObj()


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
    delivery = getText(offer_list_index, 'olpDeliveryColumn')
    isFBA = False
    if 'Fulfillment by Amazon' in delivery:
        isFBA = True

    sellerData = {
        'price': getPriceOnly(getText(offer_list_index, 'olpOfferPrice')),
        'priceShipping': getPriceOnly(getText(offer_list_index, 'olpShippingPrice')),
        'priceTotal': price + priceShipping,
        'condition': re.sub(r'([^a-zA-Z0-9\-]+|(\n))', ' ', getText(offer_list_index, 'olpCondition').strip()),
        'sellerName': sellerName,
        'sellerPositive': sellerPositive,
        'sellerRating': sellerRating,
        'seller': allSellerInfo,
        'delivery': delivery,
        'isFBA': isFBA
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

    # INCLUDE List for Condition
    conditoinTextIncludeList = 'New, Used - Acceptable, Used - Like New, Used - Good, Used - Very Good'
    # conditoinTextIncludeList = 'New'
    conditoinIncludeList = [x.strip() for x in conditoinTextIncludeList.split(',')]

    # Exclude List for Seller info
    sellerTextExcludeList = 'Just Launched'
    sellerExcludeSet = set([x.strip() for x in sellerTextExcludeList.split(',')])

    # Exclude List for Delivery
    deliveryTextExcludeList = 'India'
    deliveryExcludeSet = set([x.strip() for x in deliveryTextExcludeList.split(',')])

    print(sellerExcludeSet)
    print(deliveryExcludeSet)

    for i in sellerObject:
        boolPutInDict = True
        sellerName = getData(i)['sellerName']

        if getData(i)['priceTotal'] < 1:
            boolPutInDict = False

        if getData(i)['condition'] not in conditoinIncludeList:
            boolPutInDict = False

        if getData(i)['sellerPositive'] < 0:
            boolPutInDict = False

        if getData(i)['sellerRating'] < 0:
            boolPutInDict = False

        deliveryText = getData(i)['delivery']
        print(sellerName + '   dddddddddddddddddddddddd' + deliveryText)
        print(deliveryExcludeSet)
        for stringMatch in deliveryExcludeSet:
            if stringMatch in deliveryText:
                boolPutInDict = False

        sellerText = getData(i)['seller']
        print(sellerName + '   ssssssssssssssssssssssssss' + sellerText)
        print(sellerExcludeSet)
        for stringMatch in sellerExcludeSet:
            print(stringMatch + '****************')
            if stringMatch in sellerText:
                print('get outttttttttttttttt')
                boolPutInDict = False

        if boolPutInDict == True:
            nestedDict[sellerName] = getData(i)

    # print(nestedDict)
    return(nestedDict)


def getLowestPricedObject(myDict):
    lowestPrice = 999999999999999
    lowestKey = ''
    boolFBAExists = False

    for k, v in myDict.items():
        if v['priceTotal'] < lowestPrice:
            if v['isFBA']:
                print('FBA in the houseeeeeeeeeeeeee')
                boolFBAExists = True
                lowestPrice = v['priceTotal']
                lowestKey = k

            if not boolFBAExists:
                lowestPrice = v['priceTotal']
                lowestKey = k
                print('whereeeeeeeeeeeee my FBA')

    return myDict[lowestKey]


objectDict = storeToNestedDict(Alloffers)

print(objectDict)
print(getLowestPricedObject(objectDict))
