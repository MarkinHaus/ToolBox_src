import os
from platform import node
from importlib import import_module
from inspect import signature

from Style import Style


class MainTool:
    def __init__(self, *args, **kwargs):
        self.version = kwargs["v"]
        self.tools = kwargs["tool"]
        self.name = kwargs["name"]
        self.logs = kwargs["logs"]
        self.color = kwargs["color"]
        self.todo = kwargs["load"]
        self._on_exit = kwargs["on_exit"]
        self.stuf = False
        self.load()

    def load(self):
        if self.todo:
            self.todo()
            self.logs.append([self, "load successfully"])
        else:
            self.logs.append([self, "no load require"])
        print(f"TOOL successfully loaded : {self.name}")
        self.logs.append([self, "TOOL successfully loaded"])

    def print(self, message, *args, end="\n"):
        if self.stuf:
            return
        print(Style.style_dic[self.color] + self.name + Style.style_dic["END"] + ":", message, *args, end=end)

    def log(self, message):
        self.logs.append([self, message])


class Code:
    @staticmethod
    def decode_code(data):
        # letters = string.ascii_letters + string.digits + string.punctuation
        # decode_str = ''
        # data_n = data.split('#')
        # data = []
        # for data_z in data_n[:-1]:
        #    data.append(float(data_z))
        # i = 0
        # for data_z in data:
        #    ascii_ = data_z * 2
        #    decode_str += letters[int(ascii_)]
        #    i += 1
        # decode_str = decode_str.replace('-ou-', 'u')
        # decode_str = decode_str.split('@')
        # return decode_str
        return data

    @staticmethod
    def encode_code(data):
        # letters = string.ascii_letters + string.digits + string.punctuation
        # encode_str = ''
        # data = data.replace(' ', '@')
        # leng = data.__len__()
        # for data_st in range(leng):
        #    i = -1
        #    while data[data_st] != letters[i]:
        #        i += 1
        #        if data[data_st] == letters[i]:
        #            encode_str += str(i / 2) + '#'
        #    data_st += 1
        # return encode_str
        return data


class FileHandler(Code):
    def __init__(self, filename):
        self.file_handler_save = []
        self.file_handler_load = []
        self.file_handler_auto_save = {}
        self.file_handler_filename = filename
        self.file_handler_storage = None
        self.file_handler_index_ = -1
        self.file_handler_file_prefix = f".{filename.split('.')[1]}/"

    def open_file_handler(self, mode: str, rdu):
        if self.file_handler_storage:
            self.file_handler_storage.close()
        try:
            self.file_handler_storage = open(self.file_handler_file_prefix + self.file_handler_filename, mode)
        except FileNotFoundError:
            print(Style.RED(f"File not found: {self.file_handler_file_prefix}{self.file_handler_filename}"))
            if input("Do you want to create this path | file ? (y/n) ") in ['y', 'yes', 'Y']:
                if not os.path.exists(f"{self.file_handler_file_prefix}"):
                    os.makedirs(f"{self.file_handler_file_prefix}")
                open(self.file_handler_file_prefix + self.file_handler_filename, 'a').close()
                print("File created successfully")
                rdu()
            else:
                print(Style.YELLOW(f"pleas create this file to prosed : {self.file_handler_file_prefix}"
                                   f"{self.file_handler_filename}"))
                exit(0)

    def open_s_file_handler(self):
        self.open_file_handler('w+', self.open_s_file_handler)
        return self

    def open_l_file_handler(self):
        self.open_file_handler('r+', self.open_l_file_handler)
        return self

    def save_file_handler(self):
        for pos, data in enumerate(self.file_handler_auto_save.keys()):
            if self.file_handler_auto_save[data]:
                self.add_to_save_file_handler(data, self.file_handler_load[pos][1])
        if not self.file_handler_storage:
            print("WARNING pleas open storage")
        for line in self.file_handler_save:
            self.file_handler_storage.write(line)
            self.file_handler_storage.write('\n')

        return self

    def add_to_save_file_handler(self, key: str, value: str):
        if len(key) != 10:
            print('WARNING: key length is not 10 characters')
            return
        try:
            self.set_auto_save_file_handler(key)
            self.file_handler_save.append(key + self.encode_code(value))
        except ValueError:
            print(Style.RED(f"{value=}\n\n{key=} was not saved.\n{type(value)=}!=str"))

    def load_file_handler(self):
        if not self.file_handler_storage:
            print("WARNING pleas open storage")
        for line in self.file_handler_storage:
            line = line[:-1]
            heda = line[:10]
            enc = self.decode_code(line[10:])
            append = [heda, enc]
            self.file_handler_auto_save[heda] = True
            self.file_handler_load.append(append)
        return self

    def set_auto_save_file_handler(self, key: str):
        self.file_handler_auto_save[key] = False

    def get_file_handler(self, obj: str) -> str or None:
        self.file_handler_index_ = -1
        for objects in self.file_handler_load:
            self.file_handler_index_ += 1
            # print(objects)
            if obj == objects[0]:
                return objects[1]
        return None


class App:
    def __init__(self, prefix: str = ""):

        config_filename = prefix + node() + ".config"

        self.config_fh = FileHandler(config_filename)
        self.config_fh.open_l_file_handler()
        self.config_fh.load_file_handler()

        self.keys = {
            "MACRO": "macro~~~~:",
            "MACRO_C": "m_color~~:",
            "HELPER": "helper~~~:",
            "debug": "debug~~~~:",
            "id": "name-spa~:",
            "st-load": "mute~load:",
        }

        self.MACRO = self.get_config_data("MACRO", ['HELP', 'LOAD-MOD', 'LOGS', 'EXIT', '_hr', '..', 'cls', 'monit'])
        self.MACRO_color = self.get_config_data("MACRO_C", {'HELP': 'GREEN', 'LOAD-MOD': 'BLUE', 'EXIT': 'RED',
                                                            'monit': 'YELLOW', '..': 'MAGENTA', 'LOGS': 'MAGENTA',
                                                            'cls': 'WHITE'
                                                            })
        self.HELPER = self.get_config_data("HELPER", {
            'HELP': [['Information', 'version : 0.1.0', 'color : GREEN', 'syntax : help [command]',
                      'help is available in all subsets']],
            'LOAD-MOD': [['Information', 'version : 0.1.0', 'color : BLUE', 'syntax : LOAD-MOD [filename]',
                          'file must be in mods folder ']],
            'EXIT': [['Information', 'version : 0.1.0', 'color : RED', 'syntax : EXIT',
                      'The only way to exit in TOOL BOX']],
            '..': [['Information', 'version : 0.1.0', 'color : MAGENTA', 'syntax : ..',
                    'Brings u Back to Main']],
            'LOGS': [['Information', 'version : 0.1.0', 'color : MAGENTA', 'syntax : LOGS',
                      'show logs']],
            '_hr': [['Information', 'version : ----', 'Hotreload all mods']],
            'cls': [['Information', 'version : ----', 'Clear Screen']],
            'monit': [['Information', 'version : ----', 'go in monit mode']],
            'mode:debug': [['Test Function', 'version : ----', Style.RED('Code can crash')]]
        })

        self.id = self.get_config_data("id", config_filename)
        self.stuf_load = self.get_config_data("st-load", False)
        self.auto_save = True
        self.PREFIX = Style.CYAN(f"~{node()}@>")
        self.MOD_LIST = {}
        self.logs_ = []
        self.SUPER_SET = []
        # self.spec = []
        self.AC_MOD = None
        self.alive = True
        self.debug = True  # self.get_config_data("debug", False)

        print("SYSTEM :; " + node())

    def get_config_data(self, key, t):
        data = self.config_fh.get_file_handler(self.keys[key])
        if data is not None:
            try:
                return eval(data)
            except ValueError:
                print(f"Error Loading {key}")
        return t

    # def pre_lib_mod(self, filename):
    #    lib_mod_dir = ""
    #
    #    mod_file = open(f"mods/{filename}.py", "rb").read()
    #
    #    if not os.path.exists(f"./runtime/{self.id}/mod_lib"):
    #        os.makedirs(f"./runtime/{self.id}/mod_lib")
    #    open(self.file_handler_file_prefix + self.file_handler_filename, 'a').close()
    #
    #    open()
    #
    #    return lib_mod_dir

    def load_mod(self, filename):
        mod = import_module("mods." + filename)
        mod = getattr(mod, "Tools")

        mod = mod(logs=self.logs_)
        mod_name = mod.name
        self.MOD_LIST[mod_name.upper()] = mod
        color = mod.color if mod.color else "WHITE"
        self.MACRO.append(mod_name.upper())
        self.MACRO_color[mod_name.upper()] = color
        self.HELPER[mod_name.upper()] = mod.tools["all"]
        # for spec, _ in mod.tools["all"]:
        #     self.spec.append(mod_name.upper() + "-" + spec.upper())

        return mod

    def remove_all_modules(self):
        iter_list = self.MOD_LIST.copy()

        self.exit_all_modules()

        for mod_name in iter_list.keys():
            try:
                self.remove_mod(mod_name)
            except Exception as e:
                print(Style.RED("ERROR: %s %e" % mod_name % e))

    def exit_all_modules(self):
        for mod in self.MOD_LIST.items():
            print("closing:", mod[0], ": ", end="")
            if mod[1]._on_exit:
                try:
                    mod[1]._on_exit()
                    print(Style.GREEN(Style.Bold(f"🆗")))
                except Exception as e:
                    print(Style.YELLOW(Style.Bold(f"closing ERROR : {e}")))

    def remove_mod(self, mod_name):
        del self.MOD_LIST[mod_name.upper()]
        del self.MACRO_color[mod_name.upper()]
        del self.HELPER[mod_name.upper()]
        self.MACRO.remove(mod_name.upper())

    def colorize(self, obj):
        for pos, o in enumerate(obj):
            if o.upper() in self.MACRO:
                if o.upper() in self.MACRO_color.keys():
                    obj[pos] = f"{Style.style_dic[self.MACRO_color[o.upper()]]}{o}{Style.style_dic['END']}"
        return obj

    def pretty_print(self, obj: list):
        obj_work = obj.copy()
        obj_work = self.colorize(obj_work)
        s = ""
        for i in obj_work:
            s += str(i) + " "
        return s

    def autocompletion(self, command):
        options = []
        if command == "":
            return options
        for macro in self.MACRO + self.SUPER_SET:
            if macro.startswith(command.upper()):
                options.append(macro)

        return options

    def logs(self):
        print(f"PREFIX={self.PREFIX}"
              f"\nMACRO={self.pretty_print(self.MACRO[:7])}"
              f"\nMODS={self.pretty_print(self.MACRO[7:])}"
              f"\nSUPER_SET={self.pretty_print(self.SUPER_SET)}")
        self.command_viewer(self.logs_)

    def exit(self):
        self.exit_all_modules()
        print(Style.Bold(Style.CYAN("OK - EXIT ")))
        print('\033[?25h', end="")
        self.alive = False
        self.config_fh.open_s_file_handler()
        self.config_fh.save_file_handler()
        self.config_fh.file_handler_storage.close()

    def help(self, command: str):
        if not self.AC_MOD and command == "":
            print(f"All commands: {self.pretty_print(self.MACRO)} \nfor mor information type : help [command]")
            return "intern-error"
        elif self.AC_MOD:
            print(Style.Bold(self.AC_MOD.name))
            self.command_viewer(self.AC_MOD.tools["all"])
            return self.AC_MOD.tools["all"]

        elif command.upper() in self.HELPER.keys():
            helper = self.HELPER[command.upper()]
            print(Style.Bold(command.upper()))
            self.command_viewer(helper)
            return helper
        else:
            print(Style.RED(f"HELPER {command} is not a valid | valid commands ar"
                            f" {self.pretty_print(list(self.HELPER.keys()))}"))
            return "invalid commands"

    def save_load(self, filename):
        if self.debug:
            return self.load_mod(filename)
        try:
            return self.load_mod(filename)
        except ModuleNotFoundError:
            print(Style.RED(f"Module {filename} not found"))

    def reset(self):
        self.AC_MOD = None
        self.PREFIX = Style.CYAN(f"~{node()}@>")
        self.SUPER_SET = []

    def _get_function(self, name):
        if not self.AC_MOD:
            self.debug_print(Style.RED("No module Active"))
            return None
        if self.debug:
            return self.AC_MOD.tools[self.AC_MOD.tools["all"][self.SUPER_SET.index(name.upper())][0]]
        try:
            return self.AC_MOD.tools[self.AC_MOD.tools["all"][self.SUPER_SET.index(name.upper())][0]]
        except KeyError as e:
            print(Style.RED(f"KeyError: {e} function not found 404"))
            return None

    def run_function(self, name, command):
        # get function
        function = self._get_function(name)
        res = {}
        if not function:
            print(Style.RED(f"Function {name} not found"))
            return False
        # signature function
        sig = signature(function)
        args = len(sig.parameters)

        if args == 0:
            if self.debug:
                res = function()
            else:
                try:
                    print(Style.GREEN("🆗 ") + "\nStart function\n")
                    res = function()
                    print(Style.GREEN(f"\n-"))
                except Exception as e:
                    print(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))

        elif args == 1:
            if self.debug:
                res = function(command)
            else:
                try:
                    print(Style.GREEN("🆗 ") + "\nStart function\n")
                    res = function(command)
                    print(Style.GREEN(f"\n-"))
                except Exception as e:
                    print(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))

        elif args == 2:
            if self.debug:
                res = function(command, self)
            else:
                try:
                    print(Style.GREEN("🆗 ") + "\nStart function\n")
                    res = function(command, self)
                    print(Style.GREEN(f"\n-"))
                except Exception as e:
                    print(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
        else:
            self.debug_print(Style.YELLOW(f"! to many args {args} def ...(u): | -> {str(sig)}"))

        if self.debug:
            print(res)

        print(f"Name: {self.id} : {__name__}")

        return res

    def set_spec(self):
        self.SUPER_SET = []
        for spec in self.AC_MOD.tools["all"]:
            self.SUPER_SET.append(spec[0].upper())

    def new_ac_mod(self, name):
        self.AC_MOD = self.MOD_LIST[name.upper()]
        self.AC_MOD.stuf = self.stuf_load
        self.PREFIX = Style.CYAN(
            f"~{node()}:{Style.Bold(self.pretty_print([name.upper()]).strip())}{Style.CYAN('@>')}")
        self.set_spec()

    def save_exit(self):

        self.config_fh.add_to_save_file_handler(self.keys["HELPER"], str(self.HELPER))
        self.config_fh.add_to_save_file_handler(self.keys["MACRO"], str(self.MACRO))
        self.config_fh.add_to_save_file_handler(self.keys["MACRO_C"], str(self.MACRO_color))
        self.config_fh.add_to_save_file_handler(self.keys["debug"], str(self.debug))
        self.config_fh.add_to_save_file_handler(self.keys["st-load"], str(self.stuf_load))

    def debug_print(self, message, *args, end="\n"):
        if self.debug:
            print(message, *args, end=end)

    @staticmethod
    def command_viewer(mod_command):
        mod_command_names = []
        mod_command_dis = []
        print(f"\n")
        for msg in mod_command:
            if msg[0] not in mod_command_names:
                mod_command_names.append(msg[0])
                mod_command_dis.append([])

            for dis in msg[1:]:
                mod_command_dis[mod_command_names.index(msg[0])].append(dis)

        for tool_address in mod_command_names:
            print(Style.GREEN(f"{tool_address}, "))
            for log_info in mod_command_dis[mod_command_names.index(tool_address)]:
                print(Style.YELLOW(f"    {log_info}"))
            print("\n")

        return mod_command_names
