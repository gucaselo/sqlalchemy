import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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

app = Flask(__name__)


@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    weather_info = []
    for date, prcp in prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        weather_info.append(precipitation_dict)

    return jsonify(weather_info)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()

    stations_info = []
    for station in stations:
        stations_info.append(station)
    
    return jsonify(stations_info)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()
    session.close()
    
    tobs_info = []
    for date, tobs in tobs_year:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_info.append(tobs_dict)

    return jsonify(tobs_info)

###################################
###################################

session = Session(engine)
start_dt = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
start_dt = start_dt[0].replace("-", "")
end_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
end_dt = end_dt[0].replace("-", "")

####

@app.route("/api/v1.0/", defaults={"start":None, "end":None})
@app.route("/api/v1.0/<start>/", defaults={"end":None})
@app.route("/api/v1.0/<start>/<end>/")
def temperatures2(start, end):
    
    session = Session(engine)

    if start == None and end == None:
        start = start_dt
        end = end_dt
    
    if start != None and end == None:
        end = end_dt
        try:
            start_date = datetime.strptime(start, '%Y%m%d')
            end_date = datetime.strptime(end, '%Y%m%d')
        except:
            return (f"This is the incorrect date format. It should be YYYYMMDD<br/>")
    
    if start != None and end != None:
        try:
            start_date = datetime.strptime(start, '%Y%m%d')
            end_date = datetime.strptime(end, '%Y%m%d')
        except:
            return (f"This is the incorrect date format. It should be YYYYMMDD<br/>")
        
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).all()
    session.close()

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