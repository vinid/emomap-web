import streamlit as st
import main
import gender
import age

PAGES = {
    "Home": main,
    "Gender": gender,
    "Age": age

}

st.write("# EmoMap Covid")

page = st.sidebar.radio("", list(PAGES.keys()))
PAGES[page].app()