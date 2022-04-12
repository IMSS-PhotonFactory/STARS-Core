package testnwpf_time;

use strict;

sub l_time {
	my $this = shift;
	return time();
}
sub calc_time {
	my $this = shift;
	my $oldtime = shift;
	my $newtime = shift;
	return $newtime - $oldtime;
}

1;
