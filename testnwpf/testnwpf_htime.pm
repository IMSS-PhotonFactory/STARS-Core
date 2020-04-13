package testnwpf_time;
#use Time::HiRes qw( usleep ualarm gettimeofday tv_interval );
use Time::HiRes qw( usleep gettimeofday tv_interval );


sub l_time {
	my $this = shift;
	return [gettimeofday];
}
sub calc_time {
	my $this = shift;
	my $oldtime = shift;
	my $newtime = shift;
	return tv_interval($oldtime, $newtime);
}

1;
