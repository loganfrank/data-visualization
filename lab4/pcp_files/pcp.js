var species = ["setosa", "versicolor", "virginica"],
    traits = ["sepal length", "petal length", "sepal width", "petal width"];

var m = [80, 160, 200, 160],  //margin: [top, right, buttom, left]
    w = 1280 - m[1] - m[3],   //remaining svg width for drawing 
    h = 800 - m[0] - m[2];    //remaining svg height for drawing 

var x = d3.scalePoint().domain(traits).range([0, w]),  // convert four traits to four axis position 
    y = {};

var line = d3.line(),     
    axis = d3.axisLeft(x),foreground;

var svg = d3.select("body").append("svg:svg")   // create a svg 
    .attr("width", w + m[1] + m[3])
    .attr("height", h + m[0] + m[2])
  .append("svg:g")                              // append a group under svg 
    .attr("transform", "translate(" + m[3] + "," + m[0] + ")");  // translte by [left,top) to not drawn on the margin

var colorMap = ["red", "green", "blue"];

function colorBySpecies(d){
  var index = species.indexOf(d.species);
  return colorMap[index];
}

d3.csv("iris.csv", function(flowers) {   // after read flowers.csv, do the following - note that this is a big block that goes all the way to the end

  traits.forEach(function(d) {   // below until line 41 we are looping through each trait (d) 
    flowers.forEach(function(p) { p[d] = +p[d]; });  // forEach is to run on every data item by the provided function
                                                     // here d is every trait of the flower data, p is every row of flower table
                                                     // why do you add a '+'? convert a string to a number so that you can do math on 

    y[d] = d3.scaleLinear()     //just a scaling function to convert from the traint value to screen height linearly 
        .domain(d3.extent(flowers, function(p) { return p[d]; }))  // extend is to calculate the range of the values in each trait, h is the screen height
        .range([h, 0]);

    y[d].brush = d3.brushY()           // define a brush event 
        .extent([[-8, 16], [8, h]])    //define the brushable area: width wise only near each coordinate axis is brushable 
        .on("brush", brush)            // but you can brush across almost the entire screen height
        .on('end', brushEnd);          // I added this (Logan Frank)       
 });

  // Add foreground lines.
  foreground = svg.append("svg:g")     // now lets define the polylines (svg paths)  to be drawn undeer svg
      .attr("class", "foreground")     // give a html class name "foreground", initially all lines are viible 
    .selectAll("path")                 // append "empth path stud"
      .data(flowers)                   // read the data 
    .enter().append("svg:path")        // append a path for every element (row) from the data  
      .attr("d", path)                 // now provide the path info to svg. Where is path defined? 
      .style("stroke", function(d){    // color the polylines by their flower species 
        return colorBySpecies(d);
      });

  // Add a group element for each trait.
  var g = svg.selectAll(".trait")     //create a svg group for each trait 
      .data(traits)                   // read the traits array defined above 
    .enter().append("svg:g")          // enter a group g for each traits 
      .attr("class", "trait")         // define the class name 
      .attr("transform", function(d) { return "translate(" + x(d) + ")"; });  //translate each group by a horizontal amount for axes 
                                                    // what is x? the horizontal position calculatd by the scaling function defined above 

  // Add an axis and title.
  g.append("svg:g")                   // add a group under svg for veerical axes 
      .attr("class", "axis")  
      .each(function(d) { d3.select(this).call(axis.scale(y[d])); }); // for each vertical trait axis, CALL the D3 axis function to create one. 
    
  g.append("svg:text")                 // add the name of trait to each axis 
      .attr("text-anchor", "middle")
      .attr("y", -9)
      .text(String); 

  // Add a brush for each axis.
  g.append("svg:g")
      .attr("class", "brush")
      .each(function(d) { 
        d3.select(this).call(y[d].brush); });  // add a D3 brush
});

// Returns the path for a given data point.
function path(d) {
  return line(traits.map(function(p) { 
    return [x(p), y[p](d[p])]; 
  }));
}

// Dictionary to save extents of each dimension
var selections = {};

// The below function is used for if the user clicks the axis (i.e., reseting the brush), it should restore some paths
function brushEnd(p) {
  if (d3.event.selection === null) {
    // delete the extents
    delete selections[p];

    // Restore other paths
    var paths = d3.select('.foreground').selectAll('path')
    paths.classed('fade', function(d) {
      var outside = false;
      for (const[key, value] of Object.entries(selections)){
        outside = outside || (y[key](d[key]) < value[0] || y[key](d[key]) > value[1]);
      }
      return outside;
    });
  }
}

// Handles a brush event, toggling the display of foreground lines.
function brush(p) {
  var s = d3.event.selection;
  selections[p] = s;

  // Select all of the foreground paths
  var paths = d3.select('.foreground').selectAll('path')

  // Determine which paths are outside the provided extents
  paths.classed('fade', function(d) {
    var outside = false;
    for (const[key, value] of Object.entries(selections)){
      outside = outside || (y[key](d[key]) < value[0] || y[key](d[key]) > value[1]);
    }
    return outside;
  });

}