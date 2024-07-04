# -*- coding: utf-8 -*-
'''Helper module for WhatsApp chat analysis.

This module provides various functions to analyze WhatsApp chat data. 
It includes functions to filter messages, generate statistics, create word clouds,
identify common words and emojis, and visualize chat activity over time.
'''
from collections import Counter
# from streamlit import rerun   # uncomment this if you face error
from wordcloud import WordCloud
# Import stopwords with scikit-learn
from sklearn.feature_extraction import text as txt
import pandas as pd
import emoji

def get_words(series) -> str:
    """
    Extract words from a pandas Series.

    Args:
        series (pd.Series): Series containing text data.

    Returns:
        str: String of all words concatenated.
    """
    text_words = " ".join(series).split()
    return text_words

def filter_messages(df) -> pd.Series:
    """
    Filter out media and group notifications from messages.

    Args:
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.Series: Series with filtered messages.
    """
    # filtering media and group notifications
    temp = df[df['user']!="group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]
    # stopwords
    stop = txt.ENGLISH_STOP_WORDS
    # Filter the DataFrame with the stopwords
    filtered_df = temp['message'].apply(lambda y :  " ".join(
        [word for word in y.split() if word.lower() not in (stop)]
        ))
    # removing non word characters
    x = filtered_df.replace(r"[^\w\s]", '', regex=True)
    return x

def fetch_stats(selected_user, df):
    """
    Fetch statistics of messages, words, media, and links.

    Args:
        selected_user (str): Selected user to fetch stats for.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        tuple: Total messages, total words, total media messages, total links.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetching total messages
    total_messages = df.shape[0]
    # fetching total words
    total_words = len(get_words(df['message']))
    # fetching total media messages
    total_media = df[df['message']=="<Media omitted>\n"].shape[0]
    # fetching total links
    total_links = df[df['message'].str.contains('http','www')].shape[0]
    # from urlextract import URLExtract
    # extractor = URLExtract()
    # total_links = len(sum([extractor.find_urls(msg) for msg in df['message']],[]))

    return total_messages, total_words, total_media, total_links

def most_active_users(selected_user,df):
    """
    Get the most active users and their activity percentage.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        tuple or None: Most active users and their activity percentage if 'Overall' is selected.
    """
    if selected_user == 'Overall':
        user_list = df['user'].value_counts()
        percent_df = round(user_list/df.shape[0]*100,2)
        percent_df = percent_df.reset_index().rename(columns={'count':'percent'})
        return user_list.head(), percent_df
    return None

def generate_wordcloud(selected_user, df) -> WordCloud:
    """
    Generate a word cloud from messages.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        WordCloud or None: Generated word cloud or None if no text is available.
    """
    # Remove rows from the dataframe where the message is '<Media omitted>\n' and reset the index
    df = df[df['message']!='<Media omitted>\n'].reset_index(drop=True)
    # If the selected user is not 'Overall',
    # filter the dataframe to only include messages from the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Create a string of all the words in the messages, separated by spaces
    text = " ".join(df['message'])
    if not text:
        return None
    wordcloud = WordCloud(width=450, height=450,min_font_size=10).generate(text)
    return wordcloud

def most_common_words(selected_user, df) -> pd.DataFrame:
    """
    Get the most common words in messages.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.DataFrame: DataFrame with most common words and their counts.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = filter_messages(df)
    # Create a Counter for the words in the messages
    word_counts = Counter(" ".join(df).split())
    counter_as_tuple = word_counts.most_common(20)
    #print(f"[DEBUG] {counter_as_tuple}")
    if counter_as_tuple:
        word, count = zip(*counter_as_tuple)
        most_common_df = pd.DataFrame({'word':word, "count":count})
        return most_common_df
    return pd.DataFrame({})

def most_common_emojis(selected_user, df):
    """
    Get the most common emojis in messages.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.DataFrame: DataFrame with most common emojis and their frequency count.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = [c for msg in df['message'] for c in msg if c in emoji.EMOJI_DATA]
    emoji_freq_df = pd.DataFrame(Counter(emojis).most_common(),columns=['emoji','frequency_count'])
    return emoji_freq_df

def monthly_timeline(selected_user, df) -> pd.DataFrame:
    """
    Get the monthly timeline of messages.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.DataFrame: DataFrame with monthly message counts.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    # Create a new 'time' column with month-year format
    time = [f"{timeline['month'][i]}-{timeline['year'][i]}" for i in range(timeline.shape[0])]
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    """
    Get the daily timeline of messages.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.DataFrame: DataFrame with daily message counts.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_tmlne = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_tmlne

def week_activity_map(selected_user, df) -> pd.Series:
    """
    Get the activity map for days of the week.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.Series: Series with counts of messages for each day of the week.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df) -> pd.Series:
    """
    Get the activity map for months.

    Args:
        selected_user (str): Selected user to filter data.
        df (pd.DataFrame): DataFrame containing WhatsApp chat data.

    Returns:
        pd.Series: Series with counts of messages for each month.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
