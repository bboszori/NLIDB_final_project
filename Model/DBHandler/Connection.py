import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode

class Connection:
    def __init__(self, host, dbName, user, password, dbtype = 'mysql'):
        self.__host = host
        self.__dbName = dbName
        self.__user = user
        self.__password = password
        self.__dbtype = dbtype
        self.__connection = None

    def generateConfigdata(self):
        cf = {
            'user': self.__user,
            'password': self.__password,
            'host': self.__host,
            'database': self.__dbName,
            'raise_on_warnings': True
        }
        return cf

    def connect(self):
        try:
            self.__connection = connection.MySQLConnection(**self.generateConfigdata())
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None
        else:
            return self.__connection

    def closeconnection(self):
        if self.__connection != None:
            self.__connection.close()

