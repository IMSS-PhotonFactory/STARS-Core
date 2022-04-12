#Configuration of pm4c05a client.

if(
$::NodeName eq 'pm4c05a'
){###############################################################################
@::MotorName     = qw(motor_A motor_B motor_C motor_D);

#STARS server
$::Server = 'localhost';
$::ReadCancelBacklash = 'configparm.txt'; #Cancelbacklash Read Error for pm16c02 Version Below 1.21

## For NPORT interface
$::NPORT_HOST  = '192.168.11.126'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

}else{
	die "Bad node name.";
}
1;
