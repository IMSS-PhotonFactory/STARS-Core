#Configuration of mark102 client.
$::DeviceType="MARK102";

if(
$::NodeName eq 'shot102'
){###############################################################################
@::MotorName     = qw(X1 X2);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.126'; #NPort host name.
$::NPORT_PORT  = 4003;             #NPort port number.

# Maxumim and Minimum values for Input Check
#$::ConfigLimitMaximum{$::MotorName[0]}= 6000;
#$::ConfigLimitMinimum{$::MotorName[0]}=-2000;
#$::ConfigLimitMaximum{$::MotorName[1]}= 6000;
#$::ConfigLimitMinimum{$::MotorName[1]}=-2000;
# 9/21 Motor exchange
$::ConfigLimitMaximum{$::MotorName[0]}= 120000;
$::ConfigLimitMinimum{$::MotorName[0]}=-40000;
$::ConfigLimitMaximum{$::MotorName[1]}= 120000;
$::ConfigLimitMinimum{$::MotorName[1]}=-40000;

# Maxumim and Minimum values for Failsafe(Auto stop)
#$::ConfigFailsafeMaximum{$::MotorName[0]}= $::ConfigLimitMaximum{$::MotorName[0]};
#$::ConfigFailsafeMinimum{$::MotorName[0]}= $::ConfigLimitMinimum{$::MotorName[0]};
#$::ConfigFailsafeMaximum{$::MotorName[1]}= $::ConfigLimitMaximum{$::MotorName[1]};
#$::ConfigFailsafeMinimum{$::MotorName[1]}= $::ConfigLimitMinimum{$::MotorName[1]};

# Overwrite SpeedandAccTime
# Please comment if use controller's native settings.
#$::ConfigSpeedAccTime{$::MotorName[0]}= "50,500,0";
#$::ConfigSpeedAccTime{$::MotorName[1]}= "50,500,0";
$::ConfigSpeedAccTime{$::MotorName[0]}= "100,1000,0";
$::ConfigSpeedAccTime{$::MotorName[1]}= "100,1000,0";

}elsif(
$::NodeName eq 'shot102_2'
){###############################################################################
@::MotorName     = qw(Z1 Z2);

#STARS server
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.126'; #NPort host name.
$::NPORT_PORT  = 4004;             #NPort port number.

# Maxumim and Minimum values for Input Check
#$::ConfigLimitMaximum{$::MotorName[0]}  = 99999999;
#$::ConfigLimitMinimum{$::MotorName[0]}  =-99999999;
#$::ConfigLimitMaximum{$::MotorName[1]}=   99999999;
#$::ConfigLimitMinimum{$::MotorName[1]}=  -99999999;
#$::ConfigLimitMaximum{$::MotorName[0]}  =   103000;
#$::ConfigLimitMinimum{$::MotorName[0]}  =    -1500;
#$::ConfigLimitMaximum{$::MotorName[1]}=     103000;
#$::ConfigLimitMinimum{$::MotorName[1]}=      -1500;
$::ConfigLimitMaximum{$::MotorName[0]}  =    53000;
$::ConfigLimitMinimum{$::MotorName[0]}  =   -53000;
$::ConfigLimitMaximum{$::MotorName[1]}=      55000;
$::ConfigLimitMinimum{$::MotorName[1]}=     -49000;

# Maxumim and Minimum values for Failsafe(Auto stop)
#$::ConfigFailsafeMaximum{$::MotorName[0]} =$::ConfigLimitMaximum{$::MotorName[0]};
#$::ConfigFailsafeMinimum{$::MotorName[0]} =$::ConfigLimitMinimum{$::MotorName[0]};
#$::ConfigFailsafeMaximum{$::MotorName[1]} =$::ConfigLimitMaximum{$::MotorName[1]};
#$::ConfigFailsafeMinimum{$::MotorName[1]} =$::ConfigLimitMinimum{$::MotorName[1]};

# Overwrite SpeedandAccTime
# Please comment if use controller's native settings.
#$::ConfigSpeedAccTime{$::MotorName[0]}= "100,2000,0";    # Too fast.
#$::ConfigSpeedAccTime{$::MotorName[1]}= "100,2000,0";    # Too fast.
$::ConfigSpeedAccTime{$::MotorName[0]}= "100,1000,0";
$::ConfigSpeedAccTime{$::MotorName[1]}= "100,1000,0";

}else{
	die "Bad node name.";
}
1;
