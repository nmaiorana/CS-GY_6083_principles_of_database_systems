# Define the CRUD operations for the record_album table

# Import the mysql connector
import mysql.connector
from mysql.connector import errorcode

# Import the os module
import os

# Get the password from the environment
MYSQL_PW = os.getenv('my_sql_pw')


def connect():
    # Create and return a connection object
    cnx = None

    # Try to connect to the database
    try:
        cnx = mysql.connector.connect(user='root', password=MYSQL_PW, host='localhost', database='album_information')
        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)

        raise err


if __name__ == '__main__':
    album_information_conn = None
    try:
        album_information_conn = connect()
    except mysql.connector.Error as err:
        print('Connection failed')
    finally:
        print('Connection closed')
        if album_information_conn is not None:
            album_information_conn.close()
