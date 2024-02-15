import mysql.connector
from mysql.connector import errorcode
import os

MYSQL_PW = os.getenv('my_sql_pw')
cnx = None
try:
    cnx = mysql.connector.connect(user='root', password=MYSQL_PW, host='localhost', database='my_guitar_shop')
    cursor = cnx.cursor()
    query = 'select product_Id, product_name, category_id from products'
    cursor.execute(query)
    for (product_id, product_name, category_id) in cursor:
        print(f'ID: {product_id} NAME: {product_name} CAT: {category_id}')
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
