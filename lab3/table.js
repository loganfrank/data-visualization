function table(state_cases_data, state_cases_data_normalized, state_month_data) {
    var table = d3.select('#table_svg').append('table');
    var header = table.append('thead').append('tr');
    header.selectAll('th')
        .data(['State', 'Total Cases'])
        .enter()
        .append('th')
        .text(function(d) { return d; });

    var table_body = table.append('tbody');
    rows = table_body.selectAll('tr')
        .data(state_cases_data)
        .enter()
        .append('tr')
        .attr('original-color', function() {
            var original_color = $(this).css('background-color');
            return rgb_to_hex(original_color);
        })
        .on('mouseover', function(d) {
            var state = d[0];
            highlight(state);
            d3.select(this)
                .style('background-color', 'orange');
        })
        .on('mouseout', function(d) {
            var state = d[0];
            reset(state);
            d3.select(this)
                .style('background-color', function() {
                    return d3.select(this).attr('original-color');
                });
        })
        .on('click', function(d) {
            var state = d[0];
            update(state);
        });
    cells = rows.selectAll('td')
        .data(function(d) {
            return d;
        })
        .enter()
        .append('td')
        .text(function(d) {
            return d;
        });
}

// got this function from https://stackoverflow.com/questions/5999209/how-to-get-the-background-color-code-of-an-element-in-hex
function rgb_to_hex(colorval) {
    var parts = colorval.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    delete(parts[0]);
    for (var i = 1; i < 4; i++) {
        parts[i] = parseInt(parts[i]).toString(16);
        if (parts[i].length == 1) parts[i] = '0' + parts[i];
    }
    return '#' + parts.join('');
}

function highlight(state) {
    highlight_map(state);
    highlight_pack(state);
}

function reset(state) {
    reset_map(state);
    reset_pack(state);
}

function update(state) {
    update_bar(state);
    update_pie(state);
}