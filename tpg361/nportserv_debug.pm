package nportserv;

use strict;
use IO::Socket;
use IO::Select;
################################################################
# Nport Server mode Perl Module Ver. 1.1 Takashi Kosuge        #
#    2013-10-08 (Tue)                                          #
################################################################
use constant RCVTIMEOUT        => 3;
use constant SIOMAXLENGTH      => 1024;


# Serial port ------------------------------------------------------
sub GetSIOHandle{
	my $this = shift;
	return($this->{sport});
}

sub OutSIO{
	my $this = shift;
	my $buf  = shift;
	my $fh   = $this->{sport};

print "S:" . join(",", unpack("H2" x length($buf), $buf)) . "\n";

	print $fh $buf;
	return(1);
}

sub InSIO{
	my $this = shift;
	my $timeout = shift;
	my $delimiter = shift;
	unless($timeout){$timeout=RCVTIMEOUT;}

	my $buf;
	my $bufrt;
	my $fh = $this->{sport};

	while($this->{spreadable}->can_read($timeout)){
		sysread($fh, $buf, SIOMAXLENGTH);

print "R:" . join(",", unpack("H2" x length($buf), $buf)) . "\n";

		unless($delimiter){
			return($buf);
		}
		$bufrt .= $buf;
		if($bufrt =~ s/$delimiter$//){
			return($bufrt);
		}
	}
	return('');
}


#New and destroy this module ------------------------------------------
sub DESTROY{
	my $this=shift;
	close($this->{sport});
}
#Usage: $object = nportserv->new('host', [SerialPort]);
sub new{
	my $class  = shift;
	my $npadr = shift;
	my $sp     = shift;

	my $spfh;

	unless($npadr){$npadr = '192.168.0.230';}
	unless($sp){$sp = 4001;}

#Open serial port
	unless($spfh = new IO::Socket::INET (PeerAddr => "$npadr"
										,PeerPort => $sp
										,Proto    => 'tcp')){return(undef);}
	select($spfh);$|=1;select(STDOUT);
	binmode($spfh);

	my $this = {};
	bless $this, $class;

	$this->{sport} = $spfh;
	$this->{spreadable} = IO::Select->new();
	$this->{spreadable}->add($spfh);

	return($this);
}

1;
