# TO DO - consider looking at pulseway for further ideas
# - start by having a mode that displays one server,
#   then the option to choose which one to look at
#   then finally look to create a large dash showing all of them!`
# - look at options for displaying the data from server1 so you can start to work on functionality of this
#   perhaps display it twice as if it is two seperate connections?
# - parse data from server to variables
# - pull last line from folding file
# - encrypt data file


from pexpect import pxssh   # used for ssh connection
from functions import *     # import all functions written for this program
import sys, time, os        # other libraries

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

# pull data that doesn't need to be constantly updated
storage1 = commandSend(server1, "df -h | grep root | awk ' {print $5}'")
# print('storage used / = ' + result)
storage2 = commandSend(server1, "df -h | grep /dev/sdb2 | awk ' {print $5}'")
# print('storage used External Drive = ' + result)
print("")


server1.sendline("sudo apt update| grep packages | awk '{ print $1" " $2 " " $3 " " $4 " " $5}'")
server1.sendline(server1_pass)
server1.prompt()
test =  sshParse(str(server1.before))



# clear terminal screen and start to display data
for i in range (10):
    os.system('clear')
    print(test)
    print("Server: server1")
    print('storage used / = ' + storage1)
    print('storage used External Drive = ' + storage2)
    print(commandSend(server1, 'tail -1 /var/lib/fahclient/log.txt'))
    time.sleep(5)


server1.logout()
    