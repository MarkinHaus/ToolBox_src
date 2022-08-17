import os
import threading

from mods.mainTool import MainTool, FileHandler
from Style import Style
from importlib import import_module
from pathlib import Path
import requests


class Tools(MainTool, FileHandler):

    def __init__(self, logs=None):
        self.version = "0.2.1"
        self.name = "cloudM"
        self.logs = logs
        self.color = "CYAN"
        self.keys = {
            "DM": "def-mods~~",
            "HIS": "comm-his~~",
            "URL": "comm-vcd~~",
        }
        self.add = []
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["ADD", "adds a mod to default load"],
                    ["REM", "remove a mod from default load"],
                    ["NEW", "crate a boilerplate file to make a new mod"],
                    ["LIST", "list all automatically loaded modules"],
                    ["download", "download a mod from MarkinHaus server"],
                    ["#update", "update a mod from MarkinHaus server ", Style.RED("NOT IMPLEMENTED")],
                    ["upload", "upload a mod to MarkinHaus server"],
                    ["first-web-connection", "set up a web connection to MarkinHaus"],
                    ],
            "name": "cloudM",
            "Version": self.show_version,
            "ADD": self.add_module,
            "REM": self.rem_module,
            "LIST": self.list_mods,
            "NEW": self.new_module,
            "upload": self.upload,
            "download": self.download,
            "first-web-connection": self.add_url_con,
        }

        FileHandler.__init__(self, "modules.config")

        MainTool.__init__(self, load=self.load_open_file, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def load_open_file(self):
        self.open_l_file_handler()
        self.load_file_handler()
        self.get_version()

    def on_exit(self):
        self.open_s_file_handler()
        self.add_to_save_file_handler(self.keys["DM"], str(self.add))
        self.save_file_handler()
        self.file_handler_storage.close()

    def show_version(self):
        self.print("Version: ", self.version)

    def get_version(self):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "http://127.0.0.1:8080/cloudM/version"
        if version_command != "None":
            url = version_command + "/cloudM/version"

        self.print(url)

        try:
            self.version = requests.get(url).json()["version"]
        except Exception:
            self.print(Style.RED("Error retrieving version information "))

        self.print("Version: %s" % self.version)

    def lode_mods(self, get_mod, set_info):
        default_modules = self.get_file_handler(self.keys["DM"])

        if default_modules:
            self.print("oping modules")
            try:
                default_modules = eval(default_modules)

            except SyntaxError and TypeError:
                self.print("Data default modules is corrupted")

        if type(default_modules) is list and len(default_modules) > 0:
            for i in default_modules:
                self.add.append(i)
                self.print(f"Loading module : ", end='')
                try:
                    set_info(get_mod(i))
                except Exception as e:
                    print(Style.RED("Error") + f" loading modules : {e}")

    def load_history(self):
        history = self.get_file_handler(self.keys["HIS"])

        if history:
            try:
                history = eval(history)

            except SyntaxError and TypeError:
                self.print("Data default modules is corrupted")

        self.print("open history len : " + str(len(history)))

        if type(history) is list and len(history) > 0:
            return history
        return []

    def save_history(self, history):
        self.add_to_save_file_handler(self.keys["HIS"], str(history))

    def add_module(self, module):
        do = False
        try:
            if len(module) == 2:
                import_module("mods." + module[1])
                do = True
            else:
                self.print((Style.YELLOW("SyntaxError : add module_name=File name")))
        except ModuleNotFoundError:
            self.print(Style.RED(f"Module {module[1]} not found"))
            return
        if do:
            self.add.append(module[1])
            self.print(Style.GREEN(f"Module {module[1]} successfully added"))

    def rem_module(self, module):
        do = False
        try:
            if len(module) == 2:
                import_module("mods." + module[1])
                do = True
            else:
                self.print((Style.YELLOW("SyntaxError : add module_name=File name")))
        except ModuleNotFoundError:
            self.print(Style.RED(f"Module {module[1]} not found"))
            return
        if do:
            self.add.remove(module[1])
            self.print(Style.GREEN(f"Module {module[1]} successfully removed"))

    def list_mods(self):
        for i in self.add:
            self.print("Module : " + i)

    def new_module(self, name):
        boilerplate = """from mods.mainTool import MainTool  # , FileHandler
from Style import Style

  
class Tools(MainTool):  # FileHandler

    def __init__(self, logs=None):
        self.version = "0.0.1"
        self.name = "NAME"
        self.logs = logs
        self.color = "WHITE"
        self.tools = {
            "all": [["Version", "Shows current Version"]],
            "name": "NAME",
            "Version": self.show_version,
        }
        # FileHandler.__init__(self, "File name")
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                    name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)
    def show_version(self):
        self.print("Version: ", self.version)

    def on_start(self):
        pass

    def on_exit(self):
        pass
"""
        if len(name) > 1:
            mod_name = name[1]
            self.print("NEW MODULE: " + mod_name, end=" ")

            fle = Path("mods/" + mod_name + ".py")
            fle.touch(exist_ok=True)
            mod_file = open(fle)

            if len(mod_file.read()) != 0:
                print(Style.Bold("!"))
                self.print(Style.RED("MODULE exists pleas use a other name"))
            else:
                mod_file = open(fle, "w")
                mod_file.writelines(
                    boilerplate.replace('NAME', mod_name)
                )

                mod_file.close()
                print("🆗")

    def upload(self, input_):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "http://127.0.0.1:8080/cloudM/upload"
        if version_command != "None":
            url = version_command + "/cloudM/upload"
        try:
            if len(input_) == 3:
                type_ = input_[1]
                name = input_[2]

                if not (type_ in ["mod", "aug", "text"]):
                    self.print((Style.YELLOW(f"SyntaxError : invalid type: {type_}  accept ar : [mod|aug|text]")))
                    return

                index = ["mod", "aug", "text"].index(type_)

                server_type = ["application/mod", "application/aug", "text/*"][index]
                path = ["mods/", "Augmentation/", "text/"][index]

                try:
                    file = open(path + name, "rb").read()
                except IOError:
                    self.print((Style.RED(f"File does not exist or is not readable: {path + name}")))
                    return

                if file:
                    data = {"filename": name,
                            "data": str(file, "utf-8"),
                            "content_type": server_type
                            }

                    try:
                        def do_upload():
                            r = requests.post(url, json=data)
                            self.print(r.status_code)
                            if r.status_code == 200:
                                self.print("DON")
                            self.print(r.content)

                        threa = threading.Thread(target=do_upload)
                        self.print("Starting upload threading")
                        threa.start()

                    except Exception as e:
                        self.print(Style.RED(f"Error uploading (connoting to server) : {e}"))

            else:
                self.print((Style.YELLOW(f"SyntaxError : upload [mod|aug|text] filename {input_}")))
        except Exception as e:
            self.print(Style.RED(f"Error uploading : {e}"))
            return

    def download(self, input_):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "http://127.0.0.1:8080/cloudM/static"
        if version_command != "None":
            url = version_command + "/cloudM/static"
        try:
            if len(input_) == 3:
                type_ = input_[1]
                name = input_[2]

                if not (type_ in ["mod", "aug", "text"]):
                    self.print((Style.YELLOW(f"SyntaxError : invalid type: {type_}  accept ar : [mod|aug|text]")))
                    return

                index = ["mod", "aug", "text"].index(type_)

                path = ["/mods/", "/Augmentation/", "/text/"][index]

                url += path + name

                try:
                    r = requests.get(url)
                    self.print(r.status_code)
                    filename = r.headers["content-disposition"].split('"')[-2]
                    open("." + path + filename, "a").write(str(r.content, "utf-8"))
                    self.print("saved temp file to: " + "." + path + filename)
                    self.print("file size: " + r.headers["content-length"])

                except Exception as e:
                    self.print(Style.RED(f"Error download (connoting to server) : {e}"))

            else:
                self.print((Style.YELLOW(f"SyntaxError : download [mod|aug|text] filename {input_}")))
        except Exception as e:
            self.print(Style.RED(f"Error download : {e}"))
            return

    def add_url_con(self):
        """
        Adds a url to the list of urls
        """

        addres = input("Pleas enter URL of CloudM Backend default: http://45.79.251.173/")
        if addres == "":
            addres = "http://45.79.251.173/"
        self.print(Style.YELLOW(f"Adding url : {addres}"))
        self.add_to_save_file_handler(self.keys["HIS"], str(addres))
