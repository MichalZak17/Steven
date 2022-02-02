import os
import inspect
import datetime
import importlib

# ------------------------------------------------- Custom exceptions -------------------------------------------------

class CannotCreateDirectory(Exception):
    """
    Exception class for creating directory.

    Args:
        arg (str): Directory name.        
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory cannot be created."

class CannotCreateFile(Exception):
    """
    Exception class for creating file.

    Args:
        arg (str): File name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file cannot be created."

class DirectoryNotFound(Exception):
    """
    Exception class for directory check.

    Args:
        arg (str): Directory name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory doesn't exist."

class FileNotFound(Exception):
    """
    Exception class for file check.
    
    Args:
        arg (str): File name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file doesn't exist."

class ModuleImportFailure(Exception):
    """
    Exception class for module import failure.

    Args:
        arg (str): Module name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The attempt to import '{self.arg}' module failed."

class CannotInstallIntagratedModule(Exception):
    """
    Exception class for integrated module failure.
    
    Args:
        arg (str): Module name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module is integrated and cannot be installed."

class CannotCreateLog(Exception):
    """
    Exception class for creating log.

    Args:
        arg (str): Log name.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The log to '{self.arg}' file cannot be created."

class InvalidThreadMode(Exception):
    """
    Exception class for invalid thread mode.

    Args:
        arg (str): Thread mode.
    """
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' thread mode is invalid."

# --------------------------------------------------------------------------------------------------------------------- 

class GuardianClass:
    def __init__(self) -> None:
        self.__missing_file             =           []
        self.__missing_directory        =           []
        self.__missing_module           =           []

        self.__directory                =           {
            "data":                     "data", 
            "config":                   "config",
            "settings":                 "settings",
            "backup":                   "data/backup",
            "database":                 "data/database"
        }
        self.__file                     =           {
            "log":                      "data/logs.log",
            "config":                   "config/config.ini"
        }

        self.__modules_default          =           {
            "os":                      "os",
            "sys":                     "sys",
            "time":                    "time",
            "json":                    "json",
            "math":                    "math",
            "random":                  "random",
            "pickle":                  "pickle",
            "inspect":                 "inspect",
            "sqlite3":                 "sqlite3",
            "datetime":                "datetime",
            "threading":               "threading",
            "configparser":            "configparser",

            # ------------------------------------------------- Custom modules -------------------------------------------------

            "numpy":                   "numpy",
            "pandas":                  "pandas",
            "requests":                "requests",
            "matplotlib":              "matplotlib",
            "progressbar":             "progressbar",
        }  
        self.__modules_integrated       =           {
            "os":                      "os",
            "sys":                     "sys",
            "time":                    "time",
            "json":                    "json",
            "math":                    "math",
            "random":                  "random",
            "pickle":                  "pickle",
            "inspect":                 "inspect",
            "sqlite3":                 "sqlite3",
            "datatime":                "datetime",
            "threading":               "threading",
            "configparser":            "configparser"
        }
        self.__modules_project          =           []

        self.__TRIES                    =           5

    def __create_log(self, lvl = "info", code = "KERNEL", err = "0x0", arg = "None") -> None:
        """
        Simple logger function for GuardianClass opertaions.

        Args: 
            lvl (str): Log type.
            err (str): Error code.
            arg (str): Argument.

        """
        __caller_temp = inspect.getouterframes(inspect.currentframe(), 4)
        __caller = f"{__caller_temp[1][1]}.{__caller_temp[1][3]}()"

        try:
            with open(self.__file["log"], "a") as log:
                log.write(f"{lvl.upper()}; {__caller}; {datetime.datetime.now()}; {err}; {arg}; \n")
        except: CannotCreateLog(self.__file["log"])

    def __import_module(self, module = "None", install = False) -> None:
        """
        Import module function.
        
        Args:
            module (str): Module name.
            install (bool): Install module if module isn't integrated.
        """
        try: globals()[module] = importlib.import_module(module)
        except:
            if install:
                if not module in self.__modules_integrated:
                    try: os.system(f"pip3 install {self.__missing_module}")
                    except: self.__create_log("error", "0x1F", self.__missing_module)
                    else: 
                        try: globals()[self.__missing_module] = importlib.import_module(self.__missing_module)
                        except: self.__create_log("error", "0x1B", self.__missing_module)
                        else: self.__create_log(arg = f"The {self.__missing_module} module has been installed")

                else: self.__create_log("warning", "0x1E", f"The {module} module is integrated and cannot be installed")

            else: self.__create_log("critical", "0x1B", f"The {module} module cannot be imported")

        else: self.__create_log(arg = f"The {module} module has been imported")

    def __check_file(self, file = "None", log = True) -> bool:
        """
        Check if file exists.
        
        Args:
            file (str): File name.
            log (bool): If True, log will be created.
            
        Returns:
            bool: True if file exists, False otherwise.
        """
        if not os.path.exists(file):
            if log: self.__create_log("warning", "0x4", file)
            return False

        else: return True
    
    def __check_dir(self, dir = "None", create = True, log = True) -> bool:
        """
        Check if directory exists.
        
        Args:
            dir (str): Directory path.
            create (bool): Create directory if it doesn't exist.
            log (bool): Log event if directory doesn't exist.

        Returns:
            bool: True if directory exists, False otherwise.
        """
        if not os.path.exists(dir):
            if log: self.__create_log("warning", "0x5", dir)

            if create:
                for i in range(self.__TRIES):
                    try: os.makedirs(dir)
                    except: pass
                    else: 
                        self.__create_log(arg = f"The {dir} directory has been created")
                        break

                else: 
                    if log: self.__create_log("error", "0x20", dir)
                    raise CannotCreateDirectory(dir)
            
            return False

        else: return True
    
    def __reload_module(self, module = "None") -> None:
        """
        Reload module.

        Args:
            module (str): Module name.
        """
        try: importlib.reload(globals()[module])
        except: self.__create_log("error", "0x1C", f"The {module} module cannot be reloaded")
        else: self.__create_log(arg = f"The {module} module has been reloaded")

    def configure(self, mode = "default") -> None:
        """
        Configure the Guardian Core for future operations.

        Args:
            mode (str): Configure mode.
        """
        if not os.path.exists(self.__directory["data"]):
            for i in range(self.__TRIES):
                try: os.makedirs(self.__directory["data"])
                except: pass
                else: break

            else: raise CannotCreateDirectory(self.__directory["data"])

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file["log"])
            
            self.__create_log("warning", "0x5", self.__directory["data"])
            self.__create_log(arg = f"The {self.__directory['data']} has been created")
            self.__create_log("warning", "0x4", self.__file["log"])
            self.__create_log(arg = f"The {self.__file['log']} has been created")

        if not os.path.exists(self.__file["log"]):
            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file["log"])
 
            self.__create_log("warning", "0x4", self.__file["log"])
            self.__create_log(arg = f"The {self.__file['log']} has been created")

        for dir in self.__directory:
            self.__check_dir(dir = self.__directory[dir])

        if mode == "default":
            for module in self.__modules_default:
                try: globals()[module] = importlib.import_module(module)
                except: 
                    self.__create_log("error", "0x19", module)
                    self.__missing_module.append(module)

            for module in os.listdir("src"):
                if not os.path.isdir(module):
                    if module[-3:] == ".py" and not module == "__init__.py" and not module == "GuardianComponent.py":
                        try: globals()[module[:-3]] = importlib.import_module("src", module[:-3])
                        except: 
                            self.__create_log(err = "0x1A", arg = module[:-3])
                            raise ModuleImportFailure(module[:-3])

            if len(self.__missing_module):
                self.__create_log(arg = "Initializing modules installation")

                os.system("sudo apt install python3-pip")

                while len(self.__missing_module) > 0:
                    if not self.__missing_module[0] in self.__modules_integrated:
                        for i in range(self.__TRIES):
                            try: os.system(f"pip3 install {self.__modules_default[self.__missing_module[0]]}")
                            except: pass 
                            else: 
                                self.__create_log(arg = f"The {self.__missing_module[0]} module has been installed")

                                try: globals()[self.__missing_module[0]] = importlib.import_module(self.__missing_module[0])
                                except: pass
                                else:
                                    self.__create_log(arg = f"The {self.__missing_module[0]} module has been imported")
                                    self.__missing_module.pop(0)
                                    break
                        
                        else: 
                            self.__create_log("critical", "0x1B", self.__missing_module[0])
                            raise ModuleImportFailure(self.__missing_module[0])

                    else: 
                        self.__create_log("critical", "0x1E", f"The {self.__missing_module[0]} module has been integrated and cannot be installed")
                        raise CannotInstallIntagratedModule(self.__missing_module[0])                  

        elif mode == "safe":
            for module in self.__modules_integrated:
                try: globals()[module] = importlib.import_module(module)
                except: raise ModuleImportFailure(module)
