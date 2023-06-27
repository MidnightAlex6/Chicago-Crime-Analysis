import numpy as np
import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///static/data/crimes_2023db.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Crimes = Base.classes.Clear_Crimes_2023

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/api/v1.0/dropdown1")
def dropdown1():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all crime location descriptions
    results = session.query(Crimes.LocationDescription).distinct(Crimes.LocationDescription).order_by(Crimes.LocationDescription.asc()).all()
    session.close()
    
    # Convert list of tuples into normal list
    locationdesc_list = []
    for LocationDescription in results:
        
        locationdesc_list.append(LocationDescription[0])

    return jsonify(locationdesc_list)

@app.route("/api/v1.0/barcharts")
def barcharts():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all suicides by country"""
    results = session.query(Crimes.ID,Crimes.LocationDescription, Crimes.PrimaryType, func.count(Crimes.PrimaryType)).group_by(Crimes.LocationDescription, Crimes.PrimaryType).order_by(Crimes.LocationDescription.asc(), func.count(Crimes.PrimaryType).desc()).all()
    print(results)
    session.close()
    # Convert list of tuples into normal list
    all_crimes = []
    for ID, LocationDescription, PrimaryType, i in results:
        crimes_dict = {}
        crimes_dict["ID"] = ID
        crimes_dict["LocationDescription"] = LocationDescription
        crimes_dict["PrimaryType"] = PrimaryType
        crimes_dict["i"] = i
        all_crimes.append(crimes_dict)
        # all_crimes.append(i[0])
    return jsonify(all_crimes)


@app.route("/api/v1.0/dropdown2")
def dropdown2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all crime location descriptions
    results = session.query(Crimes.PrimaryType).distinct(Crimes.PrimaryType).order_by(Crimes.PrimaryType.asc()).all()
    print(results)
    session.close()
    
    # Convert list of tuples into normal list
    primarytype_list = []
    for PrimaryType in results:
        
        primarytype_list.append(PrimaryType[0])

    return jsonify(primarytype_list)

@app.route("/api/v1.0/heatmap1")
def heatmap1():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Retrieve all rows and aggregate "primary type" for the heatmap
    results = session.query(Crimes.ID, Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).all()
    # Prepare the data for the heatmap
    heat_data = []
    for PrimaryType, Latitude, Longitude in results:
        heatdata_dict = {}
        heatdata_dict["Primary Type"] = PrimaryType
        heatdata_dict["Latitude"] = Latitude
        heatdata_dict["Longitude"] = Longitude
        
        heat_data.append(heatdata_dict)

    return jsonify(heat_data)

@app.route("/api/v1.0/dropdown3")
def dropdown3():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all crime locations with month column
    results = session.query(Crimes.Month).distinct(Crimes.Month).all()
    print(results)
    session.close()
    
    # Convert list of tuples into normal list
    month_list = []
    for Date in results:
        
        month_list.append(Date[0])

    return jsonify(month_list)

@app.route("/api/v1.0/heatmap2")
def heatmap2():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Retrieve all rows and aggregate "primary type" for the heatmap
    results = session.query(Crimes.Latitude, Crimes.Longitude, Crimes.Month).all()
    # Prepare the data for the heatmap
    heat_data = []
    for Latitude, Longitude, Month in results:
        heatdata_dict = {}
        heatdata_dict["Latitude"] = Latitude
        heatdata_dict["Longitude"] = Longitude
        heatdata_dict["Month"] = Month
        
        heat_data.append(heatdata_dict)

    return jsonify(heat_data)

if __name__ == '__main__':
    app.run(debug=True)
