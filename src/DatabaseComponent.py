"""

This module defines functions and classes which implement a flexible database management system for
applications and libraries. Thanks to sqlite3 the module provides a lot of functionality and flexibility. If you are
unfamiliar with SQL, the best way to get to grips with it is to see the tutorials.

"""

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

    def config(self, file = "data/database/db.db", write_to_log = True, custom_extension = True):
        """
        Database configuration to define basic elements of the config.

        Args:
            file (str, optional): Defines the path to database file. Defaults to "data/database/db.db".
            write_to_log (bool, optional): Defines if the log file should be written to. Defaults to True.
            custom_extension (bool, optional): Defines whether the user may use an extension other than .log. Defaults to False.

        Raises:
            TypeError: Incorrect type for custom_extension parameter. Must be boolean;
            CannotOpenDatabase: The '[DATABASE]' table cannot be opened;
            CannotCreateCursor: Cannot create cursor for '[DATABASE]' database;
        """
        self.__file = file
        self.__write_to_log = write_to_log

        # ----------------------------------- Checking the type of custom_extension -----------------------------------

        if isinstance(custom_extension, bool): self.__custom_extension = custom_extension
        else: 
            if self.__write_to_log: self.__logger.critical(error = "0xB", args = "Incorrect type for custom_extension parameter. Must be boolean")
            raise TypeError("Incorrect type for custom_extension parameter. Must be boolean.")      

        if not self.__custom_extension:
            try: self.__file = self.__file.replace(str(self.__file.split(".")[-1]), "db")
            except: pass

            if not str(self.__file.split(".")[-1]) == "db": self.__file += ".db"

        if not os.path.exists(str(self.__file)): self.__logger.warning(error = "0x2", args = str(self.__file))

        # ------------------------------------------- Opening the database --------------------------------------------

        try: self.conn = sqlite3.connect(str(self.__file))
        except: 
            if self.__write_to_log: self.__logger.critical(error = "0x6", args = "Cannot conect to '{}' database".format(str(self.__file)))                 
            raise CannotOpenDatabase(str(self.__file))

        try: self.c = self.conn.cursor()
        except:
            if self.__write_to_log: self.__logger.critical(error = "0x6", args = "Cannot create cursor for '{}' database".format(str(self.__file)))         
            raise CannotCreateCursor()

    def check_table_exists(self, table_name):
        """
        Checks if the table exists.
        
        Args:
            table_name (str): The name of the table.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        if self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(str(table_name))).fetchall() == []: 
            return False
        else: return True        

    def create_table(self, table_name, table_elements):
        """
        Creates a table.

        Args:
            table_name (str): The name of the table.
            table_elements (list): The elements of the table.

        Raises:
            TableAlreadyExists: The '[TABLE NAME]' table already exists.
            CannotCreateTable: The '[TABLE NAME]' table cannot be created.
        """
        self.__table_elements = {}
        self.__table_elements.update(table_elements)

        if self.check_table_exists(table_name): 
            if self.__write_to_log: self.__logger.warning(error = "0x13", args = "The '{}' table already exists".format(str(table_name)))
            raise TableAlreadyExists(str(table_name))

        def __create_content(elements):
            list = ""

            for item in elements:
                list += "{} {}, ".format(str(item).lower(), str(elements[item]).upper())

            return list[:-2]

        for i in range(self.__TRIES):
            try: self.c.execute("CREATE TABLE {} ({})".format(str(table_name), str(__create_content(self.__table_elements))))
            except: pass
            else: break
        
        else:
            if self.__write_to_log: self.__logger.critical(error = "0x6", args = "The '{}' table cannot be created.".format(str(table_name)))
            raise CannotCreateTable(str(table_name))

        self.conn.commit()

    def insert_item(self, table_name, table_values):
        """
        Inserts an item to the database.

        Args:
            table_name (str): The name of the table.
            table_values (dict): The values of the item.

        Raises:
            CannotInsertToDatabase: The item cannot be inserted to the database;
        
        """
        def __create_content(values):
            list = ""

            for item in values:
                list += "'{}', ".format(str(item))

            return list[:-2]

        for i in range(self.__TRIES):
            try: self.c.execute("INSERT INTO {} VALUES ({})".format(str(table_name), str(__create_content(table_values))))
            except: pass
            else: break

        else: 
            if self.__write_to_log: self.__logger.error(error = "0x1D", 
                args = f"The item '{str(__create_content(table_values))}' cannot be inserted to the database")

            raise CannotInsertToDatabase(str(__create_content(table_values)))

        self.conn.commit()

    def insert_many(self, table_name, table_values):
        """
        Inserts many items to the database.

        Args:
            table_name (str): The name of the table.
            table_values (list): The values of the items.

        Raises:
            CannotInsertToDatabase: The items cannot be inserted to the database;
        """
        def __create_content(value):
            temp = ""

            for item in value[0]:
                temp += "?,"

            return temp[:-1]

        for i in range(self.__TRIES):
            try: self.c.executemany("INSERT INTO {} VALUES ({})".format(str(table_name), str(__create_content(table_values))), table_values)
            except: pass
            else: break

        else: 
            if self.__write_to_log: self.__logger.error(error = "0x1D", 
                args = f"The items '{str(__create_content(table_values))}' cannot be inserted to the database.")

            raise CannotInsertToDatabase(str(__create_content(table_values)))

        self.conn.commit()

    def fetchall(self, table_name):
        """
        Fetches all the items from the database.
        
        Args:
            table_name (str): The name of the table.

        Returns:
            list: The items from the database.
            """
        try: self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        except: 
            if self.__write_to_log: self.__logger.error(error = "0x1E", args = "The '{}' table cannot be fetched.".format(str(table_name)))
            raise CannotFetchTable(str(table_name))

        else: return self.c.fetchall()

    def fetchone(self, table_name):
        """
        Fetches one item from the database.
        
        Args:
            table_name (str): The name of the table.
            
        Returns:
            list: The item from the database.
        """
        try: self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        except:
            if self.__write_to_log: self.__logger.error(error = "0x1E", args = "The '{}' table cannot be fetched.".format(str(table_name)))
            raise CannotFetchTable(str(table_name))

        else: return self.c.fetchone()

    def fetchmany(self, table_name, arg):
        """
        Fetches many items from the database.

        Args:
            table_name (str): The name of the table.
            arg (int): The number of items to fetch.

        Returns:
            list: The items from the database.
        """
        try: self.c.execute("SELECT rowid, * FROM {}".format(str(table_name)))
        except: 
            if self.__write_to_log: self.__logger.error(error = "0x1E", args = "The '{}' table cannot be fetched.".format(str(table_name)))
            raise CannotFetchTable(str(table_name))

        else: return self.c.fetchmany(arg)

    def update(self, table_name, column_name, column_value):
        """
        Updates the database.

        Args:
            table_name (str): The name of the table.
            column_name (str): The name of the column.
            column_value (str): The value of the column.

        Raises:
            CannotUpdateDatabase: The database cannot be updated.
        """
        try: self.c.execute("UPDATE {} SET {} = {}".format(str(table_name), str(column_name), str(column_value)))
        except: 
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be updated | 'UPDATE {} SET {} = {}'" \
                    .format(str(table_name), str(column_name), str(column_value)))
            
            raise CannotUpdateDatabase("UPDATE {} SET {} = {}".format(str(table_name), str(column_name), str(column_value)))

        else: 
            if self.__write_to_log: self.__logger.info(info = "0x0", args = "UPDATE {} SET {} = {}" \
                .format(str(table_name), str(column_name), str(column_value)))
                
            self.conn.commit()

    def update_by_statememt(self, table_name, statement, statement_value, column_name, column_value):
        """
        Updates the database by statement.

        Args:
            table_name (str): The name of the table.
            statement (str): The statement.
            statement_value (str): The value of the statement.
            column_name (str): The name of the column.
            column_value (str): The value of the column.

        Raises:
            CannotUpdateDatabase: The database cannot be updated.
        """
        try: self.c.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(str(table_name), str(column_name), str(column_value), str(statement), str(statement_value)))
        except: 
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be updated | 'UPDATE {} SET {} = {} WHERE {} = {}'"\
                    .format(str(table_name), str(column_name), str(column_value), str(statement), str(statement_value)))
            
            raise CannotUpdateDatabase("UPDATE {} SET {} = {} WHERE {} = {}".format(str(table_name), str(column_name), str(column_value), str(statement), str(statement_value)))
        
        else:
            if self.__write_to_log: self.__logger.info(info = "0x0", args = "'UPDATE {} SET {} = {} WHERE {} = {}'" \
                .format(str(table_name), str(column_name), str(column_value), str(statement), str(statement_value)))

            self.conn.commit()

    def update_by_rowid(self, table_name, rowid, column_name, column_value):
        """
        Updates the database by rowid.

        Args:
            table_name (str): The name of the table.
            rowid (int): The rowid.
            column_name (str): The name of the column.
            column_value (str): The value of the column.

        Raises:
            CannotUpdateDatabase: The database cannot be updated.
        """
        try:self.c.execute("UPDATE {} SET {} = {} WHERE id = {}".format(str(table_name), str(column_name), str(column_value), str(rowid)))
        except: 
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be updated | 'UPDATE {} SET {} = {} WHERE id = {}'"\
                    .format(str(table_name), str(column_name), str(column_value), str(rowid)))
            
            raise CannotUpdateDatabase("UPDATE {} SET {} = {} WHERE id = {}".format(str(table_name), str(column_name), str(column_value), str(rowid)))
        
        else:
            if self.__write_to_log: 
                self.__logger.info(info = "0x0", args = "'UPDATE {} SET {} = {} WHERE id = {}'" \
                    .format(str(table_name), str(column_name), str(column_value), str(rowid)))
                    
            self.conn.commit()

    def delete(self, table_name):
        """
        Deletes the database.

        Args:
            table_name (str): The name of the table.

        Raises:
            CannotDeleteDatabase: The database cannot be deleted.
        """
        try: self.c.execute("DELETE FROM {}".format(str(table_name)))
        except: 
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be deleted | 'DELETE FROM {}'".format(str(table_name)))
            
            raise CannotDeleteElements("'DELETE FROM {}'".format(str(table_name)))

        else: 
            if self.__write_to_log: self.__logger.info(info = "0x0", args = "'DELETE FROM {}'".format(str(table_name)))
            self.conn.commit()

    def deltete_by_statement(self, table_name, statement, statement_value):
        """
        Deletes the database by the statement.

        Args:
            table_name (str): The name of the table.
            statement (str): The statement.
            statement_value (str): The value of the statement.

        Raises:
            CannotDeleteDatabase: The database cannot be deleted.
        """
        try: self.c.execute("DELETE FROM {} WHERE {} = {}".format(str(table_name), str(statement), str(statement_value)))
        except: 
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be deleted | 'DELETE FROM {} WHERE {} = {}'" \
                    .format(str(table_name), str(statement), str(statement_value)))
            
            raise CannotDeleteElements("DELETE FROM {} WHERE {} = {}".format(str(table_name), str(statement), str(statement_value)))

        else: 
            if self.__write_to_log:
                self.__logger.info(info = "0x0", args = "'DELETE FROM {} WHERE {} = {}'".format(str(table_name), str(statement), str(statement_value)))
            
            self.conn.commit()

    def deltete_by_rowid(self, table_name, rowid):
        """
        Deletes the database by rowid.

        Args:
            table_name (str): The name of the table.
            rowid (int): The rowid.

        Raises:
            CannotDeleteDatabase: The database cannot be deleted.
        """
        try: self.c.execute("DELETE FROM {} WHERE id = {}".format(str(table_name), str(rowid)))
        except:
            if self.__write_to_log: 
                self.__logger.error(error = "0x1D", args = "The item cannot be deleted | 'DELETE FROM {} WHERE id = {}'" \
                    .format(str(table_name), str(rowid)))
            
            raise CannotDeleteElements("DELETE FROM {} WHERE id = {}".format(str(table_name), str(rowid)))
        
        else: 
            if self.__write_to_log: self.__logger.info(info = "0x0", args = "DELETE FROM {} WHERE id = {}".format(str(table_name), str(rowid)))
            self.conn.commit()

    def custom_statement(self, statement):
        """
        Executes a custom statement.

        Args:
            statement (str): The statement.

        Raises:
            CannotExecuteCustomStatement: The statement cannot be executed.
        """
        try: self.c.execute(statement)
        except:
            if self.__write_to_log: self.__logger.error(error = "0x16", args = "The statement cannot be executed | '{}'".format(str(statement)))
            raise CannotExecuteCustomStatement(statement)

        else: 
            if self.__write_to_log: self.__logger.info(info = "0x0", args = str(statement))            
            self.conn.commit()

    def close(self):
        """
        Closes the database.

        Raises:
            CannotCloseDatabase: The database cannot be closed.
        """
        try: self.conn.close()
        except: 
            if self.__write_to_log: self.__logger.error(error = "0x1C", args = "The connection between  database cannot be closed.")            
            raise CannotCloseConnection()
