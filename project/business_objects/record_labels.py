# Using sqlalchemy to create a class to represent the record_labels table in the database. The RecordLabels class will
# be used to interact with the database and hold the information for a record_labels table data.

from project.tools import db_utils as dbu
import sqlalchemy as sa

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()


@reg.mapped_as_dataclass
class RecordLabels:
    __tablename__ = 'record_labels'
    record_label_id: int = mapped_column(init=False, primary_key=True)
    record_label_name: str = mapped_column(sa.String)

    @staticmethod
    def create(record_label_name):
        with dbu.get_session() as session:
            data_object = RecordLabels(record_label_name)
            session.add(data_object)
            session.commit()
            return data_object

    @staticmethod
    def read_all() -> list:
        with dbu.get_session() as session:
            data_list = session.query(RecordLabels).all()
            return data_list

    @staticmethod
    def read(record_label_id):
        with dbu.get_session() as session:
            data_object = session.query(RecordLabels).filter_by(record_label_id=record_label_id).first()
            return data_object

    @staticmethod
    def read_by_name(record_label_name):
        with dbu.get_session() as session:
            data_objects = session.query(RecordLabels).filter_by(record_label_name=record_label_name).all()
            return data_objects

    @staticmethod
    def update(data_object):
        with dbu.get_session() as session:
            data_object_to_update = session.query(RecordLabels).filter_by(record_label_id=data_object.record_label_id).first()
            data_object_to_update.record_label_name = data_object.record_label_name
            session.commit()
            return data_object_to_update

    @staticmethod
    def delete(record_label_id):
        with dbu.get_session() as session:
            session.query(RecordLabels).filter_by(record_label_id=record_label_id).delete()
            session.commit()

    @staticmethod
    def delete_by_name(record_label_name):
        with dbu.get_session() as session:
            session.query(RecordLabels).filter_by(record_label_name=record_label_name).delete()
            session.commit()
