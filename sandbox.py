
import random 

def randomSleep(myList=None):
    # Adding Random sleep times to avoid throttling from Amazon
    sleepTimesSeconds = [5,12,17,24]
    if myList:
        sleepTimesSeconds = myList
    
    # sleep(random.choice(sleepTimesSeconds)) # sleep rando seconds seconds
    print(random.choice(sleepTimesSeconds)) # sleep rando seconds seconds


for i in range(6):
    randomSleep([4,6,1])