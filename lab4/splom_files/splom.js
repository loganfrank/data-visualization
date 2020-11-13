
d3.csv("iris.csv", function(error, flowers) {  // read the flowwer data and run the function when reading is done 

	var size = 140,                 // the size of each scatterplot is 140x140 
		width = 960,                  // the width of entire drawing area 
		n = 4,
	    padding = 10;               // pading between the scatterplots 

	var x = d3.scaleLinear()        // a scale function to map the point value (var1, var2) to the x range
	    .range([padding / 2, size - padding / 2]);

	var y = d3.scaleLinear()        // a scale function to map the point value (var1, var2) to the y range
	    .range([size - padding / 2, padding / 2]);

	var xAxis = d3.axisBottom()     // D3 axis with tickmarks on the right 
	    .scale(x)                   // using the x scale function defined above as the scale of the axis 
	    .ticks(5)
	    .tickSize(size * n);

	var yAxis = d3.axisRight()      // D3 matrix with tickmarks at the bottom 
	    .scale(y)                   // using the y scale function defined above as the scale of the axis 
	    .ticks(5)
	    .tickSize(size * n);

  xAxis.tickSize(size * n);
  yAxis.tickSize(size * n);

  var domainByTrait = {},  // store the min/max of each trait from the data 
      traits = ["sepal length", "sepal width", "petal length", "petal width"], // a list of traint 
      n = traits.length;

  traits.forEach(function(trait) {  // loop through each traint 
    domainByTrait[trait] = d3.extent(flowers, function(d) { return d[trait]; }); // find the [min,max] of each trait, d is each row of the flower data 
  });

  var brush = d3.brush()
      .on("start", brushstart)
      .on("brush", brush)
      .on("end", brushend)
      .extent([[0,0],[size, size]]);

  var svg = d3.select("body").append("svg")  // create a svg drawing area 
      .attr("width", 1280)
      .attr("height", 800)
    .append("g")                            // append a svg group 
    .attr("transform", "translate(359.5,69.5)");

  // Legend.
  var legend = svg.selectAll("g.legend")    // display species legend at the bottom 
      .data(["setosa", "versicolor", "virginica"])
    .enter().append("svg:g")                // append a svg group as a containeer 
      .attr("class", "legend")              // use css style for "legend"
      .attr("transform", function(d, i) { return "translate(0," + (i * 20 + 600) + ")"; });

  legend.append("svg:circle")               // for every species, append a circle to draw 
      .attr("class", String)                // use the species name as the class name, and look up style sheet in html for the appearance 
      .attr("r", 3);

  legend.append("svg:text")                 // now display the name of the species 
      .attr("x", 12)
      .attr("dy", ".31em")
      .text(function(d) { return "Iris " + d; });  // d is the data bound above 

  // X-axis.    
  svg.selectAll(".x.axis")                // append a X axis to svg 
      .data(traits)                       // the data to bind is the trait array 
    .enter().append("g")
      .attr("class", "x axis")
      .attr("transform", function(d, i) { return "translate(" + (n - i - 1) * size + ",0)"; })
      .each(function(d) { x.domain(domainByTrait[d]); d3.select(this).call(xAxis); });  //define the x position scale function for each trait 

  // Y-axis.
  svg.selectAll(".y.axis")                // append a Y axis to svg 
      .data(traits)                       // the data to bind is the trait array 
    .enter().append("g")
      .attr("class", "y axis")
      .attr("transform", function(d, i) { 
      	return "translate(0," + i * size + ")"; 
      })
      .each(function(d) { y.domain(domainByTrait[d]); d3.select(this).call(yAxis); }); //define the y position scale function for each trait 

  var cell = svg.selectAll(".cell")  // create a scatterplot matrix, where a cell is a scatterplot 
      .data(cross(traits, traits))  // create a traits x traits list 
    .enter().append("g")
      .attr("class", "cell")        // will use cell css style 
      .attr("transform", function(d) {    // specify the translations needed for each plot 
      	return "translate(" + d.i * size + "," + d.j * size + ")"; 
      })
      .each(plot);  // call the plot function to draw the scatter plots, one for each traits X traits pair 

  // add title for the diagonal entries
  cell.filter(function(d) {       // now filter the traits x traits selection and only take trait== trait pair 
  	return d.i === d.j; })
  	  .append("text")             // add display the trait name in the cell 
      .attr("x", padding)
      .attr("y", padding)
      .attr("dy", ".71em")
      .text(function(d) { return d.x; });

  cell.call(brush);

  function plot(p) {              // this is where you draw a scatterplot based on the traits X traits combination 
    var cell = d3.select(this);   // this is the element passed to the function 

    x.domain(domainByTrait[p.x]);  // the range of first trait; now you complete the definition of x scale 
    y.domain(domainByTrait[p.y]);  // the range of second trait now you complete the definition of y scale 

    // Plot frame.
    cell.append("rect")           // plot the base (frame) of the scatterplot 
        .attr("class", "frame")   // set the class as 'frame' so thaat you can look up the stye from html
        .attr("x", padding / 2)   // upper right corner of the rectangle, note this is relative to the corner of each cell 
        .attr("y", padding / 2)
        .attr("width", size - padding)
        .attr("height", size - padding);

    // Plot dots.
    cell.selectAll("circle")      // now lets draw one circle for each row of the flower data, based on the specific trait pair 
        .data(flowers)
      .enter().append("circle")
      .attr("class", function(d) { return d.species; })
        .attr("cx", function(d) { return x(d[p.x]); })  // x is a scale funcion, map value to x coordinate, d is a row, p.x is a trait 
        .attr("cy", function(d) { return y(d[p.y]); })  // y is a scale funcion, map value to y coordinate, d is a row, p.y is a trait 
        .attr("r", 3);
  }

  var brushCell;
 
  function brushstart(p) {
    if (brushCell !== this) {
      d3.select(brushCell).call(brush.move, null); // clear brush
      brushCell = this;
    x.domain(domainByTrait[p.x]);
    y.domain(domainByTrait[p.y]);
    }
  }

  // Highlight the selected circles.
  function brush(p) {

  }
 
  function brushend() { 
    
  }
});

function cross(a, b) {
  var c = [], n = a.length, m = b.length, i, j;
  for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
  return c;
}