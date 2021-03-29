# visualstoryteller/getmorepics.py
# the function "getmorepics" is implemented to fetch picures based on an input
# text. The input text is analyzed by "getmorewords", using spaCy, a very
# efficient NLP module. Having extracted the words from the input text, images
# are fetched by "ContentImg" and "ContentImgUnsplash" and they are mixed with
# "GetStylePics".

# import the classes and functions created for the project:
from visualstoryteller.content import ContentImg
from visualstoryteller.contentunsplash import ContentImgUnsplash
from visualstoryteller.getmorewords import get_more_words
from visualstoryteller.mixmorepics import GetStylePics

def getmorepics(text, saveimage=False, savename='output.jpg'):
    '''
    A function that, given an input text, analyzes it ("get_more_words"),
    fetched picures for the extracted words ("ContentImg" and
    "ContentImgUnsplash") and creates the mixed images by "GetStylePics".

    Parameters:
        text: a string, the input text
        saveimage: boolean, True if images should be saved
        savename: string, base name for the saved images. The ending ".jpg" is
            optional, it works with or without it.
            Images will be saved as jpgs.

    It returns a dictionary, depending on the successo of the operation:
        - if no words could be extracted from the text:
            {'OK' : 0}
        - if some words could be extracted from the text, but there was an
          empty API request:
            {'OK': -1, "wrong_word": wrong_word}
        - if we could fetch (and mix the) images:
            {
            'OK': number of images, between 1 and 6,
            'content': list with the information of the content images,
            'style': list with the information of the style images
            }
          by information of the images, we mean: link to the picture,
          author's name, link to their profile
    '''

    # extract the words by the function "get_more_words", which return a list
    # of lists: words for conent images, and words for style images.
    words = get_more_words(text)

    # if no words could be extracted, return a dictionary with 'OK': 0
    if words == []:
        return {'OK' : 0} # I couldn’t get any text out

    # if the list of words is not empty, we will try to fetch the images for
    # them, saving all related information in corresponing lists:
    content_link = []
    content_author_name = []
    content_author_profile = []

    style_link = []
    style_author_name = []
    style_author_profile = []

    # variable found pics to double check the search has been successful.
    # should one request give no usable answer, it is set to False and the case
    # is treated after the for loop. "wrong_word" will store the one that
    # caused the problem.
    found_pics = True
    wrong_word = ''

    # for loop to fetch the info:
    for w in words:

        # there was one empty answer, it will not use more API requests, just
        # ends the foor loop quickly and returns the necessary dictionary.
        # if that's not the case, looking for the next pictures:
        if found_pics:
            # separating the word(s) for the content image and the word(s) for
            # the style image
            forcontent = [w[0]]
            forstyle = [w[1]]

            # fetching the image by "ContentImg"
            contentimage = ContentImg()
            link, author_name, author_profile = contentimage.get_content(forcontent)

            # adding the returned info to the list of content images.
            # if the API request has not been successful, these variables are
            # still defined.
            content_link.append(link)
            content_author_name.append(author_name)
            content_author_profile.append(author_profile)

            # if "nothing" was returned, we set "found_pics" to False and save
            # the word that has caused it (2nd element of the returned touple)
            if link == "nothing":
                found_pics = False
                # just the second return of get_content
                wrong_word = author_name

            #else we'll look for the style image
            else:
                # by "ContentImgUnsplash"
                styleimage = ContentImgUnsplash()

                # adding the returned info the list of style images
                # if the API request has not been successful, these variables
                # are still defined.
                link, author_name, author_profile = styleimage.get_content(forstyle)
                style_link.append(link)
                style_author_name.append(author_name)
                style_author_profile.append(author_profile)

                # if "nothing" was returned, we set "found_pics" to False and
                # save the word that has caused it (2nd element of the
                # returned touple)
                if link == "nothing":
                    found_pics = False
                    # just the second return of get_content
                    wrong_word = author_name

    # if we have the word but can't find a picture, return -1 and the
    # word we couldn’t find a picture for
    if not found_pics:
        return {'OK': -1, "wrong_word": wrong_word}

    # having found the content and style images, we mix them by "GetStylePics"
    mixing = GetStylePics()
    mixing.load_images(content_link, style_link)
    mixing.stylize()

    # the dictionary to return
    # the part "image" is commented out, as in our application we are saving
    # the pictures and returning their names and links. If 3D numpy arrays
    # or tensors can be returned, it can be used.
    toreturn = {
        'OK': len(mixing.stylized_image),
        # 'image': mixing.stylized_image,
        'content': [content_link, content_author_name, content_author_profile],
        'style': [style_link, style_author_name, style_author_profile]
    }

    # if we save the images (saveimage == True), then we return also the names
    # of the images saved.
    if saveimage:
        toreturn['saved'] = mixing.save_jpgs(savename)

    return toreturn
