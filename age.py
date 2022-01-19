import streamlit as st
import pandas as pd
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

    c1, c2, c3 = st.columns([2, 8, 2])

    with c2:
        st.write("## What are different age demographics talking about?")
        st.write("Did >=40 years old respond differently to the pandemic than 18 years old? Were the former more interested "
                 "in talking about issues with the economy or healthcare?")

    start_date = str(st.sidebar.date_input("Starting When?", datetime.date(2020, 1, 17)))

    end_date = str(st.sidebar.date_input("Until When?", datetime.date(2021, 1, 17)))

    mask = (data['dates'] > start_date) & (data['dates'] <= end_date)
    filtered = data.loc[mask]

    c1, c2, c3 = st.columns([5, 2, 5])
    for group, col in zip(['>=40', '<=18', '19-29', '30-39'], [c1, c3, c1, c3]):

        with col:
            age_dict = dict(Counter(filtered[filtered["age"] == group]["topic"]))
            local_sum = sum(age_dict.values())

            for _ in age_dict:
                age_dict[_] /= local_sum


            st.write(f"{group} Stats")
            source = pd.DataFrame({
                'Topics': age_dict.keys(),
                'Tweets %': age_dict.values()
            })

            c = alt.Chart(source).mark_bar().encode(
                x='Topics',
                y='Tweets %'
            )

            st.altair_chart(c, use_container_width=True)

    c1, c2, c3 = st.columns([2, 8, 2])

    with c2:
        st.write("## General Emotional level")
        st.write("Are people in the age group 19-29 more angry in general than other demographics?")

    c1, c2, c3 = st.columns([5, 2, 5])
    for group, col in zip(['>=40', '<=18', '19-29', '30-39'], [c1, c3, c1, c3]):

        with col:
            age_dict = dict(Counter(filtered[filtered["age"] == group]["emotion"]))
            local_sum = sum(age_dict.values())

            for _ in age_dict:
                age_dict[_] /= local_sum


            st.write(f"{group} Stats")
            source = pd.DataFrame({
                'Topics': age_dict.keys(),
                'Tweets %': age_dict.values()
            })

            c = alt.Chart(source).mark_bar().encode(
                x='Topics',
                y='Tweets %'
            )

            st.altair_chart(c, use_container_width=True)