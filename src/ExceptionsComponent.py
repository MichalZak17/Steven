class EncodeSetToFalse(Exception):
    def __init__(self, arg):
        self.arg = str(arg)

        super().__init__(self.arg)

    def __str__(self):
        return f" -> Encode parameter has been set to False."