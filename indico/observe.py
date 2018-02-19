from IndicoWp.config import Config, PATH
import logging
import pathlib
import configparser


class IndicoObservationController:

    def __init__(self):
        self.config = Config.get_instance()
        self.logger = logging.getLogger()

        self.path = pathlib.Path(PATH) / self.config['INDICO']['observe']
        self.observe = configparser.ConfigParser()
        self.observe.read(str(self.path))

        self.observed_categories = []
        self._load_observed_categories()

    def _load_observed_categories(self):
        for category in self.observe.keys():
            self.observed_categories.append(category)

    def all(self):
        return self.observed_categories
