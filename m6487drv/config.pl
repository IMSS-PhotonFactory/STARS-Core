#Configuration of m2xxxdrv Client.

if($::NodeName eq 'm6487drv'
){###############################################################################

#STARS server
$::Server = 'localhost';
#$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.122'; #NPort host name.
$::NPORT_PORT  = 4004;             #NPort port number.

}else{
	die "Bad node name.";
}
1;