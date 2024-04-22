# Using sqlalchemy to create a class to represent the record_albums table in the database. The RecordAlbum class will
# be used to interact with the database and hold the information for a record_albums table data.

import dataclasses
import tools.db_utils as dbu
from business_objects.record_artists_sql import RecordArtist
from business_objects.record_genres_sql import RecordGenre
from business_objects.record_labels_sql import RecordLabel
from business_objects.record_tracks_sql import RecordTrack


@dataclasses.dataclass
class RecordAlbum:
    album_id: int
    album_name: str
    release_date: str
    artist_id: int
    genre_id: int
    record_label_id: int

    @staticmethod
    def create(album_name: str, release_date: str) -> 'RecordAlbum':
        add_album = ("INSERT INTO record_albums "
                     "(album_name, release_date) "
                     "VALUES (%s, %s)")
        data_album = (album_name, release_date)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_album, data_album)
                conn.commit()
                album_id = cur.lastrowid
        return RecordAlbum.read(album_id)

    @staticmethod
    def create_by_id(album_name: str, release_date: str, artist_id: int, genre_id: int, record_label_id: int) -> 'RecordAlbum':
        add_album = ("INSERT INTO record_albums "
                     "(album_name, release_date, artist_id, genre_id, record_label_id) "
                     "VALUES (%s, %s, %s, %s, %s)")
        data_album = (album_name, release_date, artist_id, genre_id, record_label_id)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_album, data_album)
                conn.commit()
                album_id = cur.lastrowid
        return RecordAlbum.read(album_id)

    @staticmethod
    def create_by_ref(album_name: str, release_date: str, artist: RecordArtist, genre: RecordGenre, label: RecordLabel) -> 'RecordAlbum':
        return RecordAlbum.create_by_id(album_name, release_date, artist.artist_id, genre.genre_id, label.record_label_id)

    @staticmethod
    def create_by_name(album_name: str, release_date: str, artist_name: str, genre_name: str,
                       record_label_name: str) -> 'RecordAlbum':
        add_album = ("INSERT INTO record_albums "
                     "(album_name, release_date, artist_id, genre_id, record_label_id) "
                     "VALUES (%s, %s, (SELECT artist_id FROM record_artists WHERE artist_name = %s), "
                     "(SELECT genre_id FROM record_genres WHERE genre_name = %s), "
                     "(SELECT record_label_id FROM record_labels WHERE record_label_name = %s))")
        data_album = (album_name, release_date, artist_name, genre_name, record_label_name)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_album, data_album)
                conn.commit()
                album_id = cur.lastrowid
        return RecordAlbum.read(album_id)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_albums")
                for row in cursor.fetchall():
                    rows.append(RecordAlbum(row[0], row[1], row[2], row[3], row[4], row[5]))
                return rows

    @staticmethod
    def read(album_id: int) -> 'RecordAlbum':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_albums WHERE album_id = {album_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordAlbum(result[0], result[1], result[2], result[3], result[4], result[5])

    @staticmethod
    def read_by_name(album_name: str) -> 'RecordAlbum':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_albums WHERE album_name = '{album_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordAlbum(result[0], result[1], result[2], result[3], result[4], result[5])

    @staticmethod
    def delete_by_name(album_name: str):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_albums WHERE album_name = '{album_name}'"
                cursor.execute(delete_statement)
                conn.commit()

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = ("UPDATE record_albums "
                                    "SET album_name = %s, release_date = %s, artist_id = %s, genre_id = %s, record_label_id = %s "
                                    "WHERE album_id = %s")
                data_album = (
                self.album_name, self.release_date, self.artist_id, self.genre_id, self.record_label_id, self.album_id)
                cursor.execute(update_statement, data_album)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_albums WHERE album_id = %s"
                cursor.execute(delete_statement, (self.album_id,))
                conn.commit()

    def add_track(self, track_name: str, track_number: int, genre_name: str) -> RecordTrack:
        genre_id = RecordGenre.read_by_name(genre_name).genre_id
        return RecordTrack.create(self.album_id, track_name, track_number, genre_id)

    def remove_track(self, track_id: int):
        RecordTrack.delete_by_id(track_id)

    def get_tracks(self) -> list:
        return RecordTrack.read_all_by_album_id(self.album_id)

    def artist_name(self) -> str:
        return RecordArtist.read(self.artist_id).artist_name
    def genre_name(self) -> str:
        return RecordGenre.read(self.genre_id).genre_name

    def record_label_name(self) -> str:
        return RecordLabel.read(self.record_label_id).record_label_name

    def summary(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(f'select album_summary(%s)', (self.album_id,))
                return cur.fetchone()[0]
