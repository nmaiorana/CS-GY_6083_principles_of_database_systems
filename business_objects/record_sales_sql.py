# This will create a class to represent record_sales table in the database. The RecordSales class will be used to
# interact with the database and hold the information for a record_sales table data.

import dataclasses
from tools import db_utils as dbu


@dataclasses.dataclass
class RecordSales:
    sale_id: int
    album_id: int
    sale_date: str
    sale_quantity: int
    unit_sale_price: float

    @staticmethod
    def create(album_id: int, sale_date: str, sale_quantity: int, unit_sale_price: float) -> 'RecordSales':
        add_sale = ("INSERT INTO record_sales "
                    "(album_id, sale_date, sale_quantity, unit_sale_price) "
                    "VALUES (%s, %s, %s, %s)")
        data_sale = (album_id, sale_date, sale_quantity, unit_sale_price)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_sale, data_sale)
                conn.commit()
                sales_id = cur.lastrowid
        return RecordSales.read(sales_id)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_sales")
                for row in cursor.fetchall():
                    rows.append(RecordSales(row[0], row[1], row[2], row[3], row[4]))
                return rows

    @staticmethod
    def read(sale_id: int) -> 'RecordSales':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_sales WHERE sale_id = {sale_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordSales(result[0], result[1], result[2], result[3], result[4])

    @staticmethod
    def read_by_album_id(album_id: int) -> list:
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_sales WHERE album_id = {album_id}")
                record_sales = []
                for result in cursor.fetchall():
                    record_sales.append(RecordSales(result[0], result[1], result[2], result[3], result[4]))
                return record_sales

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = (
                    f"UPDATE record_sales "
                    f"SET album_id = {self.album_id}, sale_date = '{self.sale_date}', sale_quantity = {self.sale_quantity}, unit_sale_price = {self.unit_sale_price} "
                    f"WHERE sale_id = {self.sale_id}")
                cursor.execute(update_statement)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_sales WHERE sale_id = %(sale_id)s"
                delete_data = {'sale_id': self.sale_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()

