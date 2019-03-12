
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify
import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine("sqlite:///hawaii.sqlite",
    connect_args={'check_same_thread':False},
    poolclass=StaticPool)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

class Measurement(Base):
     __tablename__ = 'measurement'

class Station(Base):
     __tablename__ = 'station'

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our connection object
session = Session(engine)

app = Flask(__name__)

# # pre-declare User for the 'user' table
# class Measurement(Base):
#     __tablename__ = 'measurement'

# class Station(Base):
#     __tablename__ = 'station'

# # reflect

# Base.prepare(engine, reflect=True)
# Measurement = Base.classes.measurement
# Station = Base.classes.station








app = Flask(__name__)
@app.route("/")
def home():
    """List all available api routes."""
    return (
        "Available Routes:<br/>" +
        "/api/v1.0/precipitation<br/>"+
        "/api/v1.0/stations<br/>"+
        "/api/v1.0/tobs<br/>"+
        "/api/v1.0/<start><br/>"+
        "/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   measurement_data_1 = engine.execute("SELECT date, prcp FROM measurement WHERE date > '2016-08-22'")
   target_measurement = measurement_data_1.fetchall()
   measurement_dict = dict(target_measurement)
   
   return jsonify(measurement_dict)

@app.route("/api/v1.0/stations")
def station():
   station_data = engine.execute("SELECT station FROM station")
   target_station = station_data.fetchall()
   station_dict = dict(target_station)
   
   return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
   measurement_data_1 = engine.execute("SELECT date, tobs FROM measurement WHERE date > '2016-08-22'")
   target_measurement = measurement_data_1.fetchall()
   measurement_dict = dict(target_measurement)
   
   return jsonify(measurement_dict)


@app.route("/api/v1.0/<start>")
def start(start):
    measurement_data_1 = engine.execute("SELECT tobs FROM measurement WHERE date > %s"%start)
    target_measurement = measurement_data_1.fetchall()
    summary_measurement = {'Max': np.max(target_measurement), 'Min': np.min(target_measurement), 'Mean': np.mean(target_measurement)}
    return jsonify(summary_measurement)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    measurement_data_1 = engine.execute(f'SELECT tobs FROM measurement WHERE date BETWEEN {start} AND {end}')
    target_measurement = measurement_data_1.fetchall()
    summary_measurement = {'Max': np.max(target_measurement), 'Min': np.min(target_measurement), 'Mean': np.mean(target_measurement)}
    return jsonify(summary_measurement)



if __name__ == "__main__":
    app.run(debug=True)


    