import time
from selenium import webdriver
url = 'https://www.amazon.com/gp/offer-listing/1506330207'



def saveToFile(CanOrUS,url):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    fileNameDict = {
        '.ca': 'tempCan.html',
        '.com': 'tempUS.html'
    }

    with open(fileNameDict.get(CanOrUS), 'w') as f:
        f.write(driver.page_source)

saveToFile('.com',url)