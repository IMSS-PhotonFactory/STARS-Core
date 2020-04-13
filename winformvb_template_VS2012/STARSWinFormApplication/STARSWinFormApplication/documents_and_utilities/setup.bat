@echo off
if ERRORLEVEL 1 set ER=1

@echo off
if "%ER%"=="1" echo Please ignore previous errors.
echo --------------------------------------------------------------------------
echo on
createkey.exe $safeprojectname$.key
mkdir ..\bin\Release
copy $safeprojectname$.key ..\bin\Release\
copy $safeprojectname$.key ..\bin\Debug\
@echo off
echo --------------------------------------------------------------------------
echo     $safeprojectname$.key has been created (or updated) and copied
echo     into local directories.
echo     Please copy $safeprojectname$.key into takaserv-lib of STARS server.
echo --------------------------------------------------------------------------
pause
