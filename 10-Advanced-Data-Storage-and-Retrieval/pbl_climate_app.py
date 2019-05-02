import numpy as np
import pandas as pd
import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import timedelta
from flask import Flask, jsonify

import warnings
warnings.filterwarnings('ignore')

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# List all available api routes.
@app.route('/')
def welcome():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/START<br/>'
        f'format start date YYYY-MM-DD <br/>'
        f'/api/v1.0/START/END<br/>'
        f'format start date YYYY-MM-DD, end date as YYYY-MM-DD'
    )

#  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

#  * Return the JSON representation of your dictionary.

@app.route('/precipitation')
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp)
    dict = {}
    dates = []
    prcps = []
    for result in results:
        dates.append(result[0])
        prcps.append(result[1])
        dict = {'date':dates,'prcp':prcps}
    return jsonify(dict)

#   * Return a JSON list of stations from the dataset.

@app.route('/stations')
def stations():
    results = session.query(Station.all())
    dict = {}
    station_ids = []
    names = []
    latitudes = []
    longitudes = []
    elevations = []
    for result in results:
        station_id = str(record[1])
        name = str(record[2])
        latitude = float(record[3])
        longitude = float(record[4])
        elevation = float(record[5])
        station_ids.append(station_id)
        names.append(name)
        latitudes.append(latitude)
        longitudes.append(longitude)
        elevations.append(elevation)
    dict = {'station':stations,'name':names,'latitude':latitudes,'longitude':longitudes,'elevation':elevations}
    return jsonify(dict)

# * query for the dates and temperature observations from a year from the last data point.
# * Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route('/tobs')
def tobs():
    dates = []
    tobses = []
    dict = {}
    start_date = '2016-08-23'
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    results = engine.execute('SELECT * FROM Measurement')
    for result in results:
        date = datetime.datetime.strptime(result[2],'%Y-%m-%d')
        tobs = result[4]
        if date >= start_date:
            dates.append(date)
            tobses.append(tobs)
    dict = {'date':dates,'tobs':tobses}
    return jsonify(dict)

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route('/<start>')
def start_date_only(start):
    start_date = datetime.datetime.strptime(start,'%Y-%m-%d')
    dict = {}
    mins = []
    avgs = []
    maxes = []
    results = session.query((func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all())
    for result in results:
        mins.append(result[0])
        avgs.append(result[1])
        maxes.append(result[2])
    dict = {'min':mins,'avg':avgs,'max':maxes}
    return jsonify(dict)

if __name__ == '__main__':
    app.run(debug=True)

'''
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
'''

