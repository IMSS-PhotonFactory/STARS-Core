package karacrix;

use strict;
use IO::Socket;
use IO::Select;
################################################################
# KARACRIX/IOB30RTA Perl Module Ver. 1.1 Takashi Kosuge        #
#    2011-07-06                                                #
################################################################
use constant RCVTIMEOUT        => 3;
use constant ALARMTIMEOUT      => 0.5;
use constant ALARMMAXLENGTH    => 128;
use constant COMMANDMAXLENGTH  => 256;
use constant SIOMAXLENGTH      => 512;

my $FrameID = 0;
# Get Frame ID -----------------------------------------------------
sub _GetFrameID{
	if($FrameID < 999){
		$FrameID++;
	}else{
		$FrameID=0;
	}
	return(sprintf("%04d",$FrameID));
}


# Alarm port -------------------------------------------------------
sub GetAlarmHandle{
	my $this = shift;
	unless($this->{aport}){return(undef);}
	return($this->{aport});
}

sub GetAlarm{
	my $this = shift;
	my $timeout = shift;
	unless($timeout){$timeout=ALARMTIMEOUT;}
	my $fh = $this->{aport};
	my $fha = $this->{cport};
	my $fid='';
	my $ip;
	my $buf;
	my $bufrt;

	if($this->{apreadable}->can_read($timeout)){
		sysread($fh, $buf, ALARMMAXLENGTH);
		($fid, undef, $ip, $bufrt) = split(" ", $buf);
		if($fid ne ''){
			print $fha _GetFrameID()." almack $fid";
			if(wantarray){
				return($bufrt, $ip, $fid);
			}else{
				return($bufrt);
			}
		}
	}
	return(undef);
}

sub SetAlarm{
	my $this = shift;
	my $buf  = shift;
	unless($this->{aport}){return(_SndRcvCommand($this, "alarm 0"));}
	if(lc($buf) eq 'difu'){
		return(_SndRcvCommand($this, "alarm 1"));
	}elsif(lc($buf) eq 'difd'){
		return(_SndRcvCommand($this, "alarm 2"));
	}else{
		return(_SndRcvCommand($this, "alarm 0"));
	}
}

# Serial port ------------------------------------------------------
sub GetSIOHandle{
	my $this = shift;
	return($this->{sport});
}

sub OutSIO{
	my $this = shift;
	my $buf  = shift;
	my $fh   = $this->{sport};
	print $fh $buf;
	return(1);
}

sub InSIO{
	my $this = shift;
	my $timeout = shift;
	unless($timeout){$timeout=RCVTIMEOUT;}

	my $buf;
	my $fh = $this->{sport};

	if($this->{spreadable}->can_read($timeout)){
		sysread($fh, $buf, COMMANDMAXLENGTH);
		return($buf);
	}
	return('');
}


#ADC ---------------------------------------------------------------
sub SetCal{
	my $this = shift;
	my $buf = shift;
	unless($buf){
		return(undef);
	}
	return(_SndRcvCommand($this, "setcal $buf"));
}

sub GetCal{
	my $this = shift;
	my $buf = _SndRcvCommand($this, 'getcal');
	unless($buf){return(undef);}
	if(wantarray){
		return(split(" ", $buf));
	}else{
		return($buf);
	}
}

sub Cal{
	my $this = shift;
	return(_SndRcvCommand($this, 'cal', 20));
}

sub Range{
	my $this = shift;
	my $buf = shift;
	unless($buf){
		$buf="24 24 24 24 24 24 24 24";
	}
	return(_SndRcvCommand($this, "range $buf"));
}

sub GetADC{
	my $this = shift;
	my $buf = _SndRcvCommand($this, 'ain');
	if(wantarray){
		return(split(" ", $buf));
	}else{
		return($buf);
	}
}

#Parallel port -----------------------------------------------------
sub OutPIO{
	my $this = shift;
	my $buf = shift;
	return(_SndRcvCommand($this, "bout $buf"));
}

sub InPIO{
	my $this = shift;
	my $buf = _SndRcvCommand($this, 'bin');
	unless($buf){return(undef);}
	unless($buf =~ /^BIN ([01]{4}) ([01]{4})$/){return(undef);}
	if(wantarray){
		return($1,$2);
	}else{
		return("$1 $2");
	}
}

#==================================================================
#Hello command
sub hello{
	my $this = shift;
	return(_SndRcvCommand($this, 'hello'));
}

sub _SndRcvCommand{
	my $this = shift;
	my $buf  = shift;
	my $timeout = shift;
	unless($timeout){$timeout=RCVTIMEOUT;}

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
	if($this->{aport}){close($this->{aport});}
	close($this->{cport});
	close($this->{sport});
}
#Usage: $object = karacrix->new('Khost', [CntlPort], [SerialPort], [AlarmPort]);
sub new{
	my $class  = shift;
	my $karadr = shift;
	my $cp     = shift;
	my $sp     = shift;
	my $ap     = shift;

	my $cpfh;
	my $spfh;
	my $apfh;

	unless($karadr){$karadr = '192.168.0.200';}
	unless($cp){$cp = 20000;}
	unless($sp){$sp = 20001;}
	unless($ap){$ap = 0;}

#Open control port
	if($cp > 0){
		unless($cpfh = new IO::Socket::INET (PeerAddr => "$karadr"
										,PeerPort => $cp
										,Proto    => 'udp')){return(undef);}
		select($cpfh);$|=1;select(STDOUT);
		binmode($cpfh);
	}

#Open serial port
	if($sp > 0){
		unless($spfh = new IO::Socket::INET (LocalPort=> $sp
										,PeerAddr => "$karadr"
										,PeerPort => $sp
										,Proto    => 'udp')){return(undef);}
		select($spfh);$|=1;select(STDOUT);
		binmode($spfh);
	}

#Open alarm port
	if($ap > 0){
		unless($apfh = new IO::Socket::INET (LocalPort=> $ap
										,PeerAddr => "$karadr"
										,Proto    => 'udp')){return(undef);}
		select($apfh);$|=1;select(STDOUT);
		binmode($apfh);
	}

	my $this = {};
	bless $this, $class;

	if($ap){
		$this->{aport} = $apfh;
		$this->{apreadable} = IO::Select->new();
		$this->{apreadable}->add($apfh);
	}

	$this->{cport} = $cpfh;
	$this->{cpreadable} = IO::Select->new();
	$this->{cpreadable}->add($cpfh);

	$this->{sport} = $spfh;
	$this->{spreadable} = IO::Select->new();
	$this->{spreadable}->add($spfh);

	return($this);
}

1;
