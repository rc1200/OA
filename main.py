from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject
from oaUtilities import randomSleep, splitIntoListArray, getBothCAN_US


# ********************************************

df_asin = pd.read_csv('asin.csv')
myFullASINList = df_asin['ASIN'].drop_duplicates().values.tolist()

# RM - get a function to create the iterator based on the threading cap vs using N value
# ie. getSliceCnt
n = 5
# initalize empty lists
asinSubList = [[] for _ in range(n)]
dfList = [pd.DataFrame() for _ in range(n)]  # May not need as we are appendint o csv file
thread = [[] for _ in range(n)]

numOfLists = 1
startNum = 1
recordsPerList = 2

# creaet an array of List to store the ASIN numbers
splitIntoListArray(myFullASINList, asinSubList, numOfLists, startNum, recordsPerList)

# ********************************************





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





def saveToFile(myASINList, threadNum, myDf, fileNameExtensionName='_Result.csv'):

    for i in myASINList:
        x = dictToDF(getBothCAN_US(i, threadNum))
        print(x)

        x.to_csv(today + fileNameExtensionName, mode='a', header=False)

        # No need anymore as we are append to file now so DF is technically not needed
        # myDf = myDf.append(x)
        # myDf.to_csv(today + fileNameExtensionName)
        # randomSleep()

    print(' ****************** Non filtered DF ***************')
    print(myDf)


today = datetime.today().strftime('%Y-%m-%d')
timeStart = datetime.now()

testThreadCnt = n
# Create new threads
threads = []
for i in range(testThreadCnt):
    t = threading.Thread(target=saveToFile, args=(asinSubList[i], i, dfList[i], '_Result{}.csv'.format(i)))
    threads.append(t)

# Start new Threads
[t.start() for t in threads]
# wait for all threads before proceeding
[t.join() for t in threads]


timeEnd = datetime.now()
totalMin = timeEnd - timeStart

print('Start Time:  {}'.format(timeStart))
print('End Time:  {}'.format(timeEnd))
print('Total Time:  {}'.format(totalMin))


# df = df[(df.ProfitFactor1.between(-66,33)) & (df.Condition_usa != 'something wrong happened')]
# print('filtered df')
# print(df)
