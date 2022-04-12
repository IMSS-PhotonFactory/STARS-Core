################################################################
# CAMAC Slot Module KineticSystems Model 3655-L1A
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
use constant KINETICSYSTEMS3655L1A_PGM_VESRION => 1.1;
#################################################################
## ToDo: Constant Variables here.
use constant KINETICSYSTEMS3655L1A_INTERVAL_REFRESH => 0.1;

## ToDo: Write Globals.

#############################################################
## Execute CFSA
#############################################################
sub KINETICSYSTEMS3655L1ACXFA{
	my($f,$n,$a,$dat,$q)=@_;
	my $rt='';
	my($RC,$Q,$X,$RETDATA)=$::camac->CFSA($f,$n,$a,$dat);
#	$::tak->Sleep(50);
	$::KINETICSYSTEMS3655L1AINTERNALError{$n}=0;
	if($RC<0){
		$::KINETICSYSTEMS3655L1AINTERNALError{$n}=1;
		$::KINETICSYSTEMS3655L1AError{$n}="Er: $RC";
		print "CONNECTION ERROR: RC=[$RC:$f,$n,$a,$dat]\n";
	}elsif($X ne 1){
		$::KINETICSYSTEMS3655L1AError{$n}="Er: $RC,$Q,$X,$RETDATA";
		print "UNEXPECTED ERROR: X=[$X]\n";
	}elsif(($q ne '') and ($Q ne $q)){
		$::KINETICSYSTEMS3655L1AError{$n}="Ng: $Q,$X,$RETDATA";
	}else{
		if(wantarray){return($Q,$X,$RETDATA);}
		$rt="$Q,$X,$RETDATA";
	}
	return($rt);
}
#################################################################
### LAMCHECK
#################################################################
sub KINETICSYSTEMS3655L1ACheckLAMChanged{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my $dest=shift;unless($dest){$dest="System";}
	my($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA( 8,$slotno,15,0,'');
	if($Q eq ''){
		print "UNEXPECTED ERROR: Q=[$Q] CheckLAMChanged\n";
		return('');
	}elsif(($Q ne $::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno})){
		$::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno}=$Q;
		$::tak->Send("$nodename>$dest _ChangedLAMIsBusy $Q");
		return(1);
	}return(0);
}
#################################################################
### READ LAM STATUS
#################################################################
sub KINETICSYSTEMS3655L1AGetLAMStatusBits{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#Slot No
	my $dest=shift;unless($dest){$dest="System";}
	my($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA( 1,$slotno,12,0,1);
	if($Q eq ''){
		print "UNEXPECTED ERROR: Q=[$Q] GetLAMStatusBits\n";
		return('');
	}elsif(($DATA ne $::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno})){
		$::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno}=$DATA;
		$::tak->Send("$nodename>$dest _ChangedValueLAMStatusBits $DATA");
		return(1);
	}return(0);
}
#############################################################
## Interval handler called by CAMAC HANDLER
#############################################################
sub KINETICSYSTEMS3655L1AInterval{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;		#Slot No
	my $timercnt;
	
	if($::KINETICSYSTEMS3655L1AINTERNALError{$slotno}){return(0);};
	$timercnt=tv_interval($::KINETICSYSTEMS3655L1AIntervalTime{$slotno})
						 - KINETICSYSTEMS3655L1A_INTERVAL_REFRESH;
	if($timercnt>0){
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		KINETICSYSTEMS3655L1AGetLAMStatusBits($nodename,$slotno);
		$::Debug=$debug;
		if($::KINETICSYSTEMS3655L1AINTERNALError{$slotno}){return(0);};
		$::tak->Sleep(40);
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		KINETICSYSTEMS3655L1ACheckLAMChanged($nodename,$slotno);
		$::Debug=$debug;
		$::KINETICSYSTEMS3655L1AIntervalTime{$slotno}=[gettimeofday];
	}return(1);
}
#############################################################
## Init Function
#############################################################
sub KINETICSYSTEMS3655L1AInit{
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#SLOT NO
	my($Q,$X,$DATA);

	#Store Model
	$::KINETICSYSTEMS3655L1AINTERNALError{$slotno}='';
	$::KINETICSYSTEMS3655L1AError{$slotno}='';
	$::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno}=-1; #LAM Busy 0 or 1.
	$::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno}=''; #LAM Status Bit.

	($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA( 1,$slotno,15,0,1);
	if($Q eq ''){print "UNEXPECTED ERROR: Q=[$Q] Module identifying number reading\n";die;
	}else{$::KINETICSYSTEMS3655L1A_MODELNO{$slotno}=$DATA;}
	if($::Debug){
		print ">>This is KeneticSystems Model " . $::KINETICSYSTEMS3655L1A_MODELNO{$slotno} ."\n";
	}
	#Store LAM Status Bits
	$::tak->Sleep(40);
	unless(KINETICSYSTEMS3655L1AGetLAMStatusBits($nodename,$slotno)){die;}
	$::tak->Sleep(40);
	unless(KINETICSYSTEMS3655L1ACheckLAMChanged($nodename,$slotno)){die;}
	$::tak->Sleep(40);
	return(KINETICSYSTEMS3655L1Aset_help_list());#make helptable.
}
#############################################################
## handler called by Controller
#############################################################
sub KINETICSYSTEMS3655L1AHandler{
## ToDo: Please modify handler sub routine.
##  (The handler sub routine will be called when client
##  receives a message from a Stars server.)
	my ($from, $to, $mess) = (shift,shift,shift);
	my $nodename=shift;	#STARS NODENAME
	my $slotno=shift;	#STARS SLOTNO
	my($Q,$X,$DATA);
	my $addok=1;
	my $rt='';
	$::KINETICSYSTEMS3655L1AError{$slotno}='';

##Ignore Event/Reply Messages ##
	if($mess=~/^[_@]/){return;}
	$mess=~/^(\S+)/;
	if(!defined($::KINETICSYSTEMS3655L1Ahelpcntrl{$1})){#Command Valid Check.
		$::KINETICSYSTEMS3655L1AError{$slotno}="Er: Bad Command.";
	}elsif($mess=~/^hello$/){
		$addok=0;$rt='nice to meet you.';
	}elsif($mess=~/^help$/){
		$addok=0;$rt=KINETICSYSTEMS3655L1Aget_help_list('Cntrl');
	}elsif($mess=~/^help\s(.+)$/){
		$addok=0;$rt=KINETICSYSTEMS3655L1Aget_help_list('Cntrl',$1);
	}elsif($mess=~/^GetModuleNumber$/){
		$rt=$::KINETICSYSTEMS3655L1A_MODELNO{$slotno};
### flushdata
	}elsif($mess=~/^flushdata$/){
		$::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno}=-1;			#LAM Busy 0 or 1.
		$::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno}='';		#LAM Status Bit.
		KINETICSYSTEMS3655L1AGetLAMStatusBits($nodename,$slotno);
		KINETICSYSTEMS3655L1ACheckLAMChanged($nodename,$slotno);
		$rt="Ok:";
	}elsif($mess=~/^flushdatatome$/){
		$::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno}=-1;			#LAM Busy 0 or 1.
		$::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno}='';		#LAM Status Bit.
		KINETICSYSTEMS3655L1AGetLAMStatusBits($nodename,$slotno,"$from");
		KINETICSYSTEMS3655L1ACheckLAMChanged($nodename,$slotno,"$from");
		$rt="Ok:";
### Get LAM Status
	}elsif($mess=~/^GetValueLAMStatusBits$/){
		unless(KINETICSYSTEMS3655L1AGetLAMStatusBits($nodename,$slotno) eq ''){
			$rt=$::KINETICSYSTEMS3655L1A_LAMSTATUSBIT{$slotno};
		}
	}elsif($mess=~/^GetLAMIsBusy$/){
		unless(KINETICSYSTEMS3655L1ACheckLAMChanged($nodename,$slotno) eq ''){
			$rt=$::KINETICSYSTEMS3655L1A_LAMBUSY{$slotno};
		}
### LAM Settings
	}elsif($mess=~/^SetLAMMaskRegister\s(\d+)$/ and ($1>=1 and $1<=255)){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(17,$slotno,13,$1,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Clear LAM
	}elsif($mess=~/^ResetValueLAM$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(11,$slotno,12,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Change Inhibit
	}elsif($mess=~/^SetInhibitRegister\s([0-7])\s([0-7])$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(17,$slotno, 9,$1+$2*8,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^SetInhibitEnable\s0$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(24,$slotno, 9,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^SetInhibitEnable\s1$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(26,$slotno, 9,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Set for Run
	}elsif($mess=~/^SetCycleControlRegister\s([0-7])\s([0-7])\s([01])$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(17,$slotno, 0,$1+$2*8+$3*64,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^GetDelayMultiplier\s([0-7])$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA( 0,$slotno,$1,0,1);
		if($Q=~/^1$/){$rt=$DATA;}
	}elsif($mess=~/^SetDelayMultiplier\s([0-7])\s(\d{1,5})$/ and ($2>=1 and $2<=65535)){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(16,$slotno,$1,$2,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^Run$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA( 9,$slotno, 8,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
	}elsif($mess=~/^Run2$/){
		($Q,$X,$DATA)=KINETICSYSTEMS3655L1ACXFA(25,$slotno, 0,0,1);
		if($Q=~/^1$/){$rt='Ok:';}
### Error
	}else{
		$::KINETICSYSTEMS3655L1AError{$slotno}='Er: Bad Parameter.';
	}
## Response ##
	if(($rt eq '') and ($::KINETICSYSTEMS3655L1AError{$slotno}=~/^Ng:/)){
		$::tak->Send("$to>$from \@$mess $::KINETICSYSTEMS3655L1AError{$slotno}");
	}elsif(($rt eq '') and ($::KINETICSYSTEMS3655L1AError=~/^Er:/)){
		$::tak->Send("$to>$from \@$mess $::KINETICSYSTEMS3655L1AError{$slotno}");
	}elsif($rt eq ''){
		$::tak->Send("$to>$from \@$mess Er: $::KINETICSYSTEMS3655L1AError{$slotno}");
	}elsif($rt=~/^Ok:/ or (!($addok))){
		$::tak->Send("$to>$from \@$mess $rt"); 
	}else{
		$::tak->Send("$to>$from \@$mess Ok: $rt"); 
	}
	return(1);
}
#############################################################
## Register Program
#############################################################
sub KINETICSYSTEMS3655L1ARegister{
	my($nodename,$slotno,$pgmtag,$pgmver)=@_;
	my $intervalflg=1;
	my $rt;
	
	if($pgmtag){
		$::KINETICSYSTEMS3655L1A_PGM_TAG{$slotno}=$pgmtag;
	}else{
		$::KINETICSYSTEMS3655L1A_PGM_TAG{$slotno}='';
	}
	if($pgmver){
		$::KINETICSYSTEMS3655L1A_PGM_VER{$slotno}=$pgmver;
	}else{
		$::KINETICSYSTEMS3655L1A_PGM_VER{$slotno}=KINETICSYSTEMS3655L1A_PGM_VESRION;
	}
	if($::KINETICSYSTEMS3655L1A_PGM_TAG{$slotno}=~/\-DISABLEINTERVAL/i){
                $intervalflg = 0;
        }
	$::KINETICSYSTEMS3655L1AIntervalTime{$slotno}=[gettimeofday];
	if($intervalflg){
		$rt=MAIN_RegisterModule2Controller("$nodename","$slotno",\&KINETICSYSTEMS3655L1AInit,\&KINETICSYSTEMS3655L1AHandler,\&KINETICSYSTEMS3655L1AInterval,'',"KeneticSystems Model 3655-L1A");
	}else{
		$rt=MAIN_RegisterModule2Controller("$nodename","$slotno",\&KINETICSYSTEMS3655L1AInit,\&KINETICSYSTEMS3655L1AHandler,'','',"KeneticSystems Model 3655-L1A");
	}
	if($rt eq ''){die "Failed to register NODENAME[$nodename] SLOTNO[$slotno]\n.";}
	return(1);
}
################################################################
## Help Function
################################################################
sub KINETICSYSTEMS3655L1Aget_help_list{
	my($target,$cmd)=@_;
	if($target eq 'Cntrl'){
		unless($cmd){return(join(" ", sort(keys(%::KINETICSYSTEMS3655L1Ahelpcntrl))));}
		unless(defined($::KINETICSYSTEMS3655L1Ahelpcntrl{$cmd})){
			return('Ng: Bad Command.');
		}
		return($::KINETICSYSTEMS3655L1Ahelpcntrl{$cmd});
	}
}
sub KINETICSYSTEMS3655L1Aset_help_list{
	my @arrays=();
	%::KINETICSYSTEMS3655L1Ahelpcntrl=();
my $data=<<EOF;
SetCycleControlRegister#[F(17) A(0)]\tWrites the Cycles Control register.
SetDelayMultiplier#[F(16) A(i)]\tWrites Set Point i.(i=0 to 7)
SetInhibitEnable#[F(26) A(9)]\tSetInhibitEnable 1->Enables the ability of the module to assert inhibit. \t[F(24) A(9)]\tSetInhibitEnable 0->Disables the ability of the module to assert inhibit.
SetInhibitRegister#[F(17) A(19)]\tWrites the inhibit register.
SetLAMMaskRegister#[F(17) A(13)]\tWrites the LAM Mask register.
Run#[F(9) A(8)]\tClears and enables the counter and clears the LAM status bits.
Run2#[F(25) A(0)]\tExecutes start of counting cycle (clears and enables counter).
ResetValueLAM#[F(11) A(12)]\tClears the LAM status bits.
GetDelayMultiplier#[F(0) A(i)]\tReads Set Point i. (i=0 to 7)
GetLAMIsBusy#[F(8) A(15)]\tTests whether a LAM request is present.
GetValueLAMStatusBits#[F(1) A(12)]\tReads the LAM status bits.
GetModuleNumber#[F(1) A(15)]\tReads the module identifying number(3655).
flushdata#Send Stars Event Messages to System.
flushdatatome#Send Stars Event Messages to fromnode.
hello#Return 'nice to meet you.'
help#'help'=> Show command list. 'help <command>'=>Show command help.
EOF
	$data=$data.MAIN_subhelp();
	foreach (split(/\n/,$data)){
		@arrays=split(/#/,$_);
		unless($arrays[0] eq ''){
			$::KINETICSYSTEMS3655L1Ahelpcntrl{$arrays[0]}=$arrays[1];
		}
	}
	return(1);
}
1
