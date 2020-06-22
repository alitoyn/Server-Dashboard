def updateTermSize():
	import os
	
	defaultRows = 24
	defualtColumns = 80

	try:
		rows, columns = os.popen('stty size', 'r').read().split()
		return [int(rows), int(columns)]

	except:
		return [defaultRows, defualtColumns]

def displayDashboard(sshConnection, selectedServer):
	import config
	from Functions import dataFunctions, foldingFunctions

	currentScreen = 'd'

	print("\nLoading...\n")

	# These commands above the clear take some time so better to hide them behind 'loading'
	rootStorage = dataFunctions.getRootStorage(sshConnection)
	additionalStorage = dataFunctions.getAdditionalStorage(config.additional_storage[selectedServer], sshConnection)

	updates = dataFunctions.getUpdateData(sshConnection)
	

	clearTerminal()

	print('Server Information: ' + config.server_name[selectedServer])

	serverUptime = dataFunctions.getUptime(sshConnection)
	print(serverUptime + '\n')

	serverTempInfo = dataFunctions.getTempInfo(sshConnection)
	print(serverTempInfo)
	
	printStorageData(rootStorage, additionalStorage)

	printUpdateData(updates)    

	foldingLogData = foldingFunctions.getFoldingLogData(sshConnection)
	printFoldingData(foldingLogData)
		
	numberOfLogFiles = dataFunctions.getNumberOfLogFiles(config.extra_logfile_name[selectedServer])

	if numberOfLogFiles != 0:
		for i in range(numberOfLogFiles):
			printLogFiles(sshConnection, config.extra_logfile_name[selectedServer][i], config.extra_logfile_location[selectedServer][i])


		

def clearTerminal():
	import os

	bashCommandToClearScreen = 'clear'

	os.system(bashCommandToClearScreen)

def printStorageData(rootStorage, additionalStorage):
	integerRootStorage = int(rootStorage.split("%")[0])

	print(" Storage:")
	print('  Root Directory / = ' + rootStorage + " ", end="")                                 
	print(createPercentBar("#", integerRootStorage, 20))
	print("")

	if additionalStorage:
		integerAdditionalStorage = int(additionalStorage.split("%")[0])

		print('  Additional Storage = ' + additionalStorage + " ", end="")
		print(createPercentBar("#", integerAdditionalStorage, 20))
		print("")


def createPercentBar(symbol, percent, length):
	roundedPercentage = round((percent/100) * length)
	
	count = 0

	output = '['
	for i in range(length):
		if count < roundedPercentage:
			output += symbol
			count += 1
		else:
			output += '.'
	output += ']'

	return output

def printUpdateData(updateData):

	if updateData != None:                
		print(" Update status:\n  " + updateData.split(' ')[0] + " packages to update")
		print("")
	else:
		print(" Update status:\n Failed to get update data")
		print("")


def printFoldingData(foldingData):
	print(" Folding Status:")
	print('  ' + foldingData)

def printLogFiles(sshConnection, logfileName, logfileLocation):
	from Functions import dataFunctions

	bashCommandToPrintLogfile = 'tail -1 ' + logfileLocation

	print(" " + logfileName + ":")
	try:
		print("  " + dataFunctions.commandSend(sshConnection, bashCommandToPrintLogfile))
	except:
		print(" Logfile parse failed")
	print("")

def displayOptions(currentScreen, size):
	options = [
		"s: Server Select", 
		"d: Dashboard",
		"o: Overview",
		"f: Folding Details", 
		"c: Send Command", 
		"n: New SSH Window",
		"q: Quit"
		
	]

	output = getScreenDivider("Options", size[1])
	limit = 3
	for i in range(len(options)):
		if currentScreen != options[i][0]:
			output = output + options[i]
			if options[i][0] != "q":
				output = output + " | "
		if i == 3:
			output = output + "\n"
	return output