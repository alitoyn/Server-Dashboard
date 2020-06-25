def displayFoldingScreen(listOfSshConnections):
	import config
	from Functions import displayFunctions
	from Functions import foldingFunctions
	from Functions import controlFunctions

	foldingData = foldingFunctions.foldingXmlParse()

	terminalSize = controlFunctions.updateTermSize()
	columnsIndex = 1

	displayFunctions.clearTerminal()

	userInfoBanner = displayFunctions.getScreenDivider('User Info', terminalSize[columnsIndex])
	print(userInfoBanner)

	printFoldingUsername(foldingData)
	print('')
	printFoldingRankChange(foldingData)
	print('')
	printFoldingPointsToday(foldingData)
	print('')
	printFoldingPointsInTheLast24Hrs(foldingData)
	printFoldingPointsAverage24Hrs(foldingData)
	print('')

	serverInfoBanner = displayFunctions.getScreenDivider('Server Info', terminalSize[columnsIndex])
	print(serverInfoBanner)

	printAllServerFoldingInfo(config.server_name, listOfSshConnections)


def printFoldingUsername(foldingData):
	print("User Name: ", foldingData.User_Name.get_text())

def printFoldingRankChange(foldingData):
	print("Rank Change (24hrs):", foldingData.user.Change_Rank_24hr.get_text())

def printFoldingPointsToday(foldingData):
	print("Points Today:", foldingData.user.Points_Today.get_text())

def printFoldingPointsInTheLast24Hrs(foldingData):
	print("Points Last 24hrs:", foldingData.user.Points_Last_24hr.get_text())

def printFoldingPointsAverage24Hrs(foldingData):
	print("Points 24hrs Average:", foldingData.user.Points_24hr_Avg.get_text())

def printAllServerFoldingInfo(serverNameList, listOfSshConnections):
	from Functions import foldingFunctions

	numberOfServers = len(serverNameList)

	for i in range(numberOfServers):		
		print(serverNameList[i] + ':')

		serverFoldingData = foldingFunctions.getFoldingLogData(listOfSshConnections[i])
		print(serverFoldingData)
