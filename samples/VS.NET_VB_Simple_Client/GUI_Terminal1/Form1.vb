Public Class Form1
    Public stars As STARS.StarsInterface

    '
    ' Form START!!
    '
    Public Sub New()
        ' この呼び出しは、Windows フォーム デザイナで必要です。
        InitializeComponent()
        ' InitializeComponent() 呼び出しの後で初期化を追加します。

        If (connect2stars() = False) Then Exit Sub ' Calling connecting stars.
    End Sub

    '
    ' Connecting Stars.
    '
    Private Function connect2stars() As Boolean
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
            MessageBox.Show(se.Message)
            Return False
        End Try

        ' Step2. Add the stars handler named 'stars_received' which is called when arriving stars messages.
        Dim cbStars As STARS.WinForm.StarsCbWinForm = New STARS.WinForm.StarsCbWinForm(Me, stars)
        cbStars.StartCbHandler(New STARS.StarsCbHandler(AddressOf stars_received))
        Return True

    End Function

    '
    ' Stars Message Arrived.
    '
    Private Sub stars_received(ByVal sender As Object, ByVal ev As STARS.StarsCbArgs)
        Dim mess As String

        If (ev.Message.Trim.Equals("")) Then
            ' No Message
            txtLog_update(ev.allMessage)
            logFile_update(ev.allMessage)
            mess = ev.from + " @" + ev.Message + " Er: Bad command."
            stars.Send(mess)
            txtLog_update(mess)
            logFile_update(mess)
        ElseIf (ev.command.StartsWith("@")) Then
            ' Begin with '@' : Reply's arrived
            lbReply_update(ev.allMessage)
            txtLog_update(ev.allMessage)
            logFile_update(ev.allMessage)
        ElseIf (ev.command.StartsWith("_")) Then
            ' Begin with '_' : Event's arrived
            txtLog_update(ev.allMessage)
            logFile_update(ev.allMessage)
        ElseIf (ev.to.Equals(stars.nodeName)) Then
            ' Command Request's arrived, to nodename
            txtLog_update(ev.allMessage)
            logFile_update(ev.allMessage)
            If (ev.Message.Equals("hello")) Then
                mess = ev.from + " @" + ev.Message + " hello nice to meet you."
            ElseIf (ev.Message.Equals("help")) Then
                mess = ev.from + " @" + ev.Message + " hello help."
            Else
                mess = ev.from + " @" + ev.Message + " Er: Bad command or parameter."
            End If
            stars.Send(mess)
            txtLog_update(mess)
            logFile_update(mess)
        Else
            ' Command Request's arrived, to nodename.XXXX... maybe
            txtLog_update(ev.allMessage)
            logFile_update(ev.allMessage)
            mess = ev.from + " @" + ev.Message + " Er: " + ev.to + " is down."
            stars.Send(mess)
            txtLog_update(mess)
            logFile_update(mess)
        End If
    End Sub

    '
    ' Send Message with send button click
    '
    Private Sub btSend_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btSend.Click
        Dim mess As String
        Dim si As Integer
        mess = cbSend.Text
        If (mess.Trim.Equals("")) Then Exit Sub

        txtLog_update(mess)
        logFile_update(mess)
        lbReply_update("")

        Try
            stars.Send(mess)
        Catch se As Exception
            MessageBox.Show(se.Message)
            Me.Close()
        End Try

        si = cbSend.FindString(mess, -1)
        If (si < 0) Then
            cbSend.Items.Add(mess)
        Else
            cbSend.Items.RemoveAt(si)
            cbSend.Items.Add(mess)
            cbSend.SelectedItem = mess
        End If

    End Sub

    '
    ' Clear LogArea with clear log button click
    '
    Private Sub btLogClear_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btLogClear.Click
        txtLog.Text = ""
    End Sub

    '
    ' Start write Log to file with checkbox click.
    '
    Private Sub cbWrite2File_Click(ByVal sender As Object, ByVal e As EventArgs) Handles cbWrite2File.Click
        If (cbWrite2File.Checked = True) Then
            txtFilename.ReadOnly = False
            If (txtFilename.Text.Trim().Equals("")) Then
                txtFilename.Text = Application.StartupPath + "\\log" + String.Format("{0:yyyyMMdd}", DateTime.Now) + ".txt"
            End If
            txtFilename.ReadOnly = True
        Else
            txtFilename.ReadOnly = False
        End If
    End Sub

    '
    ' Sub routine reflesh reply text field.
    '
    Private Sub lbReply_update(ByVal message As String)
        lbReply.Text = message
    End Sub

    '
    ' Sub routine reflesh log text field
    '
    Private Sub txtLog_update(ByVal message As String)
        Dim pos As Integer
        pos = txtLog.Text.Length + message.Length + System.Environment.NewLine.Length - txtLog.MaxLength
        If (pos > 0) Then
            pos = txtLog.Text.IndexOf(System.Environment.NewLine, pos)
            If (pos > -1) Then
                Dim buf As String
                buf = txtLog.Text.Substring(pos + System.Environment.NewLine.Length, _
                        txtLog.Text.Length - pos - System.Environment.NewLine.Length) _
                      + message + System.Environment.NewLine
                txtLog.Clear()
                txtLog.AppendText(buf)
            Else
                txtLog.Clear()
                txtLog.AppendText(message + System.Environment.NewLine)
            End If
        Else
            txtLog.AppendText(message + System.Environment.NewLine)
        End If
    End Sub

    '
    ' Sub routine write2logfile
    '
    Private Sub logFile_update(ByVal message As String)
        If (cbWrite2File.Checked = False) Then Exit Sub

        If (txtFilename.Text.Trim().Equals("")) Then
            cbWrite2File.Checked = False
            Exit Sub
        End If

        Dim now As DateTime
        Dim writer As System.IO.StreamWriter

        now = DateTime.Now
        Try
            writer = New System.IO.StreamWriter(txtFilename.Text, True)
            writer.WriteLine(message)
            writer.Close()
        Catch e As Exception
            cbWrite2File.Checked = False
            txtLog_update("Log Write Error!")
            txtLog_update(e.Message)
            txtFilename.ReadOnly = False
            Return
        End Try
    End Sub

    '
    ' Sub routine reflesh numbers of log character
    '
    Private Sub txtLog_TextChanged(ByVal sender As Object, ByVal e As EventArgs)
        lbGuideMessageLog.Text = "Message Log (" + txtLog.Text.Length + " character)"
    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

    End Sub
End Class