function pack(state_cases_data, state_cases_data_normalized, state_month_data) {
    var hierarchical_data = {'children' : []};
    for (const item of state_cases_data) {
        hierarchical_data['children'].push({'state' : item[0], 'total cases' : item[1]});
    }
    
    console.log(hierarchical_data);

    var diameter = 500;

    var bubble = d3.pack(hierarchical_data)
        .size([diameter, diameter])
        .padding(1.5);
    
    pack_svg = d3.select('#pack_svg')
        .append('svg')
        .attr('width', diameter + 200)
        .attr('height', diameter)
        .attr('class', 'bubble');

    d3.select('#pack_svg')
        .append('text')
        .attr('id', 'cases_text')
        .text('No State Selected')
        .style('fill', 'black');

    var nodes = d3.hierarchy(hierarchical_data)
        .sum(function(d) {
            return d['total cases'];
        });

    var node = pack_svg.selectAll('.node')
        .data(bubble(nodes).descendants())
        .enter()
        .filter(function(d) {
            return !d.children;
        })
        .append('g')
        .attr('class', 'node')
        .attr('transform', function(d) {
            return 'translate (' + d.x + ',' + d.y + ')';
        });

    node.append('title')
        .text(function(d) {
            console.log(d);
            return d.data['state'] + ': ' + d.data['total cases'];
        });

    node.append('circle')
        .attr('r', function(d) {
            return d.r;
        })
        .style('fill', '#006622')
        .attr('id', function(d) {
            return d.data['state'].split(' ').join('_');
        })
        .attr('cases', function(d) {
            return d.data['total cases'];
        })
        .on('click', function(d) {
            // TODO
            console.log(d);
            console.log('click pack circle');
        })
        .on('mouseover', function(d) {
            var state = d.data['state'];
            highlight_map_and_table(state);
            d3.select(this)
                .style('fill', 'orange');
            d3.select('#cases_text')
                .text('Total Cases: ' + d.data['total cases']);
        })
        .on('mouseout', function(d) {
            var state = d.data['state'];   
            reset_map_and_table(state);
            d3.select(this)
                .style('fill', '#006622');
            d3.select('#cases_text')
                .text('No State Selected');
        });

    node.append('text')
        .attr('dy', '.2em')
        .style('text-anchor', 'middle')
        .text(function(d) {
            return d.data['state'];
        })
        .attr('font-size', function(d) {
            return d.r / 4;
        })
        .attr('fill', 'white')
        .on('click', function(d) {
            // TODO
            console.log(d);
            console.log('click pack text')
        })
        .on('mouseover', function(d) {
            var state = d.data['state']
            highlight_map_and_table(state);
            state = state.split(' ').join('_');
            d3.select('#pack_svg')
                .select('circle#' + state)
                .style('fill', 'orange');
            d3.select('#cases_text')
                .text('Total Cases: ' + d.data['total cases']);
        })
        .on('mouseout', function(d) {
            var state = d.data['state']
            reset_map_and_table(state);
            state = state.split(' ').join('_');
            d3.select('#pack_svg')
                .select('circle#' + state)
                .style('fill', '#006622');
            d3.select('#cases_text')
                .text('No State Selected');
        });
    
    d3.select(self.frameElement)
        .style('height', diameter + 'px');
}

function highlight_map_and_table(state) {
    highlight_map(state);
    highlight_table(state);
}

function highlight_pack(state) {
    state = state.split(' ').join('_');
    d3.select('#pack_svg')
        .select('circle#' + state)
        .style('fill', 'orange');
    d3.select('#pack_svg')
        .select('#cases_text')
        .text(function() {
            return  'Total Cases: ' + d3.select('#pack_svg')
                .select('circle#' + state)
                .attr('cases');
        });
}

function reset_map_and_table(state) {
    reset_map(state);
    reset_table(state);
}

function reset_pack(state) {
    state = state.split(' ').join('_');
    d3.select('#pack_svg')
        .select('circle#' + state)
        .style('fill', '#006622');
    d3.select('#pack_svg')
        .select('#cases_text')
        .text('No State Selected');
}

