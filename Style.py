import os
from platform import system
from time import sleep

def cls():
    if system() == "Windows":
        os.system("cls")
    if system() == "Linux":
        os.system("clear")

class Style:
    _BLACK = '\u001b[30m'
    _RED = '\u001b[31m'
    _GREEN = '\u001b[32m'
    _YELLOW = '\u001b[33m'
    _BLUE = '\u001b[34m'
    _MAGENTA = '\u001b[35m'
    _CYAN = '\u001b[36m'
    _WHITE = '\u001b[37m'
    _END = '\u001b[0m'

    _Bold = '\u001b[1m'
    _Underline = '\u001b[4m'
    _Reversed = '\u001b[7m'

    style_dic = {
        "BLACK": _BLACK,
        "RED": _RED,
        "GREEN": _GREEN,
        "YELLOW": _YELLOW,
        "BLUE": _BLUE,
        "MAGENTA": _MAGENTA,
        "CYAN": _CYAN,
        "WHITE": _WHITE,
        "END": _END,
        "Bold": _Bold,
        "Underline": _Underline,
        "Reversed": _Reversed
    }

    @staticmethod
    def END_():
        print(Style._END)

    @staticmethod
    def GREEN_():
        print(Style._GREEN)

    @staticmethod
    def BLUE(text: str):
        return Style._BLUE + text + Style._END

    @staticmethod
    def BLACK(text: str):
        return Style._BLACK + text + Style._END

    @staticmethod
    def RED(text: str):
        return Style._RED + text + Style._END

    @staticmethod
    def GREEN(text: str):
        return Style._GREEN + text + Style._END

    @staticmethod
    def YELLOW(text: str):
        return Style._YELLOW + text + Style._END

    @staticmethod
    def MAGENTA(text: str):
        return Style._MAGENTA + text + Style._END

    @staticmethod
    def CYAN(text: str):
        return Style._CYAN + text + Style._END

    @staticmethod
    def WHITE(text: str):
        return Style._WHITE + text + Style._END

    @staticmethod
    def Bold(text: str):
        return Style._Bold + text + Style._END

    @staticmethod
    def Underline(text: str):
        return Style._Underline + text + Style._END

    @staticmethod
    def Reversed(text: str):
        return Style._Reversed + text + Style._END

    @staticmethod
    def loading_al(text: str):

        b = f"{text} /"
        print(b)
        sleep(0.05)
        cls()
        b = f"{text} -"
        print(b)
        sleep(0.05)
        cls()
        b = f"{text} \\"
        print(b)
        sleep(0.05)
        cls()
        b = f"{text} |"
        print(b)
        sleep(0.05)
        cls()

    @property
    def END(self):
        return self._END

