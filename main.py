# Import default Pages
import sys
import os
from platform import system, node
from importlib import import_module
from inspect import signature
# Import local Pages

from mods.mainTool import MainTool
from Style import Style

# Import public Pages
import readchar


def load_welcome_page(mod_name="welcome"):
    mod = import_module("mods." + mod_name)
    return getattr(mod, "Tools")


def ac_mod(mod):
    return mod(logs=logs)


def lode_mod(mod: MainTool):
    mod = ac_mod(mod)
    mod_name = mod.name
    MOD_LIST[mod_name.upper()] = mod
    color = mod.color if mod.color else "WHITE"
    MACRO.append(mod_name.upper())
    MACRO_color[mod_name.upper()] = color
    HELPER[mod_name.upper()] = mod.tools["all"]

    # for spec, _ in mod.tools["all"]:
    #     MACRO.append(mod_name.upper() + "-" + spec.upper())

    return mod


def remove_all_modules():
    iter_list = MOD_LIST.copy()

    exit_all_modules()

    for mod_name in iter_list.keys():
        try:
            remove_mod(mod_name)
        except Exception as e:
            print(Style.RED("ERROR: %s %e" % mod_name % e))


def remove_mod(mod_name):
    del MOD_LIST[mod_name.upper()]
    del MACRO_color[mod_name.upper()]
    del HELPER[mod_name.upper()]
    MACRO.remove(mod_name.upper())


def cls():
    if system() == "Windows":
        os.system("cls")
    if system() == "Linux":
        os.system("clear")


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


def user_hud_cmd():
    INFO()


def colorize(obj):
    for pos, o in enumerate(obj):
        if o.upper() in MACRO:
            if o.upper() in MACRO_color.keys():
                obj[pos] = f"{Style.style_dic[MACRO_color[o.upper()]]}{o}{Style.style_dic['END']}"
    return obj


def pretty_print(obj: list):
    obj_work = obj.copy()
    obj_work = colorize(obj_work)
    s = ""
    for i in obj_work:
        s += str(i) + " "
    return s


def autocompletion(command):
    options = []
    if command == "":
        return options
    for macro in MACRO + SUPER_SET:
        if macro.startswith(command.upper()):
            options.append(macro)

    return options


def user_input(c_h):
    get_input = True
    command = ""
    print_command = []
    helper = ""
    helper_index = 0
    options = []
    history_step = 0
    # print('\033[?25l', end="")

    while get_input:

        key = readchar.readkey()

        if key == b'\x05' or key == '\x05':
            print('\033[?25h', end="")
            get_input = False
            command = "EXIT"

        elif key == readchar.key.LEFT:
            if helper_index > 0:
                helper_index -= 1

        elif key == readchar.key.RIGHT:
            if helper_index < len(options) - 1:
                helper_index += 1

        elif key == readchar.key.UP:
            command = ""
            print_command = []
            if history_step < len(c_h) - 1:
                print_command = c_h[history_step]
                history_step -= 1

        elif key == readchar.key.DOWN:
            command = ""
            print_command = []
            if history_step > 0:
                print_command = c_h[history_step]
                history_step += 1

        elif key == b'\x08' or key == '\x7f':
            if len(command) == 0 and len(print_command) != 0:
                command = print_command[-1]
                command = command[:-1]
                print_command = print_command[:-1]
            else:
                command = command[:-1]
        elif key == b' ' or key == ' ':
            print_command.append(command)
            command = ""
        elif key == b'\r' or key == '\r':
            get_input = False
            print_command.append(command)
        elif key == b'\t' or key == '\t':
            command += helper
        else:
            if type(key) == str:
                command += key
            else:
                command += str(key, "ISO-8859-1")

        options = autocompletion(command)

        if helper_index > len(options) - 1:
            helper_index = 0

        helper = ""
        do = len(options) > 0
        if do:
            helper = options[helper_index][len(command):].lower()

        to_print = PREFIX + pretty_print(print_command + [command + Style.Underline(Style.Bold(helper))])
        if do:
            to_print += " | " + Style.Bold(options[helper_index]) + " " + str(options)
        sys.stdout.write("\033[K")
        print(to_print, end="\r")

    sys.stdout.write("\033[K")
    print(PREFIX + pretty_print(print_command) + "\n")
    # print("\033[?25h", end="")

    return print_command


def open_function(u, ac_mod_):
    print(f"loading function :", end=" ")
    try:
        function = ac_mod_.tools[ac_mod_.tools["all"][SUPER_SET.index(u[0].upper())][0]]
        print(Style.GREEN("🆗"))
        print("test function signature", end=" ")

        sig = signature(function)
        params_len = len(sig.parameters)
        if params_len == 0:
            try:
                print(Style.GREEN("🆗 ") + "\nStart function\n")
                function()
                print(Style.GREEN(f"\nOK fin {u[0]}"))
            except Exception as e:
                print(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
        elif params_len == 1:
            try:
                print(Style.GREEN("🆗 ") + "\nStart function\n")
                function(u)
                print(Style.GREEN(f"\nOK fin {u[0]}"))
            except Exception as e:
                print(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
        else:
            print(Style.YELLOW(f"! to many args {params_len} def ...(u): | -> {str(sig)}"))

    except IndexError and KeyError:
        print(Style.RED("! function could not be found | may not be implemented yet. "),
              end='\r')
    except Exception as e:
        print(Style.RED(
            Style.Bold(f"fatal loading error {e} \n{' ' * 18} pleas be sure to run commands assigned to {u[0]}")),
            end='\r')


def exit_all_modules():
    for mod in MOD_LIST.items():
        print("closing:", mod[0], ": ", end="")
        if mod[1]._on_exit:
            try:
                mod[1]._on_exit()
                print(Style.GREEN(Style.Bold(f"🆗")))
            except Exception as e:
                print(Style.YELLOW(Style.Bold(f"closing ERROR : {e}")))


def default_load():
    global INFO, CLOUDM
    INFO = lode_mod(load_welcome_page()).print_t
    CLOUDM = lode_mod(load_welcome_page("cloudM"))
    CLOUDM.lode_mods(load_welcome_page, lode_mod)


def main(args):
    global AC_MOD, PREFIX, SUPER_SET, COMMAND_HISTORY
    run = True

    while run:
        print("\n" * 2)
        user_hud_cmd()
        print("\n" * 1)
        u = user_input(COMMAND_HISTORY)

        # print("U:", u, len(u))

        if len(u) == 0:
            print("hey how did you do it this area is private :>")

        elif u[0] == '':
            print("Pleas enter a command or help for mor information")

        elif u[0].lower() == '_hr':
            if input("Do you to hot-reloade alle mods? (y/n): ") in ["y", "yes", "Y"]:
                remove_all_modules()
                default_load()

        elif u[0].lower() == 'logs':
            print(f"PREFIX={PREFIX}"
                  f"\nMACRO={pretty_print(MACRO[:5])}"
                  f"\nMODS={pretty_print(MACRO[5:])}"
                  f"\nSUPER_SET={pretty_print(SUPER_SET)}")
            command_viewer(logs)
            print("HISTORY")
            command_viewer(COMMAND_HISTORY[len(COMMAND_HISTORY) - 4:])

        elif u[0].upper() == "EXIT":
            if input("Do you want to exit? (y/n): ") in ["y", "yes", "Y"]:
                # command_viewer(COMMAND_HISTORY)
                CLOUDM.save_history(COMMAND_HISTORY)
                exit_all_modules()
                print(Style.Bold(Style.CYAN("OK - EXIT ")))
                print('\033[?25h', end="")
                run = False
                return

        elif u[0].lower() == "help":
            if not AC_MOD and len(u) == 1:
                print(f"All commands: {pretty_print(MACRO)} \nfor mor information type : help [command]")
            elif AC_MOD:
                print(Style.Bold(AC_MOD.name))
                command_viewer(AC_MOD.tools["all"])
            elif len(u) == 2:
                if u[1].upper() in HELPER.keys():
                    helper = HELPER[u[1].upper()]
                    print(Style.Bold(u[1].upper()))
                    command_viewer(helper)
                else:
                    print(Style.RED(f"HELPER {u[1]} is not a valid | valid commands ar"
                                    f" {pretty_print(list(HELPER.keys()))}"))
            else:
                print(Style.RED(f"HELPER {pretty_print(u)} invalid syntax / command"))

        elif u[0].upper() == 'LOAD-MOD':
            if len(u) > 1:
                try:
                    mod = load_welcome_page(u[1])
                    lode_mod(mod)
                except ModuleNotFoundError:
                    print(Style.RED(f"Module {u[1]} not found"))
            else:
                if system() == "Windows":
                    os.system("dir .\mods")
                if system() == "Linux":
                    os.system("ls ./mods")

        elif u[0] == '..':
            AC_MOD = None
            PREFIX = Style.CYAN(f"~{node()}@>")
            SUPER_SET = []

        elif u[0].upper() in MOD_LIST.keys():
            COMMAND_HISTORY.append(u)
            AC_MOD = MOD_LIST[u[0].upper()]
            PREFIX = Style.CYAN(f"~{node()}:{Style.Bold(u[0].upper())}{Style.CYAN('@>')}")
            for spec in AC_MOD.tools["all"]:
                SUPER_SET.append(spec[0].upper())

            if len(u) > 1:
                if u[1].upper() in SUPER_SET:
                    open_function(u[1:], AC_MOD)

        elif AC_MOD:
            if u[0].upper() in SUPER_SET:
                COMMAND_HISTORY.append(u)
                open_function(u, AC_MOD)
            else:
                print(Style.RED("function could not be found"))

        else:
            print(Style.YELLOW("[-] Unknown command:") + pretty_print(u))


if __name__ == '__main__':
    # C:\Users\Markin\anaconda3\envs\ToolBoxV2\python.exe main.py
    os.system("")
    MACRO = ['HELP', 'LOAD-MOD', 'LOGS', 'EXIT', '..']
    MACRO_color = {'HELP': 'GREEN',
                   'LOAD-MOD': 'BLUE',
                   'EXIT': 'RED',
                   '..': 'MAGENTA',
                   'LOGS': 'MAGENTA'
                   }
    MOD_LIST = {}
    HELPER = {
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
    }
    PREFIX = Style.CYAN(f"~{node()}@>")
    logs = []
    SUPER_SET = []
    AC_MOD = None
    print("SYSTEM :; " + node())

    # default_load()

    INFO = lode_mod(load_welcome_page()).print_t
    CLOUDM = lode_mod(load_welcome_page("cloudM"))
    CLOUDM.lode_mods(load_welcome_page, lode_mod)
#
    COMMAND_HISTORY = CLOUDM.load_history()

    print('\033[?25l', end="")

    main(sys.argv)


# TODO Load modular Mods
#   TODO Helper mods _supported DON
#   TODO Interface mods _supported DON

#   TODO Socket mods _supported
#   TODO API mods _supported

# TODO Web interface
