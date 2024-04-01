# This will create a test case for RecordLabels

# Path: project/business_objects/test_record_labels.py

import unittest
from business_objects.orm_version.record_labels import RecordLabels


class RecordLabelsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_read_all(self):
        record_labels = RecordLabels.read_all()
        self.assertGreaterEqual(len(record_labels), 1)

    def test_read(self):
        record_label = RecordLabels.read_all()[1]
        test_record = RecordLabels.read(record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(record_label.record_label_id, test_record.record_label_id)
        self.assertEqual(record_label.record_label_name, test_record.record_label_name)

    def test_read_by_name(self):
        record_label = RecordLabels.read_all()[1]
        test_record = RecordLabels.read_by_name(record_label.record_label_name)
        self.assertIsNotNone(record_label)
        self.assertEqual(record_label.record_label_id, test_record[0].record_label_id)
        self.assertEqual(record_label.record_label_name, test_record[0].record_label_name)

    def test_create(self):
        record_label = RecordLabels.create(record_label_name='Test Label')
        self.assertIsNotNone(record_label)
        self.assertIsNotNone(record_label.record_label_id)
        self.assertEqual('Test Label', record_label.record_label_name)
        record_label = RecordLabels.read(record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual('Test Label', record_label.record_label_name)
        RecordLabels.delete(record_label.record_label_id)

    def test_update(self):
        record_label = RecordLabels.create(record_label_name='Test Label')
        record_label.record_label_name = 'Updated Label'
        RecordLabels.update(record_label)
        updated_record = RecordLabels.read(record_label.record_label_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(record_label.record_label_id, updated_record.record_label_id)
        self.assertEqual(record_label.record_label_name, updated_record.record_label_name)
        RecordLabels.delete(updated_record.record_label_id)

    def test_delete(self):
        record_label = RecordLabels.create(record_label_name='Test Label')
        RecordLabels.delete(record_label.record_label_id)
        deleted_record = RecordLabels.read(record_label.record_label_id)
        self.assertIsNone(deleted_record)

    def test_delete_by_name(self):
        record_label = RecordLabels.create(record_label_name='Test Label')
        RecordLabels.delete_by_name(record_label.record_label_name)
        deleted_record = RecordLabels.read(record_label.record_label_id)
        self.assertIsNone(deleted_record)
