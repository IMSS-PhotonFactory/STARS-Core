Stars for .NET C# Sample Program - GUI_Terminal1 

A. ABOUT 'GUI_Terminal1.exe'

 This is a stars client program using .NET architecture.
 Programing tool is Microsoft Visual Basic 2005.
 
 you can send and receive the stars messages by using this program.
 This execution file runs under .NET 2.x.

B. SOURCE and PROGRAM FILE LIST

----------------------------------------------------------------------
Filename                      -----  Description 
----------------------------------------------------------------------
<Sources>
GUI_Terminal1.sln                  -----  Solution File 
GUI_Terminal1.vbproj               -----  Visual Basic 2005 Project File 
Module.vb                          -----  Visual Basic 2005 Source File 
Form1.vb                           -----  Visual Basic 2005 Source File 
Form1.Designer.vb                  -----  Visual Basic 2005 Source File
Form1.resx                         -----  Visual Basic 2005 Source File
My Project\*.*                     -----  Auto-generated file with editing project-properties 
app.config                         -----  Auto-generated file with editing project-properties 'My Settings'
GUI_Terminal1.xml                  -----  Auto-generated file with compiling

<Released-files for Execution>
GUI_Terminal1.exe                  -----  Program Executable File 
GUI_Terminal1.exe.config           -----  Program Parameter File 
csterm.key                         -----  Stars key file  
StarsInterface.dll                 -----  Stars .NET Class library 
StarsInterfaceWinForm.dll          -----  Stars .NET Class library for Forms

<Reference>
readme.txt                         -----  Program General Information
ProgramReference.html              -----  Program Details

<Files for debug mode>
\Debug\csterm.key                  -----  Stars key file, only use for debug ----------------------------------------------------------------------
\Debug\StarsInterface.dll          -----  Stars .NET Class library, only use for debug 
\Debug\StarsInterfaceWinForm.dll   -----  Stars .NET Class library, only use for debug 


C. SETUP and RUN

 Default stars nodename is "csterm" and hostname of StarsServer is "localhost".

 1. (Optional)
    Edit GUI_Terminal1.exe.config if you want to change default stars nodename and hostname of stars server.
 ------------------------------ 
    <applicationSettings>
        <GUI_Terminal1.My.MySettings>
            <setting name="Nodename" serializeAs="String">
                <value>csterm</value>  <===== !!! Change stars nodename here!!!!
            </setting>
            <setting name="StarsServer" serializeAs="String">
                <value>localhost</value>   <===== !!! Change hostname of stars server here!!!!
            </setting>
        </GUI_Terminal1.My.MySettings>
    </applicationSettings>
 ------------------------------ 

 2. Setup the stars keyfile to Stars Server.
     Copy the stars keyfile '<stars nodename>.key' to <Stars Server's folder>/takaserv-lib/.

 3. Execute GUI_Terminal1.exe
     Run 'GUI_Terminal1.exe' after starts the stars server running.
  
     Usage: 
         GUI_Terminal1.exe [stars nodename] [stars server hostname]

D. About Program - more details.
 See 'ProgramReference.html' for program details.

(END)