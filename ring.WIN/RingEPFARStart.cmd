@echo on
REM ######################################################
REM Sample Shell for Run ring.exe in Windows OS
REM ######################################################

set TINE_HOME=.

echo TINE_HOME Directory is '%TINE_HOME%'

if not exist "%TINE_HOME%\cshosts.csv" goto CSVNOTFOUND
REM C:\stars\ring\ringEPF.exe -myaddr:130.87.183.167 
.\ringEPFAR.exe Ring localhost
goto END
:CSVNOTFOUND
ECHO TINE DATABASE FILE '%TINE_HOME%\cshosts.csv' not found.
:END