#Acceleration rate
@::rateX=(1000
,  910,  820,  750,  680,  620,  560,  510,  470,  430,  390,  360,  330,  300,  270,  240,  220,  200,  180,  160, 150, 130, 120, 110, 100
,   91,   82,   75,   68,   62,   56,   51,   47,   43,   39,   36,   33,   30,   27,   24,   22,   20,   18,   16,  15,  13,  12,  11,  10
,  9.1,  8.2,  7.5,  6.8,  6.2,  5.6,  5.1,  4.7,  4.3,  3.9,  3.6,  3.3,  3.0,  2.7,  2.4,  2.2,  2.0,  1.8,  1.6, 1.5, 1.3, 1.2, 1.1, 1.0
, 0.91, 0.82, 0.75, 0.68, 0.62, 0.56, 0.51, 0.47, 0.43, 0.39, 0.36, 0.33, 0.30, 0.27, 0.24, 0.22, 0.20, 0.18, 0.16,0.15,0.13,0.12,0.11,0.10
,0.091,0.082,0.075,0.068,0.062,0.056,0.051,0.047,0.043,0.039,0.036,0.033,0.030,0.027,0.024,0.022,0.020,0.018,0.016);

#add subs for pm16c04X
sub pm16cX_GetSTS{
	my($xx);
	mydevwrite("STS?");
	$xx=mydevread();
	return($xx);	
}

#add subs for pm16c04X
sub pm16cX_GetCwCcwLs{
	my($mn,$start)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if($start eq '3'){
		$start='F';
	}elsif($start eq '6'){
		$start='B';
	}elsif(!($start=~/^(F|B)$/)){
		$::Error="Bad Internal $start";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("${start}L?$mn");
	$xx=mydevread();
	$xx=~s/^(\+|\-)0+([^0]\S*)$/${1}${2}/;
	$xx=~s/^\+//;
	$xx=~s/^0+$/0/;
	return($xx);	
}
sub pm16cX_SetCwCcwLs{
	my($mn,$start,$xx)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if(($xx < -2147483647)||($xx > 2147483647)){
		$::Error="Data out of range.";return('');
	}
	if($start eq '3'){
		$start='F';
	}elsif($start eq '6'){
		$start='B';
	}elsif(!($start=~/^(F|B)$/)){
		$::Error="Bad Internal $start";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	$xx=sprintf("%+ld",$xx);
	mydevwrite("${start}L$mn$xx");
	return('Ok:');
}
sub pm16cX_getspeedcommon{
	my($mn,$select)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if($select eq '9'){
		$select='H';
	}elsif($select eq 'A'){
		$select='M';
	}elsif($select eq 'B'){
		$select='L';
	}elsif(!($select=~/^(H|M|L)$/)){
		$::Error="Bad Internal $select";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SPD$select?$mn");
	$xx=mydevread();
	$xx=~s/^0+([^0].*)$/$1/;
	if($xx eq ''){
		$::Error="Read error.";
	}
	return($xx);	
}
sub pm16cX_setspeedcommon{
	my($mn,$speed,$select)=@_;

	unless($select){
		$::Error="System error.";
		return('');
	}
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	if(($speed < 1)||($speed > 5000000)){
		$::Error="Data out of range.";return('');
	}
	if($select eq '9'){
		$select='H';
	}elsif($select eq 'A'){
		$select='M';
	}elsif($select eq 'B'){
		$select='L';
	}elsif(!($select=~/^(H|M|L)$/)){
		$::Error="Bad Internal $select";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
#	my $nowselect=MotorX_GetSpeedSelect($mn);
	my $mnX=sprintf("%X",$mn);
	mydevwrite("SPD$select${mnX}$speed");
#	stars->Sleep(WAIT_MEMWRITE);
#	return(MotorX_SetSpeed($mn,$nowselect));
	return('Ok:');
}

sub MotorX_GetAccRate{
	my($mn)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("RTE?$mn");
	my $xx=mydevread();
	return(pm16cX_code2rate($xx));
}
sub pm16cX_code2rate{
	my($code)=@_;
	return($::rateX[$code]);
}
sub MotorX_GetAccRateCode{
	my($mn)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("RTE?$mn");
	my $xx=mydevread();
	return($xx+0);
}

#---Speed data
sub MotorX_SetAccRate{
	my($mn,$speed)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	if($speed<0){
		$speed=0;
	}
	$mn=sprintf("%X",$mn);
	$speed=pm16cX_rate2code($speed);
	mydevwrite("RTE$mn"."$speed");
	return('Ok:');
}
sub pm16cX_rate2code{
	my($spd)=@_;
	my($code);
	for($code=1;$code <= 115;$code++){
		if($::rateX[$code] < $spd){
			return(sprintf("%03d",$code-1));
		}
	}
	return('115');
}
sub pm16cX_GetValue{
	my($mn,$start)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if($start ne '0'){
#		$::Error="Bad Internal $start";return('');
	}
	$start='PS';
	$mn=sprintf("%X",$mn);
	mydevwrite("${start}?$mn");
	$xx=mydevread();
	$xx=~s/^(\+|\-)0+([^0]\S*)$/${1}${2}/;
	$xx=~s/^\+//;
	$xx=~s/^0+$/0/;
	return($xx);	
}
sub pm16cX_Preset{
	my($mn,$start,$xx)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if(($xx < -2147483647)||($xx > 2147483647)){
		$::Error="Data out of range.";return('');
	}
	if($start ne '0'){
#		$::Error="Bad Internal $start";return('');
	}
	$start='PS';
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	$xx=sprintf("%+ld",$xx);
	mydevwrite("${start}$mn$xx");
	return('Ok:');
}

sub CtlX_GetValue{
	my($ch)=uc(shift);
	my($mn);

	if($ch ne 'A' and $ch ne 'B' and $ch ne 'C' and $ch ne 'D'){
		$::Error="Bad channel.";
		return('');
	}
#Bug read data has no \n
#	mydevwrite("STS?");
#	my $xx=mydevread();
#	print "$xx\n";
#	unless($xx=~/^[L|R](\S)(\S)(\S)(\S)\/\S+\/\S+\/\S+\/(\S+)\/(\S+)\/(\S+)\/(\S+)$/){
#		$::Error="Bad Internal $xx";return('');
#	}
#	if($ch eq 'A'){$xx=$5;}elsif($ch eq 'B'){$xx=$6;}elsif($ch eq 'C'){$xx=$7;}else{$xx=$8;}
#	$xx=~s/^([\+|\-]?)0+([^0]\S*)$/${1}${2}/;
#	$xx=~s/^\+//;
#	$xx=~s/^0+$/0/;
#	return($xx);	
	
	$mn=Ctl_GetSelected($ch);
	return(pm16cX_GetValue($mn,0));
}

sub pm16cX_SetValue{
	my $ch = uc(shift);
	my $pulse = shift;
	my $mn = shift;
	my $mode = shift;
	my $current;
	my $add_cbk;
	my $cm;
	
	if($ch ne 'A' and $ch ne 'B' and $ch ne 'C' and $ch ne 'D'){
		$::Error="Bad channel.";return('');
	}
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if(($pulse < -2147483647)||($pulse > 2147483647)){
		$::Error="Data out of range.";return('');
	}
#####	$current = Ctl_GetValue($ch);
	#Check Add by Naga
	if($mn ne Ctl_GetSelected($ch)){
		$::Error="Bad Internal $ch $mn";return('');
	}
	$current=pm16cX_GetValue($mn,0);
	
	my $abs; # REL Backlash Error 05/10/20 By Naga
	if($mode eq 'REL'){
		my $relpos = $current + $pulse;
		if(($relpos < -2147483647)||($relpos > 2147483647)){
			$::Error="Data out of range.";return('');
		}
		$abs = $relpos; # REL Backlash Error 05/10/20 By Naga
	}else{
		$abs = $pulse; # REL Backlash Error 05/10/20 By Naga
	}

	if($::CancelBacklash[$mn]>0 and $abs > $current){ # REL Backlash Error 05/10/20 By Naga
		$add_cbk = 'B';
	}elsif($::CancelBacklash[$mn]<0 and $abs < $current){ # REL Backlash Error 05/10/20 By Naga
		$add_cbk = 'B';
	}else{
		$add_cbk = '';
	}
	
	my $mnX=sprintf("%X",$mn);
	$pulse=sprintf("%+ld",$pulse);
	
	if($ch eq 'A' and $mode eq 'ABS'){
		$cm="ABS$mnX$add_cbk$pulse"; $::Flg_Busy_A=$mn;
	}elsif($ch eq 'B' and $mode eq 'ABS'){
		$cm="ABS$mnX$add_cbk$pulse"; $::Flg_Busy_B=$mn;
	}elsif($ch eq 'C' and $mode eq 'ABS'){
		$cm="ABS$mnX$add_cbk$pulse"; $::Flg_Busy_C=$mn;
	}elsif($ch eq 'D' and $mode eq 'ABS'){
		$cm="ABS$mnX$add_cbk$pulse"; $::Flg_Busy_D=$mn;
	}elsif($ch eq 'A' and $mode eq 'REL'){
		$cm="REL$mnX$add_cbk$pulse"; $::Flg_Busy_A=$mn;
	}elsif($ch eq 'B' and $mode eq 'REL'){
		$cm="REL$mnX$add_cbk$pulse"; $::Flg_Busy_B=$mn;
	}elsif($ch eq 'C' and $mode eq 'REL'){
		$cm="REL$mnX$add_cbk$pulse"; $::Flg_Busy_C=$mn;
	}elsif($ch eq 'D' and $mode eq 'REL'){
		$cm="REL$mnX$add_cbk$pulse"; $::Flg_Busy_D=$mn;
	}

	mystarssend("$::NodeName.".num2name($mn).">System _ChangedIsBusy 1");

	$::Interval_Time = INTERVAL_RUN;
	if($::Flg_Busy_A ne '' and $::Flg_Busy_B ne ''  and $::Flg_Busy_C ne ''  and $::Flg_Busy_D ne ''){
		mystarssend("System _ChangedCtlIsBusy 1");
	}
	mydevwrite("$cm");
#	$::Elaps=[gettimeofday];
	return('Ok:');
}

sub MotorX_SetLimits{
	my($mn,$st)=@_;
	
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	unless($st=~/^([0|1]){8}$/){
		$::Error="Data invalid.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETLS$mn$st");
	stars->Sleep(WAIT_MEMWRITE);
	return('Ok:');
}

sub MotorX_GetLimits{
	my($mn)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETLS?$mn");
	$xx=mydevread();
	return($xx);	
}
sub CtlX_SetSpeed{
	my $ch=uc(shift);
	my $speed = shift;
	my $mn;
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";return('');
	}
	if($ch eq ''){
		if(Ctl_IsBusy('A') or Ctl_IsBusy('B') or Ctl_IsBusy('C') or Ctl_IsBusy('D')){
			$::Error = "Busy.";return('');
		}
		for($mn=0; $mn<16; $mn++){
			unless(MotorX_SetSpeed($mn,$speed)){return('');}
			stars->Sleep(WAIT_MEMWRITE);
		}
		return('Ok:');
	}elsif($ch eq 'A'){
		if(Ctl_IsBusy('A')){$::Error = "Busy.";return('');}
		$mn=Ctl_GetSelected($ch);
		return(MotorX_SetSpeed($mn,$speed));
	}elsif($ch eq 'B'){
		if(Ctl_IsBusy('B')){$::Error = "Busy.";return('');}
		$mn=Ctl_GetSelected($ch);
		return(MotorX_SetSpeed($mn,$speed));
	}elsif($ch eq 'C'){
		if(Ctl_IsBusy('C')){$::Error = "Busy.";return('');}
		$mn=Ctl_GetSelected($ch);
		return(MotorX_SetSpeed($mn,$speed));
	}elsif($ch eq 'D'){
		if(Ctl_IsBusy('D')){$::Error = "Busy.";return('');}
		$mn=Ctl_GetSelected($ch);
		return(MotorX_SetSpeed($mn,$speed));
	}else{
		$::Error = "Bad channel.";return('');
	}
}

sub MotorX_SetSpeed{
	my $mn = shift;
	my $speed = uc(shift);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	if($speed=~/^([H|M|L])$/){
		mydevwrite("SPD$1$mn");
	}elsif($speed < 1){      #Low
		mydevwrite("SPDL$mn");
	}elsif($speed == 1){ #Middle
		mydevwrite("SPDM$mn");
	}else{               #High
		mydevwrite("SPDH$mn");
	}
	return('Ok:');
}
sub CtlX_GetSpeedSelect{
	my $ch = uc(shift);
	my $mn;
	if($ch ne 'A' and $ch ne 'B' and $ch ne 'C' and $ch ne 'D'){
		$::Error="Bad channel.";
		return('');
	}
	$mn=Ctl_GetSelected($ch);
	return(MotorX_GetSpeedSelect($mn));
}
sub MotorX_GetSpeedSelect{
	my $mn = shift;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SPD?$mn");
	my $xx=mydevread();
	if($xx=~/^([H|M|L])SPD$/){$xx=$1;}
	return($xx);
}

sub MotorX_SetMotorSettings{
	my($mn,$st)=@_;
	
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	unless($st=~/^[0|1][0|1][0|1|2][0|1]$/){
		$::Error="Data invalid.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETMT$mn$st");
	stars->Sleep(WAIT_MEMWRITE);
	return('Ok:');
}

sub MotorX_GetMotorSettings{
	my($mn)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETMT?$mn");
	$xx=mydevread();
	return($xx);	
}
sub MotorX_SetMotorStop{
	my($mn,$st)=@_;
	
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	unless($st=~/^[0|1][0|1]$/){
		$::Error="Data invalid.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("STOPMD$mn$st");
	stars->Sleep(WAIT_MEMWRITE);
	return('Ok:');
}

sub MotorX_GetMotorStop{
	my($mn)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("STOPMD?$mn");
	$xx=mydevread();
	return($xx);	
}

sub MotorX_settimingoutsettings{
	my($mn,$flag,$xx)=(shift,uc(shift),shift);
	my $prevxx;

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	if($flag eq 'M'){
		unless($xx=~/^[0|1|2|3|4|5]$/){
			$::Error="Data invalid.";return('');
		}
	}elsif($flag eq 'S' or $flag eq 'E'){
		if(($xx < -2147483647)||($xx > 2147483647)){
			$::Error="Data out of range.";return('');
		}
	}elsif($flag eq 'I'){
		if(($xx < 0)||($xx > (2147483647) )){
			$::Error="Data out of range.";return('');
		}
	}else{
		$::Error="Bad Internal $flag";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}

	$prevxx=MotorX_gettimingoutsettings($mn,$flag);
	if($prevxx eq ''){
		return('');
	}elsif($prevxx ne $xx){
		MotorX_SetTimingOutReady($mn,0); #Clear TMO Ready
		stars->Sleep(WAIT_MEMWRITE);
	}
	
	my $mnX=sprintf("%X",$mn);
	mydevwrite("TMG$flag$mnX$xx");
	return('Ok:');
}
sub MotorX_gettimingoutsettings{
	my($mn,$flag)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	unless($flag=~/^[M|S|E|I]$/){
		$::Error="Bad Internal $flag";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("TMG$flag?$mn");
	$xx=mydevread();
	if($flag=~/^[S|E|I]$/){
		$xx=~s/^([\+|\-]?)0+([^0]\S*)$/${1}${2}/;
		$xx=~s/^\+//;
		$xx=~s/^0+$/0/;
	}
	return($xx);
}
sub MotorX_SetTimingOutReady{
	my($mn,$flag)=(shift,shift);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless($flag=~/^[0|1]$/){
		$::Error="Bad Internal $flag";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	#Check Channel Selected
	if(($rt=Motor_GetSelected($mn)) eq ''){return('');}
	if($rt eq 'N'){
		$::Error="Channel unselected.";return('');
	}
	$mn=sprintf("%X",$mn);
	if($flag eq 0){
		mydevwrite("TMGC$mn");
	}else{
		mydevwrite("TMGR$mn");
	}
	return('Ok:');
}
sub MotorX_GetTimingOutReady{
	my($mn)=(shift);
	my($xx);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	#Check Channel Selected
	if(($rt=Motor_GetSelected($mn)) eq ''){return('');}
	if($rt eq 'N'){
		$::Error="Channel unselected.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("TMGR?$mn");
	$xx=uc(mydevread());
	$xx=~s/^(YES)$/1/;$xx=~s/^(NO)$/0/;
	return($xx);
}
sub CtlX_SelectForce{
	my($ch,$mn) = @_;
	my($mn2, $sel, $status, $wloop);

	if(($ch eq 'a') || ($ch eq 'A') ){
		$sel='S11';
	}elsif(($ch eq 'b') || ($ch eq 'B')){
		$sel='S12';
	}elsif(($ch eq 'c') || ($ch eq 'C')){
		$sel='S15';
	}elsif(($ch eq 'd') || ($ch eq 'D')){
		$sel='S16';
	}else{
		$::Error="Bad channel.";
		return('');
	}
	if( ($mn < 0) || ($mn > 15) ){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Ctl_IsBusy($ch)){
		$::Error = "Busy.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}

	$mn=sprintf("%X",$mn);
	mydevwrite("S10");
	$status=mydevread();

	if((uc($ch) eq 'A')&&($status =~ /^R(\S)(\S)(\S)(\S)/)){$status = $1; $mn2 = $2.$3.$4;}
	if((uc($ch) eq 'B')&&($status =~ /^R(\S)(\S)(\S)(\S)/)){$status = $2; $mn2 = $1.$3.$4;}
	if((uc($ch) eq 'C')&&($status =~ /^R(\S)(\S)(\S)(\S)/)){$status = $3; $mn2 = $1.$2.$4;}
	if((uc($ch) eq 'D')&&($status =~ /^R(\S)(\S)(\S)(\S)/)){$status = $4; $mn2 = $1.$2.$3;}

#	if($mn2 =~ /$mn/){
#		$::Error="Already selected on other channle.";
#		return('');
#	}

	if($status eq $mn){return('Ok:');}
	mydevwrite("$sel$mn");
	for($wloop=0;$wloop<5;$wloop++){
		mydevwrite("S10");
		$status=mydevread();
		if(($ch =~ /^A$/i)&&($status =~ /^R(\S)\S\S\S/)){$status = $1;}
		if(($ch =~ /^B$/i)&&($status =~ /^R\S(\S)\S\S/)){$status = $1;}
		if(($ch =~ /^C$/i)&&($status =~ /^R\S\S(\S)\S/)){$status = $1;}
		if(($ch =~ /^D$/i)&&($status =~ /^R\S\S\S(\S)/)){$status = $1;}
		if($status eq $mn){return('Ok:');}
		stars->Sleep(WAIT_SELECT);
	}
	$::Error= "Could not select.";
	return("");
}
sub MotorX_ScanHome{
	my $mn = shift;
	my $mode = shift;
	my $cha;
	my $chb;
	my $chc;
	my $chd;
	if( ($mn < 0) || ($mn > 15) ){
		$::Error="Bad motor number.";
		return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn) or Ctl_IsBusy()){
		$::Error = "Busy.";
		return('');
	}
	($cha,$chb,$chc,$chd) = Ctl_GetSelected();
	if($cha == $mn){
		return(pm16cX_Scan('A', $mn, $mode));
	}elsif($chb == $mn){
		return(pm16cX_Scan('B', $mn, $mode));
	}elsif($chc == $mn){
		return(pm16cX_Scan('C', $mn, $mode));
	}elsif($chd == $mn){
		return(pm16cX_Scan('D', $mn, $mode));
	}else{
		if(not Ctl_IsBusy('A')){
			if(Ctl_Select('A', $mn) eq ''){return('');}
			return(pm16cX_Scan('A', $mn, $mode));
		}elsif(not Ctl_IsBusy('B')){
			if(Ctl_Select('B', $mn) eq ''){return('');}
			return(pm16cX_Scan('B', $mn, $mode));
		}elsif(not Ctl_IsBusy('C')){
			if(Ctl_Select('C', $mn) eq ''){return('');}
			return(pm16cX_Scan('C', $mn, $mode));
		}elsif(not Ctl_IsBusy('D')){
			if(Ctl_Select('D', $mn) eq ''){return('');}
			return(pm16cX_Scan('D', $mn, $mode));
		}else{
			$::Error='Busy.';
			return('');
		}
	}
}
sub pm16cX_Scan{
	my $ch = uc(shift);
	my $mn = shift;
	my $mode = shift;
#mode (FD,GT)

	my($cm,$scm,$relpos);

	if($ch eq 'A'){
		$::Flg_Busy_A=$mn;
	}elsif($ch eq 'B'){
		$::Flg_Busy_B=$mn;
	}elsif($ch eq 'C'){
		$::Flg_Busy_C=$mn;
	}elsif($ch eq 'D'){
		$::Flg_Busy_D=$mn;
	}else{
		$::Error="Bad channel.";
		return('');
	}
	unless($mode=~/^(FD|GT)$/){
		$::Error="Bad Internal $mode";return('');
	}

	mystarssend("$::NodeName.".num2name($mn).">System _ChangedIsBusy 1");

	$::Interval_Time = INTERVAL_RUN;
	if(Ctl_IsBusy()){
		mystarssend("System _ChangedCtlIsBusy 1");
	}
	$mn=sprintf("%X",$mn);
	return(mydevwrite("${mode}HP$mn"));
}	
#------Stop------------------------------------------------------
sub CtlX_Stop{
	my $ch   = shift;
	my $mode = shift;
	my $cmd;

	if($mode){
		$cmd = '80';
	}else{
		$cmd = '40';
	}
	if(uc($ch) eq 'A'){
		mydevwrite("S30$cmd");
	}elsif(uc($ch) eq 'B'){
		mydevwrite("S31$cmd");
	}elsif(uc($ch) eq 'C'){
		mydevwrite("S38$cmd");
	}elsif(uc($ch) eq 'D'){
		mydevwrite("S39$cmd");
	}elsif($mode){
		mydevwrite("AESTP");
	}else{
		mydevwrite("ASSTP");
	}
	intervalX(); # Add for flush
	return('Ok:');
}
sub MotorX_SetHPsettings{
	my($mn,$xx)=(shift,shift);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	unless($xx=~/^[0|1]{4}$/){
			$::Error="Data invalid.";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETHP$flag$mn$xx");
	return('Ok:');
}
sub MotorX_GetHPsettings{
	my($mn)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SETHP?$mn");
	$xx=mydevread();
	return($xx);
}
sub MotorX_HPPreset{
	my($mn,$xx)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	if(($xx < -2147483647)||($xx > 2147483647)){
		$::Error="Data out of range.";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	$xx=sprintf("%+ld",$xx);
	mydevwrite("SHP$mn$xx");
	return('Ok:');
}
sub MotorX_GetHPValue{
	my($mn)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SHP?$mn");
	$xx=mydevread();
	if(uc($xx)=~/^NO/){
		$::Error="Ng: $xx";return('');
	}else{
		$xx=~s/^(\+|\-)0+([^0]\S*)$/${1}${2}/;
		$xx=~s/^\+//;
		$xx=~s/^0+$/0/;
	}
	return($xx);	
}
sub MotorX_SetHPOffset{
	my($mn,$xx)=(@_);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	if(($xx < 0)||($xx > 9999)){
		$::Error="Data out of range.";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SHPF$mn$xx");
	return('Ok:');
}
sub MotorX_GetHPOffset{
	my($mn)=@_;
	my($xx);
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SHPF?$mn");
	$xx=mydevread();
	$xx=~s/^([\+|\-]?)0+([^0]\S*)$/${1}${2}/;
	$xx=~s/^\+//;
	$xx=~s/^0+$/0/;
	return($xx);
}

sub CtlX_2DriveAxis{
	my($no,$mode,$mn1,$mn2,$xx1,$xx2,$xx3,$xx4) = @_;

	if( ($mn1 < 0) || ($mn1 > 15) ){$::Error="Bad motor number.";return('');}
	if( ($mn2 < 0) || ($mn2 > 15) ){$::Error="Bad motor number.";return('');}

	if($no eq ''){if(Ctl_IsBusy('A') or Ctl_IsBusy('B')){$no=1;}else{$no=0;}
	}elsif($no eq 'AB'){$no=0;
	}elsif($no eq 'CD'){$no=1;}
	
    if($mode=~/^(ACP|ACN|RCP|RCN|AAC|RAC|ACC|RCC)$/){
    	if($xx3 eq '' or $xx4 eq ''){$::Error="Data out of range.";return('');}
		if(($xx3 < -999999999)||($xx3 > 999999999)){$::Error="Data out of range.";return('');}
		if(($xx4 < -999999999)||($xx4 > 999999999)){$::Error="Data out of range.";return('');}
    }elsif($mode=~/^(ALN|RLN)$/){ #Ok
	}else{
		$::Error="Bad Internal $mode";return('');
    }
   	if($xx1 eq '' or $xx2 eq ''){$::Error="Data out of range.";return('');}
	if(($xx1 < -999999999)||($xx1 > 999999999)){$::Error="Data out of range.";return('');}
	if(($xx2 < -999999999)||($xx2 > 999999999)){$::Error="Data out of range.";return('');}

	unless(Ctl_GetFunction()){$::Error = "Offline.";return('');}
	if(Motor_IsBusy($mn1)){$::Error = "Busy.";return('');}
	if(Motor_IsBusy($mn2)){$::Error = "Busy.";return('');}
	if($no eq 1){
		if(Ctl_IsBusy('C')){$::Error = "Busy.";return('');}
		if(Ctl_IsBusy('D')){$::Error = "Busy.";return('');}
		unless(CtlX_SelectForce('C',$mn1) eq 'Ok:'){return('');}
		unless(CtlX_SelectForce('D',$mn2) eq 'Ok:'){return('');}
		$::Flg_Busy_C=$mn1;
		$::Flg_Busy_D=$mn2;
	}elsif($no eq 0){
		if(Ctl_IsBusy('A')){$::Error = "Busy.";return('');}
		if(Ctl_IsBusy('B')){$::Error = "Busy.";return('');}
		unless(CtlX_SelectForce('A',$mn1) eq 'Ok:'){return('');}
		unless(CtlX_SelectForce('B',$mn2) eq 'Ok:'){return('');}
		$::Flg_Busy_A=$mn1;
		$::Flg_Busy_B=$mn2;
	}else{
		$::Error="Bad Internal $no";return('');
	}
	mystarssend("$::NodeName.".num2name($mn1).">System _ChangedIsBusy 1");
	mystarssend("$::NodeName.".num2name($mn2).">System _ChangedIsBusy 1");
	$::Interval_Time = INTERVAL_RUN;
	if($::Flg_Busy_A ne '' and $::Flg_Busy_B ne ''  and $::Flg_Busy_C ne ''  and $::Flg_Busy_D ne ''){
		mystarssend("System _ChangedCtlIsBusy 1");
	}
	$mn1=sprintf("%X",$mn1);
	$mn2=sprintf("%X",$mn2);
	$xx1=sprintf("%+ld",$xx1);
	$xx2=sprintf("%+ld",$xx2);
    if($mode=~/^(ACP|ACN|RCP|RCN|AAC|RAC|ACC|RCC)$/){
		$xx3=sprintf("%+ld",$xx3);
		$xx4=sprintf("%+ld",$xx4);
		mydevwrite("C$no$mode$mn1$mn2$xx1/$xx2/$xx3/$xx4");
	}else{
		mydevwrite("C$no$mode$mn1$mn2$xx1/$xx2");
	}
	return('Ok:');
}
sub MotorX_ChangeSpeed{
	my($mn,$xx)=(@_);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	if(($xx < 1)||($xx > 5000000)){
		$::Error="Data out of range.";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
	}else{
#		return('Ok:');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("SPC$mn$xx");
	return('Ok:');
}

#---AutoChangeSpeed
sub MotorX_SetAutoChangeSpeed{
	my($mn,$no,$point,$xx,$func,$yy)=@_;

#	print "$mn,$no,$point,$xx,$func,$yy\n";
	if(($mn!~/^\d+$/) || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}

	$mn=sprintf("%X",$mn);
	if(($no!~/^\d+$/) || ($no<0) || ($no>127)){
		$::Error="Bad data number.";return('');
	}
	$no=sprintf("%03d",$no);
	
	$point=uc($point);
    if($point=~/^END$/){
		mydevwrite("ACS$mn$no/END/");
		return('Ok:');
	}elsif($point=~/^ADD$/){
		if(($xx!~/^-?\d+$/) || ($xx < -2147483647)||($xx > 2147483647)){
			$::Error="Data out of range.";return('');
		}
	}elsif($point=~/^TIM$/){
		if(($xx!~/^-?\d+$/) || ($xx < 0)||($xx > 65535)){
			$::Error="Data out of range.";return('');
		}
	}elsif($point=~/^(ACC|DEC)$/){
		if(($xx!~/^-?\d+$/) || ($xx < 1)||($xx > 5000000)){
			$::Error="Data out of range.";return('');
		}
	}else{
		$::Error="Bad point.";return('');
	}

	$func=uc($func);
    if($func=~/^(NOP|FST|SLW)$/){
		mydevwrite("ACS$mn$no/$point/$xx/$func/");
		return('Ok:');
	}elsif($func=~/^RTE$/){
		if(($yy!~/^-?\d+$/) || ($yy < 0)||($yy > 115)){
			$::Error="Data out of range.";return('');
		}
		mydevwrite("ACS$mn$no/$point/$xx/$func/$yy");
		return('Ok:');
	}elsif($func=~/^SPD$/){
		if(($yy!~/^-?\d+$/) || ($yy < 1)||($yy > 5000000)){
			$::Error="Data out of range.";return('');
		}
		mydevwrite("ACS$mn$no/$point/$xx/$func/$yy");
		return('Ok:');
	}else{
		$::Error="Bad func.";return('');
	}
	return('');
}

#---AutoChangeSpeed
sub MotorX_GetAutoChangeSpeed{
	my($mn,$no)=@_;
	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";return('');
	}
	$mn=sprintf("%X",$mn);
	if(($no eq '') || ($no<0) || ($no>127)){
		$::Error="Bad data number.";return('');
	}
	$no=sprintf("%03d",$no);

#	$xx="$mn$no/ADD/010000/SPD/001000"; #test
	mydevwrite("ACS?$mn$no");
	$xx=mydevread();
	if($xx=~s/$mn$no\///){
		my @tmp=split(/\//,$xx);
		if($#tmp >= 3 and $tmp[3]=~/^-?\d+$/){
			$tmp[3]=$tmp[3]+0;
		}
		if($#tmp >= 1 and $tmp[1]=~/^-?\d+$/){
			$tmp[1]=$tmp[1]+0;
		}
		$xx=join(" ",@tmp);
	}
	return($xx);	
}

#---AutoChangeSpeed
sub MotorX_SetAutoChangeSpeedReady{
	my($mn,$flag)=(shift,shift);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	if($flag=~s/^0$/C/){
	}elsif($flag=~s/^1$/P/){
	}else{
		$::Error="Bad Internal $flag";return('');
	}
	unless(Ctl_GetFunction()){
		$::Error = "Offline.";
		return('');
	}
	if(Motor_IsBusy($mn)){
		$::Error = "Busy.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	
	mydevwrite("ACS$flag$mn");
	return('Ok:');
}
sub MotorX_GetAutoChangeSpeedReady{
	my($mn)=(shift);
	my($xx);

	if(($mn eq '') || ($mn<0) || ($mn>15)){
		$::Error="Bad motor number.";
		return('');
	}
	$mn=sprintf("%X",$mn);
	mydevwrite("ACSP?$mn");
	$xx=mydevread();
	if(uc($xx)=~/NOT/){
		$xx=0;
	}else{
		$xx=1;
	}
	return($xx);
}

sub add_help_listX{
	my $title='';
	my $titlenew;
	my $buf='';
	my $target='';

#Remove Command
	delete $::helpmotor{"GetSpeedList"};
	delete $::helpcntrl{"GetSpeedList"};

	my $data=<<EOF;
Usage: DrawLine [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY
Target: Controller
    Draw straight line, using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to absolute "EndValueX",
    and "MotorNumberY" (0 to 16) from it's current to absolute "EndValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawLineREL [ChannelSet] MotorNumberX MotorNumberY ValueX ValueY
Target: Controller
    Draw straight line, using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to relative "ValueX",
    and "MotorNumberY" (0 to 16) from it's current to relative "ValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircularCw [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY CenterValueX CenterValueY
Target: Controller
    Draw cw direction circlular with absolute center position data("CenterValueX", "CenterValueY"),
    using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to absolute "EndValueX",
    and "MotorNumberY" (0 to 16) from it's current to absolute "EndValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircularCwREL [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY CenterValueX CenterValueY
Target: Controller
    Draw cw direction circlular with relative center position data("CenterValueX", "CenterValueY"),
    using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to relative "EndValueX",
    and "MotorNumberY" (0 to 16) from it's current to relative "EndValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircularCcw [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY CenterValueX CenterValueY
Target: Controller
    Draw ccw direction circlular with absolute center position data("CenterValueX", "CenterValueY"),
    using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to absolute "EndValueX",
    and "MotorNumberY" (0 to 16) from it's current to absolute "EndValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircularCcwREL [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY CenterValueX CenterValueY
Target: Controller
    Draw ccw direction circlular with relative center position data("CenterValueX", "CenterValueY"),
    using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to relative "EndValueX",
    and "MotorNumberY" (0 to 16) from it's current to relative "EndValueY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawArc [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY ByPassPointX ByPassPointY
Target: Controller
    Draw arc using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to absolute "EndValueX" passing by absolute "ByPassPointX",
    and "MotorNumberY" (0 to 16) from it's current to absolute "EndValueY" passing by absolute "ByPassPointY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawArcREL [ChannelSet] MotorNumberX MotorNumberY EndValueX EndValueY ByPassPointX ByPassPointY
Target: Controller
    Draw arc using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to relative "EndValueX" passing by relative "ByPassPointX",
    and "MotorNumberY" (0 to 16) from it's current to relative "EndValueY" passing by relative "ByPassPointY".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircle [ChannelSet] MotorNumberX MotorNumberY ByPassPointX1 ByPassPointY1 ByPassPointX2 ByPassPointY2
Target: Controller
    Draw arc using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to current passing by absolute "ByPassPointX1" and "ByPassPointX2",
    and "MotorNumberY" (0 to 16) from it's current passing by absolute "ByPassPointY1" and "ByPassPointY2".
	"ChannelSet" can be omitted to be selected automatically.

Usage: DrawCircleREL [ChannelSet] MotorNumberX MotorNumberY ByPassPointX1 ByPassPointY1 ByPassPointX2 ByPassPointY2
Target: Controller
    Draw arc using "ChannelSet" ({AB or 0} or {CD or 1})
    by moving "MotorNumberX" (0 to 16) from it's current to current passing by relative "ByPassPointX1" and "ByPassPointX2",
    and "MotorNumberY" (0 to 16) from it's current passing by relative "ByPassPointY1" and "ByPassPointY2".
	"ChannelSet" can be omitted to be selected automatically.

Usage: SpeedLow [MotorNumber]
Target: Controller
    Set speed to "Low" to "MotorNumber" (0 to 16).
    If it's not specified, all motors will be set to "Low".

Usage: SpeedMiddle [MotorNumber]
Target: Controller
    Set speed to "Middle" to "MotorNumber" (0 to 16).
    If it's not specified, all motors will be set to "Middle".

Usage: SpeedHigh [MotorNumber]
Target: Controller
    Set speed to "High" to "MotorNumber" (0 to 16).
    If it's not specified, all motors will be set to "High".

Usage: SpeedLow
Target: Motor
    Set speed to "Low".

Usage: SpeedMiddle
Target: Motor
    Set speed to "Middle".

Usage: SpeedHigh
Target: Motor
    Set speed to "High".

Usage: GetSpeedSelected MotorNumber
Target: Controller
    Return selected speed ("H" (high), "M" (middle), "L" (low)) of "MotorNumber" (0 to 16).

Usage: GetSpeedSelected
Target: Motor
    Return selected speed ("H" (high), "M" (middle), "L" (low)).

Usage: SetSpeedCurrent MotorNumber SpeedValue
Target: Controller
    Change speed to "SpeedValue" of "MotorNumber" (0 to 16) only while motor running.

Usage: SetSpeedCurrent SpeedValue
Target: Motor
    Change speed to "SpeedValue" only while motor running.

Usage: SetTimingOutMode MotorNumber Value
Target: Controller
    Set timing out mode value of "MotorNumber" (0 to 16) into "Value".
    Value 0: disable, 1: TTL gate , 2: TTL interval 200ns
          3: TTL interval 10us 4: TTL interval 100us, 5: TTL interval 1ms

Usage: SetTimingOutMode Value
Target: Motor
    Set timing out mode value into "Value".
    Value 0: disable, 1: TTL gate , 2: TTL interval 200ns
          3: TTL interval 10us 4: TTL interval 100us, 5: TTL interval 1ms

Usage: SetTimingOutStart MotorNumber Value
Target: Controller
    Set timing out start position value of "MotorNumber" (0 to 16) into "Value".

Usage: SetTimingOutStart Value
Target: Motor
    Set timing out start position value into "Value".

Usage: SetTimingOutEnd MotorNumber Value
Target: Controller
    Set timing out end position value of "MotorNumber" (0 to 16) into "Value".

Usage: SetTimingOutEnd Value
Target: Motor
    Set timing out end position value into "Value".

Usage: SetTimingOutInterval MotorNumber Value
Target: Controller
    Set timing out interval value of "MotorNumber" (0 to 16) into "Value".

Usage: SetTimingOutInterval Value
Target: Motor
    Set timing out interval value into "Value".

Usage: SetTimingOutReady MotorNumber 1|0
Target: Controller
    Set timing out ready (set=1, clear=0) of "MotorNumber" (0 to 16).

Usage: SetTimingOutReady 1|0
Target: Motor
    Set timing out ready (set=1, clear=0).

Usage: GetTimingOutMode MotorNumber
Target: Controller
    Return timing out mode value of "MotorNumber" (0 to 16).

Usage: GetTimingOutMode
Target: Motor
    Return timing out mode value.

Usage: GetTimingOutStart MotorNumber
Target: Controller
    Return timing out start position value of "MotorNumber" (0 to 16).

Usage: GetTimingOutStart
Target: Motor
    Return timing out start position value.

Usage: GetTimingOutEnd MotorNumber
Target: Controller
    Return timing out end position value of "MotorNumber" (0 to 16).

Usage: GetTimingOutEnd
Target: Motor
    Return timing out end position value.

Usage: GetTimingOutInterval MotorNumber
Target: Controller
    Return timing out interval value of "MotorNumber" (0 to 16).

Usage: GetTimingOutInterval
Target: Motor
    Return timing out interval value.

Usage: GetTimingOutReady MotorNumber
Target: Controller
    Return timing out ready value of "MotorNumber" (0 to 16).

Usage: GetTimingOutReady
Target: Motor
    Return timing out ready value.

Usage: SetHPMode MotorNumber 0XYZ
Target: Controller
    Set home position scan mode and status 4 digits value of "MotorNumber" (0 to 16) into "0XYZ" as
        0: preserved, always 0
        X: found status, 0/not found 1/found
        Y: found direction, 0/cw 1/ccw
        Z: auto start direction, 0/cw 1/ccw

Usage: SetHPMode 0XYZ
Target: Motor
    Set home position scan mode and status 4 digits value into "0XYZ" as
        0: preserved, always 0
        X: found status, 0/not found 1/found
        Y: found direction, 0/cw 1/ccw
        Z: auto start direction, 0/cw 1/ccw

Usage: GetHPMode MotorNumber
Target: Controller
    Return home position scan mode and status 4 digits value of "MotorNumber" (0 to 16).

Usage: GetHPMode
Target: Motor
    Return home position scan mode and status 4 digits value.

Usage: SetHomePosition MotorNumber Value
Target: Controller
    Write home position pulse of "MotorNumber" (0 to 16) into "Value".

Usage: SetHomePosition Value
Target: Motor
    Write home position pulse into "Value".

Usage: GetHomePosition MotorNumber
Target: Controller
    Return home position pulse value of "MotorNumber" (0 to 16).

Usage: GetHomePosition
Target: Motor
    Return home position pulse value.

Usage: SetHPOffset MotorNumber Value
Target: Controller
    Set home position offset value used in rescanning of "MotorNumber" (0 to 16) into "Value".

Usage: SetHPOffset Value
Target: Motor
    Set home position offset value used in rescanning into "Value".

Usage: GetHPOffset MotorNumber
Target: Controller
    Return home position offset value used in rescanning of "MotorNumber" (0 to 16).

Usage: GetHPOffset
Target: Motor
    Return home position offset value used in rescanning.

Usage: SetMotorSetup MotorNumber ABCD
Target: Controller
    Set motor basic properties 4 digits value of "MotorNumber" (0 to 16) into "ABCD" as
        A: 1/drive enable 0/drive disable
        B: 1/hold on 0/hold off
        C: 0/const 1/trapezoidal 2/S character
        D: 0/Pulse-Pulse 1/Pulse-Direction

Usage: SetMotorSetup ABCD
Target: Motor
    Set motor basic properties 4 digits value into "ABCD" as
        A: 1/drive enable 0/drive disable
        B: 1/hold on 0/hold off
        C: 0/const 1/trapezoidal 2/S character
        D: 0/Pulse-Pulse 1/Pulse-Direction

Usage: GetMotorSetup MotorNumber
Target: Controller
    Return motor basic properties 4 digits value of "MotorNumber" (0 to 16).

Usage: GetMotorSetup
Target: Motor
    Return motor basic properties 4 digits value.

Usage: SetStopMode MotorNumber AB
Target: Controller
    Set stop mode 2 digits value of "MotorNumber" (0 to 16) into "AB" as
        A: how to stop for cw/ccw limit switch, 0/LS slow stop 1/LS fast stop
        B: how to stop for panel stop button , 0/PB slow stop 1/PB fast stop

Usage: SetStopMode AB
Target: Motor
    Set stop mode 2 digits value into "AB" as
        A: how to stop for cw/ccw limit switch, 0/LS slow stop 1/LS fast stop
        B: how to stop for panel stop button , 0/PB slow stop 1/PB fast stop

Usage: GetStopMode MotorNumber
Target: Controller
    Get stop mode 2 digits value of "MotorNumber" (0 to 16).

Usage: GetStopMode
Target: Motor
    Get stop mode 2 digits value.

Usage: ReScanHome MotorNumber
Target: Controller
    Move "MotorNumber" (0 to 16) near to the home position previously found fastly, then start finding home position.

Usage: ReScanHome
Target: Motor
    Move near to the home position previously found fastly, then start finding home position.

Usage: GetChannelStatus
Target: Controller
    Return information of selected channels.
    Return Data Format: [R|L]abcd/PNNS/VVVV/HHJJKKLL/+-uu.../+-vv.../+-ww.../+-xx...
    "R" or "L"  Remote or Local
    "abcd"      Selected MotorNumbers(0 - F) of Channel A,B,C,D
    "PNNS"      Drive status ("P":cw "N":ccw "S":Stop) of Channel A,B,C,D
    "VVVV"      Ls status and Hold off Status (bit0:cw ls bit1:ccw ls bit2:hp ls bit3:hold off(1/hold off 0/hold on) of Channel A,B,C,D
    "HHJJKKLL"  Motor current status
        bit 0: BUSY, 1: Pulse output running, 2: Accelerating, 3: Decelerating
            4: Error, 5: Stopped by LS, 6: Stopped slowly 7: Stopped fastly
    "+-uu..."   current of Channel A
    "+-vv..."   current of Channel B
    "+-ww..."   current of Channel C
    "+-xx..."   current of Channel D

Usage: ScanHome MotorNumber
Target: Controller
    Move "MotorNumber" (0 to 16) for finding home position.

Usage: ScanHome
Target: Motor
    Move for finding home position.

Usage: SetAutoChangeSpeed MotorNumber DataNumber ConditionCode ConditionValue FunctionCode FunctionValue
Target: Controller
    Set parameters of Auto-Change-Speed function of "MotorNumber" (0 to 16).

        DataNumber    0 to 127.

        ConditionCode ConditionValue     Set condition to execute function.
        ----------------------------------------------------------------------------
            "ADD"   within +-2147483647  relative address from start point.   
            "TIM"      0 to 65535        relative time(ms) from previous point.   
            "ACC"     1 to 5000000       speed data(pps) while acceleration.
            "DEC"     1 to 5000000       speed data(pps) while deceleration.
            "END"      N/A,ignored       End of record.

        FunctionCode FunctionValue       Action speed.
        -----------------------------------------------------------------------
            "SPD"     1 to 5000000       speed in pps.   
            "RTE"      0 to 115          rate code number.   
            "SLW"      N/A,ignored       slow stop.
            "FST"      N/A,ignored       fast stop.
            "NOP"      N/A,ignored       no operation.
         N/A,ignored   N/A,ignored       when "ConditionCode" equals "END".

Usage: SetAutoChangeSpeed DataNumber ConditionCode ConditionValue FunctionCode FunctionValue
Target: Motor
    Set parameters of Auto-Change-Speed function.

        DataNumber    0 to 127.

        ConditionCode ConditionValue     Set condition to execute function.
        ----------------------------------------------------------------------------
            "ADD"   within +-2147483647  relative address from start point.   
            "TIM"      0 to 65535        relative time(ms) from previous point.   
            "ACC"     1 to 5000000       speed data(pps) while acceleration.
            "DEC"     1 to 5000000       speed data(pps) while deceleration.
            "END"      N/A,ignored       End of record.

        FunctionCode FunctionValue       Action speed.
        -----------------------------------------------------------------------
            "SPD"     1 to 5000000       speed in pps.   
            "RTE"      0 to 115        rate code number.   
            "SLW"      N/A,ignored       slow stop.
            "FST"      N/A,ignored       fast stop.
            "NOP"      N/A,ignored       no operation.
         N/A,ignored   N/A,ignored       when "ConditionCode" equals "END".

Usage: SetAutoChangeSpeedReady MotorNumber 1|0
Target: Controller
    Set Auto-Change-Speed function ready (set=1, clear=0) of "MotorNumber" (0 to 16).

Usage: SetAutoChangeSpeedReady 1|0
Target: Motor
    Set Auto-Change-Speed function ready (set=1, clear=0).

Usage: GetAutoChangeSpeed MotorNumber DataNumber
Target: Controller
    Get parameters of Auto-Change-Speed function of "DataNumber" of "MotorNumber" (0 to 16).

        DataNumber    0 to 127.

    Return Value:
        ConditionCode ConditionValue     Set condition to execute function.
        ----------------------------------------------------------------------------
            "ADD"   within +-2147483647  relative address from start point.   
            "TIM"      0 to 65535        relative time(ms) from previous point.   
            "ACC"     1 to 5000000       speed data(pps) while acceleration.
            "DEC"     1 to 5000000       speed data(pps) while deceleration.
            "END"      N/A,ignored       End of record.

        FunctionCode FunctionValue       Action speed.
        -----------------------------------------------------------------------
            "SPD"     1 to 5000000       speed in pps.   
            "RTE"      0 to 115          rate code number.   
            "SLW"      N/A,ignored       slow stop.
            "FST"      N/A,ignored       fast stop.
            "NOP"      N/A,ignored       no operation.
         N/A,ignored   N/A,ignored       when "ConditionCode" equals "END".

Usage: GetAutoChangeSpeed DataNumber
Target: Motor
    Get parameters of Auto-Change-Speed function of "DataNumber".

        DataNumber    0 to 127.

    Return Value:
        ConditionCode ConditionValue     Set condition to execute function.
        ----------------------------------------------------------------------------
            "ADD"   within +-2147483647  relative address from start point.   
            "TIM"      0 to 65535        relative time(ms) from previous point.   
            "ACC"     1 to 5000000       speed data(pps) while acceleration.
            "DEC"     1 to 5000000       speed data(pps) while deceleration.
            "END"      N/A,ignored       End of record.

        FunctionCode FunctionValue       Action speed.
        -----------------------------------------------------------------------
            "SPD"     1 to 5000000       speed in pps.   
            "RTE"      0 to 115          rate code number.   
            "SLW"      N/A,ignored       slow stop.
            "FST"      N/A,ignored       fast stop.
            "NOP"      N/A,ignored       no operation.
         N/A,ignored   N/A,ignored       when "ConditionCode" equals "END".

Usage: GetAutoChangeSpeedReady MotorNumber
Target: Controller
    Get Auto-Change-Speed function ready (set=1, clear=0) of "MotorNumber" (0 to 16).

Usage: GetAutoChangeSpeedReady
Target: Motor
    Get Auto-Change-Speed function ready (set=1, clear=0).

EOF
	foreach (split(/\n/,$data)){
#	while(<DATA>){
		$_="$_\n";
		if(/^(?:Usage|Event): (\w+)( |$)/){
			$titlenew = $1;
			if($title){
				$buf =~ s/\r//gm;
				$buf =~ s/\n/\\n/gm;
				if($target =~ /Motor/){
					$::helpmotor{$title} = $buf;
				}
				if($target =~ /Controller/){
					$::helpcntrl{$title} = $buf;
				}
				$buf = '';
			}
			$title = $1;
		}
		if(/Target: (.+)/){
			$target=$1;
			next;
		}
		$buf .= $_;
	}

	$buf =~ s/\r//gm;
	$buf =~ s/\n/\\n/gm;
	if($target =~ /Motor/){
		$::helpmotor{$title} = $buf;
	}
	if($target =~ /Controller/){
		$::helpcntrl{$title} = $buf;
	}
}
1
