import streamlit as st

st.set_page_config(page_title="Home", layout="centered")

st.title("Welcome to the Flaskblog analysis")

st.page_link("pages/articles.py", label="Articles analysis")
st.page_link("pages/users.py", label="Users analysis")