package caenc111c;

#CAMAC-C111C interface module
#2006-07-31 Ver.1.0 Yasuko Nagatani

use constant CRATE_OK=>0;
use constant CRATE_ERROR=>-1;
use constant CRATE_CONNECT_ERROR=>-2;
use constant CRATE_IRQ_ERROR=>-3;
use constant CRATE_BIN_ERROR=>-4;
use constant CRATE_CMD_ERROR=>-5;
use constant CRATE_ID_ERROR	=>-6;
use constant CRATE_MEMORY_ERROR=>-7;

use constant STX=>0x2;
use constant ETX=>0x4;
use constant STUFF=>0x10;
use constant BIN_CFSA_CMD=>0x20;
use constant BIN_CSSA_CMD=>0x21;
use constant BIN_CCCZ_CMD=>0x22;
use constant BIN_CCCC_CMD=>0x23;
use constant BIN_CCCI_CMD=>0x24;
use constant BIN_CTCI_CMD=>0x25;
use constant BIN_CTLM_CMD=>0x26;
use constant BIN_CCLWT_CMD=>0x27;
use constant BIN_LACK_CMD=>0x28;
use constant BIN_CTSTAT_CMD=>0x29;
use constant BIN_CLMR_CMD =>0x2A;
use constant BIN_CSCAN_CMD=>0x2B;
use constant BIN_NIM_SETOUTS_CMD=>0x30;
use constant NO_BIN_RESPONSE=>0xA0;

use constant OP_BLKSS=>0x0;
use constant OP_BLKFS=>0x1;
use constant OP_BLKSR=>0x2;
use constant OP_BLKFR=>0x3;
use constant OP_BLKSA=>0x4;
use constant OP_BLKFA=>0x5;

use strict;
use IO::Socket;
use Symbol;
use IO::Select;

#////////////////////////////////////////////
#//
#//	Socket helper functions implementation
#//
#////////////////////////////////////////////
$C111C::fh2='';
$C111C::readable2='';
$C111C::irq_callback='';
$C111C::irq_tid='';
#Usage: $object = C111C->new(serverhost,[openport]);
sub new{
	my $class = shift;
	my ($adr,$openport)=@_;
	my @fh=();
	my $i;
	my $port=2000;
	if($openport eq ''){@fh=(1,1,1);
	}elsif($openport=~/^([01])([01])([01])$/){@fh=($1,$2,$3);
	}elsif($openport=~/^000$/){return(undef);
	}else{return(undef);}
	
	for($i=0;$i<=2;$i++){
		if($fh[$i] eq 1){
			if($::Debug){printf("CAMAC Controller Address: $adr Port: %d\n",$port+$i);}
			$fh[$i]='';
			unless($fh[$i]=new IO::Socket::INET (PeerAddr => "$adr"
						,PeerPort => $port+$i, Proto => 'tcp')){return(undef);}
			select($fh[$i]);$|=1;select(STDOUT);binmode($fh[$i]);
		}
	}
	my $this={};
	bless $this, $class;
	if($fh[0]){
		$this->{fh0}=$fh[0];
		$this->{readable0} = IO::Select->new();
		$this->{readable0}->add($fh[0]);
	}
	if($fh[1]){
		$this->{fh1}=$fh[1];
		$this->{readable1} = IO::Select->new();
		$this->{readable1}->add($fh[1]);
	}
	if($fh[2]){
		$C111C::fh2=$fh[2];
		$C111C::readable2 = IO::Select->new();
		$C111C::readable2->add($fh[2]);
		$C111C::irq_callback = '';
		$C111C::irq_tid = 0;
	}
	$this->{no_bin_resp} = 0;
	$this->{tout_mode} = 0;
	$this->{tout_ticks} = 0;
	$this->{connected} = 1;

	return($this);
}
#Usage: $object->Send(message [, termto]);
sub Send{
	my $this=shift;
	my $no=shift;
	my $cmd=shift;
	my $size=shift;
	my $fh = $this->{"fh$no"};

	if($no eq 0){
		if($::Debug){print "Send ->$cmd\n"};
		print $fh "$cmd";
	}elsif($no eq 1){
		if($::Debug){print "Send ->"};
		$this->BIN_ShowData($cmd,$size);
		return(syswrite($fh,$cmd,$size));
	}
	return($size);
}
sub DESTROY{
	my $this=shift;
	if($this->{fh0}){close($this->{fh0});}
	if($this->{fh1}){close($this->{fh1});}
	if($C111C::fh2){close($C111C::fh2);}
	$this->{connected} = 0;
	$C111C::fh2='' ;$C111C::readable2='';
	$C111C::irq_callback='';
	$C111C::irq_tid='';
}
#////////////////////////////////////////////
#//
#//	Private Function implementation
#//
#////////////////////////////////////////////
#Usage: $object->BIN_ShowData(binmesg,msgsize);
sub BIN_ShowData{
	my $this=shift;
	my($bin_buf,$size)=@_;
	my $i;
	if($::Debug){
		for ($i=0;$i<$size;$i++){
			printf("%02x ",unpack("x".$i."C",$bin_buf));
		}
		printf("\n");
	}
	return(1);
}
#Usage: val/list = $object->BIN_Response(msgsize);
sub BIN_Response{
	my $this=shift;
	my $size=shift;
	my $fh=$this->{fh1};
	my $timeout=$this->{tout_ticks};
	my $readable=$this->{readable1};
	my $ready;
	my($b,$c);
	my $buf='';
	my($pos,$stuff,$etx_found)=(0,0,0);

	if($timeout<=0){$timeout=0.001;}
	while($etx_found eq 0) {
		unless(($ready)=$readable->can_read($timeout)){
			if($timeout!=0.001){$::Error = "Timeout";last;}
		}
		unless(sysread($fh, $b, 1)){print "sysread()?\n";last;}
		$c=unpack("C",$b);
#		printf("rcv:%x\n",$c);
		if ($c eq STX){
			$pos=0; $stuff=0;
			$buf=$b; $pos++;
		}elsif($pos){
			if($c eq STUFF) {
				$stuff=1;
			}elsif($c eq ETX){
				$buf.=$b; $pos++;
				$etx_found=1;
			}else{
				if($pos<$size){
					if($stuff){$buf.=pack("C",$c-0x80); $pos++;}
					else{$buf.=$b; $pos++;}
				}
				$stuff=0;
			}
		}
	}
	if($::Debug){print "Rcv ->";}
	$this->BIN_ShowData($buf, $pos);
	if(wantarray){return($pos,$buf);}
	return("$pos $buf");
}
#Usage: val/list = $object->BIN_AdjustFrame(binmesg,$length,$frompos,$topos);
sub BIN_AdjustFrame{
	my $this=shift;
	my $buff=shift;
	my $totallen=shift;
	my $offset=shift;
	my $length=shift;
    my($i,$c);
	my @s=();

	for($i=0;$i<$offset;$i++){
		$c=unpack("x".$i."C",$buff);
		push(@s,$c);
	}
	for(;$i<=$length;$i++){
		$c=unpack("x".$i."C",$buff);
		if($c eq STX) {
			push(@s,STUFF);
			push(@s,0x80|STX);
		}elsif($c eq ETX) {
			push(@s,STUFF);
			push(@s,0x80|ETX);
		}elsif($c eq STUFF) {
			push(@s,STUFF);
			push(@s,0x80|STUFF);
		}else{
			push(@s,$c);
		}
    }
	for(;$i<$totallen;$i++){
		push(@s,unpack("x".$i."C",$buff));
	}
	my $bin_cmd=pack("C".scalar(@s),@s);
	if(wantarray){return(scalar(@s),$bin_cmd);}
	return(scalar(@s)." $bin_cmd");
}
#Usage: val/list = IRQ_Handler;
sub IRQ_Handler{
	my $resp="A\r";
	my $fh=$C111C::fh2;
	my $timeout=$C111C::irq_tid;
	my $readable=$C111C::readable2;
	my $ready;
	my $cmd;

	if($timeout<=0){$timeout=0.001;}
	while(1){ # Not Loop
		unless(($ready)=$readable->can_read($timeout)){return;}
		unless(sysread($fh, $cmd, 255)){print "sysread()?\n";return;}
		if($::Debug){print "IRQ GET->$cmd\n";}
		if($cmd=~/^(L|C|D).(\S\S\S\S\S\S\S\S)/){
			my $irq_cmd=$1;my $irq_data=$2;
			if($C111C::irq_callback ne '') {
				$C111C::irq_callback->($irq_cmd, $irq_data);
			}
	    }
		if($::Debug){print "IRQ RES ->$resp\n";}
		print $fh "$resp";
#		syswrite($fh,$resp,2);
#		if(return is ERROR){return(CRATE_BIN_ERROR);}
		last;
    }
    return(CRATE_OK);                    
}
#////////////////////////////////////////////
#//	Config Function implementation
#////////////////////////////////////////////
sub CRTOUT{
	my $this=shift;
	my $timeout=shift;
	if($timeout>0){$this->{tout_ticks}=0;}
	return(CRATE_OK);
}
sub CRIRQ{
	my $this=shift;
	my $handler=shift;
	my $timeout=shift;
	$C111C::irq_callback=$handler;
	if($timeout>0){$C111C::irq_tid=$timeout;
	}elsif($timeout ne ''){$C111C::irq_tid=0;}
	return(CRATE_OK);
}
sub CBINR{
	my $this=shift;
	my $enable_resp=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	if($enable_resp){
		$this->{no_bin_resp}=0;
	}else{
		$this->{no_bin_resp}=NO_BIN_RESPONSE;
	}
	return(CRATE_OK);
}

#/////////////////////////////////////////////
#//
#//	ESONE Function implementation
#//
#/////////////////////////////////////////////
##########################################
# CFSA -> Executes a 24-bit CAMAC command
#         returns Q, X and DATA
##########################################
sub CFSA{
	my $this=shift;
	my($F,$N,$A,$DATA)=@_;
	my @bin_cmds=(STX,BIN_CFSA_CMD,$F,$N,$A
	        ,$DATA & 0xFF,($DATA>>8) & 0xFF,($DATA>>16) & 0xFF
	        ,$this->{no_bin_resp},ETX);
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C10",@bin_cmds);
	my $msgsize;
	($msgsize,$bin_cmd)=$this->BIN_AdjustFrame($bin_cmd, 10,2,7);
	my($Q,$X)=(0,0);
	if($this->Send(1,$bin_cmd,$msgsize) <= 0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my $bin_rcv='';
		($msgsize,$bin_rcv)=$this->BIN_Response(8);
		if($msgsize ne 8){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_CFSA_CMD)){return(CRATE_BIN_ERROR);}
		$Q    = unpack("x2C",$bin_rcv);
		$X    = unpack("x3C",$bin_rcv);
		$DATA = unpack("x4C",$bin_rcv) | (unpack("x5C",$bin_rcv) << 8) | (unpack("x6C",$bin_rcv) << 16);
	}
	if(wantarray){return(CRATE_OK,$Q,$X,$DATA);}
	return(printf("%d %d %d %d",CRATE_OK,$Q,$X,$DATA));
}
##########################################
# CSSA -> Executes a 16-bit CAMAC command
#         returns Q, X and DATA
##########################################
sub CSSA{
	my $this=shift;
	my($F,$N,$A,$DATA)=@_;
	my @bin_cmds=(STX,BIN_CSSA_CMD,$F,$N,$A
	        ,$DATA & 0xFF,($DATA>>8) & 0xFF
	        ,$this->{no_bin_resp},ETX);
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C9",@bin_cmds);
	my $msgsize;
	($msgsize,$bin_cmd)=$this->BIN_AdjustFrame($bin_cmd, 9,2,6);
	my($Q,$X)=(0,0);
	if($this->Send(1,$bin_cmd,$msgsize)<=0){return(CRATE_BIN_ERROR);}
	
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my $bin_rcv='';
		($msgsize,$bin_rcv)=$this->BIN_Response(7);
		if($msgsize ne 7){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_CSSA_CMD)){return(CRATE_BIN_ERROR);}
		$Q    = unpack("x2C",$bin_rcv);
		$X    = unpack("x3C",$bin_rcv);
		$DATA = unpack("x4C",$bin_rcv) | (unpack("x5C",$bin_rcv) << 8);
	}
	if(wantarray){return(CRATE_OK,$Q,$X,$DATA);}
	return(printf("%d %d %d %d",CRATE_OK,$Q,$X,$DATA));
}
################################
# CCCZ -> Generate Dataway Init
################################
sub CCCZ{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",STX,BIN_CCCZ_CMD,$this->{no_bin_resp},ETX);
	if($this->Send(1,$bin_cmd,4)<=0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my($msgsize,$bin_rcv)=$this->BIN_Response(3);
		if($msgsize ne 3){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_CCCZ_CMD)){return(CRATE_BIN_ERROR);}
	}
	return(CRATE_OK);
}
###############################
# CCCC -> Generate Crate Clear
###############################
sub CCCC{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",STX,BIN_CCCC_CMD,$this->{no_bin_resp},ETX);
	if($this->Send(1,$bin_cmd,4)<=0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my($msgsize,$bin_rcv)=$this->BIN_Response(3);
		if($msgsize ne 3){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_CCCC_CMD)){return(CRATE_BIN_ERROR);}
	}
	return(CRATE_OK);
}
####################################################
# CCCI -> Change Dataway Inhibit to specified value
#         data_in can be 0 or 1
####################################################
sub CCCI{
	my $this=shift;
	my $data_in=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C5",STX,BIN_CCCI_CMD,$data_in,$this->{no_bin_resp},ETX);
	if($this->Send(1,$bin_cmd,5)<=0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my($msgsize,$bin_rcv)=$this->BIN_Response(3);
		if($msgsize ne 3){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_CCCI_CMD)){return(CRATE_BIN_ERROR);}
	}
	return CRATE_OK;
}
#############################################
# CTCI -> CAMAC test Inhibit; returns 0 or 1
#############################################
sub CTCI{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C3",STX,BIN_CTCI_CMD,ETX);
	if($this->Send(1,$bin_cmd,3)<=0){return(CRATE_BIN_ERROR);}
	my($msgsize,$bin_rcv)=$this->BIN_Response(4);
	if($msgsize ne 4){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CTCI_CMD)){return(CRATE_BIN_ERROR);}
	my $DATA = unpack("x2C",$bin_rcv);
	if(wantarray){return(CRATE_OK,$DATA);}
	return(printf("%d %d",CRATE_OK,$DATA));
}
###################################################
# CTLM -> CAMAC test LAM on specified slot = 1..23
#  if slot = 0xFF perform a test for any LAM event
###################################################
sub CTLM{
	my $this=shift;
	my $slot=shift;
	my @bin_cmds=(STX,BIN_CTLM_CMD,$slot,ETX);
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",@bin_cmds);
	my $msgsize;
	($msgsize,$bin_cmd)=$this->BIN_AdjustFrame($bin_cmd, 4,2,2);
	if($this->Send(1,$bin_cmd,$msgsize)<=0){return(CRATE_BIN_ERROR);}
	my $bin_rcv;
	($msgsize,$bin_rcv)=$this->BIN_Response(4);
	if($msgsize ne 4){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CTLM_CMD)){return(CRATE_BIN_ERROR);}
	my $DATA = unpack("x2C",$bin_rcv);
	if(wantarray){return(CRATE_OK,$DATA);}
	return(printf("%d %d",CRATE_OK,$DATA));
}
################################################
# CCLWT -> CAMAC wait for LAM on specified slot
#    if N = -1 perform a wait for any LAM event
################################################
sub CCLWT{
	my $this=shift;
	my $slot=shift;
	my @bin_cmds=(STX,BIN_CCLWT_CMD,$slot,ETX);
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",@bin_cmds);
	my $msgsize;
	($msgsize,$bin_cmd)=$this->BIN_AdjustFrame($bin_cmd, 4,2,3);
	if($this->Send(1,$bin_cmd,$msgsize)<=0){return(CRATE_BIN_ERROR);}
	my $bin_rcv;
	($msgsize,$bin_rcv)=$this->BIN_Response(3);
	if($msgsize ne 3){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CCLWT_CMD)){return(CRATE_BIN_ERROR);}
	return(CRATE_OK);
}
#############################################################
# CTSTAT -> Returns Q and X values (from last access on bus)
#############################################################
sub CTSTAT{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",STX,BIN_CTSTAT_CMD,ETX);
	if($this->Send(1,$bin_cmd,4)<=0){return(CRATE_BIN_ERROR);}
	my($msgsize,$bin_rcv)=$this->BIN_Response(5);
	if($msgsize ne 5){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CTSTAT_CMD)){return(CRATE_BIN_ERROR);}
	my $Q = unpack("x2C",$bin_rcv);
	my $X = unpack("x3C",$bin_rcv);
	if(wantarray){return(CRATE_OK,$Q,$X);}
	return(printf("%d %d %d",CRATE_OK,$Q,$X));
}
###############################################
# CLMR -> Returns current LAM register, in hex
###############################################
sub CLMR{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C3",STX,BIN_CLMR_CMD,ETX);
	if($this->Send(1,$bin_cmd,3)<=0){return(CRATE_BIN_ERROR);}
	my($msgsize,$bin_rcv)=$this->BIN_Response(7);
	if($msgsize ne 7){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CLMR_CMD)){return(CRATE_BIN_ERROR);}
	my $DATA = unpack("x2C",$bin_rcv) | (unpack("x3C",$bin_rcv) << 8)
	            | (unpack("x4C",$bin_rcv) << 16) | (unpack("x5C",$bin_rcv) << 24);
	if(wantarray){return(CRATE_OK,$DATA);}
	return(printf("%d %d",CRATE_OK,$DATA));
}
##############################################
# CSCAN -> Returns current slot filled in hex
##############################################
sub CSCAN{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C3",STX,BIN_CSCAN_CMD,ETX);
	if($this->Send(1,$bin_cmd,3)<=0){return(CRATE_BIN_ERROR);}
	my($msgsize,$bin_rcv)=$this->BIN_Response(7);
	if($msgsize ne 7){return(CRATE_BIN_ERROR);}
	my $buf=unpack("x1C",$bin_rcv);
	if(($buf ne BIN_CSCAN_CMD)){return(CRATE_BIN_ERROR);}
	my $DATA = unpack("x2C",$bin_rcv) | (unpack("x3C",$bin_rcv) << 8)
	            | (unpack("x4C",$bin_rcv) << 16) | (unpack("x5C",$bin_rcv) << 24);
	if(wantarray){return(CRATE_OK,$DATA);}
	return(printf("%d %d",CRATE_OK,$DATA));
}
#####################################
# LACK -> Performs a LAM Acknowledge
#####################################
sub LACK{
	my $this=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C4",STX,BIN_LACK_CMD,$this->{no_bin_resp} & 0xFF,ETX);
	if($this->Send(1,$bin_cmd,4)<=0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my($msgsize,$bin_rcv)=$this->BIN_Response(3);
		if($msgsize ne 3){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_LACK_CMD)){return(CRATE_BIN_ERROR);}
	}
	return(CRATE_OK);
}
#/////////////////////////////////////////////
#//
#//	NIM Function implementation
#//
#/////////////////////////////////////////////
##################################
# NOSOS -> Nim Out Set Out Single
##################################
sub NOSOS{
	my $this=shift;
	my $nimo=shift;
	my $value=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my $bin_cmd=pack("C6",STX,BIN_NIM_SETOUTS_CMD
					    ,$nimo,$value,$this->{no_bin_resp},ETX);
	my $msgsize;
	($msgsize,$bin_cmd)=$this->BIN_AdjustFrame($bin_cmd, 6,2,3);
	my($Q,$X)=(0,0);
	if($this->Send(1,$bin_cmd,$msgsize)<=0){return(CRATE_BIN_ERROR);}
	if($this->{no_bin_resp} ne NO_BIN_RESPONSE) {
		my $bin_rcv='';
		($msgsize,$bin_rcv)=$this->BIN_Response(3);
		if($msgsize ne 3){return(CRATE_BIN_ERROR);}
		my $buf=unpack("x1C",$bin_rcv);
		if(($buf ne BIN_NIM_SETOUTS_CMD)){return(CRATE_BIN_ERROR);}
	}
	return(CRATE_OK);
}
#////////////////////////////////////////////
#//
#//	CMD Function implementation
#//
#////////////////////////////////////////////
sub CMD_Response{
	my $this=shift;
	my $size=shift;
	my $timeout=shift;
	my $fh=$this->{fh0};
	my $readable=$this->{readable0};
	my $ready;
	my $msgsize=0;
	my $recnum=0;
	my $retmsg='';
	my $retbuf='';
	if($timeout eq ''){
		$timeout=$this->{tout_ticks};
	}
	if($timeout<=0){$timeout=0.1;}
	if($size<=0){$size=255;}
	while(1){
		unless(($ready)=$readable->can_read($timeout)){
			if($timeout!=0.1){$::Error = "Timeout";last;}
		}
		$timeout=0;
		$retbuf='';
		unless(($recnum)=sysread($fh,$retbuf,$size)){print "sysread()?\n";last;}
		$msgsize+=$recnum;
		$retmsg=$retmsg.$retbuf;
	}
	if($::Debug){
		$retbuf=$retmsg;
		$retbuf=~s/\r/\n/g;
		print "Rcv ->$msgsize $retbuf\n";
	}
	if(wantarray){return($msgsize,$retmsg);}
	return("$msgsize $retmsg");
}
#############################
# CMDS -> Send Ascii Command
#############################
sub CMDS{
	my $this=shift;
	my $cmd=shift;
	my $size=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	if($this->Send(0,$cmd,$size)<=0){return(CRATE_CMD_ERROR);}
	return(CRATE_OK);
}
################################
# CMDR -> Receive Ascii Command
################################
sub CMDR{
	my $this=shift;
	my $size=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	my($msgsize,$retmsg)=$this->CMD_Response($size);
	return($msgsize,$retmsg);
}
#############################
# CMDSR -> Ascii Act Command
#          returns RCVDATA
#############################
sub CMDSR{
	my $this=shift;
	my $cmd=shift;
	my $size=shift;
	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	if($this->Send(0,"$cmd\r",$size+1)<=0){return(CRATE_CMD_ERROR);}
	my($msgsize,$retmsg)=$this->CMD_Response($size);
	return($msgsize,$retmsg);
}
#######################################################
# BLKBUFFS -> Block Transfer buffer size set(07/07/27)
#          returns 0 if success
#######################################################
sub BLKBUFFS{
	my $this=shift;
	my $value=shift;
	if($value<1 or $value>256){return(CRATE_CMD_ERROR);}
	my $cmd=sprintf("BLKBUFFS %d", $value);
	my($msgsize,$retmsg)=$this->CMDSR($cmd,255);
	return($msgsize,$retmsg);
}
#######################################################
# BLKBUFFG -> Block Transfer buffer size get(07/07/27)
#          returns size if success
#######################################################
sub BLKBUFFG{
	my $this=shift;
	my $cmd="BLKBUFFG";
	my($msgsize,$retmsg)=$this->CMDSR($cmd,255);
	return($msgsize,$retmsg);
}
#######################################################
# BLKTRANSF -> Block Transfer(07/07/27)
#######################################################
sub BLKxS{
	my $this=shift;
	my($binflg,$x,$F,$N,$A,$maxsize,$blksize,$outbuf)=(shift,uc(shift),shift,shift,shift,shift,shift,shift);
	my $opcode=OP_BLKFS;
	if($x eq 'S'){$opcode=OP_BLKSS;}
	my($retcode,$retmsg)=$this->BLKTRANSF($binflg,$opcode,$F,$N,$A,$maxsize,"",$blksize,$outbuf);
	return($retcode,$retmsg);
}
#---------------------------------------------
sub BLKxR{
	my $this=shift;
	my($binflg,$x,$F,$N,$A,$maxsize,$timeout,$blksize,$outbuf)=(shift,uc(shift),shift,shift,shift,shift,shift,shift,shift);
	my $opcode=OP_BLKFR;
	if($x eq 'S'){$opcode=OP_BLKSR;}
	my($retcode,$retmsg)=$this->BLKTRANSF($binflg,$opcode,$F,$N,$A,$maxsize,$timeout,$blksize,$outbuf);
	return($retcode,$retmsg);
}
#---------------------------------------------
sub BLKxA{
	my $this=shift;
	my($binflg,$x,$F,$N,$maxsize,$blksize,$outbuf)=(shift,uc(shift),shift,shift,shift,shift,shift);
	my $opcode=OP_BLKFA;
	if($x eq 'S'){$opcode=OP_BLKSA;}
	my($retcode,$retmsg)=$this->BLKTRANSF($binflg,$opcode,$F,$N,"",$maxsize,"",$blksize,$outbuf);
	return($retcode,$retmsg);
}
#---------------------------------------------
sub BLKTRANSF{
	my $this=shift;
	my($binflg,$opcode,$F,$N,$A,$totsize,$timeout,$blksize)=(shift,shift,shift,shift,shift,shift,shift,shift);
	my($output)=(shift);
	my($msgsize,$retmsg,$sendmsg);

	if($this->{connected} eq 0){return(CRATE_CONNECT_ERROR);}
	if($totsize<=0){return(CRATE_CMD_ERROR,"Invalid maxsize [$totsize].");}
	if($blksize eq ""){
		($msgsize,$retmsg)=$this->BLKBUFFG();
		if($msgsize<=0){
			return(CRATE_CMD_ERROR,"BLKBUFFG [$msgsize].");
		}
		unless($retmsg=~s/^\S+\s+//){
			return(CRATE_CMD_ERROR,"Invalid buffer size [$retmsg].");
		}
		if($retmsg<0){
			return(CRATE_CMD_ERROR,"Invalid buffer size [$retmsg].");
		}
		$blksize=$retmsg;
	}elsif($blksize>0){
		($msgsize,$retmsg)=$this->BLKBUFFS($blksize);
		if($msgsize<=0){
			return(CRATE_CMD_ERROR,"BLKBUFFS [$msgsize].");
		}
	}else{
		return(CRATE_CMD_ERROR,"Invalid buffer size [$blksize].");
	}
	if($opcode eq OP_BLKSS){
		$sendmsg=sprintf("BLKSS %d %d %d %d", $F, $N, $A, $totsize);
	}elsif($opcode eq OP_BLKSR){
		$sendmsg=sprintf("BLKSR %d %d %d %d %d", $F, $N, $A, $totsize, $timeout);
	}elsif($opcode eq OP_BLKSA){
		$sendmsg=sprintf("BLKSA %d %d %d", $F, $N, $totsize);
	}elsif($opcode eq OP_BLKFS){
		$sendmsg=sprintf("BLKFS %d %d %d %d", $F, $N, $A, $totsize);
	}elsif($opcode eq OP_BLKFR){
		$sendmsg=sprintf("BLKFR %d %d %d %d %d", $F, $N, $A, $totsize, $timeout);
	}elsif($opcode eq OP_BLKFA){
		$sendmsg=sprintf("BLKFA %d %d %d", $F, $N, $totsize);
	}else{
		return(CRATE_CMD_ERROR,"Invalid opcode [$opcode].");
	}
	my($i,$j,$bytes_per_row,$rows);
	my @row_buf=();
	my($retcode);
	my $buf;

	my $retmsgbak="";
	my $retmsgbaklen=0;
	my @bufs=();
	if($F>=0 and $F<=7){
		if($binflg){$sendmsg.=" bin";}
		my($msgsize,$retmsg)=$this->CMDSR($sendmsg);
		if($msgsize<=0){
			return(CRATE_CMD_ERROR,"$sendmsg [$msgsize].");
		}
		if($binflg){
		}else{
			$retmsgbak="";
			$retmsgbaklen=0;
			@bufs=split(/\r\n/,$retmsg,2);
			if(($#bufs eq 1) and ($bufs[1] ne '')){
				$retmsgbak=$bufs[1];
				$retmsgbaklen=length($retmsgbak);
			}
			if($::Debug){
				print "#$retmsgbak($retmsgbaklen)#\n";
			}
		}
		if($binflg){$bytes_per_row=($blksize+1)*4;
		}else{$bytes_per_row=(4+($blksize*7));}
		$rows=int($totsize/$blksize)+1;
		if($totsize % $blksize){$rows++;}
		#($msgsize,$retmsg)=$this->CMD_Response();
		if($binflg){
			($msgsize,$retmsg)=$this->CMD_Response();
			for($i=0;$i<$rows;$i++){
				$j=$i*$bytes_per_row+3;
				if($msgsize < $j){
					my($msgsize2,$retmsg2)=$this->CMD_Response(0,$timeout);
					$msgsize+=$msgsize2;
					$retmsg.=$retmsg2;
					if($msgsize < $j){
						return(CRATE_CMD_ERROR,"Invalid data size [$msgsize].");
					}
				}
				$retcode=unpack("x".($j-3)."C",$retmsg) | (unpack("x".($j-2)."C",$retmsg) <<8)
				| (unpack("x".($j-1)."C",$retmsg)<<16) | (unpack("x".($j-0)."C",$retmsg)<<24);
				if($retcode<0){
					return(CRATE_CMD_ERROR,"Invalid retcode [$retcode].");
				}
				if($retcode eq 0){
					$j+=4;
					if($msgsize < $j){return(CRATE_CMD_ERROR,"Invalid data size [$msgsize].");}
					$buf=unpack("x".($j-3)."C",$retmsg) | (unpack("x".($j-2)."C",$retmsg) <<8)
					| (unpack("x".($j-1)."C",$retmsg)<<16) | (unpack("x".($j-0)."C",$retmsg)<<24);
					return($buf, join(",",@row_buf));
				}
				for($j+=4;$j<($i+1)*$bytes_per_row;$j+=4){
					if($msgsize < $j){return(CRATE_CMD_ERROR,"Invalid data size [$msgsize].");}
					if($retcode<=0){last;}
					$buf=unpack("x".($j-3)."C",$retmsg) | (unpack("x".($j-2)."C",$retmsg) <<8)
					| (unpack("x".($j-1)."C",$retmsg)<<16) | (unpack("x".($j-0)."C",$retmsg)<<24);
					push(@row_buf,$buf);
					$retcode--;
				}
			}
			return(CRATE_CMD_ERROR,"Invalid retcode [$retcode] [".join(",",@row_buf)."].");
		}else{
			#($msgsize,$retmsg)=$this->CMD_Response();
			$retmsg=$retmsgbak;
			$msgsize=$retmsgbaklen;
			#if($retmsg ne ''){
				while($retmsg!~/\r\n/){
					if($::Debug){
						print "#$retmsg#($msgsize)";
					}
					my($msgsize2,$retmsg2)=$this->CMD_Response(0,0.01);
					if($msgsize2>0){
						$msgsize+=$msgsize2;
						$retmsg.=$retmsg2;
					}
				}
			#}
			
			$retmsg=~s/\r/\t/g;
			for($i=0;$i<$rows;$i++){
				if($msgsize<$i*$bytes_per_row+3){
					my($msgsize2,$retmsg2)=$this->CMD_Response(0,$timeout);
					$msgsize+=$msgsize2;
					$retmsg.=$retmsg2;
					if($msgsize <$i*$bytes_per_row+3){
						return(CRATE_CMD_ERROR,"Invalid data size [$msgsize].");
					}
					$retmsg=~s/\r/\t/g;
				}
				unless($retmsg=~s/^(\S{3})\s//){
					my($msgsize2,$retmsg2)=$this->CMD_Response(0,$timeout);
					$msgsize+=$msgsize2;
					$retmsg.=$retmsg2;
					unless($retmsg=~s/^(\S{3})\s//){
						return(CRATE_CMD_ERROR,"Invalid retcode [$retcode] [".join(",",@row_buf)."].");
					}
					$retcode=$1+0;
				}else{
					$retcode=$1+0;
				}
				if($retcode<0){
					return(CRATE_CMD_ERROR,"Invalid retcode [$retcode] [".join(",",@row_buf)."].");
				}
				if($retcode eq 0){
					unless($retmsg=~/^(\S{6})\s/){
						return(CRATE_CMD_ERROR,"Invalid data [$retmsg].");
					}
					my($msgsize2,$retmsg2)=$this->CMD_Response(0,0.005);
					if($msgsize2>0){
						while($retmsg2!~/\r\n/){
							if($::Debug){
								print "#$retmsg2#($msgsize2)";
							}
							($msgsize2,$retmsg2)=$this->CMD_Response(0,0.01);
						}
					}
					return(hex($1), join(",",@row_buf));
				}
				for($j=0;$j<$blksize;$j++){
					unless($retmsg=~s/^(\S{6})\s//){
						my($msgsize2,$retmsg2)=$this->CMD_Response(0,$timeout);
						$msgsize+=$msgsize2;
						$retmsg.=$retmsg2;
						unless($retmsg=~s/^(\S{6})\s//){
							return(CRATE_CMD_ERROR,"Invalid data [$retmsg].");
						}
					}
					if(($opcode eq OP_BLKSS) or ($opcode eq OP_BLKFS)){
						if($j>=$retcode){next;}
					}

					if($totsize>0){push(@row_buf,hex($1));$totsize--}
				}
			}
			return(CRATE_CMD_ERROR,"Invalid retcode [$retcode] [".join(",",@row_buf)."].");
		}
	}elsif($F>=16 and $F<=27){
		@row_buf=split(",",$output);
		if($#row_buf+1>$totsize){
			splice(@row_buf,$totsize,$#row_buf+1-$totsize);

		}
		foreach $buf (@row_buf){
			unless($buf=~/^\d+$/){
				return(CRATE_CMD_ERROR,"Invalid data [$_].");
			}
			if(($opcode eq OP_BLKSS) or ($opcode eq OP_BLKSR) or($opcode eq OP_BLKSA)){
				if($buf>=65536){
					return(CRATE_CMD_ERROR,"Invalid data [$_].");
				}
			}else{
				if($buf>=16777216){
					return(CRATE_CMD_ERROR,"Invalid data [$_].");
				}
			}
		}
		my($msgsize,$retmsg)=$this->CMDSR($sendmsg);
		if($msgsize<=0){
			return(CRATE_CMD_ERROR,"$sendmsg [$msgsize].");
		}
		$bytes_per_row=(4+($blksize*7));
		$rows=int($totsize/$blksize);
		if($totsize % $blksize){$rows++;}
		for($i=0;$i<$rows;$i++) {
			if($i eq ($rows-1)){
				$sendmsg=sprintf("%03d", $totsize % $blksize);
			}else{
				$sendmsg=sprintf("%03d", $blksize);
			}
			for($j=0;$j<$blksize;$j++) {
				if($#row_buf>=0){
					$sendmsg.=sprintf(" %06X",shift(@row_buf));
				}else{
					$sendmsg.=" 000000";
				}
			}
			$sendmsg.="\r";
			($msgsize)=$this->CMDS($sendmsg,length($sendmsg));
			if($msgsize<0){
				return(CRATE_CMD_ERROR,"$sendmsg [$msgsize].");
			}
		}
		($msgsize,$retmsg)=$this->CMD_Response();
		($_,$_)=$this->CMD_Response();
		if($msgsize<=0){
			return(CRATE_CMD_ERROR,"Invalid response [$msgsize].");
		}
		$retmsg=~s/^\s+//;$retmsg=~s/\s+$//;
		unless($retmsg=~s/^(\S+)\s(\S+)/$2/){
			return(CRATE_CMD_ERROR,"Invalid data [$retmsg].");
		}
		$retcode=$1+0;
		$retmsg+=0;
		if($retcode eq 0){
			if($retmsg>0){
				return($retmsg,"$retmsg");
			}else{
				return(CRATE_CMD_ERROR,"$retmsg data updated.");
			}
		}else{
			return(CRATE_CMD_ERROR,"Invalid retcode [$retcode].");
		}
	}else{
		return(CRATE_CMD_ERROR,"Invalid F [$F].");
	}
}
1;
