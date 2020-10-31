// created with help from: https://www.tutorialsteacher.com/d3js/create-bar-chart-using-d3js

function bar(state_cases_data, state_cases_data_normalized, state_month_data) {
    var state_data = state_month_data['Ohio'];

    // remove 0 cases months
    var i = 0;
    while (i < state_data.length) {
        var entry = state_data[i];
        var cases = entry['cases'];
        if (cases === 0) {
            state_data.splice(i, 1);
        } else {
            i++;
        }
    }

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select('#bar_svg')
        .append('svg')
        .attr('width', 550)
        .attr('height', 500);
    var margin = 200;
    var width = svg.attr('width') - margin;
    var height = svg.attr('height') - margin;

    var x = d3.scaleBand().range([0, width]).padding(0.4);
    var y = d3.scaleLinear().range([height, 0]);

    var g = svg.append('g').attr('transform', 'translate(' + margin / 2 + ',' +  margin / 2 + ')');

    x.domain(state_data.map(function(d) {
        return d['month'];
    }));
    y.domain([0, d3.max(state_data, function(d) {
        return d['cases'];
    })]);

    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', function(d) {
            return 'translate(' + ((d.length * 3)) + ',' + ((d.length * 2) + 5) + ')' + 'rotate(55)'
        });
    
    g.append('g')
        .call(d3.axisLeft(y).tickFormat(function(d) {
            return d;
        }).ticks(10));

    // construct the bars in the bar chart
    g.selectAll('#bar')
        .data(state_data)
        .enter()
        .append('rect')
        .attr('id', 'bar')
        .attr('x', function(d) {
            return x(d['month']);
        })
        .attr('y', function(d) {
            return y(d['cases']);
        })
        .attr('width', x.bandwidth())
        .attr('height', function(d) {
            return height - y(d['cases'])
        })
        .attr('fill', function(d, i) {
            return color(i);
        });

    // add title
    svg.append('text')
        .attr('transform', 'translate(100, 0)')
        .attr('x', 50)
        .attr('y', 50)
        .attr('font-size', '18px')
        .text('Ohio Monthly Cases');
    
    // add x axis label
    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .append('text')
        .attr('x', width - 150)
        .attr('y', height - 230)
        .attr('text-anchor', 'end')
        .text('Month');

    // add y axis label
    g.append('g')
        .append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -75)
        .attr('y', -60)
        .attr('text-anchor', 'end')
        .text('Number of Cases');

    // put text above the bars
    g.append('g')
        .selectAll('#top_text')
        .data(state_data)
        .enter()
        .append('text')
        .attr('id', 'top_text')
        .attr('font-size', '10px')
        .attr('x', function(d) {
            return x(d['month']);
        })
        .attr('y', function(d) {
            return y(d['cases']) - 5;
        })
        .text(function(d) {
            return d['cases'];
        });
    
}

function update_bar(state, state_month_data) {
    d3.select('#bar_svg').select('svg').remove();

    var state_data = state_month_data[state];

    // remove 0 cases months
    var i = 0;
    while (i < state_data.length) {
        var entry = state_data[i];
        var cases = entry['cases'];
        if (cases === 0) {
            state_data.splice(i, 1);
        } else {
            i++;
        }
    }

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select('#bar_svg')
        .append('svg')
        .attr('width', 550)
        .attr('height', 500);
    var margin = 200;
    var width = svg.attr('width') - margin;
    var height = svg.attr('height') - margin;

    var x = d3.scaleBand().range([0, width]).padding(0.4);
    var y = d3.scaleLinear().range([height, 0]);

    var g = svg.append('g').attr('transform', 'translate(' + margin / 2 + ',' +  margin / 2 + ')');

    x.domain(state_data.map(function(d) {
        return d['month'];
    }));
    y.domain([0, d3.max(state_data, function(d) {
        return d['cases'];
    })]);

    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', function(d) {
            return 'translate(' + ((d.length * 3)) + ',' + ((d.length * 2) + 5) + ')' + 'rotate(55)'
        });
    
    g.append('g')
        .call(d3.axisLeft(y).tickFormat(function(d) {
            return d;
        }).ticks(10));

    g.selectAll('#bar')
        .data(state_data)
        .enter()
        .append('rect')
        .attr('id', 'bar')
        .attr('x', function(d) {
            return x(d['month']);
        })
        .attr('y', function(d) {
            return y(d['cases']);
        })
        .attr('width', x.bandwidth())
        .attr('height', function(d) {
            return height - y(d['cases'])
        })
        .attr('fill', function(d, i) {
            return color(i);
        });

    svg.append('text')
        .attr('transform', 'translate(100, 0)')
        .attr('x', 50)
        .attr('y', 50)
        .attr('font-size', '18px')
        .text(state + ' Monthly Cases');
    
    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .append('text')
        .attr('x', width - 150)
        .attr('y', height - 230)
        .attr('text-anchor', 'end')
        .text('Month');

    g.append('g')
        .append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -75)
        .attr('y', -60)
        .attr('text-anchor', 'end')
        .text('Number of Cases');

        g.append('g')
        .selectAll('#top_text')
        .data(state_data)
        .enter()
        .append('text')
        .attr('id', 'top_text')
        .attr('font-size', '10px')
        .attr('x', function(d) {
            return x(d['month']);
        })
        .attr('y', function(d) {
            return y(d['cases']) - 5;
        })
        .text(function(d) {
            return d['cases'];
        });
}