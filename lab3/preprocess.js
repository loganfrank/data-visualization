// load data and call function to parse
d3.csv('./data/filtered-data.csv', load_data)

function load_data(error, dataset) {
    // parse state normalized totals into a new dict
    // also parse the state month data into a new dict
    state_to_cases = {};
    state_month_data = {};
    for(var i = 0; i < dataset.length; i++) {
        // normalized totals
        var state = dataset[i]['state'];
        var total = parseFloat(dataset[i]['normalized total cases']);
        if (!(state in state_to_cases)) {
            state_to_cases[state] = total;
        }

        // month data
        var month = dataset[i]['date'];
        var cases = parseInt(dataset[i]['monthly cases']);
        if (!(state in state_month_data)) {
            state_month_data[state] = {};
        }
        state_month_data[state][month] = cases;
    }

    // log the datasets
    console.log(state_to_cases);
    console.log(state_month_data);

    // call functions to create the views
    table(state_to_cases, state_month_data);
    map(state_to_cases, state_month_data);
    bar(state_to_cases, state_month_data);
    pie(state_to_cases, state_month_data);
    pack(state_to_cases, state_month_data);
}
