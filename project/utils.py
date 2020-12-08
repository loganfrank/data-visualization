import plotly
import plotly.express as px
import plotly.graph_objects as go 

import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd 
import numpy as np
from wordcloud import WordCloud
import tweepy

def table(dataframe):
    """
    Generates a table object to output to Dash, taken from https://dash.plotly.com/layout

    :param dataframe: the Pandas DataFrame to model the table after
    """
    obj = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
        html.Tbody([html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(len(dataframe))])
    ])
    return obj

def dropdown(id, options, placeholder='Select an item'):
    """
    :param id: the identification name for the dropdown, used for callbacks
    :param options: array of dictionaries of label-value pairs which will be the options for this dropdown menu
    :param placeholder: message that will be default before an option is selected
    """
    obj = dcc.Dropdown(
        id=id,
        options=options,
        value=options[0]['value'],
        placeholder=placeholder,
        clearable=False,
        searchable=False
    )
    return obj

def checkboxes(id, options, select_all=True):
    """
    :param id: the identification name for the checkboxes, used for callbacks
    :param options: array of dictionaries of label-value pairs which will be the options for this dropdown menu
    :param select_all: determines if all or no options are selected off the start
    """
    if select_all:
        obj = dcc.Checklist(
            options=options,
            value=[entry['value'] for entry in options]
        )
    else:
        obj = dcc.Checklist(
            options=options
        )

    return obj

def radio(id, options):
    """
    :param id: the identification name for the radio items, used for callbacks
    :param options: array of dictionaries of label-value pairs which will be the options for this dropdown menu
    """
    obj = dcc.RadioItems(
        id=id,
        options=options,
        value=options[0]['value'],
        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
    )
    return obj

def slider(id, labels, step=1):
    """
    :param id: the identification name for the slider, used for callbacks
    :param labels: array of labels
    """
    obj = dcc.Slider(
        min=0,
        max=(len(labels) - 1),
        marks={i: label for i, label in enumerate(labels)},
        value=0,
        step=step
    )
    return obj

def range_slider(id, labels, step=1):
    """
    :param id: the identification name for the slider, used for callbacks
    :param labels: array of labels
    """
    obj = dcc.RangeSlider(
        id=id,
        min=0,
        max=(len(labels) - 1),
        marks={i: label for i, label in enumerate(labels)},
        value=[0, (len(labels) - 1)],
        step=step
    )
    return obj

def handle_debate_event(debate, time_or_topic):
    if debate == 'PD1':
        if time_or_topic == 'time':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'}
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'}
            )
    elif debate == 'PD2':
        if time_or_topic == 'time':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'}
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'}
            )
    elif debate == 'VPD':
        if time_or_topic == 'time':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'}
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '900px', 'marginLeft' : '50px', 'display': 'block'}
            )


def handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp):
    # TODO WIP
    # return biden src & style, trump src & style, harris src & style, pence src & style
    print(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp, sep='\n')
    if debate == 'PD1':
        biden_style = {'display': 'block'}
        trump_style = {'display': 'block'}
        harris_style = {'display': 'none'}
        pence_style = {'display': 'none'}
    elif debate == 'PD2':
        biden_style = {'display': 'block'}
        trump_style = {'display': 'block'}
        harris_style = {'display': 'none'}
        pence_style = {'display': 'none'}
    elif debate == 'VPD':
        biden_style = {'display': 'none'}
        trump_style = {'display': 'none'}
        harris_style = {'display': 'block'}
        pence_style = {'display': 'block'}


def plot_wordcloud(data):
    """
    Helper function for creating WordCloud, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    # d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='white', width=480, height=360)
    wc.fit_words(data)
    return wc.to_image()

def make_image(b):
    """
    Helper function to make a WordCloud image we can show, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    img = BytesIO()
    plot_wordcloud(data={'apple' : 5, 'cherry' : 10, 'lemon' : 2, 'orange' : 7, 'pineapple' : 9}).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())