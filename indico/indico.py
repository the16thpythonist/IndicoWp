import IndicoWp.config as config
import IndicoWp.indico.event as event
import logging

import requests
import json
import urllib.parse as urlparse


# TODO: Make this better with making a response dict a current item and a dict query


class IndicoEventRequestController:
    """
    :ivar config: The config parser object for the project
    :ivar logger: The logger for 'IndicoRequest'
    :ivar base_url: The url of the indico website which is to be used for the program
    :ivar api_key: The api key to be used to identify the requests to the api of the site
    :ivar processor: The IndicoEventProcessor, that turns the dict structures containing the infos about the events
        into the Event objects
    """
    def __init__(self):
        self.config = config.Config.get_instance()
        self.logger = logging.getLogger('IndicoRequest')

        self.base_url = None
        self.api_key = None

        self.processor = IndicoEventProcessor()

    def set(self, observation):
        self.base_url = observation.url
        self.api_key = observation.key

    def set_url(self, base_url):
        self.base_url = base_url

    def set_key(self, key):
        self.api_key = key

    def get_category_events(self, category_id):
        """
        A list of Event objects for each event in the category given by its id.

        :param category_id: The id of the indico category for which to get the events
        :return: [event.Event]
        """
        if self.base_url is None:
            raise ValueError('no base url set for IndicoEventRequestController')

        response_dict = self.request_category(category_id)

        event_dict_list = response_dict['results']
        event_list = []
        for event_dict in event_dict_list:
            indico_event = self.processor.process(event_dict)
            event_list.append(indico_event)

        return event_list

    def request_category(self, category_id):
        """
        Sends a request for the given category id and returns the json decoded dict structure of the response

        :param category_id: The id of the indico category for which to get the events
        :return: dict
        """
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

        print(url)

        response = requests.get(url)
        response_dict = json.loads(response.text)
        return response_dict


class IndicoEventProcessor:
    """
    :ivar dict: The dict object containing the info about the event, that is being processed by the object at a given
        moment in time. Is being changed with each new event to process
    :ivar logger: The logger for IndicoProcessing
    :cvar _DEBUG_STRING_CHARACTER_COUNT: In case a item is missing in the processed dict a log entry is being made and
        to identify to which event the log message belonged, a string of the dict that is processed is being appended
        this variable specifies how many characters to use of that string
    """
    _DEBUG_STRING_CHARACTER_COUNT = 30

    def __init__(self):
        self.dict = None
        self.logger = logging.getLogger('IndicoProcessing')

    def process(self, event_dict):
        """
        Processes the given event dict into a event.Event object and returns that

        :param event_dict: The dict structure, that contains the event data
        :return: Event
        """
        self.dict = event_dict

        return self._event()

    def _event(self):
        """
        Creates the actual Event object from all the parameter objects

        :return: Event
        """
        return event.IndicoEvent(
            self._event_id(),
            self._event_description(),
            self._event_location(),
            self._event_time(),
            self._event_creator(),
            self._event_meta()
        )

    def _event_id(self):
        """
        The indico id for the event

        :return: the int id
        """
        return int(self._query_dict('id', 0))

    def _event_description(self):
        """
        Creates the EventDescription from the currently processed dict

        :return: EventDescription
        """
        description = self._query_dict('description', '')
        title = self._query_dict('title', '')
        event_type = self._query_dict('type', '')

        event_description = event.EventDescription(title, description, event_type)
        return event_description

    def _event_creator(self):
        """
        Created the EventCreator from the currently processed dict

        :return: EventCreator
        """
        creator_full_name = self._query_dict('creator/fullName', '')
        if not creator_full_name == '':
            creator_name_split = creator_full_name.split(',')
            creator_first_name = creator_name_split[1].replace(' ', '').lower()
            creator_last_name = creator_name_split[0].replace(' ', '').lower()
        else:
            creator_first_name = ''
            creator_last_name = ''
        creator_id = int(self._query_dict('creator/id', 0))
        creator_affiliation = self._query_dict('creator/affiliation', '')

        event_creator = event.EventCreator(creator_id, creator_first_name, creator_last_name, creator_affiliation)
        return event_creator

    def _event_time(self):
        """
        Created the EventTime object from the currently processed dict

        :return: EventTime
        """
        date = self._query_dict('startDate/date', '')
        time = self._query_dict('startDate/time', '')

        event_time = event.EventTime(time, date)
        return event_time

    def _creation_time(self):
        date = self._query_dict('creationDate/date', '')
        time = self._query_dict('creationDate/time', '')
        if '.' in time:
            time = time[:time.find('.')]

        event_time = event.EventTime(time, date)
        return event_time

    def _event_meta(self):
        creation_time = self._creation_time()
        url = self._query_dict('url', '')

        event_meta = event.EventMeta(url, creation_time)
        return event_meta

    def _event_location(self):
        """
        Created the EventLocation object from the dict.

        :return: EventLocation
        """
        location = self._query_dict('location', None)
        address = self._query_dict('address', None)

        event_location = event.EventLocation(location, address)
        return event_location

    def _query_dict(self, dict_query, default):
        """
        Uses a single string to perform a possibly multi layer get from the currently processed string. The keys for
        the dict structures have to be separated by '/' to indicate, that they are intended for the next layer.
        A default value has to be given in case the query fails.
        If the query fails a debug entry is added to the log file.

        :param dict_query: The string query for the dict
        :param default: The default value to be returned in case the query fails
        :return: The value in the deepest dict layer queried
        """
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
        """
        The first few character of a string format of the dict currently processed for recognition in debugging the
        log files.
        The exact amount of characters that is used can be set by the static class variable
        '_DEBUG_STRING_CHARACTER_COUNT'

        :return: The string of the dict
        """
        dict_string = str(self.dict)
        # Only taking the first few characters, the amount specified by the static field
        if len(dict_string) > self._DEBUG_STRING_CHARACTER_COUNT:
            dict_string = dict_string[self._DEBUG_STRING_CHARACTER_COUNT:]
        return dict_string
