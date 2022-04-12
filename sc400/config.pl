#Configuration of sc400/sc200 client.

if(
$::NodeName eq 'sc400'
){###############################################################################
@::MotorName   = qw(ch0 ch1 ch2 ch3);
@::EncoderName = qw(enc0 enc1 enc2 enc3);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.122'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

}elsif(
$::NodeName eq 'sc200'
){###############################################################################
@::MotorName   = qw(ch0 ch1);
@::EncoderName = qw(enc0 enc1);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.122'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

################################################################################
}else{
	die "Bad node name.";
}
1;
