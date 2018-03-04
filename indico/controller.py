from IndicoWp.indico.observe import IndicoObservationController, IndicoObservation
from IndicoWp.indico.indico import IndicoEventRequestController
from IndicoWp.indico.persistency import IndicoDatabaseController


class IndicoController:

    def __init__(self):
        self.database_controller = IndicoDatabaseController()
        self.request_controller = IndicoEventRequestController()
        self.observation_controller = IndicoObservationController()

    def observed_events(self):
        event_list = []
        for observation in self.observation_controller.values():  # type: IndicoObservation
            self.request_controller.set(observation)
            for category in observation.categories:
                event_list += self.request_controller.get_category_events(category)
        return event_list

    def insert_events(self, event_list):
        self.database_controller.insert_multiple_events(event_list)
