function bar(state_cases_data, state_cases_data_normalized, state_month_data) {
    var margin = {top: 10, right:20, bottom:135, left:40};
    var width = 680 - margin.left - margin.right;
    var height = 460 - margin.top - margin.bottom;

    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.065);
    var y = d3.scaleLinear()
        .range([0, height]);

    bar_svg = d3.select('#bar_svg')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    //x.domain(state_month_data.map(function(d) {
    //    console.log(d);
    //}));
    //y.domain([0, 100]);

    //var x_axis = d3.axisBottom().scale(x);
    //var y_axis = d3.axisLeft().scale(y);
}

function update_bar(state) {
    
}