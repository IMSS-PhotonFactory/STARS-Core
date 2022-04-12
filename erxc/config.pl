#Configuration of ER4C-03A, ER2C-03A client.

if(
$::NodeName eq 'er4c'
){###############################################################################
@::ChName     = qw(A B C D);

##STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.2.31';   #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

## Caluculatation for "GetValue" command.
@::Calc   = ('INPUT*FACTOR+OFFSET',
			 'INPUT*FACTOR+OFFSET',
			 'INPUT*FACTOR+OFFSET',
			 'INPUT*FACTOR+OFFSET');  ##Calculation.
@::Offset = (0, 0, 0, 0);                    ##Offset of calculation;
@::Factor = (1, 1, 1, 1);
@::Format = ('%.4f', '%.4f', '%.4f', '%.4f', );
@::Average= (1, 1, 1, 1);

}elsif(
$::NodeName eq 'er2c'
){###############################################################################
@::ChName  = qw(M2 G);

#STARS server
$::Server = 'localhost';

## For NPORT interface
#$::NPORT_HOST  = '192.168.2.32';   #NPort host name.
$::NPORT_HOST  = '192.168.156.123';   #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

$::DataLengthOption = 'L';                      #Counter data length, 'L' or 'l' is 10 degits, otherwize 7degits.

## Caluculatation for "GetValue" command.
@::Calc   = ('INPUT * FACTOR * -1 + OFFSET',
             'INPUT * FACTOR + OFFSET',
             'INPUT*FACTOR+OFFSET',
             'INPUT*FACTOR+OFFSET');       ##Calculation.
@::Offset = (0.508564, 1.0148, 0, 0);                    ##Offset of calculation;
@::Factor = (0.002/3600, 0.002/3600, 1, 1);

@::Format = ('%.6f', '%.6f', '%.4f', '%.4f', );
@::Average= (20, 20, 1, 1);

################################################################################
}else{
	die "Bad node name.";
}
1;

