from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject


# ********************************************

df_asin1 = pd.read_csv('asin.csv')
df_asin2 = pd.read_csv('asin.csv')
myFullASINList = df_asin2['ASIN'].drop_duplicates().values.tolist()

# myASINList1 = df_asin1.head(1)['ASIN'].drop_duplicates().values.tolist()
# myASINList2 = df_asin2.head(1)['ASIN'].drop_duplicates().values.tolist()

# myASINList1 = df_asin2.iloc[0:3].drop_duplicates().values.tolist()
# myASINList2 = df_asin2.iloc[4:9].drop_duplicates().values.tolist()
n = 5
asinSubList = [[] for _ in range(n)]
dfList = [pd.DataFrame() for _ in range(n)]
thread = [[] for _ in range(n)]

asinSubList[1] = myFullASINList[1:3]
asinSubList[2] = myFullASINList[21:23]
# myASINList1 = myFullASINList[1:3]
# myASINList2 = myFullASINList[21:23]
# myASINList1 = df_asin['ASIN'].drop_duplicates().values.tolist()
# myASINList2 = ['1337406295']

# initalize Empty Dataframe`
# df1 = pd.DataFrame()
# df2 = pd.DataFrame()

# ********************************************


def getBothCAN_US(itemNum, threadNum):

    loopDict = {'canada': ['ca', 'tempCan{}.html'.format(threadNum), None],
                'usa': ['com', 'tempUS{}.html'.format(threadNum), 'ApplyUSFilter']
                }

    compareDict = {}

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1])
        soup = myAmazonObj.soupObj()

        # stores the ENTIRE soup object to a Class to be further filtered
        alloffersObj = AllOffersObject(soup, v[2])
        # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'}
        alloffersDivTxt = alloffersObj.getAllDataFromAttrib(
            'class', 'olpOffer')
        combinedDict = alloffersObj.getAllSellerDict(alloffersDivTxt)
        lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(
            combinedDict)

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

    def pct_gain(CAD_Price, US_Price, USpctReduction=None): return (
        (US_Price*(100-USpctReduction)/100) - CAD_Price) / CAD_Price

    def getUSConversion(x):
        return x * 1.33

    dfTemp = pd.DataFrame.from_dict(myDict, orient='index')
    dfTemp["US_ConvertedPriceTo_CAD"] = dfTemp.priceTotal_usa.apply(
        getUSConversion)
    dfTemp["ProfitFactor"] = pct_gain(
        dfTemp.priceTotal_canada, dfTemp.priceTotal_usa, 0).round(2)
    dfTemp["PF_10pctBelow"] = pct_gain(
        dfTemp.priceTotal_canada, dfTemp.priceTotal_usa, 10).round(2)
    dfTemp["PF_15pctBelow"] = pct_gain(
        dfTemp.priceTotal_canada, dfTemp.priceTotal_usa, 15).round(2)
    return dfTemp


def randomSleep(myList=None):
    # Adding Random sleep times to avoid throttling from Amazon
    # sleepTimesSeconds = [5,12,17,24]
    sleepTimesSeconds = [0]
    if myList:
        sleepTimesSeconds = myList

    sleep(random.choice(sleepTimesSeconds))  # sleep rando seconds seconds


def saveToFile(myASINList, threadNum, myDf, fileNameExtensionName='_Result.csv'):

    for i in myASINList:
        x = dictToDF(getBothCAN_US(i, threadNum))
        print(x)
        myDf = myDf.append(x)
        myDf.to_csv(today + fileNameExtensionName)
        # randomSleep()

    print(' ****************** Non filtered DF ***************')
    print(myDf)


today = datetime.today().strftime('%Y-%m-%d')
timeStart = datetime.now()


# Create new threads
thread[1] = threading.Thread(target=saveToFile, args=(asinSubList[1], 1, dfList[1], '_Result{}.csv'.format(1)))
thread[2] = threading.Thread(target=saveToFile, args=(asinSubList[2], 2, dfList[2], '_Result{}.csv'.format(2)))

testThreadCnt = 2

# Start new Threads
threads = []
for i in range(1, testThreadCnt + 1):
    t = threading.Thread(target=saveToFile, args=(asinSubList[i], i, dfList[i], '_Result{}.csv'.format(i)))
    threads.append(t)

[t.start() for t in threads]
[t.join() for t in threads]


# saveToFile(myASINList1, 1, df1, '_Result1.csv')
# saveToFile(myASINList1,2, df2, '_Result2.csv')

# thread[1].join()
# thread2.join()


timeEnd = datetime.now()
totalMin = timeEnd - timeStart

print('Start Time:  {}'.format(timeStart))
print('End Time:  {}'.format(timeEnd))
print('Total Time:  {}'.format(totalMin))


# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
# print('filtered df')
# print(df)
