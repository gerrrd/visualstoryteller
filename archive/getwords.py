import nltk
from nltk.tokenize import word_tokenize
import joblib
import os
import random
from nltk.corpus import stopwords

def get_words(text):

    nltk_model_path = '/'.join([os.path.dirname(os.getcwd()),'visualstoryteller/data/nlp_model.pkl'])
    model = joblib.load(nltk_model_path)
    stopWords = set(stopwords.words('english'))
    text = nltk.word_tokenize(text)
    text = [word.lower() for word in text]
    text1 = nltk.pos_tag(text)
    nouns = []
    for n in text1:
        if n[1].startswith('N'):
            nouns.append(n[0])

    verbs = []
    for n in text1:
        if n[1].startswith('V'):
            verbs.append(n[0])

    # dealt with in getonecpic.py
    if (nouns == []) or (verbs == []):
        return 0, 0

    noun = ''
    invocab = False
    while (not invocab) and len(nouns) > 0:
        noun_chosen = random.randint(0,len(nouns)-1)
        noun = nouns.pop(noun_chosen)
        invocab = (noun in model.wv.vocab.keys())

    # if none of them is in the vocabulary:
    if not invocab:
        return 0, 0
    # else we have a word

    verb = ''
    invocab = False
    while (not invocab) and len(verbs) > 0:
        verb_chosen = random.randint(0,len(verbs)-1)
        verb = verbs.pop(verb_chosen)
        invocab = (verb in model.wv.vocab.keys())

    # if none of them is in the vocabulary:
    if not invocab:
        return 0, 0
    # else we have a word

    list_nouns = model.most_similar(positive=[noun], topn = 3)
    list_verbs = model.most_similar(positive=[verb], topn = 10)

    similar_nouns = [s[0] for s in list_nouns]
    similar_verbs = [s[0] for s in list_verbs]
    similar2_verbs = [v for v in similar_verbs if v not in stopWords]
    return similar_nouns, similar2_verbs[-3:]

