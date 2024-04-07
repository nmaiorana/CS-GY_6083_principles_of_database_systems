import unittest
import tools.db_utils as dbu
from business_objects.record_album_sql import RecordAlbum
from business_objects.record_artists_sql import RecordArtist
from business_objects.record_genres_sql import RecordGenre
from business_objects.record_labels_sql import RecordLabel


class RecordAlbumsTest(unittest.TestCase):
    test_album_id = None
    test_album_name = 'Test Album'
    test_update_album_name = 'Updated Album'
    test_artist_name = 'Boston'
    test_record_genre_name = 'Rock'
    test_record_label_name = 'Columbia'
    test_record_artist = None
    test_record_genre = None
    test_record_label = None

    def setUp(self):
        self.test_record_artist = RecordArtist.read_by_name('Boston')
        self.test_record_genre = RecordGenre.read_by_name('Rock')
        self.test_record_label = RecordLabel.read_by_name('Columbia Records')
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_albums WHERE album_name = %(album_name)s "
                delete_data = {'album_name': self.test_album_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'album_name': self.test_update_album_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def tearDown(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_albums WHERE album_name = %(album_name)s "
                delete_data = {'album_name': self.test_album_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'album_name': self.test_update_album_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def test_read_all(self):
        record_albums = RecordAlbum.read_all()
        self.assertGreaterEqual(len(record_albums), 1)

    def test_read(self):
        record_album = RecordAlbum.read_all()[0]
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(record_album)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        test_record = RecordAlbum.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_name(self):
        record_album = RecordAlbum.read_all()[0]
        test_record = RecordAlbum.read_by_name(record_album.album_name)
        self.assertIsNotNone(record_album)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        test_record = RecordAlbum.read_by_name('_______Not an album_______')
        self.assertIsNone(test_record)

    def test_create(self):
        record_album = RecordAlbum.create(album_name=self.test_album_name, release_date='2021-01-01')
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        self.assertIsNone(test_record.artist_id)
        self.assertIsNone(test_record.genre_id)
        self.assertIsNone(test_record.record_label_id)

    def test_create_by_id(self):
        record_album = RecordAlbum.create_by_id(album_name=self.test_album_name, release_date='2021-01-01',
                                          artist_id=self.test_record_artist.artist_id,
                                          genre_id=self.test_record_genre.genre_id,
                                          record_label_id=self.test_record_label.record_label_id)
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        self.assertEqual(record_album.release_date, test_record.release_date)
        self.assertEqual(record_album.artist_id, test_record.artist_id)
        self.assertEqual(record_album.genre_id, test_record.genre_id)
        self.assertEqual(record_album.record_label_id, test_record.record_label_id)

    def test_create_by_name(self):
        record_album = RecordAlbum.create_by_name(album_name=self.test_album_name,
                                                  release_date='2021-01-01',
                                                  artist_name=self.test_record_artist.artist_name,
                                                  genre_name=self.test_record_genre.genre_name,
                                                  record_label_name=self.test_record_label.record_label_name)
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        self.assertEqual(record_album.release_date, test_record.release_date)
        self.assertEqual(record_album.artist_id, test_record.artist_id)
        self.assertEqual(record_album.genre_id, test_record.genre_id)
        self.assertEqual(record_album.record_label_id, test_record.record_label_id)

    def test_create_by_ref(self):
        record_album = RecordAlbum.create_by_ref(album_name=self.test_album_name,
                                                  release_date='2021-01-01',
                                                  artist=self.test_record_artist,
                                                  genre=self.test_record_genre,
                                                  label=self.test_record_label)
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        self.assertEqual(record_album.release_date, test_record.release_date)
        self.assertEqual(record_album.artist_id, test_record.artist_id)
        self.assertEqual(record_album.genre_id, test_record.genre_id)
        self.assertEqual(record_album.record_label_id, test_record.record_label_id)

    def test_delete_by_name(self):
        record_album = RecordAlbum.create(album_name=self.test_album_name, release_date='2021-01-01')
        test_record = RecordAlbum.read(record_album.album_id)
        RecordAlbum.delete_by_name(record_album.album_name)
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNone(test_record)

    def test_update(self):
        record_album = RecordAlbum.create(album_name=self.test_album_name, release_date='2021-01-01')
        record_album.album_name = self.test_update_album_name
        record_album.update()
        test_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_album.album_id, test_record.album_id)
        self.assertEqual(record_album.album_name, test_record.album_name)
        self.assertEqual(record_album.release_date, test_record.release_date)
        self.assertIsNone(test_record.artist_id)
        self.assertIsNone(test_record.genre_id)
        self.assertIsNone(test_record.record_label_id)

    def test_delete(self):
        record_album = RecordAlbum.create(album_name=self.test_album_name, release_date='2021-01-01')
        self.assertIsNotNone(record_album)
        record_album.delete()
        deleted_record = RecordAlbum.read(record_album.album_id)
        self.assertIsNone(deleted_record)
