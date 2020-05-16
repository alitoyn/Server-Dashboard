# Functions ----------------------------------------------------------------------------------------------------------------
global flag
## pulls the data from a row in the config file
def fileParse(dataToFind, fileVariable, index):
    if dataToFind in fileVariable[index]:
        tmp = fileVariable[index].split(": ")
        length = len(tmp)
        return tmp[length - 1]
    else:
        return ""

# takes the output from the ssh connection and returns the wanted answer
def sshParse(string):
	delim = '\\r\\n'
	output = string[string.find(delim)+len(delim):string.rfind(delim)]
	return output

# takes the ssh server connection and a command and returns the result
# DEPENDANT ON sshParse function
def commandSend(server, command):
	server.sendline(command)
	server.prompt()
	return sshParse(str(server.before))

# this splits by : and dispalys the last string in the list
def foldingParse(data):
	data = data.split(":")
	return(str(data[len(data) - 1]))

def getFoldingData(id):
		import requests

		URL = "https://folding.extremeoverclocking.com/xml/user_summary.php?u=" + str(id)
		return URL
		response = requests.get(str(URL))
		with open('folding.xml', 'wb') as file:
			file.write(response.content)