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

	print('Select overview again to reset view')


	#     # print temp overview
	#     if choice == "3":
	#         os.system('clear')
	#         print("Loading temp details...\n")
			
	#         for i in range(len(server_name)):
	#             print(server_name[i] + " :")

	#             tempInfo = z.commandSend(serverSshConnections[i], 'sensors | grep Package | xargs echo').replace('\\xc2\\xb0', ' deg.')
	#             if tempInfo[0] == 'P':
	#                 print(' Package temperature:')
	#                 print(' ' + tempInfo)
	#                 print("")
	#             else:
	#                 print(' Package temperature:')
	#                 print(' Please install dependancies to see temperature')
	#                 print("")

	#     # print the user options
	#     terminalSize = z.updateTermSize()
	#     print(z.displayOptions(selectedScreen, terminalSize))

	#     print("\nInput 'r' to reset and choose another overview")

	#     # break from loop if user selects an option
	#     # this will loop for 60 seconds before repeating the loop
	#     while 1:
	#        time.sleep(0.5)
	#        if selectedScreen != "o" or selectedScreen == "r":
	#             if selectedScreen == "r":
	#                 selectedScreen = "o"
	#             break

	
def printOverviewOptions(overviewOptions):
	print("Select which option to show details for:\n")
	for i in range(len(overviewOptions)):
		print(str(i) + ':' + overviewOptions[i])

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
