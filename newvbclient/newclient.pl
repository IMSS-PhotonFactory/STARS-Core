#! /usr/bin/perl

use strict;
use constant KEYMIN => 10;
use constant KEYMAX => 18;

$|=1;
print "Make a new Stars client program in VB.\n";

### Input parameter
entvar('ClientName');
entvar('StarsServer');

my $dir = entvar('install_dir',
	"Please enter directory for $::VAR{'ClientName'}.");

### Make directory
mkdir($dir,493) or die "$!";

### Copy files
genfile('Form1.frm', "$dir/Form1.frm");
genfile('newclient.vbp', "$dir/".$::VAR{'ClientName'}.'.vbp');
genfile('newclient.vbw', "$dir/".$::VAR{'ClientName'}.'.vbw');
createkey("$dir/".$::VAR{'ClientName'}.'.key');

print "Done.\n";
print "Please send \"$dir/".$::VAR{'ClientName'}.'.key" to '.
$::VAR{'StarsServer'}."\n with ftp (asc mode).\n";

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
	binmode(BUFOUT);
	while(<BUFIN>){
		chomp;s/\r//;
		foreach $ky (keys(%::VAR)){
			s/<<$ky>>/$::VAR{$ky}/g;
		}
		print BUFOUT "$_\r\n";
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
	binmode(OBUF);
	for($lp=0;$lp<$kcount;$lp++){
	    $klen = int(rand(KEYMAX - KEYMIN)) + KEYMIN;
	    $buf='';
	    for($lp2=0;$lp2<$klen;$lp2++){
		$rd = int(rand 93)+33;
		if($rd >= 0x60){$rd++;}
		$buf .= sprintf("%c",$rd);
	    }
	    print OBUF "$buf\r\n";
	}
	close(OBUF);
	return(1);
}

