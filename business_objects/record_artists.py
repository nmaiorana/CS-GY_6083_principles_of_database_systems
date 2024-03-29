# Using sqlalchemy to create a class to represent the record_artists table in the database. The RecordArtists class will
# be used to interact with the database and hold the information for a record_artists table data.

from tools import db_utils as dbu
import sqlalchemy as sa

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()


@reg.mapped_as_dataclass
class RecordArtists:
    __tablename__ = 'record_artists'
    artist_id: int = mapped_column(init=False, primary_key=True)
    artist_name: str = mapped_column(sa.String)

    @staticmethod
    def create(artist_name):
        with dbu.get_session() as session:
            data_object = RecordArtists(artist_name)
            session.add(data_object)
            session.commit()
            return data_object

    @staticmethod
    def read_all() -> list:
        with dbu.get_session() as session:
            data_list = session.query(RecordArtists).all()
            return data_list

    @staticmethod
    def read(artist_id):
        with dbu.get_session() as session:
            data_object = session.query(RecordArtists).filter_by(artist_id=artist_id).first()
            return data_object

    @staticmethod
    def read_by_name(artist_name):
        with dbu.get_session() as session:
            data_objects = session.query(RecordArtists).filter_by(artist_name=artist_name).all()
            return data_objects

    @staticmethod
    def update(data_object):
        with dbu.get_session() as session:
            data_object_to_update = session.query(RecordArtists).filter_by(artist_id=data_object.artist_id).first()
            data_object_to_update.artist_name = data_object.artist_name
            session.commit()
            return data_object_to_update

    @staticmethod
    def delete(artist_id):
        with dbu.get_session() as session:
            session.query(RecordArtists).filter_by(artist_id=artist_id).delete()
            session.commit()

    @staticmethod
    def delete_by_name(artist_name):
        with dbu.get_session() as session:
            session.query(RecordArtists).filter_by(artist_name=artist_name).delete()
            session.commit()
