![Banner](https://github.com/MidnightAlex6/Chicago-Crime-Analysis/assets/126301312/e3234d94-55db-4905-8a0c-0479cf623ff6)

# Chicago Crime Analysis

## Background

The City of Chicago has a historical reputation for violent crime. Our group was fascinated by this topic and we proposed a more in-depth exploration of different types of crimes that happen across the city. We plan to make an interactive dashboard using crime data provided from the [Chicago Data Portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2) of crimes in 2023 to analyze and see what insights can be drawn from them. Our dashboard will include a heat map of all the crimes that happened in Chicago with an interactive drop down to filter through specific types of primary crimes that have occurred throughout the city. A bar chart of top 10 primary types of crime with an interactive drop down menu allowing users to filter through different location descriptions. A heat map of total crimes in Chicago with an interactive drop down that will allow users to filter through the months. To tackle this issue effectively, we leveraged a wide array of powerful tools and technologies including SQL, Flask, Python, HTML/CSS, and JavaScript, [D3](https://d3js.org/), [Leaflet](https://leafletjs.com/), [Bootstrap](https://getbootstrap.com/), and [Plotly](https://plotly.com/). Through our collaborative efforts, we aim to uncover valuable insights that can aid in understanding the underlying dynamics of crime in Chicago.

## Collaborators

- [Alex Valerio](https://github.com/MidnightAlex6) 
- [Zunyan Guo](https://github.com/ZunyanGuo)
- [Cara Boldarini](https://github.com/careah)
- [Lisa Maccio Maretto](https://github.com/lmacciomaretto)
- [Sanja Kesic](https://github.com/SanjaKesic)

## File Structure

- Python Folder
- Data Folder
  - Crimes_2023.csv - original file of data
  - Crimes_2023db.db - database for the project
- retrieving_data.ipynb - file that contains the data cleaning process
- Resources Folder
  - Banner.jpeg - image for the readme file
  - Crimes in Chicago Presentation - slide deck for the presentation
- Static Folder
  - css Folder
    - style.css - styling for heat maps
  - data Folder
    - Crimes_2023db.db - database for the project to connect to the Flask API
  - js Folder
    - crime_heatmap.js
    - leaflet-heat.js - Leaflet plugin for creating heat maps
- Templates Folder
  - index.html - HTML file that sets up the structure and layout of our webpage
- App.py - file for our Flask API and all the different routes used

## Screenshots of Dashboard

![Heatmap_by_type_of_crime](https://github.com/MidnightAlex6/Chicago-Crime-Analysis/assets/126301312/4bef7e29-7d1e-4841-a41f-e9e9be035dd2)

![Barchart_by_location](https://github.com/MidnightAlex6/Chicago-Crime-Analysis/assets/126301312/4815442b-a98c-4a92-8b09-8810857b49d7)

![Heatmap_by_months](https://github.com/MidnightAlex6/Chicago-Crime-Analysis/assets/126301312/cc95d42e-eafd-4007-b57e-015bfc41675c)

## Instructions

### Database Creation

- Downloaded the crime data from the City of Chicago's website as a CSV file.

- Imported the CSV file into a Jupyter Notebook for data cleaning and manipulation.

- Performed data cleaning tasks such as deleting irrelevant columns, separating the date and time information, and creating a new column to indicate the month of each crime.

- Exported the cleaned dataset as a new CSV file.

- Imported the CSV file into DB Browser for SQL.

- Created a new database named "Crimes_2023db" in DB Browser for SQL.

- Added an ID column to the database as a primary key.

### Flask API

- Import the necessary libraries: numpy, json, sqlalchemy, and flask.

- Set up the database connection using SQLAlchemy to an SQLite database.

- Reflect the existing database into a new model and prepare the engine.

- Define the Flask application.

- Set up the main route ("/") to render the index.html template.

- Define a route ("/api/v1.0/crime_heatmap_dropdown") to retrieve a list of distinct crime types from the database.

- Define a route ("/api/v1.0/chicago_crime_heatmap") to retrieve crime data including primary type, latitude, and longitude from the database.

- Define a route ("/api/v1.0/dropdown") to retrieve a list of distinct location descriptions from the database.

- Define a route ("/api/v1.0/barcharts") to retrieve data for bar charts, including location description, primary type, and count, from the database.

- Define a route ("/api/v1.0/Month_heatmap_dropdown") to retrieve a list of distinct months from the database.

- Define a route ("/api/v1.0/chicago_time_heatmap") to retrieve crime data including month, latitude, and longitude from the database.

- Run the Flask application if the script is executed directly.

### App Initialization

- Declare a variable heatLayer to store the heatmap layer.

- Define the init() function to initialize the application.

- Inside the init() function:

- Make a GET request to /api/v1.0/crime_heatmap_dropdown to retrieve the list of primary crime types for the dropdown menu.
Create a dropdown/select menu with the retrieved data.
Make a GET request to /api/v1.0/dropdown to retrieve the list of location descriptions for the bar chart dropdown menu.

- Create a dropdown/select menu with the retrieved data.

- Call the createBar() function with the default location set to "ABANDONED BUILDING" to generate the bar chart.

- Call the heatmap() function with the default crime set to "ARSON" to load the arson heatmap.

- Make a GET request to /api/v1.0/Month_heatmap_dropdown to retrieve the list of months for the heat map by months dropdown menu.

- Create a dropdown/select menu with the retrieved data.

- Call the heatmap2() function with the default month set to "JANUARY" to load the corresponding heat map.

- Define the optionChanged1(newlocation) function, which is triggered when the dropdown for the first heatmap is changed. It calls the heatmap() function with the selected crime type.

- Define the optionChanged2(newlocation2) function, which is triggered when the dropdown for the bar chart is changed. It calls the createBar() function with the selected location description.

- Define the optionChanged3(newlocation) function, which is triggered when the dropdown for the heat map by months is changed. It calls the heatmap2() function with the selected month.

- Call the init() function to start the initialization process for the first heatmap.

- Create a Leaflet map with the ID "map" and set the center to Chicago's coordinates.

- Add a tile layer to the map using the OpenStreetMap tile provider.

- Call the init() function to start the initialization process for the heat map by months.

- Create another Leaflet map with the ID "map2" and set the center to Chicago's coordinates.

- Add a tile layer to the second map using the OpenStreetMap tile provider.

- Define the heatmap(crime) function to pull latitude and longitude data from the /api/v1.0/chicago_crime_heatmap route based on the selected crime type. It creates a heatmap layer using the retrieved data and adds it to the first map.

- Define the getLocationCoordinates(locationString) function to extract latitude and longitude from a location string.

- Define the createBar(location) function to pull data from the /api/v1.0/barcharts route based on the selected location description. It generates a bar chart using the retrieved data and displays it at the HTML element with the ID "bar".

- Define the heatmap2(crime) function to pull latitude and longitude data from the /api/v1.0/chicago_time_heatmap route based on the selected month. It creates a heatmap layer using the retrieved data and adds it to the second map.

- Define the getLocationCoordinates(locationString) function to extract latitude and longitude from a location string.

### HTML

- The HTML code sets up a web page for a Crime In Chicago Dashboard.

- The required CSS and JavaScript dependencies (Bootstrap, Leaflet, D3, and Plotly) are included via external links.

- The page structure consists of a container with rows and columns for different sections.

- The "jumbotron" section displays the title and description of the dashboard.

- The "Primary Type Of Crime" section includes a dropdown menu (select element) with id "selDataset1" to select the primary type of crime. It has an onchange event listener to trigger the "optionChanged1" function when the selection changes.

- The "map" section is a placeholder div with id "map" where the Leaflet map will be rendered.

- The "Crime Locations" section includes a dropdown menu (select element) with id "selDataset2" to select crime locations. It has an onchange event listener to trigger the "optionChanged2" function when the selection changes.

- The "bar" section is a placeholder div with id "bar" where the Plotly bar chart will be rendered.

- The "Crimes by Month" section includes a dropdown menu (select element) with id "selDataset3" to select months. It has an onchange event listener to trigger the "optionChanged3" function when the selection changes.

- The "map2" section is a placeholder div with id "map2" where the second Leaflet map will be rendered.

- The JavaScript files are included at the end, with "crime_heatmap.js" containing the code to handle the interactive functionality of the dashboard, such as populating dropdowns, handling dropdown changes, and rendering the maps and charts.

### CSS Styling 

- Set the padding and margin of the body element to 0 pixels.

- Set the height of the #map, body, and html elements to 500 pixels.

- Set the height of the #map2, body, and html elements to 500 pixels.







