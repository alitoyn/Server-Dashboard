def userSelectServer():
	import config
	from Functions import displayFunctions
	from Functions import controlFunctions

	displayFunctions.clearTerminal()

	print('Select which server to show details for:')

	displayFunctions.printServerList(config.server_name)

	while 1:

		userInput = controlFunctions.getUserInput()
		try:
			userInput = int(userInput)
		except:
			pass

		wasUserInputValid = dataValidationServerSelection(userInput, config.server_name)

		if wasUserInputValid:
			break
		else:
			print('Please enter a valid input')

	return userInput


def dataValidationServerSelection(userInput, listOfServerNames):

	numberOfServers = len(listOfServerNames)

	check = False

	for i in range(numberOfServers):
		if i == userInput:
			check = True
			break

	return check
