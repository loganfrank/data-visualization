function table(state_to_cases, state_month_data) {
    var table = d3.select('#table_svg').append('table');
    var header = table.append('thread').append('tr');
    header.selectAll('th')
        .data(['State', 'Total Cases'])
        .enter()
        .append('th')
        .text(function(d) { return d; });
}

function update_table() {

}

function update_map() {

}

function update_bar() {

}

function update_pack() {

}