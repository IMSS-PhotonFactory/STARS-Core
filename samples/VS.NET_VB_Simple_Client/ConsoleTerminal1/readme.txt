Stars for VB.NET Sample Program - ConsoleTerminal1 

A. ABOUT 'ConsoleTerminal1.exe'

 This is a stars client program using .NET architecture.
 Programing tool is Microsoft Visual Basic 2005.
 
 you can send and receive the stars messages by using this program.
 This execution file runs under .NET 2.x.

B. SOURCE and PROGRAM FILE LIST

----------------------------------------------------------------------
Filename                     -----  Description 
----------------------------------------------------------------------
<Sources>
ConsoleTerminal1.sln          -----  Solution File 
ConsoleTerminal1.vbproj       -----  Visual Basic 2005 Project File 
Module1.vb                    -----  Visual Basic 2005 Source File 
My Project\*.*                -----  Auto-generated file with editing project-properties 
app.config                    -----  Auto-generated file with editing project-properties 'My Settings'
ConsoleTerminal1.xml          -----  Auto-generated file with compiling

<Released-files for Execution>
ConsoleTerminal1.exe          -----  Program Executable File 
ConsoleTerminal1.exe.config   -----  Program Parameter File 
StarsInterface.dll            -----  Stars .NET Class library 
csterm.key                    -----  Stars key file  

<Reference>
readme.txt                    -----  Program General Information
ProgramReference.html         -----  Program Details

<Files for debug mode>
\Debug\StarsInterface.dll     -----  Stars .NET Class library, only use for debug 
\Debug\csterm.key             -----  Stars key file, only use for debug 
----------------------------------------------------------------------


C. SETUP and RUN

 Default stars nodename is "csterm" and hostname of StarsServer is "localhost".

 1. (Optional)
    Edit ConsoleTerminal1.exe.config if you want to change default stars nodename and hostname of stars server.
 ------------------------------ 
    <applicationSettings>
        <ConsoleTerminal1.My.MySettings>
            <setting name="Nodename" serializeAs="String">
                <value>csterm</value>  <===== !!! Change stars nodename here!!!!
            </setting>
            <setting name="StarsServer" serializeAs="String">
                <value>localhost</value>   <===== !!! Change hostname of stars server here!!!!
            </setting>
        </ConsoleTerminal1.My.MySettings>
     </applicationSettings>
 ------------------------------ 

 2. Setup the stars keyfile to Stars Server.
     Copy the stars keyfile '<stars nodename>.key' to <Stars Server's folder>/takaserv-lib/.

 3. Execute ConsoleTerminal1.exe
     Run 'ConsoleTerminal1.exe' after starts the stars server running.
  
     Usage: 
         ConsoleTerminal1.exe [stars nodename] [stars server hostname]

D. About Program - more details.
 See 'ProgramReference.html' for program details.

(END)