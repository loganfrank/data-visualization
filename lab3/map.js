
function map(state_cases_data, state_cases_data_normalized, state_month_data) {
    d3.json('data/usa_mainland.json', create_map);
}

function create_map(error, us) {
    var svg = d3.select('#map_svg')
        .append('svg')
        .attr('width', '600px')
        .attr('height', '600px');

    var width = 600;
    var height = 600;

    var projection = d3.geoEquirectangular()
        .fitExtent([[0,0], [width, height]], us);
    
    var geoGenerator = d3.geoPath()
        .projection(projection);

    console.log(us);

    var paths = svg.selectAll('path')
        .data(us.features)
        .enter()
        .append('path')
        .attr('d', geoGenerator)
        .attr('id', function(d) {
            return d.properties.NAME10.split(' ').join('_');
        })
        .on('mouseover', function(d) {
            var state = d.properties.NAME10;
            highlight_table_and_pack(state);
            // select circle and fill
            d3.select(this)
                .style('fill', 'orange');
        })
        .on('mouseout', function(d) {
            var state = d.properties.NAME10;    
            reset_table_and_pack(state);
            // select circle and reset
            d3.select(this)
                .style('fill', '#ddd');
        });

    var texts = svg.selectAll('text')
        .data(us.features)
        .enter()
        .append('text')
        .attr('text-anchor', 'middle')
        .attr('alignment-baseline', 'middle')
        .attr('opacity', 0.5)
        .attr('font-size', '8px')
        .text(function(d) {
            return d.properties.STUSPS10;
        })
        .attr('transform', function(d) {
            var center = geoGenerator.centroid(d);
            return 'translate (' + center + ')';
        });

    // draw circles over states
    var circles = svg.selectAll('circle')
        .data(us.features)
        .enter()
        .append('circle')
        .attr('transform', function(d) {
            var center = geoGenerator.centroid(d);
            return 'translate (' + center + ')';
        })
        .attr('r', function(d) {
            var state = d.properties.NAME10;
            var normalized_cases = state_cases_data_normalized[state];
            var multiplier = 250;
            normalized_cases = normalized_cases * multiplier;
            return normalized_cases;
        })
        .attr('id', function(d) {
            return d.properties.NAME10.split(' ').join('_');
        })
        .style('fill', '#006622')
        .style('opacity', '25%')
        .on('mouseover', function(d) {
            var state = d.properties.NAME10;
            highlight_table_and_pack(state);
            // select path and fill
            d3.select(this)
                .style('fill', 'orange');
        })
        .on('mouseout', function(d) {
            var state = d.properties.NAME10;    
            reset_table_and_pack(state);
            // select path and reset
            d3.select(this)
                .style('fill', '#006622');
        });
}

function highlight_table_and_pack(state) {
    highlight_table(state);
    highlight_pack(state);
}

function highlight_map(state) {
    state = state.split(' ').join('_');
    d3.select('path#' + state).style('fill', 'orange');
}

function reset_table_and_pack(state) {
    reset_table(state);
    reset_pack(state);
}

function reset_map(state) {
    state = state.split(' ').join('_');
    d3.select('path#' + state).style('fill', '#ddd');
}