# TO DO - consider looking at pulseway for further ideas
# - ADD MORE SERVERS!!!
#   make the code work dynamically to load them 
# - start by having a mode that displays one server,
#   then the option to choose which one to look at
#   then finally look to create a large dash showing all of them!`
# - look at options for displaying the data from server[0] so you can start to work on functionality of this
#   perhaps display it twice as if it is two separate connections?
# - parse data from server to variables
# - pull last line from folding file
# - password protect application?


from pexpect import pxssh       # used for ssh connection
from functions import *         # import all functions written for this program
import sys, time, os, threading, getch # other libraries
from termcolor import colored, cprint

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

    if server[i].login (server_ip[i], server_user[i], ssh_key=server_key[i]):
        print(server_name[i] + " connected. (" + str(i + 1) + "/" + str(numberOfServers) + ")")  
    else:
        print ("SSH session for " + server_name[i] + " failed on login.")
        print (str(server[i]))
        sys.exit() # exit program for failed ssh attempt

print ("SSH session login successful")

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

# this is the server shown by default
# can be changed by the "Server Select" screen
serverSelect = 0

while userInput != "q":
    
    # main page
    if userInput == "d":
        # pull data that doesn't need to be constantly updated
        storage = commandSend(server[serverSelect], "df -h / | awk 'FNR == 2 {print $5}'")
        # need to move these lines into the local data file
        #storage2 = commandSend(server[0], "df -h | grep /dev/sdb2 | awk ' {print $5}'")

        # clear terminal screen and start to display data
        while userInput == "d":
            os.system('clear')
            
            # server name and uptime
            print('Server Information: ' + server_name[serverSelect])
            print(commandSend(server[serverSelect], 'uptime'))
            print("")
            
            # storage data
            print(" Storage:")
            print(' storage used / = ' + storage + " ", end="")                                 
            percentBar("#", int(storage.split("%")[0]), 20)
            print("")
            
            # try to print additional storage if it has been input otherwise pass over
            try:
                storage2 = commandSend(server[0], "df -h " + additional_storage[serverSelect] + "| awk 'FNR == 2 {print $5}'")
                print(' Additional Storage = ' + storage2 + " ", end="")
                percentBar("#", int(storage2.split("%")[0]), 20)
                print("")
            except:
                pass
            
            # print folding data - last line of the log file
            print(" Folding Status:")
            # pull last line from folding log file and save it as variable
            foldingLog = foldingParse(commandSend(server[i], 'tail -1 /var/lib/fahclient/log.txt'))
            print(" " + foldingLog + " ", end='')

            # the funky code here pulls out the percent from the log file line
            percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
            print("")

            # try to print data from the additional log file
            try:
                print(" " + extra_logfile_name[serverSelect] + ":")
                print(" " + commandSend(server[serverSelect], 'tail -1 ' + extra_logfile_location[serverSelect] ))
                print("")
            except:
                pass

            
            
            # print the user options
            print(displayOptions(userInput))
            
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
            os.system('clear')
            print("User Info ----------------------------------------------------------------------")
            print("User Name: ", fData.User_Name.get_text())
            print("Rank Change (24hrs):", fData.user.Change_Rank_24hr.get_text())
            print("")
            print("Points Today:", fData.user.Points_Today.get_text())
            print("")
            print("Points Last 24hrs:", fData.user.Points_Last_24hr.get_text())
            print("Points 24hrs Average:", fData.user.Points_24hr_Avg.get_text())
            print("")
            print("Server Info --------------------------------------------------------------------")
            for i in range (numberOfServers):
                print(server_name[i] + " :")
                
                # pull last line from folding log file and save it as variable
                foldingLog = foldingParse(commandSend(server[i], 'tail -1 /var/lib/fahclient/log.txt'))
                print(" " + foldingLog + " ", end='')

                # the funky code here pulls out the percent from the log file line
                percentBar("#", int(foldingLog.split('(')[-1].split('%')[0]), 20)
                print("")

            # print the user options
            print(displayOptions(userInput))
            
            # break from loop if user selects an option
            # this will loop for 60 seconds before repeating the loop
            for i in range(0, 120):
                time.sleep(0.5)
                if userInput != "f":
                    break

# logout of all servers
for i in range(numberOfServers):
    server[i].logout()

# This is the start of looking to see how many updates are availiable for an ubuntu server
# server[0].sendline("sudo apt update| grep packages | awk '{ print $1" " $2 " " $3 " " $4 " " $5}'")
# server[0].sendline(server[0]_pass)
# server[0].prompt()
# test =  sshParse(str(server[0].before))

# This is how to print in colour for later
# print(colored('Press ENTER to exit...', 'white', 'on_green'))

# not an easy fix, needs some work, doesn't let the thread stay in the background
# this is for getting characters without using enter
# import getch
# # ...
# char = getch.getch() # User input, but not displayed on the screen
# # or
# char = getch.getche() # also displayed on the screen
