from datetime import datetime
import pandas as pd
import random
import re
from time import sleep

# import requests
# from bs4 import BeautifulSoup
from oaSscrape import AMZSoupObject, AllOffersObject


ItemNumber = '007738248X'


def getBothCAN_US(itemNum):
    
    # uncomment for testing
    # loopDict = {'canada': ['ca', 'test.html'],
    #             'usa': ['com', 'testUS.html']
    #             }

    loopDict = {'canada': ['ca', None, None],
                'usa': ['com', None, 'ApplyUSFilter']
                }

    compareDict = {}

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        alloffersObj = AllOffersObject(soup, v[2]) # stores the ENTIRE soup object to a Class to be further filtered
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        combinedDict = alloffersObj.getAllSellerDict(alloffersDivTxt)
        lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)

        # if current_k == 1:
        #     compareDict[itemNum] = {'priceTotal_{}'.format(k): lowestDict['priceTotal'],
        #                             'Condition_{}'.format(k): lowestDict['condition']}
        # else:
        #     compareDict[itemNum].update({'priceTotal_{}'.format(k): lowestDict['priceTotal'],
        #                                  'Condition_{}'.format(k): lowestDict['condition']})

        if k == 'canada':
            compareDict[itemNum] = {'Seller_{}'.format(k): lowestDict['sellerName'],
                                    'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                    'Condition_{}'.format(k): lowestDict['condition']}
        else:
            compareDict[itemNum].update({'Seller_{}'.format(k): lowestDict['sellerName'],
                                         'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                         'Condition_{}'.format(k): lowestDict['condition'],
                                         'is_FBA_{}'.format(k): lowestDict['isFBA']})
        
        randomSleep([3,5,6])

    print('********************************* Final combinedDict below will be printed')
    print(compareDict)
    return compareDict








df_asin = pd.read_csv('asin.csv')
print(df_asin)
# myASINList = df_asin.head(6)['ASIN'].drop_duplicates().values.tolist()
# myASINList = df_asin['ASIN'].drop_duplicates().values.tolist()
myASINList = ['0500841152']
print(myASINList)

# initalize Empty Dataframe
df = pd.DataFrame()
print(df)

def dictToDF(myDict):

    def pct_gain(CAD_Price, US_Price, USpctReduction=None): return ( (US_Price*(100-USpctReduction)/100) - CAD_Price) / CAD_Price
    
    def getUSConversion(x):
        return x * 1.33

    dfTemp = pd.DataFrame.from_dict(myDict, orient='index')
    dfTemp["US_ConvertedPriceTo_CAD"] = dfTemp.priceTotal_usa.apply(getUSConversion)
    dfTemp["ProfitFactor"] = pct_gain(dfTemp.priceTotal_canada, dfTemp.priceTotal_usa,0).round(2)
    dfTemp["PF_10pctBelow"] = pct_gain(dfTemp.priceTotal_canada, dfTemp.priceTotal_usa,10).round(2)
    dfTemp["PF_15pctBelow"] = pct_gain(dfTemp.priceTotal_canada, dfTemp.priceTotal_usa,15).round(2)
    return dfTemp


def randomSleep(myList=None):
    # Adding Random sleep times to avoid throttling from Amazon
    sleepTimesSeconds = [5,12,17,24]
    if myList:
        sleepTimesSeconds = myList
    
    sleep(random.choice(sleepTimesSeconds)) # sleep rando seconds seconds

for i in myASINList:
    x = dictToDF(getBothCAN_US(i))
    print(x)
    df= df.append(x)
    randomSleep()
    



print(' ****************** Non filtered DF ***************')
print(df)

# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
# print('filtered df')
# print(df)

today = datetime.today().strftime('%Y-%m-%d')
df.to_csv(today + '_Result.csv')

