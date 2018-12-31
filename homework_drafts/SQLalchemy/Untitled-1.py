
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify


    


# reflect an existing database into a new model
Base = automap_base()

# pre-declare User for the 'user' table
class Measurement(Base):
    __tablename__ = 'measurement'

class Station(Base):
    __tablename__ = 'station'

# reflect
engine = create_engine("sqlite:///hawaii.sqlite")
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station








# app = Flask(__name__)
# @app.route("/")
# def home():
#     print("testing flask for the first time")
#     return "It Worked!"

# @app.route("/api/v1.0/precipitation")
# def precipitation():
#    measurement_data_1 = engine.execute("SELECT date, prcp FROM measurement WHERE date > '2016-08-22'")
#    target_measurement = measurement_data_1.fetchall()
#    measurement_dict = dict(target_measurement)
   
#    return jsonify(measurement_dict)




if __name__ == "__main__":
    app.run(debug=True)