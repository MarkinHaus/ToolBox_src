import datetime

from Style import Style
from _test._mainTool_test import get_app, app_clean_up


def get_app_cm_instance():
    app = get_app()
    app.load_mod("DB")

    assert "DB" in app.MOD_LIST

    app.load_mod("cloudM")
    assert "CLOUDM" in app.MOD_LIST

    app.new_ac_mod("cloudM")

    assert "cloudM" in app.AC_MOD.name

    return app, app.AC_MOD


# user test

class TestCommand:
    data = {}
    token = ""


def test_create_user():
    app, cm = get_app_cm_instance()
    # Testdaten erstellen
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    t = TestCommand()
    t.data = data

    # create_user Funktion aufrufen und das Ergebnis in einer Variablen speichern
    result = cm.create_user([t], app)

    # Überprüfen, ob die Funktion ein gültiges Ergebnis zurückgibt
    assert result is not None
    assert isinstance(result, str)
    app_clean_up(app)
    return data, result


def delete_test_user(app, data, uid):
    app.MOD_LIST["DB"].tools["del"](['', f"::{uid}", '*'])
    assert app.MOD_LIST["DB"].tools["get"]([f"::{uid}"], app) == ""
    app.MOD_LIST["DB"].tools["del"](['', f"user::{data['username']}::{data['email']}::{uid}", '*'])
    assert app.MOD_LIST["DB"].tools["get"]([f"user::{data['username']}::{data['email']}::{uid}"], app) == ""


def test_create_log_in_user():
    app, dt = get_app_cm_instance()
    # Testdaten erstellen
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    t = TestCommand()
    t.data = data

    # create_user Funktion aufrufen und das Ergebnis in einer Variablen speichern
    result = dt.create_user([t], app)

    # Überprüfen, ob die Funktion ein gültiges Ergebnis zurückgibt
    assert result is not None
    assert isinstance(result, str)

    # Einen Benutzer erstellen (dieser Schritt ist notwendig, damit die log_in_user Funktion etwas zum Anmelden hat)
    dt.create_user([t], app)

    # log_in_user Funktion aufrufen und das Ergebnis in einer Variablen speichern
    result = dt.log_in_user([t], app)

    # Überprüfen, ob die Funktion ein gültiges Ergebnis zurückgibt
    assert result is not None
    assert isinstance(result, str)

    app.MOD_LIST["DB"].tools["del"](['', f"user::{data['username']}::{data['email']}::", '*'])
    assert app.MOD_LIST["DB"].tools["get"]([f"user::{data['username']}::{data['email']}::"], app) == ""
    app_clean_up(app)


if __name__ == "__main__":
    s = Style()
    print(s.Underline + "get_app_cm_instance Test " + Style.BEIGEBG("started"))
    app, cm = get_app_cm_instance()
    print(s.Underline + "test_create_user Test " + Style.BEIGEBG("started"))
    data, result = test_create_user()

    t = TestCommand()
    t.token = result
    print(s.Underline + "validate_jwt Test " + Style.BEIGEBG("started"))
    uid = cm.validate_jwt([t], app)

    print(s.Underline + "delete_test_user Test " + Style.BEIGEBG("started"))
    delete_test_user(app, data, uid)
    app_clean_up(app)
    print(s.Underline + "test_create_log_in_user Test " + Style.BEIGEBG("started"))
    test_create_log_in_user()
    print(Style.GREEN("CloudM Test wos - successfully"))
