import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


class AMZSoupObject:

    ''' Creates soup object from Amazon Listing
        for parameters use:
            itemNumber => ISBN number for book
            dotCAordotCOM =>
                = 'ca' to get the Canadian Prices
                = 'com' to get the Americian Prices filtered by Prime Eligible

            readFromFile => option parameter, if set then read from a file instead of going to actual site

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
            print('going to read file')
            return BeautifulSoup(open(self.readFromFile), 'lxml')  # note for some reason html.parser was not getting all the data
        else:
            response = requests.get(self.urlType, headers=HEADERS)
            print('going to web')

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)

            return response
