import spacy

nlp = spacy.load("es_core_news_md")

def get_entities(df):
    docs = nlp.pipe(df["content"])
    return list(map(lambda doc: sorted({(ent.text, ent.label_) for ent in doc.ents if len(ent.text) > 1 and ent.label_ != "MISC"}, key=lambda x: x[1]), docs))