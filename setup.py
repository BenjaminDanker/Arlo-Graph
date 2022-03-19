# handles the setup for Microsoft Access 2010

class Setup:
	# checks for mcaccess 64 and 32
	# called from main.py main()
	def msaccess_check():
		msaccess_x86 = False
		msaccess_x = False

		try:
			open("C:/Program Files (x86)/Microsoft Office/Office14/MSACCESS.exe")
			mcaccess_x86 = True
		except FileNotFoundError:
			mcaccess_x86 = False

		try:
			open("C:/Program Files/Microsoft Office/Office14/MSACCESS.exe")
			mcaccess_x = True
		except FileNotFoundError:
			mcaccess_x = False

		if mcaccess_x86 == False and mcaccess_x == False:
			system("AccessRuntime.exe")