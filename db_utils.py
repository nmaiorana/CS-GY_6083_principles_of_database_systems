# Database access utilities

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

MYSQL_USER = 'root'
MYSQL_PW = os.getenv('my_sql_pw')
MYSQL_HOST = 'localhost'
MYSQL_DB = 'album_information'


def connect_to_db():
    cnx = None
    try:
        cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PW, host=MYSQL_HOST, database=MYSQL_DB)
        return cnx
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error


# read the query into a dataframe and set the first column as the index
def db_query_to_df(query_string: str):
    try:
        cnx = connect_to_db()
        cursor = cnx.cursor()
        cursor.execute(query_string)
        table = cursor.fetchall()
        df = pd.DataFrame(table, columns=cursor.column_names)
        df = df.set_index(df.columns[0])
        cnx.close()
        return df
    except mysql.connector.Error as db_error:
        if db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif db_error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(db_error)
        raise db_error
