# -*- coding: utf-8 -*-
'''Preprocess module

This module provides a function to clean and preprocess WhatsApp chat data.
The `preprocess` function takes a string of WhatsApp chat data as input,
extracts the dates, users, and messages, and returns a pandas DataFrame'''
import re
import pandas as pd

def preprocess(data:str) -> pd.DataFrame:
    '''Cleaning and preprocessing data'''
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}[\s\S][p,a]m\s-[\s\S]'
    messages = re.split(pattern, data)[1:]
    if len(messages)==0:
        return pd.DataFrame({'Error':["your chat file is courrpted or something went wrong!"]})
    raw_dates = re.findall(pattern, data)
    # replacing 'narrow no-break space' with a 'spcae'
    dates = [i.replace('\u202f'," ").strip() for i in raw_dates]

    # seperating users and messages
    users = []
    filter_messages = []
    for msg in messages:
        entry = re.split(r'(?<=\S):\s', msg, 1)  # Split only at the first colon followed by a space
        if len(entry) > 1:
            users.append(entry[0])
            filter_messages.append(entry[1])
        else:
            users.append('group_notification')
            filter_messages.append(entry[0])

    # converting data into dataFrame
    df = pd.DataFrame({'date':dates, 'user':users,'message':filter_messages})
    # converting string into datetime object
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p -')
    # seprating year column
    df['year'] = df['date'].dt.year
    # seperating month
    df['month'] = df['date'].dt.month_name()
    # separating day
    df['day'] = df['date'].dt.day
    # seperating hour
    df['hour'] = df['date'].dt.hour
    # separating minute
    df['minute'] =  df['date'].dt.minute
    # adding month name column in words
    df['month_num'] = df['date'].dt.month
    # adding only_date without time
    df['only_date'] = df['date'].dt.date
    # adding day_name column
    df['day_name'] = df['date'].dt.day_name()

    return df
