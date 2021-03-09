import requests
import random
import os


class ContentImg():

    per_page = 200
    pixabay = 'https://pixabay.com/api/'
    # base_uri = 'https://api.unsplash.com'
    # endpoint_content = '/search/photos'
    # client_id = os.getenv('API_KEY')
    pixabay_id = os.getenv('PIXABAY_KEY')

    def __init__(self):
        pass


    def get_content(self, words):

        # params = {
        #  'client_id': self.client_id,
        #  'query': '-'.join(words),
        #  'per_page': self.per_page
        # }

        params = {
            'key': self.pixabay_id,
            'q': '+'.join(words),
            'image_type': 'photo',
            'safesearch': True,
            'per_page': self.per_page
        }

        response = requests.get(self.pixabay, params=params)
        json_file = response.json()
        if json_file['total'] > 0:
            length_results = len(json_file['hits'])
            index = random.randint(0, length_results - 1)
            img_link = json_file['hits'][index]['webformatURL']
            author_name = json_file['hits'][index]['user']
            return img_link, author_name, '' # empty as author_profile
        # else try unsplash
        per_page = 30
        base_uri = 'https://api.unsplash.com'
        endpoint_content = '/search/photos'
        client_id = os.getenv('API_KEY')
        params = {
             'client_id': client_id,
             'query': '-'.join(words),
             'per_page': per_page
            }

        response = requests.get(base_uri+endpoint_content, params=params)
        json_file = response.json()
        length_results = len(json_file['results'])
        if length_results > 0:
            index = random.randint(0, length_results - 1)
            img_link = json_file['results'][index]['urls']['small']
            author_profile = json_file['results'][index]['user']['links']['html']
            author_name = json_file['results'][index]['user']['name']
            return [img_link, author_name, author_profile]
        # else, in worst case:
        return "nothing", words[0], "nothing"
