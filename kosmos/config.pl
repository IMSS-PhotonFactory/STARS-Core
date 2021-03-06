#Configuration of kosmos-aries client.

if(
$::NodeName eq 'aries'
){###############################################################################
@::MotorName   = qw(ch0 ch1);
@::EncoderName = qw(enc0 enc1);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = 'localhost'; #NPort host name.
$::NPORT_PORT  = 4001;        #NPort port number.

}elsif(
$::NodeName eq 'crux'
){###############################################################################
@::MotorName   = qw(ch0 ch1);
@::EncoderName = qw(enc0 enc1);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = 'localhost'; #NPort host name.
$::NPORT_PORT  = 4001;        #NPort port number.

################################################################################
}else{
	die "Bad node name.";
}
1;
