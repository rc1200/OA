import pandas as pd
import requests
from bs4 import BeautifulSoup


# store entire object into a variable
page = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=41.8843&lon=-87.6324#.XIRQYFNKgUE'
)

# lets the object know we are passing an HTML and to pars it as that
soup = BeautifulSoup(page.content, 'html.parser')

# grabbing all the code inside the div based on the ID
week = soup.find(id='seven-day-forecast-body')

# store everything within the container
# NOTE since we are using Class container instead of a tag we use "class_" since class is reserved
items = week.find_all(class_='tombstone-container')

# storing the text into a list using list comprehension
period_names = [item.find(class_='period-name').get_text() for item in items]
short_descriptions = [item.find(class_='short-desc').get_text() for item in items]
temperatures = [item.find(class_='temp').get_text() for item in items]

# passing a dictionary using Pandas Dataframe ... has the Key and List
weather_stuff = pd.DataFrame(
    {
        'period': period_names,
        'short_descriptions': short_descriptions,
        'temperatures': temperatures,
    })

print(weather_stuff)

# export the data into a csv file
weather_stuff.to_csv('exported_to_csv.csv')

'''

'''
