###########################################################
## Script library for STARS scriptclient.
## Takashi Kosuge.
$::LibVersion ='
Version: 2 
$Revision: 1.2 $
$Date: 2011-02-17 02:47:30 $
';
###########################################################
$::Version    =~ s/(\n|\r|\$)//g;
$::Version    =~ s/\s+/ /g;
$::LibVersion =~ s/(\n|\r|\$)//g;
$::LibVersion =~ s/\s+/ /g;
$::Author     =~ s/(\n|\r|\$)//g;
$::Author     =~ s/\s+/ /g;

use stars;
use strict;
use Getopt::Long;
use Math::Trig;

stLoadParam('configscript.cfg');
if($::Param{'STARS_Server'}){
	$::StarsServer = $::Param{'STARS_Server'};
}else{
	$::StarsServer = 'localhost';
}
if(($::NodeName eq '') and $::Param{'STARS_NodeName'}){
	$::NodeName = $::Param{'STARS_NodeName'};
}

$::Debug      = ''; #This variable is used for debug mode.
                    # You can use like..
                    # if($::Debug){blha-blah-blah;}

$::Remote = '';     #Screen print flag.
$::Silent = 0;      #Flg silent. all printout will be suppressed with this flg.

$::DataDir = './data';
$::DataFile = '';
$::CurrentDataFile = 'currentdata.txt';
$::CurrentDataFileNewFlag = 1;
$::CurrentDataFileOutputFlag = 1;

%::Param = ();      #Parameters;

## ToDo: You can set option switchs. See help 'Getopt::Long'.
GetOptions(
'd'        => \$::Debug,
'data=s'   => \$::DataDir,
'server=s' => \$::StarsServer,
'remote=s' => \$::Remote,
'currentoutputflag=s' => \$::CurrentDataFileOutputFlag,
'nodename=s' => \$::NodeName,
'h'        => \&usage
) or die "Bad switch.\n";


#initialise STARS
#####$::NodeName   = 'scriptclient';        #Default node name.
if($::NodeName eq ''){
	$::NodeName   = 'scriptclient';        #Default node name.
}
$::TimeOut    = 10;
$::WaitFrom   = '';
$::Cmd        = '';

$|=1;

if($::Offline){
	$::Remote = '';
}else{
	$::tak = stars->new($::NodeName, $::StarsServer)
		or die "Could not connect Stars server";
	stSendEvent("$::NodeName _Started $0.");

#2009-12-11 T. Kosuge
	$::prevSilent = $::Silent;
	$::Silent = 1;
	stWait("_Started");
	$::Silent = $::prevSilent;

}

# Print usage. ---------------------------------------------
sub usage{
## Todo: Please modify help message for "-h" option.

## Create argument list from $::Param for help output.
my $args='';
my $lparg;
my $argc = 0;
if($::Param){
	for $lparg (split(/\s+/, $::Param)){
		if($args eq ''){
			$args = " [-- $lparg";
		}else{
			$args .= " [$lparg";
		}
		$argc++;
	}
	for($lparg=0; $lparg<$argc; $lparg++){
		$args .= ']';
	}
}

## Add help message for online.
my $rmthelpsw='';
my $rmthelp='';
unless($::Offline){
	$rmthelpsw = ' [-server STARS_Server] [-nodename STARS_NodeName] [-remote Remote_Terminal] [-currentoutputflag <0|1>]';
	$rmthelp   = '
    -server STARS_Server    Set STARS server host name to connect.
                Default server host is "'.$::StarsServer.'".
    -nodename STARS_NodeName    Set STARS nodename to connect.
                Default nodename is "'.$::NodeName.'".
    -remote Remote_Terminal   Suppress print screen of stPrint and outoput
                to Remote_Terminal the message instead of the screen.
    -currentoutputflag <0|1>
                Control output of current datafile "'.$::CurrentDataFile.'".
                Set 0 to disable. Default value is "'.$::CurrentDataFileOutputFlag.'".
';
}

## Print help.
print <<__VERSION__;
$0 $::Version
 (Library $::LibVersion)
__VERSION__


print <<__AUTHOR__ if $::Author;
Author: $::Author
__AUTHOR__


print <<__USAGEANDSWITCHES__;

Usage: $0 [-h] [-d] [-data DataDir]$rmthelpsw$args
    -h      Show this help.
    -d      Run with debug mode.
    -data DataDir  Set data output directory. "./data" is used by default.$rmthelp
__USAGEANDSWITCHES__


print <<__ARGMENTS__ if $::Param;
    Argments  Use "--" as a separator of switchs and argments if any
            argment starts with "-" (eg. -123).
__ARGMENTS__


print <<__DESCRIPTION__ if $::Description;

Description: $::Description
__DESCRIPTION__


exit(0);
}


sub stSendEvent{
	if($::Offline){return('Offline');}
	my $buf = shift;
	if($buf =~ /^([a-zA-Z_0-9.\-]+)>([a-zA-Z_0-9.\-]+)\s+(\S+)/){
		$::WaitFrom = $2;
		$::Cmd = $3;
	}elsif($buf =~ /^([a-zA-Z_0-9.\-]+)\s+(\S+)/){
		$::WaitFrom = $1;
		$::Cmd = $2;
	}else{
		$::WaitFrom = '';
		$::Cmd = '';
	}
	my $rt = $::tak->Send($buf);
	return($rt);
}

sub stSendCommand{
	if($::Offline){return('Offline');}
	my $buf = shift;
	stSendEvent($buf);
	return(stWait('@'.$::Cmd));
}

sub stWait{
	if($::Offline){return('Offline');}
	if(@_ > 2){return(_stWait(@_));}
	my $waitmess = shift;
	my $waitfrom = shift;
	my $waitfrom2;
	my $flgpr=1;
	if($waitmess =~ /^\@/){$flgpr = 0;}
	unless($waitfrom){$waitfrom=$::WaitFrom;}
	if($flgpr){stPrint("Waiting $waitfrom $waitmess\n");}
	my $from = '';
	my $rt;
	my $waitfrom2;
	($waitfrom2,$_)=split(".",$waitfrom,2);
	while(1){
		($from, undef, $rt) = $::tak->Read($::TimeOut);
		unless($from){return('');}
		if($rt eq "Break"){
			$::tak->Send("\@Break Ok:", $from);
			stDie("Break");
		}elsif($rt eq "_Break"){
			stDie("Break");
		}
		if($flgpr){stPrint("\r$from $rt");}
		unless(($from eq 'System') and ($rt=~/$waitfrom2 is down/)){
			unless($from eq $waitfrom){next;}
			unless($rt =~ /^$waitmess/){next;}
		}
		$rt =~ s/^\S+\s+//;
		if($flgpr){stPrint("\n");}
		return($rt);
	}
}

sub _stWait{
	if($::Offline){return('Offline');}
	my $scount = @_;
	$scount = int($scount/2);
	my $lp;
	my @wcmd = ();
	my @wfrom = ();
	my $wcount = $scount;
	my $from;
	my $rt;
	my $mess = '';
	for($lp = 0; $lp < $scount; $lp++){
		$wcmd[$lp]  = shift;
		$wfrom[$lp] = shift;
		$mess .= "$wfrom[$lp] $wcmd[$lp]/";
	}
	$mess =~ s/\/$//;
	stPrint("Waiting $mess\n");
	while($wcount){
		($from, undef, $rt) = $::tak->Read($::TimeOut);
		unless($from){return('');}
		if($rt eq "Break"){
			$::tak->Send("\@Break Ok:", $from);
			stDie("Break");
		}elsif($rt eq "_Break"){
			stDie("Break");
		}
		stPrint("\r$from $rt");
		for($lp=0; $lp<$scount; $lp++){
			unless($wfrom[$lp]){next;}
			if($from eq $wfrom[$lp] and $rt =~ /^$wcmd[$lp]/){
				$wfrom[$lp] = '';
				$wcount--;
				stPrint("\n");
			}
		}
	}
	$rt =~ s/^\S+\s+//;
	return($rt);
}

sub stSleep{
	my $tm = shift;
	select(undef,undef,undef,$tm);
}


sub stGetLocaltime{
my $tm = shift(@_);
if($tm eq ''){$tm=time();}
my @tt = localtime($tm);
return(sprintf("%04d-%02d-%02d %02d:%02d:%02d",
$tt[5]+1900,$tt[4]+1,$tt[3],$tt[2],$tt[1],$tt[0]));
}

sub stAddSuffixDataFile{
	my $ts = stGetLocaltime();
	$ts =~ s/ +/_/g;
	$ts =~ s/://g;
	if($::DataFile){
		$::DataFile .= "_" . $ts .".txt";
	}else{
		$::DataFile = "$ts.txt";
	}
}

sub stFprintf{
	my $buf = shift;
	stWriteFile(sprintf($buf, @_));
}

sub stWriteFile{
	my $mess = shift;
	my $currentfile = '';
	unless($::DataFile){
		stAddSuffixDataFile();
	}
	unless($::DataDir =~ /\/$/){$::DataDir .= '/';}
	unless(open(DATAOUTPUTBUFFER, ">>$::DataDir$::DataFile")){
		warn "Could not write data file.\n";
		return;
	}
	print DATAOUTPUTBUFFER $mess;
	close(DATAOUTPUTBUFFER);

	if($::CurrentDataFileOutputFlag){
		if($::CurrentDataFileNewFlag){
			$::CurrentDataFileNewFlag = 0;
			$currentfile = ">$::DataDir$::CurrentDataFile";
		}else{
			$currentfile = ">>$::DataDir$::CurrentDataFile";
		}

		unless(open(DATAOUTPUTBUFFER, $currentfile)){
			warn "Could not write data file.\n";
			return;
		}
		print DATAOUTPUTBUFFER $mess;
		close(DATAOUTPUTBUFFER);
	}
	
	if($::Remote){
		$mess =~ s/[\r\n]/\\n/g;
		$::tak->Send("$::Remote _Msg $mess");
	}else{
		print $mess;
	}
}

sub stPrintf{
	my $buf = shift;
	my $mess = sprintf($buf, @_);
	stPrint($mess);
}

sub stPrint{
	my $mess = shift;
	my $del = '';

#2009-12-11 T. Kosuge
	if($::Silent){return;}

	if($::Remote){
		$mess =~ s/[\r\n]//g;
		if($mess ne ''){
			$::tak->Send("$::Remote _Msg $mess");
		}
	}else{
		if($mess =~ s/^\r//){
			printf("\r%79s\r");
		}
		print $mess;
	}
}

sub stLoadParam{
	my $fname = shift;
	unless($fname){$fname="$0.cfg";}
	open(READPARAMBUFFER, $fname) or return undef;
	while(<READPARAMBUFFER>){
		chomp;s/\r//;
		if(/^#/){next;}
		if(/(\S+)\s*=(\s*.*)/){
			$::Param{$1} = $2;
		}
	}
}

sub stSaveParam{
	my $fname = shift;
	unless($fname){$fname="$0.cfg";}
	my $lp;
	open(READPARAMBUFFER, ">".$fname) or return undef;
	for $lp (keys(%::Param)){
		print READPARAMBUFFER "$lp=$::Param{$lp}\n";
	}
	close(READPARAMBUFFER);
}

sub stSetParam{
	my $pkey = shift;
	unless($pkey){
		$pkey = $::Param;
		@_ = @ARGV;
	}
	my @pkey = split(/\s+/, $pkey);
	my $lp;
	my $prtvalue;
	my $buf;
	my @sparam = ();
	my $sparamcount;
	my $argcount = @_;

	for $lp (@pkey){
		if(@_ >0 ){
			$::Param{$lp} = shift;
#			if($::Param{$lp} =~ /['"]([\-0-9.+]+)['"]/){
#				$::Param{$lp} = $1;
#			}
		}else{
			if($::Remote){last;}
			$prtvalue = $lp;
			$prtvalue =~ s/_/ /g;
			print "Enter $prtvalue. ";
			if(defined($::Param{$lp})){
				print "($::Param{$lp}) ";
			}
			print "> ";
			$buf = <STDIN>;
			chomp($buf); $buf =~ s/\r//;
			if($buf eq ''){
				unless(defined($::Param{$lp})){return(undef);}
			}else{
				$::Param{$lp} = $buf;
			}
		}
	}
	unless($::Remote){
		for $lp (@pkey){
			$prtvalue = $lp;
			$prtvalue =~ s/_/ /g;
			printf("%8s = %s\n", $prtvalue, $::Param{$lp});
		}
	}

	for $lp (@pkey){
		push(@sparam, $::Param{$lp});
	}
	$sparamcount = @sparam;

	if(wantarray){
		if(!$::Remote and $sparamcount != $argcount){stYesNo("Ok?") or stDie("Cancelled.\n");}
		return(@sparam);
	}
	if(!$::Remote and $sparamcount != $argcount){stYesNo("Ok?") or stDie("Cancelled.\n");}
	return($sparamcount);
}

sub stYesNo{
    my $comment = shift;
    my $default = shift;
	my $ans;
	my $from;

	if($::Remote){
		$::tak->Send("GetYesNo", $::Remote);
		while(1){
			($from, undef, $ans) = $::tak->Read($::TimeOut);
			if($ans =~ /\@GetYesNo\s+([YyNn])/){
				$ans = uc($1);
				last;
			}elsif($ans eq "Break"){
				$::tak->Send("\@Break Ok:", $from);
				stDie("Break");
			}elsif($ans eq "_Break"){
				stDie("Break");
			}
		}
	}else{
    	if($default){
        	$comment .= " ([y]/n) > ";
    	}else{
        	$comment .= " (y/[n]) > ";
        	$default = 0;
    	}
    	my $prv = $|;
    	$| = 1;
    	print $comment;
    	$| = $prv;
    	$ans = <STDIN>;
    	chomp($ans);
	}

    $ans = uc($ans);
    if($ans eq 'Y'){
        return(1);
    }elsif($ans eq 'N'){
        return(0);
    }
    return($default);
}

sub stGetScanList{
	my $initial = shift;
	my $final = shift;
	my $step = shift;
	unless($step){return(undef);}

#Fix step automatically. 2011-10-11 by T. Kosuge
	$step = abs($step);
	if($initial > $final){
		$step *= -1;
	}

	my @rt = ();
	my $scan_initial;
	my $scan_final;
	my $scan_step;
	my $scan_rangev = 0;
	my $scan_lp;
	while(int($initial*(10**$scan_rangev)) != $initial*(10**$scan_rangev)){$scan_rangev++;}
	my $scan_rangev_keta = $scan_rangev;
	while(int($final*(10**$scan_rangev)) != $final*(10**$scan_rangev)){$scan_rangev++;}
	if($scan_rangev_keta<$scan_rangev){
		$scan_rangev_keta=$scan_rangev;
	}
	while(int($step*(10**$scan_rangev)) != $step*(10**$scan_rangev)){$scan_rangev++;}
	if($scan_rangev_keta<$scan_rangev){
		$scan_rangev_keta=$scan_rangev;
	}
	$scan_initial = $initial*(10**$scan_rangev);
	$scan_final = $final*(10**$scan_rangev);
	$scan_step = $step*(10**$scan_rangev);
	for($scan_lp=$scan_initial; 
		($scan_step>=0 and $scan_lp<=$scan_final) or ($scan_step<0 and $scan_lp>=$scan_final);
		 $scan_lp += $scan_step){
		if($scan_rangev_keta>=1){
			push(@rt, sprintf("%0.${scan_rangev_keta}lf",$scan_lp/(10**$scan_rangev)));
		}else{
			push(@rt, $scan_lp/(10**$scan_rangev));
		}
	}
	return(@rt);
}

sub stDie{
	my $mess = shift;
	if($::Remote){
		$mess =~ s/[\r\n]/\\n/g;
		$::tak->Send("_Died $mess", $::Remote);
		die "\n";
	}else{
		die $mess;
	}
}

1;
