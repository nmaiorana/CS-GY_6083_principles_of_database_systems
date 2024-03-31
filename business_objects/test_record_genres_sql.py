# This will create a test case for RecordGenres

import unittest
from tools import db_utils as dbu
from business_objects.record_genres_sql import RecordGenre

test_genre_name = 'Test Genre'
test_update_genre_name = 'Updated Genre'


class RecordGenresTest(unittest.TestCase):

    def tearDown(cls):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_genres WHERE genre_name = %(genre_name)s "
                delete_data = {'genre_name': test_genre_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'genre_name': test_update_genre_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def test_read_all(self):
        record_genres = RecordGenre.read_all()
        self.assertGreaterEqual(len(record_genres), 1)

    def test_read(self):
        record_genre = RecordGenre.read_all()[1]
        test_record = RecordGenre.read(record_genre.genre_id)
        self.assertIsNotNone(record_genre)
        self.assertEqual(record_genre.genre_id, test_record.genre_id)
        self.assertEqual(record_genre.genre_name, test_record.genre_name)
        self.assertEqual(record_genre.genre_description, test_record.genre_description)
        test_record = RecordGenre.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_name(self):
        record_genre = RecordGenre.read_all()[1]
        test_record = RecordGenre.read_by_name(record_genre.genre_name)
        self.assertIsNotNone(record_genre)
        self.assertEqual(record_genre.genre_id, test_record.genre_id)
        self.assertEqual(record_genre.genre_name, test_record.genre_name)
        self.assertEqual(record_genre.genre_description, test_record.genre_description)
        test_record = RecordGenre.read_by_name('_______Not a genre_______')
        self.assertIsNone(test_record)

    def test_create(self):
        record_genre = RecordGenre.create(genre_name='Test Genre', genre_description='A test genre')
        self.assertIsNotNone(record_genre)
        self.assertIsNotNone(record_genre.genre_id)
        self.assertEqual('Test Genre', record_genre.genre_name)
        self.assertEqual('A test genre', record_genre.genre_description)
        record_genre = RecordGenre.read(record_genre.genre_id)
        self.assertIsNotNone(record_genre)
        self.assertEqual('Test Genre', record_genre.genre_name)
        self.assertEqual('A test genre', record_genre.genre_description)

    def test_update(self):
        record_genre = RecordGenre.create(genre_name='Test Genre', genre_description='A test genre')
        record_genre.genre_name = 'Updated Genre'
        record_genre.update()
        updated_record = RecordGenre.read(record_genre.genre_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(record_genre.genre_id, updated_record.genre_id)
        self.assertEqual(record_genre.genre_name, updated_record.genre_name)
        self.assertEqual(record_genre.genre_description, updated_record.genre_description)

    def test_delete(self):
        record_genre = RecordGenre.create(genre_name='Test Genre', genre_description='A test genre')
        record_genre.delete()
        deleted_record = RecordGenre.read(record_genre.genre_id)
        self.assertIsNone(deleted_record)

    def test_delete_by_name(self):
        record_genre = RecordGenre.create(genre_name='Test Genre', genre_description='A test genre')
        record_genre.delete_by_name()
        deleted_record = RecordGenre.read(record_genre.genre_id)
        self.assertIsNone(deleted_record)
