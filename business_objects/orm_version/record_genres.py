# Using sqlalchemy to create a class to represent the record_genres table in the database. The RecordGenre class will
# be used to interact with the database and hold the information for a record_genres table data.

from tools import db_utils as dbu
import sqlalchemy as sa

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()


@reg.mapped_as_dataclass
class RecordGenres:
    __tablename__ = 'record_genres'
    genre_id: int = mapped_column(init=False, primary_key=True)
    genre_name: str = mapped_column(sa.String)
    genre_description: str = mapped_column(sa.String)

    @staticmethod
    def create(genre_name, genre_description):
        with dbu.get_session() as session:
            data_object = RecordGenres(genre_name, genre_description)
            session.add(data_object)
            session.commit()
            return data_object

    @staticmethod
    def read_all() -> list:
        with dbu.get_session() as session:
            data_list = session.query(RecordGenres).all()
            return data_list

    @staticmethod
    def read(genre_id):
        with dbu.get_session() as session:
            data_object = session.query(RecordGenres).filter_by(genre_id=genre_id).first()
            return data_object

    @staticmethod
    def read_by_name(genre_name):
        with dbu.get_session() as session:
            data_objects = session.query(RecordGenres).filter_by(genre_name=genre_name).all()
            return data_objects

    @staticmethod
    def update(data_object):
        with dbu.get_session() as session:
            data_object_to_update = session.query(RecordGenres).filter_by(genre_id=data_object.genre_id).first()
            data_object_to_update.genre_name = data_object.genre_name
            data_object_to_update.genre_description = data_object.genre_description
            session.commit()
            return data_object_to_update

    @staticmethod
    def delete(genre_id):
        with dbu.get_session() as session:
            session.query(RecordGenres).filter_by(genre_id=genre_id).delete()
            session.commit()

    @staticmethod
    def delete_by_name(genre_name):
        with dbu.get_session() as session:
            session.query(RecordGenres).filter_by(genre_name=genre_name).delete()
            session.commit()