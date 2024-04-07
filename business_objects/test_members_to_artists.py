import unittest
from tools import db_utils as dbu
from business_objects.record_artists_sql import RecordArtist
from business_objects.group_members_sql import GroupMember
from business_objects.members_to_artists_sql import MembersToArtists


class MembersToArtistsTest(unittest.TestCase):
    test_group_member = None
    test_record_artist = None
    test_member_to_artist = None

    def setUp(self):
        self.test_group_member = GroupMember.create('Test Member', 'USA', '2021-01-01')
        self.test_record_artist = RecordArtist.create('Test Artist')
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM members_to_artists WHERE artist_id = %(artist_id)s "
                delete_data = {'artist_id': self.test_record_artist.artist_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def tearDown(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM members_to_artists WHERE artist_id = %(artist_id)s "
                delete_data = {'artist_id': self.test_record_artist.artist_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()
        self.test_group_member.delete()
        self.test_record_artist.delete()

    def test_read_all(self):
        members_to_artists = MembersToArtists.read_all()
        self.assertGreaterEqual(len(members_to_artists), 1)

    def test_read(self):
        member_to_artist = MembersToArtists.read_all()[0]
        test_record = MembersToArtists.read(member_to_artist.members_to_artists_id)
        self.assertIsNotNone(member_to_artist)
        self.assertEqual(member_to_artist.members_to_artists_id, test_record.members_to_artists_id)
        self.assertEqual(member_to_artist.member_id, test_record.member_id)
        self.assertEqual(member_to_artist.artist_id, test_record.artist_id)
        self.assertEqual(member_to_artist.member_from_date, test_record.member_from_date)
        self.assertEqual(member_to_artist.member_to_date, test_record.member_to_date)
        test_record = MembersToArtists.read(-1)
        self.assertIsNone(test_record)

    def test_create(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        self.assertIsNotNone(member_to_artist)
        self.assertEqual(member_to_artist.member_id, self.test_group_member.member_id)
        self.assertEqual(member_to_artist.artist_id, self.test_record_artist.artist_id)
        self.assertEqual(member_to_artist.member_from_date.strftime('%Y-%m-%d'), '2021-01-01')
        self.assertEqual(member_to_artist.member_to_date.strftime('%Y-%m-%d'), '2021-12-31')

    def test_read_members(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        members = MembersToArtists.read_members(self.test_record_artist.artist_id)
        self.assertGreaterEqual(len(members), 1)
        self.assertEqual(members[0].member_id, self.test_group_member.member_id)
        self.assertEqual(members[0].artist_id, self.test_record_artist.artist_id)
        self.assertEqual(members[0].member_from_date.strftime('%Y-%m-%d'), '2021-01-01')
        self.assertEqual(members[0].member_to_date.strftime('%Y-%m-%d'), '2021-12-31')

    def test_delete(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        test_member_to_artist = MembersToArtists.read(member_to_artist.members_to_artists_id)
        test_member_to_artist.delete()
        test_member_to_artist = MembersToArtists.read(member_to_artist.members_to_artists_id)
        self.assertIsNone(test_member_to_artist)

    def test_delete_by_artist_id(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        MembersToArtists.delete_by_artist_id(self.test_record_artist.artist_id)
        test_member_to_artist = MembersToArtists.read(member_to_artist.members_to_artists_id)
        self.assertIsNone(test_member_to_artist)

    def test_delete_by_artist(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        MembersToArtists.delete_by_artist(self.test_record_artist)
        test_member_to_artist = MembersToArtists.read(member_to_artist.members_to_artists_id)
        self.assertIsNone(test_member_to_artist)

    def test_update(self):
        member_to_artist = MembersToArtists.create(self.test_group_member.member_id, self.test_record_artist.artist_id, '2021-01-01', '2021-12-31')
        member_to_artist.member_from_date = '2021-01-02'
        member_to_artist.member_to_date = '2021-12-30'
        member_to_artist.update()
        updated_member_to_artist = MembersToArtists.read(member_to_artist.members_to_artists_id)
        self.assertIsNotNone(updated_member_to_artist)
        self.assertEqual(member_to_artist.members_to_artists_id, updated_member_to_artist.members_to_artists_id)
        self.assertEqual(member_to_artist.member_id, updated_member_to_artist.member_id)
        self.assertEqual(member_to_artist.artist_id, updated_member_to_artist.artist_id)
        self.assertEqual(updated_member_to_artist.member_from_date.strftime('%Y-%m-%d'), '2021-01-02')
        self.assertEqual(updated_member_to_artist.member_to_date.strftime('%Y-%m-%d'), '2021-12-30')