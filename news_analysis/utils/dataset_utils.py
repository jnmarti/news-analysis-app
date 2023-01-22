import dateparser
from datasets import load_dataset
import pandas as pd

from utils.nlp_utils import get_entities

def get_dataset(dataset_id):
    dataset = load_dataset(dataset_id)
    df = dataset["train"].to_pandas()
    df["category_name"] = df["category"].apply(dataset["train"].features["category"].int2str)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df.sort_values("date", ascending=False)

def filter_by_date(df, start_date, end_date):
    start_date = text_to_date(start_date)
    end_date = text_to_date(end_date)
    return df[(df["date"] >= start_date) & (df["date"] <= end_date)]


def get_page(df, page, page_size):
    return df.iloc[page * page_size:(page + 1) * page_size]