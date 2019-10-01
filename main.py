import pandas as pd
import re
# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '007738248X'


# ****************  Canada  **************
myAmazonObj = AMZSoupObject(ItemNumber, 'ca', 'test.html')
soup = myAmazonObj.soupObj()

alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllOffers()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
print(lowestDict)


# ****************  US  **************
myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')
soup = myAmazonObj.soupObj()

alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllOffers()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
print(lowestDict)
