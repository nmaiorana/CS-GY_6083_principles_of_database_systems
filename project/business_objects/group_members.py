# Using sqlalchemy to create a class to represent the group_members table in the database. The GroupMember class will
# be used to interact with the database and hold the information for a group_members table data.

from project.tools import db_utils as dbu
import sqlalchemy as sa

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()


@reg.mapped_as_dataclass
class GroupMembers:
    __tablename__ = 'group_members'
    member_id: int = mapped_column(init=False, primary_key=True)
    member_name: int = mapped_column(sa.String)

    @staticmethod
    def create(member_name):
        with dbu.get_session() as session:
            data_object = GroupMembers(member_name)
            session.add(data_object)
            session.commit()
            return data_object

    @staticmethod
    def read_all() -> list:
        with dbu.get_session() as session:
            data_list = session.query(GroupMembers).all()
            return data_list

    @staticmethod
    def read(member_id):
        with dbu.get_session() as session:
            data_object = session.query(GroupMembers).filter_by(member_id=member_id).first()
            return data_object

    @staticmethod
    def read_by_name(member_name):
        with dbu.get_session() as session:
            data_objects = session.query(GroupMembers).filter_by(member_name=member_name).all()
            return data_objects

    @staticmethod
    def update(data_object):
        with dbu.get_session() as session:
            data_object_to_update = session.query(GroupMembers).filter_by(member_id=data_object.member_id).first()
            data_object_to_update.member_name = data_object.member_name
            session.commit()
            return data_object_to_update

    @staticmethod
    def delete(member_id):
        with dbu.get_session() as session:
            session.query(GroupMembers).filter_by(member_id=member_id).delete()
            session.commit()

    @staticmethod
    def delete_by_name(member_name):
        with dbu.get_session() as session:
            session.query(GroupMembers).filter_by(member_name=member_name).delete()
            session.commit()
