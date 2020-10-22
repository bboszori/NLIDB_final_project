from Model.DBHandler.Schema import Schema
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode

# MySQL connection
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

config = {
  'user': 'testuser',
  'password': 'testpassword',
  'host': '127.0.0.1',
  'database': 'classicmodels',
  'raise_on_warnings': True
}

try:
    cnx = connection.MySQLConnection(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    myschema = Schema(cnx, "classicmodels", "mysql")

    cnx.close()








