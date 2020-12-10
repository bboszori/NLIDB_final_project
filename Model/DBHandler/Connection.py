import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode

class Connection:
    def __init__(self, dbtype = 'mysql'):
        self.__dbtype = dbtype
        self.__dbName = ""
        self.connection = None

    def generateConfigdata(self, host, dbName, user, password):
        cf = {
            'user': user,
            'password': password,
            'host': host,
            'database': dbName,
            'raise_on_warnings': True
        }
        return cf

    def connect(self, host, dbName, user, password):
        self.__dbName = dbName
        try:
            self.connection = connection.MySQLConnection(**self.generateConfigdata(host, dbName, user, password))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False
        else:
            return True

    def closeconnection(self):
        if self.connection != None:
            self.connection.close()

