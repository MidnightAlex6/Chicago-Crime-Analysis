# import necessary libraries
# from models import create_classes

import numpy as np
import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///crimes_2023db.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///crimes_2023db.db"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# "old" API for heatmap with dropdown box

@app.route("/")
def welcome():
    return render_template("index.html")

# Fetch distinct values from the "primary type" column
primary_types = db.session.query(crimes_2023db.db.primary_types).distinct().all()
primary_types = [result[0] for result in primary_types]
    # Retrieve all rows and aggregate "primary type" for the heatmap
results = db.session.query(crimes_2023db.db.Latitude, crimes_2023db.db.Longitude, crimes_2023db.db.PrimaryType).all()
print(results)
    # Prepare the data for the heatmap
heat_data = {}
for result in results:
    lat = result[0]
    lon = result[1]
    primary_type = result[2]
    if primary_type not in heat_data:
        heat_data[primary_type] = []
        heat_data[primary_type].append((lat, lon))


import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)
DATABASE = 'crimes_2023db.db'

def query_database(query):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
# updated API route for heatmap with dropdown box

@app.route('/api/primary_types', methods=['GET'])
def get_primary_types():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Fetch primary types, counts, latitude, and longitude
    query = "SELECT PrimaryType, COUNT(*) as Count, Latitude, Longitude FROM Clear_Crimes_2023 GROUP BY PrimaryType"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Extract primary types, counts, latitude, and longitude from the results
    primary_types = [row[0] for row in results]
    counts = [row[1] for row in results]
    latitudes = [row[2] for row in results]
    longitudes = [row[3] for row in results]
    
    # Create a list of dictionaries with primary types, counts, latitude, and longitude
    data = [
        {"PrimaryType": ptype, "Count": count, "Latitude": lat, "Longitude": lon}
        for ptype, count, lat, lon in zip(primary_types, counts, latitudes, longitudes)
    ]
    
    conn.close()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run()
@app.route("/api/data")
def get_data():
    # Fetch distinct values from the "Primary Type" column
    query = "SELECT DISTINCT [Primary Type] FROM crimes"
    primary_types = query_database(query)
    primary_types = [result[0] for result in primary_types]

    # Fetch data for heatmap aggregation
    query = "SELECT Latitude, Longitude, [Primary Type] FROM crimes"
    results = query_database(query)

    # Prepare the data for the heatmap
    heat_data = {}
    for result in results:
        lat = result[0]
        lon = result[1]
        primary_type = result[2]

        if primary_type not in heat_data:
            heat_data[primary_type] = []

        heat_data[primary_type].append((lat, lon))

    # Prepare the data for the dropdown box
    dropdown_data = {
        "primary_types": primary_types
    }

    # Prepare the final data to be returned as JSON
    heat_data = {
        "dropdown": dropdown_data,
        "heatmap": heat_data
    }

    return jsonify(heat_data)

# extract month and add month data to API - we just need to change the name of API

@app.route('/api/primary_types', methods=['GET'])
def get_primary_types():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Fetch primary types, counts, latitude, longitude, and date
    query = "SELECT PrimaryType, COUNT(*) as Count, Latitude, Longitude, `Date(mm/dd/aaaa)` FROM Clear_Crimes_2023 GROUP BY PrimaryType"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Extract primary types, counts, latitude, longitude, and month from the results
    primary_types = [row[0] for row in results]
    counts = [row[1] for row in results]
    latitudes = [row[2] for row in results]
    longitudes = [row[3] for row in results]
    dates = [row[4] for row in results]
    
    # Extract the month from the date column
    months = [date.split('/')[0] for date in dates]
    
    # Create a list of dictionaries with primary types, counts, latitude, longitude, and month
    data = [
        {"PrimaryType": ptype, "Count": count, "Latitude": lat, "Longitude": lon, "Month": month}
        for ptype, count, lat, lon, month in zip(primary_types, counts, latitudes, longitudes, months)
    ]
    
    conn.close()
    
    return jsonify(data)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

