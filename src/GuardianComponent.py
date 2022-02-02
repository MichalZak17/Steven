

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
    def __make_log(self, lvl = "warning", err = "0x0", arg = "None", date = True):
        """
        Message format assistant

        Args: 
            lvl (str): Log level.
            err (str): Error code.
            arg (str): Argument.
            date (bool): Date flag.

        Returns:
            str: Formatted message.
        """
        part_one    =   f"{str(lvl).upper()}; "
        part_two    =   f"{str(datetime.datetime.now())}; "
        part_three  =   f"{str(err)}; "
        part_four   =   f"{str(arg)}; "

        if date:
            part_one += part_two

        part_one += part_three
        part_one += part_four

        return f"{part_one}\n"

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

        self.__directory                =           [
            "data", "data/database", "data/backup", "config"
        ]
        self.__file                     =           [
            "data/logs.log", "data/dirs.pkl",
            "data/files.pkl", "config/_thread.ini"
        ]

        self.__modules                   =           []
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

        if not os.path.exists(self.__directory[0]):
            self.__missing_directory.append(self.__directory[0])
            self.__missing_file.append(self.__file[0])

            for i in range(self.__TRIES):
                try: os.makedirs(self.__directory[0])
                except: pass
                else: break

            else: raise CannotCreateDirectory(self.__directory[0])

            # ---------------------------------------- Creating logs.log file  ----------------------------------------

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file[0], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file[0])

        # ------------------------------------------ Creating logs.log file  ------------------------------------------

        if not os.path.exists(self.__file[0]):
            self.__missing_file.append(self.__file[0])

            for i in range(self.__TRIES):
                try: self.__log = open(self.__file[0], "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(self.__file[0])

        # -------------------------------------------- Reading config file --------------------------------------------

        self.__config = configparser.ConfigParser()

        if not os.path.exists(PATH_CONFIG):
            self.__missing_file.append(PATH_CONFIG)

            with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0x2", arg = PATH_CONFIG))

            self.__modules = self.__default_modules
            self.__create_config()

            with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0x0", arg = "The {} has been restored to default.".format(PATH_CONFIG)))

        # -------------------------------------- Creating config file if missing --------------------------------------

        else:
            try:
                self.__config.read(PATH_CONFIG)
                self.__modules = self.__config["MODULES"]["modules"][1:-1].split(", ")

                for i in range(len(self.__modules)):
                    self.__modules[i] = self.__modules[i][1:-1]

            except: 
                with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0xD", arg = PATH_CONFIG))

                self.__modules = self.__default_modules
                self.__create_config()

                with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0x0", arg = "The {} has been restored to default.".format(PATH_CONFIG)))
     
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
                with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0x7E", arg = module))
                
                raise ModuleImportFailure(module)

        # --------------------------------------- Installing addnotical modules ---------------------------------------

        if len(self.__missing_module):
            os.system("sudo apt install python3-pip")

            while len(self.__missing_module) > 0:

                with open(self.__file[0], "a") as log:
                    log.write(self.__make_log(err = "0x7E", arg = self.__missing_module[0]))

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
            if not os.path.exists(dir):
                self.__missing_directory.append(dir)

        for file in self.__file:
            if not os.path.exists(file):
                self.__missing_file.append(file)

        # --------------------------------------- Adding missing files to list ----------------------------------------

        while len(self.__missing_directory) > 0:
            with open(self.__file[0], "a") as log:
                log.write(self.__make_log(err = "0x3", arg = self.__missing_directory[0]))

            if not os.path.exists(self.__missing_directory[0]):
                for i in range(self.__TRIES):
                    try: os.makedirs(self.__missing_directory[0])
                    except: pass
                    else: break

                else: raise CannotCreateDirectory(self.__missing_directory[0])

            self.__missing_directory.pop(0)

        while len(self.__missing_file) > 0:
            with open(self.__file[0], "a") as log:
                log.write(self.__make_log(err = "0x2", arg = self.__missing_file[0]))

            self.__missing_file.pop(0)

        # -------------------------------------------------- Thread ---------------------------------------------------

        class ThreadClass(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)

                self.__missing_file             =           []
                self.__missing_directory        =           []

                self.__directory                =           [
                    "data", "data/database", "data/backup",
                    "config"
                ]
                self.__file                     =           [
                    "data/logs.log", "data/dirs.pkl",
                    "data/files.pkl", PATH_CONFIG
                ]

                self.__IS_RUNNING               =           False
                self.__SLEEP_TIME               =           5
                self.__TRIES                    =           5

                # ------------------------------------------- Thread Config -------------------------------------------

                self.__config = configparser.ConfigParser()

                if not self.__config.has_section("SETTINGS"): 
                    with open(self.__file[0], "a") as log:
                        log.write(self.__make_log(err = "0xD", arg = "The 'SETTINGS' section could not be found in config file."))
                else:
                    try:
                        self.__config.read(PATH_CONFIG)
                        self.__SLEEP_TIME = self.__config["SETTINGS"].getfloat("timeaftercycle")
                        self.__TRIES = self.__config["SETTINGS"].getint("numberoftries")
                    
                    except: pass

            def __make_log(self, lvl = "warning", err = "0x0", arg = "None", date = True):
                """
                Message format assistant

                Args: 
                    lvl (str): Log level.
                    err (str): Error code.
                    arg (str): Argument.
                    date (bool): Date flag.

                Returns:
                    str: Formatted message.
                """
                part_one    =   f"{str(lvl).upper()}; "
                part_two    =   f"{str(datetime.datetime.now())}; "
                part_three  =   f"{str(err)}; "
                part_four   =   f"{str(arg)}; "

                if date:
                    part_one += part_two

                part_one += part_three
                part_one += part_four

                return f"{part_one}\n"

            def run(self):
                self.__IS_RUNNING = True

                while True:
                    time.sleep(self.__SLEEP_TIME)

                    if self.__IS_RUNNING:

                        # ---------------------------- Creating data fodler with log file  ----------------------------

                        if not os.path.exists(self.__directory[0]):
                            self.__missing_directory.append(self.__directory[0])
                            self.__missing_file.append(self.__file[0])

                            for i in range(self.__TRIES):
                                try: os.makedirs(self.__directory[0])
                                except: pass
                                else: break

                            else: raise CannotCreateDirectory(self.__directory[0])

                            # ------------------------------------------------------------------------------------------

                            for i in range(self.__TRIES):
                                try: self.__log = open(self.__file[0], "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(self.__file[0])

                        # ---------------------------------- Creating logs.log file  ----------------------------------

                        if not os.path.exists(self.__file[0]):
                            self.__missing_file.append(self.__file[0])

                            for i in range(self.__TRIES):
                                try: self.__log = open(self.__file[0], "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(self.__file[0])

                        # ------------------------------------- Opening logs file -------------------------------------

                        for i in range(self.__TRIES):
                            try: self.__log = open(self.__file[0], "a")
                            except: pass
                            else: break

                        else: raise CannotCreateFile(self.__file[0])

                        # -------------------------------- Opening data/dirs.pkl file ---------------------------------

                        for i in range(self.__TRIES):
                            try: self.__directory_list = open(self.__file[1], "rb")
                            except: pass
                            else:
                                for i in range(self.__TRIES):
                                    try:
                                        for dir in pickle.load(self.__directory_list):
                                            self.__directory.append(dir)
                                    except: pass
                                    else:
                                        self.__directory_list.close()
                                        break

                                else:
                                    self.__log.write(self.__make_log(err = "0x1E", arg = self.__file[1]))
                                    os.remove(self.__file[1])

                                break

                        else:
                            self.__log.write(self.__make_log(err = "0x1E", arg = self.__file[1]))
                            os.remove(self.__file[1])

                        # -------------------------------- Opening data/files.pkl file --------------------------------

                        for i in range(self.__TRIES):
                            try: self.__file_list = open(self.__file[2], "rb")
                            except: pass
                            else:

                                for i in range(self.__TRIES):
                                    try:
                                        for file in pickle.load(self.__file_list):
                                            self.__file.append(file)
                                    except: pass
                                    else:
                                        self.__file_list.close()
                                        break

                                else:
                                    self.__log.write(self.__make_log(err = "0x1E", arg = self.__file[2]))
                                    os.remove(self.__file[2])

                                break

                        else:
                            self.__log.write(self.__make_log(err = "0x1E", arg = self.__file[2]))
                            os.remove(self.__file[2])

                        # -------------------------------- Scanning Project Directory ---------------------------------

                        for e in os.listdir("."):
                            if os.path.isfile(str(e)):
                                if not str(e) in self.__file: self.__file.append(str(e))
                            elif os.path.isdir(str(e)):
                                if not str(e) in self.__directory: self.__directory.append(str(e))

                        for d in self.__directory:
                            if os.path.exists(str(d)):
                                for e in os.listdir(str(d)):

                                    if os.path.isfile("{}/{}".format(str(d), str(e))):
                                        if not "{}/{}".format(str(d), str(e)) in self.__file:
                                            self.__file.append("{}/{}".format(str(d), str(e)))

                                        elif os.path.isdir("{}/{}".format(str(d), str(e))):
                                            if not "{}/{}".format(str(d), str(e)) in self.__directory:
                                                self.__directory.append("{}/{}".format(str(d), str(e)))
                                            else:
                                                self.log.write(self.__make_dump_log("0x3", str(d)))

                        # ------------------------- Deleting duplicated content from the list -------------------------

                        self.__directory = list(dict.fromkeys(self.__directory))
                        self.__file = list(dict.fromkeys(self.__file))

                        # ----------------------------- Adding missing directoris to list -----------------------------

                        for dir in self.__directory:
                            if not os.path.exists(dir):
                                self.__missing_directory.append(dir)

                        for file in self.__file:
                            if not os.path.exists(file):
                                self.__missing_file.append(file)

                        # -------------------------------- Creating missing directoris --------------------------------

                        while len(self.__missing_directory) > 0:
                            self.__log.write(self.__make_log(err = "0x3", arg = self.__missing_directory[0]))

                            for i in range(self.__TRIES):
                                try: os.makedirs(self.__missing_directory[0])
                                except: pass
                                else: break

                            else: raise CannotCreateDirectory(self.__missing_directory[0])

                            self.__missing_directory.pop(0)

                        # ---------------------------------- Creating missing files -----------------------------------

                        while len(self.__missing_file) > 0:
                            self.__log.write(self.__make_log(err = "0x2", arg = self.__missing_file[0]))

                            for i in range(self.__TRIES):
                                try: temp = open(self.__missing_file[0], "w")
                                except: pass
                                else:
                                    temp.close()
                                    del temp
                                    break

                            else: raise CannotCreateDirectory(self.__missing_file[0])

                            self.__missing_file.pop(0)

                        # --------------------- Saving info about data in project folder to files ---------------------

                        with open(str(self.__file[1]), "wb") as f:
                            pickle.dump(self.__directory, f)

                        with open(str(self.__file[2]), "wb") as f:
                            pickle.dump(self.__file, f)

                    else: pass

            def stop(self, reason):
                self.__IS_RUNNING = False

                with open(str(self.__file[0]), "a") as f:
                    f.write(str(self.__make_log(lvl = "info", err = "0x0", arg = str(f"Thread stopped. Reason: {reason}"))))

            def resume(self):
                self.__IS_RUNNING = True

                with open(str(self.__file[0]), "a") as f:
                    f.write(str(self.__make_log(lvl = "info", err = "0x0", arg = str("Thread resumed"))))

            def status(self):
                return self.__IS_RUNNING

        self.Thread = ThreadClass()
        self.Thread.start()
