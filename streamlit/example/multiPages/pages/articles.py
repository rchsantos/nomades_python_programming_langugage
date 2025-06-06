import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px

from data.firestore_connection import db, DocumentReference, DocumentSnapshot

def load_data() -> pd.DataFrame:
  articles: list[DocumentSnapshot] = db.collection("articles").order_by("created_at").get()
  articles_dict: list[dict[str, str | int | DocumentReference | datetime]] = []
  for article in articles:
    article_data: dict[str, str | datetime | DocumentReference] = article.to_dict()
    user_data: dict[str, str | int] = article_data["author"].get().to_dict()
    del article_data["author"]
    articles_dict.append(article_data | user_data)

  return pd.DataFrame(articles_dict)

def article_analysis() -> None:
  df = load_data()
  df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

  min_date = df["created_at"].min()
  max_date = df["created_at"].max()

  st.sidebar.title("Filters")

  dates = st.sidebar.date_input("Date filter", [min_date, max_date], min_value=min_date, max_value=max_date)
  df_filtered = df.loc[df.created_at.between(dates[0], dates[1])]

  authors = (df.firstname + " " + df.lastname).sort_values().unique()
  authors_multi = st.sidebar.multiselect("Author filter", authors, authors)
  print(authors_multi)
  selected_firstnames = [fullname.split()[0] for fullname in authors_multi]
  selected_lastnames = [fullname.split()[1] for fullname in authors_multi]
  df_filtered = df_filtered.loc[df_filtered.firstname.isin(selected_firstnames) & df_filtered.lastname.isin(selected_lastnames)]

  title_input = st.sidebar.text_input("Title search")
  df_filtered = df_filtered.loc[df_filtered.title.map(lambda title: title_input.lower() in title.lower())]

  post_per_date: pd.DataFrame = df_filtered.groupby("created_at").size()
  
  post_per_date_bar = px.bar(post_per_date, x=post_per_date.index, y=post_per_date.values)
  
  
  st.dataframe(df_filtered)
  print(len(df_filtered))
  st.plotly_chart(post_per_date_bar)


st.set_page_config(page_title="articles_analysis")
st.title("Welcome the the articles part")

article_analysis()