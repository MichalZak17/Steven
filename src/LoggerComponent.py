"""

This module defines functions and classes which implement a flexible event logging system for
applications and libraries. The module provides a lot of functionality and flexibility. If you are
unfamiliar with logging, the best way to get to grips with it is to see the tutorials.

The basic classes defined by the module, together with their functions, are listed below:

• Loggers expose the interface that application code directly uses.
• Handlers send the log records (created by loggers) to the appropriate destination.
• Filters provide a finer-grained facility for determining which log records to output.
• Formatters specify the layout of log records in the final output.

"""

from ExceptionsComponent import *

from os.path    import exists
from datetime   import datetime
from inspect    import getouterframes, currentframe

class LoggerClass:
    def __init__(self) -> None:
        self.__directory = {
            "data": "data"
        }
        self.__file = {
            "logs": "data/logs.log"
        }

        self.__TRIES            =       5

        self.__file             = ""
        self.__mode             = ""
        self.__encode           = False
        self.__custom_extension = False

    def __encoder(self, arg):
        """
        Encodes the user-supplied argument into bytes. In future version this funtion will 
        be replaced by SecurityComponent's function.

        Args:
            arg (str): Stores the message to be encoded.

        Returns:
            bytes: Returns an argument converted to bytes ready for an event log entry
        """
        if self.__encode: return arg.encode()
        else: return arg
    
    def __format_message(self, lvl, err, arg, caller):
        """
        Returns a text message that is written to the event log as a log.

        Args:
            lvl (str): Stores information about the login level.
            err (str): Stores information about the error code.
            arg (str): Stores information about any additional information regarding the log.
            caller (str): Stores information about the caller of the function.

        Returns:
            str: Returns a text message that is written to the event log.
        """
        try: __caller = f"{caller[1][1].split('Steven/')[-1]}.{caller[1][3]}()"
        except: raise LogMessageCannotBeCreated()

        try: return f"{lvl.upper()}; {__caller}; {datetime.now()}; {err}; {self.__encoder(arg)}; \n"
        except: LogMessageCannotBeCreated()

    def configure(self, file = "logs.log", mode = "a", encode = False, custom_extension = False):
        """
        Logger configuration to define basic elements of the log.

        Args:
            file (str, optional): Defines the path to log file in "data" folder. Defaults to "logs.log".
            mode (str, optional): Defines the file type of opening and writing to the file. Defaults to "a".
            level (str, optional): Defines the logging type. Defaults to "info".
            encode (bool, optional): Defines whether the arguments are to be encoded. Defaults to False.
            custom_extension (bool, optional): Defines whether the user may use an extension other than .log. Defaults to False.
        """

        if isinstance(custom_extension, bool): self.__custom_extension = custom_extension
        else: raise InvalidParameterException("Incorrect type for custom_extension parameter. Must be boolean.")

        if not self.__custom_extension: file = file.replace(file.split(".")[-1], "log")

        if not exists(self.__directory["data"]): raise DirectoryNotFound(self.__directory["data"])

        if not exists(f"{self.__directory['data']}/{file}"):
            for i in range(self.__TRIES):
                try: self.__log = open(f"{self.__directory['data']}/{file}", "w")
                except: pass
                else: 
                    self.__file = f"{self.__directory['data']}/{file}"
                    self.__log.close()
                    break

            else: raise FileCannotBeCreated(f"{self.__directory['data']}/{file}")

        __opening_modes = ["w", "wb", "a"]

        if not mode in __opening_modes: 
            raise InvalidParameterException("Incorrect mode parameter. Must be one of the following: " + ", ".join(__opening_modes))

        self.__mode = mode
        self.__encode = encode
        self.__file = f"{self.__directory['data']}/{file}"

        del __opening_modes

    def emergency(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("EMERGENCY", err, arg, getouterframes(currentframe(), 4)))

    def alert(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("ALERT", err, arg, getouterframes(currentframe(), 4)))

    def critical(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("CRITICAL", err, arg, getouterframes(currentframe(), 4)))

    def error(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("ERROR", err, arg, getouterframes(currentframe(), 4)))

    def warning(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("WARNING", err, arg, getouterframes(currentframe(), 4)))

    def notice(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("NOTICE", err, arg, getouterframes(currentframe(), 4)))

    def info(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("INFO", err, arg, getouterframes(currentframe(), 4)))

    def debug(self, err = "0x0", arg = "None") -> None:
        """
        Enters logs to the event log file.

        Args:            
            err (str, optional): Holds an error code. Defaults to "0x0".
            arg (str, optional): Keeps any additional information. Defaults to "None".
        """
        with open(self.__file, self.__mode) as log:
            log.write(self.__format_message("DEBUG", err, arg, getouterframes(currentframe(), 4)))
