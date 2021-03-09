import functools
import os

import tensorflow as tf
import tensorflow_hub as hub
from visualstoryteller.mixutils import crop_center, load_image, load_local_image, show_n, save_image, load_content_image


#hub_handle_source = '/Users/ger/code/gerrrd/visualstoryteller/visualstoryteller/data/magenta_arbitrary-image-stylization-v1-256_2'
hub_handle_source = '/'.join([os.path.dirname(os.getcwd()),'visualstoryteller/data/magenta_arbitrary-image-stylization-v1-256_2'])
class ImageStyle():
    # intant... the model with the output and style image size, and the
    # trained neural netwrok (hub_handle), by default: arbitrary-image-stylization-v1-256
    # returs self
    def __init__(self, output_image_size = 384,
                 style_image_size = (256, 256),
                 hub_handle = hub_handle_source):
        self.content_image = None
        self.style_image = None
        self.stylized_image = None
        self.content_image_size = (output_image_size, output_image_size)
        self.output_image_size = output_image_size
        self.style_image_size = style_image_size
        self.hub_handle = hub_handle

        return None

    # loads the image given in content_url and style_url, return self
    def load_images(self, content_image_url, style_image_url):
        # self.content_image = load_image(content_image_url, self.content_image_size)
        # temp_file_name = 'output.jpg'
        # os.system(f'wget {link} --output-document={temp_file_name}')
        # self.content_image = load_local_image('output.jpg', self.content_image_size)
        # os.system(f'rm {temp_file_name}')
        self.content_image = load_content_image(content_image_url, self.content_image_size)
        self.style_image = tf.nn.avg_pool(load_image(style_image_url, self.style_image_size), ksize=[3,3], strides=[1,1], padding='SAME')
        return None

    # stylize the image
    def stylize(self):
        hub_module = hub.load(self.hub_handle)
        self.stylized_image = hub_module(self.content_image, self.style_image)[0] # 0, as more images can be done at the same time

    # prints the originals (plt.imshow)
    def show_originals(self):
        if (self.content_image != None) and (self.style_image != None):
            show_n([self.content_image, self.style_image], ['Content image', 'Style image'])
        else:
            print("Images have to be loaded first")

        return None

    # prints all 3 images (plt.imshow)
    def show_all_images(self):
        if self.stylized_image != None:
            show_n([self.content_image, self.style_image, self.stylized_image],
                   titles=['Original content image', 'Style image', 'Stylized image'])
        else:
            print("Images have to be loaded and compiled first.")

        return None

    def show_stylized_image(self):
        if self.stylized_image != None:
            show_n([self.stylized_image])
        else:
            print("Stylized image has not been created yet.")
        return None

    # returns the picture as array
    def get_pic():
        return self.stylized_image

    # saves the last
    # saves the last
    def save_jpgs(self, filename = 'output.jpg'):
        if self.stylized_image != None:
            tf.keras.preprocessing.image.save_img(filename, self.stylized_image[0])
            #save_image(self.stylized_image[0], 'data/'+filename)
        else:
            print("Stylized image has not been created yet.")
        return None
