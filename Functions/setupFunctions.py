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
	    except pxssh.ExceptionPxssh as e:
	        print ("SSH session for " + config.server_name[i] + " failed on login.")
	        print (str(serverSshConnections[i]))
	        # sys.exit() # exit program for failed ssh attempt

	print ("\nSSH session login successful")
	return serverSshConnections