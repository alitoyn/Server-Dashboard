# folding functions

def dailyDownloadFoldingUserData(id):
	import datetime, os
	#find out if file exists and save the last line
	
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
