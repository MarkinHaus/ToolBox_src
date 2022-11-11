# Import default Pages
import sys
import os
from platform import system
from Style import Style

# Import public Pages
import readchar
from mods.mainTool import App


def user_input(app):
    get_input = True
    command = ""
    print_command = []
    helper = ""
    helper_index = 0
    options = []

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
            pass

        elif key == readchar.key.DOWN:
            pass

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
        elif key == readchar.key.ENTER:
            get_input = False
            print_command.append(command)
        elif key == b'\t' or key == '\t':
            command += helper
        else:
            if type(key) == str:
                command += key
            else:
                command += str(key, "ISO-8859-1")

        options = list(set(app.autocompletion(command)))

        if helper_index > len(options) - 1:
            helper_index = 0

        helper = ""
        do = len(options) > 0
        if do:
            helper = options[helper_index][len(command):].lower()

        to_print = app.PREFIX + app.pretty_print(print_command + [command + Style.Underline(Style.Bold(helper))])
        if do:
            to_print += " | " + Style.Bold(options[helper_index]) + " " + str(options)
        sys.stdout.write("\033[K")
        print(to_print, end="\r")

    sys.stdout.write("\033[K")
    print(app.PREFIX + app.pretty_print(print_command) + "\n")

    return print_command


def main(app, img):
    mode = "live"
    r = 0
    while app.alive:
        r += 1
        if r % 10 == 0:
            img()
        command = user_input(app)

        if command[0] == '':  # log(helper)
            print("Pleas enter a command or help for mor information")

        elif command[0].lower() == '_hr':
            if input(f"Do you to hot-reloade {'alle mods' if len(command) <= 1 else command[1]}? (y/n): ") in ["y",
                                                                                                               "yes",
                                                                                                               "Y"]:
                if len(command) == 2:
                    if command[1] in app.MOD_LIST.keys():
                        app.reset()
                        try:
                            app.remove_mod(command[1])
                        except Exception as e:
                            print(Style.RED(f"Error removing module {command[1]}\nERROR:\n{e}"))

                        try:
                            app.save_load(command[1])
                        except Exception as e:
                            print(Style.RED(f"Error adding module {command[1]}\nERROR:\n{e}"))

                    else:
                        print(f"Module not found {command[1]} |  is case sensitive")
                else:
                    app.reset()
                    app.remove_all_modules()
                    app.save_load("cloudM").load_mods(tb_app.save_load)

        elif command[0].lower() == 'logs':
            app.logs()

        elif command[0].upper() == "EXIT":  # builtin events(exit)
            if input("Do you want to exit? (y/n): ") in ["y", "yes", "Y"]:
                # app.save_exit()
                app.exit()

        elif command[0].lower() == "help":  # logs(event(helper))
            app.MACRO += ['mode:live', 'mode:debug', 'monit', 'mode:stuf']
            n = command[1] if len(command) > 2 else ''
            app.help(n)

        elif command[0].upper() == 'LOAD-MOD':  # builtin events(event(cloudM(_)->event(Build)))
            if len(command) == 2:
                app.save_load(command[1])
                app.new_ac_mod(command[1])
            else:
                if system() == "Windows":
                    os.system("dir .\mods")
                if system() == "Linux":
                    os.system("ls ./mods")

        elif command[0] == '..':
            app.reset()

        elif command[0] == 'cls':
            if system() == "Windows":
                os.system("cls")
            if system() == "Linux":
                os.system("clear")

        elif command[0] == 'mode':
            app.SUPER_SET += ['mode:live', 'mode:debug', 'monit', 'mode:stuf']
            print(f'{mode}')

        elif command[0] == 'mode:live':
            mode = 'live'
            app.debug = False

        elif command[0] == 'mode:auto-save':
            app.auto_save = not app.auto_save
            print('auto-save', app.auto_save)

        elif command[0] == 'mode:debug':
            mode = 'debug'
            app.debug = True

        elif command[0] == 'monit':
            print(f"{mode=} \n{app.debug=}\n{app.id=}\n{app.auto_save=}\n{app.stuf_load=}")

        elif command[0] == 'mode:stuf':
            app.stuf_load = not app.stuf_load

        elif command[0].upper() in app.MOD_LIST.keys():
            app.new_ac_mod(command[0])

            if len(command) > 1:
                if command[1].upper() in app.SUPER_SET:
                    app.run_function(command[1], command[1:])

        elif app.AC_MOD:  # builtin events(AC_MOD(MOD))
            if command[0].upper() in app.SUPER_SET:
                app.run_function(command[0], command)
            else:
                print(Style.RED("function could not be found"))

        else:  # error(->)
            print(Style.YELLOW("[-] Unknown command:") + app.pretty_print(command))


if __name__ == '__main__':
    tb_app = App("main-")

    tb_img = tb_app.save_load("welcome").print_t

    tb_img()

    tb_app.save_load("cloudM").load_mods(tb_app.save_load)

    main(tb_app, tb_img)

    print("\n\n\n\tEXIT")
    input("Press Enter to EXIT")



#    MACRO = ['HELP', 'LOAD-MOD', 'LOGS', 'EXIT', '_hr', '..', 'TEST']
#    MACRO_color = {'HELP': 'GREEN',
#                   'LOAD-MOD': 'BLUE',
#                   'EXIT': 'RED',
#                   'TEST': 'YELLOW',
#                   '..': 'MAGENTA',
#                   'LOGS': 'MAGENTA'
#                   }
#    MOD_LIST = {}
#    HELPER = {
#        'HELP': [['Information', 'version : 0.1.0', 'color : GREEN', 'syntax : help [command]',
#                  'help is available in all subsets']],
#        'LOAD-MOD': [['Information', 'version : 0.1.0', 'color : BLUE', 'syntax : LOAD-MOD [filename]',
#                      'file must be in mods folder ']],
#        'EXIT': [['Information', 'version : 0.1.0', 'color : RED', 'syntax : EXIT',
#                  'The only way to exit in TOOL BOX']],
#        '..': [['Information', 'version : 0.1.0', 'color : MAGENTA', 'syntax : ..',
#                'Brings u Back to Main']],
#        'LOGS': [['Information', 'version : 0.1.0', 'color : MAGENTA', 'syntax : LOGS',
#                  'show logs']],
#        '_hr': [['Information', 'version : ----', 'Hotreload all mods']],
#        'TEST': [['Test Function', 'version : ----', Style.RED('Code can crash')]]
#    }
#       helper~~~:{'HELP': [['Information', 'version : 0.1.0', 'color : GREEN',
#       'syntax : help [command]', 'help is available in all subsets']],
#       'LOAD-MOD': [['Information', 'version : 0.1.0', 'color : BLUE',
#       'syntax : LOAD-MOD [filename]', 'file must be in mods folder ']],
#       'EXIT': [['Information', 'version : 0.1.0', 'color : RED',
#       'syntax : EXIT', 'The only way to exit in TOOL BOX']],
#       '..': [['Information', 'version : 0.1.0', 'color : MAGENTA',
#       'syntax : ..', 'Brings u Back to Main']], 'LOGS': [['Information',
#       'version : 0.1.0', 'color : MAGENTA', 'syntax : LOGS', 'show logs']],
#       '_hr': [['Information', 'version : ----', 'Hotreload all mods']]}
#       macro~~~~:['HELP', 'LOAD-MOD', 'LOGS', 'EXIT', '_hr', '..', 'CLS']
#       m_color~~:{'HELP': 'GREEN', 'LOAD-MOD': 'BLUE', 'EXIT': 'RED', 'CLS': 'YELLOW',
#       '..': 'MAGENTA', 'LOGS': 'MAGENTA'}
#       debug~~~~:True
#
#

