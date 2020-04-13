#Configuration of mceditor client.

if(
$::NodeName eq 'mceditor'
){###############################################################################

#############################
#		Global Variable		#
#############################

#####	ToDo: Variable	#####
#$::Server		=	'bl1b-server';		#Default Stars server = 'localhost'
$::Server		=	'localhost';		#Default Stars server = 'localhost'

$::McDirector   =	'mcdirec';			#Default mcdierctor

#####	Read File Variable	#####
$::PathName		=	'./script/';		#Default Path name = './script/'

#####	Macro Table System File Variable	#####
$::MctSysFile	=	'./system/msystem.mct';
										#Default Macro Table System file = './system/msystem.mct'

#####	System Command Variable	#####
%::System_Cmd = '';						#Default System Command = ''

#####	Perl Convert data Variable	#####
@::PerlCon_Dat = '';					#Perl Convert data = Default ''

#####	Script Excute Error parameter set	#####
$::Error		=	'DEFAULT';			#Default Erroe Massage = 'DEFAULT'

#####	FREQ: parameter set	#####
$::Ifrq_start	=	20;        			#Default FREQ Start number = 20 HZ
$::Ifrq_max		=	2000;       		#Default FREQ Max number = 2.0 KHZ
$::Ifrq_step	=	10;        			#Default FREQ Step number = 10 HZ
$::Ifrq_ampl	=	950;       			#Default FREQ Ampl number = 800 MV

#####	Mode: parameter set	#####
$::Imod_sel		=	1;        			#Default Mode Select No = 1(VOLT AC). [0:FREQ, 1:VOLT AC]

################################################################################
}else{
	die "Bad node name.";
}
1;

