import pandas as pd
ronDict = {'0133356728': {'price_canada': 58.7, 'Condition_canada': 'Used - Very Good', 'price_usa': -99, 'Condition_usa': 'something wrong happened'},
           '2222': {'price_canada': 50, 'Condition_canada': 'Used - Very Good', 'price_usa': 75, 'Condition_usa': 'something wrong happened'}}


# ronDict = {'price1': 58.7, 'Condition1': 'Used - Very Good', 'price2': -99, 'Condition2': 'something wrong happened'}


print(ronDict)


testDf = pd.DataFrame.from_dict(ronDict, orient='index')
print(testDf)


def pct_gain(x, y): return (y - x) / x


testDf["ProfitFactor"] = pct_gain(testDf.price_canada, testDf.price_usa)
print(testDf)

# diff = testDf.price_canada.apply(pct_gain2)
# print(diff)


# testDf["NewCol"] = testDf.price_canada.apply(pct_gain, y=testDf.price_usa)
# print(testDf)
