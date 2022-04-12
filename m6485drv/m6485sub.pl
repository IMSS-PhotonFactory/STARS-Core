###################################
# Globals
###################################
%::MODEL6485_KEITHLEY=();
%::CMD_KEITHLEY=();
%::PRE_KEITHLEY=();
%::CHECK_KEITHLEY=();
%::VER_KEITHLEY=();
%::HELP_KEITHLEY=();
setCMDTBL();

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
	return(checkRangeMinMax2($val));
}
#--------------------------------------------------------------------
sub checkKMathUnits{
	my $val=uc(shift);
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
	my $rt=devAct(':CALC:STAT?');if($rt eq STAT_ERR){return($rt);}
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
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(CALC|SENS)$/){
		return($val);
	}else{
		$::Error='Specify CALC(ulate[1]) or SENS(e[1]).';
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
	my $rt=devAct(':CALC2:NULL:STAT?');if($rt eq STAT_ERR){return($rt);}
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
sub syncLineFrequency{
	my $val=shift;
	my $lfr=devAct(':SYST:LFR?');
	unless($lfr){
		return(STAT_ERR);
	}else{
		$::LINE_FREQUENCY=$lfr;
		return(STAT_OK);
}	}

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
		$::Error='Specify the number: 2.1E-9(amps) to 2.1E-2(amps).';
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
		if($val>=2 and $val<=100){
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
	return($val);

	if($val=~/^(ABS|DELT)$/){
		return($val);
	}else{
		$::Error='Specify ABS(olute) or DEL(ta).';
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
			$::Error='Specify the number: 1 to 2500';
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
			if($arrays[6]=~/^[,]*(6485)[,]*$/){
				$::MODEL6485_KEITHLEY{$arrays[0]}=1;
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
#
SetMathFormat#:CALC1:FORM##\&checkMathFormat##1.0#6485#[CALC1]Select math format; MXB (mX+b) or RECiprocal(m/X+b), or LOG10.
GetMathFormat#:CALC1:FORM?####1.0#6485#[CALC1]Query math format.
SetKMathMFactor#:CALC1:KMAT:MMF##\&checkKMathMBFactor##1.0#6485#[CALC1]Configure math calculations: Set gmh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathMFactor#:CALC1:KMAT:MMF?####1.0#6485#[CALC1]Configure math calculations: Query gmh factor.
SetKMathBFactor#:CALC1:KMAT:MBF##\&checkKMathMBFactor##1.0#6485#[CALC1]Configure math calculations: Set gbh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathBFactor#:CALC1:KMAT:MBF?####1.0#6485#[CALC1]Configure math calculations: Query gbh factor.
SetKMathUnits#:CALC1:KMAT:MUN##\&checkKMathUnits##1.0#6485#[CALC1]Configure math calculations: Specify units for mX+b or m/X+b result: 1 character: A?Z, e[e=., e\f=‹, e]f=%.
GetKMathUnits#:CALC1:KMAT:MUN?####1.0#6485#[CALC1]Configure math calculations: Query units.
SetMathEnable#:CALC1:STAT##\&checkONOFF##1.0#6485#[CALC1]Enable or disable selected math calculation.
GetMathEnable#:CALC1:STAT?####1.0#6485#[CALC1]Query state of selected math calculation.
GetValueMath#:CALC1:DATA?##\&checkPreGetValueKMath##1.0#6485#[CALC1]Return all math calculation results triggered by INITiate.
#
SetLimitTestInputPath#:CALC2:FEED##\&checkCalc2InputPath##1.0#6485#[CALC2]Select input path for limit testing; CALCulate[1]or SENSe[1].
GetLimitTestInputPath#:CALC2:FEED?####1.0#6485#[CALC2]Query input path for limit tests.
SetRELInputPath#:CALC2:FEED##\&checkCalc2InputPath##1.0#6485#[CALC2]Select input path for limit testing; CALCulate[1]or SENSe[1].
GetRELInputPath#:CALC2:FEED?####1.0#6485#[CALC2]Query input path for limit tests.
SetLimitTest1Max#:CALC2:LIM:UPP##\&checkCalc2Range##1.0#6485#[CALC2]Limit 1 Testing: Configure upper limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest1Max#:CALC2:LIM:UPP?####1.0#6485#[CALC2]Limit 1 Testing: Query upper limit.
SetLimitTest1Min#:CALC2:LIM:LOW##\&checkCalc2Range##1.0#6485#[CALC2]Limit 1 Testing: Configure lower limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest1Min#:CALC2:LIM:LOW?####1.0#6485#[CALC2]Limit 1 Testing: Query lower limit.
SetLimitTest1Enable#:CALC2:LIM:STAT##\&checkONOFF##1.0#6485#[CALC2]Limit 1 Testing: Enable or disable limit 1 test.
GetLimitTest1Enable#:CALC2:LIM:STAT?####1.0#6485#[CALC2]Limit 1 Testing: Query state of limit 1 test.
IsLimitTest1FailStatus#:CALC2:LIM:FAIL?####1.0#6485#[CALC2]Limit 1 Testing: Return result of limit 1 test; 0 (pass) or 1 (fail)
SetLimitTest2Max#:CALC2:LIM2:UPP##\&checkCalc2Range##1.0#6485#[CALC2]Limit 2 Testing: Configure upper limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest2Max#:CALC2:LIM2:UPP?####1.0#6485#[CALC2]Limit 2 Testing: Query upper limit.
SetLimitTest2Min#:CALC2:LIM2:LOW##\&checkCalc2Range##1.0#6485#[CALC2]Limit 2 Testing: Configure lower limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest2Min#:CALC2:LIM2:LOW?####1.0#6485#[CALC2]Limit 2 Testing: Query lower limit.
SetLimitTest2Enable#:CALC2:LIM2:STAT##\&checkONOFF##1.0#6485#[CALC2]Limit 2 Testing: Enable or disable limit 1 test.
GetLimitTest2Enable#:CALC2:LIM2:STAT?####1.0#6485#[CALC2]Limit 2 Testing: Query state of limit 1 test.
IsLimitTest2FailStatus#:CALC2:LIM2:FAIL?####1.0#6485#[CALC2]Limit 2 Testing: Return result of limit 1 test; 0 (pass) or 1 (fail)
AcquireRELOffset#:CALC2:NULL:ACQ####1.0#6485#[CALC2]Configure and control Rel: Use input signal as Rel value.
SetRELOffset#:CALC2:NULL:OFFS##\&checkCalc2Range##1.0#6485#[CALC2]Configure and control Rel: Specify Rel value; -9.999999e20 to 9.999999e20.
GetRELOffset#:CALC2:NULL:OFFS?####1.0#6485#[CALC2]Configure and control Rel: Query Rel value.
SetRELEnable#:CALC2:NULL:STAT##\&checkONOFF##1.0#6485#[CALC2]Configure and control Rel: Enable or disable Rel.
GetRELEnable#:CALC2:NULL:STAT?####1.0#6485#[CALC2]Configure and control Rel: Query state of Rel.
GetValueREL#:CALC2:DATA?##\&checkPreGetValueREL##1.0#6485#[CALC2]Return all [CALC2]readings triggered by INITiate.
#
SetTraceStatisticType#:CALC3:FORM##\&checkTRCSTATICTYPE##1.0#6485#[CALC3]Select buffer statistic; MEAN, SDEViation, Maximum, MINimum or PKPK.
GetTraceStatisticType#:CALC3:FORM?####1.0#6485#[CALC3]Query selected statistic.
GetValueStatistic#:CALC3:DATA?##\&checkDataStatistic##1.0#6485#[CALC3]: Read the selected buffer statistic.
#
SetDisplayDigits#:DISP:DIG##\&checkDisplayDigits##1.0#6485#[DISPLAY]Set display resolution; 4 to 7.
GetDisplayDigits#:DISP:DIG?####1.0#6485#[DISPLAY]Query display resolution.
SetDisplayEnable#:DISP:ENAB##\&checkONOFF##1.0#6485#[DISPLAY]Turn fron panel display enable or disable.
GetDisplayEnable#:DISP:ENAB?####1.0#6485#[DISPLAY]Query state of display.
#
SetDataFormatElements#:FORM:ELEM##\&checkDATAELEMENTS##1.0#6485#[FORMAT]Specify data elements; READing, UNITs, TIME, and STATus.
GetDataFormatElements#:FORM:ELEM?####1.0#6485#[FORMAT]Query data format elements.
#
SetNPLCycles#:SENS:CURR:DC:NPLC##\&checkAmpNPLC##1.0#6485#[SENSE]Amps function: Set integration rate in line cycles (PLC); 0.01 to 6.0 (60 Hz) or 5.0 (50Hz).
GetNPLCycles#:SENS:CURR:DC:NPLC?####1.0#6485#[SENSE]Amps function: Query NPLC.
SetRange#:SENS:CURR:DC:RANGe##\&checkAmpRANGE##1.0#6485#[SENSE]Amps function: Configure measurement range: Select range; 2.1E-9 to 2.1E-2 (amps).
GetRange#:SENS:CURR:DC:RANGe?####1.0#6485#[SENSE]Amps function: Query range value.
SetAutoRangeEnable#:SENS:CURR:DC:RANGe:AUTO##\&checkONOFF##1.0#6485#[SENSE]Amps function: Enable or disable autorange.
GetAutoRangeEnable#:SENS:CURR:DC:RANGe:AUTO?####1.0#6485#[SENSE]Amps function: Query state of autorange.
SetAutoRangeMax#:SENS:CURR:DC:RANGe:AUTO:ULIM##\&checkAmpRANGE##1.0#6485#[SENSE]Amps function: Select autorange upper limit; 2.1E-9 to 2.1E-2 (amps).
GetAutoRangeMax#:SENS:CURR:DC:RANGe:AUTO:ULIM?####1.0#6485#[SENSE]Amps function: Query upper limit for autorange.
SetAutoRangeMin#:SENS:CURR:DC:RANGe:AUTO:LLIM##\&checkAmpRANGE##1.0#6485#[SENSE]Amps function: Select autorange lower limit; 2.1E-9 to 2.1E-2 (amps).
GetAutoRangeMin#:SENS:CURR:DC:RANGe:AUTO:LLIM?####1.0#6485#[SENSE]Amps function: Query lower limit for autorange.
SetAverageEnable#:SENS:AVER##\&checkONOFF##1.0#6485#[SENSE]Amps function: Query state of digital filter.
GetAverageEnable#:SENS:AVER?####1.0#6485#[SENSE]Amps function: Query state of advanced filter.
SetAverageTControl#:SENS:AVER:TCON##\&checkTCON##1.0#6485#[SENSE]Amps function: Select Digital filter control; MOVing or REPeat. MOV
GetAverageTControl#:SENS:AVER:TCON?####1.0#6485#[SENSE]Amps function: Query filter control.
SetAverageCount#:SENS:AVER:COUN##\&checkAVGCOUNT##1.0#6485#[SENSE]Amps function: Specify filter count; 2 to 100.
GetAverageCount#:SENS:AVER:COUN?####1.0#6485#[SENSE]Amps function: Query filter count.
SetAverageADVEnable#:SENS:AVER:ADV##\&checkONOFF##1.0#6485#[SENSE]Amps function: Enable or disable advanced filter.
GetAverageADVEnable#:SENS:AVER:ADV?####1.0#6485#[SENSE]Amps function: Query state of advanced filter.
SetAverageADVNTolarance#:SENS:AVER:ADV:NTOL##\&checkADVNTOL##1.0#6485#[SENSE]Amps function: Specify noise tolerance (in %); 0 to 105.
GetAverageADVNTolarance#:SENS:AVER:ADV:NTOL?####1.0#6485#[SENSE]Amps function: Query noise tolerance.
SetMedianEnable#:SENS:MED##\&checkONOFF##1.0#6485#[SENSE]Amps function:Enable or disable median filter.
GetMedianEnable#:SENS:MED?####1.0#6485#[SENSE]Amps function: Query state of median filter.
SetMedianRank#:SENS:MED:RANK##\&checkMEDRANK##1.0#6485#[SENSE]Amps function: Specify gnh for rank; 1 to 5 (rank = 2n+1).
GetMedianRank#:SENS:MED:RANK?####1.0#6485#[SENSE]Amps function: Query rank.
#
SetZeroCheckEnable#:SYST:ZCH##\&checkONOFF##1.0#6485#[SENSE]Amps function: Enable or disable zero check.
GetZeroCheckEnable#:SYST:ZCH?####1.0#6485#[SENSE]Amps function: Query state of zero check.
SetZeroCorrectEnable#:SYST:ZCOR##\&checkONOFF##1.0#6485#[SENSE]Amps function: Enable or disable zero correct.
GetZeroCorrectEnable#:SYST:ZCOR?####1.0#6485#[SENSE]Amps function: Query state of zero correct.
AcquireZeroCorrect#:SYST:ZCOR:ACQ####1.0#6485#[SENSE]Amps function: Acquire a new zero correct value.
SetLineFrequency#:SYST:LFR##\&checkLineFrequency#\&syncLineFrequency#1.0#6485#[SENSE]Amps function: Select power line frequency; 50 or 60 (Hz).
GetLineFrequency#:SYST:LFR?####1.0#6485#[SENSE]Amps function: Query frequency setting.
SetLineFrequencyAutoEnable#:SYST:LFR:AUTO##\&checkONOFF#\&syncLineFrequency#1.0#6485#[SENSE]Amps function: Enable or disable auto frequency.
GetLineFrequencyAutoEnable#:SYST:LFR:AUTO?###\&syncLineFrequency#1.0#6485#[SENSE]Amps function: Query state of auto frequency.
SetAutoZeroEnable#:SYST:AZERO##\&checkONOFF##1.0#6485#[SENSE]Amps function: Enable or disable autozero.
GetAutoZeroEnable#:SYST:AZERO?####1.0#6485#[SENSE]Amps function: Query state of autozero.
ResetTimeStamp#:SYST:TIME:RES####1.0#6485#[SENSE]Amps function: Reset timestamp to 0 seconds.
#
SetTraceFeed#:TRAC:FEED##\&checkTRCFEED##1.0#6485#[TRACE]Select source of readings for buffer.; CALCulate[1]orCALCulate[2]orSENSe[1].
GetTraceFeed#:TRAC:FEED?####1.0#6485#[TRACE]Query source of readings for buffer.
SetTraceTimeFormat#:TRAC:TST:FORM##\&checkTRCTIMEFORMAT##1.0#6485#[TRACE]Select timestamp format; ABSolute or DELta. ABS
GetTraceTimeFormat#:TRAC:TST:FORM?####1.0#6485#[TRACE]Query timestamp format.
GetValue#:TRAC:DATA?#\&checkPreGetValue###1.0#6485#
#
SetTriggerArmSource#:ARM:SOUR##\&checkTRIGArmSource#\&syncTRIGArmSource#10#6485#[TRIGGER]Select control source; IMMediate, TIMer, BUS,TLINk, or MANual.
GetTriggerArmSource#:ARM:SOUR?###\&syncTRIGArmSource#1.0#6485#[TRIGGER]Query arm control source.
SetTriggerArmTimer#:ARM:TIM##\&checkTRIGArmTimer##1.0#6485#[TRIGGER]Set timer interval; 0.001 to 99999.999 (sec).
GetTriggerArmTimer#:ARM:TIM?####1.0#6485#[TRIGGER]Query timer interval.
SetTriggerSource#:TRIG:SOUR##\&checkTRIGSource##1.0#6485#[TRIGGER]Select control source; IMMediate or TLINk.
GetTriggerSource#:TRIG:SOUR?####1.0#6485#[TRIGGER]Query trigger control source.
SetTriggerDelay#:TRIG:DEL##\&checkTRIGDELAY##1.0#6485#[TRIGGER]Set trigger delay; 0 to 999.9999 (sec).
GetTriggerDelay#:TRIG:DEL?####1.0#6485#[TRIGGER]Query trigger delay value.
SetTriggerAutoDelayEnable#:TRIG:DEL:AUTO##\&checkONOFF##1.0#6485#[TRIGGER]Enable or disable auto delay.
GetTriggerAutoDelayEnable#:TRIG:DEL:AUTO?####1.0#6485#[TRIGGER]Query state of auto delay.
SetTriggerArmCount#:ARM:COUN#\&dev2Idle#\&checkTRIGArmCount#\&syncTRIGArmCount#1.0#6485#[TRIGGER]Set measure count of arm control; 1 to 2500.
GetTriggerArmCount#:ARM:COUN?####1.0#6485#[TRIGGER]Query measure count of arm control.
SetTriggerCount#:TRIG:COUN#\&dev2Idle#\&checkTRIGCount#\&syncTRIGCount#1.0#6485#[TRIGGER]Set measure count of trigger control; 1 to 2500.
GetTriggerCount#:TRIG:COUN?####1.0#6485#[TRIGGER]Query measure count of trigger control.
hello#####1.0#6485#return reply message.'@hello nice to meet you.'
help#####1.0#6485#no parameter -> return command list. <paramater> -> show command <paramater> help. 
#help Only Code Embedded
hello#####1.0#6485#return reply message.'@hello nice to meet you.'
help#####1.0#6485#no parameter -> return command list. <Using paramater> -> show command <paramater> help. 
Reset#####1.0#6485#Reset Command. Return the Model 6485 to the *RST default conditions.
Preset#####1.0#6485#Preset Command. Return the Model 6485 to the :SYST:PRES defaults, optimized for front panel operation. 
LoadUserSetup#####1.0#6485#Recall Command. Return the Model 6485 to the setup configuration stored in the specified memory location.
SaveToUserSetup#####1.0#6485#Save Command. Saves the current setup to the specified memory location.
Run#####1.0#6485#Initiate one trigger cycle. Run measurement. 
GoIdle#####1.0#6485#Reset Trigger system(goes to idle state).
