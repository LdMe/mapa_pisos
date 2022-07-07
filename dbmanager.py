"""class DBManager
creates connection to mysql database and provides methods to access it
"""

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import os

load_dotenv()
""" DEBUG variable, if in environment variable exists and DEBUG=1, then debug messages are printed, if not, then not"""
DEBUG = os.environ.get('DEBUG') == '1'
class DBManager:
    """class DBManager
    creates connection to mysql database and provides methods to access it
    """

    def __init__(self):
        self.host = os.environ['MYSQL_HOST']
        self.user = os.environ['MYSQL_USER']
        self.password = os.environ['MYSQL_PASSWORD']
        self.database = os.environ['MYSQL_DATABASE']
        self.port = os.environ['MYSQL_PORT']
        self.charset = 'utf8'
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           database=self.database,
                                           port=self.port,
                                           charset=self.charset)
        self.cursor = self.cnx.cursor()

    def get_connection(self):
        return self.cnx

    def get_cursor(self):
        return self.cursor

    def create_database(self, database):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed creating database: {}".format(err))
            exit(1)

    def create_table(self, table_name, columns):
        try:
            self.cursor.execute(
                "CREATE TABLE {}({})".format(table_name, columns))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                if DEBUG:
                    print("already exists.")
            else:
                if DEBUG:
                    print(err.msg)
        else:
            if DEBUG:
                print("OK")
    def insert_data(self, table_name, columns, data,multiple=False,ignore=False):
        """ insert single/multiple and with/without ignore"""
        try:
            if multiple:
                self.cursor.execute(
                    "INSERT {} INTO {}({}) VALUES {}".format("IGNORE" if ignore else "", table_name, columns, data))
                """
                with open("done_inserts.txt", "a") as f:
                    f.write("---------------------\n")
                    f.write("INSERT {} INTO {}({}) VALUES {}".format("IGNORE" if ignore else "", table_name, columns, data)+"\n")
                """
            else:
                self.cursor.execute(
                    "INSERT {} INTO {}({}) VALUES({})".format("IGNORE" if ignore else "", table_name, columns, data))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed inserting data: {}".format(err))
                """ save failed insert into file"""
                with open("failed_inserts.txt", "a") as f:
                    f.write("INSERT {} INTO {}({}) VALUES {}".format("IGNORE" if ignore else "", table_name, columns, data)+"\n")
                #print("INSERT {} INTO {}({}) VALUES({})".format("IGNORE" if ignore else "", table_name, columns, data))
            
    def insert_data_old(self, table_name, columns, data,multiple=False,ignore=False):
        try:
            self.cursor.execute(
                "INSERT INTO {}({}) VALUES({})".format(table_name, columns, data))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed inserting data: {}".format(err))
                #print("INSERT INTO {}({}) VALUES({})".format(table_name, columns, data))        
    def select_all_data(self, table_name):
        try:
            self.cursor.execute("SELECT * FROM {}".format(table_name))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed selecting data: {}".format(err))
            #exit(1)
    def select_data(self, table_name, columns, condition):
        try:
            self.cursor.execute(
                "SELECT {} FROM {} WHERE {}".format(columns, table_name, condition))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed selecting data: {}".format(err))
            

    def update_data(self, table_name, columns, condition):
        try:
            self.cursor.execute(
                "UPDATE {} SET {} WHERE {}".format(table_name, columns, condition))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed updating data: {}".format(err))
                print("UPDATE {} SET {} WHERE {}".format(table_name, columns, condition))
            #exit(1)
    
    def delete_data(self, table_name, condition):
        try:
            self.cursor.execute(
                "DELETE FROM {} WHERE {}".format(table_name, condition))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if DEBUG:
                print("Failed deleting data: {}".format(err))
            #exit(1)

    def close_connection(self):
        self.cursor.close()
        self.cnx.close()


if __name__ == "__main__":

    """test database connection"""
    dbmanager = DBManager()
    """ select data from table  house"""
    print(dbmanager.select_all_data("location"))
    dbmanager.close_connection()
