import random
import spacy

def noun_adj(adj,verb):
    if len(adj) > 0:
        return adj[random.randint(0, len(adj)-1)]
    elif len(verb) > 0:
        return verb[random.randint(0, len(verb)-1)]
    else:
        return 'love'

def get_more_words(text, maxnouns = 6):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    nouns_adjectives = []
    verbs = [str(token.lemma_) for token in doc if token.pos_ == "VERB"]
    chunks = [x.text for x in doc.noun_chunks]
    for ch in chunks:
        chd = nlp(ch)
        nouns = [str(token) for token in chd if token.pos_ == "NOUN"]
        if len(nouns):
            adjectives = [str(token) for token in chd if token.pos_ == "ADJ"]
            for n in nouns:
                noun = n
                adj = noun_adj(adjectives, verbs)
                nouns_adjectives.append([noun, adj])

    while len(nouns_adjectives) > maxnouns:
        del nouns_adjectives[random.randint(1,len(nouns_adjectives)-2)]

    nouns_adjectives

    return nouns_adjectives
