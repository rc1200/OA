from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject
from oaUtilities import randomSleep, splitIntoListArray


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

# RM - create function to or maybe even class to create lists
startNum = 1
recordsPerList = 100
endNum = startNum + recordsPerList



# ********************************************

splitIntoListArray(myFullASINList, asinSubList, 5, 1, 100)

for i in asinSubList:
    print(i)
    print('\n\n\n')