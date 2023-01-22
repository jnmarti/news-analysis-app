from math import ceil
import dateparser
import textwrap
from datasets import load_dataset

import matplotlib.pyplot as plt
import seaborn as sns
import nlplot

import streamlit as st

from news_analysis.utils.dataset_utils import get_dataset, get_page
from news_analysis.utils.nlp_utils import get_entities

dataset_id = "justinian336/salvadoran-news"

st.markdown("## News Analysis")

if st.session_state.get("df") is None:
    with st.spinner("Loading dataset..."):
        st.session_state["df"] = get_dataset(dataset_id)
        df = st.session_state["df"]
else:
    df = st.session_state["df"]

start_date = st.sidebar.date_input(label="Start Date", value=df["date"].min(), max_value=df["date"].max())
end_date = st.sidebar.date_input(label="End Date", value=df["date"].max(), min_value=start_date)

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

    if st.session_state.get("page") is None:
        st.session_state["page"] = 0

    page = st.selectbox(
        label="Page",
        index=st.session_state["page"],
        options=list(range(1, ceil(len(df)/10)))
        )

    page_df = get_page(df, page, 10)
    page_df["entities"] = get_entities(page_df)
    
    for _, row in page_df.iterrows():
        st.markdown(f"""<h2><a href="{row['link']}">{row['title']}</a></h2>""", unsafe_allow_html=True)
        image_src = row["image_src"].replace("&w=30", "&w=300")
        st.image(image_src)
        st.markdown(f"**{row['category_name']}**")
        st.markdown(f"**{row['date']}**")
        st.markdown(f"{textwrap.shorten(row['content'], width=300, placeholder='...')}")
        if len(row["entities"]) > 0:
            with st.expander(label="Entities", expanded=True):
                for ent, lab in row["entities"]:
                    st.markdown(f"- {ent} ({lab})")
        st.markdown("---")
