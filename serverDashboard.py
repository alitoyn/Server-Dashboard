from pexpect import pxssh       # used for ssh connection
import functions as z        # import all functions written for this program
from Functions import setupFunctions, foldingFunctions, displayFunctions
import sys, time, os, threading, getch # other libraries


# Attempt to import server data from file if it exists
# TODO there must be a way to turn this into a function?
try:
    from config import *        # import all data from the config file
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)


foldingFunctions.dailyDownloadFoldingUserData(foldingUserID)
foldingData = foldingFunctions.foldingXmlParse()


serverSshConnections = setupFunctions.connectToServers()


# set the defualt landing page as the dashboard
screenToDisplay = "d"

# function that registers keyboard press in the background
# doesn't like being in the functions file
# TODO find way to work without this or move it to another file
def interrupt():
    global screenToDisplay
    while screenToDisplay != "q":
        keystrk = input()
        # thread doesn't continue until key is pressed
        screenToDisplay = keystrk
        if keystrk == "q":
            print("Exiting...")


# start the interrupt thread
inter = threading.Thread(target=interrupt)
inter.start()


# set the default rows, columns for terminal
terminalSize = [24, 80] # rows, columns


defaultServerToDisplay = 0
selectedServer = defaultServerToDisplay

serverSelectScreen = 's'
dashboardScreen = 'd'
foldingScreen = 'f'
sendCommandScreen = 's'
newSshWindowScreen = 'n'
quitProgram = 'q'


while screenToDisplay != quitProgram:

    terminalSize = displayFunctions.updateTermSize()

    
    if screenToDisplay == dashboardScreen:
        displayFunctions.displayDashboard(serverSshConnections[selectedServer], selectedServer)

        terminalSize = displayFunctions.updateTermSize()            
        print(' Select "0" to view processess and CPU load\n')
        print(z.displayOptions(screenToDisplay, terminalSize))


        
        # break from loop if user selects an option
        # this will loop for 60 seconds before repeating the loop
        for i in range(0, 120):
            time.sleep(0.5)
            if screenToDisplay == '0':
                passedCommand = 'htop'
                cmd = default_terminal + ' --command "ssh -i ' + server_key[selectedServer] + ' -p ' + server_port[selectedServer] + ' -t ' + server_user[selectedServer] + '@' + server_ip[selectedServer] + ' ' + passedCommand + '"'
                os.system(cmd)
                screenToDisplay = 'd'

            if screenToDisplay != "d":
                break


    # server select page
    if screenToDisplay == "s":
        # change the screenToDisplay to allow the user to choose new one
        # display info
        os.system('clear')
        print("Select which server to show details for:")
        for i in range(len(server_name)):
            print(str(i) + ": " + server_name[i])
        # print("\nSelection: ", end='')

        while screenToDisplay == "s":
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "s":
                    break
        
        selectedServer = int(screenToDisplay)
        # go back to main screen
        screenToDisplay = "d"

    # folding page                
    if screenToDisplay == "f":

        while screenToDisplay == "f":
            terminalSize = z.updateTermSize()
            os.system('clear')
            print(z.getScreenDivider("User Info", terminalSize[1]))
            print("User Name: ", foldingData.User_Name.get_text())
            print("Rank Change (24hrs):", foldingData.user.Change_Rank_24hr.get_text())
            print("")
            print("Points Today:", foldingData.user.Points_Today.get_text())
            print("")
            print("Points Last 24hrs:", foldingData.user.Points_Last_24hr.get_text())
            print("Points 24hrs Average:", foldingData.user.Points_24hr_Avg.get_text())
            print("")
            print(z.getScreenDivider("Server Info", terminalSize[1]))
            for i in range (len(server_name)):
                print(server_name[i] + " :")
                
                try:
                    foldingLog = z.foldingParse(z.commandSend(serverSshConnections[i], 'tail -1 /var/lib/fahclient/log.txt'))
                    print(" " + foldingLog + " ", end='')

                    try:
                        # the funky code here pulls out the percent from the log file line
                        z.percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
                    except:
                        print("")
                    print("")
                except:
                    print(" Log file parse failed")
                    print("")

            # print the user options
            print(z.displayOptions(screenToDisplay, terminalSize))
            
            # break from loop if user selects an option
            # this will loop for 60 seconds before repeating the loop
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "f":
                    break

    # send command page
    if screenToDisplay == "c":
        # display info
        os.system('clear')
        print("\nThis is currently for show and does nothing\n")
        print("Which server do you want to send a command:")
        for i in range(len(server_name)):
            print(str(i) + ": " + server_name[i])
        print("")

        while screenToDisplay == "c":
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "c":
                    break
        
        serverToSendCommand = int(screenToDisplay)
        screenToDisplay = "c"

        print("\nChoose command to send to " + server_name[serverToSendCommand])
        print("0: Shutdown")
        print("1: Reboot")
        print("2: Run Updates")
        print("3: Install Dependancies")
        print("")
        while screenToDisplay == "c":
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "c":
                    break

        commandToSendServer = int(screenToDisplay)
        passedCommand_2 = 0
        screenToDisplay = "c"

        # set command
        if(commandToSendServer == 0):
            passedCommand = 'sudo shutdown'
        if(commandToSendServer == 1):
            passedCommand = 'sudo reboot'
        if(commandToSendServer == 2):     
            passedCommand = 'sudo apt upgrade && sleep 1'
        if (commandToSendServer == 3):

            # These are the programs to install
            # need to be seperated by spaces
            programsToInstall = 'lm-sensors'

            # These are any additional commands that need to be run
            # need to be seperated by ';'
            commandsToRun = 'sudo sensors-detect'

            # This is the command sent to the server
            # Only change this if the UI of the install needs updating, otherwise use the above two options!
            passedCommand = "'sudo apt install " + programsToInstall + "; echo ''; echo 'Press ENTER for all default options, any others are used at your own risk...'; echo ''; sleep 2; " + commandsToRun + "; echo ''; echo 'installation successfull! Window closing...'; sleep 2 '"

        
        # initiate command   
        print("Opening new window...")
        cmd = default_terminal + ' --command "ssh -t -i ' + server_key[serverToSendCommand] + ' -p ' + server_port[serverToSendCommand] + ' -t ' + server_user[serverToSendCommand] + '@' + server_ip[serverToSendCommand] + ' ' + passedCommand + '"'
        output = os.system(cmd)
        time.sleep(1)

        # if passedCommand_2 != 0:
        #     cmd = default_terminal + ' --command "ssh -i ' + server_key[serverToSendCommand] + ' -p ' + server_port[serverToSendCommand] + ' -t ' + server_user[serverToSendCommand] + '@' + server_ip[serverToSendCommand] + ' ' + passedCommand_2 + '"'
        #     output = os.system(cmd)
        #     time.sleep(1)

        screenToDisplay = "d"

    if screenToDisplay == 'o':
        # display info
        os.system('clear')
        print("Select which option to show details for:\n")
        print("0: updates")
        print("1: storage")
        print("2: uptime")
        print("3: CPU temps")

        while screenToDisplay == "o":
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "o":
                    break
        
        choice = screenToDisplay
        screenToDisplay = 'o'

        # print update overview
        if choice == "0":
            os.system('clear')
            print("Loading update details...\n")
            
            for i in range(len(server_name)):
                print(server_name[i] + " :")
                
                #get update data
                try:
                    updates = z.commandSend(serverSshConnections[i], 'apt-get upgrade --dry-run | grep "newly install"')
                    update_flag = 1
                except:
                    updates = "Failed to get data"
                    update_flag = 0 

                 # try to print availble updates
                if update_flag == 1:                
                    print(" " + updates.split(' ')[0] + " packages to update")
                    print("")
                else:
                    print(updates)
                    print("")

        # print storage overview
        if choice == "1":
            os.system('clear')
            print("Loading storage details...\n")
            
            for i in range(len(server_name)):
                print(server_name[i] + " :")

                cmd = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
                storage = z.commandSend(server[i], cmd)
                try:
                    storage2 = z.commandSend(server[i], "df -h " + additional_storage[i] + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'")
                    add_stor_flag = 1
                except:
                    add_stor_flag = 0
                
                print(' Root Directory / = ' + storage + " ", end="")                                 
                z.percentBar("#", int(storage.split("%")[0]), 20)
                print("")

                # try to print additional storage if it has been input otherwise pass over
                if add_stor_flag == 1:
                    print(' Additional Storage = ' + storage2 + " ", end="")
                    z.percentBar("#", int(storage2.split("%")[0]), 20)
                    print("")

        # print uptime overview
        if choice == "2":
            os.system('clear')
            print("Loading uptime details...\n")
            
            for i in range(len(server_name)):
                print(server_name[i] + " :")

                print(z.commandSend(server[i], 'uptime'))
                print("")

        # print temp overview
        if choice == "3":
            os.system('clear')
            print("Loading temp details...\n")
            
            for i in range(len(server_name)):
                print(server_name[i] + " :")

                tempInfo = z.commandSend(serverSshConnections[i], 'sensors | grep Package | xargs echo').replace('\\xc2\\xb0', ' deg.')
                if tempInfo[0] == 'P':
                    print(' Package temperature:')
                    print(' ' + tempInfo)
                    print("")
                else:
                    print(' Package temperature:')
                    print(' Please install dependancies to see temperature')
                    print("")

        # print the user options
        terminalSize = z.updateTermSize()
        print(z.displayOptions(screenToDisplay, terminalSize))

        print("\nInput 'r' to reset and choose another overview")

        # break from loop if user selects an option
        # this will loop for 60 seconds before repeating the loop
        while 1:
           time.sleep(0.5)
           if screenToDisplay != "o" or screenToDisplay == "r":
                if screenToDisplay == "r":
                    screenToDisplay = "o"
                break

    # new ssh window page
    if screenToDisplay == "n":
        # change the screenToDisplay to allow the user to choose new one

        # display info
        os.system('clear')
        print("Which server would you like to open a conneciton with:")
        for i in range(len(server_name)):
            print(str(i) + ": " + server_name[i])

        while screenToDisplay == "n":
            for i in range(0, 120):
                time.sleep(0.5)
                if screenToDisplay != "n":
                    break

        selectedServer = int(screenToDisplay)

        print("Opening new window...")
        cmd = default_terminal + ' --command "ssh -i ' + server_key[selectedServer] + ' -p ' + server_port[selectedServer] + ' ' + server_user[selectedServer] + '@' + server_ip[selectedServer] + '"'
        os.system(cmd)

        # go back to main screen
        screenToDisplay = "d"

# logout of all servers
for i in range(len(server_name)):
    serverSshConnections[i].logout()

