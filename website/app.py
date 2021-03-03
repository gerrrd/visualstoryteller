import streamlit as st
import time
from visualstoryteller.getonepic import getonepic
import matplotlib.pyplot as plt
import nltk
nltk.download('word2vec_sample')
nltk.download('averaged_perceptron_tagger')

st.markdown('''

# Visual Storyteller

Hey there!
I am an artifical intelligence that turns your text into an image.

''')

text = st.text_input('Tell me something interesting:')

if st.button('Submit'):
    with st.spinner('I am generating your image...'):
        time.sleep(30)
    st.success('This is what I came up with:')

    result = getonepic(text, show_result=True)

    fig, ax = plt.subplots()
    im = ax.imshow(result['image'][0])
    plt.axis('off')
    st.pyplot(fig)

    content_author = result['content'][1]
    content_profile = result['content'][2]
    style_author = result['style'][1]
    style_profile = result['style'][2]

    attribution = f"Photos by [{content_author}]({content_profile}) and \
        [{style_author}]({style_profile})"

    st.markdown(attribution)

st.markdown('''

Images from [Unsplash](https://unsplash.com/)

''')
