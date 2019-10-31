from datetime import datetime
import pandas as pd
import random
import re
import threading
from time import sleep
from oaSscrape import AMZSoupObject, AllOffersObject
from oaUtilities import randomSleep, splitIntoListArray, getBothCAN_US, dictToDF, saveToFile, combineCsvToOneFile
import os
from selenium import webdriver

BASE_oaAPP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_oaAPP_Utilities_DIR  = os.path.join(BASE_oaAPP_DIR, 'cadus_utilities')

def utilsPathFileName(fileName=None):
    return os.path.join(BASE_oaAPP_Utilities_DIR, fileName)


chrome_path = 'c:\\github\\OA\\oaApp\\cadusApp\\cadus_utilities\\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)
driver.get('https://www.google.com/')


# 'c:\\github\\OA\\oaApp\\cadusApp\\cadus_utilities\\'
