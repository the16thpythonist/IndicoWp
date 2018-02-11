import IndicoWp.config as config
import logging

import requests
import json
import urllib.parse as urlparse


class IndicoEventRequestController:

    def __init__(self):
        self.config = config.Config.get_instance()
        self.logger = logging.getLogger('IndicoRequest')

        self.base_url = self.config['INDICO']['url']
        self.api_key = self.config['INDICO']['api-key']

    def request_category(self, category_id):

        # Assembling the part of the url, that uses the category id
        category_string = '/categ/{}.json'.format(category_id)

        url_query = {
            'apikey': self.api_key
        }

        url = '{}/{}?{}'.format(
            self.base_url,
            category_string,
            urlparse.urlencode(url_query)
        )

        response = requests.request(url)
        response_dict = json.loads(response.text)


