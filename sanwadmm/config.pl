#Configuration of sanwa dmm Client.

if(
$::NodeName eq 'sanwadmm'
){###############################################################################

#STARS server
$::Server = 'localhost';
#$::Server = '192.168.11.101';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.166'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

}else{
	die "Bad node name.";
}
1;