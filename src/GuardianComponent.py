import os
import datetime

# ------------------------------------------------- Custom exceptions -------------------------------------------------

class CannotCreateDirectory(Exception):
    def __init__(self, arg):
        self.arg = str(arg)

        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' directory cannot be created."

class CannotCreateFile(Exception):
    def __init__(self, arg):
        self.arg = str(arg)

        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' file cannot be created."

class ModuleImportFailure(Exception):
    def __init__(self, arg):
        self.arg = str(arg)

        super().__init__(self.arg)

    def __str__(self):
        return f" -> The attempt to import '{self.arg}' module failed."

class CannotInstallIntagratedModule(Exception):
    def __init__(self, arg):
        self.arg = str(arg)

        super().__init__(self.arg)

    def __str__(self):
        return f" -> The '{self.arg}' module is integrated and cannot be installed."

# --------------------------------------------------------------------------------------------------------------------- 

class GuardianClass:

    def __make_log(self, lvl = "warning", err = "0x0", arg = "None", date = True):
        part_one    =   f"{str(lvl).upper()}; "
        part_two    =   f"{str(datetime.datetime.now())}; "
        part_three  =   f"{str(err)}; "
        part_four   =   f"{str(arg)}; "

        if date:
            part_one += part_two

        part_one += part_three
        part_one += part_four

        return f"{part_one}\n"

    def __init__(self):
        self.__missing_file             =           []
        self.__missing_directory        =           []
        self.__missing_module           =           []

        self.__directory                =           [
            "data", "data/database", "data/backup",
            "config"
        ]
        self.__file                     =           [
            "data/logs.log", "data/dirs.pkl",
            "data/files.pkl", "config/_thread.ini"
        ]

        self.__modules                  =           {
            "os": "os",
            "sys": "sys",
            "time": "time",
            "json": "json",
            "math": "math",
            "random": "random",
            "pickle": "pickle",
            "sqlite3": "sqlite3",
            "datetime": "datetime",
            "itertools": "itertools",
            "threading": "threading",
            "configparser": "configparser",

            # -----------------------

            "numpy": "numpy",
            "geopy": "geopy",
            "discord": "discord",
            "requests": "requests",
            "geocoder": "geocoder"
        }
        self.__integrated_modules       =           {
            "os": "os",
            "sys": "sys",
            "time": "time",
            "json": "json",
            "math": "math",
            "random": "random",
            "pickle": "pickle",
            "sqlite3": "sqlite3",
            "datetime": "datetime",
            "itertools": "itertools",
            "threading": "threading",
            "configparser": "configparser"
        }

        self.project_modules            =           []

        self.__TRIES                    =           5

        # ------------------------------------ Creating data folder with log file  ------------------------------------

        if not os.path.exists(str(self.__directory[0])):
            self.__missing_directory.append(str(self.__directory[0]))
            self.__missing_file.append(str(self.__file[0]))

            for i in range(self.__TRIES):
                try: os.makedirs(str(self.__directory[0]))
                except: pass
                else: break

            else: raise CannotCreateDirectory(str(self.__directory[0]))

            # ---------------------------------------- Creating logs.log file  ----------------------------------------

            for i in range(self.__TRIES):
                try: self.__log = open(str(self.__file[0]), "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(str(self.__file[0]))

        # ------------------------------------------ Creating logs.log file  ------------------------------------------

        if not os.path.exists(str(self.__file[0])):
            self.__missing_file.append(str(self.__file[0]))

            for i in range(self.__TRIES):
                try: self.__log = open(str(self.__file[0]), "w")
                except: pass
                else:
                    self.__log.close()
                    break

            else: raise CannotCreateFile(str(self.__file[0]))

        # ---------------------------------- Importing import_module from importlib -----------------------------------

        from importlib import import_module

        # ---------------------------------------- Dynamicly importing modules ----------------------------------------

        for module in self.__modules:
            try: globals()[str(module)] = import_module(str(module))
            except: self.__missing_module.append(str(module))

        for module in os.listdir("src"):
            if not os.path.isdir(str(module)):
                if str(module)[-3:] == ".py" and not str(module) == "__init__.py" and not str(module) == "GuardianComponent.py":
                    self.project_modules.append(str(module)[:-3])

        for module in self.project_modules:
            try: globals()[str(module)] = import_module("src", str(module))
            except:
                with open(str(self.__file[0]), "a") as f:
                    f.write(str(self.__make_log(err = "0x7E", arg = str(module))))

        # --------------------------------------- Installing addnotical modules ---------------------------------------

        if len(self.__missing_module):
            os.system("sudo apt install python3-pip")

            while len(self.__missing_module) > 0:
                with open(str(self.__file[0]), "a") as f:
                    f.write(str(self.__make_log(err = "0x7E", arg = str(module))))

                if not self.__missing_module[0] in self.__integrated_modules:
                    for i in range(self.__TRIES):
                        try: os.system("pip3 install {}".format(str(self.__missing_module[0])))
                        except: pass
                        else:
                            try: globals()[str(self.__missing_module[0])] = import_module(str(self.__missing_module[0]))
                            except: raise ModuleImportFailure(str(self.__missing_module[0]))
                            else: self.__missing_module.pop(0)

                else: raise CannotInstallIntagratedModule(str(self.__missing_module[0]))

        # ------------------------------------- Adding missing directoris to list -------------------------------------

        for dir in self.__directory:
            if not os.path.exists(str(dir)):
                self.__missing_directory.append(str(dir))

        for file in self.__file:
            if not os.path.exists(str(file)):
                self.__missing_file.append(str(file))

        # --------------------------------------- Adding missing files to list ----------------------------------------

        while len(self.__missing_directory) > 0:
            with open(str(self.__file[0]), "a") as f:
                f.write(str(self.__make_log(err = "0x3", arg = str(self.__missing_directory[0]))))

            if not os.path.exists(str(self.__missing_directory[0])):
                for i in range(self.__TRIES):
                    try: os.makedirs(str(self.__missing_directory[0]))
                    except: pass
                    else: break

                else: raise CannotCreateDirectory(str(self.__missing_directory[0]))

            self.__missing_directory.pop(0)

        while len(self.__missing_file) > 0:
            with open(str(self.__file[0]), "a") as f:
                f.write(str(self.__make_log(err = "0x2", arg = str(self.__missing_file[0]))))

            if not os.path.exists(str(self.__missing_file[0])):
                for i in range(self.__TRIES):
                    try: temp = open(str(self.__missing_file[0]), "w")
                    except: pass
                    else:
                        temp.close()
                        del temp
                        break

                else: raise CannotCreateFile(str(self.__missing_file[0]))

            self.__missing_file.pop(0)

        # -------------------------------------------------- Thread ---------------------------------------------------

        class ThreadClass(threading.Thread):
            def __create_config(self):
                config = configparser.ConfigParser()

                config["SETTINGS"] = {
                    "timeaftercycle": "5",
                    "numberoftries": "5"
                }

                config["INFO"] = {
                    "cyclesprocessed": "0",
                    "eventsencountered": "0"
                }

                with open("config/_thread.ini", "w") as f:
                    config.write(f)

            def __init__(self):
                threading.Thread.__init__(self)

                self.__missing_file             =           []
                self.__missing_directory        =           []
                self.__missing_module           =           []

                self.__directory                =           [
                    "data", "data/database", "data/backup",
                    "config"
                ]
                self.__file                     =           [
                    "data/logs.log", "data/dirs.pkl",
                    "data/files.pkl", "config/_thread.ini"
                ]

                self.__IS_RUNNING               =           False
                self.__SLEEP_TIME               =           5
                self.__TRIES                    =           5

                self.__CYCLES_PROCESSED         =           0
                self.__EVENT_ENCOUNTERED        =           0


                # ------------------------------------------- Thread Config -------------------------------------------

                config = configparser.ConfigParser()

                try:
                    config.read("config/_thread.ini")
                    self.__SLEEP_TIME = config["SETTINGS"].getfloat("timeaftercycle")
                except: self.__create_config()
                else:
                    self.__SLEEP_TIME               =           config["SETTINGS"].getfloat("timeaftercycle")
                    self.__TRIES                    =           config["SETTINGS"].getint("numberoftries")
                    self.__CYCLES_PROCESSED         =           config["INFO"].getint("cyclesprocessed")
                    self.__EVENT_ENCOUNTERED        =           config["INFO"].getint("eventsencountered")

            def __make_log(self, lvl = "warning", err = "0x0", arg = "None", date = True):

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

                        if not os.path.exists(str(self.__directory[0])):
                            self.__missing_directory.append(str(self.__directory[0]))
                            self.__missing_file.append(str(self.__file[0]))

                            for i in range(self.__TRIES):
                                try: os.makedirs(str(self.__directory[0]))
                                except: pass
                                else: break

                            else: raise CannotCreateDirectory(str(self.__directory[0]))

                            # ------------------------------------------------------------------------------------------

                            for i in range(self.__TRIES):
                                try: self.__log = open(str(self.__file[0]), "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(str(self.__file[0]))

                        # ---------------------------------- Creating logs.log file  ----------------------------------

                        if not os.path.exists(str(self.__file[0])):
                            self.__missing_file.append(str(self.__file[0]))

                            for i in range(self.__TRIES):
                                try: self.__log = open(str(self.__file[0]), "w")
                                except: pass
                                else:
                                    self.__log.close()
                                    break

                            else: raise CannotCreateFile(str(self.__file[0]))

                        # ------------------------------------- Opening logs file -------------------------------------

                        for i in range(self.__TRIES):
                            try: self.__log = open(str(self.__file[0]), "a")
                            except: pass
                            else: break

                        else: raise CannotCreateFile(str(self.__file[0]))

                        # -------------------------------- Opening data/dirs.pkl file ---------------------------------

                        for i in range(self.__TRIES):
                            try: self.__directory_list = open(str(self.__file[1]), "rb")
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
                                    self.__log.write(str(self.__make_log(err = "0x1E", arg = str(self.__file[1]))))
                                    os.remove(str(self.__file[1]))

                                break

                        else:
                            self.__log.write(str(self.__make_log(err = "0x1E", arg = str(self.__file[1]))))
                            os.remove(str(self.__file[1]))

                        # -------------------------------- Opening data/files.pkl file --------------------------------

                        for i in range(self.__TRIES):
                            try: self.__file_list = open(str(self.__file[2]), "rb")
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
                                    self.__log.write(str(self.__make_log(err = "0x1E", arg = str(self.__file[2]))))
                                    os.remove(str(self.__file[2]))

                                break

                        else:
                            self.__log.write(str(self.__make_log(err = "0x1E", arg = str(self.__file[2]))))
                            os.remove(str(self.__file[2]))

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
                                                self.log.write(make_dump_log("0x3", str(d)))

                        # ------------------------- Deleting duplicated content from the list -------------------------

                        self.__directory = list(dict.fromkeys(self.__directory))
                        self.__file = list(dict.fromkeys(self.__file))

                        # ----------------------------- Adding missing directoris to list -----------------------------

                        for dir in self.__directory:
                            if not os.path.exists(str(dir)):
                                self.__missing_directory.append(str(dir))

                        for file in self.__file:
                            if not os.path.exists(str(file)):
                                self.__missing_file.append(str(file))

                        # -------------------------------- Creating missing directoris --------------------------------

                        while len(self.__missing_directory) > 0:
                            self.__log.write(str(self.__make_log(err = "0x3", arg = str(self.__missing_directory[0]))))

                            for i in range(self.__TRIES):
                                try: os.makedirs(str(self.__missing_directory[0]))
                                except: pass
                                else: break

                            else: raise CannotCreateDirectory(str(self.__missing_directory[0]))

                            self.__missing_directory.pop(0)

                        # ---------------------------------- Creating missing files -----------------------------------

                        while len(self.__missing_file) > 0:
                            self.__log.write(str(self.__make_log(err = "0x2", arg = str(self.__missing_file[0]))))

                            for i in range(self.__TRIES):
                                try: temp = open(str(self.__missing_file[0]), "w")
                                except: pass
                                else:
                                    temp.close()
                                    del temp
                                    break

                            else: raise CannotCreateDirectory(str(self.__missing_file[0]))

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
