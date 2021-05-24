import re
import nltk
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en_core_web_sm")


def get_names(string):
    doc2 = nlp(string)
    persons = [ent.text for ent in doc2.ents if ent.label_ == 'PERSON']

    return [x for x in persons if 1 < len(x.split(" ")) < 3]
