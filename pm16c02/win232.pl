#Windows RS-232 Interface
{
#require 5.003;
use Win32::SerialPort qw(:STAT 0.19);


sub device_init{
## Win32::SerialPort("COM1") 
	$::PortObj = new Win32::SerialPort("COM1") || die "Can't open : $^E\n";	
	if($::Debug){$|=1;}
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
	my $bufdbg;
	my $count=300;
	if($::Debug){print "RCV->";}
	while(!($buf =~ /\n/)){
		$count--;
		unless($count){
			if($::Debug){print "Give up wating for LF!\n";}
			return('');
		}
		$buf2 = $::PortObj->input;
		if($buf2){
			$buf .= $buf2;
			if($::Debug){
				for $bufdbg (unpack("C*", $buf2)){
					if($bufdbg==0x0d){
						printf("(CR)");
					}elsif($bufdbg==0x0a){
						printf("(LF)");
					}elsif($bufdbg>0x7f and $bufdbg<0x20){
						printf(" ");
					}else{
						printf("%s",$bufdbg);
					}
					printf("[%02X] ", $bufdbg);
				}
			}
		}else{
			select(undef,undef,undef,0.02);
		}
	}
	if($::Debug){
		printf("\n");
	}
	$buf =~ s/[\r\n]+//g;
	return($buf);
}

}
1;
