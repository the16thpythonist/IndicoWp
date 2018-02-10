

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