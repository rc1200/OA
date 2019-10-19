from datetime import datetime
import pandas as pd
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
    current_k = 0

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))
        current_k += 1

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        alloffersObj = AllOffersObject(soup, v[2]) # stores the ENTIRE soup object to a Class to be further filtered
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        combinedDict = alloffersObj.getFullSellerDictFiltered(alloffersDivTxt)
        lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)

        if current_k == 1:
            compareDict[itemNum] = {'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                    'Condition_{}'.format(k): lowestDict['condition']}
        else:
            compareDict[itemNum].update({'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                         'Condition_{}'.format(k): lowestDict['condition']})


    print('********************************* Final combinedDict below will be printed')
    print(compareDict)
    return compareDict








df_asin = pd.read_csv('asin.csv')
print(df_asin)
# myASINList = df_asin.head(6)['ASIN'].drop_duplicates().values.tolist()
# myASINList = df_asin['ASIN'].drop_duplicates().values.tolist()
myASINList = ['1455740209']
print(myASINList)

# initalize Empty Dataframe
df = pd.DataFrame()
print(df)

def dictToDF(myDict):

    def pct_gain(x, args=()): return (args - x) / x
    
    def getUSConversion(x):
        return x * 1.33

    dfTemp = pd.DataFrame.from_dict(myDict, orient='index')
    dfTemp["US_ConvertedPrice"] = dfTemp.priceTotal_usa.apply(getUSConversion)
    dfTemp["ProfitFactor1"] = pct_gain(dfTemp.priceTotal_canada, dfTemp.priceTotal_usa).round(2)
    return dfTemp


for i in myASINList:
    x = dictToDF(getBothCAN_US(i))
    print(x)
    df= df.append(x)
    sleep(5) # sleep 5 seconds


print(' ****************** Non filtered DF ***************')
print(df)

# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
# print('filtered df')
# print(df)

today = datetime.today().strftime('%Y-%m-%d')
df.to_csv(today + '_Result.csv')

