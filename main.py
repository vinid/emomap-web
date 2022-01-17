import streamlit as st
import pandas as pd
import datetime

@st.cache
def fetch_and_clean_data():
    data = pd.read_csv("data.csv")
    return data

def app():

    st.write("## Region Analysis")
    st.write("See how people in different regions in Italy have responded to the pandemic with respect to some topic. Are"
             "people scared by the vaccine? Are they angry against politicians? What's the overall sentiment?")

    data = fetch_and_clean_data()

    start_date = str(st.sidebar.date_input("Starting When?", datetime.date(2020, 1, 17)))

    end_date = str(st.sidebar.date_input("Until When?", datetime.date(2021, 1, 17)))

    topic = st.sidebar.selectbox("What?", options=["politics", "vaccine", "economics", "health"])

    mask = (data['dates'] > start_date) & (data['dates'] <= end_date)
    filtered = data.loc[mask]

    filtered = filtered[filtered["topic"] == topic]

    filtered = filtered.pivot_table(index=['regions'], columns='emotion', aggfunc='size', fill_value=0)
    filtered = pd.DataFrame(filtered.to_records()).set_index(["regions"])
    filtered = filtered.div(filtered.sum(axis=1), axis=0)

    st.bar_chart(filtered)