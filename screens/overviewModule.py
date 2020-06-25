def overview(listOfSshConnections):
	from Functions import displayFunctions
	from Functions import controlFunctions

	displayFunctions.clearTerminal()

	overviewOptions = [
		'updates',
		'storage',
		'uptime',
		'CPU temps'
	]

	printOverviewOptions(overviewOptions)

	chosenOverviewIndex = int(controlFunctions.getUserInput())

	displayFunctions.clearTerminal()

	if chosenOverviewIndex == 0:
		printUpdateOverview(listOfSshConnections)
	elif chosenOverviewIndex == 1:
		printStorageOverview(listOfSshConnections)
	elif chosenOverviewIndex == 2:
		printUptimeOverview(listOfSshConnections)
	elif chosenOverviewIndex == 3:
		printTempOverview(listOfSshConnections)

	print('Select overview again to reset view')


def printOverviewOptions(overviewOptions):
	print("Select which option to show details for:\n")
	for i in range(len(overviewOptions)):
		print(str(i) + ': ' + overviewOptions[i])

def printUpdateOverview(listOfSshConnections):
	import config
	from Functions import displayFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	print("Loading update details...\n")

	for i in range(len(config.server_name)):
		print(config.server_name[i] + ':')
		try:
			updates = dataFunctions.getUpdateData(listOfSshConnections[i])
			updates = " " + updates.split(' ')[0] + " packages to update"

		except:
			updates = "Failed to get data"

		print(updates)
		print("")


def printStorageOverview(listOfSshConnections):
	import config
	from Functions import displayFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	print("Loading storage details...\n")

	for i in range(len(config.server_name)):
		
		rootStorage = dataFunctions.getRootStorage(listOfSshConnections[i])
		additionalStorage = dataFunctions.getAdditionalStorage(config.additional_storage[i], listOfSshConnections[i])

		print(config.server_name[i] + ':')
		displayFunctions.printStorageData(rootStorage, additionalStorage)



def printUptimeOverview(listOfSshConnections):
	import config
	from Functions import displayFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	print("Loading uptime details...\n")

	for i in range(len(config.server_name)):
		
		print(config.server_name[i] + ':')
		serverUptime = dataFunctions.getUptime(listOfSshConnections[i])
		print(serverUptime + '\n')

def printTempOverview(listOfSshConnections):
	import config
	from Functions import displayFunctions
	from Functions import dataFunctions

	displayFunctions.clearTerminal()

	print("Loading CPU temperature details...\n")

	for i in range(len(config.server_name)):
		
		print(config.server_name[i] + ':')
		serverTempInfo = dataFunctions.getTempInfo(listOfSshConnections[i])
		print(serverTempInfo)