from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from IndicoWp.database import MySQLDatabaseAccess

from IndicoWp.config import Config, PROJECT_PATH

import logging
import pathlib
import json


Base = declarative_base()


class EventReference(Base):
    __tablename__ = 'event_reference'

    internal_id = Column(Integer, primary_key=True)
    indico_id = Column(Integer)
    wordpress_id = Column(Integer)


class ReferenceController:

    def __init__(self):
        self.session = MySQLDatabaseAccess.get_session()  # type: Session
        self.id_manager = IDManager()

    def close(self):
        self.id_manager.save()

    def insert_reference(self, internal_id, indico_id, wordpress_id):
        self.session.add(EventReference(
            internal_id=internal_id,
            indico_id=indico_id,
            wordpress_id=wordpress_id
        ))
        self.session.commit()

    def select_all(self):
        return self.session.query(EventReference)

    def event_from_indico_event(self, indico_event):
        # Replacing the indico id with the internal id generated by the id manager
        internal_id = self.id_manager.get()
        indico_event_copy = indico_event.copy()
        indico_event_copy.id = internal_id
        return indico_event_copy


class IDManager:

    def __init__(self):
        self.config = Config.get_instance()
        self.logger = logging.getLogger('IdManagement')

        self.path = pathlib.Path(PROJECT_PATH) / self.config['LOGGING']['ids']

        self.counter = None
        self.used = None
        self.load()

    def load(self):
        with self.path.open(mode='r') as file:
            content_dict = json.load(file)
            self.counter = content_dict['counter']
            self.used = content_dict['used']

    def save(self):
        with self.path.open(mode='w+') as file:
            content_dict = {
                'counter': self.counter,
                'used': self.used
            }
            json.dump(content_dict, file)

    def get(self):
        current_id = self.counter
        self.used.append(current_id)
        self.counter += 1
        return current_id
