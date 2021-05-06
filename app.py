#dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#flask import
from flask import Flask, jsonify

#create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect database 
Base = automap_base()
Base.prepare(engine, reflect=True)
#save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#set up flask
app = Flask(__name__)

#routes
@app.route("/")
def home():
    return (
        f'Welcome to the Hawaii weather API!</br>'
        f'The following routes are available: </br>'
        f'Precipitation Data: /api/v1.0/precipitation</br>'
        f'Station Data: /api/v1.0/stations</br>'
        f'Temperature Observations (TOBS) Data: /api/v1.0/tobs</br>'
        f'Min, Avg, Max Temperature when supplied a start date: /api/v1.0/start_date*</br>'
        f'Min, Avg, Max Temperature when supplied a start and end date: /api/v1.0/start_date/end_date*</br>'
        f'*Supply date as %Y-%m-%d</br>'
    )

@app.route("/api/v1.0/precipitation")
def prep():
    #start session
    session = Session(engine)

    #date and prep data
    measurement_data = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    
    #close session
    session.close()

    #convert list of tuples into normal list
    measurement_data_list = []
    for date, prcp in measurement_data:
        measurement_data_dict = {}
        measurement_data_dict["date"] = date
        measurement_data_dict["precipitation"] = prcp
        measurement_data_list.append(measurement_data_dict)

    return jsonify(measurement_data_list)

@app.route("/api/v1.0/stations")
def stations():
    #start session
    session = Session(engine)

    #date and prep data
    station_data = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    #close session
    session.close()

    #convert list of tuples into normal list
    station_data_list = []
    for id, station, name, latitude, longitude, elevation in station_data:
        station_data_dict = {}
        station_data_dict["id"] = id
        station_data_dict["station"] = station
        station_data_dict["name"] = name
        station_data_dict["latitude"] = latitude
        station_data_dict["longitude"] = longitude
        station_data_dict["elevation"] = elevation
        station_data_list.append(station_data_dict)

    return jsonify(station_data_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #top station found from analysis
    station = "USC00519281"
    #start session
    session = Session(engine)

    #finding latest date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    #pulling date data 
    latest_date_2 = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    latest_year = int(latest_date_2.strftime("%Y"))
    latest_month = int(latest_date_2.strftime("%m"))
    latest_day = int(latest_date_2.strftime("%d"))
    #finding 1 year before latest date
    start_date = dt.date(latest_year, latest_month, latest_day) - dt.timedelta(days=365)

    #date and latest years tobs data
    measurement_data_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).\
        filter(Measurement.station == station).\
        order_by(Measurement.date).all()
    
    #close session
    session.close()

    #convert list of tuples into normal list
    measurement_data_tobs_list = []
    for date, tobs in measurement_data_tobs:
        measurement_data_tobs_dict = {}
        measurement_data_tobs_dict["date"] = date
        measurement_data_tobs_dict["tobs"] = tobs
        measurement_data_tobs_list.append(measurement_data_tobs_dict)

    return jsonify(measurement_data_tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    #start session
    session = Session(engine)

    #finding latest date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    #date and tobs data 
    #TMIN
    TMIN_start = session.query(Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
    #TMAX
    TMAX_start = session.query(Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()

    #TAVG
    TAVG_start = session.query(Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()

    #close session
    session.close()

    #convert data into variables for returning
    #TMIN
    for date, tobs in TMIN_start:
        TMIN_start_date = date
        TMIN_start_tobs = tobs
    
    #TMAX
    for date, tobs in TMAX_start:
        TMAX_start_date = date
        TMAX_start_tobs = tobs
    
    #TAVG
    for date, tobs in TAVG_start:
        TAVG_start_tobs = round(tobs,1)

    return (
        f'The TMIN for {start} to {latest_date} is:</br>'
        f'{TMIN_start_tobs} on {TMIN_start_date}</br>'
        f'-----------------------------------------------------</br>'
        f'The TMAX for {start} to {latest_date} is:</br>'
        f'{TMAX_start_tobs} on {TMAX_start_date}</br>'
        f'-----------------------------------------------------</br>'
        f'The TAVG for {start} to {latest_date} is:</br>'
        f'{TAVG_start_tobs}</br>'
    )

@app.route("/api/v1.0/<start>/<end>")
def both(start,end):
    #start session
    session = Session(engine)

    #date and tobs data 
    #TMIN
    TMIN_both = session.query(Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()
    
    #TMAX
    TMAX_both = session.query(Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()

    #TAVG
    TAVG_both = session.query(Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()

    #close session
    session.close()

    #convert data into variables for returning
    #TMIN
    for date, tobs in TMIN_both:
        TMIN_both_date = date
        TMIN_both_tobs = tobs
    
    #TMAX
    for date, tobs in TMAX_both:
        TMAX_both_date = date
        TMAX_both_tobs = tobs
    
    #TAVG
    for date, tobs in TAVG_both:
        TAVG_both_tobs = round(tobs,1)

    return (
        f'The TMIN for {start} to {end} is:</br>'
        f'{TMIN_both_tobs} on {TMIN_both_date}</br>'
        f'-----------------------------------------------------</br>'
        f'The TMAX for {start} to {end} is:</br>'
        f'{TMAX_both_tobs} on {TMAX_both_date}</br>'
        f'-----------------------------------------------------</br>'
        f'The TAVG for {start} to {end} is:</br>'
        f'{TAVG_both_tobs}</br>'
    )

#end
if __name__ == "__main__":
    app.run(debug=True)