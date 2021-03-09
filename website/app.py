import streamlit as st
import time
import requests
from google.cloud import storage

url = 'http://localhost:8000/image'

st.markdown('''

# *Artsy* Storyteller

Hey there!
I am an artifical intelligence that turns your text into an ✨*artsy*✨ image.

''')

text = st.text_input('Tell me something interesting:')

if st.button('Submit'):
    with st.spinner('I am generating your images...'):

        # make a request to OUR api
        params = {'text': text}
        result = requests.get(url, params=params).json()

    # debugging check
    print(result)

    # check it response is empty
    if result['OK'] == 0:
        st.markdown("I couldn’t get much out of your text ☹️ Tell me something else.")

    # check if algorithm did not understand a word
    if result['OK'] == -1:
        word_error = f"I don't know the word {result['wrong_word']} 😬 Try again. "
        st.markdown(word_error)

    # display images
    elif result['OK'] > 0:
        with st.spinner('I am loading your images...'):
            n_images = result['OK']

            if n_images <= 3:
                cols13 = st.beta_columns(n_images)

                for i in range(n_images):
                    with cols13[i]:

                        st.image(result['im_urls'][i])
                        with st.beta_expander("See original picture"):
                            if result['content'][2][i] == '':
                                cont_attr = f"{result['content'][1][i]} / [Pixabay](https://pixabay.com/)"
                            else:
                                cont_attr = f"[{result['content'][1][i]}]({result['content'][2][i]}) / [Unsplash](https://unsplash.com/)"

                            st.image(result['content'][0][i], caption='content image')
                            st.markdwon(cont_attr)

                            style_attr = f"[{result['style'][1][i]}]({result['style'][2][i]}) / [Unsplash](https://unsplash.com/)"
                            st.image(result['style'][0][i], caption='style image')


            else:
                cols13 = st.beta_columns(3)
                cols46 = st.beta_columns(3)

                for i in range(3):
                    with cols13[i]:

                        st.image(result['im_urls'][i])
                        with st.beta_expander("See original picture"):
                            if result['content'][2][i] == '':
                                cont_attr = f"{result['content'][1][i]} / [Pixabay](https://pixabay.com/)"
                            else:
                                cont_attr = f"[{result['content'][1][i]}]({result['content'][2][i]}) / [Unsplash](https://unsplash.com/)"

                            st.image(result['content'][0][i], caption='content image')
                            st.markdwon(cont_attr)

                            style_attr = f"[{result['style'][1][i]}]({result['style'][2][i]}) / [Unsplash](https://unsplash.com/)"
                            st.image(result['style'][0][i], caption='style image')

                # not correct yet
                for i in range(3, n_images):
                    with cols46[i]:

                        st.image(result['im_urls'][i])
                        with st.beta_expander("See original picture"):
                            if result['content'][2][i] == '':
                                cont_attr = f"{result['content'][1][i]} / [Pixabay](https://pixabay.com/)"
                            else:
                                cont_attr = f"[{result['content'][1][i]}]({result['content'][2][i]}) / [Unsplash](https://unsplash.com/)"

                            st.image(result['content'][0][i], caption='content image')
                            st.markdwon(cont_attr)

                            style_attr = f"[{result['style'][1][i]}]({result['style'][2][i]}) / [Unsplash](https://unsplash.com/)"
                            st.image(result['style'][0][i], caption='style image')

        st.success('This is what I came up with:')

