'''
# Surfs Up!

![surfs-up.jpeg](Images/surfs-up.jpeg)

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

## Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Use the provided [starter notebook](climate_starter.ipynb) and [hawaii.sqlite](Resources/hawaii.sqlite) files to complete your climate analysis and data exploration.

* Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

* Use SQLAlchemy `create_engine` to connect to your sqlite database.

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation.png)

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Design a query to calculate the total number of stations.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

  * Hint: You may need to use functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.

* Design a query to retrieve the last 12 months of temperature observation data (tobs).

  * Filter by the station with the highest number of observations.

  * Plot the results as a histogram with `bins=12`.

    ![station-histogram](Images/station-histogram.png)

- - -

## Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

* Use FLASK to create your routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

* You will need to join the station and measurement tables for some of the analysis queries.

* Use Flask `jsonify` to convert your API data into a valid JSON response object.

- - -

### Optional: Other Recommended Analyses

* The following are optional challenge queries. These are highly recommended to attempt, but not required for the homework.

### Temperature Analysis

* The starter notebook contains a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.

* Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

* Plot the min, avg, and max temperature from your previous query as a bar chart.

  * Use the average temperature as the bar height.

  * Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

    ![temperature](Images/temperature.png)

### Daily Rainfall Average.

* Calculate the rainfall per weather station using the previous year's matching dates.

* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

* You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic tobs that match that date string.

* Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Use Pandas to plot an area plot (`stacked=False`) for the daily normals.

  ![daily-normals](Images/daily-normals.png)

## Copyright

Data Boot Camp ©2019. All Rights Reserved.
'''

#%%
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

# Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct


#%%
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

 #%% [markdown]
# # Exploratory Climate Analysis

#%%
# Design a query to retrieve the last 12 months of precipitation data and plot the results

m_data = engine.execute('SELECT * FROM Measurement')
# station,date,prcp,tobs
stations = []
dates = []
prcps = []
tobses = []

for record in m_data:
    station = record[1]
    date = dt.datetime.strptime(record[2],'%Y-%m-%d')
    dates.append(date)
    stations.append(str(station))
    prcp = record[3]
    prcps.append(prcp)
    tobs = record[4]
    tobses.append(tobs)
dict = {'station':stations,'date':dates,'prcp':prcps,'tobs':tobses}
print(dict)
m_df = pd.DataFrame(dict)
m_df.dropna(inplace=True) # does 'None' mean no precipitation, or no record of precipitation?
#%%

m_df

#%%
# station,name,latitude,longitude,elevation
s_data = engine.execute('SELECT * FROM Station')

stations = []
names = []
latitudes = []
longitudes = []
elevations = []

for record in s_data:
    station = str(record[1])
    name = str(record[2])
    latitude = float(record[3])
    longitude = float(record[4])
    elevation = float(record[5])
    stations.append(station)
    names.append(name)
    latitudes.append(latitude)
    longitudes.append(longitude)
    elevations.append(elevation)
dict = {'station':stations,'name':names,'latitude':latitudes,'longitude':longitudes,'elevation':elevations}
print(dict)
s_df = pd.DataFrame(dict)
s_df
#%%
df = pd.DataFrame
df = m_df.merge(s_df, on='station')
df



#%%
# # Calculate the date 1 year ago from the last data point in the database
data_end_date = max(dates)
data_start_date = data_end_date - timedelta(days=365)
print(data_start_date,data_end_date)
# output: 2016-08-23 00:00:00 2017-08-23 00:00:00
#%%
# Perform a query to retrieve the data and precipitation scores
precip = engine.execute('SELECT date,prcp FROM Measurement WHERE date >= ?',data_start_date)
dates = []
prcps = []

for record in precip: 
    print(record)
    date = dt.datetime.strptime(record[0],'%Y-%m-%d')
    dates.append(date)
    prcp = record[1]
    prcps.append(prcp)
dict = {'date':dates,'prcp':prcps}
# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(dict)
df.set_index('date',inplace=True)
# Sort the dataframe by date
df.sort_values(by='date',inplace=True)
df.dropna(inplace=True) # does 'None' mean no precipitation, or no record of precipitation? hashtag ain't nobody got time for that
df
#%%
# Use Pandas Plotting with Matplotlib to plot the data
plt.plot(df.index,df['prcp'])
plt.xticks=365
plt.xlabel='Date'
plt.ylabel='Precipitation (mm)'
plt.title('Precipitation (mm) - Past Year')
plt.show()
#%%

#%% [markdown]
# ![precipitation](Images/precipitation.png)

#%%
# Use Pandas to calcualte the summary statistics for the precipitation data
df.describe()
#%% [markdown]
# ![describe](Images/describe.png)

#%%
# Design a query to show how many stations are available in this dataset?
session.query(Measurement.station).distinct().count()
session.query(Station.station).distinct().count()
#%%



#%%
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.


#%%
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?


#%%
# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

#%% [markdown]
# ![precipitation](Images/station-histogram.png)

#%%
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


#%%
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.


#%%
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


#%%
# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

#%% [markdown]
# ## Optional Challenge Assignment

#%%
# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")


#%%
# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


#%%
# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


#%%
# Plot the daily normals as an area plot with `stacked=False`


