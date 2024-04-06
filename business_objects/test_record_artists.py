# This will create a test case for RecordArtists

import unittest
from tools import db_utils as dbu
from business_objects.record_artists_sql import RecordArtist

test_artist_name = 'Test Artist'
test_update_artist_name = 'Updated Artist'


class RecordArtistsTest(unittest.TestCase):
        def setUp(cls):
            with dbu.get_connector() as conn:
                with conn.cursor() as cursor:
                    delete_statement = "DELETE FROM record_artists WHERE artist_name = %(artist_name)s "
                    delete_data = {'artist_name': test_artist_name}
                    cursor.execute(delete_statement, delete_data)
                    delete_data = {'artist_name': test_update_artist_name}
                    cursor.execute(delete_statement, delete_data)
                    conn.commit()

        def tearDown(cls):
            with dbu.get_connector() as conn:
                with conn.cursor() as cursor:
                    delete_statement = "DELETE FROM record_artists WHERE artist_name = %(artist_name)s "
                    delete_data = {'artist_name': test_artist_name}
                    cursor.execute(delete_statement, delete_data)
                    delete_data = {'artist_name': test_update_artist_name}
                    cursor.execute(delete_statement, delete_data)
                    conn.commit()

        def test_read_all(self):
            record_artists = RecordArtist.read_all()
            self.assertGreaterEqual(len(record_artists), 1)

        def test_read(self):
            record_artist = RecordArtist.read_all()[1]
            test_record = RecordArtist.read(record_artist.artist_id)
            self.assertIsNotNone(record_artist)
            self.assertEqual(record_artist.artist_id, test_record.artist_id)
            self.assertEqual(record_artist.artist_name, test_record.artist_name)
            test_record = RecordArtist.read(-1)
            self.assertIsNone(test_record)

        def test_read_by_name(self):
            record_artist = RecordArtist.read_all()[1]
            test_record = RecordArtist.read_by_name(record_artist.artist_name)
            self.assertIsNotNone(record_artist)
            self.assertEqual(record_artist.artist_id, test_record.artist_id)
            self.assertEqual(record_artist.artist_name, test_record.artist_name)
            test_record = RecordArtist.read_by_name('_______Not an artist_______')
            self.assertIsNone(test_record)

        def test_create(self):
            record_artist = RecordArtist.create(artist_name='Test Artist')
            self.assertIsNotNone(record_artist)
            self.assertIsNotNone(record_artist.artist_id)