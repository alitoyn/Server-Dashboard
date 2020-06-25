from pexpect import pxssh       # used for ssh connection
import sys, time, os # other libraries

from Functions import controlFunctions
from Functions import controlFunctions
from Functions import foldingFunctions
from Functions import displayFunctions

from screens import foldingScreen as foldingScreenModule
from screens import dashboard
from screens import selectServer
from screens import sendCommandModule
from screens import newSshWindowModule
from screens import overviewModule

try:
    from config import *        # import all data from the config file
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)


foldingFunctions.dailyDownloadFoldingUserData(foldingUserID)

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
quitProgram = 'q'

# set default screen
selectedScreen = dashboardScreen

defaultServerToDisplay = 0
selectedServer = defaultServerToDisplay


while selectedScreen != quitProgram:

    skipDisplayOptions = False

    
    if selectedScreen == dashboardScreen:
            dashboard.displayDashboard(serverSshConnections[selectedServer], selectedServer)
        

    elif selectedScreen == serverSelectScreen:
        selectedServer = selectServer.userSelectServer()
        
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
        print(displayFunctions.createDisplayOptions(selectedScreen))
        userInput = controlFunctions.getUserInput()
    
        if userInput == '0':
            displayFunctions.launchProcessesView(serverSshConnections[selectedServer], selectedServer)
        else:
            selectedScreen = userInput

controlFunctions.logoutOfAllServers(serverSshConnections, server_name)




