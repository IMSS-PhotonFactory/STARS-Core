#!/usr/bin/perl
#use strict;
use Socket;

#-----------------------------------------------------------------------------
sub _getpwd{
	my($pwd)=(Cwd::getcwd());if($pwd=~/^\S\:/){$pwd=~s/\//\\/g;}
	unless($pwd=~/^(\S\:)?[\\|\/]$/){$pwd=~s/[\\|\/]$//;}return($pwd);
}
#-----------------------------------------------------------------------------
sub _usemodule{
	my($mod)=(shift);
	if($mod){
		eval "use $mod";
		unless($@){$::MYISMODULE{$mod}=1;}else{$::MYISMODULE{$mod}=0;}
		return($::MYISMODULE{$mod});
	}else{print "Error: Module name is empty.","\n";}
	return(0);
}
#-----------------------------------------------------------------------------
sub _ismodule{
	my($mod)=(shift);
	if(defined($::MYISMODULE{$mod})){return($::MYISMODULE{$mod});
	}else{print "Error: Value of module '$mod' undefined.","\n";}
	return(0);
}
#-----------------------------------------------------------------------------
sub myinit{
	%::MYISMODULE=();
	%::MYVALUE=();
	@::MYCONFIGCONTENTS=();
	%::MYCONFIGINDEX=();
	%::MYCONFIGVALUE=();
	return(1);
}
#-----------------------------------------------------------------------------
BEGIN {
	use Getopt::Long;
	use File::Copy;
	use File::Path;
	use File::Temp qw/ tempfile tempdir /;
	use FindBin qw($Bin); use lib "$Bin";

	use constant DEFAULT_CONFIG_FILE    => "starsinst.cfg";

	use constant STARS_DOWNLOAD_SITE    => "stars.kek.jp";
	use constant STARS_DOWNLOAD_PORT    => 80;
	use constant STARS_DOWNLOAD_TOPURL  => "/download_stars/";
	use constant STARS_DOWNLOAD_ZIPPAGE => "package_win.html";
	use constant STARS_DOWNLOAD_TGZPAGE => "package_unix.html";
	use constant DEFAULT_TGZCOMMAND    => 'zcat $TGZ$ | tar -xvf -';
	use constant DEFAULT_PERMISSION     => 750;

	use constant MSG0_DIR_EXIST            => 901;
	use constant MSG0_DIR_NOTFOUND         => 902;
	use constant MSG0_FILE_EXIST           => 911;
	use constant MSG0_FILE_NOTFOUND        => 912;
	use constant MSG0_FILE_COPY_FAIL       => 913;
	use constant MSG0_FILE_OPEN_FAIL       => 914;
	use constant MSG0_FILE_OVERWRITE_FAIL  => 915;
	use constant MSG0_FILE_OLD_RENAME_FAIL => 916;
	use constant MSG0_TMPFILE_COPY_FAIL    => 923;
	use constant MSG0_TMPFILE_RENAME_FAIL  => 926;
	use constant MSG0_CHMOD_FAIL           => 981;
	use constant MSG0_MKDIR_FAIL           => 982;
	use constant MSG0_PATHNAME_INVALID     => 983;
	use constant MSG0_CHMODE_INVALID       => 963;
	use constant MSG0_PERMISSION_INVALID   => 966;
	use constant MSG0_COMMAND_EXEC_FAIL    => 967;
	use constant MSG0_ARCTYPE_INVALID      => 964;
	use constant MSG0_TGZ_KEYWORD_NOTFOUND => 965;
	use constant MSG0_ZIPFILE_INVALID      => 968;
	use constant MSG0_TGZFILE_INVALID      => 969;

	use constant MSGW_COPY_SAMEFILE_SKIP   => 801;
	use constant MSGW_FILE_UTIME_FAIL      => 802;
	use constant MSGW_EXTRACT_SAMEMOD_SKIP => 803;
	use constant MSGI_COPY_START           => 701;
	use constant MSGI_COPY_DONE            => 702;
	use constant MSGI_FILE_OLD_RENAMED     => 703;
	use constant MSGI_CONFIG_UPD_START     => 704;
	use constant MSGI_CONFIG_UPD_END       => 705;
	use constant MSGI_CONFIG_UPD_UNCHANGED => 706;
	use constant MSGI_CONFIG_READ_START    => 707;
	use constant MSGI_CONFIG_READ_END      => 708;
	use constant MSGI_MKDIR_START          => 711;
	use constant MSGI_MKDIR_DONE           => 712;
	use constant MSGI_WEBDLD_START         => 713;
	use constant MSGI_WEBDLD_END           => 714;
	use constant MSGI_USERPERMISSION_BLANK => 715;
	use constant MSGI_USERTGZCOMMAND_BLANK => 716;
	use constant MSGI_COMMAND_EXEC_START   => 717;
	use constant MSG0_INTERNAL_ERROR       => 999;
	use constant MSG0_MOD_NOTFOUND         => 932;
	use constant MSG0_CONFIG_OPEN_FAIL     => 944;
	use constant MSG0_WEBDLD_FAIL          => 954;

	use constant MOD_ARCHIVE_ZIP           => "Archive::Zip";
	use constant MOD_WIN32_SHORTCUT        => "Win32::Shortcut";
	use constant KEY_ISWINOS               => 'is_winos';
	use constant KEY_DIRDELIM              => 'path_delemiter';
	use constant KEY_PWD                   => 'program_startup_directory';
	use constant KEY_ARCTYPE               => 'user_default_arctype';
	use constant KEY_ARCDIR                => 'user_default_stars_archived_file_directory';
	use constant KEY_STARSDEST             => 'user_default_stars_destination_directory';
	use constant KEY_STARSSRC              => 'user_default_stars_source_directory';
	use constant KEY_USERPERMISSION        => 'user_filepermission';
	use constant KEY_USERTGZCOMMAND        => 'user_tgzcommand';

	use constant CONST_ZIP                 => 'zip';
	use constant CONST_TGZ                 => 'tgz';

	myinit();
	_usemodule(MOD_ARCHIVE_ZIP);
	_usemodule(MOD_WIN32_SHORTCUT);
}
sub _subprintmessage{
	my($msg,$nonretflg)=(shift,shift);unless($nonretflg){$msg.="\n";}
	print $msg;
	if($::MYLOGFILE){
		$_=_cnvdatetime(1);
		unless(open(FILE,">>$::MYLOGFILE")){
print<<ESUBPRNMESSAGE1;
============================================================
Caution Me !!!!
Error: Unabled to open logfile '$::MYLOGFILE'.
If you want to skip logging, execute command 'set LOGFILE='.
============================================================
ESUBPRNMESSAGE1
			return(0);
		}
		print FILE "$_ $msg";close(FILE);
	}
	return(1);
}
#-----------------------------------------------------------------------------
sub _printmessage{
	my @args=@_;
	my($msg)=('','');
	if($#args<0){_subprintmessage("");return(1);
	}elsif($args[0] eq MSG0_DIR_EXIST){
		_subprintmessage("Error: Exists as directory '$args[1]'.");
	}elsif($args[0] eq MSG0_FILE_EXIST){
		_subprintmessage("Error: Exists as file '$args[1]'.");
	}elsif($args[0] eq MSG0_DIR_NOTFOUND){
		_subprintmessage("Error: Directory not found '$args[1]'.");
	}elsif($args[0] eq MSG0_FILE_NOTFOUND){
		_subprintmessage("Error: File not found '$args[1]'.");
	}elsif($args[0] eq MSG0_FILE_COPY_FAIL){
		_subprintmessage("Error: Unabled to copy '$args[1]' to '$args[2]'.");
	}elsif($args[0] eq MSG0_FILE_OPEN_FAIL){
		_subprintmessage("Error: Unabled to open file '$args[1]'.");
	}elsif($args[0] eq MSG0_FILE_OVERWRITE_FAIL){
		_subprintmessage("Error: Unabled to overwrite '$args[1]' to '$args[2]'.");
	}elsif($args[0] eq MSG0_TMPFILE_COPY_FAIL){
		_subprintmessage("Error: Unabled to copy '$args[1]' to temporary file '$args[2]'.");
	}elsif($args[0] eq MSGW_COPY_SAMEFILE_SKIP){
		_subprintmessage("Warn: Same file exists. Skipped copying '$args[1]' to '$args[2]'.");return(1);
	}elsif($args[0] eq MSGW_FILE_UTIME_FAIL){
		_subprintmessage("Warn: Unabled to update time stamp of '$args[1]'.");return(1);
	}elsif($args[0] eq MSGW_EXTRACT_SAMEMOD_SKIP){
		_subprintmessage("Warn: Newer version has been already extracted. Skipped extracting '$args[1]' to '$args[2]'.");return(1);
	}elsif($args[0] eq MSGI_COPY_START){
		_subprintmessage("Copying '$args[1]' to '$args[2]'..");return(1);
	}elsif($args[0] eq MSGI_COPY_DONE){
		_subprintmessage("Copy has done.");return(1);
	}elsif($args[0] eq MSGI_WEBDLD_START){
		_subprintmessage("Downloading '$args[1]' into '$args[2]'..");return(1);
	}elsif($args[0] eq MSGI_WEBDLD_END){
		_subprintmessage("Downloaded successfully.");return(1);
	}elsif($args[0] eq MSGI_MKDIR_START){
		_subprintmessage("Creating directory '$args[1]'..");return(1);
	}elsif($args[0] eq MSGI_MKDIR_DONE){
		_subprintmessage("Directory has created.");return(1);
	}elsif($args[0] eq MSGI_FILE_OLD_RENAMED){
		_subprintmessage("Old version of '$args[1]' has renamed to '$args[2]'.");return(1);
	}elsif($args[0] eq MSGI_CONFIG_UPD_START){
		_subprintmessage("Refleshing configuration file '$args[1]'..");return(1);
	}elsif($args[0] eq MSGI_CONFIG_UPD_END){
		_subprintmessage("Configuration file '$args[1]' has updated successfully.");return(1);
	}elsif($args[0] eq MSGI_CONFIG_UPD_UNCHANGED){
		_subprintmessage("No need to change configuration file '$args[1]'.");return(1);
	}elsif($args[0] eq MSGI_CONFIG_READ_START){
		_subprintmessage("Reading configuration file '$args[1]'..");return(1);
	}elsif($args[0] eq MSGI_CONFIG_READ_END){
		_subprintmessage("Configuration reading done.");return(1);
	}elsif($args[0] eq MSGI_USERPERMISSION_BLANK){
		_subprintmessage("Value for key '".KEY_USERPERMISSION."' set blank.\nDefault permission '".DEFAULT_PERMISSION."' is selected.");
		return(1);
	}elsif($args[0] eq MSGI_USERTGZCOMMAND_BLANK){
		_subprintmessage("If key '".KEY_USERTGZCOMMAND."' set blank, Default tgz file extracting command '".DEFAULT_TGZCOMMAND."' is used. Keyword \$TGZ\$ is replaced with tgz filename.");
		return(1);
	}elsif($args[0] eq MSGI_COMMAND_EXEC_START){
		_subprintmessage("Executing command \`$args[1]\`...");return(1);
	}elsif($args[0] eq MSG0_FILE_OLD_RENAME_FAIL){
		_subprintmessage("Error: Unabled to rename old version '$args[1]' to '$args[2]'.");
	}elsif($args[0] eq MSG0_TMPFILE_RENAME_FAIL){
		_subprintmessage("Error: Unabled to rename temporary file '$args[1]' to '$args[2]'.");
	}elsif($args[0] eq MSG0_PERMISSION_INVALID){
		_subprintmessage("Error: File permission value '$args[1]' invalid.");
	}elsif($args[0] eq MSG0_CHMOD_FAIL){
		_subprintmessage("Error: Permission denied '$args[1]'.");
	}elsif($args[0] eq MSG0_MKDIR_FAIL){
		_subprintmessage("Error: Unabled to create directory '$args[1]'.");
	}elsif($args[0] eq MSG0_PATHNAME_INVALID){
		_subprintmessage("Error: Invalid name '$args[1]'.");
	}elsif($args[0] eq MSG0_INTERNAL_ERROR){
		_subprintmessage("Error: Internal error $args[1].");
	}elsif($args[0] eq MSG0_MOD_NOTFOUND){
		_subprintmessage("Error: Package '$args[1]' not found. Please 'list' for it first.");
	}elsif($args[0] eq MSG0_CONFIG_OPEN_FAIL){
		_subprintmessage("Error: Unabled to open configuration file '$args[1]'.");
	}elsif($args[0] eq MSG0_WEBDLD_FAIL){
		_subprintmessage("Error: Unabled to download '$args[1]' to '$args[2]'.");
	}elsif($args[0] eq MSG0_CHMODE_INVALID){
		_subprintmessage("Error: File permission invalid '$args[1]'.");
	}elsif($args[0] eq MSG0_ARCTYPE_INVALID){
		_subprintmessage("Error: Archive-type must be 'ZIP' or 'TGZ', not '$args[1]'.");
	}elsif($args[0] eq MSG0_TGZ_KEYWORD_NOTFOUND){
		_subprintmessage("TGZ extract command has to contain keyword \$TGZ\$, which is replaced with 'tgz filename'. '$args[1]'.");
	}elsif($args[0] eq MSG0_COMMAND_EXEC_FAIL){
		_subprintmessage("Error: Command '$args[1]' executing failed. ($args[2]).");
	}elsif($args[0] eq MSG0_ZIPFILE_INVALID){
		_subprintmessage("Error: File '$args[1]' is invalid zip file.");
	}elsif($args[0] eq MSG0_TGZFILE_INVALID){
		_subprintmessage("Error: File '$args[1]' is invalid tgz file.");
	}elsif($args[0]){_subprintmessage("@args");return(1);
	}else{_subprintmessage("");return(1);}
	return(0);
}
#-----------------------------------------------------------------------------
sub _printprompt{my $msg=shift;_subprintmessage("$msg",1);return(1);}
#-----------------------------------------------------------------------------
sub _showvariable{
	my($key)=(shift);
	if($key){
		if(defined($::MYVALUE{$key})){_printmessage("$key=$::MYVALUE{$key}");
		}else{_printmessage("$key=''");}
	}else{
		foreach$_(sort(keys(%::MYVALUE))){_printmessage("$_=$::MYVALUE{$_}");}
	}
	if($key eq KEY_USERPERMISSION){
		if($::MYVALUE{$key} eq ''){_printmessage(MSGI_USERPERMISSION_BLANK);}
	}elsif($key eq KEY_USERTGZCOMMAND){
		if($::MYVALUE{$key} eq ''){_printmessage(MSGI_USERTGZCOMMAND_BLANK);}
	}
	return(1);
}
#-----------------------------------------------------------------------------
sub _setvariable{
	my($key,$val)=(shift,shift);
	if($key eq KEY_ARCTYPE){
		$val=lc($val);
		if(($val eq CONST_ZIP)or($val eq CONST_TGZ)){
			if(defined($::MYVALUE{$key})){
				if($val ne _getvariable(KEY_ARCTYPE)){
					if(mygetstarsarclist($val)){$::MYVALUE{$key}=$val;}
				}
			}else{if(mygetstarsarclist($val)){$::MYVALUE{$key}=$val;}}
		}else{_printmessage(MSG0_ARCTYPE_INVALID,$val);}
	}elsif(($key eq KEY_ARCDIR)or($key eq KEY_STARSDEST)or($key eq KEY_STARSSRC)){
		if(($val eq '') or ($val=_checkpathname($val))){$::MYVALUE{$key}=$val;}
	}elsif($key eq KEY_USERPERMISSION){
		if(($val eq '') or _getmode($val)){$::MYVALUE{$key}=$val;}
	}elsif($key eq KEY_USERTGZCOMMAND){
		if(($val eq '') or _gettgzcommand($val)){$::MYVALUE{$key}=$val;}
	}elsif($key){
		$::MYVALUE{$key}=$val;
	}else{_printmessage("Error: Keyword is empty.");return('');}
	_showvariable($key);
	return($val);
}
sub _getvariable{
	my($key)=(shift);
	if(defined($::MYVALUE{$key})){return($::MYVALUE{$key});
	}elsif($key eq KEY_ARCDIR){return('');
	}elsif($key eq KEY_STARSDEST){return('');
	}elsif($key eq KEY_STARSSRC){return('');
	}elsif($key eq KEY_USERPERMISSION){return('');
	}elsif($key eq KEY_USERPERMISSION){return('');
	}elsif($key eq KEY_USERTGZCOMMAND){return('');
	}else{_printmessage("Error: Value of '$key' undefined.");}
	return('');
}
#-----------------------------------------------------------------------------
sub _execcommand{
	my($cmd)=(shift);
	_printmessage("="x78);
	_printmessage(MSGI_COMMAND_EXEC_START,$cmd);
	_printmessage("-"x60);
	my $rt=qx/$cmd/;
	my $sts=$?;
	if($sts){
		_printmessage(MSG0_COMMAND_EXEC_FAIL,$cmd,"$! $sts $rt");
		if(wantarray){return(0,$rt);}else{return(0);}
	}else{
		_printmessage($rt);
		if(wantarray){return(1,$rt);}else{return(1);}
	}
}
#-----------------------------------------------------------------------------
sub _cnvdatetime{
	my($formatflag,$sc,$mn,$hh,$dd,$mm,$y4)
            =(shift,shift,shift,shift,shift,shift,shift);
	if($sc eq ''){
		my($d1,$d2,$d3);
		($sc,$mn,$hh,$dd,$mm,$y4,$d1,$d2,$d3)=localtime(time);
		$y4=$y4+1900;$mm=$mm+1;
	}
	unless($formatflag){
		return(sprintf("%04d%02d%02d%02d%02d%02d",$y4,$mm,$dd,$hh,$mn,$sc));
	}
	return(sprintf("%04d\/%02d\/%02d %02d:%02d:%02d",$y4,$mm,$dd,$hh,$mn,$sc));
}
#-----------------------------------------------------------------------------
sub _getconfigfilename{
	my($filename)=(shift);
	if($filename eq ''){
		$filename=_getvariable(KEY_PWD)._getvariable(KEY_DIRDELIM)."starsinst.cfg";
	}
	$filename=_checkdirnotexist($filename);return($filename);
}
#-----------------------------------------------------------------------------
sub _gettgzcommand{
	my($tgzcommand,$tgzfile)=(shift,shift);
	if($tgzcommand eq ''){
		$_=_getvariable(KEY_USERTGZCOMMAND);
		unless($_ eq ''){$tgzcommand=$_;}else{$tgzcommand=DEFAULT_TGZCOMMAND;}
	}
	if($tgzfile){
		unless($tgzcommand=~s/\$TGZ\$/$tgzfile/g){
			printmessage(MSG0_TGZ_KEYWORD_NOTFOUND,$tgzcommand);return('');
		}
	}else{
		unless($tgzcommand=~/\$TGZ\$/){
			printmessage(MSG0_TGZ_KEYWORD_NOTFOUND,$tgzcommand);return('');
		}
	}return($tgzcommand);
}
#-----------------------------------------------------------------------------
sub _getmode{
	my($mode)=(shift);
	if($mode eq ''){$mode=DEFAULT_PERMISSION;}
	unless($mode=~/^[0-7]{3}$/){
		_printmessage(MSG0_PERMISSION_INVALID,$mode);return('');
	}return($mode);
}
#-----------------------------------------------------------------------------
sub _mktempdir{
	my($dirpath)=(tempdir(CLEANUP=>1));return($dirpath);
}
#-----------------------------------------------------------------------------
sub _mktempfile{
	my($dirpath)=(shift);
	unless($dirpath=_checkdirexist($dirpath)){return(0);}
	my($fh,$filename)=tempfile(DIR=>$dirpath,UNLINK =>1);
	return($fh,$filename);
}
#-----------------------------------------------------------------------------
sub _getfileinfo{
	my($filename,$no)=(shift,shift);
	unless($filename=_checkpathname($filename)){return(0);}
	unless(-e $filename){_printmessage(MSG0_FILE_NOTFOUND,$filename);return('')}
	my @sts=stat($filename);
	$sts[2]=substr((sprintf "%03o", $sts[2]), -3);
	if($no eq ''){return($sts[9],$sts[7],$sts[2]);
	}elsif(0<=$no and $no<=$#sts){return($sts[$no]);}
	return(join(" ",@sts));
}
#-----------------------------------------------------------------------------
sub _getftype{
	my($path)=(shift);
	if(-d $path){if(-w $path){return('dw');}else{return('d');}
	}elsif(-e $path){if(-w $path){return('fw');}else{return('f');}
	}return('');
}
#-----------------------------------------------------------------------------
sub _checkdirexist{
	my($path)=(shift);unless($path=_checkpathname($path)){return('');}
	my($ftype)=_getftype($path);
	unless($ftype=~/^d/){_printmessage(MSG0_DIR_NOTFOUND,$path);return('');}
	return($path);
}
#-----------------------------------------------------------------------------
sub _checkdirnotexist{
	my($path)=(shift);unless($path=_checkpathname($path)){return('');}
	my($ftype)=_getftype($path);
	if($ftype=~/^d/){_printmessage(MSG0_DIR_EXIST,$path);return('');
	}else{return($path);}
}
#-----------------------------------------------------------------------------
sub _checkfileexist{
	my($path)=(shift);unless($path=_checkpathname($path)){return('');}
	my($ftype)=_getftype($path);
	if($ftype=~/^f/){return($path);
	}else{_printmessage(MSG0_FILE_NOTFOUND,$path);return('');}
}
#-----------------------------------------------------------------------------
sub _checkfilenotexist{
	my($path)=(shift);unless($path=_checkpathname($path)){return('');}
	my($ftype)=_getftype($path);
	if($ftype=~/^f/){_printmessage(MSG0_FILE_EXIST,$path);return('');
	}else{return($path);}
}
#-----------------------------------------------------------------------------
sub _checkpathname{
	my($path)=(shift);
	my($pwd,$pdrv,$ppath)=(_getpwd(),'','');
	my(@rank,@prank)=((),());

	my $delim=_getvariable(KEY_DIRDELIM);
	$path=~s/^\s+//;$path=~s/\s+$//;$path=~s/[\\|\/]+/$delim/;
	if($path eq ''){
		_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
	}elsif($path=~/[\\|\/]\s+/ or $path=~/\s+[\\|\/]/){
		_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
	}elsif($path=~/[\.]{3,}/){
		_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
	}elsif(_getvariable(KEY_ISWINOS)){
		unless($pwd=~/^([^\:])\:[\\|\/](.*)/){
			_printmessage(MSG0_INTERNAL_ERROR,"for PWD '$pwd'");return('');
		}else{$pdrv=$1;$ppath=$2;}
		@rank=split(/\:/,$path);
		if($#rank>=2){_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
		}elsif($#rank eq 1){
			if($rank[0]!~/^\S$/){_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
			}elsif($rank[0]=~/^$pdrv$/i){
				if($rank[1]=~s/^[\\|\/]//){$rank[0]="$pdrv\:$delim";
				}else{
					$rank[0]="$pdrv\:$delim";
					if($ppath eq ''){$rank[1]=$rank[1];
					}else{$rank[1]="$ppath$delim$rank[1]";}
				}
			}elsif(-d "$rank[0]\:$delim"){
				if($rank[1]=~s/^[\\|\/]//){$rank[0]=uc($rank[0])."\:$delim";
				}else{
					unless(chdir("$rank[0]\:")){
						_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
					}
					$ppath=_getpwd();chdir($pwd);
					if($ppath=~/^$rank[0]\:[\\|\/](.*)/i){
						$rank[0]=uc($rank[0])."\:$delim";
						if($1 eq ''){$rank[1]=$rank[1];
						}else{$rank[1]="$1$delim$rank[1]";}
					}else{_printmessage(MSG0_PATHNAME_INVALID,$path);return('');}
				}
			}else{_printmessage(MSG0_PATHNAME_INVALID,$path);return('');}
		}elsif($#rank eq 0){
			if($path=~/^([^\:]+)\:/){
				if($rank[0]!~/^\S$/){_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
				}elsif($rank[0]=~s/^$pdrv$/$pdrv\:$delim/i){
					push(@rank,$ppath);
				}elsif(-d "$rank[0]\:$delim"){
					unless(chdir("$rank[0]\:")){
						_printmessage(MSG0_PATHNAME_INVALID,$path);return('');
					}
					$ppath=_getpwd();chdir($pwd);
					if($ppath=~/^$rank[0]\:[\\|\/](.*)/i){
						$rank[0]=uc($rank[0])."\:$delim";
						push(@rank,$1);
					}else{_printmessage(MSG0_PATHNAME_INVALID,$path);return('');}
				}else{_printmessage(MSG0_PATHNAME_INVALID,$path);return('');}
			}elsif($rank[0]=~s/^[\\|\/](.*)/$pdrv\:$delim/){
				push(@rank,$1);
			}else{
				push(@rank,$rank[0]);
				$rank[0]="$pdrv\:$delim";
				if($ppath eq ''){
				}else{$rank[1]="$ppath$delim$rank[1]";}
			}
		}else{
			_printmessage(MSG0_INTERNAL_ERROR,"for PATH '$path'");return('');
		}
	}else{
		unless($pwd=~/^$delim(.*)/){
			_printmessage(MSG0_INTERNAL_ERROR,"for PWD '$pwd'");return('');
		}else{$ppath=$1;}
		if($path=~/^[\\|\/](.*)/){push(@rank,$delim);push(@rank,$1);
		}elsif($ppath eq ''){push(@rank,$delim);push(@rank,$path);
		}else{push(@rank,$delim);push(@rank,"$ppath$delim$path");}
	}

	while($rank[1]=~s/[\\|\/]$//){}
	while($rank[1]=~s/[\\|\/]\.$//){}
	while($rank[1]=~s/[\\|\/]\.[\\|\/]/$delim/){}
	while($rank[1]=~s/^\.[\\|\/]//){}
	$rank[1]=~s/^\.$//;if($rank[1]=~/^$/){return($rank[0]);}
	@prank=split(/\\|\//,$rank[1]);
	pop(@rank);
	while(defined($_=shift(@prank))){
		if($_=~/^\.{2}$/){
			if($#rank>=1){pop(@rank);
			}else{_printmessage(MSG0_PATHNAME_INVALID,$path);return('');}
		}else{push(@rank,$_);}
	}
	$path=shift(@rank).join($delim,@rank);
	return($path);
}
#-----------------------------------------------------------------------------
sub _mkpath{
	my($dirpath,$mode)=(shift,shift);
	unless($mode=_getmode($mode)){return('');}
	unless($dirpath=_checkfilenotexist($dirpath)){return('');}
	unless(-e $dirpath){
		_printmessage(MSGI_MKDIR_START,$dirpath);
		unless(mkpath($dirpath,1,0711)){
			_printmessage(MSG0_MKDIR_FAIL,$dirpath);return('');
		}
		unless(chmod(oct($mode),$dirpath)){
			_printmessage(MSG0_CHMOD_FAIL,$dirpath);return('');
		}
		_printmessage(MSGI_MKDIR_DONE,$dirpath);
	}else{
		unless(chmod(oct($mode),$dirpath)){
			_printmessage(MSG0_CHMOD_FAIL,$dirpath);return('');
		}
	}return($dirpath);
}
#-----------------------------------------------------------------------------
sub _dircopy{
	my($fdir,$tdir,$tomode,$sfx)=(shift,shift,shift,shift);
	unless($tomode=_getmode($tomode)){return(0);}
	unless($fdir=_checkdirexist($fdir)){return(0);}
	unless($tdir=_checkfilenotexist($tdir)){return(0);}
	my($fromobj,$toobj);
	my $delim=_getvariable(KEY_DIRDELIM);
	opendir(DIR, $fdir);my @dirs=readdir(DIR);closedir(DIR);
	foreach my $filename(sort(@dirs)){
		if($filename=~/^[\.]+$/){next;}
		$fromobj="$fdir$delim$filename";
		if($fromobj=~/[\\|\/]?CVS[\\|\/]?/i){next;}
		$toobj="$tdir$delim$filename";
		if(-d $fromobj){
			unless(_mkpath($toobj,$tomode)){return(0);}
			unless(_dircopy($fromobj,$toobj,$tomode,$sfx)){return(0)};
		}else{
			unless(_fcopy($fdir,$filename,$tdir,$filename,$tomode,$sfx)){
				return(0);
			}
		}
	}return(1);
}
#-----------------------------------------------------------------------------
sub _fcopy{
	my($fdir,$ffile,$tdir,$tfile,$tomode,$sfx)=(shift,shift,shift,shift,shift,shift);
	if($tfile=~/^$/) {$tfile=$ffile;}
	if($sfx=~/^$/){$sfx='bak.'._cnvdatetime(0);}
	unless($tomode=_getmode($tomode)){return(0);}
	unless($fdir=_checkdirexist($fdir)){return(0);}
	unless($tdir=_checkfilenotexist($tdir)){return(0);}

	my $delim=_getvariable(KEY_DIRDELIM);

	my $fromfile="$fdir$delim$ffile";
	unless($fromfile=_checkfileexist($fromfile)){return(0);}
	my($fromtime,$fromsize,$fmode)=_getfileinfo($fromfile);
	
	my $tofile="$tdir$delim$tfile";
	unless($tofile=_checkdirnotexist($tofile)){return(0);}
	unless(_mkpath($tdir,$tomode)){return(0);}
	my($totime,$tosize,$tmode)=();

	_printmessage(MSGI_COPY_START,$fromfile,$tofile);
	if(-e $tofile){
		($totime,$tosize,$tmode)=_getfileinfo($tofile);
		if($ffile eq $tfile){
			if(($fromtime eq $totime) and ($fromsize eq $tosize)){
				return(_printmessage(MSGW_COPY_SAMEFILE_SKIP,$fromfile,$tofile));
			}
		}
		if(-e "$tofile\.$sfx"){$sfx=$sfx.'.'._cnvdatetime(0);}
		unless(-w "$tofile"){
			unless(chmod(oct(DEFAULT_PERMISSION), $tofile)){
				return(_printmessage(MSG0_CHMOD_FAIL,$tofile));
			}
		}
		unless(rename($tofile,"$tofile\.$sfx")){
			return(_printmessage(MSG0_FILE_OLD_RENAME_FAIL,$tofile,"$tofile\.$sfx"));
		}
		unless(chmod(oct($tmode),"$tofile\.$sfx")){
			return(_printmessage(MSG0_CHMOD_FAIL,"$tofile\.$sfx"));
		}
		_printmessage(MSGI_FILE_OLD_RENAMED,$tofile,"$tofile\.$sfx");
		unless(copy($fromfile,$tofile)){
			return(_printmessage(MSG0_FILE_COPY_FAIL,$fromfile,$tofile));
		}
	}else{
		unless(copy($fromfile, $tofile)){
			return(_printmessage(MSG0_FILE_COPY_FAIL,$fromfile,$tofile));
		}
	}
	_printmessage(MSGI_COPY_DONE,$fromfile,$tofile);
	($totime,$tosize,$tmode)=_getfileinfo($tofile);
	unless($fromtime eq $totime){
		unless(utime($fromtime, $fromtime, $tofile) eq 1){
			_printmessage(MSGW_FILE_UTIME_FAIL,$tofile);
		}
	}
	unless(oct($tmode) eq oct($tomode)){
		unless(chmod(oct($tomode),$tofile)){
			return(_printmessage(MSG0_CHMOD_FAIL,$tofile));
		}
	}return(1);
}
#-----------------------------------------------------------------------------
sub _dirinput{
	my($msg1,$msg2,$default)=@_;
	my($path,$ret,$buf);
	while(1){
		_printprompt($msg1);
		$path=<STDIN>;chomp $path;if($path=~/^$/){$path=$default;}
		unless($path eq ''){$path=_checkpathname($path);}
		while(1){
		    $buf=$msg2;
			$buf=~s/#STDIN#/$path/g;
			if($path eq ''){
				_printprompt("$buf (Input R[etry] or C[ancel] then [Enter] :");
	   		}else{
	   		    _printprompt("$buf (Input Y[es] or R[etry] or C[ancel] then [Enter] :");
	   		}
			$ret=uc(<STDIN>);chomp $ret;
			if($ret=~/^R(ETRY)?$/){$path='';last;
			}elsif($ret=~/^C(ANCEL)?$/){
				$path='';_printmessage("Operation canceled.");last;
			}
			unless($path eq ''){if($ret=~/^Y(ES)?$/){last;}}
		}
		if($ret=~/^[Y|C]/){last;}
	}
	return($path);
}
#-----------------------------------------------------------------------------
sub _starssrc{
	my($dpath,$path)=(shift);
	my($msg,$ret);
	my $delim=_getvariable(KEY_DIRDELIM);
	while(1){
		if($dpath=~/^$/){
			$path=_getvariable(KEY_STARSSRC);
		}else{$path=_checkpathname($dpath);}
		if($path=~/^$/){
			$msg="Please enter directory name for stars source. :"
		}else{
			$msg="Please enter directory name for stars source. (Enter ->[$path]) :";
		}
		$path=_dirinput($msg,"Stars source directory is [#STDIN#].",$path);
		unless($path eq ''){
			unless(_checkfilenotexist($path)){$path='',next;}
			if(-d "$path".$delim."kernel2".$delim."takaserv-lib"){last;
			}elsif(-d "$path".$delim."kernel".$delim."takaserv-lib"){last;
			}else{
   			    _printprompt("Warning: Stars server has not installed in directory '$path'.\nContinue Ok\? ");
				while(1){
					_printprompt("(Input Y[es] or R[etry] or C[ancel] then [Enter] :");
					$ret=uc(<STDIN>);chomp $ret;
					if($ret=~/^Y(ES)?/){last;
					}elsif($ret=~/^R(ETRY)?/){$path='';last;
					}elsif($ret=~/^C(ANCEL)?/){$path='';last;}
				}
				if($ret=~/^[R]/){next;}
			}
		}last;
	}return($path);
}
#-----------------------------------------------------------------------------
sub _arcdir{
	my($dpath,$path)=(shift);
	my($msg);
	while(1){
		if($dpath=~/^$/){
			$path=_getvariable(KEY_ARCDIR);
		}else{$path=_checkpathname($dpath);}
		if($path=~/^$/){
			$msg="Please enter directory name for stars-archived-files. :"
		}else{
			$msg="Please enter directory name for stars-archived-files. (Enter ->[$path]) :";
		}
		$path=_dirinput($msg,"Stars-archived-files directory is [#STDIN#].",$path);
		unless($path eq ''){unless(_checkfilenotexist($path)){$path='',next;}}
		last;
	}
	return($path);
}
#-----------------------------------------------------------------------------
sub _starsdest{
	my($dpath,$path)=(shift);
	my($msg);
	while(1){
		if($dpath=~/^$/){
			$path=_getvariable(KEY_STARSDEST);
		}else{$path=_checkpathname($dpath);}
		if($path=~/^$/){$path=_getvariable(KEY_STARSDEST);}
		if($path=~/^$/){
			$msg="Please enter directory name for stars. :"
		}else{
			unless($path=_checkpathname($path)){return('');}
			$msg="Please enter directory name for stars. (Enter ->[$path]) :";
		}
		$path=_dirinput($msg,"Stars will be installed into [#STDIN#].", $path);
		unless($path eq ''){unless(_checkfilenotexist($path)){$path='',next;}}
		last;
	}
	return($path);
}
#-----------------------------------------------------------------------------
sub _mkshortcut{
	my($scfile,$cmd,$args,$wdir,$comment,$showcmd,$iconfile,$iconnumber,$hotkey)=@_;

	unless(_ismodule(MOD_WIN32_SHORTCUT)){
		_printmessage("Install perl module 'Win32::Shortcut'");return(0);
	}
	unless($scfile=_checkdirnotexist($scfile)){return(0);}
	###	Shortcut script set	###
	unless($cmd eq ''){$cmd=~s/\//\\/g;}
	unless($args eq ''){$args=~s/\//\\/g;}
	unless($wdir eq ''){$wdir=~s/\//\\/g;}
	$cmd=~s/\s+$//g;
	$wdir=~s/\s+$//g;
	if($cmd=~/\s/){
		if($cmd=~s/^'(.*)'$/"$1"/){}elsif($cmd=~s/^[^"](.*)[^"]$/"$1"/){}
	}elsif($cmd){
		if($cmd=~s/^'(.*)'$/$1/){}elsif($cmd=~s/^"(.*)"$/$1/){}
	}
	if($wdir=~/\s/){
		if($wdir=~s/^'(.*)'$/"$1"/){}elsif($wdir=~s/^[^"](.*)[^"]$/"$1"/){}
	}elsif($wdir){
		if($wdir=~s/^'(.*)'$/$1/){}elsif($wdir=~s/^"(.*)"$/$1/){}
	}

	if($showcmd eq ''){$showcmd=SW_SHOWNORMAL;}
	$iconfile=~s/\//\\/g;
	if($iconfile and $iconnumber eq ''){$iconnumber=0;}
	if($hotkey eq ''){$hotkey=0;}

	my $msg=<<EMKSHORTCUT1;
Creating shortcut '$scfile' with command '$cmd' with args '$args' and working directory '$wdir'.
EMKSHORTCUT1
	_printprompt($msg);
	
	my $sc = new Win32::Shortcut();
	$sc->Set($cmd, 		   			# Perl system address
		$args,				        # Run program file name and path
		$wdir,				        # Run program file directory
		$comment,					# Explanation of shortcut
		$showcmd,					# Run windows status (none)
		hex($hotkey),				# Shortcut key set (Ctr+Shift+7)
		$iconfile,					# Perl icon file
		$iconnumber);				# Perl icon number.

	###	Shortcut saving	###
	if(-e $scfile){
		my $sfx='bak.'._cnvdatetime(0);
		my($totime,$tosize,$tmode)=_getfileinfo($scfile);
		unless(-w $scfile){
			unless(chmod(oct(DEFAULT_PERMISSION), $scfile)){
				return(_printmessage(MSG0_CHMOD_FAIL,$scfile));
			}
		}
		unless(rename($scfile,"$scfile\.$sfx")){
			return(_printmessage(MSG0_FILE_OLD_RENAME_FAIL,$scfile,"$scfile\.$sfx"));
		}
		unless(chmod(oct($tmode),"$scfile\.$sfx")){
			return(_printmessage(MSG0_CHMOD_FAIL,"$scfile\.$sfx"));
		}
	}
	$sc->Save($scfile);
	$sc->Close($scfile);
	my $msg=<<EMKSHORTCUT2;
Shortcut '$scfile' created successfully.
EMKSHORTCUT2
	_printprompt($msg);
    return(1);
}
#-----------------------------------------------------------------------------
sub _edshortcut{
	my($scfile,$cmd,$args,$wdir,$comment,$showcmd,$iconfile,$iconnumber,$hotkey) = @_;
	unless(_ismodule(MOD_WIN32_SHORTCUT)){
		_printmessage("Install perl module 'Win32::Shortcut'");return(0);
	}

	unless($scfile=_checkfileexist($scfile)){return(0);}

	my $sfx='bak.'._cnvdatetime(0);
	my($totime,$tosize,$tmode)=_getfileinfo($scfile);
	unless(copy($scfile,"$scfile\.$sfx")){
		return(_printmessage(MSG0_FILE_COPY_FAIL,$scfile,"$scfile\.$sfx"));
	}
	unless(chmod(oct($tmode),"$scfile\.$sfx")){
		return(_printmessage(MSG0_CHMOD_FAIL,"$scfile\.$sfx"));
	}

	unless(-w $scfile){
		unless(chmod(oct(DEFAULT_PERMISSION), $scfile)){
			return(_printmessage(MSG0_CHMOD_FAIL,$scfile));
		}
	}

	###	Shortcut script set	###
	$cmd=~s/\//\\/g;
	$args=~s/\//\\/g;
	$wdir=~s/\//\\/g;
	$cmd=~s/\s+$//g;
	$wdir=~s/\s+$//g;
	if($cmd=~/\s/){
		if($cmd=~s/^'(.*)'$/"$1"/){}elsif($cmd=~s/^[^"](.*)[^"]$/"$1"/){}
	}elsif($cmd){
		if($cmd=~s/^'(.*)'$/$1/){}elsif($cmd=~s/^"(.*)"$/$1/){}
	}
	if($wdir=~/\s/){
		if($wdir=~s/^'(.*)'$/"$1"/){}elsif($wdir=~s/^[^"](.*)[^"]$/"$1"/){}
	}elsif($wdir){
		if($wdir=~s/^'(.*)'$/$1/){}elsif($wdir=~s/^"(.*)"$/$1/){}
	}

#	if($showcmd eq ''){$showcmd=SW_SHOWNORMAL;}
	$iconfile=~s/\//\\/g;
#	if($iconfile and $iconnumber eq ''){$iconnumber=0;}
#	if($hotkey eq ''){$hotkey=0;}

	my $msg=<<EEDSHORTCUT1;
Updating shortcut '$scfile' with command '$cmd' with args '$args' and working directory '$wdir'
EEDSHORTCUT1
	_printprompt($msg);

	###	Shortcut script set	###
	my $sc = new Win32::Shortcut();
    $sc->Load($scfile);
	unless($cmd eq ''){$cmd=~s/\s+$//;$sc->{'Path'}=$cmd;}
    unless($args eq ''){$args=~s/\s+$//;$sc->{'Arguments'}=$args;}
    unless($wdir eq ''){$wdir=~s/\s+$//;$sc->{'WorkingDirectory'}=$wdir;}
    unless($hotkey eq ''){$sc->{'Hotkey'}=hex($hotkey);}
    unless($showcmd eq ''){$sc->{'ShowCmd'}=$showcmd;}
    if($comment){$comment=~s/\s+$//;$sc->{'Description'}=$comment;}
    if($iconfile){$iconfile=~s/\s+$//;$sc->{'IconLocation'}=$iconfile;}
    unless($iconnumber eq ''){$sc->{'IconNumber'}=$iconnumber;}
	###	Shortcut saving	###
    $sc->Save();
    $sc->Close();
	unless(chmod(oct($tmode),$scfile)){
		return(_printmessage(MSG0_CHMOD_FAIL,$scfile));
	}
	my $msg=<<EEDSHORTCUT2;
Shortcut '$scfile' changed successfully.
EEDSHORTCUT2
	_printprompt($msg);
    return(1);
}
#-----------------------------------------------------------------------------
sub _maskargs{
	$_=shift;
	my($buf,$buf2);
	s/\\"/\$DC\$/g;s/\\'/\$SC\$/g;
	if(/^([^"]*["])/){
		($buf,$buf2)=('','');
		while(s/^([^"]*["])//){
			$buf.=$1;
			if(s/^([^"]*["])//){$buf2=$1;$buf2=~s/\s/\$s\$/g;$buf.=$buf2;
			}else{last;}
		}
		$_="$buf$_";
	}
	if(/^([^']*['])/){
		($buf,$buf2)=('','');
		while(s/^([^']*['])//){
			$buf.=$1;
			if(s/^([^']*['])//){$buf2=$1;$buf2=~s/\s/\$s\$/g;$buf.=$buf2;
			}else{last;}
		}
		$_="$buf$_";
	}
	return($_);
}
#-----------------------------------------------------------------------------
sub _cnvargs{
	my($argsaddr,$argnum)=(shift,shift);
	my $num=$#$argsaddr;
	my $i;
	for($i=0;$i<=$num;$i++){
		my $buf=$$argsaddr[$i];
		$buf=~s/^'([^']*)'$/$1/;
		$buf=~s/^"([^"]*)"$/$1/;
		$buf=~s/\$t\$/\t/g;
		$buf=~s/\$s\$/ /g;
		$buf=~s/\$DC\$/"/g;
		$buf=~s/\$SC\$/'/g;
		$$argsaddr[$i]=$buf;
	}
	if($argnum<$num){
		while($#$argsaddr!=$argnum){
			my $buf=$$argsaddr[$argnum+1];
			$buf=~s/^'([^']*)'$/$1/;
			$buf=~s/^"([^"]*)"$/$1/;
			$buf=~s/\$s\$/ /g;
			$$argsaddr[$argnum].=" $buf";
			splice( @$argsaddr, $argnum+1,1);
		}
	}else{
		for(;$i<=$argnum;$i++){push(@$argsaddr,"");}
	}
	return($argnum);
}
################################################
# _askmoduleoverwrite: comfirm overwrite module.
################################################
sub _askmoduleoverwrite{
	my($module,$toppath,$zipdate,$sfx)=(shift,shift,shift,shift);
	my($dest)=($module);
	my $delim=_getvariable(KEY_DIRDELIM);
	my $msg;
	if($::MyInteractive=~/^U$/i){
		if(!-e "$toppath$delim$module"){return('Y',"$module");
		}elsif(!-e "$toppath$delim$module\_$zipdate"){
			return('Y',"$module\_$zipdate");
		}else{return('Y',"$module\_$zipdate\.$sfx");}
	}elsif($::MyInteractive eq 'A'){
		unless(checkfilenotexist("$toppath$delim$module")){return('Y',"$module");}
	}
	while(1){
		$_=_getftype("$toppath$delim$module");
		if(/^d/i){
			$msg=<<EASKOWMSG_1;
Directory '$toppath$delim$dest' already exists.
  Enter:
    U(nique)  -> Install all packages with unique name directory, if same package exists.
    A(ll)     -> Overwite all packages, if same package exists.
    Y(es)     -> Overwite only this package. Directory '$toppath$delim$dest' will be overwritten.
    R(ename)  -> Rename directory for this package '$module' manually.
    S(kip)    -> Skip installing this package '$module'.
    C(ancel)  -> Cancel operation.
(Enter ->[U|A|Y|R|S|C]) ->
EASKOWMSG_1
			$msg=~s/[\n|\r]+$//;
			_printprompt($msg);
			$_=uc<STDIN>;chomp $_;
			unless(/^(U|UNIQUE|YES|Y|ALL|A|RENAME|R|SKIP|S|CANCEL|C)$/){next;}
		}elsif(/^f/i){
			$msg=<<EASKOWMSG_2;
'$toppath$delim$dest' already exists as file or link.
  Enter:
    U(nique)  -> Install all packages with unique name directory, if same package exists.
    R(ename)  -> Rename this package '$module' directory manually.
    S(kip)    -> Skip installing this package '$module'.
    C(ancel)  -> Cancel operation.
(Enter ->[U|R|S|C]) ->
EASKOWMSG_2
			$msg=~s/[\n|\r]+$//;
			_printprompt($msg);
			$_=uc<STDIN>;chomp $_;
			unless(/^(U|UNIQUE|RENAME|R|SKIP|S|CANCEL|C)$/){next;}
		}else{return('Y',"$dest");}

		if(/^Y(ES)?$/){return('Y',"$module");
		}elsif(/S(KIP)?$/){return('S','');
		}elsif(/C(ANCEL)?$/){return('C','');
		}elsif(/^A(LL)?$/){$::MyInteractive='A';return('Y',"$module");
		}elsif(/^U(NIQUE)?$/){
			$::MyInteractive='U';
			if(!-e "$toppath$delim$module"){return('Y',"$module");
			}elsif(!-e "$toppath$delim$module\_$zipdate"){
				return('Y',"$module\_$zipdate");
			}else{return('Y',"$module\_$zipdate\.$sfx");}
		}elsif(/R(ENAME)?$/){
			while(1){
				$msg=<<EASKOWMSG_R;
Input directory name below '$toppath' for package '$module'. ->
EASKOWMSG_R
				$msg=~s/[\n|\r]+$//;
				_printprompt($msg);
				$_=<STDIN>;chomp $_;$dest=$_;
				if(_checkfilenotexist("$toppath$delim$dest")){return('Y',$dest);}
				last;
			}
		}
	}
}
#######################################
# _unzipmodulearc: unzip stars module.
######################################
sub _unzipmodulearc{
	my($zipfile,$dest,$zipdate,$sfx,$tomode)=(shift,shift,shift,shift,shift);
	unless(_ismodule(MOD_ARCHIVE_ZIP)){
		_printmessage("Unzip manually or install perl module 'Archive::Zip'");return(0);
	}
	unless($tomode=_getmode($tomode)){return(0);}
	unless($zipfile=_checkfileexist($zipfile)){return(0);}
	unless($dest=_checkfilenotexist($dest)){return(0);}
	my $zip=Archive::Zip->new();
	unless($zip->read($zipfile) == Archive::Zip::AZ_OK){
		return(_printmessage(MSG0_ZIPFILE_INVALID,$zipfile));
	}
	my $msg=<<EZIPMSG1;	
==================================================
Extracting stars-archived zip file '$zipfile'.
==================================================
EZIPMSG1
	_printprompt($msg);
	my $tmpdir=_mktempdir();
	my $delim=_getvariable(KEY_DIRDELIM);
	my($module,$extractTop);
	my @members = $zip->members();
	foreach my $mptr (@members) {
		my $fullname = $mptr->fileName();
		if($fullname=~/^([^\\|\/]+)[\\|\/]?/){
			_printmessage("$fullname");
			if($module eq ''){
				$module=$1;
			}elsif($module ne $1){
				return(_printmessage(MSG0_ZIPFILE_INVALID,$zipfile));
			}
			$zip->extractMember($fullname,"$tmpdir$delim$fullname");
		}
	}
	unless(-d "$tmpdir$delim$module"){
		return(_printmessage(MSG0_ZIPFILE_INVALID,$zipfile));
	}
	my $msg=<<EZIPMSG2;	
Extracted to temporary directory $tmpdir.
==================================================
Install '$module' version '$zipdate'.
==================================================
EZIPMSG2
	_printprompt($msg);
	my($ans,$subdir)=_askmoduleoverwrite($module,$dest,$zipdate,$sfx);
	if($ans=~/^Y$/i){
		$extractTop="$dest$delim$subdir";
	}elsif($ans=~/^S$/i){
		_printmessage("Skipped extracting zip file '$zipfile'.");return(1);
	}else{
		_printmessage("Operation canceled.");return(0);
	}
	unless(_mkpath($extractTop,$tomode)){return(0);}
	unless(_dircopy("$tmpdir$delim$module",$extractTop,$tomode,$sfx)){return(0);}
	_printmessage("Successfully installed '$module' version '$zipdate' into '$extractTop'.");
	rmtree($tmpdir);
	return(1);
}
#######################################
# _untgzmodulearc: untgz stars module.
################################$######
sub _untgzmodulearc{
	my($tgzfile,$dest,$zipdate,$sfx,$tomode)=(shift,shift,shift,shift,shift);
	my $cmd;
	unless($cmd=_gettgzcommand('')){return(0);}
	unless($tomode=_getmode($tomode)){return(0);}
	unless($tgzfile=_checkfileexist($tgzfile)){return(0);}
	unless($dest=_checkfilenotexist($dest)){return(0);}
	my $delim=_getvariable(KEY_DIRDELIM);
	my $msg=<<ETGZMSG1;
==================================================
Extracting stars-archived tgz file '$tgzfile'.
==================================================
ETGZMSG1
	_printprompt($msg);
	my($rt,$module,$extractTop);
	unless($cmd=_gettgzcommand($cmd,$tgzfile)){return(0);}
	my $savedir=_getpwd();
	my $tmpdir=_mktempdir();
	chdir($tmpdir);
	($_,$rt)=_execcommand($cmd);
	chdir($savedir);
	unless($_){return(0);}
	$rt=~s/\r//g;
	$rt=~/^([^\n]+)/;$module=$1;
	if($module=~/^\s*$/){
		return(_printmessage(MSG0_TGZFILE_INVALID,$tgzfile));
	}
	my $msg=<<ETGZMSG2;	
Extracted to temporary directory $tmpdir.
=======================================
Install '$module' version '$zipdate'.
=======================================
ETGZMSG2
	_printprompt($msg);
	my($ans,$subdir)=_askmoduleoverwrite($module,$dest,$zipdate,$sfx);
	if($ans=~/^Y$/i){
		$extractTop="$dest$delim$subdir";
	}elsif($ans=~/^S$/i){
		_printmessage("Skipped extracting tgz file '$tgzfile'.");return(1);
	}else{
		_printmessage("Operation canceled.");return(0);
	}
	unless(_mkpath($extractTop,$tomode)){return(0);}
	unless(_dircopy("$tmpdir$delim$module",$extractTop,$tomode,$sfx)){return(0);}
	_printmessage("Successfully installed '$module' version '$zipdate' into '$extractTop'.");
	rmtree($tmpdir);
	return(1);
}
##############################################
# _downloadmodulearc: Download stars modules.
##############################################
sub _downloadmodulearc{
	my($arcurl,$arcdest)=(shift,shift);
	my $host=STARS_DOWNLOAD_SITE;
	my $port=STARS_DOWNLOAD_PORT;
	unless($arcdest=_checkfilenotexist($arcdest)){return(0);}
	unless($arcurl=~/([^\\|\/]+\_\d+\.(zip|tgz))$/i){
		return(_printmessage(MSG0_INTERNAL_ERROR
		,"ARCURL: This is not stars-archived file 'http://$host$arcurl'."));
	}
	my $arcfile=$1;
	my $ipaddress = inet_aton("$host") || die "host($host) not found.\n";
	my $sock_addr = pack_sockaddr_in($port,$ipaddress);
	socket(SOCKET,PF_INET,SOCK_STREAM,0) || die "socket error.\n";
	connect(SOCKET,$sock_addr) || die "connect $host $port error.\n";
	select(SOCKET);$|=1;select(STDOUT);
	
	print SOCKET "GET $arcurl HTTP/1.1\r\n";
	print SOCKET "HOST: $host\r\n";
	print SOCKET "\r\n";
	
	my $delim=_getvariable(KEY_DIRDELIM);
	my $arcpath="$arcdest$delim$arcfile";
	_printmessage(MSGI_WEBDLD_START,$arcfile, $arcpath);
	unless(open(FILE,">$arcpath")){
		return(_printmessage(MSG0_FILE_OPEN_FAIL,$arcpath));
	}
	select(FILE);$|=1;binmode(FILE);select(STDOUT);
	my $content='';
	while(<SOCKET>){
		$content=$content.$_;
		if($content=~/application\/zip\r\n\r\n/){last;
		}elsif($content=~/application\/x\-gzip\r\n\r\n/){last;}
	}
	while(<SOCKET>){print FILE "$_";}
	close(FILE);
	close(SOCKET);
	my($fdate,$fsize,$fmode)=_getfileinfo($arcpath);
	if($fsize<=0){return(_printmessage(MSG0_WEBDLD_FAIL,$arcfile, $arcpath));}
	_printmessage(MSGI_WEBDLD_END,$arcfile, $arcpath);
	return(1);
}
#######################################################
# mygetstarsarclist: Read a stars module info from web.
#######################################################
sub mygetstarsarclist{
	my($type)=(shift);
	my($listtopurl,$listname,$host,$port);
	if($type eq CONST_ZIP){$listname=STARS_DOWNLOAD_ZIPPAGE;
	}elsif($type eq CONST_TGZ){$listname=STARS_DOWNLOAD_TGZPAGE;
	}else{return(_printmessagae(MSG0_ARCTYPE_INVALID,$type));}
	unless($listtopurl){$listtopurl=STARS_DOWNLOAD_TOPURL;}
	unless($host){$host=STARS_DOWNLOAD_SITE;}
	unless($port){$port=STARS_DOWNLOAD_PORT;}

	%::Mymoddesc=();
	%::Myzippath=();
	%::Myzipname=();
	%::Myzipsize=();

	my $ipaddress = inet_aton("$host") || die "host($host) not found.\n";
	my $sock_addr = pack_sockaddr_in($port,$ipaddress);
	socket(SOCKET,PF_INET,SOCK_STREAM,0) || die "socket error.\n";
	connect(SOCKET,$sock_addr) || die "connect $host $port error.\n";
	select(SOCKET);$|=1;select(STDOUT);
	
	print SOCKET "GET $listtopurl$listname HTTP/1.1\r\n";
	print SOCKET "HOST: $host\r\n";
	print SOCKET "\r\n";
	
	my($buf,$flag)=('','');
	my($modname,$moddesc,$zippath,$zipname,$zipsize)=('','','','','');
	
	while(<SOCKET>){
		s/[\r|\n]//g;
		if(/\<\/body\>/){
			last;
		}
		$buf="$buf$_";
		if($flag eq ''){
			if($buf=~/\<li\>(.*)/){
				$buf=$1;
				$flag = 'modname';
			}
		}
		if($flag eq 'modname'){
			if($buf=~s/\<br\>(.*)//){
				$modname=$buf;
				$buf=$1;
				$modname=~s/\<[^\>]+\>//g;
				$flag = 'moddesc';
			}
		}
		if($flag eq 'moddesc'){
			if($buf=~s/\<a\s+href\=\s*\"([^\"]+)\"\s*\>(.*)//){
				$moddesc=$buf;
				$zippath="$listtopurl$1";
				$buf=$2;
				$moddesc=~s/\<br\>//g;
				$flag = 'zipname';
			}
		}
		if($flag eq 'zipname'){
			if($buf=~s/\<\/a\>(.*)//){
				$zipname=$buf;
				$buf=$1;
				$flag = "zipsize";
			}
		}
		if($flag eq 'zipsize'){
			if($buf=~s/\<\/li\>(.*)//){
				$zipsize=$buf;
				$buf=$1;
				$zipsize=~s/\<[^\>]+\>//g;
				$zipsize=~s/[\(|\)|\s]//g;
				$zipsize=~s/Bytes//;
				$zipsize=~s/\,//g;
				$flag='';
				$zipname=~/\_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
				$::Mymoddesc{$modname}=$moddesc;
				$::Myzippath{$modname}=$zippath;
				$::Myzipname{$modname}=$zipname;
				$::Myzipsize{$modname}=$zipsize;
			}
		}
	}
	close(SOCKET);
	return(1);
}
#####################################################
# mystarscopy: Copy stars module to other directory.
#####################################################
sub mystarscopy{
	my($src,$dest,$module,$tomode)=(shift,shift,shift,shift);
	unless($tomode=_getmode($tomode)){return(0);}
	if($src eq ''){$src=_starssrc($src);if($src eq ''){return(0);}}
	unless($src=_checkdirexist($src)){return(0);}

	unless($dest eq ''){unless($dest=_checkfilenotexist($dest)){return(0);}
	}else{$dest=_starsdest($dest);if($dest eq ''){return(0);}}
	my $delim=_getvariable(KEY_DIRDELIM);
	my($src2,$dest2)=($src,$dest);
	unless($module eq ''){
		unless($src2=_checkdirexist("$src$delim$module")){return(0);}
		unless($dest2=_checkfilenotexist("$dest$delim$module")){return(0);}
	}
	my $msg=<<EMYSTARSCPMSG1;
============================================
Starting copy of stars system.
============================================
EMYSTARSCPMSG1
	_printprompt($msg);
	my $sfx=_cnvdatetime(0);
	unless(_mkpath($dest2,$tomode)){return(0);}
	unless(_dircopy($src2,$dest2,$tomode,$sfx)){return(0);}
	$msg=<<EMYSTARSCPMSG2;
================================================
Stars system copied successfully.
================================================
EMYSTARSCPMSG2
	_printprompt($msg);
	_setvariable(KEY_STARSSRC,$src);
	_setvariable(KEY_STARSDEST,$dest);
	return(1);
}
#############################################################
# myextractarc: Control extracting stars-archived tgz files.
#############################################################
sub myextractarc{
	my($type,$arcdir,$dest,$modname,$ver,$tomode)=(lc(shift),shift,shift,shift,shift,shift);
	unless($tomode=_getmode($tomode)){return(0);}
	if($type){
		if($type eq CONST_ZIP){
			unless(_ismodule(MOD_ARCHIVE_ZIP)){
				_printmessage("Unzip manually or install perl module 'Archive::Zip'");return(0);
			}
		}
		if($type ne _getvariable(KEY_ARCTYPE)){
			unless(_setvariable(KEY_ARCTYPE,$type)){return(0);}
		}
	}else{
		$type=_getvariable(KEY_ARCTYPE);
		if($type eq CONST_ZIP){
			unless(_ismodule(MOD_ARCHIVE_ZIP)){
				_printmessage("Unzip manually or install perl module 'Archive::Zip'");return(0);
			}
		}
	}
	if($modname){
		unless(defined($::Mymoddesc{$modname})){
			return(_printmessage(MSG0_MOD_NOTFOUND,$modname));
		}
	}
	if($arcdir eq ''){$arcdir=_arcdir($arcdir);if($arcdir eq ''){return(0);}}
	unless($arcdir=_checkdirexist($arcdir)){return(0);}
	unless($dest eq ''){unless($dest=_checkfilenotexist($dest)){return(0);}
	}else{$dest=_starsdest($dest);if($dest eq ''){return(0);}}
	
	my $msg=<<EMYUNARCMSG1;
==============================================
Starting extracting stars-archived $type files.
==============================================
EMYUNARCMSG1
	_printprompt($msg);
	my $sfx=_cnvdatetime(0);
	my $delim=_getvariable(KEY_DIRDELIM);
	unless(_mkpath($dest,$tomode)){return(0);}
	my($fromobj,$cnt)=('',0);
	my($modnamebuf,$prevmodname,$zipdate)=('','','');
	opendir(DIR, $arcdir);my @dirs=readdir(DIR);closedir(DIR);
	foreach my $filename(reverse(sort(@dirs))){
		if($filename=~/^[\.]+$/){next;}
		$fromobj="$arcdir$delim$filename";
		if($filename=~/([^\\|\/]+)\_(\d{4}\d{2}\d{2}\d{2}\d{2}\d{2})\.$type$/i){
			($modnamebuf,$zipdate)=($1,$2);
			if($modname and ($modnamebuf eq $modname)){
				if($ver and ($ver ne $zipdate)){next;}
				if($type eq CONST_ZIP){
					unless(_unzipmodulearc($fromobj,$dest,$zipdate,$sfx,$tomode)){return(0);}
				}else{
					unless(_untgzmodulearc($fromobj,$dest,$zipdate,$sfx,$tomode)){return(0);}
				}
				$cnt=$cnt+1;last;
			}elsif(!$modname){
				if($ver and ($ver ne $zipdate)){next;
				}elsif(!$ver and ($modnamebuf eq $prevmodname)){
					_printmessage(MSGW_EXTRACT_SAMEMOD_SKIP,$fromobj,$dest);next;
				}
				if($type eq CONST_ZIP){
					unless(_unzipmodulearc($fromobj,$dest,$zipdate,$sfx,$tomode)){return(0);}
				}else{
					unless(_untgzmodulearc($fromobj,$dest,$zipdate,$sfx,$tomode)){return(0);}
				}
				$prevmodname=$modnamebuf;
				$cnt=$cnt+1;
			}
		}
	}
	if($modname eq ''){$modname='<all>';}
	if($ver eq ''){$ver='<newest version>';}
	my $msg=<<EMYUNARCMSG2;
===================================================================
Extracted $cnt modules where modname='$modname' and version='$ver'
Stars-archived $type files successfully extracted.
===================================================================
EMYUNARCMSG2
	_printprompt($msg);
	_setvariable(KEY_ARCDIR,$arcdir);
	_setvariable(KEY_STARSDEST,$dest);
	return(1);
}
####################################################
# mydownloadarc: Control downloading stars modules.
####################################################
sub mydownloadarc{
	my($type,$dest,$modname,$tomode)=(lc(shift),shift,shift,shift);
	unless($tomode=_getmode($tomode)){return(0);}
	if($type){
		if($type ne _getvariable(KEY_ARCTYPE)){
			unless(_setvariable(KEY_ARCTYPE,$type)){return(0);}
		}
	}else{$type=_getvariable(KEY_ARCTYPE);}
	if($modname){
		unless(defined($::Mymoddesc{$modname})){
			return(_printmessage(MSG0_MOD_NOTFOUND,$modname));
		}
	}
	unless($dest eq ''){
		unless($dest=_checkfilenotexist($dest)){return(0);}
	}else{
		$dest=_arcdir($dest);if($dest eq ''){return(0);}
	}
	my $msg=<<EMDLDARCMSG1;
============================================
Starting download of stars-archived file.
============================================
EMDLDARCMSG1
	_printprompt($msg);
	unless(_mkpath($dest,$tomode)){return(0);}
	if($modname eq ''){
		foreach $modname (sort(keys(%::Mymoddesc))){
			$msg=<<EMDLDARCMSG2;
============================================
Download stars-archived file of '$modname'.
============================================
EMDLDARCMSG2
			_printprompt($msg);
			unless(_downloadmodulearc($::Myzippath{$modname},$dest)){return(0);}
		}
	}else{
		$msg=<<EMDLDARCMSG3;
============================================
Download stars-archived file of '$modname'.
============================================
EMDLDARCMSG3
		_printprompt($msg);
		unless(_downloadmodulearc($::Myzippath{$modname},$dest)){return(0);}
	}
	$msg=<<EMDLDARCMSG4;
================================================
Stars-archived file downloaded successfully.
================================================
EMDLDARCMSG4
	_printprompt($msg);
	_setvariable(KEY_ARCDIR,$dest);
	return(1);
}
#################################################
# subinstall: Sub process of function myinstall.
#################################################
sub submyinstall{
	my($type,$dest,$modname,$sfx,$tmpdir,$tomode)=(shift,shift,shift,shift,shift,shift);
	$::Myzipname{$modname}=~/\_(\d{4}\d{2}\d{2}\d{2}\d{2}\d{2})/;
	my $zipdate=$1;
	my $msg=<<EINSTMSG1;
============================================
Download stars-archived file of '$modname'.
============================================
EINSTMSG1
	_printprompt($msg);
	unless(_downloadmodulearc($::Myzippath{$modname},"$tmpdir")){return(0);}
	my $dirdelim=_getvariable(KEY_DIRDELIM);
	my $rt;
	if($type eq CONST_ZIP){
		$rt=_unzipmodulearc("$tmpdir$dirdelim$::Myzipname{$modname}",$dest,$zipdate,$sfx,$tomode);
	}else{
		$rt=_untgzmodulearc("$tmpdir$dirdelim$::Myzipname{$modname}",$dest,$zipdate,$sfx,$tomode);
	}
	if($rt){unlink("$tmpdir$dirdelim$::Myzipname{$modname}");}
	return($rt);
}
#########################################################
# myinstall: Control download and install stars modules.
#########################################################
sub myinstall{
	my($type,$dest,$modname,$tomode)=(lc(shift),shift,shift,shift);
	unless($tomode=_getmode($tomode)){return(0);}
	if($type){
		if($type ne _getvariable(KEY_ARCTYPE)){
			unless(_setvariable(KEY_ARCTYPE,$type)){return(0);}
		}
	}else{$type=_getvariable(KEY_ARCTYPE);}
	if($modname){
		unless(defined($::Mymoddesc{$modname})){
			return(_printmessage(MSG0_MOD_NOTFOUND,$modname));
		}
	}
	unless($dest eq ''){
		unless($dest=_checkfilenotexist($dest)){return(0);}
	}else{
		$dest=_starsdest($dest);if($dest eq ''){return(0);}
	}
	my $msg=<<EMYINSTMSG1;
============================================
Starting stars installation.
============================================
EMYINSTMSG1
	_printprompt($msg);
	my $sfx=_cnvdatetime(0);
	my $tmpdir=_mktempdir();
	unless(_mkpath($dest,$tomode)){return(0);}
	if($modname eq ''){
		foreach $modname (sort(keys(%::Mymoddesc))){
			unless(submyinstall($type,$dest,$modname,$sfx,$tmpdir,$tomode)){return(0);}
		}
	}else{
		unless(submyinstall($type,$dest,$modname,$sfx,$tmpdir,$tomode)){return(0);}
	}
	$msg=<<EMYINSTMSG2;
============================================
Stars installation done successfully.
============================================
EMYINSTMSG2
	_printprompt($msg);
	_setvariable(KEY_STARSDEST,$dest);
	rmtree($tmpdir);
	return(1);
}
##############################################
# subrunscript: called by myrunscript.
##############################################
sub subrunscript{
	my($cmds,$keyaddr)=(shift,shift);
	my $pwd=_getpwd();
	my %KEYWORD=%$keyaddr;
	my %MYSAVVALUE=%::MYVALUE;
	my $rt=1;
	my($cmd,@args);

	foreach $_(split("\n",$cmds)){
		s/^\s+//;s/\s+$//;
		if(/^$/){next;}elsif(/^#/){next;}
		foreach my $mykey (keys(%KEYWORD)){s/\$$mykey\$/$KEYWORD{$mykey}/g;}
		foreach my $mykey (keys(%MYVALUE)){s/\$$mykey\$/$MYVALUE{$mykey}/g;}
		$_=_maskargs($_);
		if(/^(\S+)\s+(.+)$/){$cmd=$1;@args=split(/\s+/,$2);
		}else{$cmd=$_;@args=();}
		_printmessage("-"x60);
		_printmessage("Command='$cmd' Args='@args'");
		_printmessage("-"x60);
		unless($rt=submessageexec($cmd,@args)){last;}
	}
	%::MYVALUE=%MYSAVVALUE;
	chdir($pwd);
	return($rt);
}
##############################################
# myrunscript: run stars install script.
##############################################
sub myrunscript{
	my($scrname)=(shift);
	unless($scrname=_checkfileexist($scrname)){return(0);}
	unless(open(BUFIN,"$scrname")){
		return(_printmessage(MSG0_FILE_OPEN_FAIL,$scrname));
	}
my $msg=<<ERUNSCR2;
=====================================================
Starting to execute script file '$scrname'.
=====================================================
ERUNSCR2
	_printprompt($msg);
	my @bufs=<BUFIN>;close(BUFIN);

	my %VAR=();
	my %KEYWORD=();
	my $buf='';
	foreach $_(@bufs){
		chomp;
		if(/^\s*$/){next;
		}elsif(/^#/){next;
		}elsif(/^\!BEGIN\s+(\w+)\s*/i){
			$buf=$1;
		}elsif($buf){
			if(/^\!END(\s|$)/i){
				$VAR{$buf}=~s/\r//mg;
				unless(subrunscript($VAR{$buf},\%KEYWORD)){return(0);}
				$buf='';
			}else{$VAR{$buf}.="$_\n";}
		}elsif(/^\s*(\w+)\s+(.*)/){
			$KEYWORD{$1}=$2;$KEYWORD{$1}=~s/\r//mg;
			_printmessage("Keyword '$1' is replaced to '$2'.");
		}else{
			_printmessage("Error: Syntax invalid '$_'.");
			return(0);
		}
	}
my $msg=<<ERUNSCR2;
=====================================================
Executing script file '$scrname' done successfully.
=====================================================
ERUNSCR2
	_printprompt($msg);
	return(1);
}
#################################################
# submessageexec: command caller 
#################################################
sub submessageexec{
	my($cmd,@args)=(shift,@_);
	my $rt=0;
	my($type,$param);
	my($key,$val);
### VARIABLE FUNCTION ####
	if($cmd=~/^set$/i){
		_cnvargs(\@args,0);
		$args[0]=~s/\s+(=)\s+/$1/;
		if($args[0]=~/^([^=|\s]+)(=|\s)([^=|\s]*)()/){
			($key,$val)=($1,$3);
			unless($key=~/^user/){
				_printmessage("Error: Unabled to set '$val' to system parameter '$key'.");
			}else{$rt=_setvariable($key,$val);}
		}else{$rt=_showvariable($args[0]);}
	}elsif($cmd=~/^set(arcdir|starsdest|starssrc)$/i){
		_cnvargs(\@args,0);
		eval '$rt='."_setvariable(KEY_".uc($1).',$args[0]);';
		if($@){_printmessage("Error: Unabled to set '$args[0]' to '$1'.");}
	}elsif($cmd=~/^input(arcdir|starsdest|starssrc)$/i){
		_cnvargs(\@args,0);
		eval '$rt=_'.lc($1)."(\$args[0]);";
		if($@){_printmessage("Error: Unabled to input '$1'.");
		}elsif($rt){
			eval '$rt='."_setvariable(KEY_".uc($1).',$rt);';
			if($@){_printmessage("Error: Unabled to set '$args[0]' to '$1'.");}
		}
### SHORTCUT FUNCTION ####
	}elsif($cmd=~/^mkshortcut$/i){
		_cnvargs(\@args,7);
		$rt=_mkshortcut($args[0],$args[1],$args[2],$args[3],$args[4],$args[5],$args[6],$args[7]);
	}elsif($cmd =~ /^edshortcut$/i){
		_cnvargs(\@args,7);
		$rt=_edshortcut($args[0],$args[1],$args[2],$args[3],$args[4],$args[5],$args[6],$args[7]);
### DIRECTORY & FILE FUNCTION ####
	}elsif($cmd=~/^(mkdir|makedir|mkpath)$/i){
		_cnvargs(\@args,1);$rt=_mkpath($args[0],$args[1]);
	}elsif($cmd=~ /^(cd|chdir)$/i){
		_cnvargs(\@args,0);
		if($args[0] eq ''){
			unless($rt=chdir(_getvariable(KEY_PWD))){
				_printmessage("Error: Unabled to change directory to '"._getvariable(KEY_PWD)."'.");
			}
		}elsif($args[0]=_checkpathname($args[0])){
			unless($rt=chdir($args[0])){
				_printmessage("Error: Unabled to change directory to '".$args[0]."'.");
			}
		}
		_printmessage("Current Directory is "._getpwd());
	}elsif($cmd=~/^pwd$/i){
		_printmessage("Current Directory is "._getpwd());$rt=1;
	}elsif($cmd=~/^dircopy$/i){
		_cnvargs(\@args,3);$rt=_dircopy($args[0],$args[1],$args[2],$args[3]);
	}elsif($cmd=~/^(fcopy|filecopy)$/i){
		_cnvargs(\@args,5);$rt=_fcopy($args[0],$args[1],$args[2],$args[3],$args[4],$args[5]);
### STARS INSTALLATION FUNCTION ####
	}elsif($cmd=~/^install(zip|tgz)?$/i){
		$type=$1;
		_cnvargs(\@args,2);$rt=myinstall($type,$args[0],$args[1],$args[2]);
	}elsif($cmd=~/^download(zip|tgz)?$/i){
		$type=$1;
		_cnvargs(\@args,2);$rt=mydownloadarc($type,$args[0],$args[1],$args[2]);
	}elsif($cmd=~/^extract(zip|tgz)?$/i){
		$type=$1;
		_cnvargs(\@args,4);$rt=myextractarc($type,$args[0],$args[1],$args[2],$args[3],$args[4]);
	}elsif($cmd=~/^starscopy$/i){
		_cnvargs(\@args,3);$rt=mystarscopy($args[0],$args[1],$args[2],$args[3]);
	}elsif($cmd=~/^runscript$/i){
		_cnvargs(\@args,0);$rt=myrunscript($args[0]);
### CONFIG FUNCTION ####
	}elsif($cmd=~/^saveconfig$/i){
		_cnvargs(\@args,0);if($args[0]=~/^\s*$/){$args[0]=$::MYCONFIGFILE;}
		if($args[0]=_getconfigfilename($args[0])){
			$rt=myconfig($args[0],1);
			if($rt){_printmessage("Config file '$args[0]' has refleshed now !!!");}
		}
	}elsif($cmd=~/^readconfig$/i){
		_cnvargs(\@args,0);if($args[0]=~/^\s*$/){$args[0]=$::MYCONFIGFILE;}
		if($args[0]=_getconfigfilename($args[0])){
			unless(-e $args[0]){_printmessage(MSG0_FILE_NOTFOUND,$args[0]);
			}else{$rt=myconfig($args[0],0);}
		}
### SHELL FUNCTION ####
	}elsif($cmd=~/^runshell$/i){
		_cnvargs(\@args,0);$rt=_execcommand($args[0]);
### UTILITY FUNCTION ####
	}elsif($cmd=~/^list$/i){
		my $ver='';
		foreach (sort(keys(%::Mymoddesc))){
			$::Myzipname{$_}=~/\_(\d{4}\d{2}\d{2}\d{2}\d{2}\d{2})/;
			unless($ver){
				$ver=$1;
				_printmessage("-"x78);
				_printmessage("Show "._getvariable(KEY_ARCTYPE)." files version '$ver'.");
				_printmessage(sprintf("%-30s %s\n    %s","module_name","file_name","description"));
			}
			_printmessage("-"x78);
			_printmessage(sprintf("%-30s %s\n    %s",$_,$::Myzipname{$_},$::Mymoddesc{$_}));
		}
		_printmessage("-"x78);$rt=1;
### SHELL FUNCTION ####
	}elsif($cmd=~/^mkscripttemplate$/i){
		_cnvargs(\@args,0);$rt=_mktemplatescript($args[0]);
	}elsif($cmd=~/^help$/i){
		_cnvargs(\@args,0);$rt=subhelp($args[0]);
	}else{
		_printprompt("Unknown command '$_'; type 'help' for a list of commands.\n");
	}
	return($rt);
}
#################################################
# mymainloop: Control interactive mode.
#################################################
sub mymainloop{
$_=<<EOSTART;
Stars installer beta version 0.9.
Type 'help' to get started.

EOSTART
	_printprompt($_);
	my($cmd,@args);
	while(1) {
		$::MyInteractive='Y';
		_printprompt("starsinst>");
		$_=<STDIN>;
		s/\s+$//;
		if(/^$/){next;}elsif(/^(exit|quit)$/i){last;}
		$_=_maskargs($_);
		if(/^(\S+)\s+(.+)$/){$cmd=$1;@args=split(/\s+/,$2);
		}elsif(/^(\S+)$/)   {$cmd=$1;@args=();
		}else{
			_printprompt("Unknown command '$_'; type 'help' for a list of commands.\n");
			next;
		}
		submessageexec($cmd,@args);
	}
	return(1);
}
#####################
# main process.
#####################
#-----------------------------------------------------------------------------
sub myconfig{
	my($cfgfile,$setflg)=(shift,shift);
	if(($cfgfile=_checkpathname($cfgfile)) eq ''){return(0);}
	my($key,$content,$updflg);

	if($setflg){
		$updflg=0;
		foreach $key (sort(keys(%::MYVALUE))){
			unless(($key eq KEY_ISWINOS) or ($key=~/^user/i)){next;}
			if(defined($::MYCONFIGVALUE{$key})){
				if($::MYVALUE{$key} ne $::MYCONFIGVALUE{$key}){
					if($::MYCONFIGCONTENTS[$::MYCONFIGINDEX{$key}]
			   =~s/([\t|=]\s*)($::MYCONFIGVALUE{$key})(\s*)$/$1$::MYVALUE{$key}$3/){
						$updflg=1;
					}else{
						_printmessage("Warn: Skipped updating line '$::MYCONFIGCONTENTS[$::MYCONFIGINDEX{$key}]' with value '$::MYVALUE{$key}' of configuration.");
					}
				}
			}elsif($::MYVALUE{$key} ne ''){
				push(@::MYCONFIGCONTENTS,"$key=$::MYVALUE{$key}\n");$updflg=1;
			}
		}
		unless($updflg){return(1);}
		my($fh,$tmpfile)=_mktempfile(_mktempdir());
		print $fh join('',@::MYCONFIGCONTENTS);close($fh);
		_printmessage(MSGI_CONFIG_UPD_START,$cfgfile);
		my $md=_getftype($cfgfile);
		if($md=~/^f/){
			my($totime,$tosize,$tmode)=_getfileinfo($cfgfile);
			my $sfx='bak.'._cnvdatetime(0);
			my($totime,$tosize,$tmode)=_getfileinfo($cfgfile);
			unless(copy($cfgfile,"$cfgfile\.$sfx")){
				return(_printmessage(MSG0_FILE_COPY_FAIL,$cfgfile,"$cfgfile\.$sfx"));
			}
			unless(chmod(oct($tmode),"$cfgfile\.$sfx")){
				return(_printmessage(MSG0_CHMOD_FAIL,"$cfgfile\.$sfx"));
			}
			unless($md=~/^fw/){
				unless(chmod(oct(DEFAULT_PERMISSION),$cfgfile)){
					return(_printmessage(MSG0_CHMOD_FAIL,$cfgfile));
				}
			}
			_printmessage(MSGI_FILE_OLD_RENAMED,$cfgfile,"$cfgfile\.$sfx");
			unless(copy($tmpfile,$cfgfile)){
				return(_printmessage(MSG0_TMPFILE_RENAME_FAIL,$tmpfile,$cfgfile));
			}
			unless(chmod(oct($tmode),"$cfgfile")){
				return(_printmessage(MSG0_CHMOD_FAIL,"$cfgfile"));
			}
		}elsif($md=~/^d/){
			return(_printmessage(MSG0_DIR_EXIST,$cfgfile));
		}else{
			unless(copy($tmpfile,$cfgfile)){
				return(_printmessage(MSG0_TMPFILE_RENAME_FAIL,$tmpfile,$cfgfile));
			}
		}
		_printmessage(MSGI_CONFIG_UPD_END,$cfgfile);
	}else{
		$updflg=0;
		unless(open(CONFIG, "$cfgfile")){
			return(_printmessage(MSG0_CONFIG_OPEN_FAIL,$cfgfile));
		}
		my @bufs=<CONFIG>;close(CONFIG);
		foreach $_ (@bufs){
			if(/^#/){
			}elsif(/^([^\t=]+)([\t=])([^\t=]*)$/){
				my($key,$delim,$content)=($1,$2,$3);
				$content=~s/^\s*//;$content=~s/\s*$//;
				$key=~s/^\s*//;$key=~s/\s*$//;
				if($key eq KEY_ISWINOS){
					if($content eq _getvariable($key)){$updflg=1;}
					last;
				}
			}
		}
		_printmessage(MSGI_CONFIG_READ_START,$cfgfile);
		unless($updflg){
			_printmessage("Warn: This configuration file doesn't contain keyword '"
			      .KEY_ISWINOS."' or has created in different os. Ignored.");
			return(1);
		}
		foreach $_ (@bufs){
			push(@::MYCONFIGCONTENTS,$_);
			if(/^#/){
			}elsif(/^([^\t=]+)([\t=])([^\t=]*)$/){
				my($key,$delim,$content)=($1,$2,$3);
				$content=~s/^\s*//;$content=~s/\s*$//;
				$key=~s/^\s*//;$key=~s/\s*$//;
				if($key eq KEY_ISWINOS){
					$::MYCONFIGINDEX{$key}=$#::MYCONFIGCONTENTS;
					$::MYCONFIGVALUE{$key}=$content;
				}elsif($key=~/^user/){
					$::MYCONFIGINDEX{$key}=$#::MYCONFIGCONTENTS;
					$::MYCONFIGVALUE{$key}=$content;
					if($content ne _getvariable($key)){
						_setvariable($key,$content);
					}
				}else{
					_printmessage("Warn: Skipped reading line '$_' of configuration.");
				}
			}else{
				_printmessage("Warn: Skipped reading line '$_' of configuration.");
			}
		}
		_printmessage(MSGI_CONFIG_READ_END,$cfgfile);
	}
	return(1);
}
sub subhelp{
	my $cmd=lc(shift);
	my %helptbl=();
	$helptbl{"download"}="Download stars-archived-files from web.";
	$helptbl{"extract"}="Extract stars-archived-files already downloaded on disk.";
	$helptbl{"install"}="Download stars-archived-files from web then extract.";
	$helptbl{"starscopy"}="Copy stars directory to other directory.";
	$helptbl{"help"}="prints this screen, or help on 'command'.";
	$helptbl{"exit"}="exits this program.";
	$helptbl{"quit"}="exits this program.";
	$helptbl{"list"}="lists installable packages.";
	$helptbl{"set"}="Set configuration parameters.";
	$helptbl{"saveconfig"}="Save configuration parameters to files.";
	$helptbl{"readconfig"}="Reflesh configuration parameters from files.";

	if($cmd eq 'parameter'){
		_printmessage("-"x78);
	}elsif(($cmd eq '') or (!defined($helptbl{$cmd}))){
		foreach $_(sort(keys(%helptbl))){
			_printmessage(sprintf("%-10s - %s",$_,$helptbl{$_}));
		}
		_printmessage("\nShow more details with 'help <command>'.");
		return(1);
	}else{
		_printmessage("-"x78);
		_printmessage($helptbl{$cmd});
	}

	my $type=_getvariable(KEY_ARCTYPE);
	if($cmd=~/^set$/i){
		_printmessage("-"x40);
		_printmessage("Usage:");
		_printmessage("  "."-"x40);
		_printmessage("  'set': Show all program parameters.");
		_printmessage("  "."-"x40);
		_printmessage("  'set <paramater_name>'");
		_printmessage("     parameter_name: set parameter name which you want to see value.");
		_printmessage("  "."-"x40);
		_printmessage("   'set <paramater_name>=<value>'");
		_printmessage("      parameter_name: set parameter name which you want to set value.");
		_printmessage("      value: set value to parameter.");
		_printmessage("  "."-"x40);
		_printmessage("  Command 'help parameter' show more details about <paramater name>.");
	}elsif($cmd=~/^parameter(s)?$/i){
		_printmessage("Paramater infomation:");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_ISWINOS.": Whether this program executed in Windows OS or not.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_PWD.": This program starting directory.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_ARCTYPE.":");
		_printmessage("    Stars downloadable files has 2 archive types, 'zip' and 'tgz'.");
		_printmessage("    Value set for Windows OS 'zip', or 'tgz'.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_ARCDIR.":");
		_printmessage("    Stars archived files downloaded directory.");
 		_printmessage("    Value changed when command 'download' or 'extract' successfully.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_STARSDEST.": Stars installed directory.");
		_printmessage("    Value changed when command 'install' or 'extract' or 'starscopy' successfully.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_STARSSRC.":");
		_printmessage("    If you want to make mirror of stars, set 'copyfrom' directory of stars.");
 		_printmessage("    Value changed when command 'starscopy' successfully.");
		_printmessage("  "."-"x40);
		_printmessage("  ".KEY_USERTGZCOMMAND.":");
		_printmessage("    Shell command for extracting stars archived tgz file.");
 		_printprompt("    ");_printmessage(MSGI_USERTGZCOMMAND_BLANK);
		_printmessage("  "."-"x40);
		_printmessage(" Paramater starting with 'users_' can be replaced by command 'set' or configration file.");
	}elsif($cmd=~/^install(zip|tgz)?$/i){
		my $path=_checkpathname('stars');
		_printmessage("-"x40);
		_printmessage("Usage: 'install [stars_destination_directory] [module]'");
		_printmessage("");
		_printmessage(" stars_destination_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" module:");
		_printmessage("  set module name    - all module selected for null.");
		_printmessage("                       command 'list' will show you module names.");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" install           - All module selected.");
		_printmessage(" install \"\" kernel - Only 'kernel' module selected.");
		_printmessage(" install $path        - All module selected. Destination is '$path'.");
		_printmessage(" install $path kernel - Only 'kernel' module selected. Destination is '$path'.");
	}elsif($cmd=~/^download(zip|tgz)?$/i){
		my $path=_checkpathname(_getvariable(KEY_ARCTYPE).'s');
		_printmessage("-"x40);
		_printmessage("Usage: 'download [stars_archived_file_destination_directory] [module]'");
		_printmessage("");
		_printmessage(" stars_archived_file_destination_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" module:");
		_printmessage("  set module name    - all module selected for null.");
		_printmessage("                       command 'list' will show you module names.");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" download           - All module selected.");
		_printmessage(" download \"\" kernel - Only 'kernel' module selected.");
		_printmessage(" download $path        - All module selected. Destination is '$path'.");
		_printmessage(" download $path kernel - Only 'kernel' module selected. Destination is '$path'.");
	}elsif($cmd=~/^extract(zip|tgz)?$/i){
		my $from=_checkpathname(_getvariable(KEY_ARCTYPE).'s');
		my $to=_checkpathname('stars');
		_printmessage("-"x40);
		_printmessage("Usage: 'extract [stars_archived_file_saved_directory] [stars_destination_directory] [module] [version]'");
		_printmessage("");
		_printmessage(" stars_archived_file_saved_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" stars_destination_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" module:");
		_printmessage("  set module name    - all module selected for null.");
		_printmessage("                       command 'list' will show you module names.");
		_printmessage(" version:");
		_printmessage("  set version        - newest version selected for null.");
		_printmessage("                       format is 'yyyymmddhhmnsc'");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" extract           - All module selected.");
		_printmessage(" extract \"\" \"\" kernel - Only 'kernel' module selected.");
		_printmessage(" extract \"\" \"\" \"\" 20070622144644 - version '20070622144644' selected.");
		_printmessage(" extract $from $to - All module selected. Archived file saved in '$from' and destination is '$to'.");
	}elsif($cmd=~/^starscopy$/i){
		my $from=_checkpathname('stars');
		my $to=_checkpathname('newstars');
		_printmessage("-"x40);
		_printmessage("Usage: 'starscopy [stars_saved_directory] [stars_destination_directory] [module]'");
		_printmessage("");
		_printmessage(" stars_saved_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" stars_destination_directory:");
		_printmessage("  set directory name - interactive input supported for null.");
		_printmessage(" module:");
		_printmessage("  set module name    - all module selected for null.");
		_printmessage("                       command 'list' will show you module names.");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" starscopy - All module selected.");
		_printmessage(" starscopy \"\" \"\" kernel - Only 'kernel' module selected.");
		_printmessage(" starscopy $from $to - All module selected. Stars saved in '$from' and destination is '$to'.");
	}elsif($cmd=~/^saveconfig$/i){
		my $cfg=_checkpathname('mystars.cfg');
		_printmessage("-"x40);
		_printmessage("Usage: 'saveconfig [config_file]'");
		_printmessage("");
		_printmessage(" config_file:");
		_printmessage("  set config file name - 'starsinst.cfg' used for null.");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" saveconfig      - Save configuration to './starsinst.cfg'.");
		_printmessage(" saveconfig $cfg - Save configuration to '$cfg'.");
	}elsif($cmd=~/^readconfig$/i){
		my $cfg=_checkpathname('mystars.cfg');
		_printmessage("-"x40);
		_printmessage("Usage: 'readconfig [config_file]'");
		_printmessage("");
		_printmessage(" config_file:");
		_printmessage("  set config file name - 'starsinst.cfg' used for null.");
		_printmessage("");
		_printmessage("Example:");
		_printmessage(" readconfig      - Read configuration file './starsinst.cfg'.");
		_printmessage(" readconfig $cfg - Read configuration file '$cfg'.");
	}
	_printmessage("-"x78);
	return(1);
}
#-----------------------------------------------------------------------------
sub usage{
#####	Todo: Please modify help message for "-h" option.	#####
	print "Usage: $0 [-h]|[-config=<filename1>] [-script=<filename2>]\n";
	print<<EOUSAGE;
   -h                    Show this help.
   -config=<filename1>   Include configuration <filename1>. (default: starsinst.cfg)
   -log=<filename2>      Logging to <filename2>. (no default filename)
   -script=<filename3>   Execute script <filename3>. (no default filename)';
EOUSAGE
	exit(0);
}
#-----------------------------------------------------------------------------
sub main{
	# Internal Parameters.
	$::MyInteractive='Y';
	$::MYCONFIGFILE='';
	$::MYSCRIPT='';
	$::MYLOGFILE='';

	# ToDo: You can set option switchs. See help 'Getopt::Long'.
	GetOptions(
	'h'       => \&usage,
#	'd'       => \$::Debug,
	'log=s'   => \$::MYLOGFILE,
	'config=s'=> \$::MYCONFIGFILE,
	'script=s'=> \$::MYSCRIPT
	) or die 'Bad switch.\n';

	# Check logfilename if defined.
	if($::MYLOGFILE){
		if((-d $::MYLOGFILE) or (-f $::MYLOGFILE and !-w $::MYLOGFILE)){
			print "Error: Unabled to open logfile '$::MYLOGFILE' with write mode.","\n";
			exit;
		}
	}

	_printmessage("---------------------------------------");
	_printmessage("Reading environments..");
	# Check windows os or not.
	if(_setvariable(KEY_PWD,_getpwd())=~/^\S\:/){
		_setvariable(KEY_ISWINOS,1);_setvariable(KEY_DIRDELIM,'\\');
	}else{
		_setvariable(KEY_ISWINOS,0);_setvariable(KEY_DIRDELIM,'/');
	}

	# Set default archive file type.
	if(_getvariable(KEY_ISWINOS) and _ismodule(MOD_ARCHIVE_ZIP)){
		_setvariable(KEY_ARCTYPE,CONST_ZIP);
	}else{
		_setvariable(KEY_ARCTYPE,CONST_TGZ);
	}

	# convert to fullpath, if defined.
	if($::MYLOGFILE){
		$::MYLOGFILE=_checkpathname($::MYLOGFILE);
	}

	# Read configuration, if exist.
	$::MYCONFIGFILE=_getconfigfilename($::MYCONFIGFILE);
	unless($::MYCONFIGFILE){exit;}
	if(-e $::MYCONFIGFILE){
		_printmessage("---------------------------------------");
		unless(myconfig($::MYCONFIGFILE,0)){exit;}
	}
	
	# Run script if defined.
	if($::MYSCRIPT){
		unless($::MYSCRIPT=_checkfileexist($::MYSCRIPT)){exit;}
		unless(myrunscript($::MYSCRIPT)){exit;}
	}else{
		# Go to interactive process.
		_printmessage("---------------------------------------");
		mymainloop();
		# Save configuration.
		_printmessage("Terminating now...");
		myconfig($::MYCONFIGFILE,1);
		_printmessage("Bye.");
	}
	exit;
}
sub _mktemplatescript{
	my $outfile=shift;
	my($msg)="Please enter file name for script template saving. :";
	while($outfile=~/^\s*$/){
		$outfile=_dirinput($msg,"File name is [#STDIN#].",$outfile);
		if($outfile eq ''){last;}
		unless(_checkdirnotexist($outfile)){$outfile='',next;}
		while(-e $outfile){
			$msg="Same file exists. Overwrite Ok? (Input Y[es] or R[etry] or C[ancel] then [Enter]) :";
			_printprompt($msg);
			$_=uc<STDIN>;chomp $_;
			if(/^Y(ES)?/){last;}elsif(/^R(ETRY)?/){$outfile='';last;
			}elsif(/^C(ANCEL)?/){$outfile='';last;}
		}
		if(/^(Y|R)/){next;}
		last;
	}
	if($outfile=~/^\s*$/){return(0);}
	unless(open(FILE,">$outfile")){
		return(_printmessage(MSG0_FILE_OPEN_FAIL,$outfile));
	}
	while(<DATA>){
		print FILE $_;
	}
	_printmessage("Template script saved to '$outfile'");
	close(FILE);
	return(1);
}
main();
1;
__DATA__
#########################################
## Config file for STARS installation.	#
#########################################

#Perl_Exfile			C:/perl/bin/perl.exe
#SHORTCUTDIR			D:\

###	Installation Script	##############################################
!Begin MAIN

##################
## Windows
##################
#cd
#inputstarsdest
#install $user_default_stars_destination_directory$
#install $user_default_stars_destination_directory$ kernel
#install $user_default_stars_destination_directory$ syslogger
#filecopy $user_default_stars_destination_directory$\syslogger syslogger.key $user_default_stars_destination_directory$\kernel\takaserv-lib
#saveconfig .\winscript.cfg
#cd $user_default_stars_destination_directory$\kernel
#runshell "takaserv.exe --remove"
#runshell "takaserv.exe --install auto -lib $user_default_stars_destination_directory$\kernel\takaserv-lib"
#cd
#mkshortcut $SHORTCUTDIR$\syslogger.lnk \"$Perl_Exfile$\" "\"$user_default_stars_destination_directory$\syslogger\syslogger\" localhost" \"$user_default_stars_destination_directory$\syslogger\"

##################
## Not Windows
##################
#cd
#inputstarsdest
#install $user_default_stars_destination_directory$
#install $user_default_stars_destination_directory$ syslogger
#install $user_default_stars_destination_directory$ kernel
#install $user_default_stars_destination_directory$ syslogger
#filecopy $user_default_stars_destination_directory$\syslogger syslogger.key $user_default_stars_destination_directory$\kernel\takaserv-lib
#saveconfig ./myscript.cfg
#runshell "echo \"Read infomration file \'$user_default_stars_destination_directory$/kernel/readme.txt\'\""

!End
