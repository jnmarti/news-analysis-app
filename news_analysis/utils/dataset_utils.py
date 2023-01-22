import dateparser
from datasets import load_dataset
import pandas as pd

def get_dataset(dataset_id):
    dataset = load_dataset(dataset_id)
    df = dataset["train"].to_pandas()
    df["category_name"] = df["category"].apply(dataset["train"].features["category"].int2str)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def filter_by_date(df, start_date, end_date):
    start_date = text_to_date(start_date)
    end_date = text_to_date(end_date)
    return df[(df["date"] >= start_date) & (df["date"] <= end_date)]