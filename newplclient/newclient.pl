#! /usr/bin/perl
#####################################################################
# Create new STARS client program in Perl.
# Takashi Kosuge
# $Id$'
#
#####################################################################

use strict;
use constant KEYMIN => 10;
use constant KEYMAX => 18;

$|=1;

print "Make a new Stars client program in Perl.\n";
### Input parameter
entvar('client_name');
entvar('stars_server');

my $dir = entvar('install_dir',
	"Please enter directory for $::VAR{'client_name'}.");

$::VAR{'DefaultPort'} = '6057';
$::VAR{'Modified'} = 'Id: '.$::VAR{'client_name'}.' 00 '.ksg_localtime().'Z stars ';

### Make directory
mkdir($dir,493) or die "$!";

### Copy files
genfile('../perllib/stars.pm', "$dir/stars.pm");
genfile('newclient.tmplt', "$dir/".$::VAR{'client_name'});
createkey("$dir/".$::VAR{'client_name'}.'.key');

print "Done.\n";
print "Please send \"$dir/".$::VAR{'client_name'}.'.key" to '.
$::VAR{'stars_server'}."\n with ftp (asc mode).\n";

print "Hit Enter key.";
$_=<STDIN>;

exit(0);

sub entvar{
	my $ky=shift;
	my $mess = shift;
	unless($mess){
		$mess=$ky;
		$mess =~ s/_/ /g;
		$mess = "Please enter $mess.";
	}
	print "$mess (null = cancel) >";
	$::VAR{$ky} = <STDIN>;
	chomp($::VAR{$ky});
	if($::VAR{$ky} eq ''){
		die "Canceled\n";
	}
	return($::VAR{$ky});
}

sub genfile{
	my ($from,$to)=@_;
	my $ky;

	print "Create $to.\n";
	open(BUFIN,"$from") or die "$!";
	open(BUFOUT,">$to") or die "$!";
	while(<BUFIN>){
		chomp;s/\r//;
		foreach $ky (keys(%::VAR)){
			s/<<$ky>>/$::VAR{$ky}/g;
		}
		print BUFOUT "$_\n";
	}
	close(BUFOUT);
	close(BUFIN);
#	chmod(0744,"$to");
}

sub createkey{
	my $filename = shift;
	my $kcount = shift;

	print "Create key > $filename.\n";
	unless($filename){
		die "Bad key file name.";
	}
	unless($kcount){
		$kcount=400;
	}

	srand(time()^($$+($$<<15)));

	my $lp;
	my $ry;
	my $lp2;
	my $buf;
	my $rd;
	my $klen;
	open(OBUF, ">$filename") or die;
	for($lp=0;$lp<$kcount;$lp++){
	    $klen = int(rand(KEYMAX - KEYMIN)) + KEYMIN;
	    $buf='';
	    for($lp2=0;$lp2<$klen;$lp2++){
		$rd = int(rand 93)+33;
		if($rd >= 0x60){$rd++;}
		$buf .= sprintf("%c",$rd);
	    }
	    print OBUF "$buf\n";
	}
	close(OBUF);
	return(1);
}

sub ksg_localtime{
my $tm = shift(@_);
if($tm eq ''){$tm=time();}
my @tt = localtime($tm);
return(sprintf("%04d-%02d-%02d %02d:%02d:%02d",
$tt[5]+1900,$tt[4]+1,$tt[3],$tt[2],$tt[1],$tt[0]));
}
