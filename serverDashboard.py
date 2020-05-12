# TO DO
# - parse data from server to variables
# - pull last line from folding file

from pexpect import pxssh
from functions import *

#load data from data file into variables -----------------------------------------------------------------------------------
try:
    file = open("local_data","r")
    config = file.readlines()
    file.close()
    print("Config file found...")
except:     
    print("No config file found")
    print("Confirm the file 'local_data' exists...")
    sys.exit(0)

# data to pull from local data file
elder_user = ""
elder_pass = "" 
elder_ip = ""
count = 0 # needed for file parser

for i in config:
    if elder_user == "":
                elder_user = fileParse("elder_user", config, count)
    if elder_pass == "":
                elder_pass = fileParse("elder_pass", config, count)
    if elder_ip == "":
                elder_ip = fileParse("elder_ip", config, count)
    count = count + 1


# connect via ssh ----------------------------------------------------------------------------------------------------------

elder = pxssh.pxssh() # connect to server 'elder'
if not elder.login (elder_ip, elder_user, elder_pass):
    print ("SSH session failed on login.")
    print (str(elder))
    return 0

print ("SSH session login successful")

result = commandSend(elder, "df -h | grep root | awk ' {print $5}'")
print('storage used / = ' + result)
result = commandSend(elder, "df -h | grep /dev/sdb2 | awk ' {print $5}'")
print('storage used External Drive = ' + result)


elder.logout()
    