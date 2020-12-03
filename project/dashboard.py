import plotly
import plotly.express as px
import plotly.graph_objects as go 

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd 
import numpy as np

from utils import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Visualizing the 2020 Presidential Election!'),
        html.H4('CSE5544 Intro to Data Visualization Final Project'),
        html.H4('Ron Davies & Logan Frank'),
        html.Br(),
        html.Br(),
        html.H3('Debate Visualization'),
        html.Div(
            children=[dropdown('debate_selector', [{'label': 'Presidential Debate #1', 'value' : 'PD1'}, {'label': 'Presidential Debate #2', 'value' : 'PD2'}, {'label': 'Vice-Presidential Debate', 'value' : 'VPD'}])],
            style={'width' : '300px'}
        ),
        html.Br(),
        html.Br(),
        html.H3('Google Trends Visualization'),
        html.Div(
            children=[slider('example_slider', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={}
        )
    ],
    style={'marginLeft' : '50px', 'marginRight' : '50px', 'marginTop' : '50px'}
)


if __name__ == '__main__':
    app.run_server(debug=True)