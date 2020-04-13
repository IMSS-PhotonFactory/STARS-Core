@echo off
title STARS Server uninstaller
echo ---------------------------------------------------------------
echo STARS Server uninstaller program for windows os.
echo ---------------------------------------------------------------
echo Uninstall the 'Stars Server' windows service.
echo Please run this program with windows administrator privileges.
echo ---------------------------------------------------------------
echo Press any key to continue.
pause 
echo.
cd /D %~dp0
echo Move to current folder '%~dp0'
echo.
echo Uninstall Stars server 
@echo on
takaserv --remove
@cmd /k
