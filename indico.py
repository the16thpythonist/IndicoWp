import IndicoWp.config as config
import IndicoWp.event as event
import logging

import requests
import json
import urllib.parse as urlparse


# TODO: Make this better with making a response dict a current item and a dict query


class IndicoEventRequestController:

    def __init__(self):
        self.config = config.Config.get_instance()
        self.logger = logging.getLogger('IndicoRequest')

        self.base_url = self.config['INDICO']['url']
        self.api_key = self.config['INDICO']['api-key']

        self.processor = IndicoEventProcessor()

    def get_category_events(self, category_id):
        response_dict = self.request_category(category_id)

        event_dict_list = response_dict['results']
        event_list = []
        for event_dict in event_dict_list:
            indico_event = self.processor.process(event_dict)
            event_list.append(indico_event)

        return event_list

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
        return response_dict


class IndicoEventProcessor:

    _DEBUG_STRING_CHARACTER_COUNT = 30

    def __init__(self):
        self.dict = None
        self.id = None
        self.logger = logging.getLogger('IndicoProcessing')

    def process(self, event_dict):
        self.dict = event_dict

        return self._event()

    def _event(self):
        return event.Event(
            self._event_description(),
            self._event_location(),
            self._event_time(),
            self._event_creator()
        )

    def _event_description(self):
        description = self._query_dict('description', '')
        title = self._query_dict('title', '')
        event_type = self._query_dict('type', '')

        event_description = event.EventDescription(title, description, event_type)
        return event_description

    def _event_creator(self):
        creator_full_name = self._query_dict('creator/fullName', '')
        if not creator_full_name == '':
            creator_name_split = creator_full_name.split(',')
            creator_first_name = creator_name_split[1].replace(' ', '').lower()
            creator_last_name = creator_name_split[0].replace(' ', '').lower()
        else:
            creator_first_name = ''
            creator_last_name = ''
        creator_id = int(self._query_dict('creator/id', 0))
        creator_affiliation = self._query_dict('creator/affiliation')

        event_creator = event.EventCreator(creator_id, creator_first_name, creator_last_name, creator_affiliation)
        return event_creator

    def _event_time(self):
        date = self._query_dict('startDate/date', '')
        time = self._query_dict('startDate/time', '')

        event_time = event.EventTime(time, date)
        return event_time

    def _event_location(self):
        location = self._query_dict('location', None)
        address = self._query_dict('address', None)

        event_location = event.EventLocation(location, address)
        return event_location

    def _query_dict(self, dict_query, default):
        try:
            keys = dict_query.split('/')
            current_dict = self.dict

            for key in keys:
                current_dict = current_dict[key]

            return current_dict
        except (KeyError, ValueError) as excpetion:
            self.logger.debug('There is no key "{}" in the event dict "{}..."'.format(
                dict_query,
                self._debug_string
            ))
            return default

    @property
    def _debug_string(self):
        dict_string = str(self.dict)
        # Only taking the first few characters, the amount specified by the static field
        dict_string = dict_string[self._DEBUG_STRING_CHARACTER_COUNT:]
        return dict_string
