import os
import datetime
import configparser

PATH_CONFIG = "config/_thread.ini"

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

class DirectoryDoesntExist(Exception):
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

class FileDoesntExist(Exception):
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

# --------------------------------------------------------------------------------------------------------------------- 

class GuardianClass:
    def __create_log(self, lvl = "warning", err = "0x0", arg = "None"):
        """
        Logger function.

        Args: 
            lvl (str): Log level.
            err (str): Error code.
            arg (str): Argument.

        """
        with open(self.__file["log"], "a") as log:
            log.write(f"{lvl.upper()}; {datetime.datetime.now()}; {err}; {arg}; \n")

    def __create_config(self):
        """
        Create config file with default values.
        """
        self.__config = configparser.ConfigParser()

        self.__config["MODULES"] = {
            "modules": self.__default_modules
        }

        self.__config["SETTINGS"] = {
            "timeaftercycle": "5",
            "numberoftries": "5"
        }

        with open(PATH_CONFIG, "w") as f:
            self.__config.write(f)

    def __init__(self):
        self.__missing_file             =           []
        self.__missing_directory        =           []
        self.__missing_module           =           []

        self.__directory                =           {
            "data":                     "data", 
            "database":                     "data/database",
            "backup":                   "data/backup",
            "config":                   "config"
        }
        self.__file                     =           {
            "log":                      "data/logs.log", 
            "config":                   PATH_CONFIG
        }

        self.__modules                  =           []
        self.__default_modules          =           [
            "os",
            "sys",
            "time",
            "json",
            "math",
            "random",
            "pickle",
            "sqlite3",
            "datetime",
            "itertools",
            "threading",
            "configparser",

            # ----------------------- System modules -----------------------

            "torch",
            "numpy",
            "scipy",
            "geopy",
            "pandas",
            "discord",
            "requests",
            "geocoder",
            "matplotlib",
            "progressbar"
        ]
        self.__integrated_modules       =           [
            "os",
            "sys",
            "time",
            "json",
            "math",
            "random",
            "pickle",
            "sqlite3",
            "datetime",
            "itertools",
            "threading",
            "configparser"
        ]

        self.__project_modules          =           []

        self.__TRIES                    =           5

        # ------------------------------------ Creating data folder with log file  ------------------------------------

        if not os.path.exists(self.__directory["data"]):
            self.__missing_directory.append(self.__directory["data"])
            self.__missing_file.append(self.__file["log"])

            for i in range(self.__TRIES):
                try: os.makedirs(self.__directory["data"])
                except: pass
                else: break

            else: raise CannotCreateDirectory(self.__directory["data"])

            # ---------------------------------------- Creating logs.log file  ----------------------------------------

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file["log"])

        # ------------------------------------------ Creating logs.log file  ------------------------------------------

        if not os.path.exists(self.__file["log"]):
            self.__missing_file.append(self.__file["log"])

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file["log"], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file["log"])

        # ------------------------------------------ Checking config folder  ------------------------------------------

        if not os.path.exists(self.__directory["config"]):
            self.__missing_directory.append(self.__directory["config"])
            self.__create_log(err = "0x3", arg = self.__directory["config"])

            for i in range(self.__TRIES):
                try: os.makedirs(self.__directory["config"])
                except: pass
                else: break

            else: raise CannotCreateDirectory(self.__directory["config"])

        # -------------------------------------------- Reading config file --------------------------------------------

        self.__config = configparser.ConfigParser()

        if not os.path.exists(self.__file["config"]):
            self.__missing_file.append(self.__file["config"])
            self.__create_log(err = "0x2", arg = self.__file["config"])

            self.__modules = self.__default_modules
            self.__create_config()

            self.__create_log(arg = f"The {self.__file['config']} has been restored to default.")

        # -------------------------------------- Creating config file if missing --------------------------------------

        else:
            try:
                self.__config.read(self.__file["config"])
                self.__modules = self.__config["MODULES"]["modules"][1:-1].split(", ")

                for i in range(len(self.__modules)):
                    self.__modules[i] = self.__modules[i][1:-1]

            except: 
                self.__create_log(err = "0xD", arg = self.__file["config"])

                self.__modules = self.__default_modules
                self.__create_config()
                
                self.__create_log(arg = f"The {self.__file['config']} has been restored to default.")
     
        # ---------------------------------- Importing import_module from importlib -----------------------------------

        from importlib import import_module

        # ---------------------------------------- Dynamicly importing modules ----------------------------------------

        for module in self.__modules:
            try: globals()[module] = import_module(module)
            except: self.__missing_module.append(module)

        for module in os.listdir("src"):
            if not os.path.isdir(module):
                if module[-3:] == ".py" and not module == "__init__.py" and not module == "GuardianComponent.py":
                    self.__project_modules.append(module[:-3])

        for module in self.__project_modules:
            try: globals()[module] = import_module("src", module)
            except:
                self.__create_log(err = "0x7E", arg = module)                
                raise ModuleImportFailure(module)

        # --------------------------------------- Installing addnotical modules ---------------------------------------

        if len(self.__missing_module):
            os.system("sudo apt install python3-pip")

            while len(self.__missing_module) > 0:
                self.__create_log(err = "0x7E", arg = self.__missing_module[0])

                if not self.__missing_module[0] in self.__integrated_modules:
                    for i in range(self.__TRIES):
                        try: os.system("pip3 install {}".format(self.__missing_module[0]))
                        except: pass
                        else:
                            try: globals()[self.__missing_module[0]] = import_module(self.__missing_module[0])
                            except: raise ModuleImportFailure(self.__missing_module[0])
                            else: self.__missing_module.pop(0)

                else: raise CannotInstallIntagratedModule(self.__missing_module[0])

        # ------------------------------------- Adding missing directoris to list -------------------------------------

        for dir in self.__directory:
            if not os.path.exists(self.__directory[dir]):
                self.__missing_directory.append(self.__directory[dir])

        for file in self.__file:
            if not os.path.exists(self.__file[file]):
                self.__missing_file.append(self.__file[file])

        # --------------------------------------- Adding missing files to list ----------------------------------------

        while len(self.__missing_directory) > 0:
            self.__create_log(err = "0x3", arg = self.__missing_directory[0])

            if not os.path.exists(self.__missing_directory[0]):
                for i in range(self.__TRIES):
                    try: os.makedirs(self.__missing_directory[0])
                    except: pass
                    else: break

                else: raise CannotCreateDirectory(self.__missing_directory[0])

            self.__missing_directory.pop(0)

        while len(self.__missing_file) > 0:
            self.__create_log(err = "0x2", arg = self.__missing_file[0])
            self.__missing_file.pop(0)

        # -------------------------------------------------- Thread ---------------------------------------------------

        class ThreadClass(threading.Thread):
            def __create_log(self, lvl = "warning", err = "0x0", arg = "None"):
                """
                Logger function.

                Args: 
                    lvl (str): Log level.
                    err (str): Error code.
                    arg (str): Argument.

                """
                with open(self.__file["log"], "a") as log:
                    log.write(f"{lvl.upper()}; {datetime.datetime.now()}; {err}; {str(arg)}; \n")

            def __create_config(self):
                """
                Create config file with default values.
                """
                self.__config = configparser.ConfigParser()

                self.__config["MODULES"] = {
                    "modules": self.__default_modules
                }

                self.__config["SETTINGS"] = {
                    "timeaftercycle": "5",
                    "numberoftries": "5"
                }

                with open(PATH_CONFIG, "w") as f:
                    self.__config.write(f)
            
            def __init__(self):
                threading.Thread.__init__(self)

                self.__missing_file             =           []
                self.__missing_directory        =           []

                self.__directory                =           {
                    "data":                     "data", 
                    "database":                 "data/database",
                    "backup":                   "data/backup",
                    "config":                   "config"
                }
                self.__file                     =           {
                    "log":                      "data/logs.log", 
                    "config":                   PATH_CONFIG,
                    "dirstructure":             "data/dirs.pkl"
                }

                self.__default_modules          =           [
                    "os",
                    "sys",
                    "time",
                    "json",
                    "math",
                    "random",
                    "pickle",
                    "sqlite3",
                    "datetime",
                    "itertools",
                    "threading",
                    "configparser",

                    # ----------------------- System modules -----------------------

                    "torch",
                    "numpy",
                    "scipy",
                    "geopy",
                    "pandas",
                    "discord",
                    "requests",
                    "geocoder",
                    "matplotlib",
                    "progressbar"
                ]
                

                self.__IS_RUNNING               =           False
                self.__SLEEP_TIME               =           5
                self.__TRIES                    =           5

                # ------------------------------------------- Thread Config -------------------------------------------

                self.__config = configparser.ConfigParser()
                
                try:
                    self.__config.read(self.__file["config"])
                    self.__SLEEP_TIME = self.__config["SETTINGS"].getfloat("timeaftercycle")
                    self.__TRIES = self.__config["SETTINGS"].getint("numberoftries")
                except: 
                    self.__create_log(err = "0xD", arg = "Cannot read the config file.")
                    self.__create_config()
                    self.__create_log(arg = f"The {self.__file['config']} has been restored to default.")

            def run(self):
                self.__IS_RUNNING = True

                while True:
                    time.sleep(self.__SLEEP_TIME)

                    if self.__IS_RUNNING:

                        # ---------------------------- Creating data folder with log file  ----------------------------

                        if not os.path.exists(self.__directory["data"]):
                            self.__missing_directory.append(self.__directory["data"])
                            self.__missing_file.append(self.__file["log"])

                            for i in range(self.__TRIES):
                                try: os.makedirs(self.__directory["data"])
                                except: pass
                                else: break

                            else: raise CannotCreateDirectory(self.__directory["data"])

                            # ---------------------------------------- Creating logs.log file  ----------------------------------------

                            for i in range(self.__TRIES):
                                try: self.__log = open(self.__file["log"], "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(self.__file["log"])

                        # ---------------------------------- Creating logs.log file  ----------------------------------

                        if not os.path.exists(self.__file["log"]):
                            self.__missing_file.append(self.__file["log"])

                            for i in range(self.__TRIES):
                                try: self.__log = open(self.__file["log"], "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(self.__file["log"])
                        
                        # -------------------------------- Opening data/dirs.pkl file ---------------------------------

                        if os.path.exists(self.__file["dirstructure"]):
                            try:
                                with open(self.__file["dirstructure"], "rb") as f:
                                    self.__directory = pickle.load(f)
                            except:
                                self.__create_log(err = "0xD", arg = "Cannot read the data/dirs.pkl file.")
                                self.__create_log(arg = f"The {self.__file['dirstructure']} has been restored to default.")
                                os.remove(self.__file["dirstructure"])

                        # -------------------------------- Scanning Project Directory ---------------------------------

                        for e in os.listdir("."):
                            if os.path.isfile(str(e)):
                                if not str(e) in self.__file: self.__file[str(e)] = str(e)
                            elif os.path.isdir(str(e)):
                                if not str(e) in self.__directory: self.__directory[str(e)] = str(e)

                        temp_dict = self.__directory.copy()
                        
                        for d in temp_dict:
                            if os.path.exists(str(d)):
                                for e in os.listdir(str(d)):

                                    if os.path.isfile("{}/{}".format(str(d), str(e))):
                                        if not "{}/{}".format(str(d), str(e)) in self.__file:
                                            self.__file["{}/{}".format(str(d), str(e))] = "{}/{}".format(str(d), str(e))

                                    elif os.path.isdir("{}/{}".format(str(d), str(e))):
                                        
                                        if not "{}/{}".format(str(d), str(e)) in self.__directory:
                                            self.__directory["{}/{}".format(str(d), str(e))] = "{}/{}".format(str(d), str(e))
                                            self.__create_log(err = "0x3", arg = "{}/{}".format(str(d), str(e)))
                                                                    
                        del temp_dict           

                        # ----------------------------- Adding missing directoris to list -----------------------------

                        for dir in self.__directory:
                            if not os.path.exists(self.__directory[dir]):
                                self.__missing_directory.append(self.__directory[dir])

                        for file in self.__file:
                            if not os.path.exists(self.__file[file]):
                                self.__missing_file.append(self.__file[file])

                        # -------------------------------- Adding missing files to list -------------------------------

                        while len(self.__missing_directory) > 0:
                            self.__create_log(err = "0x3", arg = self.__missing_directory[0])

                            if not os.path.exists(self.__missing_directory[0]):
                                for i in range(self.__TRIES):
                                    try: os.makedirs(self.__missing_directory[0])
                                    except: pass
                                    else: break

                                else: raise CannotCreateDirectory(self.__missing_directory[0])

                            self.__missing_directory.pop(0)

                        while len(self.__missing_file) > 0:
                            self.__create_log(err = "0x2", arg = self.__missing_file[0])
                            self.__missing_file.pop(0)

                        # ------------------- Saving info about structure in project folder to file -------------------

                        with open("data/dirs.pkl", "wb") as f:
                            pickle.dump(self.__directory, f)

                    else: pass

        self.Thread = ThreadClass()
        self.Thread.start()
