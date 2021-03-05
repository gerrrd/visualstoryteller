import streamlit as st
import time
import matplotlib.pyplot as plt
import requests
from PIL import Image

url = 'http://localhost:8000/image'

st.markdown('''

# *Artsy* Storyteller

Hey there!
I am an artifical intelligence that turns your text into an ✨*artsy*✨ image.

''')

text = st.text_input('Tell me something interesting:')

if st.button('Submit'):
    with st.spinner('I am generating your image...'):
        time.sleep(1)
    st.success('This is what I came up with:')

    params = {'text': text}

    result = requests.get(url, params=params).json()

    print(result)

    if result['OK'] != 0:
        jpeg = result['saved']
        image = Image.open(jpeg)
        st.image(image)

        #fig, ax = plt.subplots()
        #im = ax.imshow(result['image'])
        #plt.axis('off')
        #st.pyplot(fig)

        content_image = result['content'][0]
        content_author = result['content'][1]
        content_profile = result['content'][2]
        style_image = result['style'][0]
        style_author = result['style'][1]
        style_profile = result['style'][2]

        attribution = f"Photos by [{content_author}]({content_profile}) and \
            [{style_author}]({style_profile})"

        images_links = f"[Image 1]({content_image}) / [Image 2]({style_image})"

        st.markdown(attribution)
        st.markdown(images_links)

    else:
        st.markdown("I couldn’t get much out of your text ☹️ Tell me something else.")

st.markdown('''

Images from [Unsplash](https://unsplash.com/)

''')


