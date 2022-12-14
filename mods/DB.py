from mods.mainTool import MainTool, FileHandler, App
from Style import Style
import redis


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.0.1"
        self.name = "DB"
        self.logs = app.logs_ if app else None
        self.color = "YELLOWBG"
        self.keys = {
            "url": "redis:url~"
        }
        self.encoding = 'utf-8'
        self.rcon = None
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["first-redis-connection", "set up a web connection to MarkinHaus"],
                    ["get", "get key and value from redis"],
                    ["set", "set key value pair redis"],
                    ["del", "set key value pair redis"],
                    ["all", "get all (Autocompletion helper)"],
                    ["all-k", "get all-k (get all keys) (Autocompletion helper)"]
                    ],
            "name": "DB",
            "Version": self.show_version,
            "first-redis-connection": self.add_url_con,
            "get": self.get_keys,
            "set": self.set_key,
            "del": self.delete_key,

        }
        FileHandler.__init__(self, "db.data", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()
        version_command = self.get_file_handler(self.keys["url"])
        if version_command is not None:
            self.rcon = redis.from_url(version_command)
        else:
            self.print("No url found pleas run first-redis-connection")

    def on_exit(self):
        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()

    def add_url_con(self):
        url = input("Pleas enter URL of Redis Backend default: ")
        self.add_to_save_file_handler(self.keys["url"], url)
        self.rcon = redis.from_url(url)

    def get_keys(self, command_, app: App):

        command = command_[0]
        if command == "get":
            command = command_[1]

        if command == "all":
            for key in self.rcon.scan_iter():
                val = self.rcon.get(key)
                self.print(f"{key} = {val}")
        elif command == "all-k":
            for key in self.rcon.scan_iter():
                self.rcon.get(key)
                self.print(f"{key}")
        else:
            val = ""
            for key in self.rcon.scan_iter(command):
                val = self.rcon.get(key)

            # self.print(self.check(command, app), val, app.id)
            if self.check(command, app):
                return val
        return command

    def check(self, request, app: App):
        if app.id == "tb.config":
            return True
        return True  # not "secret".upper() in request.upper()

    def set_key(self, ind):

        if len(ind) == 3:
            key = ind[1]
            val = ind[2]
            self.rcon.set(key, val)

            self.print(f"key: {key} value: {val} DON")

    def delete_key(self, ind):

        if len(ind) == 2:
            key = ind[1]
            e = self.rcon.delete(key)
            self.print(f"{e}]")
            self.print(f"key: {key} DEL")

        if len(ind) == 3:
            key_ = ind[1]
            all = ind[2] == "*"
            if all:
                # Use the scan method to iterate over all keys
                for key in self.rcon.scan_iter():
                    # Check if the key contains the substring
                    self.print(f"test: {key} ", end="")
                    if key_ in str(key, 'utf-8'):
                        # Delete the key if it contains the substring
                        self.rcon.delete(key)
                        self.print(f"DEL")
            self.print(f"Finished")

        self.print(f"function end")
