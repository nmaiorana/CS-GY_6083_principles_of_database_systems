# This python class will be used to interact with the database and hold the information for an record_label table data.

from project.tools import db_utils as dbu
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

mapper_registry = registry()


def read_record_label(record_label_id):
    prepared_statement = "SELECT * FROM record_labels WHERE record_label_id = %s"
    record_label_row = dbu.read_one_row(prepared_statement, (record_label_id,))
    return RecordLabel(record_label_row[0], record_label_row[1])


def write_record_label(record_label_name: str):
    prepared_statement = "INSERT INTO record_labels (record_label_name) VALUES (%s)"
    dbu.write_one_row(prepared_statement, (record_label_name,))


@mapper_registry.mapped
@dataclass
class RecordLabel:
    __table__ = Table('record_labels', mapper_registry.metadata,
                      Column('record_label_id', Integer, primary_key=True),
                      Column('record_label_name', String))
    record_label_id: int = field(init=False)
    record_label_name: str


if __name__ == '__main__':
    print(f"Record label: {RecordLabel.from_db(1)}")
