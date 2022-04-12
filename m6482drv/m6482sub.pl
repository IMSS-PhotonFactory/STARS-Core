###################################
# Globals
###################################
%::MODEL6482_KEITHLEY=();
%::CMD_KEITHLEY=();
%::PRE_KEITHLEY=();
%::CHECK_KEITHLEY=();
%::VER_KEITHLEY=();
%::HELP_KEITHLEY=();
setCMDTBL();

###################################
# Post Functions
###################################
sub postConvertChannelCommand{
	my $val=shift;
	my $ch=shift;
	$ch=$ch+1;
	if($val=~s/(\\\\CH)(\+)(\d+)/$1/){
		$ch = $ch+$3;
	}		
	$val=~s/\\\\CH/$ch/;
	return($val);
}
sub IsChannelCommand{
	my $val=shift;
	if($val=~/(\\\\CH)/){
		return(1);
	}else{
		return(0);
	}
}

###################################
# Check Functions
###################################
sub checkArgMissing{
	my $val=shift;
	if($val eq ''){
		$::Error=MSG_ARGMISSING;
		return(STAT_ERR);
	}
	return(STAT_OK);
}
#--------------------------------------------------------------------
sub convEtoN{
	my $val=uc(shift);
	my($v,$sign,$sign2)=('',1,1);
	if($val=~/^(-?)(\d*)(.?)(\d*)[E](-?)(\d+)$/){
		if($1 eq '-'){$sign=-1;}
		if($5 eq '-'){$sign2=-1;}
		unless("$2$4" eq ''){
			if($3 eq '.'){$v="$2.$4";}else{$v="$2$4";}
			$v=$sign*scalar($v)*(10**($sign2*$6));
		}
	}elsif($val=~/^(-?)(\d*)(.?)(\d*)$/){
		if($1 eq '-'){$sign=-1;}
		unless("$2$4" eq ''){
			if($3 eq '.'){$v="$2.$4";}else{$v="$2$4";}
			$v=$sign*scalar($v);
		}
	}
	return($v);
}

#--------------------------------------------------------------------
sub checkPreGetValue{
	my $val=uc(shift);
	my $ch=shift;
	my $rt=devAct(':TRAC:POIN:ACT?');if($rt eq STAT_ERR){return($rt);}
	unless($rt<=0){
		return(STAT_OK);
	}else{
		$::Error='Ng: No Data.';
		return(STAT_ERR);
	}
}

sub checkONOFF{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($val=~/^(0|1|OFF|ON)$/){
		return($val);
	}else{
		$::Error='Bad Parameter. Specify 1|ON to enable the operation, or 0|OFF to disable the operation.';
		return(STAT_ERR);
  	}
}
sub checkRangeMinMax2{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(abs($v)<=(9.99999)*(10**20)){
		return($v);
	}else{
		$::Error='Specify the number: -9.99999e20 to 9.99999e20.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkMathFormat{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(MXB|REC|LOG10)$/){
		return($val);
	}else{
		$::Error='Specify MXB(mX+B) or REC(iprocal m/X+b) or LOG10.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkKMathMBFactor{
	my $val=uc(shift);
	my $ch=shift;
	return(checkRangeMinMax2($val));
}
#--------------------------------------------------------------------
sub checkKMathUnits{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	
	if($val=~/^[A-Z]$/){
		return('"'.$val.'"');
	}elsif($val=~/^[\[|\]|\\]$/){
		return("'".$val."'");
	}else{
#		$::Error="Specify 1 character: A-Z or \'[\' or \']\' or \'\\'.";
#		return(STAT_ERR);
	}
	return($val);
}
#--------------------------------------------------------------------
sub checkPreGetValueKMath{
	my $val=uc(shift);
	my $ch=shift;
	$ch = $ch+1;
	my $rt=devAct(":CALC$ch:STAT?");if($rt eq STAT_ERR){return($rt);}
	if($rt=~/^(ON|1)$/){
		$rt=checkPreGetValue();if($rt eq STAT_ERR){return($rt);}
		return(STAT_OK);
	}else{
		$::Error='Ng: Set MathEnable ON before.';return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkCalc2InputPath{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(CALC|SENS)[12]$/){
		return($val);
	}else{
		$::Error='Specify CALC(ulate[1/2]) or SENS(e[1/2]).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkMathRatioFormat{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(MXB|REC|LOG10)$/){
		return($val);
	}else{
		$::Error='Specify MXB(mX+B) or REC(iprocal m/X+b) or LOG10.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkCalc2Range{
	my $val=uc(shift);
	return(checkRangeMinMax2($val));
}
#--------------------------------------------------------------------
sub checkPreGetValueREL{
	my $val=uc(shift);
	my $ch=shift;
	$ch = $ch+3;
	my $rt=devAct(":CALC$ch:NULL:STAT?");if($rt eq STAT_ERR){return($rt);}
	if($rt=~/^(ON|1)$/){
		$rt=checkPreGetValue();if($rt eq STAT_ERR){return($rt);}
		return(STAT_OK);
	}else{
		$::Error='Ng: Set RELEnable ON before.';return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTRCSTATICTYPE{
	my $val=uc(shift);
	my $ch=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(MIN|MAX|MEAN|SDEV|PKPK)$/){
		return($val);
	}else{
		$::Error='Specify MEAN or SDEV(iation) or MAX(imum) or MIN(imum) or PKPK.';
		return(STAT_ERR);
	}
}	
#--------------------------------------------------------------------
sub checkDisplayDigits{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^[4-7]$/){
		return($val);
	}else{
		$::Error='Specify the Number: 4 to 7.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkDisplayMode{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
#	return($val);

	if($val=~/^(CALC(ULATE)?[3456]|DUAL)$/){
		return($val);
	}else{
		$::Error='Specify the mode: CALC3,CALC4,CALC5,CALC6 or DUAL.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkDATAFORMAT{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(ASC|REAL|32|SRE)$/){
		return($val);
	}else{
		$::Error='Specify ASC(ii) or REAL or 32 or SRE(al).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkDATAELEMENTS{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	foreach (split(/\,/,$val)){
		unless(/^(READ|UNIT|TIME|STAT)$/){
			$::Error="Specify among READ(ing),UNIT(s),TIME and STAT(us).";
			return(STAT_ERR);
		}
	}
	return($val);
}
#--------------------------------------------------------------------
sub checkCALCDATAELEMENTS{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	foreach (split(/\,/,$val)){
		unless(/^(READ|UNIT|TIME|STAT)$/){
			$::Error="Specify among READ(ing),UNIT(s),TIME and STAT(us).";
			return(STAT_ERR);
		}
	}
	return($val);
}
#--------------------------------------------------------------------
sub checkTRACEDATAELEMENTS{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	foreach (split(/\,/,$val)){
		unless(/^(READ|UNIT|TIME|STAT)$/){
			$::Error="Specify among READ(ing),UNIT(s),TIME and STAT(us).";
			return(STAT_ERR);
		}
	}
	return($val);
}
#--------------------------------------------------------------------
sub checkLineFrequency{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(50|60)$/){
		return($val);
	}else{
		$::Error='Specify the number: 50 or 60.';
		return(STAT_ERR);
  	}
}
#--------------------------------------------------------------------
sub syncLineFrequency{
	my $val=shift;
	my $lfr=devAct(':SYST:LFR?');
	unless($lfr){
		return(STAT_ERR);
	}else{
		$::LINE_FREQUENCY=$lfr;
		return(STAT_OK);
}	}
#--------------------------------------------------------------------
sub checkAmpNPLC{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d*)(.?)(\d*)$/){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}else{
		if($val>=0.01 and $val<=($::LINE_FREQUENCY/10)){
			return($val);
		}else{
			$::Error='Specify the number: 0.01 to 6.0 if LineFrequency:60Hz, or 5.0 if LineFrequency:50Hz).';
			return(STAT_ERR);
		}
	}
}
#--------------------------------------------------------------------
sub checkAmpRANGE{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		return(STAT_ERR);
	}elsif($v<=2.1*(10**(-2)) and $v>=2.1*(10**(-9))){
		return($v);
	}else{
		$::Error='Specify the number: -21E-3(amps) to 21E-3(amps).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTCON{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(MOV|REP)$/){
		return($val);
	}else{
		$::Error='Specify REP(eat) or MOV(ing).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkAVGCOUNT{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d*)(.?)(\d*)$/){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}else{
		if($val>=1 and $val<=100){
			return($val);
		}else{
			$::Error='Specify the number: 2 to 100.';
			return(STAT_ERR);
		}
	}
}
#--------------------------------------------------------------------
sub checkADVNTOL{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d+)$/){
		$::Error='Invalid numeric format.';
		return(STAT_ERR);
	}else{
		if($val>=0 and $val<=105){
			return($val);
		}else{
			$::Error='Specify the number: 0 to 100.';
			return(STAT_ERR);
		}
	}
}
#--------------------------------------------------------------------
sub checkMEDRANK{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d+)$/){
		$::Error='Invalid numeric format.';
		return(STAT_ERR);
	}else{
		if($val>=1 and $val<=5){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 5.';
			return(STAT_ERR);
		}
	}
}

#--------------------------------------------------------------------
sub checkDataStatistic{
	my $val=uc(shift);
#	return(STAT_OK);
	my $rt=devAct(":TRAC:POIN:ACT?");
	unless($rt eq STAT_ERR){
		if($rt<=0){
			$::Error='Ng: No Data';
			return(STAT_ERR);
		}elsif($rt eq 1){
			$::Error='Ng: Only 1 data in buffer. More than 2 Data needed.';
			return(STAT_ERR);
		}else{
			return(STAT_OK);
		}
	}else{
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTRCFEED{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(SENS1|CALC|CALC2)$/){
		return($val);
	}else{
		$::Error='Specify CALC(ulate[1]) or CALC2(CALCulate2) or SENS1(SENse[1]).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTRCTIMEFORMAT{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
#	return($val);

	if($val=~/^(ABS(OLUTE)?|DELT(A)?)$/){
		return($val);
	}else{
		$::Error='Specify ABS(olute) or DEL(ta).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTRCPOINTS{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	unless($val=~/^(-?)(\d+)$/){
		$::Error='Invalid numeric format.';
	}else{
		if($val>=1 and $val<=3000){
			return($val);
		}else{
			$::Error='Specify size of buffer (1 to 3000).';
		}
	}
	return(STAT_ERR);
}	
#--------------------------------------------------------------------
sub checkTRCFEEDCONTROL{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($val=~/^(NEVER|NEXT)$/){
		return($val);
	}else{
		$::Error='Specify buffer control mode (NEVER or NEXT).';
		return(STAT_ERR);
	}
}	
#--------------------------------------------------------------------
sub checkTRIGArmSource{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($val=~/^(BUS|TLIN|MAN)$/){
		$::Error='Ng: Sorry. BUS,TLIN(k),MAN(aual) this program not supported.';
		return(STAT_ERR);
	}
	return($val);
	
	if($val=~/^(IMM|TIM)$/){
		return($val);
	}elsif($val=~/^(BUS|TLINK|MAN)$/){
		$::Error='Sorry. BUS, TLIN(k), or MAN(ual) this program version not support.';
		return(STAT_ERR);
	}else{
		$::Error='Specify IMM(ediate) or TIME(er).';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub syncTRIGArmSource{
	my($rt,$autosetflg)=@_;
	my $src=devAct(':ARM:SOUR?');
	unless($src){
		return(STAT_ERR);
	}else{
		unless(checkTRIGArmSource($src)){
			if($autosetflg){
				return(devSend(':ARM:SOUR IMM'));
			}else{
				return(STAT_ERR);
			}
		}else{
			$::ARM_SOURCE=$src;
			return(STAT_OK);
		}
	}
}
#--------------------------------------------------------------------
sub checkTRIGArmTimer{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d*)(.?)(\d*)$/){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}else{
		if($val>=0.001 and $val<=99999.999){
			return($val);
		}else{
			$::Error='Specify the number(sec): 0.001 to 99999.999';
			return(STAT_ERR);
		}
	}
}
#--------------------------------------------------------------------
sub checkTRIGArmCount{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($cal=~/^INF$/ or $val=~/^\+9\.9E37$/){
		$::Error='Ng: Sorry. INF(inite) this program not supported.';
		return(STAT_ERR);
	}
	return($val);
	
	unless($val=~/^(-?)(\d+)$/){
		if($val=~/^INF$/){
			$::Error='Sorry. INF(inite) this program version not support.';
		}else{
			$::Error='Invalid numeric format.';
		}
		return(STAT_ERR);
	}else{
		if($val>=1 and $val<=2500){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 3000';
			return(STAT_ERR);
		}
	}
}
sub syncTRIGArmCount{
	my($rt,$autosetflg)=@_;
	my $cnt=devAct(':ARM:COUN?');
	unless($cnt){
		$::ARM_COUNT=0;
		return(STAT_ERR);
	}else{
		unless(checkTRIGArmCount($cnt)){
			if($autosetflg){
				unless(devSend(':ARM:COUN 1')){
					$::ARM_COUNT=0;
					return(STAT_ERR);
				}else{
					$::ARM_COUNT=1;
					return(STAT_OK);
				}
			}else{
				$::ARM_COUNT=0;
				return(STAT_ERR);
			}
		}else{
			$::ARM_COUNT=$cnt;
			return(STAT_OK);
		}
	}
}
#--------------------------------------------------------------------
sub checkTRIGSource{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($val=~/^TLINK$/){
		$::Error='Ng: Sorry. TLIN(k) this program not supported.';
		return(STAT_ERR);
	}
	return($val);
	
	if($val=~/^IMM$/){
		return($val);
	}elsif($val=~/^TLINK$/){
		$::Error='Ng: Sorry. TLINK this program not supported.';
		return(STAT_ERR);
	}else{
		$::Error='Specify IMM(ediate) Only.';
		return(STAT_ERR);
	}
}
sub syncTRIGSource{
	my($rt,$autosetflg)=@_;
	my $src=devAct(':TRIG:SOUR?');
	unless($src){
		return(STAT_ERR);
	}else{
		unless(checkTRIGSource($src)){
			if($autosetflg){
				return(devSend(':TRIG:SOUR IMM'));
			}else{
				return(STAT_ERR);
			}
		}else{
			$::TRIG_SOURCE=$src;
			return(STAT_OK);
		}
	}
}
#--------------------------------------------------------------------
sub checkTRIGCount{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}

	if($cal=~/^INF$/ or $val=~/^\+9\.9E37$/){
		$::Error='Ng: Sorry. INF(inite) this program not supported.';
		return(STAT_ERR);
	}
	return($val);

	unless($val=~/^(-?)(\d+)$/){
		if($val=~/^INF$/){
			$::Error='Sorry. INF(inite) this program version not support.';
		}else{
			$::Error='Invalid numeric format.';
		}
		return(STAT_ERR);
	}else{
		if($val>=1 and $val<=2500){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 2500';
			return(STAT_ERR);
		}
	}
}
sub syncTRIGCount{
	my($rt,$autosetflg)=@_;
	my $cnt=devAct(':TRIG:COUN?');
	unless($cnt){
		$::TRIG_COUNT=0;
		return(STAT_ERR);
	}else{
		unless(checkTRIGCount($cnt)){
			if($autosetflg){
				unless(devSend(':TRIG:COUN 1')){
					$::TRIG_COUNT=0;
					return(STAT_ERR);
				}else{
					$::TRIG_COUNT=1;
					return(STAT_OK);
				}
			}else{
				$::TRIG_COUNT=0;
				return(STAT_ERR);
			}
		}else{
			$::TRIG_COUNT=$cnt;
			return(STAT_OK);
		}
	}
}
#--------------------------------------------------------------------
sub checkTRIGDELAY{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	unless($val=~/^(-?)(\d*)(.?)(\d*)$/){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}else{
		if($val>=0 and $val<=999.9998){
			return($val);
		}else{
			$::Error='Bad Parameter. Specify the number(sec): 0 to 999.9998';
			return(STAT_ERR);
		}
	}
}

###################################
# READ COMMAND PARAMETERS
###################################
sub setCMDTBL{
	my @arrays;
	while(<DATA>){
		@arrays=split(/#/,$_);
		unless($arrays[0] eq ''){
			$::CMD_KEITHLEY{$arrays[0]}=$arrays[1];
			if($arrays[2] ne ''){
				eval '$::PRE_KEITHLEY{$arrays[0]}='."$arrays[2];";warn $@ if $@;
			}
			if($arrays[3] ne ''){
				eval '$::CHECK_KEITHLEY{$arrays[0]}='."$arrays[3];";warn $@ if $@;
			}
			if($arrays[4] ne ''){
				eval '$::POST_KEITHLEY{$arrays[0]}='."$arrays[4];";warn $@ if $@;
			}
			$::VER_KEITHLEY{$arrays[0]}=$arrays[5];
			if($arrays[6]=~/^[,]*(6482)[,]*$/){
				$::MODEL6482_KEITHLEY{$arrays[0]}=1;
			}
			$::HELP_KEITHLEY{$arrays[0]}=$arrays[7];
		}
	}
	return('Ok:');
}
###################################
# COMMAND PARAMETERS
###################################
__DATA__
#-----------------------------------------------
# CALC[1,2] SECTION
#-----------------------------------------------
SetMathFormat#:CALC\\CH:FORM##\&checkMathFormat##1.0#6482#[CALC1,2]Select math format; MXB (mX+b) or RECiprocal(m/X+b), or LOG10.
GetMathFormat#:CALC\\CH:FORM?####1.0#6482#[CALC1,2]Query math format.
SetKMathMFactor#:CALC\\CH:KMAT:MMF##\&checkKMathMBFactor##1.0#6482#[CALC1,2]Configure math calculations: Set gmh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathMFactor#:CALC\\CH:KMAT:MMF?####1.0#6482#[CALC1,2]Configure math calculations: Query gmh factor.
SetKMathBFactor#:CALC\\CH:KMAT:MBF##\&checkKMathMBFactor##1.0#6482#[CALC1,2]Configure math calculations: Set gbh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathBFactor#:CALC\\CH:KMAT:MBF?####1.0#6482#[CALC1,2]Configure math calculations: Query gbh factor.
SetKMathUnits#:CALC\\CH:KMAT:MUN##\&checkKMathUnits##1.0#6482#[CALC1,2]Configure math calculations: Specify units for mX+b or m/X+b result: 1 character: A?Z, e[e=., e\f=‹, e]f=%.
GetKMathUnits#:CALC\\CH:KMAT:MUN?####1.0#6482#[CALC1,2]Configure math calculations: Query units.
SetMathEnable#:CALC\\CH:STAT##\&checkONOFF##1.0#6482#[CALC1,2]Enable or disable selected math calculation.
GetMathEnable#:CALC\\CH:STAT?####1.0#6482#[CALC1,2]Query state of selected math calculation.
GetValueMath#:CALC\\CH:DATA?##\&checkPreGetValueKMath##1.0#6482#[CALC1,2]Return all math calculation results triggered by INITiate.
#-----------------------------------------------
# CALC[3,4] SECTION
#-----------------------------------------------
SetRELInputPath#:CALC\\CH+2:FEED##\&checkCalc2InputPath##1.0#6482#[CALC3,4]Select input path for limit testing; CALCulate[1/2]or SENSe[1/2].
GetRELInputPath#:CALC\\CH+2:FEED?####1.0#6482#[CALC3,4]Query input path for limit tests.
SetRELOffset#:CALC\\CH+2:NULL:OFFS##\&checkCalc2Range##1.0#6482#[CALC3,4]Configure and control Rel: Specify Rel value; -9.999999e20 to 9.999999e20.
GetRELOffset#:CALC\\CH+2:NULL:OFFS?####1.0#6482#[CALC3,4]Configure and control Rel: Query Rel value.
SetRELEnable#:CALC\\CH+2:NULL:STAT##\&checkONOFF##1.0#6482#[CALC3,4]Configure and control Rel: Enable or disable Rel.
GetRELEnable#:CALC\\CH+2:NULL:STAT?####1.0#6482#[CALC3,4]Configure and control Rel: Query state of Rel.
AcquireRELOffset#:CALC\\CH+2:NULL:ACQ####1.0#6482#[CALC3,4]Configure and control Rel: Use input signal as Rel value.
GetValueREL#:CALC\\CH+2:DATA?##\&checkPreGetValueREL##1.0#6482#[CALC3,4]Return all readings triggered by INITiate.
#-----------------------------------------------
# CALC[5,6] SECTION
#-----------------------------------------------
SetMathRatioFormat#:CALC\\CH+4:FORM##\&checkMathRatioFormat##1.0#6482#[CALC5,6]Select ratio math; C3C4 (CALC3/CALC4);C4C3 (CALC4/CALC3).
GetMathRatioFormat#:CALC\\CH+4:FORM?####1.0#6482#[CALC5,6]Query state of math ratio.
SetMathRatioEnable#:CALC\\CH+4:STAT##\&checkONOFF##1.0#6482#[CALC5,6]Configure and control math ratio: Enable or disable math ratio.
GetMathRatioEnable#:CALC\\CH+4:STAT?####1.0#6482#[CALC5,6]Configure state of math ratio: Query state of math ratio.
GetValueMathRatio#:CALC\\CH+4:DATA?##\&checkPreGetValueREL##1.0#6482#[CALC5,6]Return all readings triggered by INITiate.
#-----------------------------------------------
# CALC7 SECTION: Skip
#-----------------------------------------------
#-----------------------------------------------
# CALC8 SECTION:
#-----------------------------------------------
SetTraceStatisticType#:CALC8:FORM##\&checkTRCSTATICTYPE##1.0#6482#[CALC3]Select buffer statistic; MEAN, SDEViation, Maximum, MINimum or PKPK.
GetTraceStatisticType#:CALC8:FORM?####1.0#6482#[CALC3]Query selected statistic.
GetValueStatistic#:CALC8:DATA?##\&checkDataStatistic##1.0#6482#[CALC3]: Read the selected buffer statistic.
#-----------------------------------------------
# DISPLAY SECTION
#-----------------------------------------------
SetDisplayDigits#:DISP:DIG##\&checkDisplayDigits##1.0#6482#[DISPLAY]Specify display resolution (4 to 7).
GetDisplayDigits#:DISP:DIG?####1.0#6482#[DISPLAY]Query display resolution.
SetDisplayEnable#:DISP:ENAB##\&checkONOFF##1.0#6482#[DISPLAY]Turn fron panel display enable or disable.
GetDisplayEnable#:DISP:ENAB?####1.0#6482#[DISPLAY]Query state of display.
SetDisplayMode#:DISP:MODE##\&checkDisplayMode##1.0#6482#[DISPLAY]Select display function. Name = CALC3, CALC4, CALC5, CALC6, or DUAL.
GetDisplayMode#:DISP:MODE?####1.0#6482#[DISPLAY]Query selected display function.
#-----------------------------------------------
# FORMAT SECTION
#-----------------------------------------------
SetDataFormatElements#:FORM:ELEM##\&checkDATAELEMENTS##1#6482#[FORMAT]Specify data elements; CURRent[1], CURRent2, TIME, and STATus
GetDataFormatElements#:FORM:ELEM?####1#6482#[FORMAT]Query data format elements.
SetDataFormatCalculateElements#:FORM:ELEM:CALC##\&checkCALCDATAELEMENTS##1#6482#[FORMAT]Specify CALCulate elements (CALCulate, TIME, or STATus).*
GetDataFormatCalculateElements#:FORM:ELEM:CALC?####1#6482#[FORMAT]Query CALC data elements.
SetDataFormatTraceDataElements#:FORM:ELEM:TRAC##\&checkTRACEDATAELEMENTS##1#6482#[FORMAT]Specify TRACe data elements: CURRent[1], CURRent2, CALCulate1, CALCulate2, CALCulate3, CALCulate4, CALCulate5, CALCulate6, CALCulate7, TIME, STATus, ALL, DEFault (CURRent[1], CURRent2).
GetDataFormatTraceDataElements#:FORM:ELEM:TRAC?####1#6482#[FORMAT]Query TRACe elements.
#-----------------------------------------------
# SENSE[1,2] SECTION
#-----------------------------------------------
SetRange#:SENSe\\CH:CURR:DC:RANGe##\&checkAmpRANGE##1#6482#[SENSE1,2]Amps function: Configure measurement range: Select range; -21e-3 to 21e-3 (amps).
GetRange#:SENSe\\CH:CURR:DC:RANGe?####1#6482#[SENSE1,2]Amps function: Query range value.
SetAutoRangeEnable#:SENSe\\CH:CURR:DC:RANGe:AUTO##\&checkONOFF##1#6482#[SENSE1,2]Amps function: Enable or disable autorange.
GetAutoRangeEnable#:SENSe\\CH:CURR:DC:RANGe:AUTO?####1#6482#[SENSE1,2]Amps function: Query state of autorange.
SetAutoRangeMax#:SENSe\\CH:CURR:DC:RANGe:AUTO:ULIM##\&checkAmpRANGE##1#6482#[SENSE1,2]Amps function: Select autorange upper limit; -21e-3 to 21e-3 (amps).
GetAutoRangeMax#:SENSe\\CH:CURR:DC:RANGe:AUTO:ULIM?####1#6482#[SENSE1,2]Amps function: Query upper limit for autorange.
SetAutoRangeMin#:SENSe\\CH:CURR:DC:RANGe:AUTO:LLIM##\&checkAmpRANGE##1#6482#[SENSE1,2]Amps function: Select autorange lower limit; -21e-3 to 21e-3 (amps).
GetAutoRangeMin#:SENSe\\CH:CURR:DC:RANGe:AUTO:LLIM?####1#6482#[SENSE1,2]Amps function: Query lower limit for autorange.
# Global commands below.
SetNPLCycles#:SENSe:CURR:DC:NPLC##\&checkAmpNPLC##1#6482#[SENSE1,2]Amps function: Set integration rate in line cycles (PLC); 0.01 to 6.0 (60 Hz) or 5.0 (50Hz).
GetNPLCycles#:SENSe:CURR:DC:NPLC?####1#6482#[SENSE1,2]Amps function: Query NPLC.
SetAverageEnable#:SENSe:AVER##\&checkONOFF##1#6482#[SENSE1,2]Amps function: Query state of digital filter.
GetAverageEnable#:SENSe:AVER?####1#6482#[SENSE1,2]Amps function: Query state of advanced filter.
SetAverageTControl#:SENSe:AVER:TCON##\&checkTCON##1#6482#[SENSE1,2]Amps function: Select Digital filter control; MOVing or REPeat. MOV
GetAverageTControl#:SENSe:AVER:TCON?####1#6482#[SENSE1,2]Amps function: Query filter control.
SetAverageCount#:SENSe:AVER:COUN##\&checkAVGCOUNT##1#6482#[SENSE1,2]Amps function: Specify filter count; 1 to 100.
GetAverageCount#:SENSe:AVER:COUN?####1#6482#[SENSE1,2]Amps function: Query filter count.
SetAverageADVEnable#:SENSe:AVER:ADV##\&checkONOFF##1#6482#[SENSE1,2]Amps function: Enable or disable advanced filter.
GetAverageADVEnable#:SENSe:AVER:ADV?####1#6482#[SENSE1,2]Amps function: Query state of advanced filter.
SetAverageADVNTolarance#:SENSe:AVER:ADV:NTOL##\&checkADVNTOL##1#6482#[SENSE1,2]Amps function: Specify noise tolerance (in %); 0 to 105.
GetAverageADVNTolarance#:SENSe:AVER:ADV:NTOL?####1#6482#[SENSE1,2]Amps function: Query noise tolerance.
SetMedianEnable#:SENSe:MED##\&checkONOFF##1#6482#[SENSE1,2]Amps function:Enable or disable median filter.
GetMedianEnable#:SENSe:MED?####1#6482#[SENSE1,2]Amps function: Query state of median filter.
SetMedianRank#:SENSe:MED:RANK##\&checkMEDRANK##1#6482#[SENSE1,2]Amps function: Specify gnh for rank; 1 to 5 (rank = 2n+1).
GetMedianRank#:SENSe:MED:RANK?####1#6482#[SENSE1,2]Amps function: Query rank.
#-----------------------------------------------
# SYSTEM SECTION
#-----------------------------------------------
SetAutoZeroEnable#:SYST:AZERO##\&checkONOFF##1.0#6482#[SENSE]Amps function: Enable or disable autozero.
GetAutoZeroEnable#:SYST:AZERO?####1.0#6482#[SENSE]Amps function: Query state of autozero.
SetLineFrequency#:SYST:LFR##\&checkLineFrequency#\&syncLineFrequency#1.0#6482#[SENSE]Amps function: Select power line frequency; 50 or 60 (Hz).
GetLineFrequency#:SYST:LFR?####1.0#6482#[SENSE]Amps function: Query frequency setting.
ResetTimeStamp#:SYST:TIME:RES####1.0#6482#[SENSE]Amps function: Reset timestamp to 0 seconds.
#SetZeroCheckEnable#:SYST:ZCH##\&checkONOFF##1.0#6482#[SENSE]Amps function: Enable or disable zero check.
#GetZeroCheckEnable#:SYST:ZCH?####1.0#6482#[SENSE]Amps function: Query state of zero check.
#SetZeroCorrectEnable#:SYST:ZCOR##\&checkONOFF##1.0#6482#[SENSE]Amps function: Enable or disable zero correct.
#GetZeroCorrectEnable#:SYST:ZCOR?####1.0#6482#[SENSE]Amps function: Query state of zero correct.
#AcquireZeroCorrect#:SYST:ZCOR:ACQ####1.0#6482#[SENSE]Amps function: Acquire a new zero correct value.
#-----------------------------------------------
# TRACE SECTION
#-----------------------------------------------
#GetValue#:TRAC:DATA?#\&checkPreGetValue###1.0#6482#
GetValue#####1.0#6482#
GetTraceData#####1.0#6482#
SetTraceTimeFormat#:TRAC:TST:FORM##\&checkTRCTIMEFORMAT##1#6482#[TRACE]Select timestamp format; ABSolute or DELta.
GetTraceTimeFormat#:TRAC:TST:FORM?####1#6482#[TRACE]Query timestamp format.
SetTracePoints#:TRAC:POIN##\&checkTRCPOINTS##1#6482#[TRACE]Specify size of buffer (1 to 3000).
GetTracePoints#:TRAC:POIN?####1#6482#[TRACE]Query buffer size.
SetTraceFeedControl#:TRAC:FEED:CONT##\&checkTRCFEEDCONTROL##1#6482#[TRACE]Specify buffer control mode (NEVER or NEXT).
GetTraceFeedControl#:TRAC:FEED:CONT?####1#6482#[TRACE]Query buffer control mode.
GetTraceActualPoints#:TRAC:POIN:ACT?####1#6482#[TRACE]Queries number of readings stored in the buffer.
#-----------------------------------------------
# ARM SECTION
#-----------------------------------------------
SetTriggerArmSource#:ARM:SOUR##\&checkTRIGArmSource#\&syncTRIGArmSource#10#6482#[TRIGGER]Select control source; IMMediate, TIMer, BUS,TLINk, or MANual.
GetTriggerArmSource#:ARM:SOUR?###\&syncTRIGArmSource#1.0#6482#[TRIGGER]Query arm control source.
SetTriggerArmTimer#:ARM:TIM##\&checkTRIGArmTimer##1.0#6482#[TRIGGER]Set timer interval; 0.001 to 99999.999 (sec).
GetTriggerArmTimer#:ARM:TIM?####1.0#6482#[TRIGGER]Query timer interval.
SetTriggerArmCount#:ARM:COUN#\&dev2Idle#\&checkTRIGArmCount#\&syncTRIGArmCount#1.0#6482#[TRIGGER]Set measure count of arm control; 1 to 2500.
GetTriggerArmCount#:ARM:COUN?####1.0#6482#[TRIGGER]Query measure count of arm control.
GetTriggerArmDirection#:ARM:DIR?####1.0#6482#[TRIGGER]Query state of bypass.
#-----------------------------------------------
# TRIGGER SECTION
#-----------------------------------------------
SetTriggerSource#:TRIG:SOUR##\&checkTRIGSource##1.0#6482#[TRIGGER]Select control source; IMMediate or TLINk.
GetTriggerSource#:TRIG:SOUR?####1.0#6482#[TRIGGER]Query trigger control source.
SetTriggerDelay#:TRIG:DEL##\&checkTRIGDELAY##1.0#6482#[TRIGGER]Set trigger delay; 0 to 999.9999 (sec).
GetTriggerDelay#:TRIG:DEL?####1.0#6482#[TRIGGER]Query trigger delay value.
SetTriggerCount#:TRIG:COUN#\&dev2Idle#\&checkTRIGCount#\&syncTRIGCount#1.0#6482#[TRIGGER]Set measure count of trigger control; 1 to 2500.
GetTriggerCount#:TRIG:COUN?####1.0#6482#[TRIGGER]Query measure count of trigger control.
#SetTriggerAutoDelayEnable#:TRIG:DEL:AUTO##\&checkONOFF##1.0#6482#[TRIGGER]Enable or disable auto delay.
#GetTriggerAutoDelayEnable#:TRIG:DEL:AUTO?####1.0#6482#[TRIGGER]Query state of auto delay.
#-----------------------------------------------
# COMMON SECTION
#-----------------------------------------------
hello#####1.0#6482#return reply message.'@hello nice to meet you.'
help#####1.0#6482#no parameter -> return command list. <Using paramater> -> show command <paramater> help. 
Reset#####1.0#6482#Reset Command. Return the Model 6482 to the *RST default conditions.
Preset#####1.0#6482#Preset Command. Return the Model 6482 to the :SYST:PRES defaults, optimized for front panel operation. 
LoadUserSetup#####1.0#6482#Recall Command. Return the Model 6482 to the setup configuration stored in the specified memory location.
SaveToUserSetup#####1.0#6482#Save Command. Saves the current setup to the specified memory location.
Run#####1.0#6482#Initiate one trigger cycle. Run measurement. 
TriggerRun#####1.0#6482#Initiate one trigger cycle. Run measurement. 
GoIdle#####1.0#6482#Reset Trigger system(goes to idle state).
GetDeviceList#####1.0#6482#Get channel name.
Local#:SYST:Local####1.0#6482#[SENSE]Amps function: Goto Local
