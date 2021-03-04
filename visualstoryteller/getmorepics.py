# gets one picture and returns a picture as array (plt)
from visualstoryteller.content import ContentImg
from visualstoryteller.style import StyleImg
from visualstoryteller.getmorewords import get_more_words
from visualstoryteller.mixmorepics import GetStylePics
import nltk


def getmorepics(text, show_originals=False, show_result=False, show_all=False,
                saveimage=False, savename='output.jpg'):
    '''
    parameters:
        text: string
        show_originals boolean
        show_result boolean
        show_all boolean
        saveimage boolean
        savename string
    '''

    nouns, verbs = get_more_words(text)

    content_link = []
    content_author_name = []
    content_author_profile = []

    style_link = []
    style_author_name = []
    style_author_profile = []

    for i in range(len(nouns)):
        forcontent = nouns[i]
        forstyle = [verbs[2*i], verbs[2*i + 1]]

        contentimage = ContentImg()
        link, author_name, author_profile = contentimage.get_content(forcontent)
        content_link.append(link)
        content_author_name.append(author_name)
        content_author_profile.append(author_profile)

        styleimage = ContentImg()
        link, author_name, author_profile = contentimage.get_content(forstyle)
        style_link.append(link)
        style_author_name.append(author_name)
        style_author_profile.append(author_profile)

    mixing = GetStylePics()
    mixing.load_images(content_link, style_link)
    mixing.stylize()

    # if show_all:
    #     mixing.show_all_images()

    # if show_originals:
    #     mixing.show_originals()

    # if show_result:
    #     mixing.show_stylized_image()

    toreturn = {
        'image' : mixing.stylized_image,
        'content': [content_link, content_author_name, content_author_profile],
        'style' : [style_link, style_author_name, style_author_profile]
    }

    # if saveimage:
    #     mixing.save_jpgs(savename)
    #     toreturn['saved'] = savename

    return toreturn
