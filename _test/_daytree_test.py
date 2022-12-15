import datetime

from Style import Style
from _test._mainTool_test import get_app, app_clean_up
from _test._cloudM_test import test_create_user, delete_test_user, TestCommand


def get_app_day_tree_instance():
    app = get_app()

    app.load_mod("DB")
    app.load_mod("daytree")
    app.load_mod("cloudM")

    assert "DB" in app.MOD_LIST
    assert "DAYTREE" in app.MOD_LIST
    assert "CLOUDM" in app.MOD_LIST

    app.new_ac_mod("daytree")

    assert "daytree" in app.AC_MOD.name

    return app, app.AC_MOD


def test_load_save_db():
    # Test, ob die Funktion den Wert korrekt aus der Datenbank abruft
    app, dt = get_app_day_tree_instance()

    db_key = 'test'
    app.MOD_LIST["DB"].tools["del"](['', f"dayTree::{db_key}", '*'])
    assert app.MOD_LIST["DB"].tools["get"]([f"dayTree::{db_key}"], app) == ""

    # Test, ob die Befehle "get", "set" und "del" korrekt ausgeführt werden
    app.MOD_LIST["DB"].tools["set"](["", f"dayTree::{db_key}", str([1, 2, 3])])
    r = app.MOD_LIST["DB"].tools["get"]([f"dayTree::{db_key}"], app)
    print(r)
    assert r == b'[1, 2, 3]'
    # Test, ob die Daten korrekt hinzugefügt und gespeichert werden
    data = [4, 5, 6]
    bucket = dt._load_save_db(app, db_key, data)
    assert bucket == [1, 2, 3, 4, 5, 6]
    assert app.MOD_LIST["DB"].tools["get"]([f"dayTree::{db_key}"], app) == b'[1, 2, 3, 4, 5, 6]'

    app.MOD_LIST["DB"].tools["del"](['', f"dayTree::{db_key}", '*'])
    # Test, ob die Funktion die Daten am Ende korrekt löscht
    bucket = dt._load_save_db(app, db_key, [])
    assert bucket == []
    assert app.MOD_LIST["DB"].tools["get"]([f"dayTree::{db_key}"], app) == b"[]"
    app_clean_up(app)


def test_save_task_to_bucket():
    app, dt = get_app_day_tree_instance()
    user_data, token = test_create_user()

    t = TestCommand()
    t.token = token

    uid = app.AC_MOD.get_uid([t], app)
    # Test, ob die Funktion einen Fehler zurückgibt, wenn das erste Element des Befehls kein Dictionary mit dem
    # Schlüssel "token" und "data" enthält
    # commig soooooon

    # Test, ob die Funktion das erste Element des Befehls (den Task) korrekt in der Datenbank speichert

    t.data = {"task": ["task1"]}
    command = [t]
    result = dt.save_task_to_bucket(command, app)
    assert result == "Don"
    bucket_id = f"dayTree::bucket::{uid}"
    # b = app.MOD_LIST["DB"].tools["get"]([bucket_id], app)
    # print("#"*10,b, "ds")
    # assert b == b"[['task1']]"

    # Test, ob die Funktion die Einträge in der Datenbank am Ende korrekt löscht
    # app.MOD_LIST["DB"].tools["set"](["", bucket_id, "[['task1']]"])

    t.data = {"task": ["task2"]}
    command = [t]
    result = dt.save_task_to_bucket(command, app)
    # assert app.MOD_LIST["DB"].tools["get"]([bucket_id], app) == b"[['task1'],['task2']]"
    assert result == "Don"

    app.MOD_LIST["DB"].tools["del"](['', bucket_id, '*'])
    assert app.MOD_LIST["DB"].tools["get"]([bucket_id], app) == ""

    delete_test_user(app, user_data, uid)
    app_clean_up(app)

def test_wx_format_task():
    app, dt = get_app_day_tree_instance()

    # Test, ob die Funktion eine zufällige UID für jedes Task-Objekt generiert
    task1 = {"name": "Task 1", "att": [{"t": "v", "v": 1}]}
    task2 = {"name": "Task 2", "att": [{"t": "v", "v": 2}]}
    result1 = dt._wx_format_task(task1)
    result2 = dt._wx_format_task(task2)
    assert "id" in result1 and "id" in result2
    assert result1["id"] != result2["id"]

    # Test, ob die Funktion die Eigenschaften aus dem Objekt `vg_ob` korrekt dem Task-Objekt hinzufügt
    dt.config["vg_ob"] = {"prop1": ["v"], "prop2": ["w"]}
    task = {"name": "Task", "att": [{"t": "v", "v": 1}, {"t": "w", "v": 2}]}
    result = dt._wx_format_task(task)
    assert "prop1" in result and "prop2" in result
    assert result["prop1"] == 1 and result["prop2"] == 2

    # Test, ob die Funktion die restlichen Eigenschaften des Task-Objekts korrekt übernimmt
    task = {"name": "Task", "att": [{"t": "v", "v": 1}, {"t": "w", "v": 2}], "prop3": 3}
    result = dt._wx_format_task(task)
    assert "prop3" in result
    assert result["prop3"] == 3
    app_clean_up(app)

def test_calculate_cal():
    # Create an instance of the class that contains the _calculate_cal method
    _, dt = get_app_day_tree_instance()

    # Use the current date as the due date for tasks in the test
    current_date = datetime.datetime.now().date()

    # Test 1: Check if the function returns the expected result for a given input
    item = {'priority': 5, 'due_date': current_date + datetime.timedelta(days=0)}
    r = (0, 0)
    expected_output = 5 + 1

    assert dt._calculate_cal(item, r) == expected_output

    item = {'priority': 5, 'due_date': current_date + datetime.timedelta(days=-8)}
    r = (0, 0)
    expected_output = 0
    assert dt._calculate_cal(item, r) < expected_output

    # Test 2: Check if the function returns the expected result when the 'due_date' is not provided in the input
    item = {'priority': 0, 'week': 54, 'day': 1}
    r = (1, 1)
    expected_output = 1
    assert dt._calculate_cal(item, r) >= expected_output

    # Test 3: Check if the function returns the expected result when 'due_date' and 'week' are not provided in the input
    item = {'priority': 0, 'due_date': 0, 'day': 6}
    r = (0, 0)
    expected_output = 8.5
    assert dt._calculate_cal(item, r) == expected_output

    # Test 4: Check if the function returns the expected result when all input parameters are not provided
    item = {}
    r = (0, 0)
    expected_output = -1
    assert dt._calculate_cal(item, r) == expected_output
    app_clean_up(_)


def test_get_day_x():
    # Create an instance of the class that contains the _get_day_x method
    _, dt = get_app_day_tree_instance()

    # Use the current date as the due date for tasks in the test
    current_date = datetime.datetime.now().date()

    # Test 1: Check if the function correctly returns the day, wx, and tx lists for a given input
    wx = [{'index': 0, 'priority': 5, 'due_date': current_date + datetime.timedelta(days=1)},
          {'index': 1, 'priority': 3, 'week': 1, 'day': 2},
          {'index': 2, 'priority': 0, 'day': 6},
          {'index': 3, }]
    tx = [{'priority': 7, 'week': 51, 'day': 3},
          {'priority': 1, 'week': 0, 'day': 4},
          {'priority': 4, 'day': 5},
          {'priority': 2}]
    x = [0, 0, 2]
    day, wx, tx = dt._get_day_x(wx, tx, x)
    expected_day = [[{'priority': 7, 'week': 51, 'day': 3}, {'priority': 1, 'week': 0, 'day': 4}],
                    [{'index': 0, 'priority': 5, 'due_date': current_date + datetime.timedelta(days=1)
                         , 'cal': 8.5}, {'index': 2, 'priority': 0, 'day': 6, 'cal': 8.5}]]

    expected_wx = [{'index': 1, 'priority': 3, 'week': 1, 'day': 2}, {'index': 2, 'priority': 0, 'day': 6, 'cal': 8.5}]
    expected_tx = [{'priority': 7, 'week': 51, 'day': 3}, {'priority': 1, 'week': 0, 'day': 4}]

    assert day == expected_day
    assert wx == expected_wx
    assert tx == expected_tx

    # Test 2: Check if the function returns empty day, wx, and tx lists when the input wx and tx lists are empty
    wx = []
    tx = []
    x = [0, 0, 2]
    day, wx, tx = dt._get_day_x(wx, tx, x)

    assert day == [[], []]
    assert wx == []
    assert tx == []
    app_clean_up(_)


if __name__ == '__main__':
    s = Style()

    print(s.Underline + "get_app_day_tree_instance Test " + Style.BEIGEBG("started"))
    app, _ = get_app_day_tree_instance()
    app_clean_up(app)

    print(s.Underline + "test_load_save_db Test " + Style.BEIGEBG("started"))
    test_load_save_db()

    print(s.Underline + "test_save_task_to_bucket Test " + Style.BEIGEBG("started"))
    test_save_task_to_bucket()

    print(s.Underline + "test_wx_format_task Test " + Style.BEIGEBG("started"))
    test_wx_format_task()

    print(s.Underline + "test_calculate_cal Test " + Style.BEIGEBG("started"))
    test_calculate_cal()

    print(s.Underline + "test_get_day_x Test " + Style.BEIGEBG("started"))
    test_get_day_x()

    print(Style.GREEN("DayTree Test wos - successfully"))
