let heatLayer; // Declare a variable to store the heatmap layer

// create dropdown/select menu containing primary type of crime heat map
function init() {
  // This checks that our initial function runs.
  console.log("The Init() function ran");
  // Create dropdown/select
  d3.json("/api/v1.0/crime_heatmap_dropdown")
    .then(i => {
      // Get the dropdown/select element
      let dropdownMenu = d3.select("#selDataset1")
        .selectAll("option")
        .data(i)
        .enter()
        .append("option")
        .attr("value", d => d)
        .text(d => d);
    })
    .catch(error => {
      console.error("Error retrieving dropdown data:", error);
    });

  // create dropdown/select menu containing location description for bar chart
  d3.json("/api/v1.0/dropdown").then(i => {
    // Get the dropdown/select element
    let dropdownMenu2 = d3.select("#selDataset2")
    .selectAll("option")
    .data(i)
    .enter()
    .append("option")
    .attr("value", d => d)
    .text(d =>  d);
  });

  // run functions to generate plots with default location = "STREET"
  createBar('ABANDONED BUILDING');
  // loads arson heatmap
  heatmap("ARSON");

  // Create dropdown/select menu containing months for heat map by months
  d3.json("/api/v1.0/Month_heatmap_dropdown")
    .then(i => {
      // Get the dropdown/select element
      let dropdownMenu = d3.select("#selDataset3")
        .selectAll("option")
        .data(i)
        .enter()
        .append("option")
        .attr("value", d => d)
        .text(d => d);
    })  
    .catch(error => {
      console.error("Error retrieving dropdown data:", error);
    });
  heatmap2("JANUARY");
}

// Function that runs whenever the dropdown is changed for first heatmap
function optionChanged1(newlocation) {
  console.log("Change", newlocation);
  heatmap(newlocation);
}

// function that runs whenever the dropdown is changed for bar chart
// this function is in the HTML and is called with an input called 'this.value'
// that comes from the select element (dropdown)
function optionChanged2(newlocation2){
  // code that updates graphics
  // one way is to recall each function
  createBar(newlocation2)
};

  // Function that runs whenever the dropdown is changed for heatmap by months
function optionChanged3(newlocation) {
  console.log("Change", newlocation);
  heatmap2(newlocation);
};

// Call the init() function to start the initialization process for heat map
init();
let myMap = L.map("map", {
  center: [41.8781, -87.6298], // Set center to Chicago's coordinates
  zoom: 12,
});

// Adding the tile layer for first heat map
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
}).addTo(myMap);

// Call the init() function to start the initialization process for heat map by months
let myMap2 = L.map("map2", {
  center: [41.8781, -87.6298], // Set center to Chicago's coordinates
  zoom: 12,
});

// Adding the tile layer for second heat map
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
}).addTo(myMap2);

// pulls lat and lon into array for first heat map
function heatmap(crime) {
  d3.json("/api/v1.0/chicago_crime_heatmap")
    .then(function (data) {
      let crimedata = data.filter(i => i.PrimaryType === crime);
      console.log(crimedata);
      let heatArray = [];
      crimedata.forEach(function (row) {
        let lat = row.Latitude;
        let lng = row.Longitude;
        if (!isNaN(lat) && !isNaN(lng)) {
          heatArray.push([lat, lng]);
        }
      });
      if (heatLayer) {
        // If a heatmap layer already exists, remove it from the map
        myMap.removeLayer(heatLayer);
      }
      heatLayer = L.heatLayer(heatArray, {
        radius: 20,
        blur: 20,
      }).addTo(myMap);
    })
    .catch(error => {
      console.error("Error retrieving crime data:", error);
    });
}

// No changes in the getLocationCoordinates() function for first heat map
function getLocationCoordinates(locationString) {
  let regex = /\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)/;
  let match = regex.exec(locationString);
  if (match && match.length === 3) {
    let lat = parseFloat(match[1]);
    let lng = parseFloat(match[2]);
    if (!isNaN(lat) && !isNaN(lng)) {
      return [lat, lng];
    }
  }
  return null;
}

// pulls data from flask route to create bar chart
function createBar(location){
  // code that makes bar chart at id='bar'
    d3.json("/api/v1.0/barcharts").then(data => {
    console.log(data)
    // let test = d3.select("#selDataset").property("value")
    let sampleData = data.filter(data => data.LocationDescription === location);
    let labels = sampleData.map(data => data.PrimaryType)
    let values = sampleData.map(data => data.counts)
    let labels10 = labels.slice(0, 10);
    let values10 = values.slice(0, 10);
    let trace = {
     x: labels10,
     y: values10,
     type: 'bar',
    //  text: otu_labels,
     orientation: 'v'
   };
    let plotData = [trace];
    let layout ={margin: {
     l: 100,
     r: 150,
     t: 0,
     b: 150
   }
    };
    Plotly.newPlot("bar", plotData,layout);
 })
  // checking to see if function is running
  // console.log(`This function generates bar chart of ${id} `)
}

// pulls lat and lon into array for second heat map
function heatmap2(crime) {
  d3.json("/api/v1.0/chicago_time_heatmap")
    .then(function (data) {
      let monthdata = data.filter(i => i.Month === crime);
      console.log(monthdata);
      let heatArray = [];

      monthdata.forEach(function (row) {
        let lat = row.Latitude;
        let lng = row.Longitude;
        if (!isNaN(lat) && !isNaN(lng)) {
          heatArray.push([lat, lng]);
        }
      });

      if (heatLayer) {
        // If a heatmap layer already exists, remove it from the map
        myMap2.removeLayer(heatLayer);
      }

      heatLayer = L.heatLayer(heatArray, {
        radius: 20,
        blur: 20,
      }).addTo(myMap2);
    })
    .catch(error => {
      console.error("Error retrieving crime data:", error);
    });
}

// No changes in the getLocationCoordinates() function for second heat map
function getLocationCoordinates(locationString) {
  let regex = /\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)/;
  let match = regex.exec(locationString);
  if (match && match.length === 3) {
    let lat = parseFloat(match[1]);
    let lng = parseFloat(match[2]);
    if (!isNaN(lat) && !isNaN(lng)) {
      return [lat, lng];
    }
  }
  return null;
}