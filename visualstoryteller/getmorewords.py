# visualstoryteller/getmorewords.py
# the function "get_more_words" is implemented to analyze (NLP) and input text
# with spaCy.

import random
import spacy

def noun_adj(adj=[], verb=[]):
    '''
    given a list of adjectives (adj) and verbs (verb), it returns a random
    element from the list of adjectives, or if it is empty, a random element
    from the list of verbs. If both are empty, it returns 'love'.
    '''

    # if there are adjective(s), we choose randomly one and return it
    if len(adj) > 0:
        return adj[random.randint(0, len(adj)-1)]
    # else if there are verbs(s), we choose randomly one and return it
    elif len(verb) > 0:
        return verb[random.randint(0, len(verb)-1)]
    # otherwise we return 'love'
    else:
        return 'love'

def get_more_words(text, maxnouns=6):
    '''
    Given an input text (text), it returns a list of lists
    [content word, style word]. The maximum length is given by "maxnouns",
    by default 6. Content words are chosen from the nouns, style words are
    chosen from: the adjective(s) of the noun chunk (such as "the three red
    cars", or "a blue flying dragon") the noun belongs to, or if there is no
    adjective in it, then from the list of verbs found in the text.
    '''

    # load the model provided by spaCy
    nlp = spacy.load("en_core_web_sm")

    # prepocess the text
    doc = nlp(text)

    # for the list of nouns with their corresponding adjectives, we create an
    # empty list:
    nouns_adjectives = []

    # we find the verbs of thext. This list may be empty.
    verbs = [str(token.lemma_) for token in doc if token.pos_ == "VERB"]

    # and separate the noun chunks:
    chunks = [x.text for x in doc.noun_chunks]

    # in order to find the nouns, and try to match it with the corresponing
    # adjective (or a verb from the text), we run a for loop over the noun
    # chunks:
    for ch in chunks:
        # prepocess the noun chunk:
        chd = nlp(ch)

        #f find the noun(s) in it:
        nouns = [str(token) for token in chd if token.pos_ == "NOUN"]

        # if we have found at least 1:
        if len(nouns):

            # we find the adjectives (this list may be empty)
            adjectives = [str(token) for token in chd if token.pos_ == "ADJ"]

            # for each noun found, we match it with word with "noun_adj"
            # and we append the result to nouns_adjectives
            for n in nouns:
                noun = n
                adj = noun_adj(adjectives, verbs)
                nouns_adjectives.append([noun, adj])

    # nouns_adjectives may be empty, or may be too long.
    # in case it has more than "maxnouns" elements, we randomly delete some
    # elements until it has the desired length:
    while len(nouns_adjectives) > maxnouns:
        del nouns_adjectives[random.randint(1,len(nouns_adjectives)-2)]

    # end return it.
    return nouns_adjectives
