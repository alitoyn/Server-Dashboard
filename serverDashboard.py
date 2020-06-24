from pexpect import pxssh       # used for ssh connection
import functions as z        # import all functions written for this program
import sys, time, os, threading, getch # other libraries

from Functions import controlFunctions
from Functions import controlFunctions
from Functions import foldingFunctions
from Functions import displayFunctions

from screens import foldingScreen as foldingScreenModule
from screens import dashboard
from screens import selectServer
from screens import sendCommandModule
from screens import newSshWindowModule

try:
    from config import *        # import all data from the config file
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)


foldingFunctions.dailyDownloadFoldingUserData(foldingUserID)

# if the folding screen works then this can be deleted!
# foldingData = foldingFunctions.foldingXmlParse()


serverSshConnections = controlFunctions.connectToServers()


defaultTerminalRows = 24
defaultTerminalColumns = 80
terminalSize = [defaultTerminalRows, defaultTerminalColumns]


serverSelectScreen = 's'
dashboardScreen = 'd'
foldingScreen = 'f'
sendCommandScreen = 'c'
newSshWindowScreen = 'n'
quitProgram = 'q'


# set default screen
selectedScreen = dashboardScreen

defaultServerToDisplay = 0
selectedServer = defaultServerToDisplay


while selectedScreen != quitProgram:

    skipDisplayOptions = False

    # can probably remove this after the refactor
    terminalSize = displayFunctions.updateTermSize()

    
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
    
    # NOTE WHILE REFACTORING
    # This needs to go at the bottom
    if not skipDisplayOptions:
        print(displayFunctions.createDisplayOptions(selectedScreen))
        userInput = controlFunctions.getUserInput()
    
        if userInput == '0':
            displayFunctions.launchProcessesView(serverSshConnections[selectedServer], selectedServer)
        else:
            selectedScreen = userInput


    

    

    # if selectedScreen == 'o':
    #     # display info
    #     os.system('clear')
    #     print("Select which option to show details for:\n")
    #     print("0: updates")
    #     print("1: storage")
    #     print("2: uptime")
    #     print("3: CPU temps")

    #     while selectedScreen == "o":
    #         for i in range(0, 120):
    #             time.sleep(0.5)
    #             if selectedScreen != "o":
    #                 break
        
    #     choice = selectedScreen
    #     selectedScreen = 'o'

    #     # print update overview
    #     if choice == "0":
    #         os.system('clear')
    #         print("Loading update details...\n")
            
    #         for i in range(len(server_name)):
    #             print(server_name[i] + " :")
                
    #             #get update data
    #             try:
    #                 updates = z.commandSend(serverSshConnections[i], 'apt-get upgrade --dry-run | grep "newly install"')
    #                 update_flag = 1
    #             except:
    #                 updates = "Failed to get data"
    #                 update_flag = 0 

    #              # try to print availble updates
    #             if update_flag == 1:                
    #                 print(" " + updates.split(' ')[0] + " packages to update")
    #                 print("")
    #             else:
    #                 print(updates)
    #                 print("")

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

    

    

# logout of all servers
print("Exiting...")
for i in range(len(server_name)):
    serverSshConnections[i].logout()








# function that registers keyboard press in the background
# doesn't like being in the functions file
# TODO find way to work without this or move it to another file
# def interrupt():
#     global selectedScreen
#     while selectedScreen != "q":
#         keystrk = input()
#         # thread doesn't continue until key is pressed
#         selectedScreen = keystrk
#         if keystrk == "q":
#             print("Exiting...")


# # start the interrupt thread
# inter = threading.Thread(target=interrupt)
# inter.start()

