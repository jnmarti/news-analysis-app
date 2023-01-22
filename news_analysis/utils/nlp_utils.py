import spacy

nlp = spacy.load("es_core_news_sm")

def get_entities(df):
    docs = nlp.pipe(df["content"])
    return list(map(lambda ents: [(x.text, x.label_) for x in ents], docs))