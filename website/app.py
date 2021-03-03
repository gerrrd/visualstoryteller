import streamlit as st
import time


st.markdown('''

# Visual Storyteller

Hey there!
I am an artifical intelligence that turns your text into an image.

''')

text = st.text_input('Tell me something interesting:')

if st.button('Submit'):
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')

    st.image(
     "https://images.unsplash.com/photo-1537204696486-967f1b7198c8?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1534&q=80"
    )


st.markdown('''

Images from [Unsplash](https://unsplash.com/)

''')
