import pandas as pd
ronDict = {'0133356728': {'price_canada': 58.7, 'Condition_canada': 'Used - Very Good', 'price_usa': -99, 'Condition_usa': 'something wrong happened'},
'2222': {'price_canada': 58.7, 'Condition_canada': 'Used - Very Good', 'price_usa': -99, 'Condition_usa': 'something wrong happened'}}


# ronDict = {'price1': 58.7, 'Condition1': 'Used - Very Good', 'price2': -99, 'Condition2': 'something wrong happened'}


print(ronDict)


test = pd.DataFrame.from_dict(ronDict, orient='index')
print(test)


# data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
# test = pd.DataFrame.from_dict(data)
# print(test)
