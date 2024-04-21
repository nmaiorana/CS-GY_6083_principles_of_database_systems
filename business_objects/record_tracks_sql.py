# Using MySQL Connector to create a class to represent the record_tracks table in the database. The RecordTrack class will
# be used to interact with the database and hold the information for a record_tracks table data.

import dataclasses
from tools import db_utils as dbu

from business_objects.record_genres_sql import RecordGenre


@dataclasses.dataclass
class RecordTrack:
    track_id: int
    album_id: int
    track_name: str
    track_number: int
    genre_id: int

    @staticmethod
    def create(album_id: int, track_name: str, track_number: int, genre_id: int) -> 'RecordTrack':
        add_track = ("INSERT INTO record_tracks "
                     "(album_id, track_name, track_number, genre_id) "
                     "VALUES (%s, %s, %s, %s)")
        data_track = (album_id, track_name, track_number, genre_id)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_track, data_track)
                conn.commit()
                track_id = cur.lastrowid
        return RecordTrack.read(track_id)

    @staticmethod
    def create_by_name(album_name: str, track_name: str, track_number: int, genre_name: str) -> 'RecordTrack':
        add_track = ("INSERT INTO record_tracks "
                     "(album_id, track_name, track_number, genre_id) "
                     "VALUES ((SELECT album_id FROM record_albums WHERE album_name = %s), %s, %s, "
                     "(SELECT genre_id FROM record_genres WHERE genre_name = %s))")
        data_track = (album_name, track_name, track_number, genre_name)
        print(f'Creating track: {data_track}')
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_track, data_track)
                conn.commit()
                track_id = cur.lastrowid

        print(f'Created track_id: {track_id}')
        return RecordTrack.read(track_id)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_tracks")
                for row in cursor.fetchall():
                    rows.append(RecordTrack(row[0], row[1], row[2], row[3], row[4]))
                return rows

    @staticmethod
    def read(track_id: int) -> 'RecordTrack':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_tracks WHERE track_id = {track_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordTrack(result[0], result[1], result[2], result[3], result[4])

    @staticmethod
    def read_by_name(album_name: str, track_name: str) -> 'RecordTrack':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM record_tracks WHERE album_id = (SELECT album_id FROM record_albums WHERE album_name = '{album_name}') AND track_name = '{track_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordTrack(result[0], result[1], result[2], result[3], result[4])

    @staticmethod
    def read_all_by_album_id(album_id: int) -> list:
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_tracks WHERE album_id = {album_id}")
                record_tracks = []
                for result in cursor.fetchall():
                    record_tracks.append(RecordTrack(result[0], result[1], result[2], result[3], result[4]))
                return record_tracks

    @staticmethod
    def read_by_album_name(album_name: str) -> list:
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM record_tracks WHERE album_id = (SELECT album_id FROM record_albums WHERE album_name = '{album_name}')")
                record_tracks = []
                for result in cursor.fetchall():
                    record_tracks.append(RecordTrack(result[0], result[1], result[2], result[3], result[4]))
                return record_tracks

    @staticmethod
    def delete_by_id(track_id: int):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_tracks WHERE track_id = {track_id}"
                cursor.execute(delete_statement)
                conn.commit()

    @staticmethod
    def delete_by_name(album_name: str, track_name: str):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_tracks WHERE album_id = (SELECT album_id FROM record_albums WHERE album_name = '{album_name}') AND track_name = '{track_name}'"
                cursor.execute(delete_statement)
                conn.commit()

    @staticmethod
    def delete_all_from_album_id(album_id: int):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_tracks WHERE album_id = {album_id}"
                cursor.execute(delete_statement)
                conn.commit()

    @staticmethod
    def delete_track_from_albumn(album_id: int, track_id: int):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_tracks WHERE album_id = {album_id} AND track_id = {track_id}"
                cursor.execute(delete_statement)
                conn.commit()

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = (
                    f"UPDATE record_tracks "
                    f"SET album_id = {self.album_id}, track_name = '{self.track_name}', track_number = {self.track_number}, genre_id = {self.genre_id} "
                    f"WHERE track_id = {self.track_id}")
                cursor.execute(update_statement)
                conn.commit()

    def delete(self):
        print(f'Deleting track: {self}')
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_tracks WHERE track_id = {self.track_id}"
                cursor.execute(delete_statement)
                conn.commit()

    def genre_name(self) -> str:
        return RecordGenre.read(self.genre_id).genre_name
