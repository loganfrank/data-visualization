import plotly
import plotly.express as px
import plotly.graph_objects as go 

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd 
import numpy as np
from wordcloud import WordCloud
import tweepy

from io import BytesIO
import base64

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
        html.Div(
            children=[range_slider('time_slider1', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            children=[range_slider('time_slider2', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            children=[range_slider('topic_slider1', ['The Trump and Biden Records', 'The Supreme Court', 'COVID-19', 'The Economy', 'Race and Violence in our Cities', 'The Integrity of the Election'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            children=[range_slider('topic_slider2', ['Fighting COVID-19', 'American Families', 'Race in America', 'Climate Change', 'National Security', 'Leadership'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Br(),
        html.Img(id="wordcloud1"),
        html.Img(id="wordcloud2"),
        html.Img(id="wordcloud3"),
        html.Br(),
        html.Br(),
        html.H3('Political Topics Visualization'),
        html.Div(
            children=[range_slider('month_slider', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], step=0.25)],
            style={}
        )
    ],
    style={'marginLeft' : '50px', 'marginRight' : '50px', 'marginTop' : '50px'}
)


@app.callback(dd.Output('wordcloud1', 'src'), [dd.Input('wordcloud1', 'id')])
def make_image(b):
    """
    Helper function to make a WordCloud image we can show, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    img = BytesIO()
    plot_wordcloud(data={'apple' : 5, 'cherry' : 10, 'lemon' : 2, 'orange' : 7, 'pineapple' : 9}).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

if __name__ == '__main__':
    app.run_server(debug=True)