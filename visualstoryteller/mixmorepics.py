# visualstoryteller/getmorepics.py
# The class "GetStylePicss" is implemented. It loads the content and style
# images, does the stylization, and saves the output images.
# Tensorflow's natural style transfer is used to to stylize the images.
# The train model magenta_arbitrary-image-stylization-v1-256_2 is loaded.

import os
import tensorflow as tf
import tensorflow_hub as hub
from visualstoryteller.mixutils import load_image, load_content_image

# where the trained and optimized model is saved.
hub_handle_source = '/'.join([os.path.dirname(os.getcwd()),
    'visualstoryteller/data/magenta_arbitrary-image-stylization-v1-256_2'])

class GetStylePics():
    '''
    The class that handles all content and style images, the style transfer
    and saving the images.
    '''
    def __init__(self, output_image_size=384,
                 style_image_size=(256, 256),
                 hub_handle=hub_handle_source):
        self.content_image = None
        self.style_image = None
        self.stylized_image = None
        self.content_image_size = (output_image_size, output_image_size)
        self.output_image_size = output_image_size
        self.style_image_size = style_image_size
        self.hub_handle = hub_handle
        return None

    # loads the image given in content_url and style_url, returns None
    def load_images(self, content_image_url, style_image_url):
        '''
        Given lists "content_image_url" and "style_image_url", it loads the
        corresponing picutes and saves them in two lists: "self.content_image"
        and "self.style_image".
        It returns None.
        '''

        # content and stlye images are saved in a list of Tensorflow tensors
        self.content_image = []
        self.style_image = []

        # for each pair of content and styel URLs, we load the images.
        for content, style in zip(content_image_url, style_image_url):
            contentimage = load_content_image(content, self.content_image_size)
            self.content_image.append(contentimage)
            styleimage = tf.nn.avg_pool(load_image(style, self.style_image_size), ksize=[3,3], strides=[1,1], padding='SAME')
            self.style_image.append(styleimage)
        return None

    # stylize the image
    def stylize(self):
        '''
        When images have already been loaded, content images are stylized by
        the style images. This function loads the model from Tensorflow Hub
        and creates the stylized images.
        It returns self.
        '''

        # loading the model
        hub_module = hub.load(self.hub_handle)

        # stylized images are saved in a list of tensors. Images can be accessed
        # self.stylized_image[image_number][0].
        self.stylized_image = []
        for i in range(len(self.content_image)):
            self.stylized_image.append(hub_module(self.content_image[i], self.style_image[i])[0]) # 0, as more images can be done at the same time
        return self

    # returns the picture as array, returns self.
    def get_pics():
        '''
        It returns the picture as array, returns self.
        '''
        return self.stylized_image

    def save_jpgs(self, filename='output.jpg'):
        '''
        It saves the already generated stylized images and returns the names
        of the files. Filename may end with ".jpg", but works without, as well.
        '''

        # list of filenames to return
        fnames = []

        # cut .jpg if given:
        if filename[-4:].lower() == '.jpg':
            filename = filename[:-4]

        # if there stylezed image(s), save it:
        if self.stylized_image is not None:
            for i in range(len(self.stylized_image)):

                # generate the files'name
                fname = f'{filename}_{i}.jpg'

                # append it to the list we return
                fnames.append(fname)

                # and save it.
                tf.keras.preprocessing.image.save_img(fname, self.stylized_image[i][0])
        # if it could be done, it returns None
        else:
            print("Stylized image has not been created yet.")
            return None

        return fnames
