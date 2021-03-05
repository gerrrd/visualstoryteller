import streamlit as st
import time
import matplotlib.pyplot as plt
import requests
from PIL import Image

url = 'http://localhost:8000/image'

st.markdown('''

# Visual Storyteller

Hey there!
I am an artifical intelligence that turns your text into ✨**artsy**✨ images.

''')

text = st.text_input('Tell me something interesting:')

if st.button('Submit'):
    with st.spinner('I am generating your image...'):
        time.sleep(1)
    st.success('This is what I came up with:')

    params = {'text': text}

    result = requests.get(url, params=params).json()

    print(result)
    for i in range(len(result['saved'])):

        pic = result['saved'][i]
        content_image = result['content'][0][i]
        content_author = result['content'][1][i]
        content_profile = result['content'][2][i]
        style_image = result['style'][0][i]
        style_author = result['style'][1][i]
        style_profile = result['style'][2][i]

        image = Image.open(pic)
        st.image(image)

        attribution = f"Photos by [{content_author}]({content_profile}) and \
            [{style_author}]({style_profile})"

        images_links = f"[Image 1]({content_image}) / [Image 2]({style_image})"

        st.markdown(attribution)
        st.markdown(images_links)

    #fig, ax = plt.subplots()
    #im = ax.imshow(result['image'])
    #plt.axis('off')
    #st.pyplot(fig)

    # content_image = result['content'][0]
    # content_author = result['content'][1]
    # content_profile = result['content'][2]
    # style_image = result['style'][0]
    # style_author = result['style'][1]
    # style_profile = result['style'][2]

    # attribution = f"Photos by [{content_author}]({content_profile}) and \
    #     [{style_author}]({style_profile})"

    # images_links = f"[Image 1]({content_image}) / [Image 2]({style_image})"

    # st.markdown(attribution)
    # st.markdown(images_links)

st.markdown('''

Images from [Unsplash](https://unsplash.com/)

''')


