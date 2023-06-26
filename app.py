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

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

