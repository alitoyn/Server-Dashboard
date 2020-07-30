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
	allowedInputs = dataFunctions.getListOfServerIndicies()
	chosenServerIndex = dataFunctions.checkInputAgainstList_int(allowedInputs)

	printListOfAvailableCommands(bashCommandDictionary)
	
	allowedInputs = range(len(bashCommandDictionary))
	chosenCommandIndex = dataFunctions.checkInputAgainstList_int(allowedInputs)

	chosenBashCommand = getBashCommandFromIndex(chosenCommandIndex, bashCommandDictionary)

	initiateCommandInNewWindow(chosenServerIndex, bashCommandDictionary[chosenBashCommand])

	
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

	command = config.default_terminal + ' "ssh -t -i ' + config.server_key[chosenServerIndex] + ' -p ' + config.server_port[chosenServerIndex] + ' -t ' + config.server_user[chosenServerIndex] + '@' + config.server_ip[chosenServerIndex] + ' ' + commandToRun + '"'
	os.system(command)

def getBashCommandFromIndex(chosenCommandIndex, bashCommandDictionary):
	count = 0
	for i in bashCommandDictionary:
		if count == chosenCommandIndex:
			return i
		else:
			count += 1