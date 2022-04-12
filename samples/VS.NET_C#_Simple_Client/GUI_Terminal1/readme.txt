Stars for .NET C# Sample Program - GUI_Terminal1 

A. ABOUT 'GUI_Terminal1.exe'

 This is a stars client program using .NET architecture.
 Programing tool is Microsoft Visual C# 2005.
 
 you can send and receive the stars messages by using this program.
 This execution file runs under both .NET 1.x, 2.x, and linux - Mono environment.

B. SOURCE and PROGRAM FILE LIST

----------------------------------------------------------------------
Filename                      -----  Description 
----------------------------------------------------------------------
GUI_Terminal1.sln             -----  Solution File 
GUI_Terminal1.csproj          -----  Visual C# Project File 
Program.cs                    -----  Visual C# Source File 
Form1.cs                      -----  Visual C# Source File 
Form1.Designer.cs             -----  Visual C# Source File 

\Properties\AssemblyInfo.cs        -----  Visual C# Source File
\Properties\Resources.resx         -----  .NET Managed Resources
\Properties\Resources.Designer.cs  -----  Visual C# Source File
\Properties\Settings.settings      -----  Visual Studio Settings - Designer File
\Properties\Settings.Designer.cs   -----  Visual C# Source File

StarsInterface.dll          -----  Stars .NET Class library 
StarsInterfaceWinForm.dll   -----  Stars .NET Class library for Forms

GUI_Terminal1.exe           -----  Program Executable File 
csterm.key                  -----  Stars key file  

\Debug\csterm.key           -----  Stars key file, only use for debug. 

readme.txt                  -----  Program General Information.
ProgramReference.html       -----  Program Details
StarsInterface.xml          -----  XML Information file of StarsInterface.dll
StarsInterfaceWinForm.xml   -----  XML Information file of StarsInterfaceWinForm.xml
----------------------------------------------------------------------


C. SETUP and RUN

 1. Setup the stars keyfile to Stars Server.
     Copy the stars keyfile 'csterm.key' to <Stars Server's folder>/takaserv-lib/.

 2. Execute GUI_Terminal1.exe
     Run 'GUI_Terminal1.exe' after starts the stars server running.
  
     Usage: 
         GUI_Terminal1.exe [stars nodename] [stars server hostname]

         Program parameters: 
             stars nodename: default 'csterm.key' 
             stars server hostname: default 'localhost' 


D. About Program - more details.
 See 'ProgramReference.html' for program details.

(END)