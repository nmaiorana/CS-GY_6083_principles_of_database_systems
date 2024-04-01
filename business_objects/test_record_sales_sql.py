# This will create a testcase for RecordSales

import unittest
from tools import db_utils as dbu

from business_objects.record_sales_sql import RecordSales


class RecordSalesTest(unittest.TestCase):
    test_album_id = None
    test_album_name = 'Test Album'
    test_sale_id = None
    test_sale_date = '2021-01-01'
    test_sale_quantity = 10
    test_unit_sale_price = 10.00
    test_update_sale_quantity = 20
    test_update_unit_sale_price = 20.00

    def setUp(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                data = ((self.test_album_name,))
                select_statement = "SELECT * FROM record_albums WHERE album_name = (%s)"
                cursor.execute(select_statement, data)
                result = cursor.fetchone()
                if result is None or len(result) == 0:
                    insert_statement = ("INSERT INTO record_albums "
                                        "(album_name) "
                                        "VALUES (%s)")

                    cursor.execute(insert_statement, data)
                    conn.commit()
                    self.test_album_id = cursor.lastrowid
                else:
                    self.test_album_id = result[0]


    def tearDown(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                data = ((self.test_album_name,))
                select_statement = "SELECT * FROM record_albums WHERE album_name = (%s)"
                cursor.execute(select_statement, data)
                for result in cursor.fetchall():
                    test_album_id = result[0]
                    delete_statement = "DELETE FROM record_sales WHERE album_id = %(album_id)s "
                    delete_data = {'album_id': self.test_album_id}
                    cursor.execute(delete_statement, delete_data)
                    delete_statement = "DELETE FROM record_albums WHERE album_id = %(album_id)s "
                    delete_data = {'album_id': self.test_album_id}
                    cursor.execute(delete_statement, delete_data)
                conn.commit()

    def test_read_all(self):
        record_sales = RecordSales.read_all()
        self.assertGreaterEqual(len(record_sales), 1)

    def test_read(self):
        record_sale = RecordSales.read_all()[0]
        test_record = RecordSales.read(record_sale.sale_id)
        self.assertIsNotNone(record_sale)
        self.assertEqual(record_sale.sale_id, test_record.sale_id)
        self.assertEqual(record_sale.album_id, test_record.album_id)
        self.assertEqual(record_sale.sale_date, test_record.sale_date)
        self.assertEqual(record_sale.sale_quantity, test_record.sale_quantity)
        self.assertEqual(record_sale.unit_sale_price, test_record.unit_sale_price)
        test_record = RecordSales.read(-1)
        self.assertIsNone(test_record)

    def test_read_by_album_id(self):
        record_sale = RecordSales.read_all()[1]
        test_records = RecordSales.read_by_album_id(record_sale.album_id)
        self.assertGreater(len(test_records), 0)
        self.assertEqual(test_records[0].album_id, record_sale.album_id)
        self.assertEqual(test_records[-1].album_id, record_sale.album_id)

    def test_create(self):
        record_sale = RecordSales.create(album_id=self.test_album_id, sale_date=self.test_sale_date,
                                         sale_quantity=self.test_sale_quantity,
                                         unit_sale_price=self.test_unit_sale_price)
        self.assertIsNotNone(record_sale)
        self.assertIsNotNone(record_sale.sale_id)
        self.assertEqual(self.test_album_id, record_sale.album_id)
        self.assertEqual(self.test_sale_date, record_sale.sale_date.strftime('%Y-%m-%d'))
        self.assertEqual(self.test_sale_quantity, record_sale.sale_quantity)
        self.assertEqual(self.test_unit_sale_price, record_sale.unit_sale_price)
        record_sale = RecordSales.read(record_sale.sale_id)
        self.assertIsNotNone(record_sale)
        self.assertEqual(self.test_album_id, record_sale.album_id)
        self.assertEqual(self.test_sale_date, record_sale.sale_date.strftime('%Y-%m-%d'))
        self.assertEqual(self.test_sale_quantity, record_sale.sale_quantity)
        self.assertEqual(self.test_unit_sale_price, record_sale.unit_sale_price)

    def test_update(self):
        record_sale = RecordSales.create(album_id=self.test_album_id, sale_date=self.test_sale_date,
                                         sale_quantity=self.test_sale_quantity,
                                         unit_sale_price=self.test_unit_sale_price)
        record_sale.sale_quantity = self.test_update_sale_quantity
        record_sale.unit_sale_price = self.test_update_unit_sale_price
        record_sale.update()
        updated_record = RecordSales.read(record_sale.sale_id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(record_sale.sale_id, updated_record.sale_id)
        self.assertEqual(record_sale.album_id, updated_record.album_id)
        self.assertEqual(record_sale.sale_date, updated_record.sale_date)
        self.assertEqual(self.test_update_sale_quantity, updated_record.sale_quantity)
        self.assertEqual(self.test_update_unit_sale_price, updated_record.unit_sale_price)

    def test_delete(self):
        record_sale = RecordSales.create(album_id=self.test_album_id, sale_date=self.test_sale_date,
                                         sale_quantity=self.test_sale_quantity,
                                         unit_sale_price=self.test_unit_sale_price)
        record_sale.delete()
        deleted_record = RecordSales.read(record_sale.sale_id)
        self.assertIsNone(deleted_record)
