#Configuration of m2xxxdrv Client.

if($::NodeName eq 'm6482drv'
){###############################################################################

#STARS server
$::Server = 'localhost';
#$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.0.135'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

}elsif($::NodeName eq 'm6485a2'
){###############################################################################

#STARS server
$::Server = 'localhost';
#$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.125'; #NPort host name.
$::NPORT_PORT  = 4002;             #NPort port number.

}elsif($::NodeName eq 'm6485a3'
){###############################################################################

#STARS server
$::Server = 'localhost';
#$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.125'; #NPort host name.
$::NPORT_PORT  = 4003;             #NPort port number.

}else{
	die "Bad node name.";
}
1;
