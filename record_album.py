# Define the CRUD operations for the record_album table

# Import the mysql connector
import mysql.connector
from mysql.connector import errorcode

# Import the os module
import os

# Get the password from the environment
MYSQL_PW = os.getenv('project_user_pw')
print('MYSQL_PW: ', MYSQL_PW)

# Create a connection object
cnx = None

# Try to connect to the database
try:
    cnx = mysql.connector.connect(user='project_user', password=MYSQL_PW, host='localhost', database='record_album_information')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
    else:
        print(err)

finally:
    if cnx is not None:
        cnx.close()
