import os

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def change_speaker_names(x):
    if x == 'Vice President Joe Biden':
        return 'Joe Biden'
    elif x == 'President Donald J. Trump':
        return 'Donald Trump'
    else:
        return x

def add_hour(x):
    temp = x.split(':')
    if len(temp) == 2:
        x = f'00:{x}'
    return x

def overflow(x):
    hour, minute, second = x['hour'], x['minute'], x['second']
    if second >= 60:
        minute += (second // 60)
        second = second % 60
    if minute >= 60:
        hour = (minute // 60)
        minute = minute % 60
    return hour, minute, second

def underflow(x):
    hour, minute, second = x['hour'], x['minute'], x['second']
    if second < 0:
        minute -= abs(second // 60)
        second = abs(second % 60)
    if minute < 0:
        hour = abs(minute // 60)
        minute = abs(minute % 60)
    return hour, minute, second

def convert_time(x):
    hour, minute, second = x['hour'], x['minute'], x['second']
    hour = str(hour)
    minute = str(minute)
    second = str(second)
    return f'{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}'
        
def time_in_seconds(x):
    return 3600 * x['hour'] + 60 * x['minute'] + x['second']

def format_time(x):
    hour = str(int(x // 3600))
    x = x % 3600
    minute = str(int(x // 60))
    x = x % 60
    second = str(int(x))
    return f'{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}'

vectorized_format_time = np.vectorize(format_time)


####################################
##### Data Retrieval Functions #####
####################################

def first_debate():
    # Load data
    debate1 = pd.read_csv('./data/kaggle_debate/us_election_2020_1st_presidential_debate.csv', dtype={'speaker' : str, 'minute' : str, 'text' : str})

    # Some preprocessing
    debate1['time'] = debate1['minute']
    debate1['time'] = debate1['time'].apply(add_hour)
    debate1['second'] = debate1['time'].apply(lambda x: int(x.split(':')[2]))
    debate1['minute'] = debate1['time'].apply(lambda x: int(x.split(':')[1]))
    debate1['hour'] = debate1['time'].apply(lambda x: int(x.split(':')[0]))
    debate1 = debate1[['speaker', 'time', 'hour', 'minute', 'second', 'text']]

    # Change speaker names
    debate1['speaker'] = debate1['speaker'].apply(change_speaker_names)

    # Fixes timing issues (of resets)
    hour, minute, second = debate1.iloc[[178]][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate1.iloc[179:]['hour'] = debate1.iloc[179:]['hour'] + hour
    debate1.iloc[179:]['minute'] = debate1.iloc[179:]['minute'] + minute
    debate1.iloc[179:]['second'] = debate1.iloc[179:]['second'] + second

    # Fixes potential overflow
    temp = debate1.iloc[179:][['hour', 'minute', 'second']].apply(overflow, axis=1).apply(pd.Series)
    debate1.iloc[179:]['hour'] = temp[0]
    debate1.iloc[179:]['minute'] = temp[1]
    debate1.iloc[179:]['second'] = temp[2]

    # Shift everything so we start at 00:00
    hour, minute, second = debate1.iloc[0][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate1['hour'] = debate1['hour'] - hour
    debate1['minute'] = debate1['minute'] - minute
    debate1['second'] = debate1['second'] - second

    # Fixes potential underflow
    temp = debate1[['hour', 'minute', 'second']].apply(underflow, axis=1).apply(pd.Series)
    debate1['hour'] = temp[0]
    debate1['minute'] = temp[1]
    debate1['second'] = temp[2]

    # Fix overall time
    debate1['time'] = debate1[['hour', 'minute', 'second']].apply(convert_time, axis=1)
    debate1['time_seconds'] = debate1[['hour', 'minute', 'second']].apply(time_in_seconds, axis=1)

    # Partition different dataframes
    biden_debate1 = debate1[debate1['speaker'] == 'Joe Biden']
    trump_debate1 = debate1[debate1['speaker'] == 'Donald Trump']

    # Get the slider info
    low, high = debate1['time_seconds'].iloc[[0, -1]].to_numpy()
    seconds, step_size = np.linspace(low, high, num=30, retstep=True)
    seconds = seconds.round()
    index_to_seconds = {}
    for i, second in enumerate(seconds):
        index_to_seconds[i] = second
    times = vectorized_format_time(seconds)

    return debate1, biden_debate1, trump_debate1, times, index_to_seconds


def second_debate():
    # Load data
    debate2 = pd.read_csv('./data/kaggle_debate/us_election_2020_2nd_presidential_debate.csv', dtype={'speaker' : str, 'minute' : str, 'text' : str})

    # Some preprocessing
    debate2['time'] = debate2['minute']
    debate2['time'] = debate2['time'].apply(add_hour)
    debate2['second'] = debate2['time'].apply(lambda x: int(x.split(':')[2]))
    debate2['minute'] = debate2['time'].apply(lambda x: int(x.split(':')[1]))
    debate2['hour'] = debate2['time'].apply(lambda x: int(x.split(':')[0]))
    debate2 = debate2[['speaker', 'time', 'hour', 'minute', 'second', 'text']]

    # Fixes first timing issue (of resets)
    hour, minute, second = debate2.iloc[[88]][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate2.iloc[89:337]['hour'] = debate2.iloc[89:337]['hour'] + hour
    debate2.iloc[89:337]['minute'] = debate2.iloc[89:337]['minute'] + minute
    debate2.iloc[89:337]['second'] = debate2.iloc[89:337]['second'] + second
    debate2.iloc[89:337]

    # Fixes potential overflow
    temp = debate2.iloc[89:337][['hour', 'minute', 'second']].apply(overflow, axis=1).apply(pd.Series)
    debate2.iloc[89:337]['hour'] = temp[0]
    debate2.iloc[89:337]['minute'] = temp[1]
    debate2.iloc[89:337]['second'] = temp[2]

    # Fixes first timing issue (of resets)
    hour, minute, second = debate2.iloc[[336]][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate2.iloc[337:]['hour'] = debate2.iloc[337:]['hour'] + hour
    debate2.iloc[337:]['minute'] = debate2.iloc[337:]['minute'] + minute
    debate2.iloc[337:]['second'] = debate2.iloc[337:]['second'] + second

    # Fixes potential overflow
    temp = debate2.iloc[337:][['hour', 'minute', 'second']].apply(overflow, axis=1).apply(pd.Series)
    debate2.iloc[337:]['hour'] = temp[0]
    debate2.iloc[337:]['minute'] = temp[1]
    debate2.iloc[337:]['second'] = temp[2]

    # Shift everything so we start at 00:00
    hour, minute, second = debate2.iloc[0][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate2['hour'] = debate2['hour'] - hour
    debate2['minute'] = debate2['minute'] - minute
    debate2['second'] = debate2['second'] - second

    # Fixes potential underflow
    temp = debate2[['hour', 'minute', 'second']].apply(underflow, axis=1).apply(pd.Series)
    debate2['hour'] = temp[0]
    debate2['minute'] = temp[1]
    debate2['second'] = temp[2]

    # Fix overall time
    debate2['time'] = debate2[['hour', 'minute', 'second']].apply(convert_time, axis=1)
    debate2['time_seconds'] = debate2[['hour', 'minute', 'second']].apply(time_in_seconds, axis=1)

    # Partition different dataframes
    biden_debate2 = debate2[debate2['speaker'] == 'Joe Biden']
    trump_debate2 = debate2[debate2['speaker'] == 'Donald Trump']

    # Get the slider info
    low, high = debate2['time_seconds'].iloc[[0, -1]].to_numpy()
    seconds, step_size = np.linspace(low, high, num=30, retstep=True)
    seconds = seconds.round()
    index_to_seconds = {}
    for i, second in enumerate(seconds):
        index_to_seconds[i] = second
    times = vectorized_format_time(seconds)

    return debate2, biden_debate2, trump_debate2, times, index_to_seconds


def vp_debate():
    # Load data
    debate_vp = pd.read_csv('./data/kaggle_debate/us_election_2020_vice_presidential_debate.csv', dtype={'speaker' : str, 'minute' : str, 'text' : str})

    # Some preprocessing
    debate_vp['time'] = debate_vp['minute']
    debate_vp['time'] = debate_vp['time'].apply(add_hour)
    debate_vp['second'] = debate_vp['time'].apply(lambda x: int(x.split(':')[2]))
    debate_vp['minute'] = debate_vp['time'].apply(lambda x: int(x.split(':')[1]))
    debate_vp['hour'] = debate_vp['time'].apply(lambda x: int(x.split(':')[0]))
    debate_vp = debate_vp[['speaker', 'time', 'hour', 'minute', 'second', 'text']]

    # Adjust the reset to 00:00
    hour, minute, second = debate_vp.iloc[[135]][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate_vp.iloc[135:]['hour'] = debate_vp.iloc[135:]['hour'] - hour
    debate_vp.iloc[135:]['minute'] = debate_vp.iloc[135:]['minute'] - minute
    debate_vp.iloc[135:]['second'] = debate_vp.iloc[135:]['second'] - second

    # Fixes potential underflow
    temp = debate_vp.iloc[135:][['hour', 'minute', 'second']].apply(underflow, axis=1).apply(pd.Series)
    debate_vp.iloc[135:]['hour'] = temp[0]
    debate_vp.iloc[135:]['minute'] = temp[1]
    debate_vp.iloc[135:]['second'] = temp[2]

    # Fixes first timing issue (of resets)
    hour, minute, second = debate_vp.iloc[[134]][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate_vp.iloc[135:]['hour'] = debate_vp.iloc[135:]['hour'] + hour
    debate_vp.iloc[135:]['minute'] = debate_vp.iloc[135:]['minute'] + minute
    debate_vp.iloc[135:]['second'] = debate_vp.iloc[135:]['second'] + second
    debate_vp.iloc[135:]

    # Fixes potential overflow
    temp = debate_vp.iloc[135:][['hour', 'minute', 'second']].apply(overflow, axis=1).apply(pd.Series)
    debate_vp.iloc[135:]['hour'] = temp[0]
    debate_vp.iloc[135:]['minute'] = temp[1]
    debate_vp.iloc[135:]['second'] = temp[2]

    # Shift everything so we start at 00:00
    hour, minute, second = debate_vp.iloc[0][['hour', 'minute', 'second']].to_numpy().squeeze().astype(int)
    debate_vp['hour'] = debate_vp['hour'] - hour
    debate_vp['minute'] = debate_vp['minute'] - minute
    debate_vp['second'] = debate_vp['second'] - second

    # Fixes potential underflow
    temp = debate_vp[['hour', 'minute', 'second']].apply(underflow, axis=1).apply(pd.Series)
    debate_vp['hour'] = temp[0]
    debate_vp['minute'] = temp[1]
    debate_vp['second'] = temp[2]

    # Fix overall time
    debate_vp['time'] = debate_vp[['hour', 'minute', 'second']].apply(convert_time, axis=1)
    debate_vp['time_seconds'] = debate_vp[['hour', 'minute', 'second']].apply(time_in_seconds, axis=1)

    # Partition different dataframes
    harris_debate_vp = debate_vp[debate_vp['speaker'] == 'Kamala Harris']
    pence_debate_vp = debate_vp[debate_vp['speaker'] == 'Mike Pence']

    # Get the slider info
    low, high = debate_vp['time_seconds'].iloc[[0, -1]].to_numpy()
    seconds, step_size = np.linspace(low, high, num=30, retstep=True)
    seconds = seconds.round()
    index_to_seconds = {}
    for i, second in enumerate(seconds):
        index_to_seconds[i] = second
    times = vectorized_format_time(seconds)

    return debate_vp, harris_debate_vp, pence_debate_vp, times, index_to_seconds

def get_political_topics():
    political_topics = [
        {'label': 'COVID-19', 'value': 'covid'},
        {'label': 'Economy', 'value': 'economy'},
        {'label': 'Racial Equality', 'value': 'racism'},
        {'label': 'Violence', 'value': 'violence'},
        {'label': 'Social Rights', 'value': 'social'},
        {'label': 'Healthcare', 'value': 'health'},
        {'label': 'Unemployment', 'value': 'unemployment'},
        {'label': 'Sex Equality', 'value': 'sex'},
        {'label': 'Education', 'value': 'education'},
        {'label': 'Election Integrity', 'value': 'election'},
        {'label': 'Environment', 'value': 'environment'},
        {'label': 'Police', 'value': 'police'},
        {'label': 'Military', 'value': 'military'},
        {'label': 'Foreign Policity', 'value': 'foreign'}
    ]

    political_subtopics = {
        'covid': [],
        'economy': [],
        'racism': [],
        'violence': [],
        'social': [],
        'health': [],
        'unemployment': [],
        'sex': [],
        'education': [],
        'election': [],
        'environment': [],
        'police': [],
        'military': [],
        'foreign': []
    }
    related_words_dir = './data/google_trends/related_words/'

    for topic_file in os.listdir(related_words_dir):
        topic = topic_file.split('-')[0]
        with open(f'{related_words_dir}{topic_file}', 'r') as f:
            subwords = f.readlines()
            subwords = [subword.strip(' \n') for subword in subwords]
        political_subtopics[topic] = subwords

    return political_topics, political_subtopics



