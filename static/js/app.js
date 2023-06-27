// Get the Samples endpoint

function init(){

  // this checks that our initial function runs.
  console.log("The Init() function ran")

  // create dropdown/select
  d3.json("/api/v1.0/dropdown").then(i => {
   
    // Get the dropdown/select element
    let dropdownMenu = d3.select("#selDataset")
    .selectAll("option")
    .data(i)
    .enter()
    .append("option")
    .attr("value", d => d)
    .text(d =>  d);
  });

  // run functions to generate plots with default location = "STREET"
  
  createBar('ABANDONED BUILDING')

};

// function that runs whenever the dropdown is changed
// this function is in the HTML and is called with an input called 'this.value'
// that comes from the select element (dropdown)
function optionChanged(newlocation){
  // code that updates graphics
  // one way is to recall each function
  
  createBar(newlocation)
 
};



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
     r: 0,
     t: 0,
     b: 150
   }
    };
    Plotly.newPlot("bar", plotData,layout);
 })
  // checking to see if function is running
  // console.log(`This function generates bar chart of ${id} `)

}





// function called, runs init instructions
// runs only on load and refresh of browser page
init();

// d3.json("/api/v1.0/barcharts").then(data => {  console.log(data)});