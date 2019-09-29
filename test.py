import re

deliveryText = 'TotalBook \n\n\n4.5 out of 5 stars\n81% positive over the past 12 months. (22 total ratings)'


deliveryTextExcludeList = 'Japan, India, Amazon, 12 months'
deliveryExcludeSet = set([x.strip() for x in deliveryTextExcludeList.split(',')])


for stringMatch in deliveryExcludeSet:
    if stringMatch in deliveryText:
        print('get out')


def isFBA(deliveryText):
    return 'cool' if 'TotalBook' in deliveryText:
