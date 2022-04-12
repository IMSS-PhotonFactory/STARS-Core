#Configuration of pm16c04 client.

if(
$::NodeName eq 'pm16c04'
){###############################################################################
@::MotorName     = qw(th d1 dth1 al1 l2 d2 dth2 al2 m1u m1d m1db m2u m2d m2ub m2db MotorF);

#STARS server
$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.123'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.





}elsif(
$::NodeName eq 'pm16c021'
){###############################################################################
@::MotorName  = qw(th d1 dth1 al1 l2 d2 dth2 al2 m1u m1d m1db m2u m2d m2ub m2db MotorF);

#STARS server
$::Server = '192.168.11.100';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.123'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.




}elsif(
$::NodeName eq 'pm16c4x'
){###############################################################################
@::MotorName  = qw(th dth1 d1 al1 Mt4 d2 al2 Mt7 M1UH M1UV M1DV M1DH M1Db MtD MtE MtF);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.131'; #NPort host name.
#$::NPORT_HOST  = '192.168.11.123'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

################################################################################
}else{
	die "Bad node name.";
}
1;

