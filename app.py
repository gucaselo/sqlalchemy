# Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt
from datetime import datetime
from flask import Flask, jsonify



# create engine to hawaii.sqlite
database_path = 'Resources/hawaii.sqlite'
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Replace start_date and end_date for dates in YYYYMMDD format:</br>"
        f"/api/v1.0/start_date</br>"
        f"/api/v1.0/start_date/end_date</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to obtain Precipitation information
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Add data obtained into a list
    weather_info = []
    for date, prcp in prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        weather_info.append(precipitation_dict)

    return jsonify(weather_info)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to obtain Stations information
    stations = session.query(Station.station).all()
    session.close()

    # Add data obtained into a list
    stations_info = []
    for station in stations:
        stations_info.append(station)
    return jsonify(stations_info)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session=Session(engine)

    # Query to obtain Temperatures information and most recent date
    active_station = session.query(Measurement.station).order_by(desc(func.count(Measurement.station))).group_by(Measurement.station).first()
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.station == active_station[0]).order_by(Measurement.date.desc()).all()
    session.close()
    
    # Add data obtained into a list
    tobs_info = []
    for date, tobs in tobs_year:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_info.append(tobs_dict)
    return jsonify(tobs_info)

#-----------------------------------------------------#
#     Query most recent and oldest date in dataset    #
#-----------------------------------------------------#
# Create our session (link) from Python to the DB
session = Session(engine)
start_dt = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
start_dt = start_dt[0].replace("-", "")
end_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
end_dt = end_dt[0].replace("-", "")
session.close()

# Multiple routes depending on user input for start and/or end date. 
@app.route("/api/v1.0/", defaults={"start":None, "end":None})
@app.route("/api/v1.0/<start>/", defaults={"end":None})
@app.route("/api/v1.0/<start>/<end>/")
def temperatures2(start, end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # If no dates are entered
    if start == None and end == None:
        start = start_dt
        end = end_dt
    
    # If only start date is entered
    if start != None and end == None:
        end = end_dt
        try:
            start_date = datetime.strptime(start, '%Y%m%d')
            end_date = datetime.strptime(end, '%Y%m%d')
        except:
            return (f"This is the incorrect date format. It should be YYYYMMDD<br/>")
    
    # If both start and end date are entered
    if start != None and end != None:
        try:
            start_date = datetime.strptime(start, '%Y%m%d')
            end_date = datetime.strptime(end, '%Y%m%d')
        except:
            return (f"This is the incorrect date format. It should be YYYYMMDD<br/>")

    # Query to obtain Temperatures information in a specified date range
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).all()
    session.close()

    # Add data obtained into a list 
    temp_info = []
    for tmin, tavg, tmax in temp_results:
        temp_dict = {}
        temp_dict['tmin'] = tmin
        temp_dict['tavg'] = tavg
        temp_dict['tmax'] = tmax
        temp_info.append(temp_dict)

    return jsonify(temp_info)



if __name__ == '__main__':
    app.run(debug=True)