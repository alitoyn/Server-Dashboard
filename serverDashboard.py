from pexpect import pxssh
# Functions ----------------------------------------------------------------------------------------------------------------
## pulls the data from a row in the config file
def fileParse(dataToFind, fileVariable, index):
    if dataToFind in fileVariable[index]:
        tmp = fileVariable[index].split(": ")
        length = len(tmp)
        return tmp[length - 1]
    else:
        return ""

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
count = 0 # needed for file parser

for i in config:
    if elder_user == "":
                elder_user = fileParse("elder_user", config, count)
    if elder_pass == "":
                elder_pass = fileParse("elder_pass", config, count)
    count = count + 1


# connect via ssh ----------------------------------------------------------------------------------------------------------

elder = pxssh.pxssh()
if not elder.login ('192.168.0.24', elder_user, elder_pass):
    print ("SSH session failed on login.")
    print (str(elder))
else:
    print ("SSH session login successful")
    elder.sendline ('uptime ; df -h')
    elder.prompt()         # match the prompt
    print(elder.before)     # print everything before the prompt.
    elder.logout()
    