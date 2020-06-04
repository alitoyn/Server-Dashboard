# This file creates the config file for the server-dashboard.py program
import sys, time
import functions

# find if config file exists and then prompt user to overwrite if it does --------------------------------------------------
try: 				# try to import file
	from config import *
	print("Config file already exisits")
	found = 1	
except:				# catch the exception if it does not exisit
	found = 0
	print("Config file not found")

if found == 1:	# if it does exist, primpt the user
	while 1:
			response = input("\nWould you like to overwrite it? (y/n)\n")
			# if they do not want to overwrite, close the program
			if response == 'n' or response == 'N':
				print("Rename your existing config file and then re-run this program")
				sys.exit()
			# if they do want to overwrite, leave the while loop
			elif response == 'y' or response == 'Y':
				print("input was yes")
				break
			# catch invalid responses
			else:
				print("Input invalid")
				time.sleep(0.5)




# open the config file
file = open("config.py","w")

# write in the header text -------------------------------------------------------------------------------------------------
divider_width = 125 # this is the length of the divider lines to print in the file

text = "# This file is the config for server-dashboard by Ali Toyn"
file.write(functions.getScreenDivider(text, divider_width))					# this function adds the dividers into the file

file.write("\n")
text = "# The description of all of the variables are listed below:"
file.write(functions.getScreenDivider(text, divider_width))

file.write("\n# server_name[x] = human friendly name for server\n")
file.write("# server_user[x] = username to log in to server\n")
file.write("# server_key[x] = path to ssh private key\n")
file.write("# server_ip[x] = ip address of server\n")

file.write("\n")
text = "# These variables are optional for each connection:"
file.write(functions.getScreenDivider(text, divider_width))

file.write("\n# additional_storage[x] = the mount location of an additional storage location to show data for\n")
file.write("# extra_logfile_name[x][y] = the name of a log file to track\n")
file.write("# extra_logfile_location[x][y] = the path to an additional logfile\n")

file.write("\n")
text = "# This option is needed to show info about your folding at home user:"
file.write(functions.getScreenDivider(text, divider_width))
file.write("\n# foldingUserID = the user ID for your F@H account\n")

file.write("\n")
file.write(functions.getScreenDivider("# Config Data", divider_width))

