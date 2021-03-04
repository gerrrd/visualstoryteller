import nltk
from nltk.tokenize import word_tokenize
import random
import gensim
from nltk.data import find
# from nltk.corpus import stopwords
import string
# TODO include joblib and load the model
# from sklearn.externals import joblib
# TODO we won't need download brown when we load the model
nltk.download('brown')


def get_more_words(text, maxnouns = 7):
    word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
    model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)

    # TODO pre train and here just to load the trained model
    # nltk_model_path = 'my_model_knn.pkl.pkl'
    # model = joblib.load(nltk_model_path)

    # we're not using it now:
    # stopWords = set(stopwords.words('english'))

    string.punctuation
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')

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
        if n[1].startswith('J'):
            verbs.append(n[0])
        if n[1].startswith('R'):
            verbs.append(n[0])

    original_nouns = nouns
    while len(nouns)>maxnouns:
        del nouns[random.randint(0,len(nouns)-1)]

    # TODO here we can implement a "return 0" for poor text
    if nouns == []:
        nouns = ['bear']

    # TODO here we can implement a "return 0" for poor text
    if verbs == []:
        verbs = ['fly', 'run', 'go']

    final_verbs = []

    while len(final_verbs) < 2 * len(nouns):
        for v in verbs:
            new_words = model.most_similar(positive=[v], topn = 4)[-3:-1]
            new_words2 = [s[0] for s in new_words]
            final_verbs = final_verbs + new_words2
        verbs = final_verbs

    very_final_verbs = []
    while len(very_final_verbs) < 2 * len(nouns):
        very_final_verbs.append(final_verbs.pop(random.randint(0,len(final_verbs)-1)))

    return original_nouns, very_final_verbs
