#Nport server mode Interface
{
use IO::Socket;
use IO::Select;
#use constant HOST    => '192.168.0.232';
# to-> $::NPORT_HOST
#use constant PORT    => 4001;
# to-> $::NPORT_PORT
use constant RWLOGMAX => 300;

use constant TIMEOUT => 2;

my $sock;
my $readable;


sub device_getlog{
	return(join("\t", @::RWlog));
}

sub device_setlog{
	my $buf=shift;
	if(@::RWlog >= RWLOGMAX){shift(@::RWlog);}
	push(@::RWlog, $buf);
}

sub device_read{
	my $buf1;
	my $buf2='';
	if($::Debug){print "Read >";}
	while(1){
		unless(($ready) = $readable->can_read(TIMEOUT)){
			if($::Debug){print "$buf2...Timeout\n";}
			$::Error = "Timeout";
			device_setlog("Read >$::Error");
			return('');
		}
		sysread($sock,$buf1,512) or return(undef);
		$buf2 .= $buf1;
		if($buf2 =~ s/([^\r\n]*)\r*\n//){
			$buf1=$1;
			last;
		}
	}
	if($::Debug){print "$buf1\n";}
	device_setlog("Read >$buf1");
	return($buf1);
}

sub device_write{
	my $buf=shift;
	if($::Debug){
		print "Write>$buf\n";
	}
	device_setlog("Write>$buf");
	print $sock "$buf\r\n";
	return(1);
}

sub device_init{
	$sock = new IO::Socket::INET(PeerAddr=>$::NPORT_HOST
                                   , PeerPort=>$::NPORT_PORT
                                   , Proto=>'tcp')
	||die "Socket: $!\n";
	select($sock); $|=1; select(STDOUT);
	$readable = IO::Select->new;
	$readable->add($sock);
}

}
1;

