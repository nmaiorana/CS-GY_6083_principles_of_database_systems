# This script will create a schema in a mysql database and initialize the tables.


# Path: DBInit.py

import mysql.connector
from mysql.connector import errorcode
import os

MYSQL_PW = os.getenv('my_sql_pw')
cnx = None
try:
    cnx = mysql.connector.connect
    (user='root', password=MYSQL_PW, host='localhost')
    cursor = cnx.cursor()


