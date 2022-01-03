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
    def __init__(self):
        super().__init__()

    def __str__(self):
        return " -> Cannot insert to database."