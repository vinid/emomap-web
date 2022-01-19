import streamlit as st
from collections import Counter
import altair as alt
import pandas as pd
import datetime

@st.cache
def fetch_and_clean_data():
    data = pd.read_csv("data.csv")
    return data

def app():
    data = fetch_and_clean_data()

    c1, c2, c3 = st.columns([1, 10, 1])

    with c2:
        st.write("## Talking About Which Topics")
        st.write("See what males and females talk about over the course of the pandemic")

    start_date = str(st.sidebar.date_input("Starting When?", datetime.date(2020, 1, 17)))

    end_date = str(st.sidebar.date_input("Until When?", datetime.date(2021, 1, 17)))

    mask = (data['dates'] > start_date) & (data['dates'] <= end_date)
    filtered = data.loc[mask]

    male_dict = dict(Counter(filtered[filtered["gender"] == "male"]["topic"]))
    local_sum = sum(male_dict.values())

    c1, c2, c3 = st.columns([5,2,5])

    for _ in male_dict:
        male_dict[_] /= local_sum

    female_dict = dict(Counter(filtered[filtered["gender"] == "female"]["topic"]))
    local_sum = sum(female_dict.values())

    for _ in female_dict:
        female_dict[_] /= local_sum

    with c1:
        st.write("Female Stats")
        source = pd.DataFrame({
            'Topics': female_dict.keys(),
            'Tweets %': female_dict.values()
        })

        c = alt.Chart(source).mark_bar().encode(
            x='Topics',
            y='Tweets %'
        )

        st.altair_chart(c, use_container_width=True)

    with c3:
        st.write("Male Stats")
        source = pd.DataFrame({
            'Topics': male_dict.keys(),
            'Tweets %': male_dict.values()
        })

        c = alt.Chart(source).mark_bar().encode(
            x='Topics',
            y='Tweets %'
        )

        st.altair_chart(c, use_container_width=True)

    c1, c2, c3 = st.columns([1, 10, 1])

    with c2:
        st.write("## Which Emotions")
        st.write("See which are the feelings of males and females the course of the pandemic")


    c1, c2, c3 = st.columns([5, 2, 5])

    for gen, col in zip(["male", "female"], [c1, c3]):

        gen_dict = dict(Counter(filtered[filtered["gender"] == gen]["emotion"]))
        local_sum = sum(gen_dict.values())

        for _ in gen_dict:
            gen_dict[_] /= local_sum

        with col:
            st.write(f"{gen} Emotion Stats")
            source = pd.DataFrame({
                'Emotions': gen_dict.keys(),
                'Tweets %': gen_dict.values()
            })

            c = alt.Chart(source).mark_bar().encode(
                x='Emotions',
                y='Tweets %'
            )

            st.altair_chart(c, use_container_width=True)