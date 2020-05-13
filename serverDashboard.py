# TO DO - consider looking at pulseway for further ideas
# - start by having a mode that displays one server,
#   then the option to choose which one to look at
#   then finally look to create a large dash showing all of them!`
# - look at options for displaying the data from server1 so you can start to work on functionality of this
#   perhaps display it twice as if it is two seperate connections?
# - parse data from server to variables
# - pull last line from folding file
# - encrypt data file


from pexpect import pxssh       # used for ssh connection
from functions import *         # import all functions written for this program
import sys, time, os, threading # other libraries

# Attempt to import server data from file if it exists
try:
    from local_data import *
    print("Config file found...")
except ImportError:
    print("No config file found")
    print("Confirm the file 'local_data.py' exists...")
    sys.exit(0)

# connect via ssh ----------------------------------------------------------------------------------------------------------

server1 = pxssh.pxssh() # connect to server 'server1'
if not server1.login (server1_ip, server1_user, server1_pass):
    print ("SSH session failed on login.")
    print (str(server1))
    sys.exit() # exit program for failed ssh attempt

print ("SSH session login successful")

# create interrupt thread --------------------------------------------------------------------------------------------------
# needed for the interrupt thread
flag = 1

# function that looks for keyboard press in the background
def get_input():
    global flag
    keystrk=input()
    # thread doesn't continue until key is pressed
    flag=False
    print('Exiting...')

# set this funciton as the var interrupt
interrupt = threading.Thread(target=get_input)

# main display region ------------------------------------------------------------------------------------------------------

# pull data that doesn't need to be constantly updated
storage1 = commandSend(server1, "df -h | grep root | awk ' {print $5}'")
storage2 = commandSend(server1, "df -h | grep /dev/sdb2 | awk ' {print $5}'")

# start the interrupt thread
interrupt.start()
# clear terminal screen and start to display data
while flag == 1:
    os.system('clear')
    print('Server Information: Elder')
    print(commandSend(server1, 'uptime'))
    print("")
    print("Storage:")
    print('storage used / = ' + storage1)
    print('storage used External Drive = ' + storage2)
    print("")
    print("Folding Status:")
    print(commandSend(server1, 'tail -1 /var/lib/fahclient/log.txt'))
    print("")
    print("Press ENTER to exit...")
    time.sleep(5)


server1.logout()

# This is the start of looking to see how many updates are availiable for an ubuntu server
# server1.sendline("sudo apt update| grep packages | awk '{ print $1" " $2 " " $3 " " $4 " " $5}'")
# server1.sendline(server1_pass)
# server1.prompt()
# test =  sshParse(str(server1.before))