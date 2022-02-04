import os
import inspect
import datetime
import importlib

# ------------------------------------------------- Custom exceptions -------------------------------------------------

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

class FileCannotBeCreated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file cannot be created."

class DirectoryNotFound(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory has been not found."

class DirectoryCannotBeCreated(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory cannot be created."

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

class LogMessageCannotBeCreated(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return f" -> The log message cannot be created."

class ThreadCannotBeStarted(Exception):
    def __init__(self, arg):
        self.arg = str(arg)
        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' thread cannot be started."

# --------------------------------------------------------------------------------------------------------------------- 

class GuardianClass:
    def __init__(self) -> None:
        self.__missing_file             =           []
        self.__missing_file_flagged     =           []
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
            "config":                   "config/config.ini",
            "dirstruct":                "data/dirstruct.structure"
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

        self.__THREAD_CURRENT_MODE      =           ""
        self.__THREAD_MODES             =           ["offline", "online", "error", "repairing"]
        self.__THREAD_TIMEOUT           =           5

    # --------------------------------------------------- Utilities ---------------------------------------------------

    def __create_log(self, lvl = "info", err = "0x0", arg = "None") -> None:
        """
        Logger function for GuardianClass separated opertaions.

        Args: 
            lvl (str, optional): Log type.
            err (str, optional): Error code.
            arg (str, optional): Argument.

        Levels:
            info: Information.
            warning: Warning.
            error: Error.
            emergency: Emergency.
            alert: Alert.
            critical: Critical.
            debug: Debug.
            notice: Notice.
        """
        try: 
            __caller_temp = inspect.getouterframes(inspect.currentframe(), 4)
            __caller = f"{__caller_temp[1][1]}.{__caller_temp[1][3]}()"
        except: raise LogMessageCannotBeCreated()

        __levels = [
            "emergency", "alert", "critical", "error",
            "warning", "notice", "info", "debug"
        ]

        if lvl not in __levels: raise InvalidModeException(lvl)

        try:
            with open(self.__file["log"], "a") as log:
                log.write(f"{lvl.upper()}; {__caller}; {datetime.datetime.now()}; {err}; {arg}; \n")
        except: LogCannotBeCreated(self.__file["log"])

    def __import_module(self, module = "None", install = False) -> None:
        """
        Imports a specified module. If the module is not installed, 
        it will be installed if the install parameter is True.
        
        Args:
            module (str): Module name.
            install (bool): Install module if module isn't integrated.
        """
        try: globals()[module] = importlib.import_module(module)
        except:
            if not install: self.__create_log(lvl = "warning", err = "0x1B", arg = module)
            if module in self.__modules_integrated: self.__create_log(lvl = "warning", err = "0x1E", arg = module)

            try: os.system(f"pip3 install {module}")
            except: self.__create_log(lvl = "error", err = "0x1F", arg = module)
            else: 
                try: globals()[module] = importlib.import_module(module)
                except: self.__create_log(lvl = "error", err = "0x1B", arg = module)
            
        else: self.__create_log(arg = f"The {module} module has been imported")

    def __check_file(self, file = "None", log = True) -> bool:
        """
        Check if file exists. If not return False. True otherwise.
        May log the file name if log parameter is True.
        
        Args:
            file (str): File name.
            log (bool): If True, log will be created.
            
        Returns:
            bool: True if file exists, False otherwise.
        """
        if not os.path.exists(file):
            if log: self.__create_log(lvl = "warning", err =  "0x4", arg = file)
            return False

        else: return True
    
    def __check_dir(self, dir = "None", create = True, log = True) -> bool:
        """
        Check if directory exists. If not return False. True otherwise.
        May create the directory if create parameter is True.
        May log the directory name if log parameter is True.
        
        Args:
            dir (str): Directory path.
            create (bool): Create directory if it doesn't exist.
            log (bool): Log event if directory doesn't exist.

        Returns:
            bool: True if directory exists, False otherwise.
        """
        if not os.path.exists(dir):
            if log: self.__create_log(lvl = "warning", err = "0x5", arg = dir)

            if create:
                for i in range(self.__TRIES):
                    try: os.makedirs(dir)
                    except: pass
                    else: 
                        self.__create_log(arg = f"The {dir} directory has been created")
                        break

                else: 
                    if log: self.__create_log(lvl = "error", err = "0x20", arg = dir)
                    raise DirectoryCannotBeCreated(dir)
            
            return False

        else: return True
    
    def __reload_module(self, module = "None") -> None:
        """
        Reloads a specified module.

        Args:
            module (str): Module name.
        """
        try: importlib.reload(globals()[module])
        except: self.__create_log(lvl = "error", err = "0x1C", arg = module)
        else: self.__create_log(arg = f"The {module} module has been reloaded")
    
    # ----------------------------------------------- Pre configuration -----------------------------------------------
    
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

            else: raise DirectoryCannotBeCreated(self.__directory["data"])

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise FileCannotBeCreated(self.__file["log"])
            
            self.__create_log(lvl = "warning", err = "0x5", arg = self.__directory["data"])
            self.__create_log(arg = f"The {self.__directory['data']} has been created")

            self.__create_log(lvl = "warning", err = "0x4", arg = self.__file["log"])
            self.__create_log(arg = f"The {self.__file['log']} has been created")

        if not os.path.exists(self.__file["log"]):
            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise FileCannotBeCreated(self.__file["log"])
 
            self.__create_log(lvl = "warning", err = "0x4", arg = self.__file["log"])
            self.__create_log(arg = f"The {self.__file['log']} has been created")

        for dir in self.__directory:
            self.__check_dir(dir = self.__directory[dir])

        if mode == "default":
            for module in self.__modules_default:
                try: globals()[module] = importlib.import_module(module)
                except: 
                    self.__create_log(lvl = "error", err = "0x19", arg = module)
                    self.__missing_module.append(module)

            for module in os.listdir("src"):
                if not os.path.isdir(module):
                    if module[-3:] == ".py" and not module == "__init__.py" and not module == "GuardianComponent.py":
                        try: globals()[module[:-3]] = importlib.import_module("src", module[:-3])
                        except: 
                            self.__create_log(lvl = "critical", err = "0x1A", arg = module[:-3])
                            raise ModuleCannotBeImported(module[:-3])

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
                            self.__create_log(lvl = "critical", err = "0x1B", arg = self.__missing_module[0])
                            raise ModuleCannotBeInstalled(self.__missing_module[0])

                    else: 
                        self.__create_log(lvl = "critical", err = "0x1E", arg = self.__missing_module[0])
                        raise ModuleIsIntegrated(self.__missing_module[0])                  

        elif mode == "safe":
            self.__create_log(arg = "Initializing safe mode configuration")

            for module in self.__modules_integrated:
                try: globals()[module] = importlib.import_module(module)
                except: raise ModuleCannotBeImported(module)

    # ------------------------------------------- Thread Controller Section -------------------------------------------

    """
    Thread Controller Section
    
    This section contains the methods that control the threads.
    
    Modes:
        - Offline: Thread is not running.
        - Online: Thread is running.
        - Error: Thread has an error.
        - Repairing: Thread is being repaired.
    """

    def thread_start(self, start = False) -> None:
        """
        Changes the status of the Guardian Core to online, if it's offline.

        Args:
            start (bool): If True, the thread will be started.
        """
        if not self.__THREAD_CURRENT_MODE == "online":
            self.__THREAD_CURRENT_MODE = "online"
            self.__create_log(arg = "Guardian Core mode has been changed to 'online'")

        if start:
            try:
                self.__THREAD = threading.Thread(target = self.__core)
                self.__THREAD.start()
            except:
                self.__THREAD_CURRENT_MODE = "error"
                self.__create_log(lvl = "error", err = "0x22", arg = "Guardian Core startup")
                raise ThreadCannotBeStarted("Guardian Core")   
            else: self.__create_log(arg = "Guardian Core has been started")
           
    def thread_stop(self, kill = False) -> None:
        """
        Changes the status of the Guardian Core to offline, if it's online.

        Args:
            kill (bool): If True, the thread will be killed.
        """
        if self.__THREAD_CURRENT_MODE == "online":
            self.__THREAD_CURRENT_MODE = "offline"            
            self.__create_log(arg = "Guardian Core has been turned 'offline'")

        if kill:
            self.__THREAD_CURRENT_MODE = "offline"
            self.__create_log(arg = "Guardian Core has been turned 'offline'")

            try: self.__THREAD.join()
            except: pass
            else: self.__create_log(arg = "Guardian Core has been killed")

    def thread_status(self, log = False) -> bool:
        """
        Returns the status of the Guardian Core thread.

        Args:
            log (bool): If True, the status will be logged with other parameters.

        Returns:
            bool: True if the thread is running, False otherwise.
        """
        if log: self.__create_log(arg = f"Guardian Core status: {self.__THREAD_CURRENT_MODE}")
        return self.__THREAD_CURRENT_MODE

    def __core(self):
        self.__create_log(arg = "Initializing Guardian Core thread")

        while True:
            time.sleep(self.__THREAD_TIMEOUT)

            if not self.__THREAD_CURRENT_MODE == "offline":

                if not os.path.exists(self.__directory["data"]):
                    for i in range(self.__TRIES):
                        try: os.makedirs(self.__directory["data"])
                        except: pass
                        else: break

                    else: raise DirectoryCannotBeCreated(self.__directory["data"])

                    for i in range(self.__TRIES):
                        try: self.__log = open(self.__file["log"], "w")
                        except: pass
                        else:
                            self.__log.close()
                            break

                    else: raise FileCannotBeCreated(self.__file["log"])
                    
                    self.__create_log(lvl = "warning", err = "0x5", arg = self.__directory["data"])
                    self.__create_log(arg = f"The {self.__directory['data']} has been created")

                    self.__create_log(lvl = "warning", err = "0x4", arg = self.__file["log"])
                    self.__create_log(arg = f"The {self.__file['log']} has been created")

                if not os.path.exists(self.__file["log"]):
                    for i in range(self.__TRIES):
                        try: self.__log = open(self.__file["log"], "w")
                        except: pass
                        else:
                            self.__log.close()
                            break

                    else: raise FileCannotBeCreated(self.__file["log"])
        
                    self.__create_log(lvl = "warning", err = "0x4", arg = self.__file["log"])
                    self.__create_log(arg = f"The {self.__file['log']} has been created")

                for dir in self.__directory:
                    self.__check_dir(dir = self.__directory[dir])

                if self.__check_file(self.__file["dirstruct"]):
                    try:
                        with open(self.__file["dirstruct"], "rb") as f:
                            self.__directory = pickle.load(f)
                    except:
                        self.__create_log(lvl = "warning", err = "0x16", arg = self.__file["dirstruct"])
                        os.remove(self.__file["dirstruct"])
                        self.__create_log(arg = f"The {self.__file['dirstruct']} has been removed")
                
                for e in os.listdir("."):
                    if os.path.isfile(str(e)):
                        if not str(e) in self.__file: self.__file[str(e)] = str(e)
                    elif os.path.isdir(str(e)):
                        if not str(e) in self.__directory: self.__directory[str(e)] = str(e)

                __temp_dict = self.__directory.copy()
                        
                for d in __temp_dict:
                    if os.path.exists(d):
                        for e in os.listdir(d):

                            if os.path.isfile(f"{d}/{e}"):
                                if not f"{d}/{e}" in self.__file:
                                    self.__file[f"{d}/{e}"] = f"{d}/{e}"

                            elif os.path.isdir(f"{d}/{e}"):                                
                                if not f"{d}/{e}" in self.__directory:
                                    self.__directory[f"{d}/{e}"] = f"{d}/{e}"
                                                            
                del __temp_dict

                for dir in self.__directory:
                    if not os.path.exists(self.__directory[dir]):
                        self.__missing_directory.append(self.__directory[dir])

                for file in self.__file:
                    if not os.path.exists(self.__file[file]):
                        self.__missing_file.append(self.__file[file])

                while len(self.__missing_directory) > 0:
                    self.__create_log(lvl = "warning", err = "0x5", arg = self.__missing_directory[0])

                    if not os.path.exists(self.__missing_directory[0]):
                        for i in range(self.__TRIES):
                            try: os.makedirs(self.__missing_directory[0])
                            except: pass
                            else:
                                self.__create_log(arg = f"The {self.__missing_directory[0]} has been created")
                                break

                        else: raise DirectoryCannotBeCreated(self.__missing_directory[0])

                    self.__missing_directory.pop(0)

                while len(self.__missing_file) > 0:
                    if not self.__missing_file[0] in self.__missing_file_flagged:
                        self.__create_log(lvl = "warning", err = "0x4", arg = self.__missing_file[0])
                        self.__missing_file_flagged.append(self.__missing_file[0])
                        
                    self.__missing_file.pop(0)

                with open(self.__file["dirstruct"], "wb") as f:
                    pickle.dump(self.__directory, f)