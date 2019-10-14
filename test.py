from oaSscrape import AMZSoupObject, AllOffersObject, ObjByClassAttrib

ItemNumber = '0393975916'
# myAmazonObj = AMZSoupObject(ItemNumber, 'com', 'testUS.html')
myAmazonObj = AMZSoupObject(ItemNumber, 'ca', None)
soup = myAmazonObj.soupObj()
# print(soup)


# all the offers for each ROW is stored in this Div class
# creates a list of bojects which we will further parse out
alloffersObj = AllOffersObject(soup)  # stores the entire soup object to a Class to be further filtered
alloffersDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffer'
# print(alloffersDivTxt)

# print(alloffersObj.storeAllOffersToPandas(alloffersDivTxt))
# combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
# print(combinedDict)
# lowestDict = alloffersObj.getLowestPricedObjectBasedOnCriteria(combinedDict)
# # print('\n\n\n\n\n')
# print(lowestDict)


print(alloffersObj.get_conditionTextIncludeList())
print(alloffersObj.conditionTextIncludeListProperty)
alloffersObj.conditionTextIncludeListProperty = 'New'
print(alloffersObj.conditionTextIncludeListProperty)
print(alloffersObj.deliveryTextExcludeListx)
alloffersObj.deliveryTextExcludeListx = 'ccc'
print(alloffersObj.deliveryTextExcludeListx)

# alloffersObj = AllOffersObject(soup)  # stores the entire soup object to a Class to be further filtered
# alloffrsDivTxt = alloffersObj.getAllDataFromAttrib('class', 'olpOffer')  # extracts only the Offers div tags baed on attrs={'class': 'olpOffe'
#                  # alloffersObj.getAllDataFromAttrib('class', 'olpOffer')
# print(alloffrsDivTxt)
# print(alloffersObj.extractViaRegex(str(alloffrsDivTxt), 'Hardcover', 0, 'No Matching Keyword'))

# combinedDict = alloffersObj.getFullSellerDict(alloffersDivTxt)
# print(combinedDict)
