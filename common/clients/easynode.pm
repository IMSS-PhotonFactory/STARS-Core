package easynode;

use IO::Socket;
use Symbol;
use IO::Select;


sub new{
	my $class = shift;
	my ($nodename,$adr,$port,$keyfile)=@_;
	my $fh;
	my $rt;

	unless($adr){$adr='localhost';}
	unless($port){$port=6057;}
	unless($keyfile){$keyfile = "$nodename.key";}
	unless($fh = new IO::Socket::INET (PeerAddr => "$adr"
										,PeerPort => $port
										,Proto    => 'tcp')){return(undef);}
	select($fh);$|=1;select(STDOUT);
	binmode($fh);

##---get keynumber from file
	my $keynumber;
	my $keyval='';
	my $kcount=0;
	my $lp;
	my $hd = gensym();
	$keynumber=<$fh>;chomp($keynumber);$keynumber=~s/\r//;

	unless(open($hd, "$keyfile")){
		close($fh); return(undef);
	}
	while(<$hd>){$kcount++;}
	unless($kcount){close($hd); close($fh); return(undef);}

	$kcount = $keynumber % $kcount;
	seek($hd, 0, 0);
	for($lp=0; $lp < $kcount; $lp++){$_=<$hd>;}
	$_=<$hd>;
	chomp;s/\r//;
	close($hd);
#---------------------
	print $fh "$nodename $_\n";
	$rt=<$fh>;chop($rt);$rt=~s/\r//;
	unless($rt =~ /Ok:/){
#		print $fh "quit\n";
		close($fh);
		return(undef);
	}
	my $this = {};
	bless $this, $class;
	$this->{fh}=$fh;
	$this->{readable} = IO::Select->new();
	$this->{readable}->add($fh);
	$this->{timeout} = 3;
	return($this);
}

sub gethandle{
	my $this=shift;
	return($this->{fh});
}

sub read{
	my $this=shift;
	my $fh=$this->{fh};
	my $buf;
	$buf=<$fh>;chomp($buf);$buf =~ s/\r//;
	unless($buf =~ s/^([a-zA-Z_0-9.\-]+)>[a-zA-Z_0-9.\-]+\s*//){
		return(undef);
	}
	return("$1","$buf");
}

sub _SndRcv{
	my $this=shift;
	my $cmd=shift;
	my $ready;

	my $buf1;
	my $buf2='';
	my $readable = $this->{readable};
	my $fh = $this->{fh};
	my $timeout = $this->{timeout};

	if($cmd ne ''){
		print $fh "$cmd\n";
	}

	while(1){
		unless(($ready) = $readable->can_read($timeout)){
			$::Error = "Timeout";
			return('');
		}
		sysread($fh,$buf1,128);
		$buf2 .= $buf1;
		if($buf2 =~ s/([^\r\n]*)\r*\n//){
			$buf1=$1;
			last;
		}

	}
	return($buf1);
}

sub DESTROY{
	my $this=shift;
	my $fh = $this->{fh};
	print $fh "quit\n";
	close($fh);
}

sub send{
	my $this=shift;
	my $cmd=shift;
	my $fh = $this->{fh};
	print $fh "$cmd\n";
}

sub act{
	my $this=shift;
	my $cmd=shift;
	return($this->_SndRcv("$cmd"));
}

#sub geterror{
#	my $this=shift;
#	return($this->_SndRcv("geterror"));
#}

1;
