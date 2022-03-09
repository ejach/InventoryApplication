from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app.Database.DatabaseConnector import DatabaseConnector

dbc = DatabaseConnector()

engine = create_engine(f'mysql+pymysql://{dbc.user}:{dbc.password}@{dbc.host}:{dbc.db_port}/{dbc.db}',
                       poolclass=NullPool)


class DatabaseSession:

    def __enter__(self):
        self.session = Session(engine)

        self.session.expire_on_commit = False

        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
