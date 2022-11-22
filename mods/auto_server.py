import os

import threading
from subprocess import check_output

from mods.mainTool import MainTool, FileHandler, App


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.0.2"
        self.name = "auto_server"
        self.logs = app.logs_ if app else None
        self.color = "WHITE"
        self.keys = {
            "default": "default~~~",
        }
        self.defaults = {}
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["start-setup", "Start"],
                    ["install", "Install"],
                    ["run", "Run"],
                    ["set", "set"],
                    ["set-server", "set-server"],
                    ["build", "Build"],
                    ["upload", "upload"],
                    ["test", "test"],
                    ["hotfix", "Hotfix"]],
            "name": "auto_server",
            "Version": self.show_version,
            "install": self.install,
            "run": self.run,
            "set": self.set,
            "set-server": self.set_server,
            "build": self.build,
            "upload": self.upload,
            "test": self.test,
            "hotfix": self.hotfix,
        }
        FileHandler.__init__(self, "auto-server.data", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)
        return {"version": self.version}

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()

        default = self.get_file_handler(self.keys["default"])
        if default is not None:
            self.defaults = eval(default)

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["default"], str(self.defaults))
        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()

    def install(self, command, app: App):

        os.system("tar -xvzf ../app.tar.gz")

    def run(self, command, app: App):

        if "-bg" in command:

            if "Simpel" in command:
                def run():
                    os.system("trunk server -p=8000 ../app >Simpeloutput.log 2>&1 &")

                threading.Thread(target=run).run()

            if "MHS-server" in command:
                def run():
                    os.system(" ../markin_haus_service >MHSoutput.log 2>&1 &")

                threading.Thread(target=run).run()

            if "-py-api" in command:

                if "PY-api:src" not in list(self.defaults.keys()):
                    return {"error": "PY-api:src not found"}
                if "PY-api:name" not in list(self.defaults.keys()):
                    return {"error": "PY-api:name not found"}

                src = self.defaults["PY-api:src"]
                name = self.defaults["PY-api:name"]
                start_py_api(src, name, app)
                os.system("disown")

            if "-d" in command:
                os.system("disown")

        else:

            if "Simpel" in command:
                def run():
                    os.system("trunk server ../app")

                threading.Thread(target=run).run()

            if "MHS-server" in command:
                def run():
                    os.system("../markin_haus_service")

                threading.Thread(target=run).run()

    def hotfix(self, command, app: App):

        self.test("Simpel MHS-server", app)

        if input("Done") in ["y", "yes", "j"]:
            self.build("Simpel MHS-server -upload", app)

    def build(self, command, app: App):

        if "Simpel" in command:
            print("building Simpel")
            if "Simpel:src" not in list(self.defaults.keys()):
                return {"error": "Simpel:src not found"}
            src = self.defaults["Simpel:src"]
            build_simpel(src)

        if "MHS-server" in command:
            print("building MHS-server")
            if "MHS:src" not in list(self.defaults.keys()):
                return {"error": "MHS:src not found"}
            src = self.defaults["MHS:src"]
            build_mhs(src)

    def upload(self, command, app: App):

        if "Server:pwd" not in list(self.defaults.keys()):
            return {"error": "Server:pwd not found"}
        if "Server:user" not in list(self.defaults.keys()):
            return {"error": "Server:user not found"}
        if "Server:des_path" not in list(self.defaults.keys()):
            return {"error": "Server:des_path not found"}
        if "Server:ip" not in list(self.defaults.keys()):
            return {"error": "Server:ip not found"}

        pwd = self.defaults["Server:pwd"]
        user = self.defaults["Server:user"]
        des_path = self.defaults["Server:des_path"]
        ip = self.defaults["Server:ip"]

        if "Simpel" in command:
            if "Simpel:src" not in list(self.defaults.keys()):
                return {"error": "Simpel:src not found"}
            src = self.defaults["Simpel:src"]
            print("uploading Simpel")
            upload_simpel(src, pwd, user, ip, des_path)

        if "MHS-server" in command:
            if "MHS:src" not in list(self.defaults.keys()):
                return {"error": "MHS:src not found"}
            src = self.defaults["MHS:src"]

            print("uploading MHS-server")
            upload_mhs(src, pwd, user, ip, des_path)

    def test(self, command, _app: App):

        if "Simpel" in command:
            print("building Simpel")
            if "Simpel:src" not in list(self.defaults.keys()):
                return {"error": "Simpel:src not found"}
            src = self.defaults["Simpel:src"]
            cargo_test(src)

        if "MHS-server" in command:
            print("building MHS-server")
            if "MHS:src" not in list(self.defaults.keys()):
                return {"error": "MHS:src not found"}
            src = self.defaults["MHS:src"]
            cargo_test(src)

    def set(self, command, app: App):
        if len(command) <= 0:
            return f"invalid command len {len(command)} "

        self.defaults[command[1]] = command[2]

        # root@45.79.251.173:/home/MarkinHaus/runtime

    def set_server(self, command, _app: App):  # root@45.79.251.173:PWD#/home/MarkinHaus/runtime

        if len(command) <= 4:
            return f"invalid command len {len(command)} | root@0.0.0.0:PWD#/home"

        self.defaults["Server:user"] = command[1]
        self.defaults["Server:ip"] = command[2]
        self.defaults["Server:pwd"] = command[3]
        self.defaults["Server:des_path"] = command[4]

        # root@45.79.251.173:/home/MarkinHaus/runtime


def cd_raper(function):
    def wrapper(*args, **kwargs):
        cd = os.getcwd()
        function(*args, **kwargs)
        os.chdir(cd)

    return wrapper


@cd_raper
def start_py_api(src, name, app: App):
    app.new_ac_mod("api_manager")
    api_data = app.AC_MOD.api_config[name]

    command = f"uvicorn api:app --host {api_data['host']} --port {api_data['port']}  --header api:{name}.config:{name}"

    app.reset()
    app.new_ac_mod("auto_server")
    os.chdir(src)
    os.system('cd')

    def run():
        os.system(f"{command} >MHSoutput.log 2>&1 &")

    threading.Thread(target=run).run()


@cd_raper
def cargo_test(src):
    os.chdir(src)
    os.system("cd")
    os.system("cargo test")


@cd_raper
def build_simpel(src):
    os.chdir(src)
    os.system("cd")
    os.system("cargo build --target=wasm32-unknown-unknown --release")
    os.system("mv ./traget/wasem32-unknown-unknown/relaese/simpel.wasm  ./app/simpel.wasm")


@cd_raper
def build_mhs(src):
    os.chdir(src)
    os.system("cd")
    os.system("cargo build --target=x86_64-unknown-linux-gnu --release")
    os.system("mv ./traget/wasem32-unknown-unknown/relaese/simpel.wasm  ./app/simpel.wasm")


@cd_raper
def upload_mhs(src, pwd, user, ip, des_path):
    os.chdir(src)
    os.system(f'sshpass -p "{pwd}" scp -r {user}@{ip}:{des_path} markin_haus_service')


@cd_raper
def upload_simpel(src, pwd, user, ip, des_path):
    os.chdir(src)
    os.system(f'sshpass -p "{pwd}" scp -r {user}@{ip}:{des_path} ./app')
