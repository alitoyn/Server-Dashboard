# folding functions
def dailyDownloadFoldingUserData(id):
	import datetime, os
	
	dateOfDownload = wasFoldingDataDownloadedToday('foldingStats.xml')

	today = str(datetime.datetime.today().day)

	if dateOfDownload != today:
		print("Updating folding stats...")
		# download folding data - this should be chnaged to be in python at some point
		URL = "https://folding.extremeoverclocking.com/xml/user_summary.php?u=" + id
		cmd = "wget -q -O foldingStats.xml " + URL
		os.system(cmd)
		
		appendDateToFoldingData('foldingStats.xml')

	else:
		print("Folding stats up to date")

def wasFoldingDataDownloadedToday(foldingXML):
	try:
		with open(foldingXML) as f:
			for line in f:
				pass
			dayFileWasProcessed = line
	# if the file doesn't exist then set the var as "0" to force file download
	except:		
		dayFileWasProcessed = "0"

	return dayFileWasProcessed

def appendDateToFoldingData(foldingXML):
	import datetime
	with open(foldingXML, "a") as myfile:
			myfile.write(str(datetime.datetime.today().day))


def foldingXmlParse():
	try:
		# import beautiful soup - for parsing information
		from bs4 import BeautifulSoup
		# use BS to parse the data
		with open("foldingStats.xml") as filePointer:
			data = BeautifulSoup(filePointer, "xml")
		# pass this data back to the main funciton
		return data
	except:		
		print("Folding Stats data parse failed")

def getFoldingLogData(connectedServer):
	from Functions import dataFunctions, displayFunctions

	bashCommandToGetFoldingData = 'tail -1 /var/lib/fahclient/log.txt'

	try:
		foldingLog = foldingLogParse(dataFunctions.commandSend(connectedServer, bashCommandToGetFoldingData))

		percentageFolded = int(foldingLog.split('(')[-1].split('%')[0])

		try:
			percentBar = displayFunctions.createPercentBar("#", percentageFolded, 20)
		except:
			percentBar = ''
    
	except:
		foldingLog = " Log file parse failed"
		percentBar = ''

	output = ' ' + foldingLog + ' ' +  percentBar + '\n'
    
	return output

def foldingLogParse(data):
	data = data.split(":")
	return(str(data[len(data) - 1]))