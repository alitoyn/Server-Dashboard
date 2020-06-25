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

	print('Server Information: ' + config.server_name[selectedServer])

	serverUptime = dataFunctions.getUptime(sshConnection)
	print(serverUptime + '\n')

	serverTempInfo = dataFunctions.getTempInfo(sshConnection)
	print('Package temperature:')
	print(serverTempInfo)
	
	print('Storage:')
	displayFunctions.printStorageData(rootStorage, additionalStorage)

	printUpdateData(updates)    

	foldingLogData = foldingFunctions.getFoldingLogData(sshConnection)
	printFoldingData(foldingLogData)
		
	numberOfLogFiles = getNumberOfLogFiles(config.extra_logfile_name[selectedServer])

	if numberOfLogFiles != 0:
		for i in range(numberOfLogFiles):
			printLogFiles(sshConnection, config.extra_logfile_name[selectedServer][i], config.extra_logfile_location[selectedServer][i])

	print('Select "0" to view processess and CPU load\n')


def printUpdateData(updateData):

	if updateData != None:                
		print("Update status:\n " + updateData.split(' ')[0] + " packages to update")
		print("")
	else:
		print("Update status:\n Failed to get update data")
		print("")


def printFoldingData(foldingData):
	print("Folding Status:")
	print(' ' + foldingData)

def printLogFiles(sshConnection, logfileName, logfileLocation):
	from Functions import dataFunctions

	bashCommandToPrintLogfile = 'tail -1 ' + logfileLocation

	print(logfileName + ":")
	try:
		print(" " + dataFunctions.commandSend(sshConnection, bashCommandToPrintLogfile))
	except:
		print(" Logfile parse failed")
	print("")

def getNumberOfLogFiles(logFileArray):
	arrayInitialisedTo = 0

	numberOfLogFiles = 0

	for i in range(len(logFileArray)):
		if logFileArray[i] == 0:
			break
		else:
			numberOfLogFiles += 1

	return numberOfLogFiles