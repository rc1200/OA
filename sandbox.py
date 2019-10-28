from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject
from oaUtilities import randomSleep, splitIntoListArray, combineCsvToOneFile

import csv   
numOfLists = 5
today = datetime.today().strftime('%Y-%m-%d')


allCsvFiles = ['{}_Result{}.csv'.format(today,i) for i in range(numOfLists)]
print(allCsvFiles)
headers =  ['ASIN', 'Seller_canada','priceTotal_canada', 'Condition_canada','Seller_usa', 'priceTotal_usa', 'Condition_usa',
    'is_FBA_usa','lowestPriceFloorusa','US_ConvertedPriceTo_CAD','ProfitFactor','PF_10pctBelow','PF_15pctBelow']

combineCsvToOneFile(allCsvFiles, headers, 'combinedCSV.csv')