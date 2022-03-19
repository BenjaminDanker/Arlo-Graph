from tkinter import ttk, Tk

from plot import Plot
from setup import Setup
from file_handling import Settings
from lines import Lines

# first setup, then creates main tkinter
def main():
	Setup.msaccess_check()

	system = Tk()
	system.title("Process Graph")
	system.iconbitmap("matplotlib_large.ico")

	plot_instance = Plot()

	opns = ttk.Button(text="Open Folder",command=lambda:[Lines.path_folder(), Lines.lines_folder(), plot_instance.check_buttons()])
	opns.grid(column=0,row=0,sticky="W")
	opn = ttk.Button(text="Open File",command=lambda:[Lines.path_file(), Lines.lines_file(), plot_instance.check_buttons()])
	opn.grid(column=0,row=1,sticky="W") 
	sein = ttk.Button(text="Settings",command=lambda:Settings().settings_main())
	sein.grid(column=1,row=0,sticky="W")
	plot = ttk.Button(text="Plot",command=plot_instance.matplotlib_plot)
	plot.grid(column=1,row=1)

	txt = ttk.Label(text = "                               ")
	txt.grid(column=2,row=0,sticky="W")
	text = ttk.Label(text = "")
	text.grid(row=2, column=0,sticky="W")
	text = ttk.Label(text = "")
	text.grid(row=2, column=1,sticky="W")

	text = ttk.Label(text = "Tanks")
	text.grid(row=3, column=0,sticky="W")
	text = ttk.Label(text = "   Limits")
	text.grid(row=3, column=1,sticky="W")

	system.mainloop()

if __name__ == "__main__":
	main()