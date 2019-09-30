from oaSscrape import AMZSoupObject, AllOffersObject

ItemNumber = '007738248X'
myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')
soup = myAmazonObj.soupObj()


# all the offers for each ROW is stored in this Div class
# creates a list of bojects which we will further parse out
alloffersObj = AllOffersObject(soup)  # stores the entire soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllOffers()  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'

print(alloffersObj.storeAllOffersToPandas(alloffersDivTxt))
combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
print(combinedDict)
lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
print('\n\n\n\n\n')
print(lowestDict)
