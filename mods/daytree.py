from typing import Union
from pydantic import BaseModel
from datetime import datetime
import uuid
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
                    ["due_kwd", "Day Tree designer jo"],
                    ],
            "name": "daytree",
            "Version": self.show_version,
            "designer_input": self.designer_input,
            "save_task_to_bucket": self.save_task_to_bucket,
            "get_bucket_today": self.get_bucket_today,
            "get_bucket_week": self.get_bucket_week,
            "save_task_day": self.save_task_day,
            "save_task_week": self.save_task_week,
            "due_kwd": self.due_date_to_kwd,
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
                                    "Ich muss eine Bestimmte aufgebe Erledigen, es handelt sich um eine Aufgabe."],

                           'vg_list': {'time': ['time', 'uhr', 'zeit'],
                                       'due_date': ['due_date', 'datum', 'date'],
                                       'day': ['tag', 'day'],
                                       'week': ['week', 'kw'],
                                       'priority': ['priority', 'P#', '!'],
                                       'cal': ['cal'], }
                           }
        # TODO : Config Editor
        self.config['vg_list'] = {'time': ['time', 'uhr', 'zeit'],
                                  'due_date': ['due_date', 'datum', 'date'],
                                  'day': ['tag', 'day'],
                                  'week': ['week', 'kw'],
                                  'priority': ['priority', 'P#', '!'],
                                  'cal': ['cal'], }

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
            try:
                bucket = eval(bucket)
            except TypeError:
                return "bucket-error-eval failed"
            app.MOD_LIST["DB"].tools["set"](["", f"dayTree::bucket::{uid}", str([])])

        self.print("bucket - len : ", len(bucket))

        tx, wx = self._sort_tx_wx(bucket)
        return self._append_tx_wx(app, uid, tx, wx)

    def _sort_tx_wx(self, bucket):
        wx, tx = [], []

        for task in bucket:
            wx_task = self._wx_format_task(task)
            cal = self._calculate_cal(wx_task, [0, 0])
            if cal > 0:
                wx.append(task)
            else:
                tx.append(task)

        return tx, wx

    def _wx_format_task(self, task):
        # -> {name: "dings", }

        # Lambda-Funktion zum Hinzufügen von Eigenschaften zu einem Task-Objekt
        add_properties = lambda task, vg_ob: {
            'id': str(uuid.uuid4()).replace('-', '')[10],  # Zufällige UID generieren

            # Schleife über die Eigenschaften in vg_ob
            **{prop: next(filter(lambda x: x['t'] in vg_ob[prop], task['att']), {'v': 0})['v']
               for prop in vg_ob.keys()},

            **task  # Restliche Eigenschaften aus task übernehmen
        }

        return add_properties(task, self.config['vg_ob'])

    def _calculate_cal(self, item, r):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        priority = item['priority'] if 'priority' in item.keys() else 0
        kw = int(datetime.strptime(item['due_date'], '%Y-%m-%d').strftime('%W')) if 'due_date' in item.keys() else (
            item['week'] if 'week' in item.keys() else 0)
        day = int(days.index(
            datetime.strptime(item['due_date'], '%Y-%m-%d').strftime('%A'))) if 'due_date' in item.keys() else (
            item['day'] if 'day' in item.keys() else -1)

        now = datetime.now()
        # Kalenderwoche und Tag aus dem Datetime-Objekt extrahieren

        day_rel = day - days.index(now.strftime('%A')) + r[0]  # day_now
        kw_rel = kw - int(now.strftime('%W')) + r[1]  # kw_now

        return 1 + priority + (kw_rel * 10) + day_rel

    def _sort_wx(self, wx, r):
        if r is None:
            r = [0, 0]
        todo_list_formatted = [
            {
                'name': item['name'],
                'index': i,
                'id': item['id'] if 'id' in item.keys() else 0,
                'priority': item['priority'] if 'priority' in item.keys() else 0,
                'cal': self._calculate_cal(item, r),
            }
            for i, item in enumerate(wx)
        ]
        key = lambda x: (x['cal'] < 0, x['cal'], (x[
                                                      'time'] / 100 if 'time' in x.keys() else 0))  # lambda x: (x['cal'], (x['time'] / 100 if 'time' in x.keys() else 0))

        sorted_list = sorted(todo_list_formatted,
                             key=key)
        return sorted_list

    def due_date_to_kwd(self, command, app: App):

        data = command[0].data
        uid, err = self.get_uid(command, app)

        if err:
            return uid

        due_date = data["due_date"]
        # Fälligkeitsdatum als Datetime-Objekt umwandeln
        due_date_dt = datetime.strptime(due_date, '%Y-%m-%d')

        # Kalenderwoche und Tag aus dem Datetime-Objekt extrahieren
        week = due_date_dt.strftime('%W')
        day = due_date_dt.strftime('%A')
        return week, day

    def _append_tx_wx(self, app, uid, tx, wx):
        wx = self._load_save_db(app, f"wx::{uid}", wx)
        tx = self._load_save_db(app, f"tx::{uid}", tx)
        return wx, tx

    def _get_day_x(self, wx, tx, x):
        day, ts = [], []

        wx_now = self._sort_wx(wx, [x[0], x[1]])

        if len(tx) > x[2] - 1:
            ts.append(tx[:x[2]])
            tx = tx[:x[2]]
        else:
            ts.append(tx)
            tx = []

        if len(wx_now) > x[2] - 1:
            wx_now_x_ids = [
                item["index"]
                for item in wx_now[:x[2]]
            ]
            # Lambda-Funktion zum Filtern der Task-Objekte nach den IDs
            filter_tasks = lambda ids, tasks: list(filter(lambda task: task['index'] in ids, tasks))
            wx_x = filter_tasks(wx_now_x_ids, wx)
            ts.append(wx_x)
            for index in wx_now_x_ids:
                wx.remove(wx[index])
        else:
            ts.append(wx_now)
            wx = []

        for t in ts:
            day.append(t)

        return day, wx, tx

    def get_bucket_today(self, command, app: App):
        uid, err = self.get_uid(command, app)
        if err:
            return uid

        day = self._load_save_db(app, f"day::{uid}", [])

        if len(day) == 0:
            wx, tx = self._dump_bucket(app, uid)
            day, _, _ = self._get_day_x(wx, tx, [0, 0, 10])

        return day

    def get_bucket_week(self, command, app: App):
        uid, err = self.get_uid(command, app)
        if err:
            return uid

        wx, tx = self._dump_bucket(app, uid)
        week = []
        print(f"{tx=}\n{wx=}")
        for i in range(1, 8):
            week.append([])
            if len(wx) != 0 or len(tx) != 0:
                day, tx, wx = self._get_day_x(wx, tx, [i - 1, 0, 10])
                print(f"{tx=}\n{wx=}\n{day=}")
                for t in day:
                    week[i - 1].append(t)

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
            wx, tx = self._dump_bucket(app, uid)
            day, wx, tx = self._get_day_x(wx, tx, [0, 0, 10])
            self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::tx::{uid}", str(tx)]))
            self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::wx::{uid}", str(wx)]))
            self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::day::{uid}", str(day)]))
        elif len(day) == 10:
            return day

        self.print(app.MOD_LIST["DB"].tools["set"](["", f"dayTree::day::{uid}", str(day)]))
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
