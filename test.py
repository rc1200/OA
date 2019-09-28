import re
txt = 'Ships from Japan.\n          bef,comm      Learnshipping time. return policy.'

deliveryStrippedSet = set(re.split('(\.|\s|\,)', txt))
s1 = set(deliveryStrippedSet)
print(s1)


for i in deliveryStrippedSet:
    print(i)
