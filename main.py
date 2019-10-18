from datetime import datetime
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

    # uncomment for testing
    # loopDict = {'canada': ['ca', 'test.html'],
    #             'usa': ['com', 'testUS.html']
    #             }

    loopDict = {'canada': ['ca', None],
                'usa': ['com', None]
                }

    # compareDict = {itemNum: {}}
    compareDict = {}
    current_k = 0

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))
        current_k += 1

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        alloffersObj = AllOffersObject(soup)  # stores the ENTIRE soup object to a Class to be further filtered
        # alloffersDivTxt = alloffersObj.getAllDataFromAttrib()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'} if left blank inside brackets
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
        print('xxxxxxxxxxxxxxxxxxxxxxx current combinedDict below will be printed')
        print(compareDict)
        lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
        # print(lowestDict)
        # compareDict[itemNum][k] = {'price': lowestDict['price'],
        #                            'Condition': lowestDict['condition']
        #                            }

        # compareDict[k] = {'price': lowestDict['price'],
        #                   'Condition': lowestDict['condition']
        #                   }

        if current_k == 1:
            compareDict[itemNum] = {'price_{}'.format(k): lowestDict['price'],
                                    'Condition_{}'.format(k): lowestDict['condition']}
        else:
            compareDict[itemNum].update({'price_{}'.format(k): lowestDict['price'],
                                         'Condition_{}'.format(k): lowestDict['condition']})

        print('sdfsssssssss')
        print(compareDict[itemNum])

    print('********************************* Final combinedDict below will be printed')
    print(compareDict)
    return compareDict


# myASINList = [ItemNumber, 22222222, 32156, 44444, 555555]

df = pd.read_csv('asin.csv')
print(df)
# myASINList = df.head(6)['ASIN'].drop_duplicates().values.tolist()
myASINList = df['ASIN'].drop_duplicates().values.tolist()

print(myASINList)

# myASINList = ['0133356728', '0131194577', '019994184X']

# getBothCAN_US('0133356728')  # issues,
# getBothCAN_US('0131194577') # works
# getBothCAN_US('019994184X') # works


# initalize Empty Dataframe
df = pd.DataFrame()
print(df)

def passMyDf(myDict):

    def pct_gain(x, args=()): return (args - x) / x
    
    def getUSConversion(x):
        return x * 1.33

    dfTemp = pd.DataFrame.from_dict(myDict, orient='index')
    dfTemp["US_ConvertedPrice"] = dfTemp.price_usa.apply(getUSConversion)
    dfTemp["ProfitFactor1"] = pct_gain(dfTemp.price_canada, dfTemp.price_usa).round(2)
    return dfTemp

for i in myASINList:
    x = passMyDf(getBothCAN_US(i))
    df= df.append(x)


print('*************************Final')
print(df)


# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
print('filtered df')
print(df)

today = datetime.today().strftime('%Y-%m-%d')
df.to_csv(today + '_Result.csv')

