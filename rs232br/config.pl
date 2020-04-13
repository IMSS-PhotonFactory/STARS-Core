#Configuration of RS232 Bridge Client.

if(
$::NodeName eq 'rs232br'
){##############################################################################
#STARS server
$::Server = 'localhost';

## For NPORT interface
#$::NPORT_HOST  = '192.168.11.132'; #NPort host name.
$::NPORT_HOST  = 'localhost'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.



}elsif(
$::NodeName eq 'rs232br-telnet'
){##############################################################################
$::TelnetNode = $::NodeName;        #Telnet mode will be activate if $::TelnetNode is not ''.



#STARS server
$::Server = 'localhost';

#$::NPORT_HOST  = '192.168.11.132'; #NPort host name.
$::NPORT_HOST  = 'localhost'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

#Login script,
$::Script=<<"SCRIPT";
SEND:telnet localhost 6057
KEYW:$::NodeName
SENDB:0x1d
SEND:mode character
SEND: 
SCRIPT

##Example of script commands.
#SENDB:0x10 0x20 12 13
#SEND:telnet localhost 6057
#KEYW:$::NodeName

$::ConsoleDelimiter = "\r";
#\n is used in normal mode and \n is used in telnet mode by default.
#

#Disconnect, this string is sent automatically at disconeection time.
$::DisconnectionMessage = "quit";

#Detect disconnect.
$::DetectDisconnection  = "Connection closed by foreign host";

#}elsif(
#$::NodeName eq 'rs232br-execute'
#){##############################################################################


}else{
	die "Bad node name.";
}
1;