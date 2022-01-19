import streamlit as st
import main
import gender
import age
import age_emotion

PAGES = {
    "Home": main,
    "Gender": gender,
    "Age": age,
    "Age Emotion": age_emotion

}

st.write("# EmoMap Covid")

page = st.sidebar.radio("", list(PAGES.keys()))
PAGES[page].app()