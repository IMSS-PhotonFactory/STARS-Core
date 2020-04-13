#################################################################
# CAMAC Controller Module CAEN Model C111C
# 2006-08-31 Yasuko Nagatani
##-------------------------------------------------------
## CVS $Revision: 1.1 $ $Date: 2010-01-19 01:55:24 $ $Author: yasukon $
##-------------------------------------------------------
## Updated
#################################################################
use Time::HiRes qw(gettimeofday tv_interval);
use strict;
#################################################################
## ToDo: Constant Variables here.
use constant CAENC111C_PGM_VERSION     => '1.1'; # PGM Ver.No
use constant CAENC111C_INTERVAL_REFRESH => 0.5;    # NoBusy sec
use constant CAENC111C_COMBOBUSYCHECK => 0;      # 0 Nocheck
use constant CAENC111C_NIMINEVTCOUNTERCHANGED => 0; # 0 Nocheck
#################################################################
$::CAENC111CINTERNALError='';
$::CAENC111CIntervalTime=[gettimeofday];
$::CAENC111CError='';
$::CAENC111C_FLAG_INHIBIT=-1;		#Inhibit 0 or 1.
@::CAENC111C_BIT_SLOTIN=();		    #Slot IN or NOT
$::CAENC111C_NODENAME='';
%::CAENC111C_COMBOIsBusy=();
$::CAENC111C_COMBOIsBusy{1}=-1;		#COMBO1 Busy or not.
$::CAENC111C_COMBOIsBusy{2}=-1;		#COMBO2 Busy or not.
%::CAENC111C_ComboEventCounter=();
$::CAENC111C_ComboEventCounter{1}=-1;
$::CAENC111C_ComboEventCounter{2}=-1;
%::CAENC111C_NIMInEventCounter=();
$::CAENC111C_NIMInEventCounter{1}=-1;	#NIMIN1EventCounter Value.
$::CAENC111C_NIMInEventCounter{3}=-1;	#NIMIN3EventCounter Value.
@::CAENC111C_LAM=();
#############################################################
## INHIBIT CHECK
#############################################################
sub CAENC111CCheckInhibitChanged{
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	my $dest=shift;unless($dest){$dest="System";}
	
	$::CAENC111CINTERNALError=0;
	my($RC,$retmsg)=$::camac->CTCI();
#	$::tak->Sleep(50);
	if($RC<0){
		$::CAENC111CINTERNALError=1;
		$::CAENC111CError="Er: $RC,$retmsg";
		print "CONNECTION ERROR: RC=[$RC] CTCI\n";
		return('');
	}
	if($::CAENC111C_FLAG_INHIBIT ne $retmsg){
		if($retmsg=~/^0$/){
			$::tak->Send("$nodename>$dest _ChangedInhibitIsBusy 0");
		}elsif($retmsg=~/^1$/){
			$::tak->Send("$nodename>$dest _ChangedInhibitIsBusy 1");
		}else{
			$::CAENC111CError="Er: $RC,$retmsg";
			print "UNEXPECTED ERROR: DATA=[$retmsg] CTCI\n";
			return('');
		}
		$::CAENC111C_FLAG_INHIBIT=$retmsg;
		return(1);
	}return(0);
}
#############################################################
## Scan : Dangerous Run clear Settings
#############################################################
sub CAENC111CScan{
	my($i,$buf);
	$::CAENC111CINTERNALError=0;
	my($RC,$retmsg)=$::camac->CSCAN();
#	$::tak->Sleep(50);
	if($RC<0){
		$::CAENC111CINTERNALError=1;
		$::CAENC111CError="Er: $RC,$retmsg";
		print "CONNECTION ERROR: RC=[$RC] CTCI\n";
		return('');
	}
	$buf=sprintf("%X",scalar($retmsg));
	@::CAENC111C_BIT_SLOTIN=reverse(
	  split(//,unpack("B".length($buf)*4, pack("H".length($buf),$buf))));
	for($i=@::CAENC111C_BIT_SLOTIN;$i<23;$i++){
		$::CAENC111C_BIT_SLOTIN[$i]=0;
	}
	if(scalar(@::CAENC111C_BIT_SLOTIN) eq 24){pop(@::CAENC111C_BIT_SLOTIN);}
	if($::Debug){print ">>SLOT Status is\n";}
	for($i=0;$i<23;$i++){
		if($::CAENC111C_BIT_SLOTIN[$i]=~/^1$/){
			if($::Debug){printf("[%02d:SCANNED]\t",$i+1);}
		}elsif($::CAENC111C_BIT_SLOTIN[$i]=~/^0$/){
			if($::Debug){printf("[%02d: EMPTY ]\t",$i+1);}
		}else{
			print "UNEXPECTED ERROR: DATA=[$::CAENC111C_BIT_SLOTIN[$i]] CSCAN\n";
			return('');
		}
	}
	if($::Debug){print "\n";}
	return(1);
}
#############################################################
## TEXTTERM
#############################################################
sub CAENC111CTEXTTERMINAL{
	my($cmd,$sizelen)=@_;
	my($RC,$retmsg)=$::camac->CMDSR("$cmd",$sizelen);
#	$::tak->Sleep(50);
	if($RC<0){
		$::CAENC111CError="Er: $RC,$retmsg";
		print "CMD EXECUTE ERROR: RC=[$RC] $cmd\n";
		return('');
	}
	($RC,$retmsg)=split(/\s/,$retmsg,2);
	if($RC<0){
		$::CAENC111CError="Ng: $RC,$retmsg";
		print "CMD EXECUTE ERROR: RC=[$RC] $cmd\n";
		return('');
	}
	if($retmsg eq ''){return("Ok:");}return("Ok: $retmsg");
}
#############################################################
## COMBO IsBusy Check
#############################################################
sub CAENC111CCheckComboIsBusyChanged{
	my($c1,$c2,$dest)=@_;unless($dest){$dest="System";}
	my($val,$changed)=(-1,0);
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	unless(CAENC111C_COMBOBUSYCHECK){return(1);}
	$::CAENC111CINTERNALError=0;
	unless($c1 or $c2){return('');}
	if($c1){
		my $changed1=0;
		($_,$val)=split(/\s/,CAENC111CTEXTTERMINAL("nim_testcombo 1",255),2);
#		$::tak->Sleep(50);
		if(~/^Ok:/){
			if($::CAENC111C_COMBOIsBusy{1} ne $val){
				if($val<=0){
					$::tak->Send("$nodename>$dest _ChangedComboIsBusy 1 0");
				}else{
					$::tak->Send("$nodename>$dest _ChangedComboIsBusy 1 1");
				}
				$::CAENC111C_COMBOIsBusy{1}=$val;
				$changed=1;
				$changed1=1;
			}
		}else{$::CAENC111CINTERNALError=1;return('');}
		if(1){
			$::tak->Sleep(40);
			$val=$::camac->CMDSR("nim_getcev 1",255);
#			$::tak->Sleep(50);
			if($val>=0){
				if($::CAENC111C_ComboEventCounter{1} ne $val){
					$::tak->Send("$nodename>$dest _ChangedValueComboEventCounter 1 $val");
					$::CAENC111C_ComboEventCounter{1}=$val;
				}
			}else{$::CAENC111CINTERNALError=1;return('');}
		}
	}
	$::tak->Sleep(40);
	if($c2){
		my $changed2=0;
		($_,$val)=split(/\s/,CAENC111CTEXTTERMINAL("nim_testcombo 2",255),2);
#			$::tak->Sleep(50);
		if(~/^Ok:/){
			if($::CAENC111C_COMBOIsBusy{2} ne $val){
				if($val<=0){
					$::tak->Send("$nodename>$dest _ChangedComboIsBusy 2 0");
				}else{
					$::tak->Send("$nodename>$dest _ChangedComboIsBusy 2 1");
				}
				$::CAENC111C_COMBOIsBusy{2}=$val;
				$changed=1;
				$changed2=1;
			}
		}else{$::CAENC111CINTERNALError=1;return('');}
		if(1){
			$::tak->Sleep(40);
			$val=$::camac->CMDSR("nim_getcev 2",255);
#			$::tak->Sleep(50);
			if($val>=0){
				if($::CAENC111C_ComboEventCounter{2} ne $val){
					$::tak->Send("$nodename>$dest _ChangedValueComboEventCounter 2 $val");
					$::CAENC111C_ComboEventCounter{2}=$val;
		 		}
			}else{$::CAENC111CINTERNALError=1;return('');}
		}
	}
	if($changed){return(1);}
	return(0);
}
#############################################################
## NIMIN Event Counter
#############################################################
sub CAENC111CCheckNIMInEventCounterIsChanged{
	my($c1,$c2,$dest)=@_;unless($dest){$dest="System";}
	my($val,$changed)=(-1,0);
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	unless(CAENC111C_NIMINEVTCOUNTERCHANGED){return(1);}
	$::CAENC111CINTERNALError=0;
	unless($c1 or $c2){return('');}
	if($c1){
		($_,$val)=split(/\s/,CAENC111CTEXTTERMINAL("nim_geticnt 1",255),2);
#		$::tak->Sleep(50);
		if(~/^Ok:/){
			if($::CAENC111C_NIMInEventCounter{1} ne $val){
				$::tak->Send("$nodename>$dest _ChangedValueNIMINEventCounter 1 $val");
				$::CAENC111C_NIMInEventCounter{1}=$val;
				$changed=1;
			}
		}else{$::CAENC111CINTERNALError=1;return('');}
	}
	if($c2){
		$::tak->Sleep(40);
		($_,$val)=split(/\s/,CAENC111CTEXTTERMINAL("nim_geticnt 3",255),2);
#		$::tak->Sleep(50);
		if(~/^Ok:/){
			if($::CAENC111C_NIMInEventCounter{3} ne $val){
				$::tak->Send("$nodename>$dest _ChangedValueNIMINEventCounter 3 $val");
				$::CAENC111C_NIMInEventCounter{3}=$val;
				$changed=1;
			}
		}else{$::CAENC111CINTERNALError=1;return('');}
	}
	if($changed){return(1);}
	return(0);
}
#############################################################
## INHIBIT CHECK
#############################################################
sub CAENC111CCheckLAMChanged{
	my $hex=shift;
	my $lack=shift;
	my $dest=shift;unless($dest){$dest="System";}
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	my @bits=();
	my($i,$nname);
	my $changed=0;

	$::CAENC111CINTERNALError=0;
	if($hex eq ''){
		$::tak->Sleep(40);
		my($RC,$retmsg)=$::camac->CLMR();
#		$::tak->Sleep(50);
		if($RC<0){
			$::CAENC111CINTERNALError=1;
			$::CAENC111CError="Er: $RC,$retmsg";
			print "CONNECTION ERROR: RC=[$RC] CLMR\n";
			return('');
		}else{
			$hex=sprintf("%06x",$retmsg);
		}
	}
	@bits = reverse(split(//,unpack("B24", pack("H6","$hex"))));
	for($i=1;$i<=23;$i++){
		if(($lack) or ($::CAENC111C_LAM[$i-1] ne $bits[$i-1])){
			$::CAENC111C_LAM[$i-1]=$bits[$i-1];
			if($bits[$i-1] eq 1){
				$nname=MAIN_getnodenamebyno($i);
				unless($nname eq ''){
					$::tak->Send("$nname>$dest _ChangedLAMIsBusy ".$bits[$i-1]);
				}
				$changed=1;
			}else{
				$nname=MAIN_getnodenamebyno($i);
				unless($nname eq ''){
					$::tak->Send("$nname>$dest _ChangedLAMIsBusy ".$bits[$i-1]);
				}
				$changed=1;
			}
		}
	}
	return($changed);
}
#############################################################
## IRQ handler called by CAMAC HANDLER
#############################################################
sub CAENC111CIRQ{
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	my ($irq_cmd, $irq_data)=@_;
	my ($bit,$changed1,$changed2)=('',0,0);
	
	if($irq_cmd=~/^C$/){
		$irq_data=~/^\S\S\S\S\S\S\S(\S)$/;$bit=scalar($1);
		if(($bit&0x01) eq 0x01){
			print ">>combo1 interrupt pending\n";
			unless(CAENC111C_COMBOBUSYCHECK){return(1);}
#			$::CAENC111C_COMBOIsBusy{1}=1;
#			$::tak->Send("$nodename>System _ChangedComboIsBusy 1 1");
#			$changed1=CAENC111CCheckComboIsBusyChanged(1,0);
		}
		if(($bit&0x02) eq 0x02){
			print ">>combo2 interrupt pending\n";
			unless(CAENC111C_COMBOBUSYCHECK){return(1);}
#			$::CAENC111C_COMBOIsBusy{2}=1;
#			$::tak->Send("$nodename>System _ChangedComboIsBusy 2 1");
#			$changed2=CAENC111CCheckComboIsBusyChanged(0,1);
		}
		if(($bit&0x04) eq 0x04){
			print ">>dtc combo1 interrupt pending\n";
			unless(CAENC111C_COMBOBUSYCHECK){return(1);}
			unless($changed1){
#				$changed1=CAENC111CCheckComboIsBusyChanged(1,0);
			}
		}
		if(($bit&0x08) eq 0x08){
			print ">>dtc combo2 interrupt pending\n";
			unless(CAENC111C_COMBOBUSYCHECK){return(1);}
			unless($changed2){
#				$changed2=CAENC111CCheckComboIsBusyChanged(0,1);
			}
		}
	}elsif($irq_cmd=~/^D$/){
		print ">>DEFAULT pushbutton pressure\n";
	}elsif($irq_cmd=~/^L$/){
		$irq_data=~/^\S\S(\S\S\S\S\S\S)$/;
		print ">>LAM is changed $1\n";
		CAENC111CCheckLAMChanged($1);
	}
	return(1);
}
#############################################################
## Interval handler called by CAMAC HANDLER
#############################################################
sub CAENC111CInterval{
	my $nodename=$::CAENC111C_NODENAME;	#STARS NODENAME
	
	if($::CAENC111CINTERNALError){return(0);}

	if(tv_interval($::CAENC111CIntervalTime)>CAENC111C_INTERVAL_REFRESH){
		caenc111c::IRQ_Handler();	#Check CAMAC IRQ

		if($::CAENC111CINTERNALError){return(0);}
		$::tak->Sleep(40);
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		CAENC111CCheckInhibitChanged();
		$::Debug=$debug;
		
#		if($::CAENC111CINTERNALError){return(0);}
#		$::tak->Sleep(40);
#		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
#		CAENC111CCheckComboIsBusyChanged(1,1);
#		$::Debug=$debug;
#		if($::CAENC111CINTERNALError){return(0);}
#		$::tak->Sleep(40);
#		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
#		CAENC111CCheckNIMInEventCounterIsChanged(1,1);
#		$::Debug=$debug;

		if($::CAENC111CINTERNALError){return(0);}
		my $debug=$::Debug;if($::Debug eq 1){$::Debug=0;}
		$::tak->Sleep(40);
		CAENC111CCheckLAMChanged('');
		$::Debug=$debug;

		$::CAENC111CIntervalTime=[gettimeofday];
	}
	return(1);
}
#############################################################
## Init Function
#############################################################
sub CAENC111CInit{
	my $nodename=shift;	#STARS NODENAME
	my $N=shift;		#SLOT NO: Ignore
	my $RC;
	my $i;
	$::CAENC111C_NODENAME=$nodename;
	unless(CAENC111CCheckInhibitChanged()){die;}
	$::tak->Sleep(40);
	
#	unless(CAENC111CCheckComboIsBusyChanged(1,1)){die;}
#	$::tak->Sleep(40);
#	unless(CAENC111CCheckNIMInEventCounterIsChanged(1,1)){die;}
#	$::tak->Sleep(40);

	unless(CAENC111CCheckLAMChanged('',1)){die;}
	$::tak->Sleep(40);
	if(($RC=$::camac->CRIRQ(\&MAIN_irq))<0){
		print "CONNECTION ERROR: RC=[$RC] CRIRQ\n";die;
	}
	return(CAENC111Cset_help_list());#make helptable.
}
#############################################################
## handler called by Controller
#############################################################
sub CAENC111CHandler{
## ToDo: Please modify handler sub routine.
##  (The handler sub routine will be called when client
##  receives a message from a Stars server.)
	my ($from, $to, $mess) = @_;
	my $rt='';
	my $addok=1;
	$::CAENC111CError='';

##Ignore Event/Reply Messages ##
	if($mess=~/^[_@]/){return;}
	
	$mess=~/^(\S+)/;
##Command Support help No Support
	if(!defined($::CAENC111Chelpcntrl{$1})){#Command Valid Check.
		{$::CAENC111CError="Er: Bad Command.";}
	}elsif($mess=~/^hello$/){
		$addok=0;$rt='nice to meet you.';
	}elsif($mess=~/^help$/){
		$addok=0;$rt=CAENC111Cget_help_list('Cntrl');
	}elsif($mess=~/^help\s(.+)$/){
		$addok=0;$rt=CAENC111Cget_help_list('Cntrl',$1);
	}elsif($mess=~/^flushdata$/){
		$::CAENC111C_FLAG_INHIBIT=-1;		#Inhibit 0 or 1.
		$::CAENC111C_COMBOIsBusy{1}=-1;		#COMBO1 Busy or not.
		$::CAENC111C_COMBOIsBusy{2}=-1;		#COMBO2 Busy or not.
		$::CAENC111C_ComboEventCounter{1}=-1;
		$::CAENC111C_ComboEventCounter{2}=-1;
		$::CAENC111C_NIMInEventCounter{1}=-1;	#NIMIN1EventCounter Value.
		$::CAENC111C_NIMInEventCounter{3}=-1;	#NIMIN3EventCounter Value.
		CAENC111CCheckInhibitChanged();
		CAENC111CCheckComboIsBusyChanged(1,1);
		CAENC111CCheckNIMInEventCounterIsChanged(1,1);
		CAENC111CCheckLAMChanged('',1);
		$rt="Ok:";
	}elsif($mess=~/^flushdatatome$/){
		$::CAENC111C_FLAG_INHIBIT=-1;		#Inhibit 0 or 1.
		$::CAENC111C_COMBOIsBusy{1}=-1;		#COMBO1 Busy or not.
		$::CAENC111C_COMBOIsBusy{2}=-1;		#COMBO2 Busy or not.
		$::CAENC111C_ComboEventCounter{1}=-1;
		$::CAENC111C_ComboEventCounter{2}=-1;
		$::CAENC111C_NIMInEventCounter{1}=-1;	#NIMIN1EventCounter Value.
		$::CAENC111C_NIMInEventCounter{3}=-1;	#NIMIN3EventCounter Value.
		CAENC111CCheckInhibitChanged("$from");
		CAENC111CCheckComboIsBusyChanged(1,1,"$from");
		CAENC111CCheckNIMInEventCounterIsChanged(1,1,"$from");
		CAENC111CCheckLAMChanged('',1,"$from");
		$rt="Ok:";
### Init
	}elsif($mess=~/^(CSCAN|RunSlotScan)$/){
		if(CAENC111CScan()){$rt="Ok: ".join(" ",@::CAENC111C_BIT_SLOTIN);}
	}elsif($mess=~/^(CCCZ|RunDatawayInit)$/){
		my($rc,$retmsg)=$::camac->CCCZ();
		if($rc>=0){$rt="Ok:";CAENC111CCheckInhibitChanged();
		}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^(CCCC|RunCrateClear)$/){
		my($rc,$retmsg)=$::camac->CCCC();
		if($rc>=0){$rt="Ok:";CAENC111CCheckInhibitChanged();
		}else{$::CAENC111CError="$rc";}
### Inhibit
	}elsif($mess=~/^(CTCI|GetInhibitIsBusy)$/){
		unless(CAENC111CCheckInhibitChanged('') eq ''){
			$rt="Ok: $::CAENC111C_FLAG_INHIBIT";
		}
	}elsif($mess=~/^(CCCI|SetInhibit)\s([01])$/){
		my($rc,$retmsg)=$::camac->CCCI($2);
		if($rc>=0){$rt="Ok:";CAENC111CCheckInhibitChanged();
		}else{$::CAENC111CError="$rc";}
### LAM
	}elsif($mess=~/^(CTLM|GetLAMIsBusy)\s([1-9]|1[0-9]|2[0-3])$/){
		my($rc,$retmsg)=$::camac->CTLM($2);
		if($rc>=0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^(CLMR|GetLAMRegister)$/){
		my($rc,$retmsg)=$::camac->CLMR();
		if($rc>=0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^LACK$/){
		my($rc,$retmsg)=$::camac->LACK();
		if($rc>=0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$rc";}
### NIM Input
	}elsif($mess=~/^GetValueNIMInAll$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getin",255);
	}elsif($mess=~/^GetValueNIMIn\s([1-4])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getins $1",255);
#	}elsif($mess=~/^SetNIMInEventCounterSettings\s([13])\s([01])\s([01])\s([01])$/){
#		$rt=CAENC111CTEXTTERMINAL("nim_setievcnt $1 $2 $3 $4",255);
	}elsif($mess=~/^GetNIMInEventCounterSettings\s([13])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getievcnt $1",255);
	}elsif($mess=~/^GetValueNIMInEventCounter\s([13])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_geticnt $1",255);
	}elsif($mess=~/^ResetNIMInEventCounter\s([13])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_reseticnt $1",255);
### NIM Output
	}elsif($mess=~/^GetValueNIMOutAll$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getout",255);
	}elsif($mess=~/^GetValueNIMOut\s([1-4])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getouts $1",255);
	}elsif($mess=~/^SetValueNIMOutAll\s([0|1])\s([0|1])\s([0|1])\s([0|1])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_setout $1 $2 $3 $4",255);
	}elsif($mess=~/^SetValueNIMOut\s([1-4])\s(0|1)$/){
		$rt=CAENC111CTEXTTERMINAL("nim_setouts $1 $2",255);
### NIM Pulse
	}elsif($mess=~/^RunPulseGenerator\s(\d+)\s([1-7])\s([01])$/ and (1<=$1 and $1<=1023)){
		$rt=CAENC111CTEXTTERMINAL("nim_setpulse $1 $2 $3",255);
	}elsif($mess=~/^GetPulseGeneratorSettings$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getpulse",255);
	}elsif($mess=~/^StopPulseGenerator$/){
		$rt=CAENC111CTEXTTERMINAL("nim_pulseoff",255);
### Combo
	}elsif($mess=~/^ResetCombo\s([12])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_resetcombo $1 1",255);
		if($rt){$rt=CAENC111CTEXTTERMINAL("nim_cack $1",255);}
		if($rt){$rt="Ok:";}
	}elsif($mess=~/^GetComboIsBusy\s([12])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_testcombo $1",255);
	}elsif($mess=~/^GetValueComboDeadTimeCounter\s([12])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_getcdtc $1",255);
	}elsif($mess=~/^GetValueComboEventCounter\s([12])$/){
		my $rc=$::camac->CMDSR("nim_getcev $1",255);
		if($rc>=0){$rt=$rc;}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^ResetComboEventCounter\s([12])$/){
		$rt=CAENC111CTEXTTERMINAL("nim_resetcev $1",255);
### SEND COMMAND
	}elsif($mess=~/^CFSA\s(\S+)\s(\S+)\s(\S+)\s(\S+)$/){
		my($rc,$Q,$X,$DATA)=$::camac->CFSA($1,$2,$3,$4);
		if($rc>=0){$rt="Ok: $Q $X $DATA";}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^CSSA\s(\S+)\s(\S+)\s(\S+)\s(\S+)$/){
		my($rc,$Q,$X,$DATA)=$::camac->CSSA($1,$2,$3,$4);
 		if($rc>=0){$rt="Ok: $Q $X $DATA";}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^TEXTTERM\s(.+)$/){
		my($rc,$retmsg)=$::camac->CMDSR($1,255);
		if($rc>0){$retmsg=~s/^(\S+)\s*/$1\,/;
		$rt="Ok: $retmsg";
		}else{$::CAENC111CError="$rc"}
### BLK functions 07/07/27
	}elsif($mess=~/^BLKBUFFS\s(\d+)$/){
		my($rc,$retmsg)=$::camac->BLKBUFFS($1);
		if($rc>0){$rt="Ok:";}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^BLKBUFFG$/){
		my($rc,$retmsg)=$::camac->BLKBUFFG();
		if($rc>0){$retmsg=~s/^\S+\s+//;$rt="Ok: $retmsg";
		}else{$::CAENC111CError="$rc";}
	}elsif($mess=~/^BLK(S|F)S([B]?)\s([0-7])\s(\d+)\s(\d+)\s(\d+)$/){
		my($rc,$retmsg)=$::camac->BLKxS($2,$1,$3,$4,$5,$6,"","");
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}elsif($mess=~/^BLK(S|F)S\s(1[6-9]|2[0-7])\s(\d+)\s(\d+)\s(\d+)\s(.+)/){
		my($rc,$retmsg)=$::camac->BLKxS(0,$1,$2,$3,$4,$5,"",$6);
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}elsif($mess=~/^BLK(S|F)R([B]?)\s([0-7])\s(\d+)\s(\d+)\s(\d+)\s(\d+)$/){
		my($rc,$retmsg)=$::camac->BLKxR($2,$1,$3,$4,$5,$6,$7,"","");
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}elsif($mess=~/^BLK(S|F)R\s(1[6-9]|2[0-7])\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(.+)/){
		my($rc,$retmsg)=$::camac->BLKxR(0,$1,$2,$3,$4,$5,$6,"",$7);
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}elsif($mess=~/^BLK(S|F)A([B]?)\s([0-7])\s(\d+)\s(\d+)$/){
		my($rc,$retmsg)=$::camac->BLKxA($2,$1,$3,$4,$5,"","");
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}elsif($mess=~/^BLK(S|F)A\s(1[6-9]|2[0-7])\s(\d+)\s(\d+)\s(.+)/){
		my($rc,$retmsg)=$::camac->BLKxA(0,$1,$2,$3,$4,"",$5);
		if($rc>0){$rt="Ok: $retmsg";}else{$::CAENC111CError="$retmsg";}
	}else{
		$::CAENC111CError='Er: Bad Parameter.';
	}
## Response ##
	if(($rt eq '') and ($::CAENC111CError=~/^Ng:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC111CError");
	}elsif(($rt eq '') and ($::CAENC111CError=~/^Er:/)){
		$::tak->Send("$to>$from \@$mess $::CAENC111CError");
	}elsif($rt eq ''){
		$::tak->Send("$to>$from \@$mess Er: $::CAENC111CError");
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
sub CAENC111CRegister{
	my($nodename,$slotno,$counternodetag)=@_;
	my $i;
	my $rt=MAIN_RegisterModule2Controller("$nodename","24",\&CAENC111CInit,\&CAENC111CHandler,\&CAENC111CInterval,\&CAENC111CIRQ,"CAEN Model C111C","1.0");
	if($rt eq ''){die "Failed to register NODENAME[$nodename] SLOTNO[$slotno]\n.";}
	return(1);									
}
################################################################
## Help Function
################################################################
sub CAENC111Cget_help_list{
	my($target,$cmd)=@_;
	if($target eq 'Cntrl'){
		unless($cmd){return(join(" ", sort(keys(%::CAENC111Chelpcntrl))));}
		unless(defined($::CAENC111Chelpcntrl{$cmd})){
			return('Ng: Bad Command.');
		}
		return($::CAENC111Chelpcntrl{$cmd});
	}
}
sub CAENC111Cset_help_list{
	my @arrays=();
	my @cmds=();
	my $i;
	%::CAENC111Chelpcntrl=();
my $data=<<EOF;
hello#Returns 'nice to meet you.'
help#'help' => Show command list. 'help <command>' =>Show command help.
flushdata#Send Stars Event Messages to System.
flushdatatome#Send Stars Event Messages to fromnode.
CSCAN#Start Slot Scanning and returns status 1(in) or 0(empty) of all slots(1 to 23).
CCCZ|RunDatawayInit#Generate dataway initialize.
CCCC|RunCrateClear#Generate crate clear.
CFSA#args:F A N value =>execute CAMAC command with 16-bit data.
CSSA#args:F A N value =>execute CAMAC command with 24-bit data.
CTCI|GetInhibitIsBusy#Get dataway inhibit 0(reset) or 1(set).
CCCI|SetInhibit#args:0|1 Set dataway inhibit 0(reset) or 1(set).
CTLM|GetLAMIsBusy#args:1-23(Slot No) =>CAMAC test LAM on specified slotno and returns a LAM status 1(on) or 0(off).
CLMR|GetLAMRegister#Returns a value of current LAM register.
LACK#LAM acknowledge.
GetValueNIMInAll#Returns current value of all four NIM inputs.
GetValueNIMIn#args:1-4(NIM Input No) =>Returns a current value of specified NIM input.
GetValueNIMInEventCounter#args:1|3(NIM Input No) =>Returns a current value of specified NIM input's Event Counter.
ResetNIMInEventCounter#args:1|3(NIM Input No) =>Reset a specified NIM input's Event Counter.
GetValueNIMOutAll#Returns current values of all four NIM outputs.
GetValueNIMOut#args:1-4(NIM Output No) =>Returns a current value of specified NIM output.
SetValueNIMOutAll#args:0|1 0|1 0|1 0|1(values of NIM Output 1 to 4) =>Set values of all four NIM outputs.
SetValueNIMOut#args:1-4(NIM Output No) 0|1(value) =>Set a current value of specified NIM output.
RunPulseGenerator#args: 1-1023(period multiplier) 1-7(width level multiplier) 0|1(polarity) =>Start Pulse Generator using NIM Output 1 with configuration paramaters.
StopPulseGenerator#Stop Pulse Generator using NIM Output 1.
ResetComboEventCounter#args:1|2(Combo I/O No) =>Reset a specified COMBO I/O Event Counter.
ResetCombo#args:1|2(Combo I/O No) =>Reset a COMBO FF of specified COMBO I/O.
GetValueComboEventCounter#args:1|2(Combo I/O No) =>Returns a current value of specified COMBO I/O Event Counter.
GetComboIsBusy#args:1|2(Combo I/O No) =>Returns a COMBO busy status 1(busy) or 0(not) of specified COMBO I/O.
TEXTTERM#Execute CAMAC command in text mode.
BLKBUFFS#Block transfer buffer size set
BLKBUFFG#Block transfer buffer size get
BLKSS#Ascii Block transfer, 16-bit, Q-stop mode.
BLKFS#Ascii Block transfer, 24-bit, Q-stop mode.
BLKSR#Ascii Block transfer, 16-bit, Q-repeat mode.
BLKFR#Ascii Block transfer, 24-bit, Q-repeat mode.
BLKSA#Ascii Block transfer, 16-bit, address scan mode.
BLKFA#Ascii Block transfer, 24-bit, address scan mode.
BLKSSB#Binary only read block transfer, 16-bit, Q-stop mode.
BLKFSB#Binary only read block transfer, 24-bit, Q-stop mode.
BLKSRB#Binary only read block transfer, 16-bit, Q-repeat mode.
BLKFRB#Binary only read block transfer, 24-bit, Q-repeat mode.
BLKSAB#Binary only read block transfer, 16-bit, address scan mode.
BLKFAB#Binary only read block transfer, 24-bit, address scan mode.
EOF
#Removed help
#Bug remove
#SetNIMInEventCounterSettings#args: 1|3(NIM in no) 0|1(enable) 0|1(polarity) 0|1(externReset) =>Sets specified NIM input's Event Counter Settings.
#GetNIMInEventCounterSettings#args: 1|3(NIM Input No) =>Returns a specified NIM input's Event Counter Settings.
#just remove
#GetPulseGeneratorSettings#Return configuration paramaters of Pulse Generator using NIM Output 1.
#GetValueComboDeadTimeCounter#args:1|2(combo no) =>Returns current value of COMBO Dead Time Counter.
	$data=$data.MAIN_mainhelp();
	foreach (split(/\n/,$data)){
		@arrays=split(/#/,$_);
		@cmds=split(/\|/,$arrays[0]);
		for($i=0;$i<@cmds;$i++){
			unless($cmds[$i] eq ''){
				$::CAENC111Chelpcntrl{$cmds[$i]}=$arrays[1];
			}
		}
	}
	return(1);
}
1
