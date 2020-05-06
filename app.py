# Set Up the Flask Weather App

# -- Importing dependencies
import datetime as dt
import numpy as np
import pandas as pd

# -- Importing SQLAlchemy dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# -- Import Flask dependencies
from flask import Flask, jsonify

# -- Access SQLite Database 
engine = create_engine("sqlite:///hawaii.sqlite")

# -- Reflect database into classes
Base = automap_base()

# -- Reflect database 
Base.prepare(engine, reflect=True) 

# -- Create a variable for each class for later reference 
Measurement = Base.classes.measurement
Station = Base.classes.station

# -- Session link from Python to database 
session = Session(engine)

# Set Up Flask

# -- Create Flask application 
app = Flask(__name__)

# -- Define welcome route
@app.route("/")

# -- Function with Return statement 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# -- New route: Precipitation
@app.route("/api/v1.0/precipitation")

# -- Precipitation function 
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
   # -- Jsonify to format results into a JSON structured file
    return jsonify(precip)

# -- New route: Stations
@app.route("/api/v1.0/stations")

# -- Stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# -- New route: Temperature Observations
@app.route("/api/v1.0/tobs")

# -- Temp. Observations Function 
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# -- New route: Statistics
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# -- Statistics Function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

