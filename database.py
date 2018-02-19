from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.ext.declarative import declarative_base

from IndicoWp.config import Config


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class MySQLDatabaseAccess:

    _engine = None
    _session_maker = None

    @staticmethod
    def get_session():
        if MySQLDatabaseAccess._session_maker is None:
            MySQLDatabaseAccess._create_session_maker()

        return MySQLDatabaseAccess._session_maker()  # type: Session

    @staticmethod
    def create_database():
        Base = declarative_base()
        MySQLDatabaseAccess._create_engine()
        Base.metadata.create_all(MySQLDatabaseAccess._engine)

    @staticmethod
    def _create_session_maker():
        MySQLDatabaseAccess._create_engine()

        MySQLDatabaseAccess._session_maker = sessionmaker(bind=MySQLDatabaseAccess._engine)

    @staticmethod
    def _create_engine():
        config = Config.get_instance()
        username = config['MYSQL']['username']
        password = config['MYSQL']['password']
        host = config['MYSQL']['host']
        database = config['MYSQL']['database']

        engine_string = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            username,
            password,
            host,
            database
        )

        MySQLDatabaseAccess._engine = create_engine(engine_string)
