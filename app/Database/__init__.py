from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

engine = create_engine(f'mysql+pymysql://{environ.get("username")}:{environ.get("password")}@{environ.get("host")}:'
                       f'{int(environ.get("db_port"))}/{environ.get("db")}', poolclass=NullPool)


class DatabaseSession:

    def __enter__(self):
        self.session = Session(engine)

        self.session.expire_on_commit = False

        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
