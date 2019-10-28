import random
from oaSscrape import AMZSoupObject, AllOffersObject
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



def getBothCAN_US(itemNum, threadNum):
    
    loopDict = {'canada': ['ca', 'tempCan{}.html'.format(threadNum), None],
                'usa': ['com', 'tempUS{}.html'.format(threadNum), 'ApplyUSFilter']
                }

    compareDict = {}

    for k, v in loopDict.items():
        print('{}: reading dict {},{} {}'.format(itemNum, k, v[0], v[1]))

        # stores each Item into an amazon Object, first do Canada, then US based on Dict
        myAmazonObj = AMZSoupObject(itemNum, v[0], v[1], True)
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