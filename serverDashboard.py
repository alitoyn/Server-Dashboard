from Functions import controlFunctions
from Functions import dataFunctions
from Functions import foldingFunctions
from Functions import displayFunctions

from screens import foldingScreenModule
from screens import dashboardModule
from screens import selectServerModule
from screens import sendCommandModule
from screens import newSshWindowModule
from screens import overviewModule

if controlFunctions.checkFileExists('config.py'):
    print("Config file found...")
    import config
else:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    controlFunctions.exitProgram()

controlFunctions.appUpdater()

foldingFunctions.dailyDownloadFoldingUserData(config.foldingUserID)

serverSshConnections = controlFunctions.connectToServers()

defaultTerminalRows = 24
defaultTerminalColumns = 80
terminalSize = [defaultTerminalRows, defaultTerminalColumns]

serverSelectScreen = 's'
dashboardScreen = 'd'
foldingScreen = 'f'
sendCommandScreen = 'c'
newSshWindowScreen = 'n'
overviewScreen = 'o'
launchProcesses = '0'
quitProgram = 'q'

listOfScreens = [serverSelectScreen, dashboardScreen, foldingScreen, 
                 sendCommandScreen, newSshWindowScreen, overviewScreen,
                  launchProcesses, quitProgram ]

# set default screen
selectedScreen = dashboardScreen

defaultServerToDisplay = 0
selectedServer = defaultServerToDisplay


while selectedScreen != quitProgram:

    skipDisplayOptions = False
   
    if selectedScreen == dashboardScreen:
            if controlFunctions.checkServerIsLoggedIn(serverSshConnections[selectedServer]):
                dashboardModule.displayDashboard(serverSshConnections[selectedServer], selectedServer)
            else:
                displayFunctions.printServerNotLoggedIn(selectedServer)
        
    elif selectedScreen == serverSelectScreen:
        selectedServer = selectServerModule.userSelectServer()
        
        selectedScreen = dashboardScreen
        skipDisplayOptions = True

    elif selectedScreen == foldingScreen:
        foldingScreenModule.displayFoldingScreen(serverSshConnections)

    elif selectedScreen == sendCommandScreen:
        sendCommandModule.getCommandAndSend()

        selectedScreen = dashboardScreen
        skipDisplayOptions = True

    elif selectedScreen == newSshWindowScreen:
        newSshWindowModule.newSshWindow()

        selectedScreen = dashboardScreen
        skipDisplayOptions = True

    elif selectedScreen == overviewScreen:
        overviewModule.overview(serverSshConnections)

    if not skipDisplayOptions:
        print(controlFunctions.createDisplayOptions(selectedScreen))
        
        userInput = dataFunctions.checkInputAgainstList_char(listOfScreens)
    
        if userInput == '0':
            controlFunctions.launchProcessesView(serverSshConnections[selectedServer], selectedServer)
        else:
            selectedScreen = userInput

controlFunctions.logoutOfAllServers(serverSshConnections)

