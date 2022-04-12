#! /usr/bin/perl

use strict;
use Getopt::Long;
use stars;

#################################################################
# streg.pl
# $Revision: 1.4 $
# $Date: 2007/04/23 09:26:54 $
#################################################################
$::RegFile   = 'reg.txt';      #Registry file
#################################################################

##Init variables
%::Reg=();        #cache

loadstregcache();
#savestregcache();

sub createstregcache{
	my $node = shift;
	my $property = shift;
	my $key = "$node:$property";
	if(defined($::Reg{$key})){
		$::Error = 'Property already exists.';
		return('');
	}
	$::Reg{$key}='';
	return('Ok:');
}

sub undefstregcache{
	my $node = shift;
	my $property = shift;
	my $key = "$node:$property";
	unless(defined($::Reg{$key})){
		$::Error = 'There is no property.';
		return('');
	}
	undef($::Reg{$key});
	return('Ok:');
}

sub getstregcacheregex{
	my $node = shift;
	my $property = shift;

	my $buf;
	my $key;
	my @ckeys = keys(%::Reg);
	@ckeys = grep(/^$node:$property/, @ckeys);
	my @vals = ();

	for $key (@ckeys){
		$buf=$key;
		$buf =~ s/^[^:]+://;
		if(defined($::Reg{$key})){
			push(@vals, "$buf=".$::Reg{$key});
		}
	}
	$buf=join("\t", @vals);

	if($buf eq ''){return('default');}
	return($buf);
}

sub getstregcache{
	my $node = shift;
	my $property = shift;
	my $key = "$node:$property";
	return($::Reg{$key});
}

sub getstregkey{
	my $node = shift;
	my $val  = shift;
	my $key;
	my @rtval = ();
	my $buf;

	for $key (keys(%::Reg)){
		if($::Reg{$key} eq $val){
			push(@rtval, $key);
		}
	}
	$buf=join(" ", @rtval);
	$buf =~ s/(^| )$node://g;
	return($buf);
}

sub setstregcache{
	my $node = shift;
	my $property = shift;
	my $value = shift;
	my $key = "$node:$property";
	if($::Reg{$key} eq $value){
		return('Ok:');
	}
	$::Reg{$key}=$value;
	savestregcache();
	return('Ok:');
}

sub loadstregcache{
	open(BUFREG, $::RegFile);
	while(<BUFREG>){
		chomp;s/\r//;
		if(/^#/){next;}
		if(/^([^=]+)=(.*)/){
			$::Reg{$1} = $2;
		}
	}
	return('Ok:');
}

sub savestregcache{
	my $lp;
	open(BUFREG, ">$::RegFile");
	for $lp (keys(%::Reg)){
		if(defined($::Reg{$lp})){
			print BUFREG $lp."=".$::Reg{$lp}."\n";
		}
	}
	close(BUFREG);
	return('Ok:');
}
