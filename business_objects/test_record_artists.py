# This will create a test case for RecordArtists

import unittest
from tools import db_utils as dbu
from business_objects.record_artists_sql import RecordArtist
from business_objects.group_members_sql import GroupMember
from business_objects.members_to_artists_sql import MembersToArtists

test_artist_name = 'Test Artist'
test_update_artist_name = 'Updated Artist'


class RecordArtistsTest(unittest.TestCase):
    test_group_member = None

    def setUp(cls):
        cls.test_group_member = GroupMember.create('Test Member', 'USA', '2021-01-01')
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
        cls.test_group_member.delete()

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

    def test_update(self):
        record_artist = RecordArtist.create(artist_name=test_artist_name)
        record_artist.artist_name = test_update_artist_name
        record_artist.update()
        test_record = RecordArtist.read(record_artist.artist_id)
        self.assertIsNotNone(test_record)
        self.assertEqual(record_artist.artist_id, test_record.artist_id)
        self.assertEqual(record_artist.artist_name, test_record.artist_name)
        self.assertEqual(test_record.artist_name, test_update_artist_name)

    def test_delete(self):
        record_artist = RecordArtist.create(artist_name=test_artist_name)
        record_artist.delete()
        test_record = RecordArtist.read(record_artist.artist_id)
        self.assertIsNone(test_record)

    def test_add_member(self):
        record_artist = RecordArtist.create(artist_name=test_artist_name)
        group_member = GroupMember.create('Test Member', 'USA', '2021-01-01')
        record_artist.add_member(group_member, '2021-01-01', '2021-12-31')
        test_record = RecordArtist.read(record_artist.artist_id)
        self.assertIsNotNone(test_record)
        test_members = test_record.members()
        self.assertEqual(len(test_members), 1)
        self.assertEqual(test_members[0].member_name, 'Test Member')
        self.assertEqual(test_members[0].from_date, '2021-01-01')
        self.assertEqual(test_members[0].to_date, '2021-12-31')
