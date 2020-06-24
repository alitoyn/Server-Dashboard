def getCommandAndSend():
	import config
	from Functions import displayFunctions
	from Functions import dataFunctions
	from Functions import controlFunctions

	bashCommandsToInstallDependancies = constructInstallDependanciesCommand()

	bashCommandDictionary = {
		'Shutdown': 'sudo shutdown',
		'Reboot': 'sudo reboot',
		'Run Updates': 'sudo apt upgrade && sleep 1',
		'Install Dependancies': bashCommandsToInstallDependancies

	}

	displayFunctions.clearTerminal()

	print("Which server do you want to send a command:")

	displayFunctions.printServerList()
	chosenServerIndex = int(controlFunctions.getUserInput())

	printListOfAvailableCommands(bashCommandDictionary)
	chosenCommandIndex = int(controlFunctions.getUserInput())

	chosenBashCommand = getBashCommandFromIndex(chosenCommandIndex, bashCommandDictionary)

	initiateCommandInNewWindow(chosenServerIndex, bashCommandDictionary[chosenBashCommand])

	# # send command page
	# if selectedScreen == "c":
	#     # display info
	#     os.system('clear')
	#     print("\nThis is currently for show and does nothing\n")
	#     print("Which server do you want to send a command:")
	#     for i in range(len(server_name)):
	#         print(str(i) + ": " + server_name[i])
	#     print("")

	#     while selectedScreen == "c":
	#         for i in range(0, 120):
	#             time.sleep(0.5)
	#             if selectedScreen != "c":
	#                 break
		
	#     serverToSendCommand = int(selectedScreen)
	#     selectedScreen = "c"

	#     print("\nChoose command to send to " + server_name[serverToSendCommand])
	#     print("0: Shutdown")
	#     print("1: Reboot")
	#     print("2: Run Updates")
	#     print("3: Install Dependancies")
	#     print("")
	#     while selectedScreen == "c":
	#         for i in range(0, 120):
	#             time.sleep(0.5)
	#             if selectedScreen != "c":
	#                 break

	#     commandToSendServer = int(selectedScreen)
	#     passedCommand_2 = 0
	#     selectedScreen = "c"

	#     # set command
	#     if(commandToSendServer == 0):
	#         passedCommand = 'sudo shutdown'
	#     if(commandToSendServer == 1):
	#         passedCommand = 'sudo reboot'
	#     if(commandToSendServer == 2):     
	#         passedCommand = 'sudo apt upgrade && sleep 1'
	#     if (commandToSendServer == 3):

	#         # These are the programs to install
	#         # need to be seperated by spaces
	#         programsToInstall = 'lm-sensors'

	#         # These are any additional commands that need to be run
	#         # need to be seperated by ';'
	#         commandsToRun = 'sudo sensors-detect'

	#         # This is the command sent to the server
	#         # Only change this if the UI of the install needs updating, otherwise use the above two options!
	#         passedCommand = "'sudo apt install " + programsToInstall + "; echo ''; echo 'Press ENTER for all default options, any others are used at your own risk...'; echo ''; sleep 2; " + commandsToRun + "; echo ''; echo 'installation successfull! Window closing...'; sleep 2 '"

		
	#     # initiate command   
	#     print("Opening new window...")
	#     cmd = default_terminal + ' --command "ssh -t -i ' + server_key[serverToSendCommand] + ' -p ' + server_port[serverToSendCommand] + ' -t ' + server_user[serverToSendCommand] + '@' + server_ip[serverToSendCommand] + ' ' + passedCommand + '"'
	#     output = os.system(cmd)
	#     time.sleep(1)

	#     # if passedCommand_2 != 0:
	#     #     cmd = default_terminal + ' --command "ssh -i ' + server_key[serverToSendCommand] + ' -p ' + server_port[serverToSendCommand] + ' -t ' + server_user[serverToSendCommand] + '@' + server_ip[serverToSendCommand] + ' ' + passedCommand_2 + '"'
	#     #     output = os.system(cmd)
	#     #     time.sleep(1)

	#     selectedScreen = "d"



def constructInstallDependanciesCommand():
	# These are the programs to install
	# need to be seperated by spaces
	programsToInstall = 'lm-sensors'

	# These are any additional commands that need to be run
	# need to be seperated by ';'
	commandsToRunOnServer = 'sudo sensors-detect'

	# This is the command sent to the server
	# Only change this if the UI of the install needs updating, otherwise use the above two options!
	constructedBashCommand = "'sudo apt install " + programsToInstall + "; echo ''; echo 'Press ENTER for all default options, any others are used at your own risk...'; echo ''; sleep 2; " + commandsToRunOnServer + "; echo ''; echo 'installation successfull! Window closing...'; sleep 2 '"

	return constructedBashCommand


def printListOfAvailableCommands(availbleCommandsDict):
	count = 0
	for i in availbleCommandsDict:
		print(str(count) + ': ' + i)
		count += 1

def initiateCommandInNewWindow(chosenServerIndex, commandToRun):
	import config, os

	command = config.default_terminal + ' --command "ssh -t -i ' + config.server_key[chosenServerIndex] + ' -p ' + config.server_port[chosenServerIndex] + ' -t ' + config.server_user[chosenServerIndex] + '@' + config.server_ip[chosenServerIndex] + ' ' + commandToRun + '"'
	os.system(command)

def getBashCommandFromIndex(chosenCommandIndex, bashCommandDictionary):
	count = 0
	for i in bashCommandDictionary:
		if count == chosenCommandIndex:
			return i
		else:
			count += 1