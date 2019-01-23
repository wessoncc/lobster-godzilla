function buildMetadata(selData) {
  d3.json(`/metadata/${selData}`).then(function(response) {

    var sampleData = d3.select("#sample-metadata");

    sampleData.html("");

    Object.entries(response).forEach(function([key, value]){
      sampleData.append("h6").text(`${key}: ${value}`);
    });
  }); 
}
function buildCharts(selData) {
  d3.json(`/samples/${selData}`).then(function(response){
    const otu_ids = response.otu_ids;
    const otu_labels = response.otu_labels;
    const sample_values = response.sample_values;

    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "OTU ID" }
    };
    var bubbleData = [
      {
        x: otu_ids,
        y: sample_values,
        text: otu_labels,
        mode: "markers",
        marker: {
          size: sample_values,
          color: otu_ids,
          colorscale: "Earth"
        }
      }
    ];
    Plotly.plot("bubble", bubbleData, bubbleLayout);
    
    var pieData = [
      {
        value: sample_values.slice(0, 10),
        labels: otu_ids.slice(0, 10),
        hovertext: otu_labels.slice(0, 10),
        hoverinfo: "hovertext",
        type: "pie"
      }
    ];

    var pieLayout = {
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", pieData, pieLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();