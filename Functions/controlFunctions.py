def checkFileExists(filename):
    import os.path
    if os.path.isfile(filename):
        return True
    else:
        return False

def connectToServers():
    import config
    from pexpect import pxssh

    numberOfServers = len(config.server_name)

    serverSshConnections = {} # this list holds the ssh connections

    print("\nConnect to servers...")
    for i in range(numberOfServers):
        serverSshConnections[i] = pxssh.pxssh() # connect to server 'server[0]'

        try:
            e = serverSshConnections[i].login (config.server_ip[i], config.server_user[i], ssh_key=config.server_key[i], quiet=True, port=config.server_port[i])
            print(config.server_name[i] + " connected. (" + str(i + 1) + "/" + str(numberOfServers) + ")")  
        except pxssh.ExceptionPxssh:
            print ("SSH session for " + config.server_name[i] + " failed on login.")
            serverSshConnections[i] = None

    activeConnections = checkAtLeastOneConnectionActive(serverSshConnections)

    if activeConnections != True:
        print('\nNo servers successfully logged in')
        exitProgram()

    print ("\nSSH session login successful")
    return serverSshConnections

def checkAtLeastOneConnectionActive(serverSshConnections):
    check = False

    for i in range(len(serverSshConnections)):
        if serverSshConnections[i] != None:
            check = True

    return check


def createDisplayOptions(currentScreen):
    from Functions import displayFunctions

    terminalSize = updateTermSize()

    screenOptions = [
        "s: Server Select", 
        "d: Dashboard",
        "o: Overview",
        "f: Folding Details", 
        "c: Send Command", 
        "n: New SSH Window",
        "q: Quit"   
    ]

    output = displayFunctions.getScreenDivider("Options", terminalSize[1])
    limitPerRow = 3
    numberOfScreenOptions = len(screenOptions)
    count = 0

    for i in range(numberOfScreenOptions):

        if currentScreen != screenOptions[i][0]:
            output = output + screenOptions[i]
            
            # if the option is not the last one,
            # then add the deliminator
            if screenOptions[i][0] != "q":
                output = output + " | "
        
        if count == limitPerRow:
            output = output + "\n"
            count == -1

        count += 1
    return output


def launchProcessesView(connectedServer, selectedServer):
    import config, os
    from Functions import dataFunctions

    bashCommandForProcessess = 'htop'

    fullBashCommand = config.default_terminal + ' "ssh -i ' + config.server_key[selectedServer] + ' -p ' + config.server_port[selectedServer] + ' -t ' + config.server_user[selectedServer] + '@' + config.server_ip[selectedServer] + ' ' + bashCommandForProcessess + '"'

    os.system(fullBashCommand)

def logoutOfAllServers(listOfSshConnections):
    print("Exiting...")
    for i in range(len(listOfSshConnections)):
        if checkServerIsLoggedIn(listOfSshConnections[i]):
            listOfSshConnections[i].logout()

def exitProgram():
    import sys
    sys.exit(0)

def updateTermSize():
	import os
	
	defaultRows = 24
	defualtColumns = 80

	try:
		rows, columns = os.popen('stty size', 'r').read().split()
		return [int(rows), int(columns)]

	except:
		return [defaultRows, defualtColumns]

def checkServerIsLoggedIn(serverSshConnection):
    if serverSshConnection != None:
        return True
    else:
        return False

def appUpdater():
    import os, time
    from Functions import dataFunctions

    bashCommandToUpdateRepo = 'git remote update | xargs echo > updateData; git status -uno > updateData'
    os.system(bashCommandToUpdateRepo)

    response = checkForUpdates()

    if response == True:
        question = '\nThere is an update available\nWould you like to apply the update?\n'
        allowedResponses = ['Y', 'y', 'N', 'n']
        answer = dataFunctions.dataValWithQuestion(question, allowedResponses)
        if answer == 'Y' or answer == 'y':

            os.system('git pull >> updateData')

            print('Restart the program to complete update\n\n')
            time.sleep(2)
    else:
        print('App up to date.')

    bashCommandToRemoveDataFile = 'rm updateData'
    os.system('rm updateData')

def checkForUpdates():

    updatesAvailableResponse = '  (use "git pull" to update your local branch)\n'

    with open('updateData') as f:
        for line in f:
            if line == updatesAvailableResponse:
                return True
    return False