import os
import sqlite3
from .LoggerComponent import LoggerClass
from .ExceptionsComponent import *

class DatabaseClass:

    def __init__(self):
        self.__logger = LoggerClass()
        self.__logger.config(file = "db_logs.log")

        self.__table_elements       =       {}

        self.__TRIES                =       5

    def config(self, file):
        if not os.path.exists(str(file)):
            self.__logger.warning(error = "0x2", args = str(file))

        try: self.conn = sqlite3.connect(str(file))
        except: raise CannotOpenDatabase(str(file))

        try: self.c = self.conn.cursor()
        except: raise CannotCreateCursor()

    def __check_table_exists(self, t_name):
        try: self.c.execute("SELECT * FROM {}".format(str(t_name)))
        except: pass

        if self.c.fetchall() == []: return True
        else: return False

    def create_table(self, table_name, table_elements):
        self.__table_elements = {}
        self.__table_elements.update(table_elements)

        if self.__check_table_exists(table_name): raise TableAlreadyExists(str(table_name))

        def __create_content(elements):
            list = ""

            for item in elements:
                list += "{} {}, ".format(str(item).lower(), str(elements[item]).upper())

            return list[:-2]

        for i in range(self.__TRIES):
            try: self.c.execute("CREATE TABLE {} ({})".format(str(table_name), str(__create_content(self.__table_elements))))
            except: pass
            else: break
        
        else: raise CannotCreateTable(str(table_name))

        self.conn.commit()

    def insert_item(self, table_name, table_values):
        def __create_content(values):
            list = ""

            for item in values:
                list += "'{}', ".format(str(item))

            return list[:-2]

        for i in range(self.__TRIES):
            try: self.c.execute("INSERT INTO {} VALUES ({})".format(str(table_name), str(__create_content(table_values))))
            except: pass
            else: break

        else: raise CannotInsertToDatabase()

        self.conn.commit()

    def insert_many(self, table_name, table_values):
        def __create_content(value):
            temp = ""

            for item in value[0]:
                temp += "?,"

            return temp[:-1]

        for i in range(self.__TRIES):
            try: self.c.executemany("INSERT INTO {} VALUES ({})".format(str(table_name), str(__create_content(table_values))), table_values)
            except: pass
            else: break

        else: Exception("Cannot insert dictionary to database.")

        self.conn.commit()

    def fetchall(self, table_name):
        self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        return self.c.fetchall()

    def fetchone(self, table_name):
        self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        return self.c.fetchone()

    def fetchmany(self, table_name, arg):
        self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        return self.c.fetchmany(arg)

    def update(self, table_name, column_name, column_value):
        self.c.execute("UPDATE {} SET {} = {}".format(str(table_name), str(column_name), str(column_value)))
        self.conn.commit()

    def update_by_statememt(self, table_name, statement, statement_value, column_name, column_value):
        self.c.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(str(table_name), str(column_name), str(column_value), str(statement), str(statement_value)))
        self.conn.commit()

    def update_by_rowid(self, table_name, rowid, column_name, column_value):
        self.c.execute("UPDATE {} SET {} = {} WHERE id = {}".format(str(table_name), str(column_name), str(column_value), str(rowid)))
        self.conn.commit()

    def delete(self, table_name):
        self.c.execute("DELETE FROM {}".format(str(table_name)))
        self.conn.commit()

    def deltete_by_statement(self, table_name, statement, statement_value):
        self.c.execute("DELETE FROM {} WHERE {} = {}".format(str(table_name), str(statement), str(statement_value)))
        self.conn.commit()

    def deltete_by_rowid(self, table_name, rowid):
        self.c.execute("DELETE FROM {} WHERE id = {}".format(str(table_name), str(rowid)))
        self.conn.commit()

    def close(self):
        self.conn.close()
