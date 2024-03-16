# This python class will be used to interact with the database and hold the information for an record_label table data.

import db_utils as dbu
from dataclasses import dataclass


def read_record_label(record_label_id):
    # Create a connection object
    conn = dbu.connect_to_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM record_label WHERE record_label_id = '{record_label_id}'")
    record_label_row = cursor.fetchone()
    conn.close()
    return record_label_row


@dataclass
class RecordLabel:
    record_label_id: int
    record_label_name: str

    def __init__(self, record_label_name):
        self.record_label = record_label_name

    def add_record_label(self):
        # Create a connection object
        conn = dbu.connect_to_db()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO record_label (record_label) VALUES ('{self.record_label}')")
        conn.commit()
        conn.close()

    def get_record_labels(self):
        # Create a connection object
        conn = dbu.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM record_label")
        record_labels = cursor.fetchall()
        conn.close()
        return record_labels
