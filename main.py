import pandas as pd
import re
# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '007738248X'


# # ****************  Canada  **************
# myAmazonObj = AMZSoupObject(ItemNumber, 'ca', 'test.html')
# soup = myAmazonObj.soupObj()

# alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
# alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
# combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
# lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
# print(lowestDict)1


# # ****************  US  **************
# myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')
# soup = myAmazonObj.soupObj()

# alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
# alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
# combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
# lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
# print(lowestDict)


def getBothCAN_US(itemNum):

    loopDict = {'canada': ['ca', 'test.html'],
                'usa': ['com', 'testUS.html']
                }

    # compareDict = {itemNum: {}}
    compareDict = {}

    for k, v in loopDict.items():
        print('reading dict {},{} {}'.format(k, v[0], v[1]))

        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
        lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
        # print(lowestDict)
        # compareDict[itemNum][k] = {'price': lowestDict['price'],
        #                            'Condition': lowestDict['condition']
        #                            }

        compareDict[k] = {'price': lowestDict['price'],
                          'Condition': lowestDict['condition']
                          }

    print(compareDict)
    return compareDict


myISBNList = [ItemNumber, 22222222, 32156, 44444, 555555]
combinedDict = {}

count = 1
for i in myISBNList:
    print(i)
    combinedDict[i] = getBothCAN_US(i)
    count += 13

print('combinedDict ==== ')
print(combinedDict)
