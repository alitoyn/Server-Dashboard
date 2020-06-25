def userSelectServer():
	import config
	from Functions import displayFunctions
	from Functions import controlFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	print('Select which server to show details for:')

	displayFunctions.printServerList()

	allowedInputs = dataFunctions.getListOfServerIndicies()
	userInput = dataFunctions.checkInputAgainstList_int(allowedInputs)

	return userInput
