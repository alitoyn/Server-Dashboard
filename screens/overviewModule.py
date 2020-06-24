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

	print('Select overview again to reset view')


	

	#     # print uptime overview
	#     if choice == "2":
	#         os.system('clear')
	#         print("Loading uptime details...\n")
			
	#         for i in range(len(server_name)):
	#             print(server_name[i] + " :")

	#             print(z.commandSend(server[i], 'uptime'))
	#             print("")

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





	#     # print storage overview
	#     if choice == "1":
	#         os.system('clear')
	#         print("Loading storage details...\n")
			
	#         for i in range(len(server_name)):
	#             print(server_name[i] + " :")

	#             cmd = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
	#             storage = z.commandSend(server[i], cmd)
	#             try:
	#                 storage2 = z.commandSend(server[i], "df -h " + additional_storage[i] + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'")
	#                 add_stor_flag = 1
	#             except:
	#                 add_stor_flag = 0
				
	#             print(' Root Directory / = ' + storage + " ", end="")                                 
	#             z.percentBar("#", int(storage.split("%")[0]), 20)
	#             print("")

	#             # try to print additional storage if it has been input otherwise pass over
	#             if add_stor_flag == 1:
	#                 print(' Additional Storage = ' + storage2 + " ", end="")
	#                 z.percentBar("#", int(storage2.split("%")[0]), 20)
	#                 print("")