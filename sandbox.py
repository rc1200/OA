from datetime import datetime
import pandas as pd
import random
import re
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject


# ********************************************

df_asin1 = pd.read_csv('asin.csv')
df_asin2 = pd.read_csv('asin.csv')
myASINList1 = df_asin1.head(3)['ASIN'].drop_duplicates().values.tolist()
myASINList2 = df_asin2.head(3)['ASIN'].drop_duplicates().values.tolist()
# myASINList1 = df_asin['ASIN'].drop_duplicates().values.tolist()
# myASINList2 = ['1337406295']

# initalize Empty Dataframe
df1 = pd.DataFrame()
df2 = pd.DataFrame()

# ********************************************

def getBothCAN_US(itemNum):
    
    loopDict = {'canada': ['ca', 'tempCan.html', None],
                'usa': ['com', 'tempUS.html', 'ApplyUSFilter']
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


        if k == 'canada':
            compareDict[itemNum] = {'Seller_{}'.format(k): lowestDict['sellerName'],
                                    'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                    'Condition_{}'.format(k): lowestDict['condition']}
        else:
            compareDict[itemNum].update({'Seller_{}'.format(k): lowestDict['sellerName'],
                                         'priceTotal_{}'.format(k): lowestDict['priceTotal'],
                                         'Condition_{}'.format(k): lowestDict['condition'],
                                         'is_FBA_{}'.format(k): lowestDict['isFBA'],
                                         'lowestPriceFloor{}'.format(k): lowestDict['lowestPriceFloor']})
        
        # randomSleep([3,5,6])
        randomSleep([0])

    print('********************************* Final combinedDict below will be printed')
    print(compareDict)
    return compareDict





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
    # sleepTimesSeconds = [5,12,17,24]
    sleepTimesSeconds = [0]
    if myList:
        sleepTimesSeconds = myList
    
    sleep(random.choice(sleepTimesSeconds)) # sleep rando seconds seconds



def saveToFile(myASINList, myDf, fileNameExtensionName='_Result.csv'):

    for i in myASINList:
        x = dictToDF(getBothCAN_US(i))
        print(x)
        myDf= myDf.append(x)
        myDf.to_csv(today + fileNameExtensionName)
        randomSleep()

    print(' ****************** Non filtered DF ***************')
    print(myDf)







today = datetime.today().strftime('%Y-%m-%d')
timeStart = datetime.now()

saveToFile(myASINList1, df1, '_Result1.csv')
saveToFile(myASINList1, df1, '_Result2.csv')

timeEnd = datetime.now()
totalMin = timeEnd - timeStart

print('Start Time:  {}'.format(timeStart))
print('End Time:  {}'.format(timeEnd))
print('Total Time:  {}'.format(totalMin))


# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
# print('filtered df')
# print(df)



