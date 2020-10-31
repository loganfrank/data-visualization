function pie(state_cases_data, state_cases_data_normalized, state_month_data) {
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

    d3.select('#pie_svg')
        .append('text')
        .attr('id', 'state_text')
        .text('Ohio')
        .style('fill', 'black');
    
    d3.select('#pie_svg').append('br');

    pie_svg = d3.select('#pie_svg')
        .append('svg')
        .attr('width', 1000)
        .attr('height', 800)
        .append('g');

    var pieGenerator = d3.pie()
        .value(function(d) { 
            return d['cases'];
        })
        .sort(function(a, b) {
            return b['cases'] - a['cases'];
        });

    var arcData = pieGenerator(state_data);

    var arcGenerator = d3.arc()
        .innerRadius(50)
        .outerRadius(120);

    // construct the pie
    d3.select('#pie_svg')
        .select('svg')
        .select('g')
        .selectAll('path')
        .data(arcData)
        .enter()
        .append('path')
        .attr('fill', function(d, i) {
            return color(i);
        })
        .attr('d', arcGenerator);
        
    // add text over the pie chart sections
    d3.select('#pie_svg')
        .select('svg')
        .select('g')
        .selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .each(function(d) {
            var centroid = arcGenerator.centroid(d);
            d3.select(this)
                .text(d.data['cases'])
                .attr('font-size', '10px');
            d3.select(this).attr('x', centroid[0] - d3.select(this).text().length * 2.5)
                .attr('y', centroid[1])
                .attr('dy', '0.33em');
        });

    d3.select('#pie_svg')
        .select('g')
        .attr('transform', 'translate(150, 150)');

    // create the legend
    var legend = d3.select('#pie_svg')
        .select('svg')
        .selectAll('#legend')
        .data(pieGenerator(state_data))
        .enter()
        .append('g')
        .attr('transform', function(d, i) {
            return 'translate(280,' + (200 + (i * 20 + 20)) + ')';
        })
        .attr('id', 'legend');
    legend.append('rect')
        .attr('width', 10)
        .attr('height', 10)
        .attr('fill', function(d, i) {
            return color(i);
        });
    legend.append('text')
        .text(function(d) {
            return d.data['month'];
        })
        .style('font-size', 12)
        .attr('x', 15)
        .attr('y', 9);
}

function update_pie(state, state_month_data) {
    d3.select('#pie_svg').select('svg').remove();
    d3.select('#pie_svg').select('#state_text').remove();
    d3.select('#pie_svg').select('br').remove();

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

    d3.select('#pie_svg')
        .append('text')
        .attr('id', 'state_text')
        .text(state)
        .style('fill', 'black');
    
    d3.select('#pie_svg').append('br');

    pie_svg = d3.select('#pie_svg')
        .append('svg')
        .attr('width', 1000)
        .attr('height', 800)
        .append('g');

    var pieGenerator = d3.pie()
        .value(function(d) { 
            return d['cases'];
        })
        .sort(function(a, b) {
            return b['cases'] - a['cases'];
        });

    var arcData = pieGenerator(state_data);

    var arcGenerator = d3.arc()
        .innerRadius(50)
        .outerRadius(120);

    d3.select('#pie_svg')
        .select('svg')
        .select('g')
        .selectAll('path')
        .data(arcData)
        .enter()
        .append('path')
        .attr('fill', function(d, i) {
            return color(i);
        })
        .attr('d', arcGenerator);
        
    d3.select('#pie_svg')
        .select('svg')
        .select('g')
        .selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .each(function(d) {
            var centroid = arcGenerator.centroid(d);
            d3.select(this)
                .text(d.data['cases'])
                .attr('font-size', '10px');
            d3.select(this).attr('x', centroid[0] - d3.select(this).text().length * 2.5)
                .attr('y', centroid[1])
                .attr('dy', '0.33em');
        });

    d3.select('#pie_svg')
        .select('g')
        .attr('transform', 'translate(150, 150)');

    // create the legend
    // used: https://stackoverflow.com/questions/32298837/how-to-add-a-nice-legend-to-a-d3-pie-chart
    var legend = d3.select('#pie_svg')
        .select('svg')
        .selectAll('#legend')
        .data(pieGenerator(state_data))
        .enter()
        .append('g')
        .attr('transform', function(d, i) {
            return 'translate(280,' + (200 + (i * 20 + 20)) + ')';
        })
        .attr('id', 'legend');
    
    legend.append('rect')
        .attr('width', 10)
        .attr('height', 10)
        .attr('fill', function(d, i) {
            return color(i);
        });
    
    legend.append('text')
        .text(function(d) {
            return d.data['month'];
        })
        .style('font-size', 12)
        .attr('x', 15)
        .attr('y', 9);
}