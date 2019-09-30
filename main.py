import pandas as pd
import re
# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '007738248X'
myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')
soup = myAmazonObj.soupObj()


# all the offers for each ROW is stored in this Div class
# creates a list of bojects which we will further parse out
alloffersObj = AllOffersObject(soup)  # stores the entire soup object to a Class to be further filtered
allOffers = alloffersObj.getAllOffers()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'

print(allOffers)


# ************************************

# def storeToPandas(offers):
#     tempPandas = pd.DataFrame()
#     for i in offers:
#         # if getData(i):
#         tempPandas = tempPandas.append(getData(i), ignore_index=True)

#     return tempPandas


# myPanda = storeToPandas(Alloffers)
# # export the data into a csv file
# myPanda.to_csv('exported_to_csv.csv')


# ************************************


# def storeToNestedDict(sellerObject):
#     nestedDict = {}
#     boolPutInDict = True

#     # INCLUDE List for Condition
#     conditoinTextIncludeList = 'New, Used - Acceptable, Used - Like New, Used - Good, Used - Very Good'
#     # conditoinTextIncludeList = 'New'
#     conditoinIncludeList = [x.strip() for x in conditoinTextIncludeList.split(',')]

#     # Exclude List for Seller info
#     sellerTextExcludeList = 'Just Launched'
#     sellerExcludeSet = set([x.strip() for x in sellerTextExcludeList.split(',')])

#     # Exclude List for Delivery
#     deliveryTextExcludeList = 'India'
#     deliveryExcludeSet = set([x.strip() for x in deliveryTextExcludeList.split(',')])

#     print(sellerExcludeSet)
#     print(deliveryExcludeSet)

#     for i in sellerObject:
#         boolPutInDict = True
#         sellerName = getData(i)['sellerName']

#         if getData(i)['priceTotal'] < 1:
#             boolPutInDict = False

#         if getData(i)['condition'] not in conditoinIncludeList:
#             boolPutInDict = False

#         if getData(i)['sellerPositive'] < 0:
#             boolPutInDict = False

#         if getData(i)['sellerRating'] < 0:
#             boolPutInDict = False

#         deliveryText = getData(i)['delivery']
#         print(sellerName + '   dddddddddddddddddddddddd' + deliveryText)
#         print(deliveryExcludeSet)
#         for stringMatch in deliveryExcludeSet:
#             if stringMatch in deliveryText:
#                 boolPutInDict = False

#         sellerText = getData(i)['seller']
#         print(sellerName + '   ssssssssssssssssssssssssss' + sellerText)
#         print(sellerExcludeSet)
#         for stringMatch in sellerExcludeSet:
#             print(stringMatch + '****************')
#             if stringMatch in sellerText:
#                 print('get outttttttttttttttt')
#                 boolPutInDict = False

#         if boolPutInDict == True:
#             nestedDict[sellerName] = getData(i)

#     # print(nestedDict)
#     return(nestedDict)


# def getLowestPricedObject(myDict):
#     lowestPrice = 999999999999999
#     lowestKey = ''
#     boolFBAExists = False

#     for k, v in myDict.items():
#         if v['priceTotal'] < lowestPrice:
#             if v['isFBA']:
#                 print('FBA in the houseeeeeeeeeeeeee')
#                 boolFBAExists = True
#                 lowestPrice = v['priceTotal']
#                 lowestKey = k

#             if not boolFBAExists:
#                 lowestPrice = v['priceTotal']
#                 lowestKey = k
#                 print('whereeeeeeeeeeeee my FBA')

#     return myDict[lowestKey]


# objectDict = storeToNestedDict(Alloffers)

# print(objectDict)
# print(getLowestPricedObject(objectDict))
