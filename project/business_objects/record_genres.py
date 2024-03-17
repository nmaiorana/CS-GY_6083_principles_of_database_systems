# Using sqlalchemy to create a class to represent the record_genres table in the database. The RecordGenre class will
# be used to interact with the database and hold the information for a record_genres table data.
from dataclasses import dataclass

from project.tools import db_utils as dbu
import sqlalchemy as sa

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()


@reg.mapped_as_dataclass
class RecordGenres:
    __tablename__ = 'record_genres'
    genre_id: int = mapped_column(init=False, primary_key=True)
    genre_name: str = mapped_column(sa.String)
    genre_description: str = mapped_column(sa.String)


if __name__ == '__main__':
    Session = sa.orm.sessionmaker(dbu.engine)
    session = Session()
    test_genre_name = 'TEST Genre'
    updated_genre_name = 'Updated Genre'
    print(f'Current record genres:')
    for record in session.query(RecordGenres).all():
        print(record)

    new_record = RecordGenres(genre_name=test_genre_name, genre_description='A new genre')
    session.add(new_record)
    session.commit()
    print(f'New record genres:')
    for record in session.query(RecordGenres).all():
        print(record)

    record_to_update = session.query(RecordGenres).filter_by(genre_id=new_record.genre_id).first()
    record_to_update.genre_name = updated_genre_name
    session.commit()
    print(f'Updated record genres:')
    for record in session.query(RecordGenres).all():
        print(record)

    record_to_update.genre_name = test_genre_name
    session.commit()

    # Clean up
    session.query(RecordGenres).filter_by(genre_name=test_genre_name).delete()
    session.query(RecordGenres).filter_by(genre_name=updated_genre_name).delete()
    session.commit()
    print(f'Original record genres:')
    for record in session.query(RecordGenres).all():
        print(record)

    session.close()
