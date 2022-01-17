import streamlit as st
import pandas as pd
from collections import Counter
import altair as alt
import datetime

@st.cache
def fetch_and_clean_data():
    data = pd.read_csv("data.csv")
    return data

def app():
    data = fetch_and_clean_data()

    st.write("# EmoMap Covid")

    start_date = str(st.sidebar.date_input("Starting When?"))

    end_date = str(st.sidebar.date_input("Until When?"))

    mask = (data['dates'] > start_date) & (data['dates'] <= end_date)
    filtered = data.loc[mask]

    c1, c2, c3 = st.columns([5, 2, 5])
    for group, col in zip(['>=40', '<=18', '19-29', '30-39'], [c1, c3, c1, c3]):

        with col:
            male_dict = dict(Counter(filtered[filtered["gender"] == "male"]["topic"]))
            local_sum = sum(male_dict.values())



            for _ in male_dict:
                male_dict[_] /= local_sum

            female_dict = dict(Counter(filtered[filtered["gender"] == "female"]["topic"]))
            local_sum = sum(female_dict.values())

            for _ in female_dict:
                female_dict[_] /= local_sum

            st.write(f"{group} Stats")
            source = pd.DataFrame({
                'Topics': female_dict.keys(),
                'Tweets %': female_dict.values()
            })

            c = alt.Chart(source).mark_bar().encode(
                x='Topics',
                y='Tweets %'
            )

            st.altair_chart(c, use_container_width=True)

