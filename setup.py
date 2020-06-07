# This file creates the config file for the server-dashboard.py program
import sys, time
import functions

# find if config file exists and then prompt user to overwrite if it does --------------------------------------------------
try: 				# try to import file
	# open the config file
	file = open("config.py","r")
	file.close()
	print("Config file already exists")
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
text = "# This option is needed to open additional terminal windows:"
file.write(functions.getScreenDivider(text, divider_width))
file.write("\n# default_terminal = the terminal you want to use\n")

file.write("\n")
file.write(functions.getScreenDivider("# Config Data", divider_width))

# init empty lists to fill later on ----------------------------------------------------------------------------------------
text = "# Leave this section here to init empty lists"
file.write(functions.getScreenDivider(text, divider_width))
file.write("server_name = {}\n")
file.write("server_user = {}\n")
file.write("server_key = {}\n")
file.write("server_ip = {}\n")
file.write("server_storage = {}\n")
file.write("additional_storage = {}\n")
file.write("extra_logfile_name = [[0 for i in range(10)] for j in range(10)]\n")
file.write("extra_logfile_location = [[0 for i in range(10)] for j in range(10)]\n")

# start the user added data section ----------------------------------------------------------------------------------------

allowed_inputs = ["y", "Y", "n", "N"]

count = 0

while 1:
		# for the first loop assume the user does want to add a server
	if count != 0:
		response = functions.dataVal("\nWould you like to add another server? (y/n)\n", allowed_inputs)
	else:
		response = "y"

	# check response, if the answer is no, then break the loop
	if response == "N" or response == 'n':
		break
	
	# otherwise start taking data
	else:
		file.write("\n")
		file.write(functions.getScreenDivider("# Data for server[" + str(count) + "]", divider_width))
		
		# get server name
		response = input("\nWhat is the name of the server?\n")
		file.write("server_name[" + str(count) + "] = '" + response + "'\n")

		# get server user
		response = input("\nWhat is the username to login with?\n")
		file.write("server_user[" + str(count) + "] = '" + response + "'\n")

		# get server ip
		response = input("\nWhat is IP address of the server? e.g. 192.168.X.X or myip.com\n")
		file.write("server_ip[" + str(count) + "] = '" + response + "'\n")

		# get server port number
		response = input("\nWhich port would you like to use for the SSh connection? e.g. default is 22\n")
		file.write("server_port[" + str(count) + "] = '" + response + "'\n")

		# get ssh key location
		response = input("\nWhat path to the ssh private key? e.g. /home/user/.ssh/key\n")
		file.write("server_key[" + str(count) + "] = '" + response + "'\n")

		# Does the user have an additional storage location
		response = functions.dataVal("\nDo you have an additional storage location you want to see data for? (y/n)\n", allowed_inputs)
		if response == 'Y' or response == 'y':
			response = input("\nWhat is the path to the additional storage? e.g. /mount/drive\n")
			file.write("additional_storage[" + str(count) + "] = '" + response + "'\n")

		
		# Does the user have any logfiles they want to track
		response = functions.dataVal("\nDo you have a logfile you want to track? (y/n)\n", allowed_inputs)
		
		if response == 'y' or response == 'Y':
			logfile_count = 0
			
			while 1:
				if logfile_count != 0:
					response = functions.dataVal("\nWould you like to add another logfile? (y/n)\n", allowed_inputs)
				else:
					response = "y"

				if response == 'N' or response =='n':
					break

				response = input("\nWhat is the name of the logfile?\n")
				file.write("extra_logfile_name[" + str(count) + "][" + str(logfile_count) + "] = '" + response + "'\n")

				response = input("\nWhat is the path to the logfile? e.g. /backups/log.txt\n")
				file.write("extra_logfile_location[" + str(count) + "][" + str(logfile_count) + "] = '" + response + "'\n")

				logfile_count += 1

		
		count += 1

file.write("\n")
file.write(functions.getScreenDivider("# Additional Data", divider_width))
file.write("\n")

# get folding data
response = functions.dataVal("\nDo you want to track your F@H stats? (y/n)\n", allowed_inputs)
if response == 'Y' or response == 'y':
	response = input("\nWhat is your F@H user ID?\n")
	file.write("foldingUserID = '" + response + "'\n")
else:
	file.write("foldingUserID = ''\n")

# get default terminal name
response = input("\nWhat is your default terminal? This is needed to open additional windows\n")
file.write("default_terminal = '" + response + "'\n")

file.close()

print("Setup Successful")  