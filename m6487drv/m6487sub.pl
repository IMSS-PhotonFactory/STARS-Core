###################################
# Globals
###################################
%::MODEL6487_KEITHLEY=();
%::CMD_KEITHLEY=();
%::PRE_KEITHLEY=();
%::CHECK_KEITHLEY=();
%::VER_KEITHLEY=();
%::HELP_KEITHLEY=();
setCMDTBL();

###################################
# Check Functions Added for m6487
###################################
sub convNDN{
	my $val=uc(shift);
	my($v,$sign,$sign2)=('',1,1);
	if($val=~/^#H([0-9|A-E]+)$/){
		$v = hex($1);
	}elsif($val=~/^#Q([0-7]+)$/){
		$v = oct($1);
	}elsif($val=~/^#B([0|1]+)$/){
		$v = unpack("C",  pack("B".length($1),$1));
	}elsif($val=~/^(\d+)$/){
		$v = $1;
	}
	return($v);
}
#--------------------------------------------------------------------
sub checkSource2{
	my $val=shift;
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convNDN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif($v>=0 and $v<=15){
		return($v);
	}else{
		$::Error='Specify the number: 0 to 15.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkDataFormatSource2{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(ASC|HEX|OCT|BIN)$/){
		return($val);
	}else{
		$::Error='Specify ASC(ii) or HEX(adecimal) or OCT(al) or BIN(ary).';
		return(STAT_ERR);
	}
}
sub checkVoltage{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(abs($v)<=505){
		return($v);
	}else{
		$::Error='Specify the number: -505 to 505 (V).';
		return(STAT_ERR);
	}
}
sub checkVoltSourceAmplitude{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(abs($v)<=500){
		return($v);
	}else{
		$::Error='Specify the number: -500 to 500.';
		return(STAT_ERR);
	}
}

sub checkOHMSAVTimeInterval{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);
}
sub checkOHMSAVCycles{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(0<=$v and $v<=9999){
		return($v);
	}else{
		$::Error='Specify the number: 0 to 9999.';
		return(STAT_ERR);
	}
}
sub checkOHMSUnits{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(AMPS|OHMS)$/){
		return($val);
	}else{
		$::Error='Specify AMPS or OHMS.';
		return(STAT_ERR);
	}
}
sub checkVoltSourceRange{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);
}
sub checkVoltSourceILimit{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);
	my $v=convEtoN($val);
	if($v eq ''){
		return(STAT_ERR);
	}elsif($v<=2.5*(10**(-5)) and $v>=2.5*(10**(-2))){
		return($v);
	}else{
		$::Error='Specify the number: 2.5E-5(amps) to 2.5E-2(amps).';
		return(STAT_ERR);
	}
}
sub checkVoltageSweepDelay{
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
sub checkTTLOutputPatern{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(0<=$v and $v<=15){
		return($v);
	}else{
		$::Error='Specify the number: 0 to 15.';
		return(STAT_ERR);
	}
}
sub checkTTLDelayPatern{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	my $v=convEtoN($val);
	if($v eq ''){
		$::Error='Invalid number format.';
		return(STAT_ERR);
	}elsif(0<=$v and $v<=60){
		return($v);
	}else{
		$::Error='Specify the number: 0 to 60.';
		return(STAT_ERR);
	}
}
sub checkTTL4Mode{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);

	if($val=~/^(EOT|BUSY)$/){
		return($val);
	}else{
		$::Error='Specify EOTest or BUSY.';
		return(STAT_ERR);
	}
}
sub checkTTL4ActiveBusyStatus{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);
	if($val=~/^[0|1]$/){
		return($val);
	}else{
		$::Error='Specify the number: 0 or 1.';
		return(STAT_ERR);
	}
}
#--------------------------------------------------------------------
sub checkTRIGArmCount2{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
#Comment for SetTriggerCount INF
	if($val=~/^INF$/ or $val=~/^\+9\.9E37$/){
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
		if($val>=1 and $val<=2048){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 2048';
			return(STAT_ERR);
		}
	}
}
#--------------------------------------------------------------------
sub checkTracePoints{
	my $val=uc(shift);
	if(checkArgMissing($val) eq STAT_ERR){return(STAT_ERR);}
	return($val);
	
	unless($val=~/^(-?)(\d+)$/){
		$::Error='Invalid numeric format.';
		return(STAT_ERR);
	}else{
		if($val>=1 and $val<=3000){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 3000';
			return(STAT_ERR);
		}
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
		unless(/^(READ|UNIT|TIME|STAT|DEF|ALL|VSO)$/){
			$::Error="Specify among READ(ing),UNIT(s),VSO(urce),TIME and STAT(us),DEF(ault),and ALL.";
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

	if($val=~/^INF$/ or $val=~/^\+9\.9E37$/){
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
		if($val>=1 and $val<=2048){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 2048';
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
		if($val>=1 and $val<=2048){
			return($val);
		}else{
			$::Error='Specify the number: 1 to 2048';
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
			if($arrays[6]=~/^[,]*(6487)[,]*$/){
				$::MODEL6487_KEITHLEY{$arrays[0]}=1;
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
SetMathFormat#:CALC1:FORM##\&checkMathFormat##1.0#6487#[CALC1]Select math format; MXB (mX+b) or RECiprocal(m/X+b), or LOG10.
GetMathFormat#:CALC1:FORM?####1.0#6487#[CALC1]Query math format.
SetKMathMFactor#:CALC1:KMAT:MMF##\&checkKMathMBFactor##1.0#6487#[CALC1]Configure math calculations: Set gmh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathMFactor#:CALC1:KMAT:MMF?####1.0#6487#[CALC1]Configure math calculations: Query gmh factor.
SetKMathBFactor#:CALC1:KMAT:MBF##\&checkKMathMBFactor##1.0#6487#[CALC1]Configure math calculations: Set gbh for mX+b and m/X+b calculation; -9.99999e20 to 9.99999e20.
GetKMathBFactor#:CALC1:KMAT:MBF?####1.0#6487#[CALC1]Configure math calculations: Query gbh factor.
SetKMathUnits#:CALC1:KMAT:MUN##\&checkKMathUnits##1.0#6487#[CALC1]Configure math calculations: Specify units for mX+b or m/X+b result: 1 character: A?Z, e[e=., e\f=‹, e]f=%.
GetKMathUnits#:CALC1:KMAT:MUN?####1.0#6487#[CALC1]Configure math calculations: Query units.
SetMathEnable#:CALC1:STAT##\&checkONOFF##1.0#6487#[CALC1]Enable or disable selected math calculation.
GetMathEnable#:CALC1:STAT?####1.0#6487#[CALC1]Query state of selected math calculation.
GetValueMath#:CALC1:DATA?##\&checkPreGetValueKMath##1.0#6487#[CALC1]Return all math calculation results triggered by INITiate.
#
SetLimitTestInputPath#:CALC2:FEED##\&checkCalc2InputPath##1.0#6487#[CALC2]Select input path for limit testing; CALCulate[1]or SENSe[1].
GetLimitTestInputPath#:CALC2:FEED?####1.0#6487#[CALC2]Query input path for limit tests.
SetRELInputPath#:CALC2:FEED##\&checkCalc2InputPath##1.0#6487#[CALC2]Select input path for limit testing; CALCulate[1]or SENSe[1].
GetRELInputPath#:CALC2:FEED?####1.0#6487#[CALC2]Query input path for limit tests.
SetLimitTest1Max#:CALC2:LIM:UPP##\&checkCalc2Range##1.0#6487#[CALC2]Limit 1 Testing: Configure upper limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest1Max#:CALC2:LIM:UPP?####1.0#6487#[CALC2]Limit 1 Testing: Query upper limit.
SetLimitTest1Min#:CALC2:LIM:LOW##\&checkCalc2Range##1.0#6487#[CALC2]Limit 1 Testing: Configure lower limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest1Min#:CALC2:LIM:LOW?####1.0#6487#[CALC2]Limit 1 Testing: Query lower limit.
SetLimitTest1Enable#:CALC2:LIM:STAT##\&checkONOFF##1.0#6487#[CALC2]Limit 1 Testing: Enable or disable limit 1 test.
GetLimitTest1Enable#:CALC2:LIM:STAT?####1.0#6487#[CALC2]Limit 1 Testing: Query state of limit 1 test.
IsLimitTest1FailStatus#:CALC2:LIM:FAIL?####1.0#6487#[CALC2]Limit 1 Testing: Return result of limit 1 test; 0 (pass) or 1 (fail)
SetLimitTest2Max#:CALC2:LIM2:UPP##\&checkCalc2Range##1.0#6487#[CALC2]Limit 2 Testing: Configure upper limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest2Max#:CALC2:LIM2:UPP?####1.0#6487#[CALC2]Limit 2 Testing: Query upper limit.
SetLimitTest2Min#:CALC2:LIM2:LOW##\&checkCalc2Range##1.0#6487#[CALC2]Limit 2 Testing: Configure lower limit: Set limit; -9.99999e20 to 9.99999e20.
GetLimitTest2Min#:CALC2:LIM2:LOW?####1.0#6487#[CALC2]Limit 2 Testing: Query lower limit.
SetLimitTest2Enable#:CALC2:LIM2:STAT##\&checkONOFF##1.0#6487#[CALC2]Limit 2 Testing: Enable or disable limit 1 test.
GetLimitTest2Enable#:CALC2:LIM2:STAT?####1.0#6487#[CALC2]Limit 2 Testing: Query state of limit 1 test.
IsLimitTest2FailStatus#:CALC2:LIM2:FAIL?####1.0#6487#[CALC2]Limit 2 Testing: Return result of limit 1 test; 0 (pass) or 1 (fail)
AcquireRELOffset#:CALC2:NULL:ACQ####1.0#6487#[CALC2]Configure and control Rel: Use input signal as Rel value.
SetRELOffset#:CALC2:NULL:OFFS##\&checkCalc2Range##1.0#6487#[CALC2]Configure and control Rel: Specify Rel value; -9.999999e20 to 9.999999e20.
GetRELOffset#:CALC2:NULL:OFFS?####1.0#6487#[CALC2]Configure and control Rel: Query Rel value.
SetRELEnable#:CALC2:NULL:STAT##\&checkONOFF##1.0#6487#[CALC2]Configure and control Rel: Enable or disable Rel.
GetRELEnable#:CALC2:NULL:STAT?####1.0#6487#[CALC2]Configure and control Rel: Query state of Rel.
GetValueREL#:CALC2:DATA?##\&checkPreGetValueREL##1.0#6487#[CALC2]Return all [CALC2]readings triggered by INITiate.
#
SetTraceStatisticType#:CALC3:FORM##\&checkTRCSTATICTYPE##1.0#6487#[CALC3]Select buffer statistic; MEAN, SDEViation, Maximum, MINimum or PKPK.
GetTraceStatisticType#:CALC3:FORM?####1.0#6487#[CALC3]Query selected statistic.
GetValueStatistic#:CALC3:DATA?##\&checkDataStatistic##1.0#6487#[CALC3]: Read the selected buffer statistic.
#
SetDisplayDigits#:DISP:DIG##\&checkDisplayDigits##1.0#6487#[DISPLAY]Set display resolution; 4 to 7.
GetDisplayDigits#:DISP:DIG?####1.0#6487#[DISPLAY]Query display resolution.
SetDisplayEnable#:DISP:ENAB##\&checkONOFF##1.0#6487#[DISPLAY]Turn fron panel display enable or disable.
GetDisplayEnable#:DISP:ENAB?####1.0#6487#[DISPLAY]Query state of display.
#
#SetDataFormatElements#:FORM:ELEM##\&checkDATAELEMENTS##1.0#6487#[FORMAT]Specify data elements; READing, UNITs, TIME, and STATus.
SetDataFormatElements#:FORM:ELEM##\&checkDATAELEMENTS##1.0#6487#[FORMAT]Specify data elements; READing, UNITs, VSOurce, TIME, STATus, DEFault and ALL.
GetDataFormatElements#:FORM:ELEM?####1.0#6487#[FORMAT]Query data format elements.
#
SetNPLCycles#:SENS:CURR:DC:NPLC##\&checkAmpNPLC##1.0#6487#[SENSE]Amps function: Set integration rate in line cycles (PLC); 0.01 to 6.0 (60 Hz) or 5.0 (50Hz).
GetNPLCycles#:SENS:CURR:DC:NPLC?####1.0#6487#[SENSE]Amps function: Query NPLC.
SetRange#:SENS:CURR:DC:RANGe##\&checkAmpRANGE##1.0#6487#[SENSE]Amps function: Configure measurement range: Select range; 2.1E-9 to 2.1E-2 (amps).
GetRange#:SENS:CURR:DC:RANGe?####1.0#6487#[SENSE]Amps function: Query range value.
SetAutoRangeEnable#:SENS:CURR:DC:RANGe:AUTO##\&checkONOFF##1.0#6487#[SENSE]Amps function: Enable or disable autorange.
GetAutoRangeEnable#:SENS:CURR:DC:RANGe:AUTO?####1.0#6487#[SENSE]Amps function: Query state of autorange.
SetAutoRangeMax#:SENS:CURR:DC:RANGe:AUTO:ULIM##\&checkAmpRANGE##1.0#6487#[SENSE]Amps function: Select autorange upper limit; 2.1E-9 to 2.1E-2 (amps).
GetAutoRangeMax#:SENS:CURR:DC:RANGe:AUTO:ULIM?####1.0#6487#[SENSE]Amps function: Query upper limit for autorange.
SetAutoRangeMin#:SENS:CURR:DC:RANGe:AUTO:LLIM##\&checkAmpRANGE##1.0#6487#[SENSE]Amps function: Select autorange lower limit; 2.1E-9 to 2.1E-2 (amps).
GetAutoRangeMin#:SENS:CURR:DC:RANGe:AUTO:LLIM?####1.0#6487#[SENSE]Amps function: Query lower limit for autorange.
SetAverageEnable#:SENS:AVER##\&checkONOFF##1.0#6487#[SENSE]Amps function: Query state of digital filter.
GetAverageEnable#:SENS:AVER?####1.0#6487#[SENSE]Amps function: Query state of advanced filter.
SetAverageTControl#:SENS:AVER:TCON##\&checkTCON##1.0#6487#[SENSE]Amps function: Select Digital filter control; MOVing or REPeat. MOV
GetAverageTControl#:SENS:AVER:TCON?####1.0#6487#[SENSE]Amps function: Query filter control.
SetAverageCount#:SENS:AVER:COUN##\&checkAVGCOUNT##1.0#6487#[SENSE]Amps function: Specify filter count; 2 to 100.
GetAverageCount#:SENS:AVER:COUN?####1.0#6487#[SENSE]Amps function: Query filter count.
SetAverageADVEnable#:SENS:AVER:ADV##\&checkONOFF##1.0#6487#[SENSE]Amps function: Enable or disable advanced filter.
GetAverageADVEnable#:SENS:AVER:ADV?####1.0#6487#[SENSE]Amps function: Query state of advanced filter.
SetAverageADVNTolarance#:SENS:AVER:ADV:NTOL##\&checkADVNTOL##1.0#6487#[SENSE]Amps function: Specify noise tolerance (in %); 0 to 105.
GetAverageADVNTolarance#:SENS:AVER:ADV:NTOL?####1.0#6487#[SENSE]Amps function: Query noise tolerance.
SetMedianEnable#:SENS:MED##\&checkONOFF##1.0#6487#[SENSE]Amps function:Enable or disable median filter.
GetMedianEnable#:SENS:MED?####1.0#6487#[SENSE]Amps function: Query state of median filter.
SetMedianRank#:SENS:MED:RANK##\&checkMEDRANK##1.0#6487#[SENSE]Amps function: Specify gnh for rank; 1 to 5 (rank = 2n+1).
GetMedianRank#:SENS:MED:RANK?####1.0#6487#[SENSE]Amps function: Query rank.
#
SetZeroCheckEnable#:SYST:ZCH##\&checkONOFF##1.0#6487#[SENSE]Amps function: Enable or disable zero check.
GetZeroCheckEnable#:SYST:ZCH?####1.0#6487#[SENSE]Amps function: Query state of zero check.
SetZeroCorrectEnable#:SYST:ZCOR##\&checkONOFF##1.0#6487#[SENSE]Amps function: Enable or disable zero correct.
GetZeroCorrectEnable#:SYST:ZCOR?####1.0#6487#[SENSE]Amps function: Query state of zero correct.
AcquireZeroCorrect#:SYST:ZCOR:ACQ####1.0#6487#[SENSE]Amps function: Acquire a new zero correct value.
SetLineFrequency#:SYST:LFR##\&checkLineFrequency#\&syncLineFrequency#1.0#6487#[SENSE]Amps function: Select power line frequency; 50 or 60 (Hz).
GetLineFrequency#:SYST:LFR?####1.0#6487#[SENSE]Amps function: Query frequency setting.
SetLineFrequencyAutoEnable#:SYST:LFR:AUTO##\&checkONOFF#\&syncLineFrequency#1.0#6487#[SENSE]Amps function: Enable or disable auto frequency.
GetLineFrequencyAutoEnable#:SYST:LFR:AUTO?###\&syncLineFrequency#1.0#6487#[SENSE]Amps function: Query state of auto frequency.
SetAutoZeroEnable#:SYST:AZERO##\&checkONOFF##1.0#6487#[SENSE]Amps function: Enable or disable autozero.
GetAutoZeroEnable#:SYST:AZERO?####1.0#6487#[SENSE]Amps function: Query state of autozero.
ResetTimeStamp#:SYST:TIME:RES####1.0#6487#[SENSE]Amps function: Reset timestamp to 0 seconds.
#
SetTraceFeed#:TRAC:FEED##\&checkTRCFEED##1.0#6487#[TRACE]Select source of readings for buffer.; CALCulate[1]orCALCulate[2]orSENSe[1].
GetTraceFeed#:TRAC:FEED?####1.0#6487#[TRACE]Query source of readings for buffer.
SetTraceTimeFormat#:TRAC:TST:FORM##\&checkTRCTIMEFORMAT##1.0#6487#[TRACE]Select timestamp format; ABSolute or DELta. ABS
GetTraceTimeFormat#:TRAC:TST:FORM?####1.0#6487#[TRACE]Query timestamp format.
GetValue#:TRAC:DATA?#\&checkPreGetValue###1.0#6487#
#
SetTriggerArmSource#:ARM:SOUR##\&checkTRIGArmSource#\&syncTRIGArmSource#10#6487#[TRIGGER]Select control source; IMMediate, TIMer, BUS,TLINk, or MANual.
GetTriggerArmSource#:ARM:SOUR?###\&syncTRIGArmSource#1.0#6487#[TRIGGER]Query arm control source.
SetTriggerArmTimer#:ARM:TIM##\&checkTRIGArmTimer##1.0#6487#[TRIGGER]Set timer interval; 0.001 to 99999.999 (sec).
GetTriggerArmTimer#:ARM:TIM?####1.0#6487#[TRIGGER]Query timer interval.
SetTriggerSource#:TRIG:SOUR##\&checkTRIGSource##1.0#6487#[TRIGGER]Select control source; IMMediate or TLINk.
GetTriggerSource#:TRIG:SOUR?####1.0#6487#[TRIGGER]Query trigger control source.
SetTriggerDelay#:TRIG:DEL##\&checkTRIGDELAY##1.0#6487#[TRIGGER]Set trigger delay; 0 to 999.9999 (sec).
GetTriggerDelay#:TRIG:DEL?####1.0#6487#[TRIGGER]Query trigger delay value.
SetTriggerAutoDelayEnable#:TRIG:DEL:AUTO##\&checkONOFF##1.0#6487#[TRIGGER]Enable or disable auto delay.
GetTriggerAutoDelayEnable#:TRIG:DEL:AUTO?####1.0#6487#[TRIGGER]Query state of auto delay.
SetTriggerArmCount#:ARM:COUN#\&dev2Idle#\&checkTRIGArmCount#\&syncTRIGArmCount#1.0#6487#[TRIGGER]Set measure count of arm control; 1 to 2048 or INF.
GetTriggerArmCount#:ARM:COUN?####1.0#6487#[TRIGGER]Query measure count of arm control.
SetTriggerCount#:TRIG:COUN#\&dev2Idle#\&checkTRIGCount#\&syncTRIGCount#1.0#6487#[TRIGGER]Set measure count of trigger control; 1 to 2048.
GetTriggerCount#:TRIG:COUN?####1.0#6487#[TRIGGER]Query measure count of trigger control.
hello#####1.0#6487#return reply message.'@hello nice to meet you.'
help#####1.0#6487#no parameter -> return command list. <paramater> -> show command <paramater> help. 
#help Only Code Embedded
hello#####1.0#6487#return reply message.'@hello nice to meet you.'
help#####1.0#6487#no parameter -> return command list. <Using paramater> -> show command <paramater> help. 
Reset#####1.0#6487#Reset Command. Return the Model 6487 to the *RST default conditions.
Preset#####1.0#6487#Preset Command. Return the Model 6487 to the :SYST:PRES defaults, optimized for front panel operation. 
LoadUserSetup#####1.0#6487#Recall Command. Return the Model 6487 to the setup configuration stored in the specified memory location.
SaveToUserSetup#####1.0#6487#Save Command. Saves the current setup to the specified memory location.
Run#####1.0#6487#Initiate one trigger cycle. Run measurement. 
GoIdle#####1.0#6487#Reset Trigger system(goes to idle state).
#
#m6487 ADDED COMMANDS
#
GetTraceMode#:TRAC:MODE?####1.0#6487#Query buffer mode: DC(normal) or AVOLtage(A-V ohms).
SetTracePoints#:TRAC:POIN##\&checkTracePoints##1.0#6487#[TRACE]Specify size of buffer: 1 to 3000.
GetTracePoints#:TRAC:POIN?####1.0#6487#[TRACE]Query buffer size.
ClearTraceBuffer#:TRAC:CLEAR####1.0#6487#[TRACE]Clear readings from buffer.
RunVoltageSweap#####1.0#6487#Arm sweep and init.
RunOHMSAVMode#####1.0#6487#Arm A-V ohms mode and init.
InitTrigger#####1.0#6487#Initiate one trigger cycle. Run measurement. 
#
#m6487 NEW COMMANDS
#
SetLimitTest1MaxSource2#:CALC2:LIM:UPP:SOURCE2##\&checkSource2##1.0#6487#[CALC2]Limit 1 Testing: Configure upper limit: Specify 4-bit I/O "fail" pattern; 0 to 15.
GetLimitTest1MaxSource2#:CALC2:LIM:UPP:SOURCE2?####1.0#6487#[CALC2]Limit 1 Testing: Query upper limit: 4-bit I/O "fail" pattern.
SetLimitTest1MinSource2#:CALC2:LIM:LOW:SOURCE2##\&checkSource2##1.0#6487#[CALC2]Limit 1 Testing: Configure lower limit: Specify 4-bit I/O "fail" pattern; 0 to 15.
GetLimitTest1MinSource2#:CALC2:LIM:LOW:SOURCE2?####1.0#6487#[CALC2]Limit 1 Testing: Query lower limit: 4-bit I/O "fail" pattern.
SetLimitTest2MaxSource2#:CALC2:LIM2:UPP:SOURCE2##\&checkSource2##1.0#6487#[CALC2]Limit 2 Testing: Configure upper limit: Specify 4-bit I/O "fail" pattern; 0 to 15.
GetLimitTest2MaxSource2#:CALC2:LIM2:UPP:SOURCE2?####1.0#6487#[CALC2]Limit 2 Testing: Query upper limit: 4-bit I/O "fail" pattern.
SetLimitTest2MinSource2#:CALC2:LIM2:LOW:SOURCE2##\&checkSource2##1.0#6487#[CALC2]Limit 2 Testing: Configure lower limit: Specify 4-bit I/O "fail" pattern; 0 to 15.
GetLimitTest2MinSource2#:CALC2:LIM2:LOW:SOURCE2?####1.0#6487#[CALC2]Limit 2 Testing: Query lower limit: 4-bit I/O "fail" pattern.
ResetCompositeLimit#:CALC2:CLIM:CLE####1.0#6487#[CALC2]Composit limits: Clear I/O port and restore it back to SOURCE2:TTL settings.
SetCompositeLimitAutoClearEnable#:CALC2:CLIM:CLE:AUTO##\&checkONOFF##1.0#6487#[CALC2]Composit limits: When enabled, I/O port clears when INITiate is sent.
GetCompositeLimitAutoClearEnable#:CALC2:CLIM:CLE:AUTO?####1.0#6487#[CALC2]Composit limits: Query auto-clear state
SetCompositeLimitSource2#:CALC2:CLIM:PASS:SOURCE2##\&checkTTLOutputPatern##1.0#6487#[CALC2]Composit limits: Define "pass" Digital I/O output pattern.
GetCompositeLimitSource2#:CALC2:CLIM:PASS:SOURCE2?####1.0#6487#[CALC2]Composit limits: Qurey digital I/O output pattern.
# SENSE COMMANDS
SetAnalogFilterDampEnable#:SENS:DAMP##\&checkONOFF##1.0#6487#[SENSE]Amps function: Analog filter damping: Enable or disable.
GetAnalogFilterDampEnable#:SENS:DAMP?####1.0#6487#[SENSE]Amps function: Query analog filter damping: Enable or disable.
SetOHMSModeEnable#:SENS:OHMS##\&checkONOFF##1.0#6487#[SENSE]Amps function: OHMS mode command: Enable or disable.
GetOHMSModeEnable#:SENS:OHMS?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query enable or disable.
ActivateOHMSAVMode#:SENS:OHMS:AVOL####1.0#6487#[SENSE]Amps function: OHMS mode command: Arm A-V ohms mode.
IsOHMSAVModeActivate#:SENS:OHMS:AVOL?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query if A-V ohms is armed. (1=armed).
AbortOHMSAVMode#:SENS:OHMS:AVOL:ABOR####1.0#6487#[SENSE]Amps function: OHMS mode command: Abort A-V ohms mode.
SetOHMSAVHighVoltage#:SENS:OHMS:AVOL:VOLT##\&checkVoltage##1.0#6487#[SENSE]Amps function: OHMS mode command: Set high voltage value (-505 to 505V).
GetOHMSAVHighVoltage#:SENS:OHMS:AVOL:VOLT?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query high voltage value.
SetOHMSAVTimeInterval#:SENS:OHMS:AVOL:TIME##\&checkOHMSAVTimeInterval##1.0#6487#[SENSE]Amps function: OHMS mode command: Set time interval for each phase.
GetOHMSAVTimeInterval#:SENS:OHMS:AVOL:TIME?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query time interval for each phase.
GetOHMSAVPoints#:SENS:OHMS:AVOL:POIN?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query number of points.
SetOHMSAVOneshotEnable#:SENS:OHMS:AVOL:ONES##\&checkONOFF##1.0#6487#[SENSE]Amps function: OHMS mode command: Enable or disable one-shot mode.
GetOHMSAVOneshotEnable#:SENS:OHMS:AVOL:ONES?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query enable or disable one-shot mode.
SetOHMSAVCycles#:SENS:OHMS:AVOL:CYCL##\&checkOHMSAVCycles##1.0#6487#[SENSE]Amps function: OHMS mode command: Set number of A-V cycles (1 to 9999).
GetOHMSAVCycles#:SENS:OHMS:AVOL:CYCL?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query number of A-V cycles.
SetOHMSAVUnits#:SENS:OHMS:AVOL:UNIT##\&checkOHMSUnits##1.0#6487#[SENSE]Amps function: OHMS mode command: Select AMPS or OHMS units.
GetOHMSAVUnits#:SENS:OHMS:AVOL:UNIT?####1.0#6487#[SENSE]Amps function: OHMS mode command: Query units.
ClearOHMSAVBuffer#:SENS:OHMS:AVOL:CLE####1.0#6487#[SENSE]Amps function: OHMS mode command: Clear A-V ohms buffer.
SetOHMSAVBufferAutoClearEnable#:SENS:OHMS:AVOL:CLE:AUTO##\&checkONOFF##1.0#6487#[SENSE]Amps function: OHMS mode command: Enable or disable A-V buffer auto clear.
GetOHMSAVBufferAutoClearEnable#:SENS:OHMS:AVOL:CLE:AUTO?####1.0#6487#[SENSE]Amps function: OHMS mode command: Enable or disable auto clear.
GetOHMSAVCounts#:SENS:OHMS:AVOL:BCO?####1.0#6487#[SENSE]Amps function: Query filter damping OHMS: number of A-V cycles that have been completed and are averaged to make up present buffer.
# SOURCE VOLTAGE
SetVoltageSourceAmplitude#:SOUR:VOLT##\&checkVoltSourceAmplitude##1.0#6487#[SOURCE1]Set voltage source amplitude (-500 to 500).
GetVoltageSourceAmplitude#:SOUR:VOLT?####1.0#6487#[SOURCE1]Query voltage source amplitude.
SetVoltageSourceRange#:SOUR:VOLT:RANG##\&checkVoltSourceRange##1.0#6487#[SOURCE1]Set voltage source range.
SetVoltageSourceCurrentLimit#:SOUR:VOLT:ILIM##\&checkVoltSourceILimit##1.0#6487#[SOURCE1]Set voltage source current limit.
SetVoltageSourceEnable#:SOUR:VOLT:STAT##\&checkONOFF##1.0#6487#[SOURCE1]Enable or disable voltage source output state.
GetVoltageSourceEnable#:SOUR:VOLT:STAT?####1.0#6487#[SOURCE1]Query enable or disable voltage source output state.
SetVoltageInterlockEnable#:SOUR:VOLT:INT##\&checkONOFF##1.0#6487#[SOURCE1]Enable or disable voltage interlock for 10V range.
GetVoltageInterlockEnable#:SOUR:VOLT:INT?####1.0#6487#[SOURCE1]Query enable or disable voltage interlock state.
IsVoltageInterlockFailStatus#:SOUR:VOLT:INT:FAIL?####1.0#6487#[SOURCE1]Query voltage interlock state (1 = interlock asserted).
# SOURCE VOLTAGE SWEEP
SetVoltageSweapStartVoltage#:SOUR:VOLT:SWE:STAR##\&checkVoltage##1.0#6487#[SOURCE1]Sweep commands: Set program start voltage (-505 to 505V).
GetVoltageSweapStartVoltage#:SOUR:VOLT:SWE:STAR?####1.0#6487#[SOURCE1]Sweep commands: Query program start voltage.
SetVoltageSweapStopVoltage#:SOUR:VOLT:SWE:STOP##\&checkVoltage##1.0#6487#[SOURCE1]Sweep commands: Set program stop voltage (-505 to 505V).
GetVoltageSweapStopVoltage#:SOUR:VOLT:SWE:STOP?####1.0#6487#[SOURCE1]Sweep commands: Query program stop voltage.
SetVoltageSweapStepVoltage#:SOUR:VOLT:SWE:STEP##\&checkVoltage##1.0#6487#[SOURCE1]Sweep commands: Set program step voltage (-505 to 505V).
GetVoltageSweapStepVoltage#:SOUR:VOLT:SWE:STEP?####1.0#6487#[SOURCE1]Sweep commands: Query program step voltage.
SetVoltageSweapCenterVoltage#:SOUR:VOLT:SWE:CENTER##\&checkVoltage##1.0#6487#[SOURCE1]Sweep commands: Set program center voltage (-505 to 505V).
GetVoltageSweapCenterVoltage#:SOUR:VOLT:SWE:CENTER?####1.0#6487#[SOURCE1]Sweep commands: Query program center voltage.
SetVoltageSweapSpanVoltage#:SOUR:VOLT:SWE:SPAN##\&checkVoltage##1.0#6487#[SOURCE1]Sweep commands: Set program span voltage (-505 to 505V).
GetVoltageSweapSpanVoltage#:SOUR:VOLT:SWE:SPAN?####1.0#6487#[SOURCE1]Sweep commands: Query program span voltage.
SetVoltageSweapDelay#:SOUR:VOLT:SWE:DELAY##\&checkVoltageSweepDelay##1.0#6487#[SOURCE1]Sweep commands: Set delay (0 to 999.9999s).
GetVoltageSweapDelay#:SOUR:VOLT:SWE:DELAY?####1.0#6487#[SOURCE1]Sweep commands: Query delay.
ActivateVoltageSweap#:SOUR:VOLT:SWE:INIT####1.0#6487#[SOURCE1]Sweep commands: Arm sweep. Put source in operate.
AbortVoltageSweap#:SOUR:VOLT:SWE:ABORT####1.0#6487#[SOURCE1]Sweep commands: Abort sweep. Put source in standby.
IsVoltageSweapStatus#:SOUR:VOLT:SWE:STAT?####1.0#6487#[SOURCE1]Sweep commands: Query if sweep running (1 = sweep in progress).
# SOURCE2
SetDigitalIOTTLLevel#:SOUR2:TTL##\&checkTTLOutputPatern##1.0#6487#[SOURCE2]Specify specify Digital I/O pattern (0 to 15).
GetDigitalIOTTLLevel#:SOUR2:TTL?####1.0#6487#[SOURCE2]Query specify Digital I/O output value.
ClearDigitalIOTTL#:SOUR2:CLE####1.0#6487#[SOURCE2]Clear Digital I/O port immediately.
SetDigitalIOTTLAutoClearEnable#:SOUR2:CLE:AUTO##\&checkONOFF##1.0#6487#[SOURCE2]Enable or disable Digital I/O port auto-clear.
GetDigitalIOTTLAutoClearEnable#:SOUR2:CLE:AUTO?####1.0#6487#[SOURCE2]Query enable or disable Digital I/O port auto-clear.
SetDigitalIOTTLDelay#:SOUR2:CLE:AUTO:DEL##\&checkTTLDelayPatern##1.0#6487#[SOURCE2]Specify delay(pulse width) for pass/fail pattern (0 to 60 sec).
GetDigitalIOTTLDelay#:SOUR2:CLE:AUTO:DEL?####1.0#6487#[SOURCE2]Query delay(pulse width) for pass/fail pattern (0 to 60 sec).
SetDigitalIOTTL4Mode#:SOUR2:TTL4:MODE##\&checkTTL4Mode##1.0#6487#[SOURCE2]Specify output line 4 mode: EOTest ot BUSY.
GetDigitalIOTTL4Mode#:SOUR2:TTL4:MODE?####1.0#6487#[SOURCE2]Query output line 4 mode.
SetDigitalIOTTL4ActiveLevel#:SOUR2:TTL4:BST##\&checkTTL4ActiveBusyStatus##1.0#6487#[SOURCE2]Select active TTL level for busy 1 = ON or 0 = OFF.
GetDigitalIOTTL4ActiveLevel#:SOUR2:TTL4:BST?####1.0#6487#[SOURCE2]Query active TTL level.
