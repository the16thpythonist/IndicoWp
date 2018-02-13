from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine

from IndicoWp.database import MySQLDatabaseAccess

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


class IndicoBackupController:

    def __init__(self):
        self.session = MySQLDatabaseAccess.get_session()  # type: Session
