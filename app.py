# -*- coding: utf-8 -*-
'''WhatsApp Chat Analyser App

This module provides a Streamlit-based application for analysing WhatsApp chat logs.
It allows users to upload a text file containing their WhatsApp chat log, and then
provides various statistics and insights about the chat, including total messages
and total words sent by each user.

The app provides a user-friendly interface for selecting a chat log file, choosing
a user to analyse, and viewing the analysis results.'''
import sys
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import preprocess
import helper

st.sidebar.title("Whatsapp Chat Analyser")
st.title("Chat Analysis")

uploded_file = st.sidebar.file_uploader("Choose a text file")
# converting bytedata into utf-8
if uploded_file is not None:
    data = uploded_file.read().decode('utf-8')
    df = preprocess.preprocess(data)
    # if chat file is corrupted then exit
    if df.shape[0] == 1:
        st.dataframe(df)
        sys.exit()
    st.dataframe(df)

    # fetch unique users
    userlist = df['user'].unique().tolist()
    userlist.remove('group_notification')
    userlist.sort()
    userlist.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis with respect to",userlist)

    if st.sidebar.button("Show Analysis"):
        # creating grid of 4 columns to display stats
        col1, col2, col3, col4 = st.columns(4,vertical_alignment='bottom')
        # fetching stats from helper module
        total_messages,total_words, total_media,total_links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)

        with col2:
            st.header("Total Words")
            st.title(total_words)

        with col3:
            st.header("Media Shared")
            st.title(total_media)

        with col4:
            st.header("Links Shared")
            st.title(total_links)

        # timeline analysis
        st.title("Timeline of Messages")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation="vertical")
        plt.xlabel('month-year')
        plt.ylabel('message-count')
        plt.grid()
        st.pyplot(fig)

        # daily timeline analysis
        st.title("Daily Timeline of Messages")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color="purple")
        plt.xticks(rotation="vertical")
        plt.xlabel('date')
        plt.ylabel('message-count')
        plt.grid()
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2, vertical_alignment='center')
        with col1:
            st.header("Most active day")
            active_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_day.index, active_day.values)
            plt.xticks(rotation="vertical")
            plt.ylabel('message-count')
            plt.xlabel('day')
            plt.grid()
            st.pyplot(fig)

        with col2:
            st.header("Most active month")
            active_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color='orange')
            plt.xticks(rotation="vertical")
            plt.ylabel('message-count')
            plt.xlabel('month')
            plt.grid()
            st.pyplot(fig)


        # creating grid of 2 columns
        col1, col2 = st.columns(2,vertical_alignment='center')
        # fetching most active users
        if selected_user =="Overall" :
            most_active_users, percent_df = helper.most_active_users(selected_user,df)
            fig,ax = plt.subplots()
            with col1:
                st.header("Most active users")
                # plotting bar graph
                ax.bar(most_active_users.index,most_active_users,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


            with col2:
                st.header(" "*20)
                st.dataframe(percent_df)

        # wordcloud
        st.header("Wordcloud")
        wordcoud = helper.generate_wordcloud(selected_user, df)
        if wordcoud:
            fig, ax = plt.subplots()
            ax.imshow(wordcoud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(fig)
        else:
            st.subheader("No words found !")

        # most common words
        st.header("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        if most_common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(most_common_df['word'],most_common_df['count'],color='green')
            plt.xlabel('Count')
            plt.ylabel('Words')
            plt.title('Most common words')
            plt.grid()
            st.pyplot(fig)
        else:
            st.subheader("No data found!")

        # most commom emojis
        st.header("Most Common Emojis")
        most_common_emojis = helper.most_common_emojis(selected_user, df)
        fig, ax = plt.subplots()
        emoji_freq_df = most_common_emojis.head(10)
        # Setting the font family to a font that supports emojis
        plt.rcParams['font.family'] = 'Segoe UI Emoji'  # Use 'Noto Color Emoji' if installed

        col1, col2 = st.columns(2,vertical_alignment='center')

        with col1:
            st.dataframe(most_common_emojis)

        # Create the pie chart
        with col2:
            if not most_common_emojis.shape[0] ==0:
                try:
                    wedges, texts, autotexts = ax.pie(
                        emoji_freq_df['frequency_count'],
                        labels=emoji_freq_df['emoji'],
                        autopct="%.2f")
                    img_idx = most_common_emojis.index[most_common_emojis['emoji']  == "🥲"]
                    img_idx = img_idx.tolist()[0]
                    #  Load the image you want to use as a label
                    IMAGE_PATH = "icons/emoji.png"  # Replace with the path to your image
                    image = plt.imread(IMAGE_PATH)

                    # Create an OffsetImage object
                    imagebox = OffsetImage(image, zoom=0.13)  # Adjust zoom as needed

                    # Select the slice you want to annotate (e.g., the first slice)
                    # Change this to the index of the slice you want to annotate
                    slice_index = img_idx

                    # Get the angle and position for the annotation
                    angle = (wedges[slice_index].theta2 + wedges[slice_index].theta1) / 2
                    # Offset x coordinate
                    x = wedges[slice_index].r * 1.2 * np.cos(np.deg2rad(angle))
                    # Offset y coordinate
                    y = wedges[slice_index].r * 1.2 * np.sin(np.deg2rad(angle))

                    # Create an AnnotationBbox
                    ab = AnnotationBbox(imagebox, (x, y), frameon=False, xybox=(8.3, -10),
                                        xycoords='data',
                                        boxcoords="offset points")

                    # Add the AnnotationBbox to the axes
                    ax.add_artist(ab)
                except IndexError:
                    pass

                # Adjust the display settings
                plt.setp(autotexts, size=8, weight="bold", color="white")
                plt.title('Emoji Frequency', fontsize=14)
                st.pyplot(fig)
            else:
                st.subheader("No emoji data found!")
