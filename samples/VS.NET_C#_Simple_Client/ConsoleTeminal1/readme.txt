Stars for .NET C# Sample Program - ConsoleTerminal1 

A. ABOUT 'ConsoleTerminal1.exe'

 This is a stars client program using .NET architecture.
 Programing tool is Microsoft Visual C# 2005.
 
 you can send and receive the stars messages by using this program.
 This execution file runs under both .NET 1.x, 2.x, and linux - Mono environment.

B. SOURCE and PROGRAM FILE LIST

----------------------------------------------------------------------
Filename                -----  Description 
----------------------------------------------------------------------
ConsoleTerminal1.sln    -----  Solution File 
ConsoleTerminal1.csproj -----  Visual C# Project File 
Program.cs              -----  Visual C# Source File 
StarsInterface.dll      -----  Stars .NET Class library 

ConsoleTerminal1.exe    -----  Program Executable File 
csterm.key              -----  Stars key file  
\Debug\csterm.key       -----  Stars key file, only use for debug. 

readme.txt              -----  Program General Information.
ProgramReference.html   -----  Program Details
StarsInterface.xml      -----  XML Information file of StarsInterface.dll
----------------------------------------------------------------------


C. SETUP and RUN

 1. Setup the stars keyfile to Stars Server.
     Copy the stars keyfile 'csterm.key' to <Stars Server's folder>/takaserv-lib/.

 2. Execute ConsoleTerminal1.exe
     Run 'ConsoleTerminal1.exe' after starts the stars server running.
  
     Usage: 
         ConsoleTerminal1.exe [stars nodename] [stars server hostname]

         Program parameters: 
             stars nodename: default 'csterm.key' 
             stars server hostname: default 'localhost' 


D. About Program - more details.
 See 'ProgramReference.html' for program details.

(END)