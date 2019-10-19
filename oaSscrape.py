import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


class AMZSoupObject(object):

    ''' Doc String

        Creates soup object from Amazon Listing
        for parameters use:
            itemNumber => ISBN number for book
            dotCAordotCOM =>
                = 'ca' to get the Canadian Prices
                = 'com' to get the Americian Prices filtered by Prime Eligible

            [readFromFile] => option parameter, put File Name of the html document instad of fetching from web
                            if has value then read from a file instead of going to actual site

    sample: myAmazonObj = AMZSoupObject('007738248X', 'com', 'testUS.html') N.B. Reads from file because of file name 'testUS.html'
    sample: myAmazonObj = AMZSoupObject('007738248X', 'com') NOT reading from file, instead going to web to fetch data

    '''

    # constant for all classes
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

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
            # note for some reason html.parser was not getting all the data
            return BeautifulSoup(open(self.readFromFile), 'lxml')
        else:
            response = requests.get(self.urlType(), headers=self.HEADERS)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)

            return BeautifulSoup(response.content, 'lxml')


class AllOffersObject(object):
    """docstring for Alloffers
        all the offers for each ROW is stored in this Div class
        creates a list of ojects which we will further parse out

        getAllDataFromAttrib: stores HTML doc for all the offers



    """
    # Class Variables, use Setters to change default values
    __PriceMustBeGreaterThan = 1
    __PositiveFeedbackPctMustBeGreaterThan = 87
    __SellerRatingMustBeGreaterThan = 34

    def __init__(self, offersSoup, USFilter=None):
        self.offersSoup = offersSoup
        self.USFilter = USFilter

        # Private Varables N.B. Keep hard coded, add methon to update later
        # INCLUDE List for Condition
        self.__conditionTextExcludeList = 'used-acceptablexxx, collectible-acceptable, Rental'
        # Exclude List for Seller info
        self.__sellerTextExcludeList = 'Just Launched'
        # Exclude List for Delivery
        self.__deliveryTextExcludeList = 'India'

        self.setUsFilters(self.USFilter)

    # change Values if US Prices
    def setUsFilters(self, v):
        if v is not None:
            self.__PriceMustBeGreaterThan = 1
            self.__PositiveFeedbackPctMustBeGreaterThan = -99
            self.__SellerRatingMustBeGreaterThan = -99
            self.__conditionTextExcludeList = 'Rental'
            self.__sellerTextExcludeList = 'xazxx'
            self.__deliveryTextExcludeList = 'xazxx'

        return None

    # Setters for Class Variables

    def setPriceMustBeGreaterThan(self, v):
        self.__PriceMustBeGreaterThan = v

    def setPositiveFeedbackPctMustBeGreaterThan(self, v):
        self.__PositiveFeedbackPctMustBeGreaterThan = v

    def setSellerRatingMustBeGreaterThan(self, v):
        self.__SellerRatingMustBeGreaterThan = v

    # Option 1 for getter and setter, use variable to call the getter and setter methods and use as a property
    def get_conditionTextIncludeList(self):
        return self.__conditionTextExcludeList

    def set_conditionTextIncludeList(self, setter_value):
        self.__conditionTextExcludeList = setter_value

    conditionTextIncludeListProperty = property(
        get_conditionTextIncludeList, set_conditionTextIncludeList)

    # Option 2, explictly using decorators
    @property
    def deliveryTextExcludeList(self):
        return self.__deliveryTextExcludeList

    # @deliveryTextExcludeList.setter
    # instead use a method instead to explictly define it is a method
    def setDeliveryTextExcludeList(self, setter_value):
        self.__deliveryTextExcludeList = setter_value

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

        price = self.getPriceOnly(self.getText(
            offer_list_index, 'olpOfferPrice'))
        # price = float(extractViaRegex(getText(offer_list_index, 'olpOfferPrice'), '(\d+\.?\d+)', '0'))
        priceShipping = self.getPriceOnly(
            self.getText(offer_list_index, 'olpShippingPrice'))
        allSellerInfo = self.getText(offer_list_index, 'olpSellerColumn')
        sellerName = self.extractViaRegex(
            allSellerInfo, '^(.*)\n.*', 1, 'Amazon')
        sellerPositive = int(self.extractViaRegex(
            allSellerInfo, '(\d+)%', 1, '0'))
        # sellerRating = extractViaRegex(allSellerInfo, '(\d+,?\d+)\stotal ratings', 1, '0')
        sellerRating = int(self.extractViaRegex(
            allSellerInfo, '(\d?,?\d+)\stotal ratings', 1, '0').replace(',', ''))
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
                tempPandas = tempPandas.append(
                    self.getCategoryDataForOneSeller(i), ignore_index=True)

        # export the data into a csv file
        tempPandas.to_csv('exported_to_csv.csv')
        return tempPandas

    def storeToNestedDictFiltered(self, sellerObject):
        nestedDict = {}
        boolPutInDict = True

        # INCLUDE List for Condition (see private variables)
        conditoinExcludeSet = set(
            [x.strip() for x in self.__conditionTextExcludeList.split(',')])

        # Exclude List for Seller info  (see private variables)
        sellerExcludeSet = set(
            [x.strip() for x in self.__sellerTextExcludeList.split(',')])

        # Exclude List for Delivery  (see private variables)
        deliveryExcludeSet = set(
            [x.strip() for x in self.__deliveryTextExcludeList.split(',')])

        for i in sellerObject:
            boolPutInDict = True
            sellerName = self.getCategoryDataForOneSeller(i)['sellerName']
            currentConditon = self.getCategoryDataForOneSeller(i)['condition']

            if self.getCategoryDataForOneSeller(i)['priceTotal'] < self.__PriceMustBeGreaterThan:
                # if self.getCategoryDataForOneSeller(i)['priceTotal'] < 1:
                boolPutInDict = False

            if currentConditon in conditoinExcludeSet:
                boolPutInDict = False

            if self.getCategoryDataForOneSeller(i)['sellerPositive'] < self.__PositiveFeedbackPctMustBeGreaterThan:
                # if self.getCategoryDataForOneSeller(i)['sellerPositive'] != 'sdsd':
                # if self.getCategoryDataForOneSeller(i)['sellerPositive'] < 0:
                print('{}  xxxxxxxxxxxxx   storeToNestedDictFiltered  xxxxxxxxxxxxxxx {}'.format(
                    self.__PositiveFeedbackPctMustBeGreaterThan, self.getCategoryDataForOneSeller(i)['sellerPositive']))
                boolPutInDict = False

            if self.getCategoryDataForOneSeller(i)['sellerRating'] < self.__SellerRatingMustBeGreaterThan:
                # if self.getCategoryDataForOneSeller(i)['sellerRating'] < 0:
                # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxx', self.getCategoryDataForOneSeller(i)['sellerRating'])
                boolPutInDict = False

            deliveryText = self.getCategoryDataForOneSeller(i)['delivery']
            for stringMatch in deliveryExcludeSet:
                if stringMatch in deliveryText:
                    boolPutInDict = False

            sellerText = self.getCategoryDataForOneSeller(i)['seller']
            for stringMatch in sellerExcludeSet:
                if stringMatch in sellerText:
                    boolPutInDict = False

            # Amazon Seller Hidden Gem - normally gets filtered out due to no ratings
            # Special conditon for Rental as we want to ensure we filter that out
            if sellerName == 'Amazon' and currentConditon != 'Rental':
                boolPutInDict = True

           
            if boolPutInDict == True:
                nestedDict[sellerName] = self.getCategoryDataForOneSeller(i)

        return(nestedDict)

    def getFullSellerDictFiltered(self, alloffersDivTxt):
        print(self.storeToNestedDictFiltered(alloffersDivTxt))
        return self.storeToNestedDictFiltered(alloffersDivTxt)
        # combinedDict = self.storeToNestedDictFiltered(alloffersDivTxt)
        # return combinedDict

    def getLowestPricedObjectBasedOnCriteria(self, myDict):

        # myDict = getFullSellerDictFiltered(alloffersDivTxt)
        lowestPrice = 999999999999999
        lowestKey = ''
        boolFBAExists = False

        # fake dictionary to ensure something is passed if no matching criteria or issues with Amazon
        fakeDict = {'fakeDict': {
            'price': -99,
            'priceShipping': 0.0,
            'priceTotal': -99,
            'condition': 'something wrong happened',
            'sellerName': 'fakeDict',
            'sellerPositive': -99,
            'sellerRating': -99,
            'seller': 'something wrong happened',
            'delivery': '',
            'isFBA': False
        }}

        for k, v in myDict.items():
            if v['priceTotal'] < lowestPrice:
                if v['isFBA']:
                    boolFBAExists = True
                    lowestPrice = v['priceTotal']
                    lowestKey = k
                    print('current lowest key is {}'.format(lowestKey))

                if not boolFBAExists:
                    lowestPrice = v['priceTotal']
                    lowestKey = k
                    print('current lowest key is {}'.format(lowestKey))

        if myDict:
            return myDict[lowestKey]
        else:
            print('ffffffffffffffff             fakeDict           fffffffffff')
            print(fakeDict['fakeDict'])
            return fakeDict['fakeDict']

    def sandbox(self, singleObj):
        print(self.getText(self.offersSoup, 'olpOfferPrice'))
        print(self.getCategoryDataForOneSeller(self.offersSoup))
        print('ass')


class ObjByClassAttrib(AllOffersObject):

    ''' inherit from AllOffersObject so we can reuse methods to grab data'''

    # def __init__(self, classAttrib):
    def __init__(self, offersSoup, classAttrib):
        super().__init__(offersSoup)
        self.classAttrib = classAttrib

    def test(self):
        print('this is a test : pass parameter {}'.format(self.classAttrib))
