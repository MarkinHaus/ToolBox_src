from mods.mainTool import MainTool  # , FileHandler
from Style import Style
import os
from subprocess import check_output
import sys
import ctypes


def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except Exception as e:
		print("ERROR: %s" %e)
		return False


class Tools(MainTool):  # FileHandler

	def __init__(self, app=None):
		self.version = "0.0.1"
		self.name = "cmd"
		self.logs = app.logs_ if app else None
		self.color = "WHITE"
		self.tools = {
			"all": [["Version", "Shows current Version"],
					["run", "run cmd commands"],
					["info", "get system info"],
					["download", "download modules"],
					["ls", "run exa modules"],
					],
			"name": "cmd",
			"Version": self.show_version,
			"run": self.run,
			"info": self.info,
			"ls": self.ls,
			"download": self.download,
		}
		# FileHandler.__init__(self, "File name")
		MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
						  name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

	def show_version(self):
		self.print("Version: ", self.version)

	def on_start(self):
		pass

	def on_exit(self):
		pass

	def run(self, command):
		if len(command) >= 1:
			user_input = ""
			for i in command[1:]:
				user_input += i + " "
			user_input = user_input.strip()
			self.print(f"{user_input=}\n")

			if "cd" in user_input:
				if user_input == "cd":
					os.system(f"{user_input}")
				else:
					os.chdir(f"{user_input.replace('cd ', '')}")
			else:
				if user_input == "admin":
					admin = is_admin()
					self.print("is admin :", admin)
					if admin:
						os.system("netstat -b")
					else:
						# Re-run the program with admin rights
						ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
				else:
					os.system(user_input)

		else:
			self.print((Style.YELLOW("SyntaxError : run cmd_command")))

	def info(self):
		for i in list(os.uname()):
			self.print(i)
		print("https://www.youtube.com/watch?v=dQa9mveTSV4")

	def download(self, command):

		if len(command) > 1:
			os.system("sudo apt install "+command[1])
		else:
			print("downloadable commands")
			for i in ['exa', '']:
				print(i)

	def ls(self, command):
		self.print(Style.RED("module not found pleas install | command : ") + Style.WHITE("download exa"))
		check_output("exa", shell=True, universal_newlines=True)
		print(" "*100, end="\r")

		if len(command) > 1:
			self.run(["exa"]+command[1:])
		else:
			self.run(["exa"])
