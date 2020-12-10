from Model.NLHandler.Parser import Parser
from Model.NLHandler.ParseTree import ParseTree
from Model.DBHandler.Schema import Schema
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import warnings
from Model.NLHandler.Translator import Translator
from Model.DBHandler.Query import Query
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
    #pt = parser.createParsetree('Show the number of orders before 2005.01.01')
    pt = parser.createParsetree('Show all employee name and their jobtitle')

    for n in pt.get_nodelist:
        l = parser.getComponentoptions(n)
        n.setComponent(l[0])

    pt.removeunknownnodes()

    tr = Translator(pt, schema)
    query = tr.translateParsetree()
    print(query.sqlquerystring())

    # for ch in pt.get_nodelist:
    #
    #     if not ch.getRemoved:
    #         print("Word: " + ch.getWord.get_text())
    #         print("CT: " + ch.getComponent.get_type)
    #         print("CT: " + ch.getComponent.get_component)
    #         print("CP: " + str(ch.getComponent.get_similarity))
    #         print(ch.getRemoved)
    #         print('---------------------')
    #         for n in ch.getChildren:
    #             print(n.getWord.get_text())
    #         print('---------------------')
