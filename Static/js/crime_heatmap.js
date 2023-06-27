let heatLayer; // Declare a variable to store the heatmap layer

function init() {
  // This checks that our initial function runs.
  console.log("The Init() function ran");

  // Create dropdown/select
  d3.json("/api/v1.0/crime_heatmap_dropdown")
    .then(i => {
      // Get the dropdown/select element
      let dropdownMenu = d3.select("#selDataset")
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

  // loads arson heatmap
  heatmap("ARSON");
}

// Function that runs whenever the dropdown is changed
function optionChanged(newlocation) {
  console.log("Change", newlocation);
  heatmap(newlocation);
}

// Call the init() function to start the initialization process
init();

let myMap = L.map("map", {
  center: [41.8781, -87.6298], // Set center to Chicago's coordinates
  zoom: 12,
});

// Adding the tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
}).addTo(myMap);

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

// No changes in the getLocationCoordinates() function
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
