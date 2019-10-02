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

def urlType(dotCAordotCOM, itemNumber):
    if dotCAordotCOM.upper() == 'CA':
        return 'https://www.amazon.ca/gp/offer-listing/{}'.format(itemNumber)
    elif dotCAordotCOM.upper() == 'COM':
        return 'https://www.amazon.com/gp/offer-listing/{}/ref=olp_f_primeEligible?f_primeEligible=true'.format(itemNumber)


def getBothCAN_US(itemNum):

        # for testing
    # loopDict = {'canada': ['ca', 'test.html'],
    #             'usa': ['com', 'testUS.html']
    #             }

    loopDict = {'canada': ['ca', None],
                'usa': ['com', None]
                }

    # compareDict = {itemNum: {}}
    compareDict = {}

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))

        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
        # alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
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


# myASINList = [ItemNumber, 22222222, 32156, 44444, 555555]

df = pd.read_csv('asin.csv')
print(df)
myASINList = df['ASIN'].drop_duplicates().values.tolist()
print(myASINList)


# combinedDict = {}
# count = 1
# for i in myASINList:
#     print(i)
#     combinedDict[i] = getBothCAN_US(i)

# print('combinedDict ==== ')
# print(combinedDict)


getBothCAN_US('0133356728')
# getBothCAN_US('0131194577')
