import pandas as pd
ronDict = {'0133356728': {'price_canada': 58.7, 'Condition_canada': 'Used - Very Good', 'price_usa': 65, 'Condition_usa': 'something wrong happened'},
           '2222': {'price_canada': 50, 'Condition_canada': 'Used - Very Good', 'price_usa': 100, 'Condition_usa': 'something wrong happened'}}


# ronDict = {'price1': 58.7, 'Condition1': 'Used - Very Good', 'price2': -99, 'Condition2': 'something wrong happened'}



print(ronDict)
df = pd.DataFrame()
print(df)

def passMyDf (df1, myDict):

    def pct_gain(x, args=()): return (args - x) / x

    dfTemp = pd.DataFrame.from_dict(myDict, orient='index')
    dfTemp["ProfitFactor1"] = pct_gain(dfTemp.price_canada, dfTemp.price_usa).round(2)
    return dfTemp

x = passMyDf (df,ronDict)
df= df.append(x)
df= df.append(x)

print('*************************Final')
print(df)