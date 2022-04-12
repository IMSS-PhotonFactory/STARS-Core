package karanetbox;

use strict;
use IO::Socket;
use IO::Select;
################################################################
# KARACRIX/NetBox-E100-BK1682A  Perl Module Ver. 1.0           #
#                                        Takashi Kosuge        #
#    2009-07-03                                                #
################################################################
# 2018-08-21 (Tue) Added 'Auto' in constructor.

use constant DEFAULTRCVTIMEOUT  => 3;
use constant DEFAULTEVNTTIMEOUT => 3;
use constant COMMANDMAXLENGTH   => 256;

my $FrameID = 0;
my $PrevInData = 0;

# Get from SWITCH-IN-16 ------------------------------------------
sub GetSw{
	my $this = shift;
	my $buf;
	my $rt = _SndRcvCommand($this, "din");
	if(wantarray){
		if($rt =~ /DIN ([01]{16}) /){
			return(split(//, $1));
		}else{
			return(());
		}
	}else{
		if($rt =~ /DIN ([01]{16}) /){
			return($1);
		}else{
			return(undef);
		}
	}
}


# Get Statur of Relay output -----------------------------------------
sub GetRy{
	my $this = shift;
	my $buf;
	my $rt = _SndRcvCommand($this, "din");
	if(wantarray){
		if($rt =~ /DIN [01]{16} ([01]{8}) /){
			return(split(//, $1));
		}else{
			return(());
		}
	}else{
		if($rt =~ /DIN [01]{16} ([01]{8}) /){
			return($1);
		}else{
			return(undef);
		}
	}
}

# Set Relay outoput -----------------------------------------------------
sub SetRy{
	my $this = shift;
	my $buf = shift;
	unless($buf =~ /^[01\-]{8}$/){return('Er: Bad value');}
	my $rt = _SndRcvCommand($this, "dout $buf");
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# Get Statur of Transistor output -----------------------------------------
sub GetTr{
	my $this = shift;
	my $buf;
	my $rt = _SndRcvCommand($this, "din");
	if(wantarray){
		if($rt =~ /DIN [01]{16} [01]{8} ([01]{2})/){
			return(split(//, $1));
		}else{
			return(());
		}
	}else{
		if($rt =~ /DIN [01]{16} [01]{8} ([01]{2})/){
			return($1);
		}else{
			return(undef);
		}
	}
}

# Set Transistor outoput -----------------------------------------------------
sub SetTr{
	my $this = shift;
	my $buf = shift;
	unless($buf =~ /^[01\-]{2}$/){return('Er: Bad value');}
	my $rt = _SndRcvCommand($this, "dout2 $buf");
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# Get counter -----------------------------------------
sub GetCnt{
	my $this = shift;
	my $buf;
	my $rt = _SndRcvCommand($this, "dcin");
	if($rt =~ /DCIN (.+)/){
		return(split(/ /, $1));
	}else{
		return(());
	}
}

# Preset counter --------------------------------------
sub PresetCnt{
	my $this = shift;
	my $ch = shift;
	my $val = shift;
	$ch=int($ch);
	if($ch<1 or $ch>16){return('Er: Bad channel');}
	$val=int($val);
	if($val<0 or $val>999999999){return('Er: Value is out of range');}
	my $rt = _SndRcvCommand($this, "di-cnt-set $ch $val");
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# Reset all counter --------------------------------------
sub ResetAllCnt{
	my $this = shift;
	my $rt = _SndRcvCommand($this, "di-cnt-all0-reset");
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# Get Digital input on Time hold Input ------------------------------
sub GetTim{
	my $this = shift;
	my $buf;
	my $rt = _SndRcvCommand($this, "dtin");
	if($rt =~ /DTIN (.+)/){
		return(split(/ /, $1));
	}else{
		return(());
	}
}

# Check Version etc. -----------------------------------------------
sub hello{
	return(Hello(shift));
}

sub Hello{
	my $this = shift;
	my $rt = _SndRcvCommand($this, "hello");
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# SendCommand -----------------------------------------------------
sub SendCommand{
	my $this = shift;
	my $cmd = shift;
	my $rt = _SndRcvCommand($this, $cmd);
	$rt =~ s/[\r\n]//g;
	return($rt);
}

# Receive event data -----------------------------------------------
sub ReceiveEvent{
	my $this = shift;
	my $timeout = shift;
	my $fh = $this->{eport};
	my $buf;
	my $nbuf;
	my @buf;
	unless($timeout){
		$timeout = $this->{etimeout};
	}
	if($this->{epreadable}->can_read($timeout)){
		sysread($fh, $buf, COMMANDMAXLENGTH);
		if($buf =~ / EVT ([0|1]{16}) /){
			$buf = reverse($1);
			@buf = unpack("CC", pack("B16", $buf));
			$nbuf = $buf[0] * 0x100 + $buf[1];
			if($PrevInData != $nbuf){
				$buf = $PrevInData ^ $nbuf;
				$PrevInData = $nbuf;
				return($nbuf, $buf);
			}
		}
	}
	return(());
}



# Get Frame ID -----------------------------------------------------
sub _GetFrameID{
	if($FrameID < 9999){
		$FrameID++;
	}else{
		$FrameID=0;
	}
	return(sprintf("%04d",$FrameID));
}


#==================================================================
sub _SndRcvCommand{
	my $this = shift;
	my $buf  = shift;
	my $timeout = shift;
	unless($timeout){
		$timeout = $this->{ctimeout};
	}

	my $fh = $this->{cport};
	my $fid = _GetFrameID();

	print $fh "$fid $buf";
	while($this->{cpreadable}->can_read($timeout)){
		sysread($fh, $buf, COMMANDMAXLENGTH);
		if($buf =~ s/^$fid //){
			return($buf);
		}
	}
	return(undef);
}




#New and destroy this module ------------------------------------------
sub DESTROY{
	my $this=shift;
	close($this->{cport});
}
#Usage: $object = karanetbox->new('Khost', [Kport], [LocalPort], [LocalEventPort]);
sub new{
	my $class   = shift;
	my $karadr  = shift;
	my $cp      = shift;
	my $lcp     = shift;
	my $lep     = shift;

	my $cpfh;
	my $epfh;

	unless($karadr){$karadr = '192.168.0.200';}
	unless($cp){$cp = 20000;}
	unless($lcp){$lcp = $cp;}

#Open control port
	if(uc($lcp) eq 'AUTO'){
		unless($cpfh = new IO::Socket::INET (PeerAddr => "$karadr"
											,PeerPort => $cp
											,Proto    => 'udp')){return(undef);}
	}else{
		unless($cpfh = new IO::Socket::INET (PeerAddr => "$karadr"
											,PeerPort => $cp
											,LocalPort => $lcp
											,Proto    => 'udp')){return(undef);}
	}


	select($cpfh);$|=1;select(STDOUT);
	binmode($cpfh);

#Open event port
	if($lep){
		unless($epfh = new IO::Socket::INET (PeerAddr => "$karadr"
											,LocalPort => $lep
											,Proto    => 'udp')){return(undef);}
		select($epfh);$|=1;select(STDOUT);
		binmode($epfh);
	}

	my $this = {};
	bless $this, $class;

	$this->{cport} = $cpfh;
	$this->{cpreadable} = IO::Select->new();
	$this->{cpreadable}->add($cpfh);
	$this->{ctimeout} = DEFAULTRCVTIMEOUT;

	if($lep){
		$this->{eport} = $epfh;
		$this->{epreadable} = IO::Select->new();
		$this->{epreadable}->add($epfh);
		$this->{etimeout} = DEFAULTEVNTTIMEOUT;
	}

	return($this);
}

1;
