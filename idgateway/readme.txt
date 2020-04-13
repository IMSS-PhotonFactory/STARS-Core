##
## STARS idgateway
##

==========================================================================
About "idgateway" Setup
---------------------------------------------------------------------------
=> See "idgatewayGeneral.pdf".

==========================================================================
About "idgateway" Installed Beamline List
---------------------------------------------------------------------------
=> BL-3A for IDServer"ID03" BusyControl Unsupported Version
=> BL-16A for IDServer"ID161" 2010/4/1
=> NW-2A for IDServer"NW2" 2010/4/12
=> NE-1A for IDServer"NE1" 2010/5/7

==========================================================================
About Stars Commands => See "idgatewayCommandReference.pdf".
---------------------------------------------------------------------------
******************************
 for IDServerID:	ID03
******************************
Target: Gap (must be number-format. minus ok)

Move:		idgateway.(IDServerID).Gap SetValue <Gap Value>
GetCurrent:	idgateway.(IDServerID).Gap GetValue

Example (for ID03):

(Send)  idgateway.ID03.Gap GetValue
(Reply) idgateway.ID03.Gap>term1 @GetValue 5.1
(Send)  idgateway.ID03.Gap SetValue 5.9960
(Reply) idgateway.ID03.Gap>term1 @SetValue 5.9960 Ok:

******************************
 for IDServerID:	ID161
******************************
Target: Mode (must be in list of "0:C+R 1:C-R 2:LHR 3:LVR 4:E+R 5:E-R")

Move:		idgateway.ID161.Mode SetValue <Mode Value>
GetCurrent:	idgateway.ID161.Mode GetValue	
GetBusyOrNot:	idgateway.ID161.Mode IsBusy
Event:		idgateway.ID161.Mode _ChangedValue <Mode Current>
		idgateway.ID161.Mode _ChangedIsBusy <0 or 1>

Target: Rho2 (must be number-format. minus ok)

Move:		idgateway.ID161.Rho2 SetValue <Rho2 Value>
GetCurrent:	idgateway.ID161.Rho2 GetValue	
GetBusyOrNot:	idgateway.ID161.Rho2 IsBusy
Event:		idgateway.ID161.Rho2 _ChangedValue <Rho2 Current>
		idgateway.ID161.Rho2 _ChangedIsBusy <0 or 1>

Example (for ID161):

(Send)  idgateway.ID161.Mode GetValue
(Reply) idgateway.ID161.Mode>term1 @GetValue 1
(Send)  idgateway.ID161.Mode IsBusy
(Reply) idgateway.ID161.Mode>term1 @IsBusy 0
(Send)  idgateway.ID161.Rho2 IsBusy
(Reply) idgateway.ID161.Rho2>term1 @IsBusy 0
(Send)  idgateway.ID161.Mode SetValue 0
(Reply) idgateway.ID161.Mode>term1 @SetValue 0 Ok:
(Send)  idgateway.ID161.Mode GetValue
(Reply) idgateway.ID161.Mode>term1 @GetValue 0
(Send)  idgateway.ID161.Rho2 SetValue 5.9960
(Reply) idgateway.ID161.Rho2>term1 @SetValue 5.9960 Ok:

******************************
 for IDServerID:	NW2
******************************
Target: Gap and Tpr (must be number-format. minus ok)

Move:		idgateway.NW2.Gap SetValue <Gap Value>
GetCurrent:	idgateway.NW2.Gap GetValue	
GetBusyOrNot:	idgateway.NW2.Gap IsBusy
Event:		idgateway.NW2.Gap _ChangedValue <Gap Current>
		idgateway.NW2.Gap _ChangedIsBusy <0 or 1>

Move:		idgateway.NW2.Tpr SetValue <Tpr Value>
GetCurrent:	idgateway.NW2.Tpr GetValue	
GetBusyOrNot:	idgateway.NW2.Tpr IsBusy
Event:		idgateway.NW2.Tpr _ChangedValue <Tpr Current>
		idgateway.NW2.Tpr _ChangedIsBusy <0 or 1>

Example (for NW2):

(Send)  idgateway.NW2.Gap IsBusy
(Reply) idgateway.NW2.Gap>term1 @IsBusy 0
(Send)  idgateway.NW2.Gap SetValue 18
(Reply) idgateway.NW2.Gap>term1 @SetValue 18 Ok:
(Send)  idgateway.NW2.Tpr IsBusy
(Reply) idgateway.NW2.Tpr>term1 @IsBusy 0
(Send)  idgateway.NW2.Tpr SetValue 1
(Reply) idgateway.NW2.Tpr>term1 @SetValue 1 Ok:

******************************
 for IDServerID:	NE1
******************************
Target: GapY (must be number-format. minus ok)

Move:		idgateway.NE1.GapY SetValue <GapY Value>
GetCurrent:	idgateway.NE1.GapY GetValue	
GetBusyOrNot:	idgateway.NE1.GapY IsBusy
Event:		idgateway.NE1.GapY _ChangedValue <GapY Current>
		idgateway.NE1.GapY _ChangedIsBusy <0 or 1>

Example (for NE1):

(Send)  idgateway.NE1.GapY IsBusy
(Reply) idgateway.NE1.GapY>term1 @IsBusy 0
(Send)  idgateway.NE1.GapY SetValue 40
(Reply) idgateway.NE1.GapY>term1 @SetValue 40 Ok:

************************************************
Stars Commands for Ring Information (ReadOnly)
************************************************
idgateway.Ring.DCCT GetValue
idgateway.Ring.Energy GetValue
idgateway.Ring.Vacuum GetValue
idgateway.Ring.Lifetime GetValue
idgateway.Ring.IDGap GetValue
idgateway.Ring.Status GetValue
idgateway.Ring.Message GetValue
