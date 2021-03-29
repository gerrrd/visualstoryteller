# visualstoryteller/contentunsplash.py
# ContentImgUnsplash class implemented to fetch the link of a picture from
# unsplash.com given a list of words, using API requests.
# OTher APIs can be implemented to provide a wider range visual input and to
# minimize the case when no picture is found.

import requests
import random
import os

class ContentImgUnsplash():
    '''
    A class to fetch pictures from unsplash.com.
    '''

    # base parameters for unsplash.com:
    per_page = 30
    base_uri = 'https://api.unsplash.com'
    endpoint_content = '/search/photos'
    client_id = os.getenv('API_KEY')

    def __init__(self):
        pass

    def get_content(self, words):
        '''
        The function to fetch the pictures given a list of words.
        It will try to get them from unsplash.com.com. It returns a touple:
        a link to the image, the author's name, and a link to the author's
        profile.
        If no picture could be found, it returns:
            "nothing", the first given word, "nothing"
        '''

        # exact parameters for the API requests
        params = {
         'client_id': self.client_id,
         'query': '-'.join(words),
         'per_page': self.per_page
        }

        # API request using the above defined parameters and the given "words"
        response = requests.get(self.base_uri+self.endpoint_content, params=params)
        json_file = response.json()
        length_results = len(json_file['results'])

        # return the touple if the response is not empty
        if length_results > 0:
            index = random.randint(0, length_results - 1)
            img_link = json_file['results'][index]['urls']['small']
            author_profile = json_file['results'][index]['user']['links']['html']
            author_name = json_file['results'][index]['user']['name']
            return img_link, author_name, author_profile

        # else, in worst case:
        return "nothing", words[0], "nothing"
