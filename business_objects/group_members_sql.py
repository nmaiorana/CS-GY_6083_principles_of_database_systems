# Using MySQL Connector to create a class to represent the group_members table in the database. The GroupMember class will
# be used to interact with the database and hold the information for a group_members table data.

import dataclasses
from tools import db_utils as dbu


@dataclasses.dataclass
class GroupMember:
    member_id: int
    member_name: str
    member_country: str
    member_birthdate: str

    @staticmethod
    def create(member_name: str, member_country: str, member_birthdate: str) -> 'GroupMember':
        add_member = ("INSERT INTO group_members "
                      "(member_name, member_country, member_birthdate) "
                      "VALUES (%s, %s, %s)")
        data_member = (member_name, member_country, member_birthdate)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_member, data_member)
                conn.commit()
                member_id = cur.lastrowid
        return GroupMember.read(member_id)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM group_members")
                for row in cursor.fetchall():
                    rows.append(GroupMember(row[0], row[1], row[2], row[3]))
                return rows

    @staticmethod
    def read(member_id: int) -> 'GroupMember':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM group_members WHERE member_id = {member_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return GroupMember(result[0], result[1], result[2], result[3])

    @staticmethod
    def read_by_name(member_name: str) -> 'GroupMember':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM group_members WHERE member_name = '{member_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return GroupMember(result[0], result[1], result[2], result[3])

    @staticmethod
    def delete_by_name(member_name: str):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM group_members WHERE member_name = '{member_name}'"
                cursor.execute(delete_statement)
                conn.commit()

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = (
                    f"UPDATE group_members "
                    f"SET member_name = '{self.member_name}', member_country = '{self.member_country}', member_birthdate = '{self.member_birthdate}' "
                    f"WHERE member_id = {self.member_id}")
                cursor.execute(update_statement)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM group_members WHERE member_id = %(member_id)s"
                delete_data = {'member_id': self.member_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()