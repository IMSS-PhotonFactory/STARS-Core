#! /usr/bin/python
# TEST user client type.

import socket

mynode    = 'pyuserclient'  #Node name of this client
server    = 'localhost'     #Host name of STARS Server
port      = 6057            #STARS server port. Default is 6057

# Connect STARS Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# Get key number. This number means, which keyword should be used (0 is 1st).
# But only 1 keyword "stars" is prepared in this example (see pyuserclient.key).
# It means "stars" is used as the keyword at any time.
keynum = s.recv(1024)
print 'Key number:', keynum,
keyword = 'stars'

# Create connection with STARS server
s.sendall(mynode + ' ' + keyword + '\n')
msg = s.recv(1024)
print 'Result:', msg,

# Send hello command to STARS server
s.sendall('System hello\n')
msg = s.recv(1024)
print msg,

# Send gettime command to STARS server
s.sendall('System gettime\n')
msg = s.recv(1024)
print msg,

# Send hello command to pyioclient.
# An error command will be returned if pyioclient is not running.
s.sendall('pyioclient hello\n')
msg = s.recv(1024)
print msg,

print 'Hit enter to end.'
msg = raw_input()
s.close()
