from IndicoWp.event import EventCreator, EventTime, EventLocation, EventDescription, Event

import pytest


@pytest.fixture()
def event(request):
    # Creating a normal EventCreator
    event_creator = EventCreator(1, 'Max', 'Mustermann', 'KIT')
    # Creating default time
    event_time = EventTime('02:00:00', '2020-01-01')
    # Creating default description
    event_description = EventDescription('test', 'testing', 'seminar')
    # Creating default Location
    event_location = EventLocation('KIT', 'Karlsruhe')

    event = Event(event_description, event_location, event_time, event_creator)
    return event
