//-------------------------------------------------------------------------------------------------------------------------------------------------
// Url for data points
//-------------------------------------------------------------------------------------------------------------------------------------------------
var quakeUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
var faultUrl = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_plates.json";
//-------------------------------------------------------------------------------------------------------------------------------------------------
// Call function to create map
//-------------------------------------------------------------------------------------------------------------------------------------------------
CreateMap(quakeUrl, faultUrl);
//-------------------------------------------------------------------------------------------------------------------------------------------------
// Create map
//-------------------------------------------------------------------------------------------------------------------------------------------------
function CreateMap(quakeUrl, faultUrl) {
  // Get the earthquake data
    d3.json(quakeUrl, function(data) {
    // Stores response into quakeData
    var quakeData = data;
    // Get the faultline
    d3.json(faultUrl, function(data) {
      // Stores response into faultData
      var faultData = data;
      // Passes data into createFeatures function
      createFeatures(quakeData, faultData);
    });
  });
  // Create features
  function createFeatures(quakeData, faultData) {
    // Defines two functions that are run once for each feature in quakeData
    // Creates markers for each earthquake and add descriptive pop-up
    function onEachQuakeLayer(feature, layer) {
      return new L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], {
        fillOpacity: 1,
        color: chooseColor(feature.properties.mag),
        fillColor: chooseColor(feature.properties.mag),
        radius:  markerSize(feature.properties.mag)
      });
    }
    function onEachquake(feature, layer) {
      layer.bindPopup("<h3>" + feature.properties.mag+ " magnitude; " + feature.properties.place + "</h3>"+
      "<hr>"+
      "<p>" + "Lat: " + feature.geometry.coordinates["1"] + ", Long: " + feature.geometry.coordinates["0"]+
        "<p>"+ new Date(feature.properties.time) + "</p>")
    }
    // Creates a GeoJSON layer containing the features array of the earthquakeData object
    // Run the onEachEarthquake & onEachQuakeLayer functions once for each element in the array
    var earthquakes = L.geoJSON(quakeData, {
      onEachFeature: onEachquake,
      pointToLayer: onEachQuakeLayer
    });
    // Creates a GeoJSON layer containing the features array of the faultData object
    var faultLines = L.geoJSON(faultData, {
      onEachFeature: function(feature, layer) {
      layer.setStyle({
        fillOpacity: 0
      });
      layer.on({
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0
          })},
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.2
          })}});
      layer.bindPopup("<h3>" + feature.properties.PlateName + " Plate" + "</h3>");
    }
  });
    // Sends earthquakes and faultLines layers to the createMap function
    createMap(earthquakes, faultLines);
  }
  // Function to create map
  function createMap(earthquakes, faultLines) {
      // Custom Darkmap layer
        var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/wessoncc/cjs89m3fy1k5r1ft6scmmovb2/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
            attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
            maxZoom: 18,
            accessToken: API_KEY
        });
      // Satmap layer
        var satmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
            attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
            maxZoom: 18,
            accessToken: API_KEY
        });
    // Define a baseMaps object to hold base layers
    var baseMaps = {
      "Dark Map": darkmap,
      "Satelite Map": satmap,
    };
    // Create overlay object to hold overlay layers
    var overlayMaps = {
      "Earthquakes": earthquakes,
      "Faultlines": faultLines
    };
    // Create map with default display settings
    var map = L.map("map", {
      center: [39.8283, -98.5785],
      zoom: 3,
      layers: [darkmap, faultLines],
      scrollWheelZoom: false
    });
    // Create a layer control
    // Pass in baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: true
    }).addTo(map);
  }
}
//-------------------------------------------------------------------------------------------------------------------------------------------------
// chooseColor function
// change circle color based on magnitude
//-------------------------------------------------------------------------------------------------------------------------------------------------
function chooseColor(magnitude) {
  return magnitude > 6 ? "red":
    magnitude > 5 ? "orange":
      magnitude > 4 ? "gold":
        magnitude > 3 ? "yellow":
          magnitude > 2 ? "yellowgreen":
            magnitude > 1 ? "greenyellow":
            "green"; // <= 1 default
}
//-------------------------------------------------------------------------------------------------------------------------------------------------
// markerSize function
// Change circle size based on magnitude
//-------------------------------------------------------------------------------------------------------------------------------------------------
function markerSize(magnitude) {
  return magnitude**1.8;
}