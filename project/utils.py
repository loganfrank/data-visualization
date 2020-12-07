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
        options=options,
        value=options[0]['value']
    )

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
        min=0,
        max=(len(labels) - 1),
        marks={i: label for i, label in enumerate(labels)},
        value=[0, (len(labels) - 1)],
        step=step
    )
    return obj

def plot_wordcloud(data):
    """
    Helper function for creating WordCloud, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    # d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='white', width=480, height=360)
    wc.fit_words(data)
    return wc.to_image()

