##
## manager
##

==========================================================================
Usage: perl manager [-config <Configuration Filename>]

manager needs "manager configuration file".

Please edit the "manager configuration file" before running this program.

"manager.cfg" is the default filename of "manager configuration file". 
Use "-config" option to change the filename of it.

==========================================================================
Current version =>
 2009-02-27 
  AutoRestart function - "try to execute commands until success" is mainly added.
  Logging function is added.
  $Revision: 1.1 $
---------------------------------------------
 2006/04/24 
   Previous distribution.($Revision: 1.1 $)
==========================================================================
About manager configuration file.

############################
# Parameters for Stars 
############################
NodeName      = manager-bl1a
StarsServer   = localhost
StarsPort     = 6057
StarsKey      = manager-bl1a.key
StarsInterval = 500

# StarsInterval (New parameter)
# => unit: milliseconds.
# => default value: 5000 (5 sec)
# => This value is used as interval for checking AutoRestart

############################
# Parameters for Logging
############################
Logging       = no
Logdir        = d:\

# Logging (New parameter)
# => set yes for enabling logging.
# => default value: no

# Logdir (New parameter)
# => set [logging directory name] to Logdir 
# => default value: [undefined]
# => Please set this value if you want to use logging function.

################################################
# Parameters for controlling child processes
################################################
#UseKill      = KILL
#UseKill      = STOP
UseKill       = yes

################################################
# Parameters for allowed controller for manager 
################################################
MasterNode    = term1 spman-bl1a manager-cntrl

################################################
# Parameters for AutoRun
################################################
AutoRestart   = no
AutoRun       = syslogger

# AutoRestart (New parameter)
# => set yes for enabling "AutoRestart" function.
# => default value: no
# => "AutoRestart Function"
# =>  Try to restart commands, which is listed in "AutoRun" and has restartable setting, if it have failed to be executed. 
# =>  Explicitly teminated commands via manager is excluded from the target of "Auto Restart".

################################################
# Parameters for commands to be executed.
################################################
### syslogger
Dev:syslogger         = perl syslogger -dir d:\
Dev:syslogger:Dir     = d:\CVSROOT\stars\syslogger
Dev:syslogger:AutoRestart = yes
Dev:syslogger:AutoRestart:CheckInterval = 10000

# Dev:[command name]
# => Set command statement.

# Dev:[command name]:Dir
# => Set command executing directory.

# Dev:[command name]:AutoRestart (New parameter)
# => default: no (Disabled)
# => Set yes if you want to enable this command automatically restartable.

# Dev:[command name]:AutoRestart:CheckInterval (New parameter)
# => unit: milliseconds.
# => default: 15000 (15 sec)
# => Set checking time interval for being automatically restarted.
