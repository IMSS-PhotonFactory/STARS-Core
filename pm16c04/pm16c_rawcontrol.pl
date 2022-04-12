## This library for pm16c04 raw control, for like spec.

sub mysubchangevaluecmd{
	my $cmd=shift;
	my $ch=shift;
	my $flg=0;
	$mn = Ctl_GetSelected($ch);
	if($ch eq 'A'){
		if($::Flg_Busy_A eq ''){
			$flg++;
			$::Flg_Busy_A=$mn;
		}
	}elsif($ch eq 'B'){
		if($::Flg_Busy_B eq ''){
			$flg++;
			$::Flg_Busy_B=$mn;
		}
	}elsif($ch eq 'C'){
		if($::Flg_Busy_C eq ''){
			$flg++;
			$::Flg_Busy_C=$mn;
		}
	}elsif($ch eq 'D'){
		if($::Flg_Busy_D eq ''){
			$flg++;
			$::Flg_Busy_D=$mn;
		}
	}
	if($flg){
		mydevwrite("$cmd"); stars->Sleep(WAIT_MEMWRITE);
		mystarssend("$::NodeName.".num2name($mn).">System _ChangedIsBusy 1");
		$::Interval_Time = INTERVAL_RUN;
		if($::Flg_Busy_A ne '' and $::Flg_Busy_B ne ''  and $::Flg_Busy_C ne ''  and $::Flg_Busy_D ne ''){
			$::tak->Send("System _ChangedCtlIsBusy 1");
		}
	}
	return($flg);
}

sub sendrawcommand{
	my $cmd=uc(shift);
	my $execflg=0;
	my $rt='';
	my $ch='';
	my $mn='';
	my $arg='';
	my $buf;
	$cmd=~s/^\s+//;$cmd=~s/\s+$//;
	
	if($cmd eq ''){return('Ok:');
	#### Remote/Local
	}elsif(($cmd=~/^S1[RL]/) or	($cmd=~/^(LOC|REM)/)) {
		mydevwrite("$cmd");stars->Sleep(WAIT_SELECT);$execflg++;
		Ctl_GetFunction();
	#### CHANNEL SELECT
	}elsif(($cmd=~/^S1[1256]/) or ($cmd=~/^SETCH/)){
		mydevwrite("$cmd");stars->Sleep(WAIT_SELECT);$execflg++;
   	#### READ BUSY STATUS CHECK
	}elsif(($cmd=~/^S2[1357]/) or ($cmd=~/^STS\?/)){
		mydevwrite("$cmd");stars->Sleep(WAIT_MEMWRITE);$execflg++;
		$rt=mydevread();
		if($cmd=~/STS\?/){
			$rt=~/^\S\S\S\S\S\/\S\S\S\S\/\S\S\S\S\/(\S\S)(\S\S)(\S\S)(\S\S)/;
			if($1 & 1){}elsif($2 & 1){}elsif($3 & 1){}elsif($4 & 1){
			}else{
				if($::PM16CX){intervalX();}else{interval();}
			}
		}else{
			$rt=~/^R(\S\S)/;
			unless($1 & 1){if($::PM16CX){intervalX();}else{interval();}}
		}
		#Busy off -> exec interval to sync
	#### PAUSE/HOLD/STOP
	}elsif($cmd=~/^S3[0189](16|17|18|19|40|80)/){
		$arg=$1;
		if($arg eq '18'){stars->Sleep(WAIT_HOLD_OFF);}
		mydevwrite("$cmd");
		if($arg eq '19'){
			stars->Sleep(WAIT_HOLD_ON);
		}else{
			stars->Sleep(WAIT_MEMWRITE);
		}
		$execflg++;
	#### MOVE
	}elsif($cmd=~/^S3([0189])(08|09|0C|0D|0E|0F|1E|1F)/){
		$ch=$1;
		if($ch=~s/0/A/){}elsif($ch=~s/1/B/){}elsif($ch=~s/8/C/){}elsif($ch=~s/9/D/){}
		$execflg+=mysubchangevaluecmd($cmd,$ch);
	}elsif($cmd=~/^S3([23AB])/){
		$ch=$1;
		if($ch=~s/2/A/){}elsif($ch=~s/3/B/){}elsif($ch=~s/A/C/){}elsif($ch=~s/B/D/){}
		$execflg+=mysubchangevaluecmd($cmd,$ch);
	}elsif($cmd=~/^(RT|F)HP([ABCD])/){
		$ch=$2;
		$execflg+=mysubchangevaluecmd($cmd,$ch);
	#### PRESET
	}elsif(($cmd=~/^S5(\S)[012]/) or ($cmd=~/^PS(\S)/)){
		$mn=$1;
		if($mn=~/^[0-9A-F]$/){
			mydevwrite("$cmd");stars->Sleep(WAIT_MEMWRITE);$execflg++;
			mydevwrite("S4${mn}0");
			$buf=mydevread(); $buf=~/^R(\S+)/; $buf=hex($1);
			$mn=hex($mn);
			$::tak->Send("$::NodeName.".num2name($mn).">System _ChangedValue $buf");
		}
   	#### WRITE BACKLASH
	}elsif($cmd=~/^B(\S)(.*)/){
		$mn=$1;
		$arg=$2;
		if($arg!~/\?/){
			if($mn=~/^[0-9A-F]$/){
				mydevwrite("$cmd");stars->Sleep(WAIT_MEMWRITE);$execflg++;
				$mn=hex($mn);
				Motor_GetCancelBacklash($mn);
			}
		}
	#### PM16CX MOVE
	}elsif(
	    ($cmd=~/^(ABS|REL)(\S)/) or
        ($cmd=~/^(CSCAN[PN])(\S)/) or
        ($cmd=~/^(SCAN[PN])(\S)/) or
        ($cmd=~/^(SCANH[PN])(\S)/) or
        ($cmd=~/^(FDHP)(\S)/) or
        ($cmd=~/^(GTHP)(\S)/) or
        ($cmd=~/^(JOG[PN])(\S)/)
        )
    {
		$mn=$2;
		$ch='';
		if($mn=~/^[0-9A-F]$/){
			$mn=hex($mn);
			my($cha,$chb,$chc,$chd)  = Ctl_GetSelected();
			if($cha == $mn){$ch='A';
			}elsif($chb == $mn){$ch='B';
			}elsif($chc == $mn){$ch='C';
			}elsif($chd == $mn){$ch='D';
			}else{
				if(not Ctl_IsBusy('A')){
					if(Ctl_Select('A', $mn) eq ''){}else{$ch='A';}
				}elsif(not Ctl_IsBusy('B')){
					if(Ctl_Select('B', $mn) eq ''){}else{$ch='B';}
				}elsif(not Ctl_IsBusy('C')){
					if(Ctl_Select('C', $mn) eq ''){}else{$ch='C';}
				}elsif(not Ctl_IsBusy('D')){
					if(Ctl_Select('D', $mn) eq ''){}else{$ch='D';}
				}
			}
			$execflg+=mysubchangevaluecmd($cmd,$ch);
		}
	#### PM16CX MOVE-INTERPOLATION
	}elsif(($cmd=~/^C([01])[AR][LCA][PNC](\S)(\S)/)) {
 		$ch=$1;
 		$arg = $1;
    	my $mn1=$2;
    	my $mn2=$3;
		if(($mn1=~/^[0-9A-F]$/) and ($mn2=~/^[0-9A-F]$/)){
	    	if($arg eq 0){
	    		$mn1=hex($mn1);
		    	$mn2=hex($mn2);
				if(CtlX_SelectForce('A', $mn1) eq ''){$ch='';}
				if(CtlX_SelectForce('B', $mn2) eq ''){$ch='';}
				if($ch ne ''){
					$::Flg_Busy_A=$mn1;
					$::Flg_Busy_B=$mn2;
				}
   		 	}elsif($arg eq 1){
	    		$mn1=hex($mn1);
		    	$mn2=hex($mn2);
				if(CtlX_SelectForce('C', $mn1) eq ''){$ch='';}
				if(CtlX_SelectForce('D', $mn2) eq ''){$ch='';}
				if($ch ne ''){
					$::Flg_Busy_C=$mn1;
					$::Flg_Busy_D=$mn2;
				}
    		}
			mydevwrite("$cmd");stars->Sleep(WAIT_MEMWRITE);$execflg++;
			if($ch ne ''){
				$::tak->Send("$::NodeName.".num2name($mn1).">System _ChangedIsBusy 1");
				$::tak->Send("$::NodeName.".num2name($mn2).">System _ChangedIsBusy 1");
				$::Interval_Time = INTERVAL_RUN;
				if($::Flg_Busy_A ne '' and $::Flg_Busy_B ne ''  and $::Flg_Busy_C ne ''  and $::Flg_Busy_D ne ''){
					$::tak->Send("System _ChangedCtlIsBusy 1");
				}
			}
		}
	}
	unless($execflg){
		mydevwrite("$cmd");stars->Sleep(WAIT_MEMWRITE);$execflg++;
		$buf=mydevread(0.1);
		if($buf){if($buf!~/Timeout/){$rt=$buf;}}
	}
	if($rt eq ''){
		$rt="Ok:";
	}else{
		$rt="Ok: $rt";
	}
	return($rt);
}
1;