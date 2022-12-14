import os
from mods.mainTool import MainTool, FileHandler, App
from Style import Style


class Tools(MainTool, FileHandler):  # FileHandler

    def __init__(self, app=None):
        self.version = "0.0.2"
        self.name = "dev_tool_manager"
        self.logs = app.logs_ if app else None
        self.color = "GREYBG"
        self.keys = {
            "DEV": "dev~config"
        }
        self.api_config = {}
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["edit-st-tool", ""],
                    ["start-st-tool", ""],
                    ["stop-st-tool", ""],
                    ["restart-st-tool", ""],
                    ["delete-st-tool", ""],
                    ["info", ""],
                    ],
            "name": "api_manager",
            "Version": self.show_version,
            "edit-st-tool": self.new_sd,
            "start-st-tool": self.start_sd,
            "stop-st-tool": self.stop_sd,
            "info": self.info,
            "restart-api": self.restart_sd,

        }
        FileHandler.__init__(self, "dev-tool.data", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)

    def info(self):
        for api in list(self.api_config.keys()):
            self.print(f"Name: {api}")
            self.print(self.api_config[api])
        return self.api_config

    def new_sd(self, command):
        if len(command) <= 2:
            return "invalid command length [api:name mod_list]"

        self.api_config[command[1]] = {"Name": command[1], "Modules": command[1:], "version": self.version}

    def load_api_mods(self, load_mod, api_name):
        default_modules = self.api_config[api_name]["Modules"]

        print(default_modules)

        if type(default_modules) is list and len(default_modules) > 0:
            for i in default_modules:
                self.print(f"Loading module {i} : ", end='')
                try:
                    self.log(f"Open mod {i}")
                    load_mod(i)
                except Exception as e:
                    print(Style.RED("Error") + f" loading modules : {e}")
                    self.log(f"Error mod {i}")

    def start_sd(self, command, app: App):
        if len(command) < 1:
            return "invalid command length [name]"
        api_name = command[1]
        if not api_name in list(self.api_config.keys()):
            return f"invalid api name {api_name} : {list(self.api_config.keys())}"

        api_data = self.api_config[api_name]

        self.print(app.pretty_print(api_data))
        g = f"streamlit run dev_tool.py ata:{api_name}.config:{api_name}" # --server.enableCORS=false --server.port=80 (--server.ip=80)?

        os.system(g)
        print(g)

    def stop_sd(self, command, app: App):
        pass

    def restart_sd(self, command, app: App):
        pass

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()
        config = self.get_file_handler(self.keys["DEV"])
        if config is not None:
            self.api_config = eval(config)

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["DEV"], str(self.api_config))

        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()



