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
	from Functions import controlFunctions

	if controlFunctions.checkServerIsLoggedIn(connectedServer):

		bashCommandForRootStorage = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
		rootStorage = commandSend(connectedServer, bashCommandForRootStorage)

	else:
		rootStorage = 'Server Not Logged In'

	return rootStorage

def getAdditionalStorage(additionalStorageLocation, connectedServer):
	from Functions import controlFunctions

	if additionalStorageLocation != None:

		if controlFunctions.checkServerIsLoggedIn(connectedServer):	

			bashCommandForAdditionalStorage = "df -h " + additionalStorageLocation + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
			additionalStorage = commandSend(connectedServer, bashCommandForAdditionalStorage)

		else:
			additionalStorage = 'Server not logged in'

	else:
		additionalStorage = None

	return additionalStorage


def getUpdateData(connectedServer):
	from Functions import controlFunctions

	bashGetUpdatesCommand = 'apt-get upgrade --dry-run | grep "newly install"'

	if controlFunctions.checkServerIsLoggedIn(connectedServer):
		try:
			updateData = commandSend(connectedServer, bashGetUpdatesCommand)
			output = updateData.split(' ')[0] + " packages to update\n"
		
		except:
			output = 'Failed to get update data'
	else:
		output = 'Server not logged in'

	return output

def printUpdateData(updateData):

	if updateData != None:                
		print("Update status:\n " + updateData.split(' ')[0] + " packages to update")
		print("")
	else:
		print("Update status:\n Failed to get update data")
		print("")


def getUptime(connectedServer):
	from Functions import controlFunctions
	
	bashCommandForUptime = 'uptime'

	if controlFunctions.checkServerIsLoggedIn(connectedServer):
		uptimeData = commandSend(connectedServer, bashCommandForUptime)
	else:
		uptimeData = ' Server not logged in'

	return uptimeData

def getTempInfo(connectedServer):
	from Functions import controlFunctions

	bashCommandForTempInfo = 'sensors | grep Package | xargs echo'
	if controlFunctions.checkServerIsLoggedIn(connectedServer):
		# The replace fixes the broken degree symbol
		tempInfo = commandSend(connectedServer, bashCommandForTempInfo).replace('\\xc2\\xb0', ' deg.')

		expectedStartOfResponse = 'P'

		if checkFirstLetterOfString(tempInfo, expectedStartOfResponse):
			output = ' ' + tempInfo + '\n'
		else:
			output = 'Please install dependancies to see temperature\n'
	else:
		output = ' Server not logged in'

	return output

def checkFirstLetterOfString(string, char):
	if string[0] == char:
		return True
	else:
		return False


def dataValWithQuestion(question, allowedInputs):
	import time
	check = 0
	length = len(allowedInputs)
	while(1):
		response = input(question)
		for i in range(length):
			if response == allowedInputs[i]:
				check = 1
				break
		if check == 0:
			print("\nPlease enter a valid input...\n")
			time.sleep(0.5)
		else:
			return response
			break

def checkInputAgainstList_int(allowedInputs):
	import time
	check = 0
	length = len(allowedInputs)
	while(1):
		response = input()
		try:
			response = int(response)
		except:
			pass

		for i in range(length):
			if response == allowedInputs[i]:
				check = 1
				break
		if check == 0:
			print("\nPlease enter a valid input...\n")
			time.sleep(0.5)
		else:
			return response
			break

def checkInputAgainstList_char(allowedInputs):
	import time
	check = 0
	length = len(allowedInputs)
	while(1):
		response = input()
		for i in range(length):
			if response == allowedInputs[i]:
				check = 1
				break
		if check == 0:
			print("\nPlease enter a valid input...\n")
			time.sleep(0.5)
		else:
			return response
			break

def getListOfServerIndicies():
	import config
	output = []
	for i in range(len(config.server_name)):
		output.append(i)
	return output

def getListOfIndicesFromList(inputList):
	outputList = []
	for i in range(len(inputList)):
		outputList.append(i)
	return outputList
