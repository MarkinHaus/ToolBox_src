from mods.mainTool import App
from fastapi import FastAPI, Request
from typing import Union
import sys
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_item():
    result = tb_img()
    return {"result": result}


@app.get("/exit")
def read_item():
    tb_app.exit()
    return {"exit": exit(0)}


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

    tb_app = App(config_file)
    tb_img = tb_app.save_load("welcome").print_a
    tb_img()
    tb_app.save_load("api_manager").load_api_mods(tb_app.save_load, name)
    tb_app.new_ac_mod("welcome")
