@echo off
title STARS Server installer
echo ---------------------------------------------------------------
echo STARS Server installer program for windows os.
echo ---------------------------------------------------------------
echo Install a 'Stars Server' windows service.
echo     Stars Server port: 6057
echo     Service name: takaserv
echo Please run this program with windows administrator privileges.
echo ---------------------------------------------------------------
echo Press any key to continue.
pause 
echo.
cd /D %~dp0
echo Move to current folder '%~dp0'
echo.
echo Install Stars server.
@echo on
takaserv --install auto -lib %~dp0takaserv-lib
@cmd /k
