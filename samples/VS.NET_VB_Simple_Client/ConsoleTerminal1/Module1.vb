Module Module1

    'Declare Stars Object
    Private stars As STARS.StarsInterface

    Sub Main()

        '!!See Project MySettings Property!! Default nodename and server
        '        Dim starsargs() As String = New String() {"csterm", "localhost"}
        Dim starsargs() As String = New String() {My.Settings.Nodename, My.Settings.StarsServer}

        ' Check Program Parameters
        Dim cmds As String() = System.Environment.GetCommandLineArgs()
        If (cmds.Length >= 3) Then
            starsargs(0) = cmds(1)
            starsargs(1) = cmds(2)
        ElseIf (cmds.Length = 2) Then
            starsargs(0) = cmds(1)
        End If

        ' Step1. Connect to Stars.
        stars = New STARS.StarsInterface(starsargs(0), starsargs(1))
        Try
            stars.Connect()
        Catch se As Exception
            Console.WriteLine(se.Message)
            Exit Sub
        End Try

        ' Step2. Add the stars handler named 'Stars_Message_Received' which is called when arriving stars messages via TCP/IP socket.
        stars.StartCbHandler(New STARS.StarsCbHandler(AddressOf Stars_Message_Received))

        ' Step3. Waiting for the input from console.
        ' until entering 'Quit' or 'Exit'.
        Console.WriteLine("Input Stars Message, for example 'System hello', or 'help' for help.")
        Dim buf As String
        While (True)
            buf = Console.ReadLine()
            If (buf.Trim.Equals("")) Then
                Continue While
            ElseIf (buf.ToUpper().Equals("QUIT")) Then
                Exit While
            ElseIf (buf.ToUpper().Equals("EXIT")) Then
                Exit While
            ElseIf (buf.ToUpper().Equals("HELP")) Then
                Console.WriteLine("Enter [help|quit|exit|'Stars Message to be sended']")
            Else
                Console.WriteLine("SEND#" + buf + "#")
				Try
	                stars.Send(buf)
                Catch se As Exception
                    Console.WriteLine(se.Message)
                    Exit While
	            End Try
            End If
        End While
    End Sub

    '
    ' This is Stars Handler called when arriving Stars Messages.
    '
    Private Sub Stars_Message_Received(ByVal sender As Object, ByVal cb As STARS.StarsCbArgs)
        Dim sendbuf As String
        If (cb.Message.Trim.Equals("")) Then
            ' No Message
            Console.WriteLine("RECV#{0}", cb.allMessage + "#")
            sendbuf = cb.from + " @" + cb.Message + " Er: Bad command."
            stars.Send(sendbuf)
            Console.WriteLine("RPLY#" + sendbuf)
        ElseIf (cb.command.StartsWith("@")) Then
            ' Begin with '@' : Reply's arrived
            Console.WriteLine("RECV#{0}", cb.allMessage)
        ElseIf (cb.command.StartsWith("_")) Then
            ' Begin with '_' : Event's arrived
            Console.WriteLine("EVNT#{0}", cb.allMessage)
        ElseIf (cb.to.Equals(stars.nodeName)) Then
            ' Command Request's arrived, to nodename
            Console.WriteLine("RECV#{0}", cb.allMessage + "#")
            If (cb.Message.Equals("hello")) Then
                sendbuf = cb.from + " @" + cb.Message + " hello nice to meet you"
                stars.Send(sendbuf)
                Console.WriteLine("RPLY#" + sendbuf)
            ElseIf (cb.Message.Equals("help")) Then
                sendbuf = cb.from + " @" + cb.Message + " hello help"
                stars.Send(sendbuf)
                Console.WriteLine("RPLY#" + sendbuf)
            Else
                sendbuf = cb.from + " @" + cb.Message + " Er: Bad command or parameter."
                stars.Send(sendbuf)
                Console.WriteLine("RPLY#" + sendbuf)
            End If
        Else
            ' Command Request's arrived, to nodename.XXXX... maybe
            Console.WriteLine("RECV#{0}", cb.allMessage + "#")
            sendbuf = cb.from + " @" + cb.Message + " Er: " + cb.to + " is down."
   	        stars.Send(sendbuf)
            Console.WriteLine("RPLY#" + sendbuf)
        End If
    End Sub
End Module
