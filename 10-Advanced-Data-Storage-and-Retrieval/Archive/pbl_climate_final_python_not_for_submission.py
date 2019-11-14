
#%%
# Dependencies
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date, timedelta

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

# Reflect Tables into SQLAlchemy ORM

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
#  # Exploratory Climate Analysis

#%%
# Design a query to retrieve the last 12 months of precipitation data and plot the results

m_data = engine.execute('SELECT * FROM Measurement')

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

m_df = pd.DataFrame(dict)
m_df.dropna(inplace=True) # does 'None' mean no precipitation, or no record of precipitation?


#%%



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
s_df = pd.DataFrame(dict)


#%%
main_df = pd.DataFrame
main_df = m_df.merge(s_df, on='station')


#%%
# # Calculate the date 1 year ago from the last data point in the database
data_end_date = max(dates)
data_start_date = data_end_date - timedelta(days=365)
print(data_start_date,data_end_date)


#%%
# Perform a query to retrieve the data and precipitation scores
precip = engine.execute('SELECT date,prcp FROM Measurement WHERE date >= ?',data_start_date)
dates = []
prcps = []

for record in precip: 
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
# Remove rows with null values
precip.dropna(inplace=True)


#%%
# Use Pandas Plotting with Matplotlib to plot the data
plt.plot(precip.index,precip['prcp'])
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.title('Precipitation - Past Year')
plt.show()
plt.savefig('prcp.png')


#%%
# Use Pandas to calcualte the summary statistics for the precipitation data
precip.describe()


#%%
# Design a query to show how many stations are available in this dataset?
session.query(Measurement.station).distinct().count() #output: 9
#session.query(Station.station).distinct().count() #output: 9. Samesies!


#%%
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
most_active_stations = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
most_active_stations


#%%
# Using the station id from the previous query, 
most_active_station = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
most_active_station
most_active_station = most_active_station[0]
most_active_station


#%%
# calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(min_temp)
max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(max_temp)
avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station==most_active_station).all()
display(avg_temp)


#%%
# Choose the station with the highest number of temperature observations.
station_with_most_tobs = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).first()
station_with_most_tobs = station_with_most_tobs[0]
display(station_with_most_tobs)
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
last_years_tobs = session.query(Measurement.tobs).filter(Measurement.date >= data_start_date).all()
last_years_tobs = pd.DataFrame(data=last_years_tobs)
#tobs_for_histogram = pd.DataFrame
#last_years_tobs = pd.Series(last_years_tobs)
#tobs_for_histogram['tobs'] = last_years_tobs 
tobs_for_histogram = last_years_tobs['tobs'].tolist()


#%%
# plt.hist(last_years_tobs,bins=12) ### HANGS IN BOTH VSCODE AND JUPYTER NOTEBOOK
plt.hist(tobs_for_histogram, bins=12)
plt.title('Temperature Observations Over 12 Months - Most Active Station')
plt.xlabel('Temperature (F)')
plt.ylabel('Frequency')
plt.legend('tobs', loc=2)
plt.show()
plt.savefig('histogram.png')


#%%
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
start_date = data_start_date
end_date = data_end_date
def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


#%%
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
start_date = vacay_start_date - timedelta(days=730) #using 2017 data b/c 2018 data not available
end_date = vacay_end_date - timedelta(days=730)
vacation_dates = calc_temps(start_date,end_date)
vacation_dates = pd.DataFrame


#%%
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

#x = 'Avg.'
#plt.bar(x, 79.70370370370371, yerr = 12)
plt.bar('Avg',79.70370370370371,yerr=12)
plt.title('Trip Avg Temp')
plt.ylabel('Temperature °F')
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



