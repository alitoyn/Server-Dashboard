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
	import datetime, os
	#find out if file exists and save the last line
	try:
		with open('foldingStats.xml') as f:
			for line in f:
				pass
			processedDay = line
	# if the file doesn't exist then set the var as "0" to force file download
	except:		
		processedDay = "0"

	# if the file was not last processed today
	if processedDay != str(datetime.datetime.today().day):
		print("Updating folding stats...")
		# download folding data - this should be chnaged to be in python at some point
		URL = "https://folding.extremeoverclocking.com/xml/user_summary.php?u=" + id
		cmd = "wget -q -O foldingStats.xml " + URL
		os.system(cmd)
		# append the day of the month to the end
		with open("foldingStats.xml", "a") as myfile:
			myfile.write(str(datetime.datetime.today().day))
	else:
		print("Folding stats up to date")

# parses the folding data xml file and returns a var holding the information
def foldingXmlParse():
	try:
		# import beautiful soup - for parsing information
		from bs4 import BeautifulSoup
		# use BS to parse the data
		with open("foldingStats.xml") as fp:
			data = BeautifulSoup(fp, "xml")
		# pass this data back to the main funciton
		return data
	except:		
		print("Folding Stats data parse failed")

def percentBar(symbol, percent, length):
	data = round((percent/100) * length)
	count = 0
	print("[", end="")
	for i in range(length):
		if count < data:
			print(symbol, end="")
			count += 1
		else:
			print(".", end="")
	print("]")

def displayOptions(currentScreen, size):
	options = [
		"s: Server Select", 
		"d: Dashboard",
		"o: Overview",
		"f: Folding Details", 
		"c: Send Command", 
		"n: New SSH Window",
		"q: Quit"
		
	]

	# output = "--------------------------------------------------------------------------------\n"
	# output = output + "Options:\n"
	output = getScreenDivider("Options:", size)
	limit = 3
	for i in range(len(options)):
		if currentScreen != options[i][0]:
			output = output + options[i]
			if options[i][0] != "q":
				output = output + " | "
		if i == 3:
			output = output + "\n"
	return output

def updateTermSize():
	import os
	try:
		r, c = os.popen('stty size', 'r').read().split()
		return [int(r), int(c)]

	except:
		return [24, 80]

def getScreenDivider(text, size):
	output = text + " "

	for i in range(size[1] - len(text) - 1):
		output = output + "-"
	output = output + "\n"
	return output
