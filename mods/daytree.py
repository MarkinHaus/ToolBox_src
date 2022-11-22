from typing import Union
from pydantic import BaseModel

from mods.mainTool import MainTool, FileHandler, App
from Style import Style


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.0.1"
        self.name = "daytree"
        self.logs = app.logs_ if app else None
        self.color = "BEIGE2"
        self.keys = {"Config": "config~~~:",
                     "Bucket": "bucket~~~:"}
        self.config = {}
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["designer_input", "Day Tree designer input Stream"],
                    ["save_task_to_bucket", "Day Tree designer jo"],
                    ],
            "name": "daytree",
            "Version": self.show_version,
            "designer_input": self.designer_input,
            "save_task_to_bucket": self.save_task_to_bucket,
        }
        FileHandler.__init__(self, "daytree.config", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()
        config = self.get_file_handler(self.keys["Config"])
        if config is not None:
            self.config = eval(config)
        else:
            self.config = {"Modi": ["Ich mus um eine bestimmte Uhrzeit an einem bestimmten Ort mit oder ohne weitere "
                                    "Personen Besuchen, es handelt sich um einen Termin.",
                                    "Ich möchte mich an eine Sache oder Tätigkeit erinnern, es handelt sich um eine "
                                    "Erinnerung.",
                                    "Ich muss eine Bestimmte aufgebe Erledigen, es handelt sich um eine Aufgabe."]}

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["Config"], str(self.config))
        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()

    def designer_input(self, command, app: App):
        if "ISAA" not in list(app.MOD_LIST.keys()):
            return "Server has no ISAA module"
        if len(command) > 2:
            return {"error": f"Command-invalid-length {len(command)=} | 2 {command}"}

        uid, err = self.get_uid(command, app)

        if err:
            return uid

        data = command[0].data
        self.print(data["input"])

        # end =  app.MOD_LIST["ISAA"].tools["validate_jwt"](command, app)

        # task.att = [["test", "test"]]

        att_list = []
        att_test = {'v': 'test', 't': 'test'}
        att_list.append(att_test)
        return att_list

    def save_task_to_bucket(self, command, app: App):

        if len(command) > 2:
            return {"error": f"Command-invalid-length {len(command)=} | 2 {command}"}

        uid, err = self.get_uid(command, app)
        if err:
            return uid

        bucket = app.MOD_LIST["DB"].tools["get"](["-", f"dayTree::bucket::{uid}"], app)
        print(bucket)
        if bucket == "":
            bucket = []
        else:
            bucket = eval(bucket)

        bucket.append(command[0].data["task"])

        app.MOD_LIST["DB"].tools["set"](["", f"dayTree::bucket::{uid}", str(bucket)])

        return "Don"

    def get_uid(self, command, app: App):
        if "CLOUDM" not in list(app.MOD_LIST.keys()):
            return "Server has no cloudM module"

        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        res = app.MOD_LIST["CLOUDM"].tools["validate_jwt"](command, app)

        if type(res) is str:
            return res, True

        return res["uid"], False

    def save_inbox_api(self, command, app: App):

        data = command[0].data
        uid, err = self.get_uid(command, app)

        if err:
            return uid

        return app.MOD_LIST["DB"].tools["set"](["", f"dayTree::task::{uid}", data])

    def get_inbox_api(self, command, app: App):

        uid, err = self.get_uid(command, app)

        if err:
            return uid

        return app.MOD_LIST["DB"].tools["get"](["-", f"dayTree::task::{uid}"])
