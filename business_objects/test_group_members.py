import unittest
from tools import db_utils as dbu
from business_objects.group_members_sql import GroupMember


class GroupMembersTest(unittest.TestCase):
    test_member_name = 'Test Member'
    test_member_country = 'Test Country'
    test_member_birthdate = '2021-01-01'
    test_update_member_name = 'Updated Member'
    test_update_member_country = 'Updated Country'
    test_update_member_birthdate = '2021-02-02'

    def setUp(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM group_members WHERE member_name = %(member_name)s "
                delete_data = {'member_name': self.test_member_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'member_name': self.test_update_member_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def tearDown(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM group_members WHERE member_name = %(member_name)s "
                delete_data = {'member_name': self.test_member_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'member_name': self.test_update_member_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def test_read_all(self):
        group_members = GroupMember.read_all()
        self.assertGreaterEqual(len(group_members), 1)

    def test_read(self):
        group_member = GroupMember.read_all()[0]
        test_record = GroupMember.read(group_member.member_id)
        self.assertIsNotNone(group_member)
        self.assertEqual(group_member.member_id, test_record.member_id)
        self.assertEqual(group_member.member_name, test_record.member_name)
        self.assertEqual(group_member.member_country, test_record.member_country)
        self.assertEqual(group_member.member_birthdate, test_record.member_birthdate)
        test_record = GroupMember.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_name(self):
        group_member = GroupMember.read_all()[0]
        test_record = GroupMember.read_by_name(group_member.member_name)
        self.assertIsNotNone(group_member)
        self.assertEqual(group_member.member_id, test_record.member_id)
        self.assertEqual(group_member.member_name, test_record.member_name)
        self.assertEqual(group_member.member_country, test_record.member_country)
        self.assertEqual(group_member.member_birthdate, test_record.member_birthdate)
        test_record = GroupMember.read_by_name('_______Not a member_______')
        self.assertIsNone(test_record)

    def test_create(self):
        group_member = GroupMember.create(member_name=self.test_member_name, member_country=self.test_member_country,
                                          member_birthdate=self.test_member_birthdate)
        self.assertIsNotNone(group_member)
        self.assertIsNotNone(group_member.member_id)
        self.assertEqual(self.test_member_name, group_member.member_name)
        self.assertEqual(self.test_member_country, group_member.member_country)
        self.assertEqual(self.test_member_birthdate, group_member.member_birthdate.strftime('%Y-%m-%d'))
        group_member = GroupMember.read(group_member.member_id)
        self.assertIsNotNone(group_member)

    def test_update(self):
        group_member = GroupMember.create(member_name=self.test_member_name, member_country=self.test_member_country,
                                          member_birthdate=self.test_member_birthdate)
        group_member.member_name = self.test_update_member_name
        group_member.member_country = self.test_update_member_country
        group_member.member_birthdate = self.test_update_member_birthdate
        group_member.update()
        updated_member = GroupMember.read(group_member.member_id)
        self.assertIsNotNone(updated_member)
        self.assertEqual(self.test_update_member_name, updated_member.member_name)
        self.assertEqual(self.test_update_member_country, updated_member.member_country)
        self.assertEqual(self.test_update_member_birthdate, updated_member.member_birthdate.strftime('%Y-%m-%d'))

    def test_delete_by_name(self):
        group_member = GroupMember.create(member_name=self.test_member_name, member_country=self.test_member_country,
                                          member_birthdate=self.test_member_birthdate)
        self.assertIsNotNone(group_member)
        self.assertIsNotNone(group_member.member_id)
        self.assertEqual(self.test_member_name, group_member.member_name)
        record = GroupMember.read_by_name(self.test_member_name)
        self.assertIsNotNone(record)
        self.assertEqual(group_member.member_name, record.member_name)
        GroupMember.delete_by_name(self.test_member_name)
        record = GroupMember.read_by_name(self.test_member_name)
        self.assertIsNone(record)

    def test_delete(self):
        group_member = GroupMember.create(member_name=self.test_member_name, member_country=self.test_member_country,
                                          member_birthdate=self.test_member_birthdate)
        self.assertIsNotNone(group_member)
        self.assertIsNotNone(group_member.member_id)
        self.assertEqual(self.test_member_name, group_member.member_name)
        record = GroupMember.read(group_member.member_id)
        self.assertIsNotNone(record)
        self.assertEqual(group_member.member_name, record.member_name)
        group_member.delete()
        record = GroupMember.read(group_member.member_id)
        self.assertIsNone(record)
