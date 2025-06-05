import streamlit as st
import pandas as pd

st.title("My first streamlit APP")

wines = pd.read_csv("wine-reviews/winemag-data-130k-v2.csv", index_col=0)

countries = st.sidebar.multiselect("Countries", wines["country"].unique(), ["Italy"])

wines_filtered = wines.loc[wines.country.isin(countries)]

st.dataframe(wines_filtered)

st.write(wines_filtered.price.max())
