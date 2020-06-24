# takes the ssh server connection and a command and returns the result
def commandSend(connectedServer, command):

	connectedServer.sendline(command)
	connectedServer.prompt()
	
	return sshParse(str(connectedServer.before))


def sshParse(string):

	unwantedData = '\\r\\n'
	
	cleanedString = string[string.find(unwantedData)+len(unwantedData):string.rfind(unwantedData)]
	
	return cleanedString



def getRootStorage(connectedServer):

	bashCommandForRootStorage = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
	rootStorage = commandSend(connectedServer, bashCommandForRootStorage)

	return rootStorage

def getAdditionalStorage(additionalStorageLocation, connectedServer):

	if additionalStorageLocation != None:

		bashCommandForAdditionalStorage = "df -h " + additionalStorageLocation + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
		additionalStorage = commandSend(connectedServer, bashCommandForAdditionalStorage)

	else:
		additionalStorage = None

	return additionalStorage


def getUpdateData(connectedServer):
	bashGetUpdatesCommand = 'apt-get upgrade --dry-run | grep "newly install"'

	try:
		updateData = commandSend(connectedServer, bashGetUpdatesCommand)
	except:
		updateData = None

	return updateData


def getUptime(connectedServer):

	bashCommandForUptime = 'uptime'

	uptimeData = commandSend(connectedServer, bashCommandForUptime)

	return uptimeData

def getTempInfo(connectedServer):
	
	bashCommandForTempInfo = 'sensors | grep Package | xargs echo'

	# The replace fixes the broken degree symbol
	tempInfo = commandSend(connectedServer, bashCommandForTempInfo).replace('\\xc2\\xb0', ' deg.')

	expectedStartOfResponse = 'P'

	if checkFirstLetterOfString(tempInfo, expectedStartOfResponse):
		output = 'Package temperature:\n  '
		output += tempInfo
		output += '\n'
	else:
		output = 'Package temperature:\n '
		output += 'Please install dependancies to see temperature\n'

	return output

def checkFirstLetterOfString(string, char):
	if string[0] == char:
		return True
	else:
		return False

def getNumberOfLogFiles(logFileArray):
	arrayInitialisedTo = 0

	numberOfLogFiles = 0

	for i in range(len(logFileArray)):
		if logFileArray[i] == 0:
			break
		else:
			numberOfLogFiles += 1

	return numberOfLogFiles
