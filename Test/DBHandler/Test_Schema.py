from Model.DBHandler.Schema import Schema
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import pyodbc
import pymssql
#
# MS SQL connection
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15

# conn_mssql = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
#                         Server='DHUB7135\SDSTEST',database='AdventureWorks2019', user='testuser',
#                       password='test')
#
# cursor = conn_mssql.cursor()

#conn_mssql.close()



# MySQL connection
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

config = {
  'user': 'testuser',
  'password': 'testpassword',
  'host': '127.0.0.1',
  'database': 'classicmodels',
  'raise_on_warnings': True
}

tables = []

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
    cursor = cnx.cursor()
    cursor.execute("SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = '%s';" % 'classicmodels')
    tablelist = cursor.fetchall()
    tables = []

    cursor.execute("SELECT table_name, column_name, referenced_table_name, referenced_column_name from "
                   "information_schema.key_column_usage where referenced_table_name is not null AND TABLE_SCHEMA = '%s'" % 'classicmodels')

    forkeys = cursor.fetchall()
    print(forkeys)

    cnx.close()









