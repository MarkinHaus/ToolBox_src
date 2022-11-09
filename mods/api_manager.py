import os
from platform import system

from mods.mainTool import MainTool, FileHandler, App
from Style import Style


class Tools(MainTool, FileHandler):  # FileHandler

    def __init__(self, logs=None):
        self.version = "0.0.1"
        self.name = "api_manager"
        self.logs = logs
        self.color = "WHITE"
        self.keys = {
            "Apis": "api~config"
        }
        self.api_config = {}
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["edit-api", ""],
                    ["start-api", ""],
                    ["stop-api", ""],
                    ["restart-api", ""],
                    ["delete-api", ""],
                    ["info", ""],
                    ],
            "name": "api_manager",
            "Version": self.show_version,
            "edit-api": self.new_api,
            "start-api": self.start_api,
            "stop-api": self.stop_api,
            "info": self.info,
            "restart-api": self.restart_api,

        }
        FileHandler.__init__(self, "api-m.data")
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)

    def info(self, command, app: App):
        app.pretty_print(app.command_viewer(self.api_config))

    def new_api(self, command):
        if len(command) <= 4:
            return "invalid command length [api:name host port mod_list]"
        host = command[2]
        if host == "lh":
            host = "127.0.0.1"
        if host == "0":
            host = "0.0.0.0"
        port = command[3]
        if port == "0":
            port = "8000"
        mod_list = command[5:]
        self.api_config[command[1]] = {"Name": command[1], "Modules": mod_list, "version": self.version,
                                       "port": port, "host": host}

    def load_api_mods(self, load_mod, api_name):
        default_modules = self.api_config[api_name]["Modules"]

        print(default_modules)

        if type(default_modules) is list and len(default_modules) > 0:
            for i in default_modules:
                self.print(f"Loading module : ", end='')
                try:
                    load_mod(i)
                    self.log(f"Open mod {i}")
                except Exception as e:
                    print(Style.RED("Error") + f" loading modules : {e}")
                    self.log(f"Error mod {i}")

    def start_api(self, command, app: App):
        if len(command) <= 2:
            return "invalid command length [name debug:live]"
        api_name = command[1]
        debug = command[2] == "debug"
        if not api_name in list(self.api_config.keys()):
            return f"invalid api name {api_name} : {list(self.api_config.keys())}"

        api_data = self.api_config[api_name]

        self.print(app.pretty_print(api_data))
        g = f"uvicorn api:app --host {api_data['host']} --port {api_data['port']}  --header api:{api_name}.config:{api_name}"
        os.system(g)
        print(g)

    def stop_api(self, command, app: App):
        pass

    def restart_api(self, command, app: App):
        pass

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()
        config = self.get_file_handler(self.keys["Apis"])
        if config is not None:
            self.api_config = eval(config)

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["Apis"], str(self.api_config))

        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()
