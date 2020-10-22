from Model.DBHandler.Schema import Schema
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import pyodbc
import pymssql

# MS SQL connection
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15

# cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
#                         Server='127.0.0.1,1443,SDSTEST',
#                         user='SDSReportUser', password='SDSreportpass#2016')

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








