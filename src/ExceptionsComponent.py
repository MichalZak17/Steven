"""
Exception with arguments template:

    class [EXCEPTION NAME](Exception):
        def __init__(self, arg):
            self.arg = str(arg)

            super().__init__(self.arg)

        def __str__(self):
            return f" -> [MESSAGE]"

Exception without arguments template:

    class [EXCEPTION NAME](Exception):
        def __init__(self):
            super().__init__()

        def __str__(self):
            return f" -> [MESSAGE]"
"""

class FileNotFound(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file has been not found."

class FileCorrupted(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file has been corrupted."

class FileAlreadyExists(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file already exists."

class FileCannotBeCreated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file cannot be created."

class FileCannotBeDeleted(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file cannot be deleted."


class DirectoryNotFound(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory has been not found."

class DirectoryAlreadyExists(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory already exists."

class DirectoryCannotBeCreated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory cannot be created."

class DirectoryCannotBeDeleted(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory cannot be deleted."


class ModuleCannotBeImported(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module cannot be imported."

class ModuleCannotBeReloaded(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module cannot be reloaded."

class ModuleCannotBeInstalled(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module cannot be installed."

class ModuleCannotBeUninstalled(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module cannot be uninstalled."

class ModuleIsIntegrated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module is integrated."


class InvalidModeException(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' mode is invalid."

class InvalidParameterException(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' parameter is invalid."


class LogCannotBeCreated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' log file cannot be created."


class CannotOpenDatabase(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' table cannot be opened."

class CannotCreateCursor(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return " -> Cannot create cursor."

class CannotCreateTable(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' table cannot be created."

class TableAlreadyExists(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' table already exists and cannot be created again."

class CannotInsertToDatabase(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> Cannot insert '{self.arg}' to database."

class CannotFetchTable(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> Cannot fetch '{self.arg}' table."

class CannotUpdateDatabase(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> Cannot update '{self.arg}' elements in database."

class CannotDeleteElements(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> Cannot delete elements from database | '{self.arg}'."

class CannotExecuteCustomStatement(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> Cannot execute custom statement | '{self.arg}'."

class CannotCloseConnection(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return " -> Cannot close the database."

class EncodeSetToFalse(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return f" -> Encode parameter has been set to False."
