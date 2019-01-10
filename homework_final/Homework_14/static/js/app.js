// from data.js
var tableData = data;

// YOUR CODE HERE!
var tbody = d3.select("tbody");

var filter = d3.select("#filter-btn");

filter.on("click", function() {
  d3.event.preventDefault();
  var inputElement = d3.select("#datetime");
  var inputValue = inputElement.property("value");
  console.log(inputValue);
  console.log(tableData);
  var filteredData = tableData.filter(data => data.datetime === inputValue);
  console.log(filteredData)

  filteredData.forEach(function(ufoReport) {
    console.log(ufoReport);
    var row = tbody.append("tr");
    
    Object.entries(ufoReport).forEach(function([key, value]){
        console.log(key, value);
        var cell = tbody.append("td");
        cell.text(value);
      });
  });
});  