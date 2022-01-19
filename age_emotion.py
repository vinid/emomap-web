import streamlit as st
import pandas as pd
from collections import Counter
import altair as alt
import numpy as np

@st.cache
def fetch_and_clean_data():
    data = pd.read_csv("data_myear.csv")
    return data

def app():

    st.write("Topic-emotion relationship split by age demographic")

    data = fetch_and_clean_data()

    first_demo = st.sidebar.selectbox("First Demographic Group", options=['>=40', '30-39',  '19-29', '19-29'])
    second_demo = st.sidebar.selectbox("Second Demographic Group", options=['30-39',  '19-29', '<=18'])
    topic = st.sidebar.selectbox("Topic", options=['politics', 'economics', 'vaccine'])
    emotion = st.sidebar.selectbox("Topic", options=['joy', 'anger', 'sadness', 'fear'])

    data = data[~(data["emotion"] == "none")]

    filter_first_demo = ((data["age"] == first_demo) & (data["topic"] == topic))
    filter_second_demo = ((data["age"] == second_demo) & (data["topic"] == topic))

    first_demo_df = data[filter_first_demo]
    second_demo_df = data[filter_second_demo]

    first_sum = first_demo_df.groupby(["myear"]).count().reset_index()
    second_sum = second_demo_df.groupby(["myear"]).count().reset_index()

    first_demo_df = first_demo_df.groupby(["myear", "emotion"]).count().reset_index()
    second_demo_df = second_demo_df.groupby(["myear", "emotion"]).count().reset_index()

    first_demo_df = first_demo_df.merge(first_sum, on=["myear"])
    second_demo_df = second_demo_df.merge(second_sum, on=["myear"])




    classes = []
    values = []


    for base_df, demo in zip([first_demo_df, second_demo_df], [first_demo, second_demo]):

        to_data_df = base_df[base_df["emotion_x"] == emotion]
        print(to_data_df)
        local_val = to_data_df["topic_x"].values / to_data_df["topic_y"].values

        values.append(local_val)
        classes.append(f"{emotion}+{demo}")



    print(classes)
    print(np.array(values).shape)
    chart_data = pd.DataFrame(
        np.array(values).reshape((22, 2)),
        columns=classes, index=to_data_df["myear"].values.tolist())



    st.line_chart(chart_data)