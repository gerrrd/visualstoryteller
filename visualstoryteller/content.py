# visualstoryteller/content.py
# ContentImg class implemented to fetch the link of a picture from pixabay.com
# or from unsplash.com given a list of words, using API requests.
# OTher APIs can be implemented to provide a wider range visual input and to
# minimize the case when no picture is found.

import requests
import random
import os

class ContentImg():
    '''
    A class to fetch pictures from pixabay.com, or if there is no picture
    available, it will fetch one from unsplash.com.
    '''

    # base parameters used for pixabay:
    per_page = 200
    pixabay = 'https://pixabay.com/api/'
    pixabay_id = os.getenv('PIXABAY_KEY')

    def __init__(self):
        pass


    def get_content(self, words):
        '''
        The function to fetch the pictures given a list of words.
        It will try to get them from pixabay.com, if it is not successful,
        then from unsplash.com It returns a touple: a link to the image,
        the author's name, and in case of unsplash.com, also a link to the
        author's profile. From pixabay, the last element is an empty string.
        If no picture could be found, it returns:
            "nothing", the first given word, "nothing"
        '''

        # the parameters used for pixabay:
        params = {
            'key': self.pixabay_id,
            'q': '+'.join(words),
            'image_type': 'photo',
            'safesearch': True,
            'per_page': self.per_page
        }

        # API request using the above defined parameters and the given "words"
        response = requests.get(self.pixabay, params=params)
        json_file = response.json()

        # return the touple if the response is not empty
        if json_file['total'] > 0:
            length_results = len(json_file['hits'])
            index = random.randint(0, length_results - 1)
            img_link = json_file['hits'][index]['webformatURL']
            author_name = json_file['hits'][index]['user']
            return img_link, author_name, '' # empty as author_profile

        # else try unsplash:

        # parameters for unsplash.com
        per_page = 30
        base_uri = 'https://api.unsplash.com'
        endpoint_content = '/search/photos'
        client_id = os.getenv('API_KEY')
        params = {
             'client_id': client_id,
             'query': '-'.join(words),
             'per_page': per_page
            }

        # API request with these parameters and "words"
        response = requests.get(base_uri+endpoint_content, params=params)
        json_file = response.json()
        length_results = len(json_file['results'])

        # return the touple if the response is not empty:
        if length_results > 0:
            index = random.randint(0, length_results - 1)
            img_link = json_file['results'][index]['urls']['small']
            author_profile = json_file['results'][index]['user']['links']['html']
            author_name = json_file['results'][index]['user']['name']
            return [img_link, author_name, author_profile]

        # else, in worst case:
        return "nothing", words[0], "nothing"
