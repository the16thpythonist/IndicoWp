import datetime


class EventLocation:
    """
    Parameter object, that represents the location of a Event and contains the string information about the location
    name and the address of the location.

    :ivar location: The string name of the location of the event
    :ivar address: The string of the address of the event
    """
    def __init__(self, location, address):
        self.location = location
        self.address = address


class EventCreator:
    """
    Parameter object, that represents the location of an Event and contains the information about the author of the
    Event on the indico platform, which includes the affiliation, id, first and last name.

    :ivar id: The string id of the author
    :ivar first_name: The string first name of the author
    :ivar last_name: The string last name of the author
    :ivar affiliation: The string info about the affiliation of the creator
    """
    def __init__(self, indico_id, first_name, last_name, affiliation):
        self.id = indico_id
        self.first_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation


class EventDescription:
    """
    Parameter object, that represents the description of an event and contains the inf about the title, description and
    type of event.

    :ivar title: The title of the event
    :ivar description: The string description of the event
    :ivar type: The string definition of what type of event it is
    """
    def __init__(self, title, description, event_type):
        self.title = title
        self.description = description
        self.type = event_type


class EventTime:
    """
    Parameter object, that represents the time of an event, including the date and time it is supposed to take place

    :ivar time: The string time of the event. Has to have the format:
        "hour:minutes:seconds"
    :ivar date: The string date of the event. Has to have the format:
        "year-month-day"
    """
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, time_string, date_string):
        self.time = time_string
        self.date = date_string

    @property
    def datetime(self):
        """
        Creates a new datetime object from the date and time string

        :return: datetime.datetime object for the time and date the event is supposed to take place
        """
        # Joining the string of the date and the time, so they match the format and can be converted to te datetime
        datetime_string = '{} {}'.format(self.date, self.time)

        datetime_object = datetime.datetime.strptime(datetime_string, self.DATETIME_FORMAT)
        return datetime_object


class EventMeta:

    def __init__(self, url, creation_time):
        self.url = url
        self.creation_time = creation_time


class IndicoEvent:
    """
    The data model for representing a Event of the indico website.
    It contains info about the description, type and title of the event, the location and address, the time it
    is supposed to take place and the event creator

    :ivar event_description: EventDescription object, containing the title, type and descritpion
    :ivar event_location: EventLocation containing the location name and the address
    :ivar event_time: EventTime containing starting time and date
    :ivar event_creator: EventCreator containing the creator name, id and affiliation
    """
    def __init__(self, indico_id, event_description, event_location, event_time, event_creator, event_meta):
        self.id = indico_id  # type: int
        self.event_description = event_description  # type: EventDescription
        self.event_location = event_location  # type: EventLocation
        self.event_time = event_time  # type: EventTime
        self.creator = event_creator  # type: EventCreator
        self.event_meta = event_meta  # type: EventMeta

    @property
    def url(self):
        return self.event_meta.url  # type: str

    @property
    def creation_time(self):
        return self.event_meta.creation_time  # type: EventTime

    @property
    def description(self):
        return self.event_description.description

    @property
    def type(self):
        return self.event_description.type

    @property
    def title(self):
        return self.event_description.title

    @property
    def location(self):
        return self.event_location.location

    @property
    def address(self):
        return self.event_location.address

    @property
    def datetime(self):
        return self.event_time.datetime

    @property
    def created(self):
        return self.creation_time.datetime

    def copy(self):
        event = IndicoEvent(
            self.id,
            self.event_description,
            self.event_location,
            self.event_time,
            self.creator,
            self.creation_time
        )
        return event
