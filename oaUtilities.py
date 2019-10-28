import random
from time import sleep


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