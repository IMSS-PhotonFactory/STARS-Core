#Configuration of ORTEC974 Client.

if(
$::NodeName eq 'ortec974'
){###############################################################################

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.122'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

@::CounterName   = qw(counter01 counter02 counter03 counter04);

}else{
	die "Bad node name.";
}
1;