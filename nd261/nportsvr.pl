#Nport server mode Interface
{
use IO::Socket;
use IO::Select;
#use constant HOST    => '192.168.0.232';
# to-> $::NPORT_HOST
#use constant PORT    => 4001;
# to-> $::NPORT_PORT

use constant TIMEOUT => 2;

my $sock;
my $readable;

sub device_read{
	my $buf1;
	my $buf2='';
	if($::Debug){print "Read >";}
	while(1){
		unless(($ready) = $readable->can_read(TIMEOUT)){
			if($::Debug){print "$buf2...Timeout\n";}
			$::Error = "Timeout";
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
	return($buf1);
}


sub device_write{
	my $buf = shift;
	my $flgdel = shift;
	my $buf2 = '';
	if($flgdel){
		print $sock "$buf";
	}else{
		print $sock "$buf\r\n";
	}
	if($::Debug){
		$buf2 = $buf;
		$buf2 =~ s/\n/(LF)/g;
		$buf2 =~ s/\r/(CR)/g;
		print "SND->$buf2 [ ";
		for $buf2 (unpack("C*", $buf)){
			printf("%02X ", $buf2);
		}
		print "]\n";
	}
	return(1)
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

