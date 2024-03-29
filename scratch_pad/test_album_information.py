import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

MYSQL_PW = os.getenv('my_sql_pw')
cnx = None
try:
    cnx = mysql.connector.connect(user='root', password=MYSQL_PW, host='localhost', database='album_information')
    cursor = cnx.cursor()
    query = 'select * from album_information'
    cursor.execute(query)
    albums_table = cursor.fetchall()
    albums_df = pd.DataFrame(albums_table, columns=cursor.column_names)
    albums_df = albums_df.set_index(['album_name'])
    print(albums_df)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if cnx is not None:
        cnx.close()
