#! /usr/bin/python
# TEST IO client type.

import socket

mynode    = 'pyioclient'  #Node name of this client
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


print 'Waiting commands from STARS server. ^C to end.'
# Handle commands
while True:
#Extract From, To, Message
    msg = s.recv(1024)
    msg = msg.rstrip('\n')
    msg = msg.replace('>', ' ')   #Replace "From>To Command" into "From To Command"
    cmd = msg.split()
    print 'From:   ', cmd[0]
    print 'To:     ', cmd[1]
    print 'Message:', cmd[2]

#Handle commands.
    if cmd[2] == 'hello':
        s.sendall(cmd[0] + ' @hello nice to meet you.\n')
    elif cmd[2] == 'help':
        s.sendall(cmd[0] + ' @help hello terminate.\n')
    elif cmd[2] == 'terminate':
        s.sendall(cmd[0] + ' @terminate Ok:\n')
        break
    elif cmd[2][0] == '_' or cmd[2][0] == '@':
        continue
    else:
        s.sendall(cmd[0] + ' @' + cmd[2] + ' Er: Bad command or parameter.\n')

s.close()
