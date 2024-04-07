# Using MySQL Connector to create a class to represent the members_to_artists table in the database. The GroupMembers class will
# be used to interact with the database and hold the information for a members_to_artists table data.

import dataclasses
from tools import db_utils as dbu

from business_objects.group_members_sql import GroupMember
from business_objects.record_artists_sql import RecordArtist


@dataclasses.dataclass
class MembersToArtists:
    members_to_artists_id: int
    member_id: int
    artist_id: int
    member_from_date: str
    member_to_date: str

    @staticmethod
    def create(member_id: int, artist_id: int, member_from_date: str, member_to_date: str) -> 'MembersToArtists':
        add_member = ("INSERT INTO members_to_artists "
                      "(member_id, artist_id, member_from_date, member_to_date) "
                      "VALUES (%s, %s, %s, %s)")
        data_member = (member_id, artist_id, member_from_date, member_to_date)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_member, data_member)
                conn.commit()
                member_id = cur.lastrowid
        return MembersToArtists.read(member_id)

    @staticmethod
    def create_by_ref(member: GroupMember, artist: RecordArtist, member_from_date: str, member_to_date: str) -> 'MembersToArtists':
        return MembersToArtists.create(member.member_id, artist.artist_id, member_from_date, member_to_date)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM members_to_artists")
                for row in cursor.fetchall():
                    rows.append(MembersToArtists(row[0], row[1], row[2], row[3], row[4]))
                return rows

    @staticmethod
    def read(member_to_artists_id: int) -> 'MembersToArtists':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM members_to_artists WHERE members_to_artists_id = {member_to_artists_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return MembersToArtists(result[0], result[1], result[2], result[3], result[4])

    @staticmethod
    def read_members(artist_id: int) -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM members_to_artists WHERE artist_id = {artist_id}")
                for row in cursor.fetchall():
                    rows.append(MembersToArtists(row[0], row[1], row[2], row[3], row[4]))
                return rows

    @staticmethod
    def delete_by_artist_id(artist_id: int):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM members_to_artists WHERE artist_id = {artist_id}"
                cursor.execute(delete_statement)
                conn.commit()

    @staticmethod
    def delete_by_artist(artist: RecordArtist):
        MembersToArtists.delete_by_artist_id(artist.artist_id)

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = ("UPDATE members_to_artists "
                                    "SET member_id = %s, artist_id = %s, member_from_date = %s, member_to_date = %s "
                                    "WHERE members_to_artists_id = %s")
                data = (self.member_id, self.artist_id, self.member_from_date, self.member_to_date, self.members_to_artists_id)
                cursor.execute(update_statement, data)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM members_to_artists WHERE members_to_artists_id = %s"
                data = (self.members_to_artists_id,)
                cursor.execute(delete_statement, data)
                conn.commit()