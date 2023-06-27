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

if __name__ == '__main__':
    app.run(debug=True)