import spacy

nlp = spacy.load("es_core_news_sm")

def get_entities(df):
    docs = nlp.pipe(df["content"])
    return list(map(lambda doc: sorted({(ent.text, ent.label_) for ent in doc.ents if len(ent.text) > 1}, key=lambda x: x[1]), docs))