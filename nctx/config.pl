#Configuration of NCT08-01 Client.

if(
$::NodeName eq 'ct08'
){###############################################################################

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.100.151'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

#@::CounterName   = qw(C00 C01 C02 C03 C04 C05 C06 C07 TMR);

}elsif(
$::NodeName eq 'ct16'
){###############################################################################

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.100.151'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

#@::CounterName   = qw(C00 C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 TMR);

}elsif(
$::NodeName eq 'nct08'
){###############################################################################

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.100.151'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

#@::CounterName   = qw(C00 C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C30 C31 TMR);

}elsif(
$::NodeName eq 'ct48'
){###############################################################################

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.100.151'; #NPort host name.
$::NPORT_PORT  = 7777;             #NPort port number.

#@::CounterName   = qw(C00 C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C30 C31 C32 C33 C34 C35 C36 C37 C38 C39 C40 C41 C42 C43 C44 C45 C46 C47 TMR);

}else{
        die "Bad node name.";
}
1;
