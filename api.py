from mods.mainTool import App
from fastapi import FastAPI
from typing import Union
import sys

app = FastAPI()


@app.get("/")
def read_item():
    result = tb_img()
    return {"result": result}


@app.get("/mod-list")
def read_item():
    return {"mod-list": list(tb_app.MOD_LIST.keys())}


@app.get("/SUPER_SET")
def read_item():
    return {"logs": tb_app.SUPER_SET}


@app.get("/prefix")
def read_item():
    return {"logs": tb_app.PREFIX}


@app.get("/logs")
def read_item():
    logs = {}
    for log in tb_app.logs_:
        logs[log[0].name] = []
        logs[log[0].name].append(log[1:])
    print(logs)
    return {"logs": logs}


@app.get("/{name}")
def read_item(name: str):
    res = "mod-404"
    if name.upper() in tb_app.MOD_LIST:
        tb_app.new_ac_mod(name.upper())
        res = f"{name}-mod-online"
    return {"result": res}


@app.get("/mod/index/{name}")
def read_item(name: str):
    try:
        tb_app.new_ac_mod(name)
        result = tb_app.help('')
    except:
        result = "None"
    return {"name": name, "result": result}


@app.get("/{mod}/run/{name}")
def read_item(mod: str, name: str, command: Union[str, None] = None):
    res = {}
    if not command:
        command = ''
    if tb_app.AC_MOD.name != mod.upper():
        if mod.upper() in tb_app.MOD_LIST:
            tb_app.new_ac_mod(mod)

    if tb_app.AC_MOD:
        res = tb_app.run_function(name, command.split('|'))

    return {"mod": mod, "name": name, "command": command, "result": res}


if __name__ == 'api':

    config_file = "api.config"
    name = ""

    for i in sys.argv[2:]:
        if i.startswith('api'):
            d = i.split(':')
            config_file = d[1]
            name = d[2]

    config_file = "api.config"
    tb_app = App(config_file)
    tb_img = tb_app.save_load("welcome").print_a
    tb_img()
    tb_app.save_load("api_manager").load_api_mods(tb_app.save_load, name)
    tb_app.new_ac_mod("welcome")
