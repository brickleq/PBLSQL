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
from datetime import date, timedelta
from flask import Flask, jsonify

# Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, text

#%%
# # * Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.


vacay_start_date = dt.date(2019,8,4)
vacay_end_date = dt.date(2019,8,10)

#vacay_start_date = dt.datetime.strftime(vacay_start_date, '%Y-%m-%d')
#vacay_end_date = dt.datetime.strftime(vacay_end_date, '%Y-%m-%d')

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect() #do i need this?
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
main_df = pd.DataFrame
main_df = m_df.merge(s_df, on='station')
main_df



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
precip = pd.DataFrame(dict)
precip.set_index('date',inplace=True)
# Sort the dataframe by date
precip.sort_values(by='date',inplace=True)
precip.dropna(inplace=True) # does 'None' mean no precipitation, or no record of precipitation? hashtag ain't nobody got time for that
precip
df = precip
#%%
# Use Pandas Plotting with Matplotlib to plot the data
plt.plot(df.index,df['prcp'])
plt.xticks=365
plt.yticks=7
plt.xlabel='Date'
plt.ylabel='Precipitation'
plt.title('Precipitation - Past Year')
plt.show()
plt.savefig('prcp.png')
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
session.query(Measurement.station).distinct().count() #output: 9
#session.query(Station.station).distinct().count() #output: 9. Samesies!

#%%
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
most_active_stations = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
print(most_active_stations)

#%%
# Using the station id from the previous query, 
most_active_station = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
most_active_station
most_active_station = most_active_station[0]
most_active_station

#%%
# calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
'''
lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()
display(lowest_temp)
'''
#%%
min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(min_temp)
max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(max_temp)
avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(avg_temp)

#%%
# Choose the station with the highest number of temperature observations.
station_with_most_tobs = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).first()
display(station_with_most_tobs)
station_with_most_tobs = station_with_most_tobs[0]
display(station_with_most_tobs)
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
last_years_tobs = session.query(Measurement.tobs).filter(Measurement.date >= data_start_date).all()
display(last_years_tobs)
last_years_tobs = pd.DataFrame(data=last_years_tobs)
#tobs_for_histogram = pd.DataFrame
#last_years_tobs = pd.Series(last_years_tobs)
#tobs_for_histogram['tobs'] = last_years_tobs 
tobs_for_histogram = last_years_tobs['tobs'].tolist()
#%%

# plt.hist(last_years_tobs,bins=12) ### HANGS IN BOTH VSCODE AND JUPYTER NOTEBOOK
import matplotlib.pyplot as plt
plt.hist(tobs_for_histogram, bins=12)
plt.title('Temperature Observations Over 12 Months - Most Active Station')
plt.xlabel('Temperature (F)')
plt.ylabel('Frequency')
plt.legend('Temperature Observations', location='best')
plt.show()
plt.savefig('histogram.png')
#%% [markdown]
# ![precipitation](Images/station-histogram.png)

#%%
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
start_date = data_start_date
end_date = data_end_date
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
start_date = vacay_start_date - timedelta(days=730) #using 2017 data b/c 2018 data not available
end_date = vacay_end_date - timedelta(days=730)
print(calc_temps(start_date,end_date))
'''
trip_temps = str(calc_temps(start_date,end_date))
trip_temps = trip_temps.split(', ')
peak_to_peak = trip_temps[2] - trip_temps[0]
trip_temps = calc_temps(start_date,end_date)
'''
#%%
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
plt.bar(x=79.70370370370371, yerr = 12, width=1, height=90)
#plt.errorbar(71,83,yerr=12)
plt.title='Trip Avg Temp'
plt.show()
plt.savefig('bar_chart.png')

#%%
# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
vacay_start_date = dt.datetime(2019,8,4)
vacay_end_date = dt.datetime(2019,8,10)

#vacay_start_date = dt.datetime.strftime(vacay_start_date, '%Y-%m-%d')
#vacay_end_date = dt.datetime.strftime(vacay_end_date, '%Y-%m-%d')
start_date = vacay_start_date - timedelta(days=730)
end_date = vacay_end_date - timedelta(days=730)

main_df.head()
precip_df = main_df[(main_df['date'] > start_date) & (main_df['date'] <= end_date)]
precip_df
grouped = precip_df.groupby(['station'])['prcp'].sum().reset_index()
grouped = grouped.sort_values('prcp',ascending=False)
grouped
precip_df = pd.DataFrame
precip_df = grouped.merge(s_df, on='station')
precip_df
#%%
stations = precip_df.station.unique()

#%%
'''
## Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

* Use FLASK to create your routes.
'''
app = Flask(__name__)
import warnings
warnings.filterwarnings('ignore')

'''
### Routes

* `/`

  * Home page.

  * List all routes that are available.
'''
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end>"
    )
#%%

'''
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
'''