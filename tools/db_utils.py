# Database access utilities

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, Connection, inspect
from sqlalchemy import create_engine

MYSQL_USER = 'root'
MYSQL_PW = os.getenv('my_sql_pw')
MYSQL_HOST = 'localhost'
MYSQL_DB = 'album_information'

url_object = URL.create(
    drivername="mysql+mysqlconnector",
    username=MYSQL_USER,
    password=MYSQL_PW,
    host=MYSQL_HOST,
    database=MYSQL_DB
)

engine = create_engine(url_object)
Session = sessionmaker(engine, expire_on_commit=False)


def get_session():
    return Session()


def get_connection_string() -> str:
    return url_object.__to_string__()


def get_inspector() -> inspect:
    return inspect(engine)


def get_table_names() -> list:
    return get_inspector().get_table_names()


def get_view_names() -> list:
    return get_inspector().get_view_names()


def get_columns(table_name: str) -> list:
    return get_inspector().get_columns(table_name)


def sqlalchemy_connect_to_db() -> Connection:
    return engine.connect()


def sqlalchemy_query_to_df(query_string: str, index_col: str | list = None) -> pd.DataFrame:
    try:
        df = pd.read_sql_query(query_string, con=engine, index_col=index_col)
        return df
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error


# Read one row from the database using a prepared statement
def read_one_row(query: str, values: tuple):
    try:
        conn = sqlalchemy_connect_to_db()
        cursor = conn.cursor(prepared=True)
        cursor.execute(query, values)
        row = cursor.fetchone()
        conn.close()
        return row
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error


# Write one row to the database using a prepared statement
def write_one_row(query: str, values: tuple):
    try:
        conn = sqlalchemy_connect_to_db()
        cursor = conn.cursor(prepared=True)
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error


if __name__ == "__main__":
    connection = sqlalchemy_connect_to_db()
    print(connection)
    connection.close()
    print("Connection closed")
    print(sqlalchemy_query_to_df("SELECT * FROM record_albums", "album_id"))
    print(sqlalchemy_query_to_df('select * from album_information_details',
                                 ['name', 'release_date', 'artist_name', 'record_label_name', 'track_number']))


# use msql.connector to execute a query
def execute(query):
    try:
        with get_connector() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error


def get_connector():
    conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PW, host=MYSQL_HOST, database=MYSQL_DB)
    return conn
