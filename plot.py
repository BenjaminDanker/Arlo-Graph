# Handles the checkmark boxes from tkinter and matplotlib plotting

import tkinter
from tkinter import filedialog, ttk
from tkinter import BooleanVar
from tkinter.ttk import Checkbutton
from matplotlib import dates
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedFormatter, LinearLocator
from matplotlib.dates import DateFormatter
import pandas as pd
from pandas.tseries.offsets import Minute
import datetime

from lines import Lines
from file_handling import Settings


class Plot:
	# plots after Plot button is pushed
	# called from main.py main()
	def matplotlib_plot(self):
		plt.close()


		# graphing box size ratio
		plt.rcParams["figure.figsize"]=6,3

		# get plot info
		fig,axes=plt.subplots()


		# set beginning and end of the x-axis
		start_date = self.lines[0][len(self.lines[0])-2]
		end_date = self.lines[len(self.lines)-1][len(self.lines[0])-2]

		axes.set_xlim([start_date,end_date])


		# graphing
		for num,(check_button, tank_names) in enumerate(zip(self.boolean_check_tank_list, self.tank_names_list)):
			if check_button.get() == True:

				# graphing temperature line
				date_datetime_list = {}
				for num2, c in enumerate(self.lines):
					date_time = c[len(self.lines[num2])-2]

					c = c[1:len(c)-2]
					temperature = c[num]

					date_datetime_list.update({date_time:temperature})

				date_pandas = pd.Series(date_datetime_list)
				current_line = axes.plot(date_pandas, label=tank_names)


				# graphing limit line
				if self.boolean_check_limit_list[num].get() == True:
					low_limit_dict = {start_date:self.tank_name_limit_dict[tank_names]["low"], end_date:self.tank_name_limit_dict[tank_names]["low"]}
					low_limit_line_pandas = pd.Series(low_limit_dict)
					axes.plot(low_limit_line_pandas, current_line[0].get_color(), alpha=.3)

					high_limit_dict = {start_date:self.tank_name_limit_dict[tank_names]["high"], end_date:self.tank_name_limit_dict[tank_names]["high"]}
					high_limit_line_pandas = pd.Series(high_limit_dict)
					axes.plot(high_limit_line_pandas, current_line[0].get_color(), alpha=.3)


		# legend
		axes.legend(loc="upper right",bbox_to_anchor=(1,1))

		# date format
		axes.xaxis.set_major_formatter(DateFormatter("%d-%m-%Y %H:%M:%S"))

		# x-axis view settings
		axes.tick_params(axis="x",rotation=20,labelsize=8,which="major")

		# graphing box positioning
		plt.subplots_adjust(left=.04,bottom=.09,right=.99,top=.97)

		# labels
		plt.xlabel("Time")
		plt.ylabel("Temperature(F) / Humidity(%)")

		# grid lines' settings
		plt.grid(b=True,which="major",color=".8")

		# graph title
		plt.title("Process Monitor")


		plt.show()


	# creates checkmark boxes from tkinter
	# called from main.py main()
	def check_buttons(self):
		if Lines.path != "":
			self.lines = Lines.lines
			self.tanks_line = Lines.tanks_line
			self.tank_name_limit_dict = Settings.limit_dict


			self.boolean_check_limit_list = []
			self.boolean_check_tank_list = []
			self.tank_names_list = []
			row = 3
			for num, c in enumerate(self.tanks_line):
				c = c[1]
				row = row + 1

				# tank check boxes
				self.boolean_check_tank_list.append(BooleanVar())
				self.tank_names_list.append(c)
				check = Checkbutton(text=c,variable=self.boolean_check_tank_list[num])
				check.grid(column=0,row=row,sticky="W")

				# limit check boxes
				try:
					self.boolean_check_limit_list.append(BooleanVar())
					check = Checkbutton(text=str(self.tank_name_limit_dict[c]["low"])+"-"+str(self.tank_name_limit_dict[c]["high"]),variable=self.boolean_check_limit_list[num])
					check.grid(column=1,row=row,sticky="W")

				except KeyError:
					pass

		else:
			print("check button else")
			text = ttk.Label(text = "Invalid File")
			text.grid(column=2,row=0,sticky="W")