#Configuration of mdirec client.

if(
$::NodeName eq 'mcdirec'
){###############################################################################

#############################
#		Global Variable		#
#############################

#####	ToDo: Variable	#####
$::Server		=	'localhost';

#####	Read File Variable	#####
$::PathName		=	'./script/';

#####	Macro Table System File Variable	#####
$::MctSysFile	=	'./system/msystem.mct';

#####	System Command Variable	#####
%::System_Cmd = '';				#Default System Command = ''

#####	Script Excute Error parameter set	#####
$::Error		=	'DEFAULT';

#####	Script Excute Error parameter set	#####
$::Break		=	'';

################################################################################
}else{
	die "Bad node name.";
}
1;

