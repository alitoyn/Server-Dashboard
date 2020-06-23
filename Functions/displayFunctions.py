def updateTermSize():
	import os
	
	defaultRows = 24
	defualtColumns = 80

	try:
		rows, columns = os.popen('stty size', 'r').read().split()
		return [int(rows), int(columns)]

	except:
		return [defaultRows, defualtColumns]

	

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

def createDisplayOptions(currentScreen):
	terminalSize = updateTermSize()

	screenOptions = [
		"s: Server Select", 
		"d: Dashboard",
		"o: Overview",
		"f: Folding Details", 
		"c: Send Command", 
		"n: New SSH Window",
		"q: Quit"	
	]

	output = getScreenDivider("Options", terminalSize[1])
	limitPerRow = 3
	numberOfScreenOptions = len(screenOptions)
	count = 0

	for i in range(numberOfScreenOptions):

		if currentScreen != screenOptions[i][0]:
			output = output + screenOptions[i]
			
			# if the option is not the last one,
			# then add the deliminator
			if screenOptions[i][0] != "q":
				output = output + " | "
		
		if count == limitPerRow:
			output = output + "\n"
			count == -1

		count += 1
	return output

def getScreenDivider(text, size):
	output = text + " "

	for i in range(size - len(text) - 1):
		output = output + "-"
	output = output + "\n"
	return output

def launchProcessesView(connectedServer, selectedServer):
	import config, os
	from Functions import dataFunctions

	bashCommandForProcessess = 'htop'

	fullBashCommand = config.default_terminal + ' --command "ssh -i ' + config.server_key[selectedServer] + ' -p ' + config.server_port[selectedServer] + ' -t ' + config.server_user[selectedServer] + '@' + config.server_ip[selectedServer] + ' ' + bashCommandForProcessess + '"'

	os.system(fullBashCommand)

