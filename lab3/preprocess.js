// load data and call function to parse
d3.csv('./data/filtered-data.csv', load_data)

function load_data(error, dataset) {
    //console.log(dataset)

    // parse state normalized totals into a new dict
    state_to_cases = {};
    state_cases_data = [];
    state_cases_data_normalized = {};
    for(var i = 0; i < dataset.length; i++) {
        var state = dataset[i]['state'];
        var total = parseInt(dataset[i]['total cases']);
        var normalized_total = parseFloat(dataset[i]['normalized total cases']);
        if (!(state in state_to_cases)) {
            state_to_cases[state] = total;
            state_cases_data_normalized[state] = normalized_total;
        }
    }
    for(const [key, value] of Object.entries(state_to_cases)) {
        state_cases_data.push([key, value])
    }

    var month_int_to_string = {
        '1'  : 'January',
        '2'  : 'February',
        '3'  : 'March',
        '4'  : 'April',
        '5'  : 'May',
        '6'  : 'June',
        '7'  : 'July',
        '8'  : 'August',
        '9'  : 'September',
        '10' : 'October'
    };

    // parse the state month data into a new dict
    state_month_data = {};
    for(var i = 0; i < dataset.length; i++) {
        var state = dataset[i]['state'];
        var month = dataset[i]['date'];
        var cases = parseInt(dataset[i]['monthly cases']);

        if (!(state in state_month_data)) {
            state_month_data[state] = [];
        }
        state_month_data[state].push({'month' : month_int_to_string[month], 'cases' : cases});
    }

    // log the datasets
    console.log(state_cases_data);
    console.log(state_cases_data_normalized);
    console.log(state_month_data)

    // call functions to create the views
    table(state_cases_data, state_cases_data_normalized, state_month_data);
    map(state_cases_data, state_cases_data_normalized, state_month_data);
    pack(state_cases_data, state_cases_data_normalized, state_month_data);
    pie(state_cases_data, state_cases_data_normalized, state_month_data);
    bar(state_cases_data, state_cases_data_normalized, state_month_data);
    
}
