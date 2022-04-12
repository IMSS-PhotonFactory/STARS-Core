#Windows RS-232 Interface
{
#require 5.003;
use Win32::SerialPort qw(:STAT 0.19);


sub device_init{
## Win32::SerialPort("COM1") 
	$::PortObj = new Win32::SerialPort("COM1") || die "Can't open : $^E\n";	
	$::PortObj->baudrate(9600);
	$::PortObj->parity("even");
	$::PortObj->databits(7);
	$::PortObj->stopbits(2);
	$::PortObj->handshake("none");

}


sub device_write{
	my $buf = shift;
	my $flgdel = shift;
	my $buf2 = '';
	if($flgdel){
		$::PortObj->write($buf);
	}else{
		$::PortObj->write("$buf\r\n");
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


sub device_read{
	my $buf='';
	my $buf2='';
	my $count=300;
	while(!($buf =~ /\n/)){
		$count--;
		unless($count){
			if($::Debug){print "Give up wating for LF!: ";}
			return('');
		}
		$buf2 = $::PortObj->input;
		if($buf2){
			$buf .= $buf2;
		}else{
			select(undef,undef,undef,0.02);
		}
	}
	if($::Debug){
		$buf2 = $buf;
		$buf2 =~ s/\n/(LF)/g;
		$buf2 =~ s/\r/(CR)/g;
		print "RCV->$buf2 [ ";
		for $buf2 (unpack("C*", $buf)){
			printf("%02X ", $buf2);
		}
		print "]\n";
	}
	$buf =~ s/[\r\n]+//g;
	return($buf);
}

}
1;
