from IndicoWp.indico import IndicoEventRequestController, IndicoEventProcessor
from IndicoWp.indico.event import IndicoEvent

import pytest


@pytest.fixture()
def event_dict_basic(request):
    event_dict = {
        'creator': {
            'fullName': 'MUSTERMANN, Max',
            'id': '1',
            'affiliation': 'KIT'
        },
        'startDate': {
            'date': '2017-01-01',
            'time': '02:00:00'
        },
        'title': 'test',
        'description': 'testing',
        'type': 'seminar',
        'location': 'KIT',
        'address': 'Karlsruhe'
    }
    return event_dict


@pytest.fixture()
def event_processor(request):
    processor = IndicoEventProcessor()
    return processor


@pytest.fixture()
def event_requester(request):
    requester = IndicoEventRequestController()
    return requester


def test_indico_event_processing_basic(event_dict_basic, event_processor):
    event = event_processor.process(event_dict_basic)  # type: IndicoEvent

    assert event.creator.first_name == 'max'
    assert event.creator.last_name == 'mustermann'
    assert event.creator.id == 1

    assert event.datetime.hour == 2

    assert event.title == 'test'
    assert event.description == 'testing'
    assert event.type == 'seminar'

    assert event.location == 'KIT'
    assert event.address == 'Karlsruhe'


def test_indico_category_request_basic(event_requester):
    event_list = event_requester.get_category_events(384)
    assert isinstance(event_list, list)
    assert len(event_list) >= 1
    assert isinstance(event_list[0], IndicoEvent)
