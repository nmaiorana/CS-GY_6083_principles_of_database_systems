# This will create a test case for RecordGenres

# Path: project/business_objects/test_record_genres.py

import unittest
from business_objects.record_genres import RecordGenres


class RecordGenresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_read_all(self):
        record_genres = RecordGenres.read_all()
        self.assertGreaterEqual(len(record_genres), 1)

    def test_read(self):
        record_genre = RecordGenres.read_all()[1]
        test_record = RecordGenres.read(record_genre.genre_id)
        self.assertIsNotNone(record_genre)
        self.assertEqual(record_genre.genre_id, test_record.genre_id)
        self.assertEqual(record_genre.genre_name, test_record.genre_name)
        self.assertEqual(record_genre.genre_description, test_record.genre_description)

    def test_read_by_name(self):
        record_genre = RecordGenres.read_all()[1]
        test_record = RecordGenres.read_by_name(record_genre.genre_name)
        self.assertIsNotNone(record_genre)
        self.assertEqual(record_genre.genre_id, test_record[0].genre_id)
        self.assertEqual(record_genre.genre_name, test_record[0].genre_name)
        self.assertEqual(record_genre.genre_description, test_record[0].genre_description)

    def test_create(self):
        record_genre = RecordGenres.create(genre_name='Test Genre', genre_description='A test genre')
        self.assertIsNotNone(record_genre)
        self.assertIsNotNone(record_genre.genre_id)
        self.assertEqual('Test Genre', record_genre.genre_name)
        self.assertEqual('A test genre', record_genre.genre_description)
        record_genre = RecordGenres.read(record_genre.genre_id)
        self.assertIsNotNone(record_genre)
        self.assertEqual('Test Genre', record_genre.genre_name)
        self.assertEqual('A test genre', record_genre.genre_description)
        RecordGenres.delete(record_genre.genre_id)

    def test_update(self):
        record_genre = RecordGenres.create(genre_name='Test Genre', genre_description='A test genre')
        record_genre.genre_name = 'Updated Genre'
        RecordGenres.update(record_genre)
        updated_record = RecordGenres.read(record_genre.genre_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(record_genre.genre_id, updated_record.genre_id)
        self.assertEqual(record_genre.genre_name, updated_record.genre_name)
        self.assertEqual(record_genre.genre_description, updated_record.genre_description)
        RecordGenres.delete(updated_record.genre_id)

    def test_delete(self):
        record_genre = RecordGenres.create(genre_name='Test Genre', genre_description='A test genre')
        RecordGenres.delete(record_genre.genre_id)
        deleted_record = RecordGenres.read(record_genre.genre_id)
        self.assertIsNone(deleted_record)

    def test_delete_by_name(self):
        record_genre = RecordGenres.create(genre_name='Test Genre', genre_description='A test genre')
        RecordGenres.delete_by_name(record_genre.genre_name)
        deleted_record = RecordGenres.read(record_genre.genre_id)
        self.assertIsNone(deleted_record)
