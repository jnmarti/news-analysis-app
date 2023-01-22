import dateparser
from datasets import load_dataset

def text_to_date(text):
    return dateparser.parse(text)

def get_dataset(dataset_id):
    dataset = load_dataset(dataset_id)
    df = dataset["train"].to_pandas()
    df["category_name"] = df["category"].apply(dataset["train"].features["category"].int2str)
    # df["date"] = df["date"].apply(text_to_date)
    return df