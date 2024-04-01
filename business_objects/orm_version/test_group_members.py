# This will create a test case for GroupMembers

# Path: project/business_objects/test_group_members.py

import unittest
from business_objects.orm_version.group_members import GroupMembers


class GroupMembersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_read_all(self):
        group_members = GroupMembers.read_all()
        self.assertGreaterEqual(len(group_members), 1)

    def test_read(self):
        group_member = GroupMembers.read_all()[1]
        test_record = GroupMembers.read(group_member.member_id)
        self.assertIsNotNone(group_member)
        self.assertEqual(group_member.member_id, test_record.member_id)
        self.assertEqual(group_member.member_name, test_record.member_name)

    def test_read_by_name(self):
        group_member = GroupMembers.read_all()[1]
        test_record = GroupMembers.read_by_name(group_member.member_name)
        self.assertIsNotNone(group_member)
        self.assertEqual(group_member.member_id, test_record[0].member_id)
        self.assertEqual(group_member.member_name, test_record[0].member_name)

    def test_create(self):
        group_member = GroupMembers.create(member_name='Test Member')
        self.assertIsNotNone(group_member)
        self.assertIsNotNone(group_member.member_id)
        self.assertEqual('Test Member', group_member.member_name)
        group_member = GroupMembers.read(group_member.member_id)
        self.assertIsNotNone(group_member)
        self.assertEqual('Test Member', group_member.member_name)
        GroupMembers.delete(group_member.member_id)

    def test_update(self):
        group_member = GroupMembers.create(member_name='Test Member')
        group_member.member_name = 'Updated Member'
        GroupMembers.update(group_member)
        updated_record = GroupMembers.read(group_member.member_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(group_member.member_id, updated_record.member_id)
        self.assertEqual(group_member.member_name, updated_record.member_name)
        GroupMembers.delete(updated_record.member_id)

    def test_delete(self):
        group_member = GroupMembers.create(member_name='Test Member')
        GroupMembers.delete(group_member.member_id)
        deleted_record = GroupMembers.read(group_member.member_id)
        self.assertIsNone(deleted_record)

    def test_delete_by_name(self):
        group_member = GroupMembers.create(member_name='Test Member')
        GroupMembers.delete_by_name(group_member.member_name)
        deleted_record = GroupMembers.read(group_member.member_id)
        self.assertIsNone(deleted_record)
