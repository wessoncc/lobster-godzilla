var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 60,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var xScale = d3.scaleLinear().domain([300, 1000]).range([0, width])
var yScale = d3.scaleLinear().domain([10, 85]).range([height, 0])

var bottomAxis = d3.axisBottom(xScale);
var leftAxis = d3.axisLeft(yScale);

d3.csv("assets/data/data.csv").then(function(CensusData) {
    console.log(CensusData)
    CensusData.forEach(function(data) {
        data.poverty = +data.poverty;
        data.obesity = +data.obesity;
        console.log(data.poverty)
        console.log(data.obesity)
    });
});