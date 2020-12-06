from Model.NLHandler.Parser import Parser
from Model.NLHandler.ParseTree import ParseTree
from Model.DBHandler.Schema import Schema
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import warnings
warnings.filterwarnings("ignore", message=r"\[W007\]", category=UserWarning)

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
    schema = Schema(cnx, 'classicmodels', 'mysql')
    parser = Parser(schema)
    pt = parser.createParsetree('Show the number of orders where the status is shipped')

    print(pt.get_root.getChildren[0].getWord.get_text())
    l = parser.getComponentoptions(pt.get_root.getChildren[0])
    print('Component: ' + l[0].get_component)
    print('Type: ' + l[0].get_type)
    print('Similarity: ' + str(l[0].get_similarity))

