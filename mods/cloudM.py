from mods.mainTool import MainTool, FileHandler
from Style import Style
from importlib import import_module
from pathlib import Path


class Tools(MainTool, FileHandler):

    def __init__(self, logs=None):
        self.version = "0.2.0"
        self.name = "cloudM"
        self.logs = logs
        self.color = "CYAN"
        self.keys = {
            "DM": "def-mods~~",
            "HIS": "comm-his~~"
        }
        self.add = []
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["ADD", "adds a mod to default load"],
                    ["REM", "remove a mod from default load"],
                    ["NEW", "crate a boilerplate file to make a new mod"],
                    ["LIST", "list all automatically loaded modules"],
                    ["download", "download a mod from MarkinHaus server ", Style.RED("NOT IMPLEMENTED")],
                    ["update", "update a mod from MarkinHaus server ", Style.RED("NOT IMPLEMENTED")],
                    ],
            "name": "cloudM",
            "Version": self.show_version,
            "ADD": self.add_module,
            "REM": self.rem_module,
            "LIST": self.list_mods,
            "NEW": self.new_module,
        }

        FileHandler.__init__(self, "modules.config")

        MainTool.__init__(self, load=self.load_open_file, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def load_open_file(self):
        self.open_l_file_handler()
        self.load_file_handler()

    def on_exit(self):
        self.open_s_file_handler()
        self.add_to_save_file_handler(self.keys["DM"], str(self.add))
        self.save_file_handler()
        self.file_handler_storage.close()

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
            self.print("NEW MODULE: "+mod_name, end=" ")

            fle = Path("mods/"+mod_name+".py")
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

    def show_version(self):
        self.print("Version: ", self.version)

