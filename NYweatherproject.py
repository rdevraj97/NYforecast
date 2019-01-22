from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd

# url to scrap; downloads webpage that contains New York's forecast
my_url = 'https://forecast.weather.gov/MapClick.php?lat=40.7146&lon=-74.0071#.XDqft1xKhPY'

page_html = urlopen(my_url)


# creates Beautifulsoup class to parse the page
parse = soup(page_html, 'html.parser')

# we search for seven_day which is the div that contains extended forecast items
ext_forecast = parse.find(id="seven-day-forecast")

# each forecast item is contained in "tombstone-container" class.
forecast_items = ext_forecast.find_all(class_="tombstone-container")

# selects all different types of periods that are described in the forecast
period_timings = ext_forecast.select(".tombstone-container .period-name")

periods = [pt.get_text() for pt in period_timings]

# extracts all short descriptions from the tombstone-container css tag 
short_descriptions = [sd.get_text() for sd in ext_forecast.select(".tombstone-container .short-desc")]

# extracts the temperatures scattered over different periods
temperatures = [t.get_text() for tmp in ext_forecast.select(".tombstone-container .temp")]

# extracts all long descriptions of the weather
long_descriptions = [ld["title"] for ld in ext_forecast.select(".tombstone-container img")]


# Pandas dataframe; creates a well-formatted and easily readable table,
# consisting of New York's weather forecast for the next few days

forecast_NY = pd.DataFrame({
    "When?": periods,
    "Weather": short_descriptions,
    "Temperature": temperatures,
    "Detailed weather": long_descriptions
    })

    
    
