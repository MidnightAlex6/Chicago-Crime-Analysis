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

# main page for dashboard
@app.route("/")
def welcome():
    return render_template("index.html")

# route used for the crime heatmap drop down menu
@app.route("/api/v1.0/crime_heatmap_dropdown")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of
    # Query all crime data data
    # results = session.query(Crimes.ID, Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).all()
    results = session.query(Crimes.PrimaryType).distinct(Crimes.PrimaryType).order_by(Crimes.PrimaryType.asc()).all()
    print(results)
    session.close()
    
    # Convert list of tuples into normal list
    all_crimes = []
    for PrimaryType in results:
        
        all_crimes.append(PrimaryType[0])

    return jsonify(all_crimes)

# route used for the crime heat map data
@app.route("/api/v1.0/chicago_crime_heatmap")
def others():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all crime data
    # results = session.query(Crimes.ID, Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).all()
    results = session.query(Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).order_by(Crimes.PrimaryType.asc())
    print(results)
    session.close()
    # Convert list of tuples into normal list
    all_crimes = []
    for PrimaryType, Latitude, Longitude in results:
        crimes_dict = {}
        #crimes_dict["ID"] = ID
        crimes_dict["PrimaryType"] = PrimaryType
        crimes_dict["Latitude"] = Latitude
        crimes_dict["Longitude"] = Longitude
        all_crimes.append(crimes_dict)
    return jsonify(all_crimes)

# route used for the location description drop down menu
@app.route("/api/v1.0/dropdown")
def names2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query data
    results = session.query(Crimes.LocationDescription).distinct(Crimes.LocationDescription).order_by(Crimes.LocationDescription.asc()).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    all_crimes = []
    for LocationDescription in results:

        all_crimes.append(LocationDescription[0])

    return jsonify(all_crimes)

# route used for the bar chart data
@app.route("/api/v1.0/barcharts")
def others2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all suicides by country"""
    # Query all suicide data
    # results = session.query(Crimes.ID, Crimes.LocationDescription, Crimes.PrimaryType).all()
    results = session.query(Crimes.LocationDescription, Crimes.PrimaryType, func.count(Crimes.PrimaryType)).group_by(Crimes.LocationDescription, Crimes.PrimaryType).order_by(Crimes.LocationDescription.asc(), func.count(Crimes.PrimaryType).desc()).all()
    print(results)
    session.close()
    
    # Convert list of tuples into normal list
    all_crimes = []
    for LocationDescription, PrimaryType, i in results:
        crimes_dict = {}
        crimes_dict["LocationDescription"] = LocationDescription
        crimes_dict["PrimaryType"] = PrimaryType
        crimes_dict["counts"] = i
        all_crimes.append(crimes_dict)

    return jsonify(all_crimes)

# route used for the crime by month heat map drop down menu
@app.route("/api/v1.0/Month_heatmap_dropdown")
def names3():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of
    # Query all crime data data
    # results = session.query(Crimes.ID, Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).all()
    results = session.query(Crimes.Month).distinct(Crimes.Month).order_by(Crimes.Month).all()
    print(results)
    session.close()
    
    # Convert list of tuples into normal list
    all_crimes3 = []
    for Month in results:
        
        all_crimes3.append(Month[0])

    return jsonify(all_crimes3)

# route used for the crime by month data heat map
@app.route("/api/v1.0/chicago_time_heatmap")
def others3():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all crime data
    # results = session.query(Crimes.ID, Crimes.PrimaryType, Crimes.Latitude, Crimes.Longitude).all()
    results = session.query(Crimes.Month, Crimes.Latitude, Crimes.Longitude).order_by(Crimes.Month.asc())
    print(results)
    session.close()
    # Convert list of tuples into normal list
    all_crimes = []
    for Month, Latitude, Longitude in results:
        crimes_dict = {}
        #crimes_dict["ID"] = ID
        crimes_dict["Month"] = Month
        crimes_dict["Latitude"] = Latitude
        crimes_dict["Longitude"] = Longitude
        all_crimes.append(crimes_dict)
    return jsonify(all_crimes)

if __name__ == '__main__':
    app.run(debug=True)