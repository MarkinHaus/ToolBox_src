import sys
import threading

from mods.mainTool import MainTool, FileHandler, App
from Style import Style
from importlib import import_module
from pathlib import Path
import requests
import hashlib, binascii, os

import uuid

from datetime import datetime, timedelta, timezone
import jwt


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.2.3"
        self.name = "cloudM"
        self.logs = app.logs_ if app else None
        self.color = "CYAN"
        self.keys = {
            "DM": "def-mods~~",
            "HIS": "comm-his~~",
            "URL": "comm-vcd~~",
            "TOKEN": "comm-tok~~",
        }
        self.add = []
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["ADD", "adds a mod to default load ", "add is case sensitive"],
                    ["REM", "remove a mod from default load", "add is case sensitive"],
                    ["NEW", "crate a boilerplate file to make a new mod", "add is case sensitive"],
                    ["LIST", "list all automatically loaded modules"],
                    ["download", "download a mod from MarkinHaus server", "add is case sensitive"],
                    ["#update", "update a mod from MarkinHaus server ", Style.RED("NOT IMPLEMENTED"),
                     "add is case sensitive"],
                    ["#update-core", "update ToolBox from (git) MarkinHaus server ",
                     "add is case sensitive"],
                    ["upload", "upload a mod to MarkinHaus server", "add is case sensitive"],
                    ["first-web-connection", "set up a web connection to MarkinHaus"],
                    ["create-account", "create a new account"],
                    ["login", "login with Username & password"],
                    ["create_user", "create a new user - api instance"],
                    ["validate_jwt", "validate a  user - api instance"],
                    ["log_in_user", "log_in user - api instance"],
                    ["download_api_files", "download mods"],
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
            "create-account": self.create_account,
            "login": self.log_in,
            "create_user": self.create_user,
            "log_in_user": self.log_in_user,
            "validate_jwt": self.validate_jwt,
            "download_api_files": self.download_api_files,
            "#update-core": self.update_core,
        }

        FileHandler.__init__(self, "modules.config", app.id if app else __name__)

        MainTool.__init__(self, load=self.load_open_file, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def load_open_file(self):
        self.open_l_file_handler()
        self.load_file_handler()
        self.get_version()

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["DM"], str(list(set(self.add))))
        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()

    def show_version(self, command):
        self.print(command)
        self.print("Version: ", self.version)
        return self.version

    def get_version(self):
        version_command = self.get_file_handler(self.keys["URL"])
        url = f"http://127.0.0.1:5000/get/cloudm/run/Version?command=V:{self.version}"
        if version_command is not None:
            url = version_command + "/get/cloudm/run/Version?command=V:" + f"{self.version=}"

        self.print(url)

        try:
            self.version = requests.get(url).json()["res"]
        except Exception:
            self.print(Style.RED("Error retrieving version information "
                                 "\n\tplease check your command : cloudM first-web-connection"))

        self.print("Version: %s" % self.version)

    def load_mods(self, load_mod):
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
                    load_mod(i)
                    self.log(f"Open mod {i}")
                except Exception as e:
                    self.print(Style.RED("Error") + f" loading modules : {e}")
                    self.log(f"Error mod {i}")

    def load_history(self):
        history = self.get_file_handler(self.keys["HIS"])

        if history:
            try:
                history = eval(history)
                self.print("open history len : " + str(len(history)))

                if type(history) is list and len(history) > 0:
                    return history
            except SyntaxError and TypeError:
                self.print("Data default modules is corrupted")

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

    def __init__(self, app=None):
        self.version = "0.0.2"
        self.name = "NAME"
        self.logs = app.logs_ if app else None
        self.color = "WHITE"
        # self.keys = {}
        self.tools = {
            "all": [["Version", "Shows current Version"]],
            "name": "NAME",
            "Version": self.show_version,
        }
        # FileHandler.__init__(self, "File name", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                        name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)
                    
    def show_version(self):
        self.print("Version: ", self.version)

    def on_start(self):
        # self.open_l_file_handler()
        # self.load_file_handler()
        pass

    def on_exit(self):
        # self.open_s_file_handler()
        # self.save_file_handler()
        # self.file_handler_storage.close()
        pass
"""
        if len(name) > 1:
            mod_name = name[1]
            self.print("NEW MODULE: " + mod_name, end=" ")

            fle = Path("mods/" + mod_name + ".py")
            fle.touch(exist_ok=True)
            mod_file = open(fle)

            if len(mod_file.read()) != 0:
                self.print(Style.Bold("!"))
                self.print(Style.RED("MODULE exists pleas use a other name"))
            else:
                mod_file = open(fle, "w")
                mod_file.writelines(
                    boilerplate.replace('NAME', mod_name)
                )

                mod_file.close()
                self.print("🆗")

    def upload(self, input_):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "http://127.0.0.1:8081/upload-file"
        if version_command is not None:
            url = version_command + "/upload-file"
        try:
            if len(input_) >= 2:
                name = input_[1]
                os.system("cd")
                try:
                    file = open("/mods/" + name + ".py", "rb").read()
                except IOError:
                    self.print((Style.RED(f"File does not exist or is not readable: ./mods/{name}.py")))
                    return

                if file:
                    data = {"filename": name,
                            "data": str(file, "utf-8"),
                            "content_type": "file/py"
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
                self.print((Style.YELLOW(f"SyntaxError : upload filename {input_}")))
        except Exception as e:
            self.print(Style.RED(f"Error uploading : {e}"))
            return

    def download(self, input_):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "http://127.0.0.1:8081/get/cloudm/run/download_api_files?command="
        if version_command is not None:
            url = version_command + "/get/cloudm/run/download_api_files?command=DB"
        try:
            if len(input_) >= 2:
                name = input_[1]

                url += name + ".py"

                try:
                    data = requests.get(url).json()["res"]
                    self.version = requests.get(url).json()["res"]
                    open("./mods/" + name, "a").write(str(data, "utf-8"))
                    self.print("saved file to: " + "./mods" + name)

                except Exception as e:
                    self.print(Style.RED(f"Error download (connoting to server) : {e}"))

            else:
                self.print((Style.YELLOW(f"SyntaxError : download [mod|aug|text] filename {input_}")))
        except Exception as e:
            self.print(Style.RED(f"Error download : {e}"))
            return

    def download_api_files(self, command):
        filename = command[0]
        if ".." in filename:
            return "invalid command"

        return open("./mods/" + filename, "rb").read()

    def add_url_con(self):
        """
        Adds a url to the list of urls
        """

        url = input("Pleas enter URL of CloudM Backend default [https://simpelm] : ")
        if url == "":
            url = "https://simeplm"
        self.print(Style.YELLOW(f"Adding url : {url}"))
        self.add_to_save_file_handler(self.keys["URL"], url)

    def create_account(self):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "https://simeplm/cloudM/create_acc_mhs"
        if version_command is not None:
            url = version_command + "/cloudM/create_acc_mhs"
        os.system(f"start {url}")

    def log_in(self, input_):
        version_command = self.get_file_handler(self.keys["URL"])
        url = "https://simeplm/cloudM/login"
        if version_command is not None:
            url = version_command + "/cloudM/login"

        if len(input_) == 3:
            username = input_[1]
            password = input_[2]

            data = {"username": username,
                    "password": password}

            r = requests.post(url, json=data)
            self.print(r.status_code)
            self.print(str(r.content, 'utf-8'))
            token = r.json()["token"]
            error = r.json()["error"]

            if not error:
                claims = token.split(".")[1]
                import base64
                json_claims = base64.b64decode(claims + '==')
                claims = eval(str(json_claims, 'utf-8'))
                self.print(Style.GREEN(f"Welcome : {claims['username']}"))
                self.print(Style.GREEN(f"Email : {claims['email']}"))
                self.add_to_save_file_handler(self.keys["TOKEN"], token)
                self.print("Saving token to file...")

                self.on_exit()
                self.load_open_file()

                self.print("Saved")

            else:
                self.print(Style.RED(f"ERROR: {error}"))
        else:
            self.print(Style.RED(f"ERROR: {input_} len {len(input_)} != 3"))

    def update_core(self, command, app: App):
        self.print("Init Restarting..")
        os.system("git pull")
        app.reset()
        app.remove_all_modules()
        while 1:
            try:
                com = " ".join(sys.orig_argv)
            except AttributeError:
                com = "python3 "
                com += " ".join(sys.argv)
            os.system(com)
            print("Restarting..")
            exit(0)

    def create_user(self, command, app: App):
        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        data = command[0].data

        username = data["username"]
        email = data["email"]
        password = data["password"]

        uid = str(uuid.uuid4())

        tb_token_jwt = app.MOD_LIST["DB"].tools["get"](["jwt-secret-cloudMService"], app)

        if not tb_token_jwt:
            return "jwt - not found pleas register one"

        if self.test_if_exists(username, app):
            return "username already exists"

        if self.test_if_exists(email, app):
            return "email already exists"
        jwt_key = crate_sing_key(username, email, password, uid, gen_token_time({"v": self.version}, 4380),
                                 tb_token_jwt, app)
        app.MOD_LIST["DB"].tools["set"](["", f"user::{username}::{email}::{uid}", jwt_key])
        return jwt_key

    def log_in_user(self, command, app: App):
        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        data = command[0].data
        token = command[0].token

        username = data["username"]
        password = data["password"]

        tb_token_jwt = app.MOD_LIST["DB"].tools["get"](["jwt-secret-cloudMService"], app)

        if not tb_token_jwt:
            return "jwt - not found pleas register one"

        user_data_token = app.MOD_LIST["DB"].tools["get"]([f"user::{username}::*"], app)

        user_data: dict = get_jwtdata(user_data_token, str(tb_token_jwt, "utf-8"))

        if type(user_data) is str:
            return user_data

        if "username" not in list(user_data.keys()):
            return "invalid Token"

        if "password" not in list(user_data.keys()):
            return "invalid Token"

        t_username = user_data["username"]
        t_password = user_data["password"]
        print(t_username)
        if t_username != username:
            return "username does not match"

        if not verify_password(t_password, password):
            return "invalid Password"

        self.print("user login successful : ", t_username)

        return crate_sing_key(username, user_data["email"], "", user_data["uid"],
                              gen_token_time({"v": self.version}, 4380),
                              tb_token_jwt, app)

    def validate_jwt(self, command, app: App):
        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        token = command[0].token
        tb_token_jwt = app.MOD_LIST["DB"].tools["get"](["jwt-secret-cloudMService"], app)
        return validate_jwt(token, tb_token_jwt, app.id)

    def test_if_exists(self, name: str, app: App):
        if "DB" not in list(app.MOD_LIST.keys()):
            return "Server has no database module"

        db: MainTool = app.MOD_LIST["DB"]

        get_db = db.tools["get"]

        return get_db([f"*::{name}"], app) != ""


# Create a hashed password
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


# Check hashed password validity
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def gen_token_time(massage: dict, hr_ex):
    massage['exp'] = datetime.now(tz=timezone.utc) + timedelta(hours=hr_ex)
    return massage


def crate_sing_key(username: str, email: str, password: str, uid: str, message: dict, jwt_secret: str,
                   app: App or None = None):
    # Load an RSA key from a JWK dict.
    password = hash_password(password)
    message['username'] = username
    message['password'] = password
    message['email'] = email
    message['uid'] = uid
    message['aud'] = app.id if app else "-1"

    jwt_ket = jwt.encode(message, jwt_secret, algorithm="HS512")
    return jwt_ket


def get_jwtdata(jwt_key: str, jwt_secret: str):
    try:
        token = jwt.decode(jwt_key, jwt_secret, leeway=timedelta(seconds=10),
                           algorithms=["HS512"], verify=False)
        return token
    except jwt.exceptions.InvalidSignatureError:
        return "InvalidSignatureError"


def validate_jwt(jwt_key: str, jwt_secret: str, aud) -> dict or str:
    try:
        token = jwt.decode(jwt_key, jwt_secret, leeway=timedelta(seconds=10),
                           algorithms=["HS512"], audience=aud, do_time_check=True, verify=True)
        return token
    except jwt.exceptions.InvalidSignatureError:
        return "InvalidSignatureError"
    except jwt.exceptions.ExpiredSignatureError:
        return "ExpiredSignatureError"
    except jwt.exceptions.InvalidAudienceError:
        return "InvalidAudienceError"
    except jwt.exceptions.MissingRequiredClaimError:
        return "MissingRequiredClaimError"
    except Exception as e:
        return str(e)


# CLOUDM #update-core
# API_MANAGER start-api main a
