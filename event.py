

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
        self.description = description,
        self.type = event_type



