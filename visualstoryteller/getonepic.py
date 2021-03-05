# gets one picture and returns a picture as array (plt)
from visualstoryteller.content import ContentImg
from visualstoryteller.style import StyleImg
from visualstoryteller.getwords import get_words
from visualstoryteller.mixpictures import ImageStyle
from tensorflow.keras.preprocessing.image import img_to_array
import nltk


def getonepic(text, show_originals=False, show_result=False, show_all=False,
              saveimage = False, savename = 'output.jpg'):
    '''
    parameters:
        text: string
        show_originals boolean
        show_result boolean
        show_all boolean
        saveimage boolean
        savename string
    '''


    nouns, verbs = get_words(text)

    contentimage=ContentImg()
    content_link, content_author_name, content_author_profile \
        = contentimage.get_content(nouns)

    styleimage=ContentImg()
    style_link, style_author_name, style_author_profile \
        = styleimage.get_content(verbs)

    mixing = ImageStyle()
    mixing.load_images(content_link, style_link)
    mixing.stylize()

    if show_all:
        mixing.show_all_images()

    if show_originals:
        mixing.show_originals()

    if show_result:
        mixing.show_stylized_image()

    toreturn = {
        'image': mixing.stylized_image,
        #'imagelist' : list(img_to_array(mixing.stylized_image)),
        'content': [content_link, content_author_name, content_author_profile],
        'style': [style_link, style_author_name, style_author_profile]
    }

    if saveimage:
        mixing.save_jpgs(savename)
        toreturn['saved'] = f"../api/{savename}"

    return toreturn
