from datetime import datetime
import pandas as pd
import re
from time import sleep

# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '0071834443'
# getBothCAN_US('0133356728')  # issues,
# getBothCAN_US('0131194577') # works
# getBothCAN_US('019994184X') # works

# # ****************  Canada  **************
# myAmazonObj = AMZSoupObject(ItemNumber, 'ca', 'test.html')
myAmazonObj = AMZSoupObject(ItemNumber, 'com', None)
soup = myAmazonObj.soupObj()

alloffersObj = AllOffersObject(soup, 'ApplyUSFilter')  # stores the ENTIRE soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
combinedDict = alloffersObj.getFullSellerDictFiltered(alloffersDivTxt)

print('**************************  print Dict  **************************')
print(combinedDict)
print('**************************  done print Dict  **************************')
lowestDictPriceObject = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
print(lowestDictPriceObject)
