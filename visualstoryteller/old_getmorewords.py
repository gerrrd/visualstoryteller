import random
#import joblib
import os
# from nltk.corpus import stopwords
import string


def get_more_words(text, maxnouns = 7):

    # nltk_model_path = '/'.join([os.path.dirname(os.getcwd()),'visualstoryteller/data/nlp_model.pkl'])
    # model = joblib.load(nltk_model_path)

    # we're not using it now:
    # stopWords = set(stopwords.words('english'))

    string.punctuation
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')

    text = nltk.word_tokenize(text)
    #text = [word.lower() for word in text]

    text1 = nltk.pos_tag(text)

    nouns = []
    for n in text1:
        if n[1].startswith('N'):
            nouns.append(n[0])

    verbs = []
    for n in text1:
        if n[1].startswith('V'):
            verbs.append(n[0])
        if n[1].startswith('J'):
            verbs.append(n[0])
        if n[1].startswith('R'):
            verbs.append(n[0])

    original_nouns = nouns
    while len(nouns)>maxnouns:
        del nouns[random.randint(0,len(nouns)-1)]

    # TODO here we can implement a "return 0" for poor text
    if nouns == []:
        return 0, 0

    # TODO here we can implement a "return 0" for poor text
    if verbs == []:
        return 0, 0

    final_verbs = []

    while len(final_verbs) < 2 * len(nouns):
        for v in verbs:
            # new
            new_words2 = []
            if v in model.wv.vocab.keys():
                new_words = model.most_similar(positive=[v], topn = 4)[-3:-1]
                new_words2 = [s[0] for s in new_words]
            # new
            final_verbs = final_verbs + new_words2
        verbs = final_verbs

    very_final_verbs = []
    while len(very_final_verbs) < 2 * len(nouns):
        very_final_verbs.append(final_verbs.pop(random.randint(0,len(final_verbs)-1)))

    return original_nouns, very_final_verbs