from datetime import datetime
import pandas as pd
import re
from time import sleep

# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '1284128350'


# # ****************  Canada  **************
# myAmazonObj = AMZSoupObject(ItemNumber, 'ca', 'test.html')
myAmazonObj = AMZSoupObject(ItemNumber, 'ca', None)
soup = myAmazonObj.soupObj()

# stores the ENTIRE soup object to a Class to be further filtered
alloffersObj = AllOffersObject(soup)
# extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
alloffersDivTxt = alloffersObj.getAllDataFromAttrib()
combinedDict = alloffersObj.getFullSellerDictFiltered(alloffersDivTxt)

print('**************************  print Dict  **************************')
print(combinedDict)
print('**************************  done print Dict  **************************')
lowestDictPriceObject = alloffersObj.getLowestPricedObjectBasedOnCriteria(
    combinedDict)
print(lowestDictPriceObject)
