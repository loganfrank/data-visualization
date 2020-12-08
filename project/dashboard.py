import plotly
import plotly.express as px
import plotly.graph_objects as go 

import dash
from dash.dependencies import Input, Output
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
        html.Div([
            html.Div(
                children=[dropdown('debate_selector', [{'label': 'Presidential Debate #1', 'value' : 'PD1'}, {'label': 'Presidential Debate #2', 'value' : 'PD2'}, {'label': 'Vice-Presidential Debate', 'value' : 'VPD'}])],
                style={'width' : '300px', 'display': 'inline-block', 'marginRight': '50px'}
            ),
            html.Div(
                children=[radio('debate_time_topic_selector', [{'label': 'Time', 'value': 'time'}, {'label': 'Topic', 'value': 'topic'}])],
                style={'width' : '300px', 'display': 'inline-block'}
            ),
        ]),
        html.Br(),
        html.Div(
            id='time_slider1_div',
            children=[range_slider('time_slider1', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            id='time_slider2_div',
            children=[range_slider('time_slider2', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            id='topic_slider1_div',
            children=[range_slider('topic_slider1', ['The Trump and Biden Records', 'The Supreme Court', 'COVID-19', 'The Economy', 'Race and Violence in our Cities', 'The Integrity of the Election'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            id='topic_slider2_div',
            children=[range_slider('topic_slider2', ['Fighting COVID-19', 'American Families', 'Race in America', 'Climate Change', 'National Security', 'Leadership'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            id='time_slider_vp_div',
            children=[range_slider('time_slider_vp', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Div(
            id='topic_slider_vp_div',
            children=[range_slider('topic_slider_vp', ['Coronavirus Pandemic', 'Economy', 'Supreme Court', 'China / Foreign Policy', 'Racism', 'Presidential Health and Succession'])],
            style={'width' : '900px', 'marginLeft' : '50px'}
        ),
        html.Br(),
        html.Img(id="biden_cloud"),
        html.Img(id="trump_cloud"),
        html.Img(id="harris_cloud"),
        html.Img(id="pence_cloud"),
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

@app.callback(
    Output('time_slider1_div', 'style'),
    Output('time_slider2_div', 'style'),
    Output('topic_slider1_div', 'style'),
    Output('topic_slider2_div', 'style'),
    Output('time_slider_vp_div', 'style'),
    Output('topic_slider_vp_div', 'style'),
    Input('debate_selector', 'value'),
    Input('debate_time_topic_selector', 'value')
)
def change_slider(debate, time_or_topic):
    return handle_debate_event(debate, time_or_topic)

@app.callback(
    Output('biden_cloud', 'src'),
    Output('biden_cloud', 'style'),
    Output('trump_cloud', 'src'),
    Output('trump_cloud', 'style'),
    Output('harris_cloud', 'src'),
    Output('harris_cloud', 'style'),
    Output('pence_cloud', 'src'),
    Output('pence_cloud', 'style'),
    Input('debate_selector', 'value'),
    Input('debate_time_topic_selector', 'value'),
    Input('time_slider1', 'value'),
    Input('time_slider2', 'value'),
    Input('topic_slider1', 'value'),
    Input('topic_slider2', 'value'),
    Input('time_slider_vp', 'value'),
    Input('topic_slider_vp', 'value'),
)
def change_wordcloud(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp):
    return handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp)

if __name__ == '__main__':
    app.run_server(debug=True)