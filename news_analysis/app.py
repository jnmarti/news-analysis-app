import dateparser
import textwrap
from datasets import load_dataset

import matplotlib.pyplot as plt
import seaborn as sns
import nlplot

import streamlit as st

from news_analysis.utils.dataset_utils import get_dataset

dataset_id = "justinian336/salvadoran-news"

st.markdown("## News Analysis")

if st.session_state.get("df") is None:
    with st.spinner("Loading dataset..."):
        st.session_state["df"] = get_dataset(dataset_id)
        df = st.session_state["df"]
else:
    df = st.session_state["df"]

start_date = st.sidebar.date_input(label="Start Date", value=df["date"].min(), max_value=df["date"].max())
end_date = st.sidebar.date_input(label="Start Date", value=df["date"].max(), min_value=start_date)

df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

tab1, tab2 = st.tabs(["Dataset Stats", "News Explorer"])

with tab1:
    st.markdown(f"**Number of articles: {len(df):,}**")
    st.markdown("### News Category Counts")
    category_counts = df["category_name"].value_counts().to_frame().reset_index().rename(columns={"index": "category", "category_name": "count"})
    st.bar_chart(category_counts, x="category", y="count")

    with st.spinner("Analyzing titles..."):
        npt = nlplot.NLPlot(df, target_col="title")
        stopwords = npt.get_stopword(top_n=50, min_freq=0)
    
    fig_title_bigram = npt.bar_ngram(
        title='Title Bigrams',
        xaxis_label='word_count',
        yaxis_label='word',
        ngram=2,
        top_n=50,
        width=500,
        height=500,
        color=None,
        horizon=True,
        stopwords=stopwords,
        verbose=False,
        save=False,
    )

    st.plotly_chart(fig_title_bigram)

with tab2:
    for _, row in df.head(10).iterrows():
        st.markdown(f"""<div><a href="{row['link']}">{row['title']}</a><div>""", unsafe_allow_html=True)
        st.markdown(f"**{row['category_name']}**")
        st.markdown(f"**{row['date']}**")
        st.markdown(f"{textwrap.shorten(row['content'], width=500, placeholder='...')}")
        st.markdown("---")