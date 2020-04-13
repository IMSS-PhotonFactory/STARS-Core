package stars;

#2001-10-03 Ver.1.2 Takashi Kosuge

use IO::Socket;
use Symbol;
use IO::Select;

%cbhandler=();
%cbmode=();
%cbbuf=();
@cbhandle=();

#Usage: $object->addcallback(subroutine, [filehandle], [mode]);
sub addcallback{
	my $this=shift;
	my $handler=shift;
	my $fh=shift;
	my $mode=shift;

	unless($fh){$fh=$this->{fh};}
	unless($mode){$mode='Stars';}
	unless($mode eq 'Direct' or $mode eq 'Lf' or $mode eq 'Stars' or $mode eq 'Detect'){
		$mode='Direct';
	}
	$cbhandler{$fh}=$handler;
	$cbmode{$fh}=$mode;
	$cbbuf{$fh}='';
	push(@cbhandle,$fh);
}

#Usage: stars->Mainloop([timeout]);
sub Mainloop{
	my $dummy=shift;
	my $handler=shift;
	my $timeout=shift;
	my $ready;
	my $rd;

	my $s;
	my $buf;

	$timeout /= 1000;
	unless($timeout){$timeout=undef;}

	my $rd=IO::Select->new;
	foreach $s (@cbhandle){$rd->add($s);}
	while(1){
		unless(($ready) = IO::Select->select($rd, undef, undef, $timeout)){
			if($handler ne ''){$handler->();}
			next;
		}
		foreach $s (@$ready){
			if($cbmode{$s} eq 'Detect'){
				$cbhandler{$s}->();
			}elsif(sysread($s, $buf, 512)){
				if($cbmode{$s} eq 'Direct'){
					$cbhandler{$s}->("$buf");
					next;
				}
				$cbbuf{$s} .= $buf;
				while($cbbuf{$s} =~ s/([^\r\n]*)\r*\n//){
					$buf=$1;
					if($cbmode{$s} eq 'Stars'){
unless($buf =~ s/^([a-zA-Z_0-9.\-]+)>([a-zA-Z_0-9.\-]+)\s*//){next;}
						$cbhandler{$s}->("$1","$2","$buf");
					}else{
						$cbhandler{$s}->("$buf");
					}
				}
			}else{
				delete $cbhandler{$s};
				delete $cbmode{$s};
				delete $cbbuf{$s};
#				$rd->remove($s);
				return(undef);
			}
		}
	}
}

#Usage: $object = stars->new(nodename, [serverhost], [serverport], [keyfile]);
sub new{
	my $class = shift;
	my ($nodename,$adr,$port,$keyfile)=@_;
	my $fh;
	my $rt;

	unless($adr){$adr='localhost';}
	unless($port){$port=<<DefaultPort>>;}
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
	$this->{timeout} = 10;
	return($this);
}

#Usage: $fh = $object->gethandle();
sub gethandle{
	my $this=shift;
	return($this->{fh});
}

#Usage: val/list = $object->Read();
sub Read{
	my $this=shift;
	my $timeout=shift;
	my $fh=$this->{fh};
	my $buf;
	my $readable = $this->{readable};
	my $ready;

  while(1){
	if($cbbuf{$fh} =~ s/([^\r\n]*)\r*\n//){
		$buf = $1;
		if(wantarray){
			unless($buf =~ s/^([a-zA-Z_0-9.\-]+)>([a-zA-Z_0-9.\-]+)\s*//){
				return(());
			}
			return("$1","$2","$buf");
		}
		return("$buf");
	}
	unless(($ready) = $readable->can_read(0.001)){
		if(wantarray){
			return('', '', '');
		}
		return('');
	}
	unless( sysread($fh, $buf, 512) ){return(undef)};
	$cbbuf{$fh} .= $buf;
  }
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
		sysread($fh,$buf1,512) or return(undef);
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

#Usage: $object->Send(message [, termto]);
sub Send{
	my $this=shift;
	my $cmd=shift;
	my $termto = shift;

	my $fh = $this->{fh};
	if($termto){
		print $fh "$termto $cmd\n";
	}else{
		print $fh "$cmd\n";
	}
}

#Usage: val/list = $object->act(message);
sub act{
	my $this=shift;
	my $cmd=shift;
	my $buf;

	$buf = $this->_SndRcv("$cmd");
	unless(defined($buf)){
		if(wantarray){return(());}else{return(undef);}
	}
	if(wantarray){
		$buf =~ s/^([a-zA-Z_0-9.\-]+)>([a-zA-Z_0-9.\-]+)\s*//;
		return("$1","$2","$buf");
	}
	return("$buf");
}

#Usage: $object->sleep(mSec);
sub Sleep{
	my $class = shift;
	my $stime=shift;
	$stime /= 1000;
	if($stime<0.001){return(undef)};
	select(undef,undef,undef,$stime);
}


1;
