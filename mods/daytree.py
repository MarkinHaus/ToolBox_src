from typing import Union
from pydantic import BaseModel
import datetime

from scipy.constants import day

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
                    ["get_bucket_today", "Day Tree designer jo"],
                    ["get_bucket_week", "Day Tree designer jo"],
                    ["save_task_day", "Day Tree designer jo"],
                    ["save_task_week", "Day Tree designer jo"],
                    ],
            "name": "daytree",
            "Version": self.show_version,
            "designer_input": self.designer_input,
            "save_task_to_bucket": self.save_task_to_bucket,
            "get_bucket_today": self.get_bucket_today,
            "get_bucket_week": self.get_bucket_week,
            "save_task_day": self.save_task_day,
            "save_task_week": self.save_task_week,
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

        self._load_save_db(app, f"bucket::{uid}", [command[0].data["task"]])

        return "Don"

    def _load_save_db(self, app: App, db_key, data):
        bucket = app.MOD_LIST["DB"].tools["get"]([f"dayTree::{db_key}"], app)
        if bucket == "":
            bucket = []
        else:
            bucket = eval(bucket)

        for elm in data:
            bucket.append(elm)

        app.MOD_LIST["DB"].tools["set"](["", f"dayTree::{db_key}", str(bucket)])
        return bucket

    def _dump_bucket(self, app: App, uid):

        bucket = app.MOD_LIST["DB"].tools["get"]([f"dayTree::bucket::{uid}"], app)  # 1 bf bl
        if bucket == "":
            bucket = []
        else:
            bucket = eval(bucket)
            app.MOD_LIST["DB"].tools["set"](["", f"dayTree::bucket::{uid}", str([])])

        self.print("bucket - len : ", len(bucket))
        tx, wx = self._sort_tx_wx(bucket)
        return self._append_tx_wx(app, uid, tx, wx)

    @staticmethod
    def _sort_tx_wx(bucket):
        wx, tx = [], []
        for task in bucket:
            if "time" in task["att"]:
                wx.append(task)
            elif "uhr" in task["att"]:
                wx.append(task)
            elif "Time" in task["att"]:
                wx.append(task)
            elif "Uhr" in task["att"]:
                wx.append(task)
            else:
                tx.append(task)
        return tx, wx

    def _append_tx_wx(self, app, uid, tx, wx):
        wx = self._load_save_db(app, f"wx::{uid}", wx)
        tx = self._load_save_db(app, f"tx::{uid}", tx)
        return tx, wx

    def _get_day_x(self, wx, tx):
        self.print("")
        day = []
        if len(wx) >= 10:
            day.append(wx[::-1][:10])
            wx = wx[:10]
        else:
            day.append(wx[::-1])
            wx = []
        if len(tx) >= 10:
            day.append(tx[::-1][:10])
            tx = tx[:10]
        else:
            day.append(tx[::-1])
            tx = []
        return day, wx, tx

    def _cal_n_day(self, tx, wx):
        # day_num = datetime.datetime.today().weekday()
        # kw = list(datetime.datetime.today().isocalendar())[1]
        day = []
        self.print("Ezy mode")
        if len(tx) >= 13:
            tx = tx[::-1]
            self.print(f"{tx[0]=}")
            day = tx[:10]
        else:
            tx = tx[::-1]
            i = 0
            for t in tx:
                if i >= 2:
                    break
                self.print(f"i:{i}tx={t}")
                i += 1
            day = tx
        return day

    def _cal_n_week(self, tx, wx):
        # day_num = datetime.datetime.today().weekday()
        # kw = list(datetime.datetime.today().isocalendar())[1] # _cal_n_day

        week = []
        for i in range(0, 7):
            # if len(wx) == 0: # add repeatig task
            #    add_(i+1)
            if len(wx) >= 10:
                week.append(wx[::-1][:10])
                wx = wx[:10]
            else:
                week.append(wx[::-1])
                wx = []
            if len(tx) >= 10:
                week.append(tx[::-1][:10])
                tx = tx[:10]
            else:
                week.append(tx[::-1])
                tx = []
        return week

    def get_bucket_today(self, command, app: App):
        uid, err = self.get_uid(command, app)
        if err:
            return uid

        tx, wx = self._dump_bucket(app, uid)
        day, tx, wx = self._get_day_x(wx, tx)
        for task in self._cal_n_day(tx, wx):
            day.append(task)

        return day

    def get_bucket_week(self, command, app: App):
        uid, err = self.get_uid(command, app)
        if err:
            return uid

        tx, wx = self._dump_bucket(app, uid)
        week = []
        for i in range(0, 6):
            day, tx, wx = self._get_day_x(wx, tx)
            week.append(day)

        return week

    def get_uid(self, command, app: App):
        if "CLOUDM" not in list(app.MOD_LIST.keys()):
            return "Server has no cloudM module"

        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        res = app.MOD_LIST["CLOUDM"].tools["validate_jwt"](command, app)

        if type(res) is str:
            return res, True

        return res["uid"], False

    def save_task_day(self, command, app: App):

        data = command[0].data
        uid, err = self.get_uid(command, app)

        if err:
            return uid

        day = data["task"]

        if len(day) == 0:
            tx, wx = self._dump_bucket(app, uid)
            day, tx, wx = self._get_day_x(wx, tx)
            for task in self._cal_n_day(tx, wx):
                day.append(task)
            self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::tx::{uid}", str(tx)]))
            self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::wx::{uid}", str(wx)]))

        return day

    def save_task_week(self, command, app: App):

        data = command[0].data
        uid, err = self.get_uid(command, app)

        if err:
            return uid

        week = data["week"]
        self.print("Lazy save_task_week")
        # tx = []
        # for i in range(0, 7):
        #     tx = self.r_twx(app, uid)

        tx, wx = [], []
        for i, day in enumerate(week):
            self.print(f"sorting:{i} - len {len(day)}")
            _tx, _wx = self._sort_tx_wx(day)
            for t in _tx:
                tx.append(t)

        self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::tx::{uid}", str(tx)]))
        self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::week::{uid}", str(week)]))

        return "week"

    def r_twx(self, app, uid):
        tx = self._get_twx("t", app, uid)
        if len(tx) >= 10:
            tx = tx[:10]
            return tx
        return []

    def _get_twx(self, c, app, uid):
        cx = app.MOD_LIST["DB"].tools["get"]([f"dayTree::{c}x::{uid}"], app)
        self.print(f"{c}x={cx}")
        if cx == "":
            cx = []
        else:
            cx = eval(cx)
        return cx
