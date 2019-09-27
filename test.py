import re


# def getPriceOnly(priceString):
#     x = re.sub('[^0-9.]', "", priceString)
#     return(float(x))


def getPriceOnly(priceString):
    return(float(re.sub('[^0-9.]', "", priceString)))


print(getPriceOnly('ffaf 123.45  faff') + 9000)
print(type(getPriceOnly('ffaf 123.45  faff')))


def myFunc(e):
    return len(e)


def myFuncLast(a):
    return a[-1]


def myFunc2nd(a):
    return a[1]


cars = ['149', '357', '238']

# cars.sort(key=myFunc)
# print(cars)

cars.sort(key=myFuncLast)
print(cars)

cars.sort(key=lambda x: x[1])
print(cars)
