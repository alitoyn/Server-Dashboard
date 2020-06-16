# TO DO - consider looking at pulseway for further ideas

# - password protect application?

# folding additions:
#   - predict how long is left?

from pexpect import pxssh       # used for ssh connection
import functions as z        # import all functions written for this program
import sys, time, os, threading, getch # other libraries

# get config info ----------------------------------------------------------------------------------------------------------

# Attempt to import server data from file if it exists
try:
    from config import *        #import all data from the config file
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)

# get the most up to date folding data for the user
z.getFoldingData(foldingUserID)
fData = z.foldingXmlParse()


# connect via ssh ----------------------------------------------------------------------------------------------------------

# connect to all servers
numberOfServers = len(server_name)

server = {} # this list holds the ssh connections

print("\nConnect to servers...")
for i in range(numberOfServers):
    server[i] = pxssh.pxssh() # connect to server 'server[0]'

    try:
        e = server[i].login (server_ip[i], server_user[i], ssh_key=server_key[i], quiet=True, port=server_port[i])
        print(server_name[i] + " connected. (" + str(i + 1) + "/" + str(numberOfServers) + ")")  
    except pxssh.ExceptionPxssh as e:
        print ("SSH session for " + server_name[i] + " failed on login.")
        print (str(server[i]))
        # sys.exit() # exit program for failed ssh attempt

print ("\nSSH session login successful")

# create interrupt thread --------------------------------------------------------------------------------------------------
# needed for the interrupt thread

# set the defualt landing page as the dashboard
userInput = "d"

# function that registers keyboard press in the background
# doesn't like being in the functions file
def interrupt():
    global userInput
    while userInput != "q":
        keystrk = input()
        # thread doesn't continue until key is pressed
        userInput = keystrk
        if keystrk == "q":
            print("Exiting...")

# display region ------------------------------------------------------------------------------------------------------

# start the interrupt thread
inter = threading.Thread(target=interrupt)
inter.start()

# set the default rows, columns for terminal
termSize = [24, 80] # rows, columns

# this is the server shown by default
# can be changed by the "Server Select" screen
serverSelect = 0

while userInput != "q":
    # update current rows and columns of the terminal 
    # rows, columns = os.popen('stty size', 'r').read().split()
    termSize = z.updateTermSize()

    # main page
    if userInput == "d":
        # prompt the user that something is happening
        print("\nLoading...\n")

        # pull data that doesn't need to be constantly updated
        # get storage data
        cmd = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
        storage = z.commandSend(server[serverSelect], cmd) #"df -h / | awk 'FNR == 2 {print $5 $2}'"
        try:
            storage2 = z.commandSend(server[serverSelect], "df -h " + additional_storage[serverSelect] + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'")
            add_stor_flag = 1
        except:
            add_stor_flag = 0

        #get update data
        try:
            updates = z.commandSend(server[serverSelect], 'apt-get upgrade --dry-run | grep "newly install"')
            update_flag = 1
        except:
            updates = "Failed to get data"
            update_flag = 0       

        # clear terminal screen and start to display data
        while userInput == "d":
            # clear the screen
            os.system('clear')
            
            # server name and uptime
            print('Server Information: ' + server_name[serverSelect])
            print(z.commandSend(server[serverSelect], 'uptime'))
            print("")

            # Try to print temperature information
            # NEED TO FIX THIS!!! - strip the output between \x's and replace with degrees sign!
            tempInfo = z.commandSend(server[serverSelect], 'sensors | grep Package | xargs echo').replace('\\xc2\\xb0', ' deg.')
            if tempInfo[0] == 'P':
                print(' Package temperature:')
                print(' ' + tempInfo)
                print("")
            else:
                print(' Package temperature:')
                print(' Please install dependancies to see temperature')
                print("")
            
            # storage data
            print(" Storage:")
            print(' Root Directory / = ' + storage + " ", end="")                                 
            z.percentBar("#", int(storage.split("%")[0]), 20)
            print("")

            # try to print additional storage if it has been input otherwise pass over
            if add_stor_flag == 1:
                print(' Additional Storage = ' + storage2 + " ", end="")
                z.percentBar("#", int(storage2.split("%")[0]), 20)
                print("")

            # try to print availble updates
            if update_flag == 1:                
                print(" Update status:\n " + updates.split(' ')[0] + " packages to update")
                print("")
            else:
                print(" Update status:\n " + updates)
                print("")
            
            # print folding data - last line of the log file
            print(" Folding Status:")
            # pull last line from folding log file and save it as variable
            try:
                foldingLog = z.foldingParse(z.commandSend(server[serverSelect], 'tail -1 /var/lib/fahclient/log.txt'))
                print(" " + foldingLog + " ", end='')

                try:
                    # the funky code here pulls out the percent from the log file line
                    z.percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
                except:
                    print("")
            except:
                print(" Log file parse failed")
            print("")

            # try to print data from the additional log file
            for i in range(len(extra_logfile_name[serverSelect])):
                if extra_logfile_name[serverSelect][i] == 0:
                    break
                try:
                    print(" " + extra_logfile_name[serverSelect][i] + ":")
                    print(" " + z.commandSend(server[serverSelect], 'tail -1 ' + extra_logfile_location[serverSelect][i] ))
                    print("")
                except:
                    pass

            # print the user options at the bottom
            termSize = z.updateTermSize()            
            print('\n Select "0" to view processess and CPU load\n')
            print(z.displayOptions(userInput, termSize))


            
            # break from loop if user selects an option
            # this will loop for 60 seconds before repeating the loop
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput == '0':
                    passedCommand = 'htop'
                    cmd = default_terminal + ' --command "ssh -i ' + server_key[serverSelect] + ' -p ' + server_port[serverSelect] + ' -t ' + server_user[serverSelect] + '@' + server_ip[serverSelect] + ' ' + passedCommand + '"'
                    os.system(cmd)
                    userInput = 'd'

                if userInput != "d":
                    break

    # server select page
    if userInput == "s":
        # change the userinput to allow the user to choose new one
        # display info
        os.system('clear')
        print("Select which server to show details for:")
        for i in range(numberOfServers):
            print(str(i) + ": " + server_name[i])
        # print("\nSelection: ", end='')

        while userInput == "s":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "s":
                    break
        
        serverSelect = int(userInput)
        # go back to main screen
        userInput = "d"

    # folding page                
    if userInput == "f":

        while userInput == "f":
            termSize = z.updateTermSize()
            os.system('clear')
            print(z.getScreenDivider("User Info", termSize[1]))
            print("User Name: ", fData.User_Name.get_text())
            print("Rank Change (24hrs):", fData.user.Change_Rank_24hr.get_text())
            print("")
            print("Points Today:", fData.user.Points_Today.get_text())
            print("")
            print("Points Last 24hrs:", fData.user.Points_Last_24hr.get_text())
            print("Points 24hrs Average:", fData.user.Points_24hr_Avg.get_text())
            print("")
            print(z.getScreenDivider("Server Info", termSize[1]))
            for i in range (numberOfServers):
                print(server_name[i] + " :")
                
                try:
                    foldingLog = z.foldingParse(z.commandSend(server[i], 'tail -1 /var/lib/fahclient/log.txt'))
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
            print(z.displayOptions(userInput, termSize))
            
            # break from loop if user selects an option
            # this will loop for 60 seconds before repeating the loop
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "f":
                    break

    # send command page
    if userInput == "c":
        # display info
        os.system('clear')
        print("\nThis is currently for show and does nothing\n")
        print("Which server do you want to send a command:")
        for i in range(numberOfServers):
            print(str(i) + ": " + server_name[i])
        print("")

        while userInput == "c":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "c":
                    break
        
        serverToSendCommand = int(userInput)
        userInput = "c"

        print("\nChoose command to send to " + server_name[serverToSendCommand])
        print("0: Shutdown")
        print("1: Reboot")
        print("2: Run Updates")
        print("3: Install Dependancies")
        print("")
        while userInput == "c":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "c":
                    break

        commandToSendServer = int(userInput)
        passedCommand_2 = 0
        userInput = "c"

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

        userInput = "d"

    if userInput == 'o':
        # display info
        os.system('clear')
        print("Select which option to show details for:\n")
        print("0: updates")
        print("1: storage")
        print("2: uptime")
        print("3: CPU temps")

        while userInput == "o":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "o":
                    break
        
        choice = userInput
        userInput = 'o'

        # print update overview
        if choice == "0":
            os.system('clear')
            print("Loading update details...\n")
            
            for i in range(numberOfServers):
                print(server_name[i] + " :")
                
                #get update data
                try:
                    updates = z.commandSend(server[i], 'apt-get upgrade --dry-run | grep "newly install"')
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
            
            for i in range(numberOfServers):
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
            
            for i in range(numberOfServers):
                print(server_name[i] + " :")

                print(z.commandSend(server[i], 'uptime'))
                print("")

        # print temp overview
        if choice == "3":
            os.system('clear')
            print("Loading temp details...\n")
            
            for i in range(numberOfServers):
                print(server_name[i] + " :")

                tempInfo = z.commandSend(server[i], 'sensors | grep Package | xargs echo').replace('\\xc2\\xb0', ' deg.')
                if tempInfo[0] == 'P':
                    print(' Package temperature:')
                    print(' ' + tempInfo)
                    print("")
                else:
                    print(' Package temperature:')
                    print(' Please install dependancies to see temperature')
                    print("")

        # print the user options
        termSize = z.updateTermSize()
        print(z.displayOptions(userInput, termSize))

        print("\nInput 'r' to reset and choose another overview")

        # break from loop if user selects an option
        # this will loop for 60 seconds before repeating the loop
        while 1:
           time.sleep(0.5)
           if userInput != "o" or userInput == "r":
                if userInput == "r":
                    userInput = "o"
                break

    # new ssh window page
    if userInput == "n":
        # change the userinput to allow the user to choose new one

        # display info
        os.system('clear')
        print("Which server would you like to open a conneciton with:")
        for i in range(numberOfServers):
            print(str(i) + ": " + server_name[i])

        while userInput == "n":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "n":
                    break

        serverSelect = int(userInput)

        print("Opening new window...")
        cmd = default_terminal + ' --command "ssh -i ' + server_key[serverSelect] + ' -p ' + server_port[serverSelect] + ' ' + server_user[serverSelect] + '@' + server_ip[serverSelect] + '"'
        os.system(cmd)

        # go back to main screen
        userInput = "d"

# logout of all servers
for i in range(numberOfServers):
    server[i].logout()

