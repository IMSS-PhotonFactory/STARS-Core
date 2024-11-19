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
$::NPORT_BUFREMAIN='';

sub device_clearreadbuffer{
	$::NPORT_BUFREMAIN='';
}
sub device_read{
	my $timeout=shift;

	my $buf1;
	my $buf2='';
	my $rt;

	$buf2=$::NPORT_BUFREMAIN;
	if($timeout<=0){
		$timeout=TIMEOUT;
		if($::Debug){print "Read >";}
	}else{
		if($::Debug){print "Read($timeout)>";}
	}
	if($buf2 =~ s/([^\r\n]*)\r*\n//){
		$buf1=$1;
		$::NPORT_BUFREMAIN=$buf2;
		if($::Debug){print "REMAIN:$buf1\n";}
		return($buf1);
	}
	while(1){
#		unless(($ready) = $readable->can_read(TIMEOUT)){
		unless(($ready) = $readable->can_read($timeout)){
			if($::Debug){print "$buf2...Timeout\n";}
			$::Error = "Timeout";
			$::NPORT_BUFREMAIN='';
			return('');
		}
		
		unless($rt=sysread($sock,$buf1,512)){
			if($::Debug){print "$buf2...sysread error\n";}
			$::Error = "Unknown error";
			$::NPORT_BUFREMAIN='';
			return(undef);
		}
		$buf2 .= $buf1;
		if($buf2 =~ s/([^\r\n]*)\r*\n//){
			$buf1=$1;
			$::NPORT_BUFREMAIN=$buf2;
			last;
		}
	}
	if($::Debug){print "$buf1\n";}
	return($buf1);
}


sub device_write{
	my $buf = shift;
	my $flgdel = shift;

	if($::Debug){
		my $buf2 = $buf;
		$buf2 =~ s/\n/(LF)/g;
		$buf2 =~ s/\r/(CR)/g;
		print "Write>$buf2";
		if($flgdel){
			print "[";
			for $buf2 (unpack("C*", $buf)){
				printf("%02X ", $buf2);
			}
			print "]";
		}
		print "\n";
	}
	if($flgdel){
		print $sock "$buf";
	}else{
		print $sock "$buf\r\n";
#		print $sock "$buf\r";
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
	return($sock);
}

}
1;

