# visualstoryteller/mixutils.py
# functions to load pictures, crop them and save them are implemented.
# copied from Tensorflow's documentation and examples. Some have been slightly
# changed/adapted.

# necessary imports for the image and file operations
import functools
import os
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pylab as plt
import tensorflow as tf

# @title Define image loading and visualization functions  { display-mode: "form" }

def crop_center(image):
  """Returns a cropped square image. Returns the image."""
  shape = image.shape
  new_shape = min(shape[1], shape[2])
  offset_y = max(shape[1] - shape[2], 0) // 2
  offset_x = max(shape[2] - shape[1], 0) // 2
  image = tf.image.crop_to_bounding_box(
      image, offset_y, offset_x, new_shape, new_shape)
  return image

@functools.lru_cache(maxsize=None)
def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
  """Loads and preprocesses images. Returns the image."""
  # Cache image file locally.
  image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
  # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
  img = plt.imread(image_path).astype(np.float32)[np.newaxis, ...]
  if img.max() > 1.0:
    img = img / 255.
  if len(img.shape) == 3:
    img = tf.stack([img, img, img], axis=-1)
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

@functools.lru_cache(maxsize=None)
def load_content_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
  """Loads and preprocesses images. Returns the image."""
  # Cache image file locally.
  # image loading has been changed to PIL.Image:
  r = requests.get(image_url)
  im = Image.open(BytesIO(r.content))
  # im.convert("RGB") is needed in some cases, when the returned picture is
  # black&white, and we may encounter dimensionality problems.
  img = np.array(im.convert("RGB")).reshape((im.size[1],im.size[0],3))
  if img.max() > 1.0:
    img = img / 255.
  if len(img.shape) == 3:
    img = np.expand_dims(img, axis = 0)
    # instead of:
    # img = tf.stack([img, img, img], axis=-1)
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

# It is not used in the application, but if we want to mix local images,
# this method can be used to load them (instied of an URL)
@functools.lru_cache(maxsize=None)
def load_local_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
  """Loads and preprocesses images from a local device. Returns the image."""
  # Cache image file locally.
  img = plt.imread(image_url).astype(np.float32)[np.newaxis, ...]
  if img.max() > 1.0:
    img = img / 255.
  if len(img.shape) == 3:
    img = tf.stack([img, img, img], axis=-1)
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

def save_image(img, file_name):
  '''Saves the image. Returns None.'''
  plt.imshow(img, aspect='equal')
  plt.axis('off')
  plt.savefig(file_name)
  return None
