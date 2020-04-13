##
## STARS kernel
##



STARS Server
$Date: 2010-01-19 02:43:50 $ Takashi Kosuge
==========================================================================

Usage: takaserv [-h] [-port ServerPort] [-lib LibDir] [-key KeyDir]
          [-service ServiceName]

You are able to run STARS server as service with Windows.
Install and run as service:
   takaserv --install auto -lib LibDir
Remove service:
   takaserv --remove

If your OS is FreeBSD, Linux etc., you are able to run STARS server on
 back ground.
   ./takaserv &


Please refer document files in "doc" directory.

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
2008-03-14
[Reconnectable deny and allow.]
This version of kernel has reconnectable qualifying functions and it is
 in test fase. 
Please note that the specifications might be changed in the future.

"reconnectable_deny.cfg" and "reconnectable_allow.cfg" under "takaserv-lib" are used 
for checking limitation of reconnections. These files are simple text file and
they have reconnectable check list which are separated with LF(or CR + LF for Windows).

If the stars client which has same terminal name has already connected to stars when 
trying to connect, 
Kernel checkes reconnectable with "reconnectable_deny.cfg" first,
then the "terminal name" and "terminal name + host name" doesn't
match the deny list, it checks with "reconnectable_allow.cfg".
If the "terminal name" or "teminal name + host name" matches,
the connected client will be disconnected then new client will be connected. 

Example of "reconnectable_deny.cfg" and "reconnectable_allow.cfg" are shown below.
("#" character of first column is used for comment.)

# Example of reconnectable_allow.cfg
# term1 from localhost can be reconnectable. 
term1 localhost
# term2 from any host can be reconnectable. 
term2

==========================================================================
2007-07-05
[Command deny and allow.]
This version of kernel has command qualifying functions.

"command_deny.cfg" and "command_allow.cfg" under "takaserv-lib" are used 
for checking limitation of commands. These files are simple text file and
they have command check list which are separated with LF(or CR + LF for Widows).

Kernel checkes a command with "command_deny.cfg" first, then the command doesn't
match the deny list, it checks with "command_allow.cfg". If the command muches,
it will be sent to corresponding client.

Example of "command_deny.cfg" and "command_allow.cfg" are shown below.
("#" character of first column is used for comment.)

# Example of command_deny.cfg
# Restrict SetValue command from term1 to ioc1 and ioc2.
#
term1>ioc1 SetValue
term1>ioc2 SetValue


# Example of command_allow.cfg
# Allow only hello command from term1 to System.
#
term1>System hello

==========================================================================
2008-12-11 "allow.cfg" and "<nodename>.allow" supports hostname,ip address and regular  expression.

2008-03-14 Added reconnectable function.

2007-07-05 Bug fixed.
           Fixed regex part of checking command allow and deny.

2007-06-22 Release.

2007-04-23 Bug(?) fixed.
           System replied error message when receiving reply message.
           New version of takaserv does not respond "reply message" to the "System".

2007-01-23 Bug has been fixed.
           The bug was,
           if a terminal which has a hierachical structre sends a flgon command to "System" like,
           "term1.xx>System flgon term2"
           then term2 sends,
           "System _Event"
           STARS server will be down.


2006-11-06 Added function which restricts message delivery.

2005-04-27 Development has been started.

