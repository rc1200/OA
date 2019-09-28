import re

myjson = {
    'habitualexcellence': {
        'price': 59.99,
        'priceShipping': 6.49,
        'priceTotal': 66.48,
        'condition': 'Used\n         - Like New',
        'seller': 'habitualexcellence \n\n\nJust Launched\n                        (Seller Profile)',
        'delivery': 'Ships from ON, Canada.\n        \n\nShipping rates\n                 and return policy.'
    },
    'Amazon': {
        'price': 89.95,
        'priceShipping': 0.0,
        'priceTotal': 89.95,
        'condition': 'New',
        'seller': '',
        'delivery': 'Shipping rates\n                 and return policy.'
    }}

txt = 'Ergodebooks Ships from USA \n\n\n4.5 out of 5 stars\n93% positive over the past 12 months. (10,240 total ratings)'


def extractViaRegex(strSample, regExPattern, groupNumber, NoneReplacementVal):
    returnRegEx = re.search(regExPattern, strSample)
    if returnRegEx is None:
        returnRegEx = NoneReplacementVal
    else:
        print('aaa' + returnRegEx.group(0))
        returnRegEx = returnRegEx.group(groupNumber).strip()

    return returnRegEx


sellerPositive = extractViaRegex(txt, r'(\d\d)%', 1, '0')
print(sellerPositive)

txt = 'x           New'
sellerPositive = re.search(r'(?<!x)\s*New', txt)

# print(sellerPositive.group(0))
print(sellerPositive)


a = 'Used - Like New'
b = 'New'

print(a in b)
print(b in a)
