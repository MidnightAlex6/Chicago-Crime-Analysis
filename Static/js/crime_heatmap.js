let myMap = L.map("map", {
    center: [41.8781, -87.6298], // Set center to Chicago's coordinates
    zoom: 7
  });
  
  // Adding the tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
  }).addTo(myMap);
  
  let jsonUrl = "./static/data/Clear_Crimes_2023.json";
  
  d3.json(jsonUrl).then(function(data) {
  
    let heatArray = [];
  
    data.forEach(function(row) {
      let locationString = row.Location;
      let coordinates = getLocationCoordinates(locationString);
      if (coordinates) {
        heatArray.push(coordinates);
      }
    });
  
    let heat = L.heatLayer(heatArray, {
      radius: 20,
      blur: 35
    }).addTo(myMap);
  
  });
  
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
  
