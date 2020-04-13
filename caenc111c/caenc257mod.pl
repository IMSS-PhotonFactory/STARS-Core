#################################################################
# CAMAC Slot Module CAEN Model C257
# 2006-08-31 Yasuko Nagatani
##-------------------------------------------------------
## CVS $Revision: 1.1 $ $Date: 2010-01-19 01:55:24 $ $Author: yasukon $
##-------------------------------------------------------
## Updated
#################################################################
use Time::HiRes qw(gettimeofday tv_interval);
use strict;
#################################################################
## Rewrite PGM Version for renewal.
use constant CAENC257_PGM_VERSION     => '1.1';
#################################################################

## ToDo: Constant Variables here.
use constant CAENC257_INTERVAL_REFRESH    => 0.5;

## ToDo: Write Globals.
#@::CAENC257CounterName: 			#Comment is true, Global set by config.pl.

#############################################################
## Execute CFSA
#############################################################
sub CAENC257CXFA{
	my($f,$n,$a,$dat,$q)=@_;
	my $rt='';
	my($RC,$Q,$X,$RETDATA)=$::camac->CFSA($f,$n,$a,$dat);
#	$::tak->Sleep(50);
	$::CAENC257INTERNALError{$n}=0;
	if($RC<0){
		$::CAENC257INTERNALError{$n}=1;
		$::CAENC257Error{$n}="Er: $RC";
		print "CONNECTION ERROR: RC=[$RC:$f,$n,$a,$dat]\n";
	}elsif($X ne 1){
		$::CAENC257Error{$n}="Er: $RC,$Q,$X,$RETDATA";
		print "UNEXPECTED ERROR: X=[$X]\n";
	}elsif(($q ne '') and ($Q ne $q)){
		$::CAENC257Error{$n}="Ng: $Q,$X,$RETDATA";
	}else{
		if(wantarray){return($Q,$X,$RETDATA);}
		$rt="$Q,$X,$RETDATA";
	}
	return($rt);
}
#################################################################
### LAMCHECK
#################################################################
sub CAENC257CheckLAMChanged{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my $dest=shift;unless($dest){$dest="System";}
	my($Q,$X,$DATA)=CAENC257CXFA(8,$slotno,0,0,'');
	if($Q eq ''){
		print "UNEXPECTED ERROR: Q=[$Q] CheckLAMChanged\n";
		return('');
	}elsif($Q ne $::CAENC257_LAMBUSY{$slotno}){
		$::CAENC257_LAMBUSY{$slotno}=$Q;
		$::tak->Send("$nodename>$dest _ChangedLAMIsBusy $Q");
		return(1);
	}return(0);
}
#################################################################
### INHIBIT CHECK
#################################################################
sub CAENC257CheckInhibitChanged{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my($Q)=shift;
	my $dest=shift;unless($dest){$dest="System";}
	if($Q ne $::CAENC257_FLAG_INHIBIT{$slotno}){
		$::CAENC257_FLAG_INHIBIT{$slotno}=$Q;
		if($Q=~/^1$/){
			$::tak->Send("$nodename>$dest _ChangedInhibitIsBusy 1");
		}elsif($Q=~/^0$/){
			$::tak->Send("$nodename>$dest _ChangedInhibitIsBusy 0");
		}
#		CAENC257GetValue($nodename,$slotno,1,$dest);
		return(1);
	}return(0);
}
#################################################################
### GETVALUE
#################################################################
sub CAENC257GetValue{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my $all=shift;
	my $dest=shift;unless($dest){$dest="System";}
	my $i;
	my($Q,$X,$DATA);
	 
	for($i=0;$i<=15;$i++){
		($Q,$X,$DATA)=CAENC257CXFA( 0,$slotno,$i,0,'');
		$::tak->Sleep(40);
		if($Q eq ''){print "UNEXPECTED ERROR: Q=[$Q] GetValue\n";return(0);
		}else{
#			if(CAENC257CheckInhibitChanged($nodename,$slotno,$Q,$dest)){last;}
			CAENC257CheckInhibitChanged($nodename,$slotno,$Q,$dest);
			if($all or ($::CAENC257_VALUE{$slotno}[$i] ne $DATA)){
				$::CAENC257_VALUE{$slotno}[$i]=$DATA;
				$::tak->Send("$::CAENC257CounterName{$slotno}[$i]>$dest _ChangedValue $DATA");
			}
		}
	}return(1);
}
#############################################################
## Interval handler called by CAMAC HANDLER
#############################################################
sub CAENC257Interval{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my $timercnt;
	
	if($::CAENC257INTERNALError{$slotno}){return(0);};
	$timercnt=tv_interval($::CAENC257IntervalTime{$slotno}) - CAENC257_INTERVAL_REFRESH;
	if($timercnt>0){
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		CAENC257GetValue($nodename,$slotno,0);
		$::Debug=$debug;
		if($::CAENC257INTERNALError{$slotno}){return(0);};
		$::tak->Sleep(40);
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		CAENC257CheckLAMChanged($nodename,$slotno);
		$::Debug=$debug;
		$::CAENC257IntervalTime{$slotno}=[gettimeofday];
	}return(1);
}
#############################################################
## Init Function
#############################################################
sub CAENC257Init{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#SLOT NO
	
	$::CAENC257INTERNALError{$slotno}='';
	$::CAENC257Error{$slotno}='';
	$::CAENC257_FLAG_INHIBIT{$slotno}=-1; #Inhibit 1 or 0.
	$::CAENC257_LAMBUSY{$slotno}=-1;      #LAM Busy 0 or 1.
	@{$::CAENC257_VALUE{$slotno}}=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16];
	                                      #Store Previous Counter Value.
	unless(CAENC257CheckLAMChanged($nodename,$slotno)){die;}
	$::tak->Sleep(40);
	unless(CAENC257GetValue($nodename,$slotno,1)){die;}
	return(CAENC257set_help_list());#make helptable.
}
#############################################################
## handler called by Controller
#############################################################
sub CAENC257Handler{
## ToDo: Please modify handler sub routine.
##  (The handler sub routine will be called when client
##  receives a message from a Stars server.)
	my ($from, $to, $mess) = (shift,shift,shift);
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#SLOT NO
	my($Q,$X,$DATA);
	my $addok=1;
	my $rt='';
	$::CAENC257Error{$slotno}='';
	
##Ignore Event/Reply Messages ##
	if($mess=~/^[_@]/){return;}
	$mess=~/^(\S+)/;
	if(!defined($::CAENC257helpcntrl{$1})){#Command Valid Check.
		$::CAENC257Error{$slotno}="Er: Bad Command.";
	}elsif($mess=~/^hello$/){
		$addok=0;$rt='nice to meet you.';
	}elsif($mess=~/^help$/){
		$addok=0;$rt=CAENC257get_help_list('Cntrl');
	}elsif($mess=~/^help\s(.+)$/){
		$addok=0;$rt=CAENC257get_help_list('Cntrl',$1);
### flushdata
	}elsif($mess=~/^flushdata$/){
		$::CAENC257_FLAG_INHIBIT{$slotno}=-1;		#Inhibit 0 or 1.
		$::CAENC257_LAMBUSY{$slotno}=-1;				#LAM Busy 0 or 1.
		CAENC257GetValue($nodename,$slotno,1);
		CAENC257CheckLAMChanged($nodename,$slotno);
		$rt="Ok:";
	}elsif($mess=~/^flushdatatome$/){
		$::CAENC257_FLAG_INHIBIT{$slotno}=-1;		#Inhibit 0 or 1.
		$::CAENC257_LAMBUSY{$slotno}=-1;				#LAM Busy 0 or 1.
		CAENC257GetValue($nodename,$slotno,1,"$from");
		CAENC257CheckLAMChanged($nodename,$slotno,"$from");
		$rt="Ok:";
### GetValue
	}elsif($mess=~/^GetValue$/){
		my $binflg=0;
		if($::CAENC257_PGM_TAG{$slotno}=~/\-BINGETVALUE/i){$binflg=1;}
		my($rc,$retmsg)=$::camac->BLKxA($binflg,'F',0,$slotno,16,16);
		if($rc>0){$rt=$retmsg;}else{$::CAENC257Error{$slotno}=$retmsg;}
	}elsif($mess=~/^GetValue\s([0-9]|10|11|12|13|14|15)$/){
		my $cno=$1;
		($Q,$X,$DATA)=CAENC257CXFA( 0,$slotno,$cno,0,'');
		if($Q=~/^[01]$/){
			if(($::CAENC257_VALUE{$slotno}[$cno] ne $DATA)){
				$::CAENC257_VALUE{$slotno}[$cno]=$DATA;
				$::tak->Send("$::CAENC257CounterName{$slotno}[$cno]>System _ChangedValue $DATA");
			}
			$rt=$DATA;CAENC257CheckInhibitChanged($nodename,$slotno,$Q);
		}
	}elsif($mess=~/^GetValueInhibitReset\s([0-9]|10|11|12|13|14|15)$/){
		my $cno=$1;
		($Q,$X,$DATA)=CAENC257CXFA( 2,$slotno,$cno,0,'');
		if($Q=~/^[01]$/){
			if(($::CAENC257_VALUE{$slotno}[$cno] ne $DATA)){
				$::CAENC257_VALUE{$slotno}[$cno]=$DATA;
				$::tak->Send("$::CAENC257CounterName{$slotno}[$cno]>System _ChangedValue $DATA");
			}
			$rt=$DATA;CAENC257CheckInhibitChanged($nodename,$slotno,$Q);
		}
### Reset
	}elsif($mess=~/^Reset$/){
		($Q,$X,$DATA)=CAENC257CXFA( 9,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Get LAM Jumper Settings
	}elsif($mess=~/^GetLAMJumperSettings$/){
		($Q,$X,$DATA)=CAENC257CXFA( 1,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt=$DATA;}
### Get Inhibit Status
	}elsif($mess=~/^GetInhibitIsBusy$/){
		($Q,$X,$DATA)=CAENC257CXFA( 0,$slotno, 0,0,'');
		if($Q=~/^[01]$/){$rt=$Q;CAENC257CheckInhibitChanged($nodename,$slotno,$Q);}
### Get LAM Status
	}elsif($mess=~/^GetLAMIsBusy$/){
		($Q,$X,$DATA)=CAENC257CXFA( 8,$slotno, 0,0,'');
		if($Q=~/^[01]$/){$rt=$Q;}
	}elsif(($mess=~/^GetValueInternalLAM$/)){
		($Q,$X,$DATA)=CAENC257CXFA(27,$slotno, 0,0,'');
		if($Q=~/^[01]$/){$rt=$Q;}
### Change LAM
	}elsif($mess=~/^ResetValueLAM$/){
		($Q,$X,$DATA)=CAENC257CXFA(10,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^SetLAMEnable\s0$/){
		($Q,$X,$DATA)=CAENC257CXFA(24,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^SetLAMEnable\s1$/){
		($Q,$X,$DATA)=CAENC257CXFA(26,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Generate Test Input
	}elsif($mess=~/^RunTestSignal$/){
		($Q,$X,$DATA)=CAENC257CXFA(25,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^GetCounterName\s([0-9]|10|11|12|13|14|15)$/){
		$rt=$::CAENC257CounterName[$1];
	}elsif($mess=~/^GetCounterNameList$/){
		$rt=join(" ",@::CAENC257CounterName);
### Error
	}else{
		$::CAENC257Error{$slotno}='Er: Bad Parameter.';
	}
## Response ##
	if(($rt eq '') and ($::CAENC257Error{$slotno}=~/^Ng:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC257Error{$slotno}");
	}elsif(($rt eq '') and ($::CAENC257Error{$slotno}=~/^Er:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC257Error{$slotno}");
	}elsif($rt eq ''){
		$::tak->Send("$to>$from \@$mess Er: $::CAENC257Error{$slotno}");
	}elsif($rt=~/^Ok:/ or (!($addok))){
		$::tak->Send("$to>$from \@$mess $rt"); 
	}else{
		$::tak->Send("$to>$from \@$mess Ok: $rt"); 
	}
	return(1);
}
#############################################################
## handler called by Controller
#############################################################
sub CAENC257CounterHandler{
## ToDo: Please modify handler sub routine.
##  (The handler sub routine will be called when client
##  receives a message from a Stars server.)
	my ($from, $to, $mess) = (shift,shift,shift);
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;
	my($Q,$X,$DATA);
	my $addok=1;
	my $rt='';
	$::CAENC257Error{$slotno}='';
	my $cno=$::CAENC257CounterNumber{$nodename};
	if($cno eq ''){
		$::tak->Send("\@$mess Er: $to is down.", $from);return;
	}
##Ignore Event/Reply Messages ##
	if($mess=~/^[_@]/){return;}
	$mess=~/^(\S+)/;
	if(!defined($::CAENC257helpcountercntrl{$1})){#Command Valid Check.
		$::CAENC257Error{$slotno}="Er: Bad Command.";
	}elsif($mess=~/^hello$/){
		$addok=0;$rt='nice to meet you.';
	}elsif($mess=~/^help$/){
		$addok=0;$rt=CAENC257get_help_list('Counter');
	}elsif($mess=~/^help\s(.+)$/){
		$addok=0;$rt=CAENC257get_help_list('Counter',$1);
	}elsif($mess=~/^GetCounterNumber$/){
		$rt=$::CAENC257CounterNumber{$nodename};
### GetValue
	}elsif($mess=~/^GetValue$/){
		($Q,$X,$DATA)=CAENC257CXFA( 0,$slotno,$cno,0,'');
		if($Q=~/^[01]$/){
			if(($::CAENC257_VALUE{$slotno}[$cno] ne $DATA)){
				$::CAENC257_VALUE{$slotno}[$cno]=$DATA;
				$::tak->Send("$::CAENC257CounterName{$slotno}[$cno]>System _ChangedValue $DATA");
			}
			$rt=$DATA;CAENC257CheckInhibitChanged($nodename,$slotno,$Q);
		}
	}elsif($mess=~/^GetValueInhibitReset$/){
		($Q,$X,$DATA)=CAENC257CXFA( 2,$slotno,$cno,0,'');
		if($Q=~/^[01]$/){
			if(($::CAENC257_VALUE{$slotno}[$cno] ne $DATA)){
				$::CAENC257_VALUE{$slotno}[$cno]=$DATA;
				$::tak->Send("$::CAENC257CounterName{$slotno}[$cno]>System _ChangedValue $DATA");
			}
			$rt=$DATA;CAENC257CheckInhibitChanged($nodename,$slotno,$Q);
		}
### Error
	}else{
		$::CAENC257Error{$slotno}='Er: Bad Parameter.';
	}
## Response ##
	if(($rt eq '') and ($::CAENC257Error{$slotno}=~/^Ng:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC257Error{$slotno}");
	}elsif(($rt eq '') and ($::CAENC257Error{$slotno}=~/^Er:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC257Error{$slotno}");
	}elsif($rt eq ''){
		$::tak->Send("$to>$from \@$mess Er: $::CAENC257Error{$slotno}");
	}elsif($rt=~/^Ok:/ or (!($addok))){
		$::tak->Send("$to>$from \@$mess $rt"); 
	}else{
		$::tak->Send("$to>$from \@$mess Ok: $rt"); 
	}
	return;
}
#############################################################
## Register Program
#############################################################
sub CAENC257Register{
	my($nodename,$slotno,$counternodetag,$pgmtag,$pgmver)=@_;
	my $i;
	my $intervalflg=1;
	my $rt;
	if($pgmtag){
		$::CAENC257_PGM_TAG{$slotno}=$pgmtag;
	}else{
		$::CAENC257_PGM_TAG{$slotno} = '';
	}

	if($pgmver){
		$::CAENC257_PGM_VER{$slotno}=$pgmver;
	}else{
		$::CAENC257_PGM_VER{$slotno} = CAENC257_PGM_VERSION;
	}

	if($::CAENC257_PGM_TAG{$slotno}=~/\-DISABLEINTERVAL/i){
		$intervalflg = 0;
	}
	$::CAENC257IntervalTime{$slotno}=[gettimeofday];
	
	if($intervalflg){
		$rt=MAIN_RegisterModule2Controller("$nodename","$slotno",\&CAENC257Init,\&CAENC257Handler,\&CAENC257Interval,'',"CEAN Model C257");
	}else{
		$rt=MAIN_RegisterModule2Controller("$nodename","$slotno",\&CAENC257Init,\&CAENC257Handler,'','',"CEAN Model C257");
	}
	if($rt eq ''){die "Failed to register NODENAME[$nodename] SLOTNO[$slotno]\n.";}
	if($counternodetag eq ''){$counternodetag=$nodename;}
	if(defined(@{$::CAENC257CounterName{$slotno}})){
		unless( scalar(@{$::CAENC257CounterName{$slotno}}) eq 16 ){
			die 'Number of Counter Invalid. @{$::CAENC257CounterName{'.$slotno.'}}'."\n";
		}else{
			for($i=0;$i<=15;$i++){
				$::CAENC257CounterName{$slotno}[$i]="$counternodetag.$::CAENC257CounterName{$slotno}[$i]";
			}
		}
	}elsif(defined(@::CAENC257CounterName)){
		unless( scalar(@::CAENC257CounterName) eq 16 ){
			die 'Number of Counter Invalid. @::CAENC257CounterName'."\n";
		}else{
			for($i=0;$i<=15;$i++){
				$::CAENC257CounterName{$slotno}[$i]="$counternodetag.$::CAENC257CounterName[$i]";
			}
		}
	}else{
		for($i=0;$i<=15;$i++){
			$::CAENC257CounterName{$slotno}[$i]=sprintf("$counternodetag.C%02d",$i);
		}
	}
	for($i=0;$i<=15;$i++){
		if($::Debug){
			print "$::CAENC257CounterName{$slotno}[$i]\n";
		}
		$rt=MAIN_RegisterModule2Controller($::CAENC257CounterName{$slotno}[$i],"$slotno",'',\&CAENC257CounterHandler,'','',"CEAN Model C257 - Counter");
		$::CAENC257CounterNumber{$::CAENC257CounterName{$slotno}[$i]}=$i;
	}return(1);
}
################################################################
## Help Function
################################################################
sub CAENC257get_help_list{
	my($target,$cmd)=@_;
	if($target eq 'Cntrl'){
		unless($cmd){return(join(" ", sort(keys(%::CAENC257helpcntrl))));}
		unless(defined($::CAENC257helpcntrl{$cmd})){
			return('Ng: Bad Command.');
		}
		return($::CAENC257helpcntrl{$cmd});
	}else{
		unless($cmd){return(join(" ", sort(keys(%::CAENC257helpcountercntrl))));}
		unless(defined($::CAENC257helpcountercntrl{$cmd})){
			return('Ng: Bad Command.');
		}
		return($::CAENC257helpcountercntrl{$cmd});
	}
}
sub CAENC257set_help_list{
	my @arrays=();
my $data=<<EOF;
GetValue#[F(0) A(i)]\tReads the value held in the counter addressed by i (i=0 to 15). Q is true only if the input is inhibited.
GetValueInhibitReset#[F(2) A(i)]\tSame As GetValue, and with reads the 15th channel and, if the input inhibited,resets all the channels and the LAM line.
GetLAMJumperSettings#[F(1)]\tReads the status of the internal jumpers for LAM enabling/disabling (R(i)=1 if CH(i)=enabled).
GetLAMIsBusy#[F(8)]\tTests the LAM line. Q is true if LAM is enable and present.
GetInhibitIsBusy#Returns 1 if the input is inhibited or returns 0.
Reset#[F(9)]\tResets the all module (All the scales and the internal LAM are set to 0.The LAM line is disbaled.
SetLAMEnable#[F(26)]\tSetLAMEnable 1->Enables the LAM.\t[F(24)]\tSetLAMEnable 0->Disables the LAM.
ResetValueLAM#[F(10)]\tClears the LAM.
GetValueInternalLAM#[F(27)]\tTests the Internal LAM. Q is true if LAM is enable and present.
RunTestSignal#[F(25)]\tTests the counters (same as the Test input signal). At the S2 time all the channels are increased (valid only in single channel configuration).
hello#Return 'nice to meet you.'
help#'help'=> Show command list. 'help <command>'=>Show command help.
flushdata#Send Stars Event Messages to System.
flushdatatome#Send Stars Event Messages to fromnode.
GetCounterName#Return stars nodename specified with the input counter number.
GetCounterNameList#Return stars nodename list of counter name.
EOF
	$data=$data.MAIN_subhelp();
	%::CAENC257helpcntrl=();
	foreach (split(/\n/,$data)){
		@arrays=split(/#/,$_);
		unless($arrays[0] eq ''){$::CAENC257helpcntrl{$arrays[0]}=$arrays[1];}
	}
my $data=<<EOF;
hello#Return 'nice to meet you.'
help#'help'=> Show command list. 'help <command>'=>Show command help.
GetValue#[F(0) A(i)]\tReads the value held in the counter addressed by i (i=0 to 15). Q is true only if the input is inhibited.
GetValueInhibitReset#[F(2) A(i)]\tSame As GetValue, and with reads the 15th channel and, if the input inhibited,resets all the channels and the LAM line.
GetCounterNumber#Return the input counter number.
EOF
	%::CAENC257helpcountercntrl=();
	foreach (split(/\n/,$data)){
		@arrays=split(/#/,$_);
		unless($arrays[0] eq ''){$::CAENC257helpcountercntrl{$arrays[0]}=$arrays[1];}
	}
	return(1);
}
1
