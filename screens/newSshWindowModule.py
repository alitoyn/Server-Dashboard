def newSshWindow():
	from Functions import displayFunctions
	from Functions import controlFunctions

	displayFunctions.clearTerminal()

	displayFunctions.printServerList()

	selectedServer = int(controlFunctions.getUserInput())

	createNewSshConnection(selectedServer)


def createNewSshConnection(selectedServer):
	import config, os
	
	bashCommand = config.default_terminal + ' --command "ssh -i ' + config.server_key[selectedServer] + ' -p ' + config.server_port[selectedServer] + ' ' + config.server_user[selectedServer] + '@' + config.server_ip[selectedServer] + '"'

	os.system(bashCommand)