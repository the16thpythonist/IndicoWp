from IndicoWp.config import Config, PATH, PROJECT_PATH

import logging
import pathlib
import configparser
import json


class IndicoObservationController:

    def __init__(self):
        self.config = Config.get_instance()
        self.logger = logging.getLogger()

        self.path = pathlib.Path(PROJECT_PATH) / self.config['INDICO']['observe']
        self.observe = configparser.ConfigParser()
        self.observe.read(str(self.path))

        self.dict = {}
        self._load_observed_categories()

    def _load_observed_categories(self):
        for name in self.observe.keys():
            if name == 'DEFAULT':
                continue

            _dict = self.observe[name]
            url = _dict['url']
            key = _dict['key']
            category_list = json.loads(_dict['categories'])

            observation = IndicoObservation(
                name,
                category_list,
                url,
                key
            )

            self.dict[name] = observation

    def __getitem__(self, item):
        return self.dict[item]

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()


class IndicoObservation:

    def __init__(self, name, category_list, url, key):
        self.name = name
        self.categories = category_list
        self.url = url
        self.key = key
