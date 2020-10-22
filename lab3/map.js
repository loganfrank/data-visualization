
function map(state_cases_data, state_cases_data_normalized, state_month_data) {
    d3.json('data/usa_mainland.json', create_map);
}

function create_map(error, us) {
    var svg = d3.select('#map_svg')
        .append('svg')
        .attr('width', '600px')
        .attr('height', '600px');

    console.log(us);
    var width = 600;
    var height = 600;

    var projection = d3.geoEquirectangular()
        .fitExtent([[0,0], [width, height]], us);
    
    var geoGenerator = d3.geoPath()
        .projection(projection);

    var paths = svg.selectAll('path')
        .data(us.features)
        .enter()
        .append('path')
        .attr('d', geoGenerator);

    var texts = svg.selectAll('text')
        .data(us.features)
        .enter()
        .append('text')
        .attr('text-anchor', 'middle')
        .attr('alignment-baseline', 'middle')
        .attr('opacity', 0.5)
        .text(function(d) {
            return d.properties.STUSPS10;
        })
        .attr('transform', function(d) {
            var center = geoGenerator.centroid(d);
            return 'translate (' + center + ')';
        });
}

function highlight_map(state) {

}

function reset_map(state) {

}