// Initialize Leaflet map with Chicago's coordinates
var map = L.map('map').setView([41.8781, -87.6298], 10);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

// Read CSV file using D3
//d3.csv(' ') add file here
    .then(function (data) {
        // Create empty heatmap layer
        var heatmapLayer = L.heatLayer([], { radius: 20 }).addTo(map);

        // Populate heatmap layer with data
        data.forEach(function (row) {
            var lat = parseFloat(row.Latitude);
            var lng = parseFloat(row.Longitude);
            if (!isNaN(lat) && !isNaN(lng)) {
                heatmapLayer.addLatLng([lat, lng]);
            }
        });
    });