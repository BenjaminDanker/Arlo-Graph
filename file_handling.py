# Handles settings tab that deals with the limits and saving into a file

import tkinter
from tkinter import ttk
import pickle

from lines import Lines


class Settings:
	limit_dict = pickle.load(open("limits.pkl", "rb"))

	def __init__(self):
		self.limit_dict = Settings.limit_dict
		self.settings_system = tkinter.Tk()
		self.row = 0


	# saves limit_dict into pickle file
	# called from Settings.settings_main()
	def save(self):
		pickle.dump(self.limit_dict, open("limits.pkl", "wb"))


	# removes limit row
	# called from Settings.row_create()
	def row_remove(self, key_label, low_value_label, high_value_label, remove_button, current_key):
		del self.limit_dict[current_key]

		key_label.destroy()
		low_value_label.destroy()
		high_value_label.destroy()
		remove_button.destroy()


	# creates limit row
	# called from Settings.settings_main() and Settings.row_add()
	def row_create(self):
		current_key = self.keys_list[self.num]


		key_label = ttk.Label(self.settings_system, text=self.keys_list[self.num])
		key_label.grid(row=self.row+3, column=2)

		low_value_label = ttk.Label(self.settings_system, text=self.values_list[self.num]["low"])
		low_value_label.grid(row=self.row+3, column=3)

		high_value_label = ttk.Label(self.settings_system, text=self.values_list[self.num]["high"])
		high_value_label.grid(row=self.row+3, column=4)


		remove_button = ttk.Button(self.settings_system, text="x",
			command=lambda:Settings.row_remove(self, key_label, low_value_label, high_value_label, remove_button, current_key))
		remove_button.grid(row=self.row+3, column=1)


	# adds a row from entries once add button is clicked
	# called from Settings.settings_main()
	def row_add(self):
		try:
			if self.name_entry.get() not in self.limit_dict:
				limit_dict = {self.name_entry.get():{"low":int(self.minimum_entry.get()), "high":int(self.maximum_entry.get())}}
				self.limit_dict.update(limit_dict)

				self.keys_list = list(limit_dict.keys())
				self.values_list = list(limit_dict.values())

				self.num = 0
				self.row = self.row + 1

				self.row_create()
		except ValueError:
			pass



	# create settings interface
	# called from main.py main()
	def settings_main(self):
		self.settings_system.title("Settings")
		self.settings_system.iconbitmap("matplotlib_large.ico")

		# row 0
		save_button = ttk.Button(self.settings_system, text="Save", command=self.save)
		save_button.grid(row=0, column=0, sticky="NW")

		text = ttk.Label(self.settings_system, text = "Name")
		text.grid(row=0, column=2, sticky="S")

		text = ttk.Label(self.settings_system, text = "Minimum")
		text.grid(row=0, column=3, sticky="S")

		text = ttk.Label(self.settings_system, text = "Maximum")
		text.grid(row=0, column=4, sticky="S")

		# row 1
		add_button = ttk.Button(self.settings_system, text="Add", command=self.row_add)
		add_button.grid(row=1, column=1, sticky="W", padx=10, pady=10)

		self.name_entry = tkinter.Entry(self.settings_system)
		self.name_entry.grid(row=1, column=2, padx=10)

		self.minimum_entry = tkinter.Entry(self.settings_system)
		self.minimum_entry.grid(row=1, column=3, padx=10)

		self.maximum_entry = tkinter.Entry(self.settings_system)
		self.maximum_entry.grid(row=1, column=4, padx=10)

		# pads row 2
		text = ttk.Label(self.settings_system, text = "")
		text.grid(row=2, column=0)

		# row n
		self.keys_list = list(self.limit_dict.keys())
		self.values_list = list(self.limit_dict.values())
		for self.num, c in enumerate(self.limit_dict):
			self.row = self.num
			Settings.row_create(self)


		self.settings_system.mainloop()