import pandas as pd
import random
from oaSscrape import AMZSoupObject, AllOffersObject
from time import sleep
import os


BASE_oaAPP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_oaAPP_Utilities_DIR  = os.path.join(BASE_oaAPP_DIR, 'cadus_utilities')

def utilsPathFileName(fileName):
    return os.path.join(BASE_oaAPP_Utilities_DIR, fileName)


def randomSleep(myList=None):
    ''' random sleep function
        
        randomSleep() -> use default sleep seconds to choose from
        randomSleep([3,5,6]) -> define your own list
        randomSleep([2]) -> define your own list single value
        randomSleep(2) -> define your own list (converts to list)

    '''
    sleepTimesSeconds = [5,12,17,24]

    if myList:
        if isinstance(myList, list):
            sleepTimesSeconds = myList
        else:
            sleepTimesSeconds = [myList]

    sleep(random.choice(sleepTimesSeconds))  # sleep rando seconds seconds



def splitIntoListArray (sourceList, splitListArray, rangeVal, start, recordsPerList):
    '''
        get initial CSV list, then breaks them down to individual List array
        based on the recordsPerList
        end result is a list array with different ASIN numbers to be used for MultiThreading
    '''

    startNum = start
    endNum = startNum + recordsPerList
    for i in range(rangeVal):
        splitListArray[i] = sourceList[ startNum : endNum]
        startNum = endNum
        endNum = startNum + recordsPerList



def getBothCAN_US(itemNum, threadNum, isTest):
    
    loopDict = {'canada': ['ca', 'tempCan{}.html'.format(threadNum), None],
                'usa': ['com', 'tempUS{}.html'.format(threadNum), 'ApplyUSFilter']
                }

    compareDict = {}

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], utilsPathFileName(v[1]), isTest) 
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
        # randomSleep([2])

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



def saveToFile(myASINList, threadNum, todaysDate, fileNameExtensionName='_Result.csv', isTest=False):
    # def saveToFile(myASINList, threadNum, myDf, fileNameExtensionName='_Result.csv'):  -- OLD

    for i in myASINList:
        x = dictToDF(getBothCAN_US(i, threadNum, isTest))
        print(x)

        x.to_csv(utilsPathFileName(todaysDate + fileNameExtensionName), mode='a', header=False) 

        # No need anymore as we are append to file now so DF is technically not needed
        # myDf = myDf.append(x)
        # myDf.to_csv(today + fileNameExtensionName)
        # randomSleep()

    print(' ****************** Non filtered DF ***************')
    print(x)



def combineCsvToOneFile (allCsvFiles, headers, NewFileName):
    
    combined_csv_to_Pandas = pd.concat([pd.read_csv(utilsPathFileName(f),names=headers) for f in allCsvFiles ])
    print('combinging csv and writing to new file')
    print(combined_csv_to_Pandas.head())
    combined_csv_to_Pandas.to_csv( NewFileName, index=False, encoding='utf-8-sig')