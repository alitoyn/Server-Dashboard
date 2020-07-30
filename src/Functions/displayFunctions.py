def clearTerminal():
	import os

	bashCommandToClearScreen = 'clear'

	os.system(bashCommandToClearScreen)

def printStorageData(rootStorage, additionalStorage):
	try:
		integerRootStorage = int(rootStorage.split("%")[0])

		print(' Root Directory / = ' + rootStorage + " ", end="")                                 
		print(createPercentBar("#", integerRootStorage, 20))

		if additionalStorage:
			integerAdditionalStorage = int(additionalStorage.split("%")[0])

			print(' Additional Storage = ' + additionalStorage + " ", end="")
			print(createPercentBar("#", integerAdditionalStorage, 20))
		print("")

	except:
		print(' Server not logged in\n')

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


def getScreenDivider(text, size):
	output = text + " "

	for i in range(size - len(text) - 1):
		output = output + "-"
	output = output + "\n"
	return output


def printServerList():
	from config import server_name

	numberOfServers = len(server_name)

	for i in range(numberOfServers):
		print(str(i) + ": " + server_name[i])
	print("\nSelection: ", end='')

def printServerNotLoggedIn(serverIndex):
	import config

	clearTerminal()

	print(config.server_name[serverIndex] + ' is not loged in.')
	print('Please restart program to try again or select another server\n')
