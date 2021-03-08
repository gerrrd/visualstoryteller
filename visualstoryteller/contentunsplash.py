import requests
import random
import os


class ContentImgUnsplash():

    per_page = 30
    base_uri = 'https://api.unsplash.com'
    endpoint_content = '/search/photos'
    client_id = os.getenv('API_KEY')

    def __init__(self):
        pass

    def get_content(self, words):

        params = {
         'client_id': self.client_id,
         'query': '-'.join(words),
         'per_page': self.per_page
        }

        response = requests.get(self.base_uri+self.endpoint_content, params=params)
        json_file = response.json()
        length_results = len(json_file['results'])
        index = random.randint(0, length_results - 1)
        img_link = json_file['results'][index]['urls']['small']
        author_profile = json_file['results'][index]['user']['links']['html']
        author_name = json_file['results'][index]['user']['name']

        return img_link, author_name, author_profile
