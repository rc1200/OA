from datetime import datetime
from time import sleep


myDict =  {1: {'Name': 'a'},
2: {'Name' : 'b'},
3: {'Name' : 'a'}
}
x = [v['Name'] for k,v in myDict.items()]
print(x)
occurance = x.count('a')
print(occurance)

# # print(myDict)

# def test(mydict):
#     nestedDict = {}

#     for k,v in myDict.items():
#         x = [v for k,v in nestedDict.items()]
#         print (k, v)
#         if v in x:
#             countOcc = x.count(v)
#             print(countOcc)
#             nestedDict[v + str(countOcc)] = v
#         else:
#             nestedDict[v] = v

#     print (nestedDict)
#     return nestedDict

# test(myDict)



import re

#Check if the string starts with "The" and ends with "Spain":

import re

mylist = ["dog", "cat", "wildcat", "thundercat", "cow", "hooo"]
print ('mylist.count("dog")')
print (mylist.count("dog"))
r = re.compile(".*cat")
newlist = list(filter(r.match, mylist)) # Read Note
print(len(newlist))
if newlist:
    print('something in list')