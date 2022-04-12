#Configuration of pm16c02 client.

if(
$::NodeName eq 'pm16c02'
){###############################################################################
@::MotorName     = qw(theta DTH unused_2 unused_3 MFV MRV MFH MRH BNT unused_9 unused_A unused_B unused_C unused_D unused_E unused_F);

$::ReadCancelBacklash = 'backlash.txt'; #Cancelbacklash Read Error for pm16c02 Version Below 1.21

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.123'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.





}elsif(
$::NodeName eq 'pm16c021'
){###############################################################################
@::MotorName     = qw(th d1 dth1 al1 l2 d2 dth2 al2 m1u m1d m1db m2u m2d m2ub m2db MotorF);

$::ReadCancelBacklash = 'backlash.txt'; #Cancelbacklash Read Error For pm16c02 Version Below 1.21

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.151'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.





}elsif(
$::NodeName eq 'pm16c022'
){###############################################################################
@::MotorName  = qw(s1u s1d s115 s117 s2u s2d s215 s217 s3u s3d s315 s317 a1sc1 a1sh MotorE a1sv);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.151'; #NPort host name.
$::NPORT_PORT  = 4002;             #NPort port number.





################################################################################
}else{
	die "Bad node name.";
}
1;

