import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

MYSQL_PW = os.getenv('my_sql_pw')
cnx = None
try:
    cnx = mysql.connector.connect(user='root', password=MYSQL_PW, host='localhost', database='my_guitar_shop')
    cursor = cnx.cursor()
    query = 'select product_Id, product_name, category_name from products join categories on products.category_Id = categories.category_Id'
    cursor.execute(query)
    products_table = cursor.fetchall()
    products_df = pd.DataFrame(products_table, columns=cursor.column_names)
    products_df = products_df.set_index('product_Id')
    print(products_df)
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
