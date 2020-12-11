import math
import re
from io import BytesIO
import base64

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
    options = [{'label': option, 'value': option} for option in options]
    if select_all:
        obj = dcc.Checklist(
            id=id,
            options=options,
            value=[entry['value'] for entry in options],
            labelStyle={'display': 'inline-block', 'marginRight': '15px'}
        )
    else:
        obj = dcc.Checklist(
            id=id,
            options=options,
            labelStyle={'display': 'inline-block', 'marginRight': '15px'}
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
        id=id,
        min=0,
        max=(len(labels) - 1),
        marks={i: {'label': (label.lstrip('00:') if label != '00:00:00' else '0:00'), 'style': {'font-size': '11px'}} for i, label in enumerate(labels)},
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
        marks={i: {'label': (label.lstrip('00:') if label != '00:00:00' else '0:00'), 'style': {'font-size': '11px'}} for i, label in enumerate(labels)},
        value=[0, (len(labels) - 1)],
        step=step,
        allowCross=False
    )
    return obj

def handle_debate_event(debate, time_or_topic):
    if debate == 'PD1':
        if time_or_topic == 'time':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'}
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'}
            )
    elif debate == 'PD2':
        if time_or_topic == 'time':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
            )
    elif debate == 'VPD':
        if time_or_topic == 'time':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'}
            )
        elif time_or_topic == 'topic':
            return (
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'none'},
                {'width' : '96%', 'marginLeft' : '50px', 'display': 'block'}
            )

placeholder_wordcloud_data = {'apple' : 5}
remove_string = ['the', 'is', 'of', 'that', 'to', 'and', 'he', 'you', 'it', 'a', 'in', 'crosstalk', 'i', 'we', 'have', 'they', 'its', 'but', 'because', 'was', 'were', 'be', 'do', 'at', 'not', 'what',
                 'are', 'by', 'for', 'thats', 'your', 'with', 'this', 'so', 'on', 'doing', 'going', 'who', 'way', 'want', 'look', 'has', 'im', 'if', 'get', 'all', 'about', 'now', 'as', 'well', 'out',
                 'did', 'said', 'how', 'down', 'would', 'when', 'had', 'like', 'there', 'them', 'no']

def cloud(data):
    """
    Helper function for creating WordCloud, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    wc = WordCloud(background_color='white', width=450, height=450)
    wc.fit_words(data)
    return wc.to_image()

def make_wordcloud(data):
    """
    Helper function to make a WordCloud image we can show, taken from https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    """
    img = BytesIO()
    cloud(data=data).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

def temporary_word_cloud():
    return make_wordcloud(placeholder_wordcloud_data)

def create_wordcloud(slider_range, dataframe, index_to_time):
    if slider_range[0] == slider_range[1]:
        hist = {}
        hist['none'] = 1
    else:
        # Do some linear interpolation
        low = slider_range[0]    
        low_low = math.floor(low)
        low_high = math.ceil(low)

        low_low_y = index_to_time[low_low]
        low_high_y = index_to_time[low_high]

        low_dec = low - low_low
        low = low_low_y + (low_dec * (low_high_y - low_low_y))

        high = slider_range[1]
        high_low = math.floor(high)
        high_high = math.ceil(high)

        high_low_y = index_to_time[high_low]
        high_high_y = index_to_time[high_high]

        high_dec = high - high_low
        high = high_low_y + (high_dec * (high_high_y - high_low_y))

        # Threshold the data frame 
        parsed = dataframe[(dataframe['time_seconds'] >= low) & (dataframe['time_seconds'] <= high)]

        # Parse the text to get word to frequency pairs
        text = parsed['text']
        text = ' '.join(text)
        text = re.sub(r'[^\w\s]','',text).lower()
        text = text.split()
        text = np.array([w for w in text if w not in remove_string])
        words, frequencies = np.unique(text, return_counts=True)

        # Create a dictionary for histogram
        hist = {}
        for word, frequency in zip(words, frequencies):
            hist[word] = frequency

    return make_wordcloud(hist)

topic_index_to_time1 = {
    0: 0,
    1: 1040,
    2: 1938,
    3: 2894,
    4: 3961,
    5: 4949,
    6: 5636,
}

topic_index_to_time2 = {
    0: 0,
    1: 1741,
    2: 2872,
    3: 4241,
    4: 5033,
    5: 5748,
    6: 5975,
}

topic_index_to_time_vp = {
    0: 0,
    1: 804,
    2: 1403,
    3: 1957,
    4: 2550,
    5: 3381,
    6: 4026,
    7: 4690,
    8: 5270
}

def create_wordcloud_from_topic(slider_range, dataframe, index_to_time):
    # Do some linear interpolation
    low = index_to_time[slider_range[0]]
    high = index_to_time[slider_range[1] + 1]

    # Threshold the data frame 
    parsed = dataframe[(dataframe['time_seconds'] >= low) & (dataframe['time_seconds'] <= high)]

    # Parse the text to get word to frequency pairs
    text = parsed['text']
    text = ' '.join(text)
    text = re.sub(r'[^\w\s]','',text).lower()
    text = text.split()
    text = np.array([w for w in text if w not in remove_string])
    words, frequencies = np.unique(text, return_counts=True)

    # Create a dictionary for histogram
    hist = {}
    for word, frequency in zip(words, frequencies):
        hist[word] = frequency

    return make_wordcloud(hist)

def handle_wordcloud_event(debate, time_or_topic, time1, time2, topic1, topic2, time_vp, topic_vp, both, candidate1, candidate2, times, index_to_time):
    # Handle who is visible and who isn't
    if debate == 'PD1' or debate == 'PD2':
        biden_style = {'display': 'inline-block'}
        trump_style = {'display': 'inline-block', 'marginLeft': '100px'}
        p_style = {'display': 'block', 'marginLeft': '100px'}
        harris_style = {'display': 'none'}
        pence_style = {'display': 'none'}
        vp_style = {'display': 'none'}
    elif debate == 'VPD':
        biden_style = {'display': 'none'}
        trump_style = {'display': 'none'}
        p_style = {'display': 'none'}
        harris_style = {'display': 'inline-block'}
        pence_style = {'display': 'inline-block', 'marginLeft': '100px'}
        vp_style = {'display': 'block', 'marginLeft': '100px'}

    # Handle generating the word clouds
    if time_or_topic == 'time':
        if debate == 'PD1':
            wc1 = create_wordcloud(time1, candidate1, index_to_time)
            wc2 = create_wordcloud(time1, candidate2, index_to_time)
        elif debate == 'PD2':
            wc1 = create_wordcloud(time2, candidate1, index_to_time)
            wc2 = create_wordcloud(time2, candidate2, index_to_time)
        elif debate == 'VPD':
            wc3 = create_wordcloud(time_vp, candidate1, index_to_time)
            wc4 = create_wordcloud(time_vp, candidate2, index_to_time)
    elif time_or_topic == 'topic':
        if debate == 'PD1':
            wc1 = create_wordcloud_from_topic(topic1, candidate1, topic_index_to_time1)
            wc2 = create_wordcloud_from_topic(topic1, candidate2, topic_index_to_time1)
        elif debate == 'PD2':
            wc1 = create_wordcloud_from_topic(topic2, candidate1, topic_index_to_time2)
            wc2 = create_wordcloud_from_topic(topic2, candidate2, topic_index_to_time2)
        elif debate == 'VPD':
            wc3 = create_wordcloud_from_topic(topic_vp, candidate1, topic_index_to_time_vp)
            wc4 = create_wordcloud_from_topic(topic_vp, candidate2, topic_index_to_time_vp)

    if debate == 'PD1' or debate == 'PD2':
        wc3 = temporary_word_cloud()
        wc4 = temporary_word_cloud()
    elif debate == 'VPD':
        wc1 = temporary_word_cloud()
        wc2 = temporary_word_cloud()

    return wc1, biden_style, wc2, trump_style, p_style, wc3, harris_style, wc4, pence_style, vp_style


def handle_spectrogram_event(debate, value):
    if debate == 'PD1':
        file_select = 'pDebate'
    elif debate == 'PD2':
        file_select = 'p2Debate'
    elif debate == 'VPD':
        file_select = 'vpDebate'
    image_filename = f'./data/spectrograms/{file_select}{value}.jpg'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

week_index = np.linspace(0, 11, 49)
csv_directory = './data/google_trends/interest/'

def find_nearest(array, value):
    """
    Taken from https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def handle_google_trends_event(topic, selected_subtopics, month_value):
    dataframe = pd.read_csv(f'{csv_directory}{topic}.csv')
    dataframe['indexes'] = week_index
    low = find_nearest(week_index, month_value[0])
    high = find_nearest(week_index, month_value[1])

    dataframe = dataframe[(dataframe['indexes'] >= low) & (dataframe['indexes'] <= high)]
    dataframe = dataframe[selected_subtopics]

    dataframe['total'] = dataframe.sum(axis=1)
    dataframe['total'] = dataframe['total'] / dataframe['total'].max() * 100
    dataframe = dataframe.reset_index()
    fig = px.line(dataframe, x='index', y='total', title='Google Trends Relative Interest over Week Number')

    fig.update_layout(
        xaxis_title='Relative Interest',
        yaxis_title='Week Number in 2020',
    )
    return fig