#Configuration of id gateway client.

if(
$::NodeName eq 'idgateway'
){###############################################################################

#STARS server
$::Server = 'localhost';
## For IDGW interface
$::NPORT_HOST  = '192.168.11.120';    #ID Gateway host name.
#$::NPORT_HOST  = 'pfconrg03.kek.jp';
$::NPORT_PORT  = 8881;               #ID Gateway port number.
#################################################################
@::IDCANWRITE = qw(NE1);			 #ID Move Allowed
$::ConfigMaximumDifference{"GapY"}=0.002;
$::Logging    = 1;
$::LogDir     = 'c:/stars/logdata';
#$::LogDir     = '.';
$::ConfigLimitMaximum{"GapY"}=100;
$::ConfigLimitMinimum{"GapY"}=30;
$::ConfigAutoResetBusyTime{"GapY"}=30000;	 #MiliSeconds


## 
################################################################################
}else{
	die "Bad node name.";
}
1;
