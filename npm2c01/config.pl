#Configuration of npm2c01 client.

if(
$::NodeName eq 'npm2c01'
){###############################################################################
@::MotorName     = qw(theta DTH);


#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.121'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

}else{
	die "Bad node name.";
}
1;
