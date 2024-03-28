# Using MySQL Connector to create a class to represent the record_genres table in the database. The RecordGenre class will
# be used to interact with the database and hold the information for a record_genres table data.

import dataclasses
from project.tools import db_utils as dbu


@dataclasses.dataclass
class RecordGenres:
    __tablename__ = 'record_genres'
    genre_id: int
    genre_name: str
    genre_description: str

    @staticmethod
    def create(genre_name, genre_description):
        add_genre = ("INSERT INTO record_genres "
                     "(genre_name, genre_description) "
                     "VALUES (%s, %s)")
        data_genre = (genre_name, genre_description)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_genre, data_genre)
                conn.commit()
        return RecordGenres.read_by_name(genre_name)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_genres")
                for row in cursor.fetchall():
                    rows.append(RecordGenres(row[0], row[1], row[2]))
                return rows

    @staticmethod
    def read(genre_id):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_genres WHERE genre_id = {genre_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordGenres(result[0], result[1], result[2])

    @staticmethod
    def read_by_name(genre_name):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_genres WHERE genre_name = '{genre_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordGenres(result[0], result[1], result[2])

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = (
                    f"UPDATE record_genres "
                    f"SET genre_name = '{self.genre_name}', genre_description = '{self.genre_description}' "
                    f"WHERE genre_id = {self.genre_id}"
                )
                cursor.execute(update_statement)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_genres WHERE genre_id = {self.genre_id}"
                cursor.execute(delete_statement)
                conn.commit()

    def delete_by_name(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_genres WHERE genre_name = '{self.genre_name}'"
                cursor.execute(delete_statement)
                conn.commit()
