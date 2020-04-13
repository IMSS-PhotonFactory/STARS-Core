package picnic;

use strict;
use IO::Socket;
use IO::Select;
################################################################
# Picnic Perl Module Ver. 1.3 Takashi Kosuge                   #
#    2001-10-03                                                #
################################################################
use constant RCVTIMEOUT => 0.5;
use constant RCVRETRY   => 4;
##Control Display-----------------------------------------------
#Usage: @responce = $object->PrintLcd( 'Strings' );
sub PrintLcd{
	my $this = shift;
	my $mess = shift;
	my @mess;
	my $len;
	my @buf;

	if($mess eq ''){
		return(_SendToLcd($this,1,1));
	}

	@mess = split("\n", $mess);

	if(defined $mess[0] and $mess[0] ne ''){
		$len = length($mess[0]);
		@buf = unpack("C$len",$mess[0]);
		@buf = _SendToLcd($this, 1, 1, @buf);
		unless(@buf){return(());}
	}

	if(defined $mess[1] and $mess[1] ne ''){
		$len = length($mess[1]);
		@buf = unpack("C$len",$mess[1]);
		@buf = _SendToLcd($this, 1, 168, @buf);
		unless(@buf){return(());}
	}

	return((1));
}

#Usage: @responce = $object->SetLcd( mode );
sub SetLcd{
	my $this = shift;
	my $mode = shift;
	unless($mode >=0 and $mode <=7){return(());}
	$mode += 8;
	return(_SendToLcd($this,1,$mode));
}

sub _SendToLcd{
	my $this = shift;
	my (@buf) = @_;
	my $len = @buf;
	unless(defined $this->{lcdport}){
		return(());
	}
	my $fh = $this->{lcdport};
	my $buf = pack("C$len",@buf);
	my $try;
	for($try = 0; $try <= RCVRETRY; $try++){
		print $fh "$buf";
		if($this->{lcdreadable}->can_read(RCVTIMEOUT)){
			$len=sysread($fh, $buf, 128);
			return( unpack("C$len", $buf) );
		}
	}
	return(());
}


##Control Serial Port-------------------------------------------
#Usage: $fh  = $object->GetSIOHandle();
sub GetSIOHandle(){
	my $this = shift;
	return($this->{sport});
}

#Usage: $val = $object->InSIO();
sub InSIO{
	my $this = shift;
	my @header;
	my @data;
	my $len;
	my $buf='';
	my $rlen;

	unless((@header[0..15], @data) = _GetSerialResponse($this)){
		return('');
	}
	unless(@data){return('');}
	$rlen = $header[1] - 16;

	while(1){
		$len = @data;
		$buf .= pack("C$len", @data);
		if(length($buf) >= $rlen){last;}
		unless(@data = _GetSerialResponse($this)){
			return('');

		}
	}
	return("$buf");
}

#Usage: @responce = $object->OutSIO( 'Strings' );
sub OutSIO{
	my $this = shift;
	my $mess = shift;
	if($mess eq ''){return((1));}
	my $len = length($mess);
	my @buf = unpack("C$len",$mess);
	return(_SendToSerial($this, 3, @buf));
}

#Usage: @responce = $object->DefSIO( 'Baud', 'myIPaddress' );
sub DefSIO{
	my $this = shift;
	my $baud = shift;
	my $ip = shift;

	my %baud = (  '9600' => 129,
				 '19200' =>  64,
				 '38400' =>  32,
				 '57600' =>  21,
				'115200' =>  10);
	$baud = $baud{"$baud"};
	unless($baud){$baud = 129;}
	my @ip = split(/\./, $ip);

	unless(_SendToSerial($this, 2)){return(());}
	return(_SendToSerial($this, 1, @ip[0..3], $baud, 0));
}

sub _SendToSerial{
	my $this = shift;
	my (@buf) = @_;
	my $len = @buf;
	my $fh = $this->{sport};
	my $buf = pack("C$len",@buf);
	my $try;
	for($try = 0; $try <= RCVRETRY; $try++){
		print $fh "$buf";
		if($this->{spreadable}->can_read(RCVTIMEOUT)){
			$len=sysread($fh, $buf, 128);
			return( unpack("C$len", $buf) );
		}
	}
	return(());
}

sub _GetSerialResponse{
	my $this = shift;
	my $fh = $this->{sport};
	my $len;
	my $buf;
	unless($this->{spreadable}->can_read(RCVTIMEOUT * RCVRETRY)){
		return(());
	}
	$len=sysread($fh, $buf, 128);
	return( unpack("C$len", $buf) );
}


##Control Parallel IO ------------------------------------------

#Usage: $val = $object->InPIO( 'a|b' );
sub InPIO{
	my $this = shift;
	my $ch   = shift;

	my $och;
	my @rt;

	unless( @rt = _SendToParallel($this, 0)){return(undef);}
	if($ch eq 'a'){
		return($rt[0]);
	}else{
		return($rt[1]);
	}
}

#Usage: $val = $object->OutPIOW( 'a|b', io );
sub OutPIOW{
	my $this = shift;
	my $ch   = shift;
	my $val  = shift;
	my $och;
	my @rt;

	if($ch eq 'a'){
		$och = 5;
	}elsif($ch eq 'b'){
		$och = 6;
	}else{
		return(undef);
	}
	if($val < 0 or $val > 0xff){ return(undef);}

	unless( @rt = _SendToParallel($this, 3, $och, 1, 0, $val)){return(undef);}
	if($ch eq 'a'){
		return($rt[0]);
	}else{
		return($rt[1]);
	}
}

#Usage: $val = $object->OutPIO( 'a|b', Bit, 1|0 );
sub OutPIO{
	my $this = shift;
	my $ch   = shift;
	my $bit  = shift;
	my $val  = shift;
	my $och;
	my @rt;

	if($ch eq 'a'){
		$och = 5;
	}elsif($ch eq 'b'){
		$och = 6;
	}else{
		return(undef);
	}
	if($bit < 0 or $bit>7){ return(undef);}
	if($val == 0){
		@rt = _SendToParallel($this, 2, $och, $bit);
	}else{
		@rt = _SendToParallel($this, 1, $och, $bit);
	}
	unless( @rt ){return(undef);}
	if($ch eq 'a'){
		return($rt[0]);
	}else{
		return($rt[1]);
	}
}

#Usage: $tris = $object->DefPIOW( 'a|b', io );
sub DefPIOW{
	my $this = shift;
	my $ch   = shift;
	my $val  = shift;
	my $och;
	my @rt;

	if($ch eq 'a'){
		$och = 0x85;
	}elsif($ch eq 'b'){
		$och = 0x86;
	}else{
		return(undef);
	}
	if($val < 0 or $val > 0xff){ return(undef);}

	unless( @rt = _SendToParallel($this, 3, $och, 1, 0, $val)){return(undef);}
	if($ch eq 'a'){
		return($rt[2]);
	}else{
		return($rt[3]);
	}
}

#Usage: $tris = $object->DefPIO( 'a|b', Bit, 'i|o' );
sub DefPIO{
	my $this = shift;
	my $ch   = shift;
	my $bit  = shift;
	my $val  = shift;
	my $och;
	my @rt;

	if($ch eq 'a'){
		$och = 0x85;
	}elsif($ch eq 'b'){
		$och = 0x86;
	}else{
		return(undef);
	}
	if($bit < 0 or $bit>7){ return(undef);}
	if($val eq 'o'){
		@rt = _SendToParallel($this, 2, $och, $bit);
	}elsif($val eq 'i'){
		@rt = _SendToParallel($this, 1, $och, $bit);
	}else{
		return(undef);
	}
	unless( @rt ){return(undef);}
	if($ch eq 'a'){
		return($rt[2]);
	}else{
		return($rt[3]);
	}
}

#Usage: $calculated = $object->GetADCV( ADC_Ch [, Wait]);
sub GetADCV{
	my $this = shift;
	my $ch = shift;
	my $wait = shift;
	my $rt;
	$rt = GetADC($this, $ch, $wait);
	unless( defined($rt) ){ return(undef);}
	return(int( $rt/512 * 500 + 0.5) / 200);

}

#Usage: $direct = $object->GetADC( ADC_Ch [, Wait]);
sub GetADC{
	my $this = shift;
	my $ch = shift;
	my $wait = shift;
	my $sch = (0x81, 0x89, 0x91, 0x99, 0xa1)[$ch];
	my @rt;
	my $buf;
	unless($wait){$wait = 0;}
	if($wait>0xff or $wait<1){$wait = 0;}
	unless( @rt = _SendToParallel($this, 4, $sch, 0)){return(undef);}
	$buf = $rt[4] * 0x100 + $rt[5];
	return($buf);
}

#Usage: @list = $p->GetParallelStatus();
sub GetParallelStatus{
	my $this = shift;
	return( _SendToParallel($this, 0));
}

sub _SendToParallel{
	my $this = shift;
	my (@buf) = @_;
	my $len = @buf;
	my $fh = $this->{pport};
	my $buf = pack("C$len",@buf);
	my $try;
	for($try = 0; $try <= RCVRETRY; $try++){
		print $fh "$buf";
		if($this->{ppreadable}->can_read(RCVTIMEOUT)){
			$len=sysread($fh, $buf, 128);
			return( unpack("C$len", $buf) );
		}
	}
	return(());
}

#New and destroy this module ------------------------------------------
sub DESTROY{
	my $this=shift;
	if($this->{lcdport}){close($this->{lcdport});}
	close($this->{pport});
	close($this->{sport});
}
#Usage: $object = pinic->new('PicHost', [LCDPort], [PIOPort], [SerialPort]);
sub new{
	my $class = shift;
	my ($picadr, $lcdp, $pp, $sp)=@_;
	my $lcdfh;
	my $ppfh;
	my $spfh;

	unless($picadr){$picadr = 'localhost';}
	unless($pp){$pp = 10001;}
	unless($sp){$sp = 10002;}

#Open parallel port
	unless($ppfh = new IO::Socket::INET (PeerAddr => "$picadr"
										,PeerPort => $pp
										,Proto    => 'udp')){return(undef);}
	select($ppfh);$|=1;select(STDOUT);
	binmode($ppfh);

#Open serial port
	unless($spfh = new IO::Socket::INET (PeerAddr => "$picadr"
										,PeerPort => $sp
										,Proto    => 'udp')){return(undef);}
	select($spfh);$|=1;select(STDOUT);
	binmode($spfh);

#Open LCD port
	if($lcdp){
		unless($lcdfh = new IO::Socket::INET (PeerAddr => "$picadr"
										,PeerPort => $lcdp
										,Proto    => 'udp')){return(undef);}
		select($lcdfh);$|=1;select(STDOUT);
		binmode($lcdfh);
	}

	my $this = {};
	bless $this, $class;
	if($lcdp){
		$this->{lcdport} = $lcdfh;
		$this->{lcdreadable} = IO::Select->new();
		$this->{lcdreadable}->add($lcdfh);
	}

	$this->{pport} = $ppfh;
	$this->{ppreadable} = IO::Select->new();
	$this->{ppreadable}->add($ppfh);

	$this->{sport} = $spfh;
	$this->{spreadable} = IO::Select->new();
	$this->{spreadable}->add($spfh);

	return($this);
}

1;
