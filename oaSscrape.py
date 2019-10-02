import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


class AMZSoupObject(object):

    ''' Creates soup object from Amazon Listing
        for parameters use:
            itemNumber => ISBN number for book
            dotCAordotCOM =>
                = 'ca' to get the Canadian Prices
                = 'com' to get the Americian Prices filtered by Prime Eligible

            readFromFile => option parameter, put File Name of the html document instad of fetching from web
                            if has value then read from a file instead of going to actual site

    sample: myAmazonObj = AMZSoupObject('007738248X', 'com', 'testUS.html') N.B. Reads from file because of file name 'testUS.html'
    sample: myAmazonObj = AMZSoupObject('007738248X', 'com') NOT reading from file, instead going to web to fetch data

    '''

    # constant for all classes
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, itemNumber, dotCAordotCOM, readFromFile=None):
        self.itemNumber = itemNumber
        self.dotCAordotCOM = dotCAordotCOM
        self.readFromFile = readFromFile

    def urlType(self):
        if self.dotCAordotCOM.upper() == 'CA':
            return 'https://www.amazon.ca/gp/offer-listing/{}'.format(self.itemNumber)
        elif self.dotCAordotCOM.upper() == 'COM':
            return 'https://www.amazon.com/gp/offer-listing/{}/ref=olp_f_primeEligible?f_primeEligible=true'.format(self.itemNumber)

    def soupObj(self):
        if self.readFromFile is not None:
            # soup = BeautifulSoup(open('test.html'), 'lxml')  # note for some reason html.parser was not getting all the data
            # soup = BeautifulSoup(open('testUS.html'), 'lxml')  # note for some reason html.parser was not getting all the data
            print('Reading from file')
            return BeautifulSoup(open(self.readFromFile), 'lxml')  # note for some reason html.parser was not getting all the data
        else:
            response = requests.get(self.urlType, headers=HEADERS)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)

            return response


class AllOffersObject(object):
    """docstring for Alloffers
        all the offers for each ROW is stored in this Div class
        creates a list of ojects which we will further parse out

        getAllDataFromAttrib: stores HTML doc for all the offers



    """

    def __init__(self, offersSoup):
        self.offersSoup = offersSoup

        # Private Varables N.B. Keep hard coded, add methon to update later
        # INCLUDE List for Condition
        self.__conditionTextIncludeList = 'New, Used - Acceptable, Used - Like New, Used - Good, Used - Very Good'
        # Exclude List for Seller info
        self.__sellerTextExcludeList = 'Just Launched'
        # Exclude List for Delivery
        self.__deliveryTextExcludeList = 'India'

    def getAllDataFromAttrib(self, htmlType=None, attribName=None):

        htmlTypeVal = htmlType if htmlType else 'class'
        attribNameVal = attribName if attribName else 'olpOffer'
        return self.offersSoup.find_all(attrs={htmlTypeVal: attribNameVal})

    # safeguad when fetching data if type is NONE ie. there is no text (ie. Shipping olpShippingPrice class)
    def getText(self, sellerDivSoupObj, className):
        if sellerDivSoupObj.find(attrs={'class': className}) is not None:
            return sellerDivSoupObj.find(attrs={'class': className}).text.strip()
        else:
            return '0'

    def getPriceOnly(self, priceString):
        return(float(re.sub('[^0-9.]', "", priceString)))

    def extractViaRegex(self, strSample, regExPattern, groupNumber, NoneReplacementVal):
        returnRegEx = re.search(regExPattern, strSample)
        if returnRegEx is None:
            returnRegEx = NoneReplacementVal
        else:
            returnRegEx = returnRegEx.group(groupNumber).strip()

        return returnRegEx

    def getCategoryDataForOneSeller(self, offer_list_index):

        price = self.getPriceOnly(self.getText(offer_list_index, 'olpOfferPrice'))
        # price = float(extractViaRegex(getText(offer_list_index, 'olpOfferPrice'), '(\d+\.?\d+)', '0'))
        priceShipping = self.getPriceOnly(self.getText(offer_list_index, 'olpShippingPrice'))
        allSellerInfo = self.getText(offer_list_index, 'olpSellerColumn')
        sellerName = self.extractViaRegex(allSellerInfo, '^(.*)\n.*', 1, 'Amazon')
        sellerPositive = int(self.extractViaRegex(allSellerInfo, '(\d\d)%', 1, '0'))
        # sellerRating = extractViaRegex(allSellerInfo, '(\d+,?\d+)\stotal ratings', 1, '0')
        sellerRating = int(self.extractViaRegex(allSellerInfo, '(\d+,?\d+)\stotal ratings', 1, '0').replace(',', ''))
        delivery = self.getText(offer_list_index, 'olpDeliveryColumn')
        isFBA = False
        if 'Fulfillment by Amazon' in delivery:
            isFBA = True

        sellerData = {
            'price': self.getPriceOnly(self.getText(offer_list_index, 'olpOfferPrice')),
            'priceShipping': self.getPriceOnly(self.getText(offer_list_index, 'olpShippingPrice')),
            'priceTotal': price + priceShipping,
            'condition': re.sub(r'([^a-zA-Z0-9\-]+|(\n))', ' ', self.getText(offer_list_index, 'olpCondition').strip()),
            'sellerName': sellerName,
            'sellerPositive': sellerPositive,
            'sellerRating': sellerRating,
            'seller': allSellerInfo,
            'delivery': delivery,
            'isFBA': isFBA
        }

        return sellerData

    def storeAllOffersToPandas(self, allOffers):
        tempPandas = pd.DataFrame()
        for i in allOffers:
            if self.getCategoryDataForOneSeller(i):
                tempPandas = tempPandas.append(self.getCategoryDataForOneSeller(i), ignore_index=True)

        # export the data into a csv file
        tempPandas.to_csv('exported_to_csv.csv')
        return tempPandas

    def storeToNestedDict(self, sellerObject):
        nestedDict = {}
        boolPutInDict = True

        # INCLUDE List for Condition (see private variables)
        conditoinIncludeSet = set([x.strip() for x in self.__conditionTextIncludeList.split(',')])

        # Exclude List for Seller info  (see private variables)
        sellerExcludeSet = set([x.strip() for x in self.__sellerTextExcludeList.split(',')])

        # Exclude List for Delivery  (see private variables)
        deliveryExcludeSet = set([x.strip() for x in self.__deliveryTextExcludeList.split(',')])

        for i in sellerObject:
            boolPutInDict = True
            sellerName = self.getCategoryDataForOneSeller(i)['sellerName']

            if self.getCategoryDataForOneSeller(i)['priceTotal'] < 1:
                boolPutInDict = False

            if self.getCategoryDataForOneSeller(i)['condition'] not in conditoinIncludeSet:
                boolPutInDict = False

            if self.getCategoryDataForOneSeller(i)['sellerPositive'] < 0:
                boolPutInDict = False

            if self.getCategoryDataForOneSeller(i)['sellerRating'] < 0:
                boolPutInDict = False

            deliveryText = self.getCategoryDataForOneSeller(i)['delivery']
            for stringMatch in deliveryExcludeSet:
                if stringMatch in deliveryText:
                    boolPutInDict = False

            sellerText = self.getCategoryDataForOneSeller(i)['seller']
            for stringMatch in sellerExcludeSet:
                if stringMatch in sellerText:
                    boolPutInDict = False

            if boolPutInDict == True:
                nestedDict[sellerName] = self.getCategoryDataForOneSeller(i)

        return(nestedDict)

    def getFullSellerDict(self, alloffersDivTxt):
        combinedDict = self.storeToNestedDict(alloffersDivTxt)
        return combinedDict

    def getLowestPricedObjectBasedOnCriteria(self, myDict):

        # myDict = getFullSellerDict(alloffersDivTxt)
        lowestPrice = 999999999999999
        lowestKey = ''
        boolFBAExists = False

        for k, v in myDict.items():
            if v['priceTotal'] < lowestPrice:
                if v['isFBA']:
                    boolFBAExists = True
                    lowestPrice = v['priceTotal']
                    lowestKey = k

                if not boolFBAExists:
                    lowestPrice = v['priceTotal']
                    lowestKey = k

        return myDict[lowestKey]

    def sandbox(self, singleObj):
        print(self.getText(self.offersSoup, 'olpOfferPrice'))
        print(self.getCategoryDataForOneSeller(self.offersSoup))
        print('ass')
        print(self.storeToPandas(singleObj))


class ObjByClassAttrib(AllOffersObject):

    ''' inherit from AllOffersObject so we can reuse methods to grab data'''

    # def __init__(self, classAttrib):
    def __init__(self, offersSoup, classAttrib):
        super().__init__(offersSoup)
        self.classAttrib = classAttrib

    def test(self):
        print('this is a test : pass parameter {}'.format(self.classAttrib))
