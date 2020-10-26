function pie(state_cases_data, state_cases_data_normalized, state_month_data) {
    var state_data = state_month_data['Ohio'];

    console.log(state_data);

    // remove 0 cases months
    var i = 0;
    while (i < state_data.length) {
        var entry = state_data[i];
        var month = entry['month'];
        var cases = entry['cases'];
        if (cases === 0) {
            state_data.splice(i, 1);
        } else {
            i++;
        }
    }
    console.log(state_data)

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    pie_svg = d3.select('#pie_svg')
        .append('svg')
        .attr('width', 1000)
        .attr('height', 800)
        .append('g');

    var pieGenerator = d3.pie()
        .value(function(d) { 
            console.log(d);
            return d['cases'];
        })
        .sort(function(a, b) {
            console.log(a);
            console.log(b);
            return a['month'].localeCompare(b['month']);
        });

    var arcData = pieGenerator(state_data);

    var arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(100);

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
        

    console.log(arcData);

    d3.select('#pie_svg')
        .select('svg')
        .select('g')
        .selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .each(function(d) {
            console.log(d);
            var centroid = arcGenerator.centroid(d);
            console.log(centroid);
            d3.select(this)
                .attr('x', centroid[0])
                .attr('y', centroid[1])
                .attr('dy', '0.33em')
                .text(d.data['month'])
                .attr('font-size', '9px');
        });

    d3.select('#pie_svg')
        .select('g')
        .attr('transform', 'translate(150, 200)');
    
}

function update_pie(state) {
    
}