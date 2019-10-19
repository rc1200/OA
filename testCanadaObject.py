from datetime import datetime
import pandas as pd
import re
from time import sleep

# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '0500841152'

# # ****************  Canada  **************
# myAmazonObj = AMZSoupObject(ItemNumber, 'ca', 'test.html')
myAmazonObj = AMZSoupObject(ItemNumber, 'ca', None)
soup = myAmazonObj.soupObj()


# with open('testSoup.html', 'w', encoding='utf-8') as f_out:
#     f_out.write(soup.prettify())
#     f_out.close()


# alloffersObj = AllOffersObject(soup, 'ApplyUSFilter')  # stores the ENTIRE soup object to a Class to be further filtered
alloffersObj = AllOffersObject(soup, None)  # stores the ENTIRE soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
combinedDict = alloffersObj.getAllSellerDict(alloffersDivTxt)

print('**************************  print Dict  **************************')
print(combinedDict)
print('**************************  done print Dict  **************************')
lowestDictPriceObject = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
print(lowestDictPriceObject)
