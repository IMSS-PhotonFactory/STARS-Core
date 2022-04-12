Imports System.Configuration
Imports STARS
Imports STARS.WinForm

Public Class Form1
    Private stars As StarsInterface
    Private myNodeName As String
    Private starsServerName As String
    Private keyFileName As String
    Private starsPort As Integer


    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

        ' Load settings
        ' Settings are written in app.config file.
        myNodeName = ConfigurationManager.AppSettings("myNodeName")
        starsServerName = ConfigurationManager.AppSettings("starsServerName")
        keyFileName = ConfigurationManager.AppSettings("keyFileName")
        starsPort = System.Convert.ToInt32(ConfigurationManager.AppSettings("starsPort"))

        ' Connect to Stars.
        stars = New StarsInterface(myNodeName, starsServerName, keyFileName, starsPort)
        Try
            stars.Connect()
        Catch ex As Exception
            MessageBox.Show(ex.Message)
            Me.Close()
            Exit Sub
        End Try

        ' Send STARS message "System gettime".
        stars.Send("System gettime")

        ' Get reply of system time from StarsServer and show it on messagebox.
        Dim rcvMesg As StarsMessage = stars.Receive()
        MessageBox.Show("Reply by using ReceiveMethod: " + rcvMesg.allMessage)

        ' Add the stars handler named 'handler' which is called when arriving stars messages.
        Dim cb As StarsCbHandler = New StarsCbHandler(AddressOf handler)
        Dim cbStars As StarsCbWinForm = New StarsCbWinForm(Me, stars)

        ' If callback mode started,  don't use stars.Receive() function.
        cbStars.StartCbHandler(cb)

    End Sub

    Private Sub handler(ByVal sender As Object, ByVal ev As STARS.StarsCbArgs)
        ' Receiving Stars message by callback mode. Show reply at messagebox.
        MessageBox.Show("Reply via callback: " + ev.allMessage)
        Exit Sub
    End Sub
End Class
