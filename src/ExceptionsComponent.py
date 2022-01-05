# -------------------------------------------- LoggerComponent Exceptions ---------------------------------------------

class EncodeSetToFalse(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return f" -> Encode parameter has been set to False."

# ------------------------------------------- DatabaseComponent Exceptions --------------------------------------------

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