# Database access utilities

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

MYSQL_USER = 'root'
MYSQL_PW = os.getenv('my_sql_pw')
MYSQL_HOST = 'localhost'
MYSQL_DB = 'album_information'

connect_string = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PW}@{MYSQL_HOST}/{MYSQL_DB}'


def get_connector():
    conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PW, host=MYSQL_HOST, database=MYSQL_DB)
    return conn


def query_to_df(query_string: str, index_col: str | list = None) -> pd.DataFrame:
    try:
        df = pd.read_sql(query_string, connect_string, index_col=index_col)
        return df
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error
