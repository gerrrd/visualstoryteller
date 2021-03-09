import requests
import random
import os

class StyleImg():

    per_page = 30

    base_uri = 'https://api.unsplash.com'
    endpoint_style = '/topics/textures-patterns/photos'
    client_id = os.getenv('API_KEY')

    def __init__(self):
        pass

    def get_style(self):

        params = {
         'client_id': self.client_id,
         'per_page': self.per_page
        }

        response = requests.get(self.base_uri + self.endpoint_style, params=params)
        json_file = response.json()
        index = random.randint(0, self.per_page-1)
        img_link = json_file[index]['urls']['small']
        author_profile = json_file[index]['user']['links']['html']
        author_name = json_file[index]['user']['name']

        return img_link, author_name, author_profile
