from pexpect import pxssh

#write coder here to pull password from other file
user = 
password = 

s = pxssh.pxssh()
if not s.login ('192.168.0.24', user, password):
    print ("SSH session failed on login.")
    print (str(s))
else:
    print ("SSH session login successful")
    s.sendline ('uptime ; df -h')
    s.prompt()         # match the prompt
    print (s.before)     # print everything before the prompt.
    s.logout()
    