#Configuration of CAENC111C.
if($::Debug){print "NodeName is $::NodeName\n";}

if($::NodeName eq "caenc111c"){

	$::Server="localhost";
	$::CAMAC_HOST="192.168.11.153";
	$::DISABLEINTERVAL=1;

	## Include CAEN C111C Module Stars Driver and Configuration
	require 'caenc111cmod.pl';
	CAENC111CRegister("$::NodeName","CAENC111C","1.0");
	
	## Include Kenetic Systems Model 3655-L1A Module Stars Driver and Configuration
	require 'ks3655l1amod.pl';
	KINETICSYSTEMS3655L1ARegister("$::NodeName.ks3655","23","CAENC111C","1.0");

	## Include CAEN C257 Module Stars Driver and Configuration
	require 'caenc257mod.pl';
	@::CAENC257CounterName=qw(C00 C01 C02 C03 C04 C05 C06 C07 C08 C09 C0A C0B C0C C0D C0E C0F);
	CAENC257Register("$::NodeName.c257A","22","$::NodeName","CAENC111C","1.0");

	## Include CAEN C257 Module Stars Driver and Configuration - for No. 2
	require 'caenc257mod.pl';
	@::CAENC257CounterName=qw(C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C1A C1B C1C C1D C1E C1F);
	CAENC257Register("$::NodeName.c257B","21","$::NodeName","CAENC111C","1.0");

	## Include CAEN C257 Module Stars Driver and Configuration - for No. 3
	require 'caenc257mod.pl';
	@::CAENC257CounterName=qw(C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C2A C2B C2C C2D C2E C2F);
	CAENC257Register("$::NodeName.c257C","20","$::NodeName","CAENC111C","1.0");

}else{die "Bad NodeName\n";}
1;