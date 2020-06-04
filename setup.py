# This file creates the config file for the server-dashboard.py program
import sys, time

# find if config file exists and then prompt user to overwrite if it does --------------------------------------------------
try: 				# try to import file
	from config import *
	print("Config file already exisits")
	found = 1	
except:				# catch the exception if it does not exisit
	found = 0
	print("Config file not found")

if found == 1:	# if it does exist, primpt the user
	while 1:
			response = input("\nWould you like to overwrite it? (y/n)\n")
			# if they do not want to overwrite, close the program
			if response == 'n' or response == 'N':
				print("Rename your existing config file and then re-run this program")
				sys.exit()
			# if they do want to overwrite, leave the while loop
			elif response == 'y' or response == 'Y':
				print("input was yes")
				break
			# catch invalid responses
			else:
				print("Input invalid")
				time.sleep(0.5)

