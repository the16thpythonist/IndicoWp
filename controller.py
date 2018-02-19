from IndicoWp.wordpress import WordpressController
from IndicoWp.indico.controller import IndicoController
from IndicoWp.reference import ReferenceController


class Controller:

    def __init__(self):
        self.wordpress_controller = WordpressController()
        self.indico_controller = IndicoController()
        self.reference_controller = ReferenceController()

    def post_observed_events(self):
        # Getting all the observed events
        events = self.indico_controller.observed_events()
        # filter those already on the website
        references = self.reference_controller.select_all()
        reference_event_ids = list(map(lambda e: e.indico_id, references))

        events = list(filter(lambda e: e not in reference_event_ids, events))

        for event in events:
            # Actually posting the events to the website
            wordpress_id = self.wordpress_controller.post_event(event)
            # Adding a reference entry
            internal_event = self.reference_controller.event_from_indico_event(event)
            self.reference_controller.insert_reference(
                internal_event.id,
                event.id,
                wordpress_id
            )

    def close(self):
        self.reference_controller.close()