# Using sqlalchemy to create a class to represent the record_labels table in the database. The RecordLabel class will
# be used to interact with the database and hold the information for a record_labels table data.

import dataclasses
import tools.db_utils as dbu


@dataclasses.dataclass
class RecordLabel:
    record_label_id: int
    record_label_name: str


    @staticmethod
    def create(record_label_name: str) -> 'RecordLabel':
        add_label = ("INSERT INTO record_labels "
                     "(record_label_name) "
                     "VALUES (%s)")
        data_label = (record_label_name,)
        with dbu.get_connector() as conn:
            with conn.cursor() as cur:
                cur.execute(add_label, data_label)
                conn.commit()
                record_label_id = cur.lastrowid
        return RecordLabel.read(record_label_id)

    @staticmethod
    def read_all() -> list:
        rows = []
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM record_labels")
                for row in cursor.fetchall():
                    rows.append(RecordLabel(row[0], row[1]))
                return rows

    @staticmethod
    def read(record_label_id: int) -> 'RecordLabel':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_labels WHERE record_label_id = {record_label_id}")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordLabel(result[0], result[1])

    @staticmethod
    def read_by_name(record_label_name: str) -> 'RecordLabel':
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM record_labels WHERE record_label_name = '{record_label_name}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                return RecordLabel(result[0], result[1])


    @staticmethod
    def delete_by_name(record_label_name: str):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = f"DELETE FROM record_labels WHERE record_label_name = '{record_label_name}'"
                cursor.execute(delete_statement)
                conn.commit()

    def update(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                update_statement = (
                    f"UPDATE record_labels "
                    f"SET record_label_name = '{self.record_label_name}' "
                    f"WHERE record_label_id = {self.record_label_id}")
                cursor.execute(update_statement)
                conn.commit()

    def delete(self):
        with dbu.get_connector() as conn:
            with conn.cursor() as cursor:
                delete_statement = "DELETE FROM record_labels WHERE record_label_id = %(record_label_id)s"
                delete_data = {'record_label_id': self.record_label_id}
                cursor.execute(delete_statement, delete_data)
                conn.commit()