import os
import string
from Style import Style


class MainTool:
    def __init__(self, *args, **kwargs):
        self.version = kwargs["v"]
        self.tools = kwargs["tool"]
        self.name = kwargs["name"]
        self.logs = kwargs["logs"]
        self.color = kwargs["color"]
        self.load(kwargs["load"])
        self._on_exit = kwargs["on_exit"]

    def load(self, todo):
        if todo:
            todo()
            self.logs.append([self, "load successfull"])
        else:
            self.logs.append([self, "no load require"])
        print(f"TOOL successfully loaded : {self.name}")
        self.logs.append([self, "TOOL successfully loaded"])

    def print(self, message, *args, end="\n"):
        print(Style.style_dic[self.color]+self.name + Style.style_dic["END"] + ":", message, *args, end=end)


class Code:
    @staticmethod
    def decode_code(data):
        #letters = string.ascii_letters + string.digits + string.punctuation
        #decode_str = ''
        #data_n = data.split('#')
        #data = []
        #for data_z in data_n[:-1]:
        #    data.append(float(data_z))
        #i = 0
        #for data_z in data:
        #    ascii_ = data_z * 2
        #    decode_str += letters[int(ascii_)]
        #    i += 1
        #decode_str = decode_str.replace('-ou-', 'u')
        #decode_str = decode_str.split('@')
        #return decode_str
        return data

    @staticmethod
    def encode_code(data):
        #letters = string.ascii_letters + string.digits + string.punctuation
        #encode_str = ''
        #data = data.replace(' ', '@')
        #leng = data.__len__()
        #for data_st in range(leng):
        #    i = -1
        #    while data[data_st] != letters[i]:
        #        i += 1
        #        if data[data_st] == letters[i]:
        #            encode_str += str(i / 2) + '#'
        #    data_st += 1
        #return encode_str
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
            self.file_handler_storage = open(self.file_handler_file_prefix+self.file_handler_filename, mode)
        except FileNotFoundError:
            print(Style.RED(f"File not found: {self.file_handler_file_prefix}{self.file_handler_filename}"))
            if input("Do you want to create this path | file ? (y/n) ") in ['y', 'yes', 'Y']:
                if not os.path.exists(f"{self.file_handler_file_prefix}"):
                    os.makedirs(f"{self.file_handler_file_prefix}")
                open(self.file_handler_file_prefix+self.file_handler_filename, 'a').close()
                print("File created successfully")
                rdu()
            else:
                print(Style.YELLOW(f"pleas create this file to prosed : {self.file_handler_file_prefix}"
                                   f"{self.file_handler_filename}"))
                exit(0)

    def open_s_file_handler(self):
        self.open_file_handler('w+', self.open_s_file_handler)

    def open_l_file_handler(self):
        self.open_file_handler('r+', self.open_l_file_handler)

    def save_file_handler(self):
        for pos, data in enumerate(self.file_handler_auto_save.keys()):
            if self.file_handler_auto_save[data]:
                self.add_to_save_file_handler(data, self.file_handler_load[pos][1])
        if not self.file_handler_storage:
            print("WARNING pleas open storage")
        for line in self.file_handler_save:
            self.file_handler_storage.write(line)
            self.file_handler_storage.write('\n')

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
        return self.file_handler_load

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
