# This will create a test case for RecordArtists

# Path: project/business_objects/test_record_artists.py

import unittest
from business_objects.record_artists import RecordArtists


class RecordArtistsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_read_all(self):
        record_artists = RecordArtists.read_all()
        self.assertGreaterEqual(len(record_artists), 1)

    def test_read(self):
        record_artist = RecordArtists.read_all()[1]
        test_record = RecordArtists.read(record_artist.artist_id)
        self.assertIsNotNone(record_artist)
        self.assertEqual(record_artist.artist_id, test_record.artist_id)
        self.assertEqual(record_artist.artist_name, test_record.artist_name)

    def test_read_by_name(self):
        record_artist = RecordArtists.read_all()[1]
        test_record = RecordArtists.read_by_name(record_artist.artist_name)
        self.assertIsNotNone(record_artist)
        self.assertEqual(record_artist.artist_id, test_record[0].artist_id)
        self.assertEqual(record_artist.artist_name, test_record[0].artist_name)

    def test_create(self):
        record_artist = RecordArtists.create(artist_name='Test Artist')
        self.assertIsNotNone(record_artist)
        self.assertIsNotNone(record_artist.artist_id)
        self.assertEqual('Test Artist', record_artist.artist_name)
        record_artist = RecordArtists.read(record_artist.artist_id)
        self.assertIsNotNone(record_artist)
        self.assertEqual('Test Artist', record_artist.artist_name)
        RecordArtists.delete(record_artist.artist_id)

    def test_update(self):
        record_artist = RecordArtists.create(artist_name='Test Artist')
        record_artist.artist_name = 'Updated Artist'
        RecordArtists.update(record_artist)
        updated_record = RecordArtists.read(record_artist.artist_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(record_artist.artist_id, updated_record.artist_id)
        self.assertEqual(record_artist.artist_name, updated_record.artist_name)
        RecordArtists.delete(updated_record.artist_id)

    def test_delete(self):
        record_artist = RecordArtists.create(artist_name='Test Artist')
        RecordArtists.delete(record_artist.artist_id)
        deleted_record = RecordArtists.read(record_artist.artist_id)
        self.assertIsNone(deleted_record)

    def test_delete_by_name(self):
        record_artist = RecordArtists.create(artist_name='Test Artist')
        RecordArtists.delete_by_name(record_artist.artist_name)
        deleted_record = RecordArtists.read(record_artist.artist_id)
        self.assertIsNone(deleted_record)
