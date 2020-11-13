var margin = {top: 80, right: 0, bottom: 10, left: 80},
    width = 720,
    height = 720;

var x = d3.scaleBand().range([0, width]),   // create D3 scale functions 
    z = d3.scaleLinear().domain([0, 4]).clamp(true),
    c = d3.scaleOrdinal(d3.schemeCategory10)
          .domain(d3.range(10));

var svg = d3.select("body").append("svg")  // create a svg drawable with width/height/margins info 
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");  // transform the whole drawable by margins 

d3.json("miserables.json", function(miserables) {   // read the json file. You shold take a look at the josn file so that 
                                                    //  you know how nodes/links/group are defined
                                                    //  Make sure you remember all lines up to the end is in the handler 

  var matrix = [],                                  //  matrix will be used to place the nodes/links info from json, empty here 
      nodes = miserables.nodes,                     //  nodes store all the nodes, and n is the length   
      n = nodes.length;

  // Compute index per node.
  nodes.forEach(function(node, i) {                 // now let's walk through each node using javascript's forEach() feature 
    node.index = i;                                 // the node index is defined by the order that a node is listed in the json 
    node.count = 0;                                 //  how many time the node has appear in the show? 0 for now and updated later. 
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; }); // create a list that represents a row in the matrix 
  });

  // Convert links to matrix; count the character occurrences.
  miserables.links.forEach(function(link) {         //now let's add the co-occurence count of node(character) i and j to matrix[i][j].z 
    matrix[link.source][link.target].z += link.value;   // remember esch link is read from json that shows the co-currence of source and target 
    matrix[link.target][link.source].z += link.value;   // where source and target are two characters in the play 
    matrix[link.source][link.source].z += link.value;
    matrix[link.target][link.target].z += link.value;
    nodes[link.source].count += link.value;             // also update each node's appearance count 
    nodes[link.target].count += link.value;
  });

  // orderByName is D3 scale function which is to map from a character name to an integer indicating the order of characters (nodes) in the matrix rows/columns 
  // now let's define the range first. i.e., the final position of character 
  // ***** this is what you should modify for you lab!! 
  var orderByName = d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); })  
                                                 
  x.domain(orderByName);   // now define the scale domain, that is the character name
                           // so with domain and range defined, you can assign the row/column index by the name 

  svg.append("rect")       // now let's append a big svg rectangle as the base of the whole matrix 
      .attr("class", "background")   // check style.css to see what the backgruond style (color) is 
      .attr("width", width)          // the entire svg drawable width 
      .attr("height", height);       // the entire svg drawable width 

  var row = svg.selectAll(".row") // now let's process the matrix data and ready to draw the matrix elements as squares
      .data(matrix)               // bind the data first 
    .enter().append("g")          // every row of squares is a group (g) in svg 
      .attr("class", "row")       // assign each row a class id 'row' 
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })  // for each row translate downwards based on the row's index 
      .each(row);                 //  for each row, call the plot function 'row' 

  //row.append("line")              
  //    .attr("x2", width);

  
  row.append("text")              //display characters along the rows
      .attr("x", -6)
      .attr("y", x.bandwidth() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return nodes[i].name; });


  var column = svg.selectAll(".column")   // create a svg group to display the character names along the colomn (horizontal)
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });  // move to the correct horizontal pos and rotate the text by 90 degrees

  //column.append("line")
  //    .attr("x1", -width);

  column.append("text")   // display the character names 
      .attr("x", 6)
      .attr("y", x.bandwidth() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return nodes[i].name; });

  

  function row(row) {  // now draw those little color squares in the matrix row 
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z>0; }))  // make a new selection that only returns elements that have non zero count 
        .enter().append("rect")    
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })  // put the rect at the horizontal location returns by x() 
        .attr("width", x.bandwidth()) 
        .attr("height", x.bandwidth())
        .style("fill-opacity", function(d) { return z(d.z); })
        .style("fill", function(d) { return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null; });
  }

  function mouseover() {

  }

  function mouseout() {
 
  }

});