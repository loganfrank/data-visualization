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
from data_processing import first_debate
from data_processing import second_debate
from data_processing import vp_debate
from data_processing import get_political_topics

# Collect necessary data
debate1, biden1, trump1, times1, index1 = first_debate()
debate2, biden2, trump2, times2, index2 = second_debate()
debate_vp, harris, pence, times_vp, index_vp = vp_debate()

political_topics, political_subtopics = get_political_topics()

# Set up the dashboard page
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
            children=[range_slider('time_slider1', times1, step=0.25)],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Div(
            id='topic_slider1_div',
            children=[range_slider('topic_slider1', ['The Supreme Court', 'COVID-19', 'The Economy', 'Race and Violence in our Cities', 'The Trump and Biden Records', 'The Integrity of the Election'])],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Div(
            id='time_slider2_div',
            children=[range_slider('time_slider2', times2, step=0.25)],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Div(
            id='topic_slider2_div',
            children=[range_slider('topic_slider2', ['Fighting COVID-19', 'National Security', 'American Families', 'Race in America', 'Climate Change', 'Leadership'])],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Div(
            id='time_slider_vp_div',
            children=[range_slider('time_slider_vp', times_vp, step=0.25)],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Div(
            id='topic_slider_vp_div',
            children=[range_slider('topic_slider_vp', ['Coronavirus Pandemic', 'The Role of the Vice President', 'Economy', 'Climate Change', 'China / Foreign Policy', 'Supreme Court', 'Racism', 'The Integrity of the Election'])],
            style={'width' : '96%', 'marginLeft' : '50px', 'marginRight' : '50px'}
        ),
        html.Br(),
        html.Div(
            id='p_cloud',
            children=[
                html.Div(id='biden_div', children=[html.H3('Joe Biden', style={'marginLeft': '35%'}), html.Img(id="biden_cloud")], style={'display': 'inline-block'}),
                html.Div(id='trump_div', children=[html.H3('Donald Trump', style={'marginLeft': '35%'}), html.Img(id="trump_cloud")], style={'display': 'inline-block'})
            ]
        ),
        html.Div(
            id='vp_cloud',
            children=[
                html.Div(id='harris_div', children=[html.H3('Kamala Harris', style={'marginLeft': '35%'}), html.Img(id="harris_cloud")], style={'display': 'inline-block'}),
                html.Div(id='pence_div', children=[html.H3('Mike Pence', style={'marginLeft': '35%'}), html.Img(id="pence_cloud")], style={'display': 'inline-block'})
            ]
        ),
        html.Br(),
        html.Br(),
        html.H3('Political Topics Visualization'),
        html.Div(
            children=[dropdown('political_topics_selector', political_topics)],
            style={'width' : '300px', 'display': 'block', 'marginRight': '50px'}
        ),
        html.Br(),
        html.Div(
            id='political_subtopics_checkboxes',
            children=[checkboxes(id='subtopics', options=political_subtopics['COVID-19'])],
            style={}
        ),
        html.Br(),
        html.Div(
            children=[range_slider('month_slider', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], step=0.25)],
            style={}
        )
    ],
    style={'marginLeft' : '50px', 'marginRight' : '50px', 'marginTop' : '50px', 'marginBottom': '500px'}
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
    Output('biden_div', 'style'),
    Output('trump_cloud', 'src'),
    Output('trump_div', 'style'),
    Output('p_cloud', 'style'),
    Output('harris_cloud', 'src'),
    Output('harris_div', 'style'),
    Output('pence_cloud', 'src'),
    Output('pence_div', 'style'),
    Output('vp_cloud', 'style'),
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
    if debate == 'PD1':
        return handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp, debate1, biden1, trump1, times1, index1)
    elif debate == 'PD2':
        return handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp, debate2, biden2, trump2, times2, index2)
    elif debate == 'VPD':
        return handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp, debate_vp, harris, pence, times_vp, index_vp)
    else:
        raise Exception('Unknown debate')

@app.callback(
    Output('political_subtopics_checkboxes', 'children'),
    Input('political_topics_selector', 'value')
)
def change_political_topics_checkboxes(political_topic):
    return [checkboxes(id='subtopics', options=political_subtopics[political_topic])]

if __name__ == '__main__':
    app.run_server(debug=True)