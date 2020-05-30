# TO DO - consider looking at pulseway for further ideas

# - dash to display multiple servers
# - password protect application?

# folding additions:
#   - predict how long is left?

# use getpass from the following code to save password for sudo login later...
# from pexpect import pxssh
# import getpass
# try:
#     s = pxssh.pxssh()
#     hostname = raw_input('hostname: ')
#     username = raw_input('username: ')
#     password = getpass.getpass('password: ')
#     s.login(hostname, username, password)
#     s.sendline('uptime')   # run a command
#     s.prompt()             # match the prompt
#     print(s.before)        # print everything before the prompt.
#     s.sendline('ls -l')
#     s.prompt()
#     print(s.before)
#     s.sendline('df')
#     s.prompt()
#     print(s.before)
#     s.logout()
# except pxssh.ExceptionPxssh as e:
#     print("pxssh failed on login.")
#     print(e)

from pexpect import pxssh       # used for ssh connection
from functions import *        # import all functions written for this program
import sys, time, os, threading, getch # other libraries
from termcolor import colored, cprint
import getpass

# get config info ----------------------------------------------------------------------------------------------------------

# Attempt to import server data from file if it exists
try:
    from local_data import *
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)

# get the most up to date folding data for the user
getFoldingData(foldingUserID)
fData = foldingXmlParse()

# connect via ssh ----------------------------------------------------------------------------------------------------------

# connect to all servers
numberOfServers = len(server_name)

server = {} # this list holds the ssh connections

print("\nConnect to servers...")
for i in range(numberOfServers):
    server[i] = pxssh.pxssh() # connect to server 'server[0]'

    try:
        e = server[i].login (server_ip[i], server_user[i], ssh_key=server_key[i], quiet=True)
        print(server_name[i] + " connected. (" + str(i + 1) + "/" + str(numberOfServers) + ")")  
    except pxssh.ExceptionPxssh as e:
        print ("SSH session for " + server_name[i] + " failed on login.")
        print (str(server[i]))
        # sys.exit() # exit program for failed ssh attempt

print ("\nSSH session login successful")

# create interrupt thread --------------------------------------------------------------------------------------------------
# needed for the interrupt thread
userInput = "d"

# function that registers keyboard press in the background
# doesn't like being in the functions folder
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
    termSize = updateTermSize()

    # main page
    if userInput == "d":
        # prompt the user that something is happening
        print("\nLoading...\n")

        # pull data that doesn't need to be constantly updated
        # get storage data
        # cmd = "df -h / | awk 'FNR == 2 {print $5 " (" $3 "/" $2 ")"}'"
        cmd = "df -h / | awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'"
        storage = commandSend(server[serverSelect], cmd) #"df -h / | awk 'FNR == 2 {print $5 $2}'"
        try:
            storage2 = commandSend(server[serverSelect], "df -h " + additional_storage[serverSelect] + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'")
            add_stor_flag = 1
        except:
            add_stor_flag = 0

        #get update data
        try:
            updates = commandSend(server[serverSelect], 'apt-get upgrade --dry-run | grep "newly install"')
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
            print(commandSend(server[serverSelect], 'uptime'))
            print("")
            
            # storage data
            print(" Storage:")
            print(' Root Directory / = ' + storage + " ", end="")                                 
            percentBar("#", int(storage.split("%")[0]), 20)
            print("")

            # try to print additional storage if it has been input otherwise pass over
            if add_stor_flag == 1:
                print(' Additional Storage = ' + storage2 + " ", end="")
                percentBar("#", int(storage2.split("%")[0]), 20)
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
                foldingLog = foldingParse(commandSend(server[serverSelect], 'tail -1 /var/lib/fahclient/log.txt'))
                print(" " + foldingLog + " ", end='')

                try:
                    # the funky code here pulls out the percent from the log file line
                    percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
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
                    print(" " + commandSend(server[serverSelect], 'tail -1 ' + extra_logfile_location[serverSelect][i] ))
                    print("")
                except:
                    pass

            # print the user options at the bottom
            termSize = updateTermSize()            
            print(displayOptions(userInput, termSize))
            
            # break from loop if user selects an option
            # this will loop for 60 seconds before repeating the loop
            for i in range(0, 120):
                time.sleep(0.5)
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
            termSize = updateTermSize()
            os.system('clear')
            print(getScreenDivider("User Info", termSize))
            print("User Name: ", fData.User_Name.get_text())
            print("Rank Change (24hrs):", fData.user.Change_Rank_24hr.get_text())
            print("")
            print("Points Today:", fData.user.Points_Today.get_text())
            print("")
            print("Points Last 24hrs:", fData.user.Points_Last_24hr.get_text())
            print("Points 24hrs Average:", fData.user.Points_24hr_Avg.get_text())
            print("")
            print(getScreenDivider("Server Info", termSize))
            for i in range (numberOfServers):
                print(server_name[i] + " :")
                
                try:
                    foldingLog = foldingParse(commandSend(server[i], 'tail -1 /var/lib/fahclient/log.txt'))
                    print(" " + foldingLog + " ", end='')

                    try:
                        # the funky code here pulls out the percent from the log file line
                        percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
                    except:
                        print("")
                    print("")
                except:
                    print(" Log file parse failed")
                    print("")

            # print the user options
            print(displayOptions(userInput, termSize))
            
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
        print("")
        while userInput == "c":
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "c":
                    break

        commandToSendServer = int(userInput)
        userInput = "c"

        if(commandToSendServer == 0):
            print("Performing shutdown...")
        if(commandToSendServer == 1):
            print("Performing reboot...")
        if(commandToSendServer == 2):
            print("Performing update...")
            # this doesn't work yet
            # password = getpass.getpass('sudo password: ')
            # commandSend(server[serverToSendCommand], 'sudo apt-get update && sudo apt upgrade')
            # commandSend(server[serverToSendCommand], password)
        time.sleep(1)
        userInput = "d"

    if userInput == 'o':
        # display info
        os.system('clear')
        print("Select which option to show details for:\n")
        print("0: updates")
        print("1: storage")
        print("2: uptime")

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
                    updates = commandSend(server[i], 'apt-get upgrade --dry-run | grep "newly install"')
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
                storage = commandSend(server[i], cmd)
                try:
                    storage2 = commandSend(server[i], "df -h " + additional_storage[i] + "| awk 'FNR == 2 {print $5 " + '" (" $3 " / " $2 ")"}' + "'")
                    add_stor_flag = 1
                except:
                    add_stor_flag = 0
                
                print(' Root Directory / = ' + storage + " ", end="")                                 
                percentBar("#", int(storage.split("%")[0]), 20)
                print("")

                # try to print additional storage if it has been input otherwise pass over
                if add_stor_flag == 1:
                    print(' Additional Storage = ' + storage2 + " ", end="")
                    percentBar("#", int(storage2.split("%")[0]), 20)
                    print("")

        # print uptime overview
        if choice == "2":
            os.system('clear')
            print("Loading uptime details...\n")
            
            for i in range(numberOfServers):
                print(server_name[i] + " :")

                print(commandSend(server[i], 'uptime'))
                print("")

        # print the user options
        termSize = updateTermSize()
        print(displayOptions(userInput, termSize))

        # break from loop if user selects an option
        # this will loop for 60 seconds before repeating the loop
        while 1:
           time.sleep(0.5)
           if userInput != "o":
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
        cmd = default_terminal + ' --command "ssh -i ' + server_key[serverSelect] + ' ' + server_user[serverSelect] + '@' + server_ip[serverSelect] + '"'
        os.system(cmd)

        # go back to main screen
        userInput = "d"

# logout of all servers
for i in range(numberOfServers):
    server[i].logout()

