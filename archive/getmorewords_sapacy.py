# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy

# Load English tokenizer, tagger, parser and NER
def get_more_words(text):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

# Process whole document
    

# Analyze syntax
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]

# Find named entities, phrases and concepts
#for entity in doc.ents:
    #print(entity.text, entity.label_)

    return noun_phrases, verbs
