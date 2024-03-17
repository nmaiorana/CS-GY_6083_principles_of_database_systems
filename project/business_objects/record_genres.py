# Using sqlalchemy to create a class to represent the record_genres table in the database. The RecordGenre class will
# be used to interact with the database and hold the information for a record_genres table data.

from project.tools import db_utils as dbu
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

print(f'Connection string: {dbu.get_connection_string()}')
pengine = sa.create_engine(dbu.get_connection_string())

Base = declarative_base()

metadata = sa.MetaData()
metadata.reflect(dbu.engine, only=['record_genres'])


class RecordGenres(Base):
    __table__ = metadata.tables['record_genres']


if __name__ == '__main__':
    Session = sa.orm.sessionmaker(dbu.engine)
    session = Session()
    print(session.query(RecordGenres).all())
