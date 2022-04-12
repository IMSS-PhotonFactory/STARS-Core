#Configuration of ER4C-03A, ER2C-03A client.

if(
$::NodeName eq 'ly72'
){###############################################################################
@::ChName      = qw(X Y);

## Label Select 'ABC' or 'XYZ'
$::LabelSelect = 'ABC';

##STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = 'localhost';   #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

## Caluculatation for "GetValue" and "GetValueM" command.
#@::Calc   = ('',
#			 '',
#			 '');  ##Calculation.
@::Calc   = ('INPUT*FACTOR+OFFSET',
			 'INPUT*FACTOR+OFFSET',
			 'INPUT*FACTOR+OFFSET');  ##Calculation.
@::Offset = (0, 0, 0);                    ##Offset of calculation;
@::Factor = (1, 1, 1);
@::Format = ('%s', '%s', '%s');

}else{
	die "Bad node name.";
}
1;

