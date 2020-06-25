def newSshWindow():
	from Functions import displayFunctions
	from Functions import controlFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	displayFunctions.printServerList()

	allowedInputs = dataFunctions.getListOfServerIndicies()
	selectedServer = int(dataFunctions.checkInputAgainstList_int(allowedInputs))

	createNewSshConnection(selectedServer)


def createNewSshConnection(selectedServer):
	import config, os
	
	bashCommand = config.default_terminal + ' --command "ssh -i ' + config.server_key[selectedServer] + ' -p ' + config.server_port[selectedServer] + ' ' + config.server_user[selectedServer] + '@' + config.server_ip[selectedServer] + '"'

	os.system(bashCommand)