# gets one picture and returns a picture as array (plt)
from visualstoryteller.content import ContentImg
from visualstoryteller.contentunsplash import ContentImgUnsplash
from visualstoryteller.getmorewords import get_more_words
from visualstoryteller.mixmorepics import GetStylePics

def getmorepics(text, saveimage=False, savename='output.jpg'):
    '''
    parameters:
        text: string
        show_originals boolean
        show_result boolean
        show_all boolean
        saveimage boolean
        savename string
    '''

    words = get_more_words(text)
    if words == []:
        return {'OK' : 0} # I couldn’t get any text out

    content_link = []
    content_author_name = []
    content_author_profile = []

    style_link = []
    style_author_name = []
    style_author_profile = []

    found_pics = True
    wrong_word = ''
    for w in words:
        if found_pics:
            forcontent = [w[0]]
            forstyle = [w[1]]

            contentimage = ContentImg()
            link, author_name, author_profile = contentimage.get_content(forcontent)
            content_link.append(link)
            content_author_name.append(author_name)
            content_author_profile.append(author_profile)
            if link == "nothing":
                found_pics = False
                # just the second return of get_content
                wrong_word = author_name
            else:
                styleimage = ContentImgUnsplash()
                link, author_name, author_profile = styleimage.get_content(forstyle)
                style_link.append(link)
                style_author_name.append(author_name)
                style_author_profile.append(author_profile)
                if link == "nothing":
                    found_pics = False
                    # just the second return of get_content
                    wrong_word = author_name

    # if we have the word but can't find a picture, return -1 and the
    # word we couldn’t find a picture for
    if not found_pics:
        return {'OK': -1, "wrong_word": wrong_word}

    mixing = GetStylePics()
    mixing.load_images(content_link, style_link)
    mixing.stylize()

    toreturn = {
        'OK': len(mixing.stylized_image),
        # 'image': mixing.stylized_image,
        'content': [content_link, content_author_name, content_author_profile],
        'style': [style_link, style_author_name, style_author_profile]
    }

    if saveimage:
        toreturn['saved'] = mixing.save_jpgs(savename)

    return toreturn
