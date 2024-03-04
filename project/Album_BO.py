# This will be the data access object for the album information.
from dataclasses import dataclass

# Path: project/album_information_object.py
# This class will hold the information for an album and provide methods to interact with the database.

import db_utils as dbu


# Create a class to hold the information for an album

@dataclass
class AlbumInformation:
    album_name: str
    artist: str
    release_date: str
    record_label: str
    genre: str

    def add_album(self):
        # Create a connection object
        conn = dbu.connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO record_album (album_name, artist, release_date, number_of_tracks, record_label, genre) VALUES ('{self.album_name}', '{self.artist}', '{self.release_date}', {self.number_of_tracks}, '{self.record_label}', '{self.genre}')")
        conn.commit()
        conn.close()

    def get_albums(self):
        # Create a connection object
        conn = dbu.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM record_album")
        albums = cursor.fetchall()
        conn.close()
        return albums
