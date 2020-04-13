##
## Client bridge version 1
##

Client Bridge Version: 1 Revision: 1.0 Date: 2007/07/20 00:00:00
Usage: clientBridge [-h] [-port ServerPort] [-lib LibDir] [-key KeyDir]
          [-service ServiceName] [-nodename NodeName]
          [-starsserver StarsServer] [-starsport StarsServerPort]
          [-starskeyfile StarsServerKeyFile]

You are able to run Client bridge as service with Windows.
Install and run as service:
   clientBridge --install auto -port ServerPort -lib LibDir -starsserver StarsServer
-starskeyfile StarsServerKeyFile
Remove service:
   clientBridge --remove

If your OS is FreeBSD, Linux etc., you are able to run Client bridge on
 back ground.
   ./clientBridge -port ServerPort -starsserver StarsServer &
   
==========================================================================
2008-12-11
[allow.cfg and <nodename>.allow supports hostname,ip address and regular expression.]

The file 'allow.cfg' which has the client's list connectable to starsserver,
is changed to support the expression of the ip address in addition to the hostname, 
and regular expression.

Example of "allow.cfg"
("#" character of first column is used for comment.)

# Example of allow.cfg
127.0.0.1
localhost
# IP address between 192.168.11.204 - 192.168.11.206
192.168.11.20[4-6]
# IP address matches 192.168.11. #now commented
#192.168.11.*

-------------------------
The file '<nodename>.allow' is optional which's used to limit the client
connectable to starsserver using nodename '<nodename>'
by the client's hostname or ip address information.
The file '<nodename>.allow' supports hostname and ip address and regular expression.

Example of "<nodename>.allow" are shown below.
("#" character of first column is used for comment.)

# Example of term1.allow
127.0.0.1
localhost
# IP address betweem 192.168.11.204 - 192.168.11.206
192.168.11.20[4-6]
# IP address matches 192.168.11. #now commented
#192.168.11.*
==========================================================================

2008-12-11 "allow.cfg" and "<nodename>.allow" supports hostname,ip address and regular  expression.
           "kernel\takaserv" made same changes at 2008-12-11.

2007-12-12 Program name changed to 'clientBridge'.

2007-07-20 1st released as program name 'starsbr'.
