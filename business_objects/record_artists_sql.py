# Using sqlalchemy to create a class to represent the record_artists table in the database. The RecordArtist class will
# be used to interact with the database and hold the information for a record_artists table data.

import dataclasses
import tools.db_utils as dbu


@dataclasses.dataclass
class RecordArtist:
    artist_id: int
    artist_name: str

    @staticmethod
    def create(artist_name):
        add_artist = ("INSERT INTO record_artists "
                      "(artist_name) "
                      "VALUES (%s)")
        data_artist = (artist_name,)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_artist, data_artist)
                conn.commit()
        return RecordArtist.read_by_name(artist_name)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_artists")
                for row in cursor.fetchall():
                    rows.append(RecordArtist(row[0], row[1]))
                return rows

    @staticmethod
    def read(artist_id):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_artists WHERE artist_id = {artist_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordArtist(result[0], result[1])

    @staticmethod
    def read_by_name(artist_name):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_artists WHERE artist_name = '{artist_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordArtist(result[0], result[1])

    @staticmethod
    def delete_by_name(artist_name):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_artists WHERE artist_name = '{artist_name}'"
                cursor.execute(delete_statement)
                conn.commit()

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = ("UPDATE record_artists "
                                    "SET artist_name = %s "
                                    "WHERE artist_id = %s")
                data = (self.artist_name, self.artist_id)
                cursor.execute(update_statement, data)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_artists WHERE artist_id = %s"
                data = (self.artist_id,)
                cursor.execute(delete_statement, data)
                conn.commit()
