from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from IndicoWp.database import MySQLDatabaseAccess, get_or_create
from IndicoWp.indico.event import IndicoEvent

Base = declarative_base()


class Creator(Base):
    __tablename__ = 'creator'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    affiliation = Column(String(300))


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    starting = Column(DATETIME)
    location = Column(String(200))
    address = Column(String(200))
    description = Column(Text)
    type = Column(String(100))
    title = Column(String(100))
    creator_id = Column(Integer, ForeignKey('creator.id'))

    creator = relationship(Creator)


class IndicoDatabaseController:

    def __init__(self):
        self.session = MySQLDatabaseAccess.get_session()  # type: Session

    def insert_multiple_events(self, event_list):
        for event in event_list:  # type: IndicoEvent
            self.insert_event(event)

    def insert_event(self, event):
        creator_model = get_or_create(
            self.session,
            Creator,
            id=event.creator.id,
            first_name=event.creator.first_name,
            last_name=event.creator.last_name,
            affiliation=event.creator.affiliation
        )

        event_model = get_or_create(
            self.session,
            Event,
            id=event.id,
            starting=event.datetime,
            location=event.location,
            address=event.address,
            description=event.description,
            type=event.type,
            title=event.title,
            creator_id=event.creator.id,
            creator=creator_model
        )