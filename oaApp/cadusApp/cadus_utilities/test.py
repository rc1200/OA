from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from . oaSscrape import AMZSoupObject, AllOffersObject
from . oaUtilities import randomSleep, splitIntoListArray, getBothCAN_US, dictToDF, saveToFile, combineCsvToOneFile, utilsPathFileName




def runSuperCode():

    # ********************************************

    df_asin = pd.read_csv(utilsPathFileName('asin2.csv'))
    myFullASINList = df_asin['ASIN'].drop_duplicates().values.tolist()

    numOfLists = 1
    startNum = 1
    recordsPerList = 1

    # initalize empty lists
    asinSubList = [[] for _ in range(numOfLists)]
    thread = [[] for _ in range(numOfLists)]
    # dfList = [pd.DataFrame() for _ in range(n)]  # May not need as we are appendint o csv file

    # ********************************************


    # # creaet an array of List to store the ASIN numbers
    splitIntoListArray(myFullASINList, asinSubList, numOfLists, startNum, recordsPerList)

    today = datetime.today().strftime('%Y-%m-%d')
    timeStart = datetime.now()

    # Create new threads and append to list
    threads = []
    for i in range(numOfLists):
        t = threading.Thread(target=saveToFile, args=(asinSubList[i], i, today, '_Result{}.csv'.format(i), False))
            # def saveToFile(myASINList, threadNum, todaysDate, fileNameExtensionName='_Result.csv', isTest):
            # -> see oaUtilities.py for details
        threads.append(t)

    # Start all Threads stored in list
    [t.start() for t in threads]
    # wait for all threads before proceeding
    [t.join() for t in threads]


    timeEnd = datetime.now()
    totalMin = timeEnd - timeStart


    print('Start Time:  {}'.format(timeStart))
    print('End Time:  {}'.format(timeEnd))
    print('Total Time:  {}'.format(totalMin))


    # ***********************   combine all csv files  **********************************

    allCsvFiles = ['{}_Result{}.csv'.format(today,i) for i in range(numOfLists)]
    print(allCsvFiles)
    headers =  ['ASIN', 'Seller_canada','priceTotal_canada', 'Condition_canada','Seller_usa', 'priceTotal_usa', 'Condition_usa',
        'is_FBA_usa','lowestPriceFloorusa','US_ConvertedPriceTo_CAD','ProfitFactor','PF_10pctBelow','PF_15pctBelow']

    combineCsvToOneFile(allCsvFiles, headers, utilsPathFileName('combinedCSV.csv'))

    # ***********************   combine all csv files  **********************************