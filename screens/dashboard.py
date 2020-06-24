def displayDashboard(sshConnection, selectedServer):
	import config
	from Functions import dataFunctions, controlFunctions, foldingFunctions, displayFunctions

	currentScreen = 'd'

	print("\nLoading...\n")

	# These commands above the clear take some time so better to hide them behind 'loading'
	rootStorage = dataFunctions.getRootStorage(sshConnection)
	additionalStorage = dataFunctions.getAdditionalStorage(config.additional_storage[selectedServer], sshConnection)

	updates = dataFunctions.getUpdateData(sshConnection)
	

	displayFunctions.clearTerminal()

	print(' Server Information: ' + config.server_name[selectedServer])

	serverUptime = dataFunctions.getUptime(sshConnection)
	print(serverUptime + '\n')

	serverTempInfo = dataFunctions.getTempInfo(sshConnection)
	print(serverTempInfo)
	
	displayFunctions.printStorageData(rootStorage, additionalStorage)

	displayFunctions.printUpdateData(updates)    

	foldingLogData = foldingFunctions.getFoldingLogData(sshConnection)
	displayFunctions.printFoldingData(foldingLogData)
		
	numberOfLogFiles = dataFunctions.getNumberOfLogFiles(config.extra_logfile_name[selectedServer])

	if numberOfLogFiles != 0:
		for i in range(numberOfLogFiles):
			displayFunctions.printLogFiles(sshConnection, config.extra_logfile_name[selectedServer][i], config.extra_logfile_location[selectedServer][i])

	print(' Select "0" to view processess and CPU load\n')