import unittest

from business_objects.record_genres_sql import RecordGenre
from tools import db_utils as dbu
from business_objects.record_album_sql import RecordAlbum
from business_objects.record_tracks_sql import RecordTrack


class RecordTracksTest(unittest.TestCase):
    test_album_name = 'Test Album'
    test_record_album = None
    test_track_name = 'Test Track'
    test_track_number = 1
    test_update_track_name = 'Updated Track'
    test_update_track_number = 2
    test_record_genre = None
    test_update_record_genre = None

    def setUp(self):
        RecordAlbum.delete_by_name(self.test_album_name)
        RecordGenre.delete_by_name('Test Genre')
        RecordGenre.delete_by_name('Updated Genre')
        self.test_record_album = RecordAlbum.create(album_name=self.test_album_name, release_date='2021-01-01')
        self.test_record_genre = RecordGenre.create(genre_name='Test Genre', genre_description='Test Description')
        self.test_update_record_genre = RecordGenre.create(genre_name='Updated Genre',
                                                           genre_description='Updated Description')

    def tearDown(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_tracks WHERE album_id = %(album_id)s "
                delete_data = {'album_id': self.test_record_album.album_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

        self.test_record_album.delete()
        self.test_record_genre.delete()
        self.test_update_record_genre.delete()

    def test_read_all(self):
        record_tracks = RecordTrack.read_all()
        self.assertGreaterEqual(len(record_tracks), 1)

    def test_read(self):
        record_track = RecordTrack.read_all()[0]
        test_record = RecordTrack.read(record_track.track_id)
        self.assertIsNotNone(record_track)
        self.assertEqual(record_track.track_id, test_record.track_id)
        self.assertEqual(record_track.album_id, test_record.album_id)
        self.assertEqual(record_track.track_name, test_record.track_name)
        self.assertEqual(record_track.track_number, test_record.track_number)
        self.assertEqual(record_track.genre_id, test_record.genre_id)
        test_record = RecordTrack.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_name(self):
        record_track = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name,
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        print(f'record_track: {record_track}')
        test_record = RecordTrack.read_by_name(self.test_record_album.album_name, record_track.track_name)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_track.track_id, test_record.track_id)
        self.assertEqual(record_track.album_id, test_record.album_id)
        self.assertEqual(record_track.track_name, test_record.track_name)
        self.assertEqual(record_track.track_number, test_record.track_number)
        self.assertEqual(record_track.genre_id, test_record.genre_id)
        test_record = RecordTrack.read_by_name('_______Not a track_______', '_______Not a track_______')
        self.assertIsNone(test_record)

    def test_create(self):
        record_track = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name,
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        self.assertIsNotNone(record_track)
        self.assertIsNotNone(record_track.track_id)
        self.assertEqual(self.test_record_album.album_id, record_track.album_id)
        self.assertEqual(self.test_track_name, record_track.track_name)
        self.assertEqual(self.test_track_number, record_track.track_number)
        self.assertEqual(self.test_record_genre.genre_id, record_track.genre_id)

    def test_create_by_name(self):
        record_track = RecordTrack.create_by_name(album_name=self.test_record_album.album_name,
                                                  track_name=self.test_track_name,
                                                  track_number=self.test_track_number,
                                                  genre_name=self.test_record_genre.genre_name)
        self.assertIsNotNone(record_track)
        self.assertIsNotNone(record_track.track_id)
        self.assertEqual(self.test_record_album.album_id, record_track.album_id)
        self.assertEqual(self.test_track_name, record_track.track_name)
        self.assertEqual(self.test_track_number, record_track.track_number)
        self.assertEqual(self.test_record_genre.genre_id, record_track.genre_id)

    def test_update(self):
        record_track = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name,
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        record_track.track_name = self.test_update_track_name
        record_track.track_number = self.test_update_track_number
        record_track.genre_id = self.test_update_record_genre.genre_id
        record_track.update()
        test_record = RecordTrack.read(record_track.track_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_track.track_id, test_record.track_id)
        self.assertEqual(record_track.album_id, test_record.album_id)
        self.assertEqual(record_track.track_name, test_record.track_name)
        self.assertEqual(record_track.track_number, test_record.track_number)
        self.assertEqual(record_track.genre_id, test_record.genre_id)

    def test_delete(self):
        record_track = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name,
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        record_track.delete()
        test_record = RecordTrack.read(record_track.track_id)
        self.assertIsNone(test_record)

    def test_delete_by_id(self):
        record_track = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name,
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        RecordTrack.delete_by_id(record_track.track_id)
        test_record = RecordTrack.read(record_track.track_id)
        self.assertIsNone(test_record)

    def test_delete_all_from_album_id(self):
        record_track_1 = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name +' 1',
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        record_track_2 = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name +' 2',
                                          track_number=self.test_track_number + 1,
                                          genre_id=self.test_record_genre.genre_id)
        RecordTrack.delete_all_from_album_id(self.test_record_album.album_id)
        test_record = RecordTrack.read(record_track_1.track_id)
        self.assertIsNone(test_record)
        test_record = RecordTrack.read(record_track_2.track_id)
        self.assertIsNone(test_record)

    def test_delete_track_from_album(self):
        record_track_1 = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name + ' 1',
                                          track_number=self.test_track_number,
                                          genre_id=self.test_record_genre.genre_id)
        record_track_2 = RecordTrack.create(album_id=self.test_record_album.album_id,
                                          track_name=self.test_track_name + ' 2',
                                          track_number=self.test_track_number + 1,
                                          genre_id=self.test_record_genre.genre_id)
        RecordTrack.delete_track_from_albumn(self.test_record_album.album_id, record_track_1.track_id)
        test_record = RecordTrack.read(record_track_1.track_id)
        self.assertIsNone(test_record)
        test_record = RecordTrack.read(record_track_2.track_id)
        self.assertIsNotNone(test_record)