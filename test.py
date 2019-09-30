from oaSscrape import AMZSoupObject

ItemNumber = '007738248X'
myclass = AMZSoupObject(ItemNumber, 'com', 'test.html')
print(myclass.itemNumber)
# print(myclass.soupObj())
print(myclass.__doc__)
