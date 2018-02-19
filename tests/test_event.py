from IndicoWp.indico.event import EventCreator, EventTime, EventLocation, EventDescription, IndicoEvent

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

    event = IndicoEvent(event_description, event_location, event_time, event_creator)
    return event


def test_event_object_basic(event):
    assert event.description == 'testing'
    assert event.title == 'test'
    assert event.type == 'seminar'
    assert event.location == 'KIT'
    assert event.address == 'Karlsruhe'
    assert event.creator.first_name == 'Max'
    assert event.creator.last_name == 'Mustermann'
    assert event.creator.affiliation == 'KIT'
    assert event.creator.id == 1
    assert event.datetime.hour == 2
