# Handles getting path and file from .mdb files

from tkinter import filedialog
from os import walk
from tkinter import ttk
import pyodbc

class Lines:
	path = None
	tanks_line = None
	lines = None

	# sets path of folder
	# called from main.py main()
	def path_folder():
		try:
			Lines.path = filedialog.askdirectory(initialdir=Lines.path,title="Select Folder")
		except NameError:
			directory = Lines.path.dirname(Lines.path.abspath(__file__))[::-1]
			for num, c in enumerate(directory):
				if c == "\\":
					directory = directory[num:]
					directory = directory[::-1]
					break

			Lines.path = filedialog.askdirectory(initialdir=directory,title="Select Folder")

	# sets path of file
	# called from main.py main()
	def path_file():
		try:
			Lines.path = filedialog.askopenfilename(initialdir=Lines.path,title="Select File", filetypes=[("mdb","*.mdb")])
		except NameError:
			directory = Lines.path.dirname(Lines.path.abspath(__file__))[::-1]
			for num, c in enumerate(directory):
				if c == "\\":
					directory = directory[num:]
					directory = directory[::-1]
					break

			Lines.path = filedialog.askopenfilename(initialdir=directory,title="Select File", filetypes=[("mdb","*.mdb")])



	# sets the contents of the folder of .mdb files as list
	# called from main.py main()
	def lines_folder():
		path_dict = {}
		path_list = []
		lines = []
		invcount = 0
		for (path, directory_names, file_names) in walk(Lines.path):
			for c in file_names:
				if c[len(c)-4:] == ".mdb":
					if c[len(c)-7:] == "old.mdb":
						c_new  = c[:len(c)-9] + "0" + ".mdb"
					else:
						c_new  = c[:len(c)-5] + "1" + ".mdb"
					path_list.append(c_new)
					path_dict.update({c_new:path+"/"+c})

		path_list = sorted(path_list)
		for c in path_list:
			try:
				pyodbc_connection = pyodbc.connect('Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path};'.format(path=path_dict[c])).cursor()

				for column_name in pyodbc_connection.columns():
					column_name = column_name[2]

				SQL = 'SELECT * FROM {column_name};'.format(column_name=column_name)
				lines = lines + pyodbc_connection.execute(SQL).fetchall()
			except:
				invcount += 1
				txt = ttk.Label(text = "{invcount} Invalid Files".format(invcount=invcount))
				txt.grid(column=2,row=0,sticky="W")

		SQL = 'SELECT * FROM AlarmValue;'
		Lines.tanks_line = pyodbc_connection.execute(SQL).fetchall()
		Lines.lines = lines

	# sets the contents of the .mdb file as list
	# called from main.py main()
	def lines_file():
		try:
			pyodbc_connection = pyodbc.connect('Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path};'.format(path=Lines.path)).cursor()

			for column_name in pyodbc_connection.columns():
				column_name = column_name[2]

			SQL = 'SELECT * FROM {column_name};'.format(column_name=column_name)
			Lines.lines = pyodbc_connection.execute(SQL).fetchall()

			SQL = 'SELECT * FROM AlarmValue;'
			Lines.tanks_line = pyodbc_connection.execute(SQL).fetchall()
			
		except:
			text = ttk.Label(text = "Invalid File")
			text.grid(column=2,row=0,sticky="W")