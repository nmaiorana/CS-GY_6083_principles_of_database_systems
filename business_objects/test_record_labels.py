import unittest
from tools import db_utils as dbu
from business_objects.record_labels_sql import RecordLabel

test_label_name = 'Test Record Label'
test_update_label_name = 'Updated Record Label'


class RecordLabelsTest(unittest.TestCase):

    def setUp(cls):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_labels WHERE record_labels.record_label_name = %(label_name)s "
                delete_data = {'label_name': test_label_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'label_name': test_update_label_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def tearDown(cls):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_labels WHERE record_label_name = %(label_name)s "
                delete_data = {'label_name': test_label_name}
                cursor.execute(delete_statement, delete_data)
                delete_data = {'label_name': test_update_label_name}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

    def test_read_all(self):
        record_labels = RecordLabel.read_all()
        self.assertGreaterEqual(len(record_labels), 1)

    def test_read(self):
        record_label = RecordLabel.read_all()[1]
        test_record = RecordLabel.read(record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(record_label.record_label_id, test_record.record_label_id)
        self.assertEqual(record_label.record_label_name, test_record.record_label_name)
        test_record = RecordLabel.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_name(self):
        record_label = RecordLabel.read_all()[1]
        test_record = RecordLabel.read_by_name(record_label.record_label_name)
        self.assertIsNotNone(record_label)
        self.assertEqual(record_label.record_label_id, test_record.record_label_id)
        self.assertEqual(record_label.record_label_name, test_record.record_label_name)
        test_record = RecordLabel.read_by_name('_______Not a label_______')
        self.assertIsNone(test_record)

    def test_create(self):
        new_record_label = RecordLabel.create(record_label_name=test_label_name)
        self.assertIsNotNone(new_record_label)
        self.assertIsNotNone(new_record_label.record_label_id)
        self.assertEqual(test_label_name, new_record_label.record_label_name)
        record_label = RecordLabel.read(new_record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(new_record_label.record_label_name, record_label.record_label_name)

    def test_delete_by_name(self):
        new_record_label = RecordLabel.create(record_label_name=test_label_name)
        self.assertIsNotNone(new_record_label)
        self.assertIsNotNone(new_record_label.record_label_id)
        self.assertEqual(test_label_name, new_record_label.record_label_name)
        record_label = RecordLabel.read_by_name(test_label_name)
        self.assertIsNotNone(record_label)
        self.assertEqual(new_record_label.record_label_name, record_label.record_label_name)
        RecordLabel.delete_by_name(test_label_name)
        record_label = RecordLabel.read_by_name(test_label_name)
        self.assertIsNone(record_label)

    def test_update(self):
        new_record_label = RecordLabel.create(record_label_name=test_label_name)
        self.assertIsNotNone(new_record_label)
        self.assertIsNotNone(new_record_label.record_label_id)
        self.assertEqual(test_label_name, new_record_label.record_label_name)
        record_label = RecordLabel.read(new_record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(new_record_label.record_label_name, record_label.record_label_name)
        new_record_label.record_label_name = test_update_label_name
        new_record_label.update()
        record_label = RecordLabel.read(new_record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(new_record_label.record_label_name, record_label.record_label_name)
        self.assertNotEqual(test_label_name, record_label.record_label_name)
        self.assertEqual(test_update_label_name, record_label.record_label_name)

    def test_delete(self):
        new_record_label = RecordLabel.create(record_label_name=test_label_name)
        self.assertIsNotNone(new_record_label)
        self.assertIsNotNone(new_record_label.record_label_id)
        self.assertEqual(test_label_name, new_record_label.record_label_name)
        record_label = RecordLabel.read(new_record_label.record_label_id)
        self.assertIsNotNone(record_label)
        self.assertEqual(new_record_label.record_label_name, record_label.record_label_name)
        new_record_label.delete()
        record_label = RecordLabel.read(new_record_label.record_label_id)
        self.assertIsNone(record_label)

