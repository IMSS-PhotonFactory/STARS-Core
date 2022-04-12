VERSION 5.00
Object = "{248DD890-BB45-11CF-9ABC-0080C7E7B78D}#1.0#0"; "MSWINSCK.OCX"
Begin VB.UserControl StarsControl 
   ClientHeight    =   780
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   1695
   ClipControls    =   0   'False
   InvisibleAtRuntime=   -1  'True
   Picture         =   "StarsControl.ctx":0000
   ScaleHeight     =   780
   ScaleWidth      =   1695
   ToolboxBitmap   =   "StarsControl.ctx":030A
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   100
      Left            =   1080
      Top             =   0
   End
   Begin MSWinsockLib.Winsock Winsock1 
      Left            =   600
      Top             =   0
      _ExtentX        =   741
      _ExtentY        =   741
      _Version        =   393216
   End
End
Attribute VB_Name = "StarsControl"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = True
Const DEFPORT = 6057
Const DEFHOST = "localhost"

Public Port As Long
Public IsConnected As Boolean

Private PauseSend As Boolean
Private TerminalName As String
Private KeyFileName As String
Private ListCount As Long
Private InputBuffer As String


Event Connected(Message As String)
Event Disconnected()
Event CommandArrived(TermFrom As String, TermTo As String, Message As String)
Event ReplyArrived(TermFrom As String, TermTo As String, Message As String)
Event EventArrived(TermFrom As String, TermTo As String, Message As String)
Event Error(Message As String)
Public Sub Sleep(mileSeconds As Long)
    Module1.Sleep mileSeconds
End Sub

Public Sub Send(Message As String, Optional TermTo As String)
    Do While PauseSend
        Module1.Sleep 100
        DoEvents
    Loop
    If TermTo = Empty Then
        Winsock1.SendData Message & vbLf
    Else
        Winsock1.SendData TermTo & " " & Message & vbLf
    End If
    PauseSend = True
End Sub
Public Sub Disconnect()
    Dim Buff As String
    Winsock1.GetData Buff
    Winsock1.Close
    IsConnected = False
    RaiseEvent Disconnected
End Sub
Public Sub Connect(Tname As String, Optional Rhost As String = DEFHOST, Optional Rport As Long = DEFPORT, Optional Keyfile As String)
    Dim F                   'File Handle
    Dim KeyNumber As Long
    Dim Buff As String
    
    If Keyfile = Empty Then Keyfile = Tname & ".key"
    TerminalName = Tname
    KeyFileName = Keyfile
    
    F = FreeFile
    On Error Resume Next
    Open KeyFileName For Input As F
    If Err.Number > 0 Then
        RaiseEvent Error(Err.Description)
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0
    ListCount = 0
    Do Until EOF(F)
        Line Input #F, Buff
        ListCount = ListCount + 1
    Loop
    Close (F)
    Winsock1.RemoteHost = Rhost
    Winsock1.RemotePort = Rport
    Winsock1.Connect

End Sub

Private Sub Timer1_Timer()
    Timer1.Enabled = False
    HandleMessage
End Sub

Private Sub UserControl_Initialize()
    IsConnected = False
    PauseSend = False
End Sub

Private Sub Winsock1_DataArrival(ByVal bytesTotal As Long)
    Dim Buff As String
    Dim PeriodFlg As Boolean
    Dim messIndex As Long
    Dim messNumber As Long
    Dim F
    Dim Lp As Long
    
    'Add read strings to data buffer
    Winsock1.GetData Buff, vbString, bytesTotal
    InputBuffer = InputBuffer & Buff
    If InStr(1, Buff, Chr(10), vbTextCompare) < 1 Then Exit Sub
    
If Not IsConnected Then
    'Analyze message data
    If Right(InputBuffer, 1) = vbLf Then PeriodFlg = True Else PeriodFlg = False
    dMessage = Split(InputBuffer, vbLf)
    messNumber = UBound(dMessage)
    If PeriodFlg Then
        InputBuffer = ""
    Else
        InputBuffer = dMessage(messNumber)
        messNumber = messNumber - 1
    End If

        'Connection request was refused
        Buff = dMessage(0)
        If InStr(1, Buff, "Bad host", vbTextCompare) >= 1 Then
            Disconnect
            RaiseEvent Error(Buff)
            Exit Sub
        ElseIf InStr(1, Buff, "Er:", vbTextCompare) >= 1 Then
            Disconnect
            RaiseEvent Error(Buff)
            Exit Sub
        ElseIf InStr(1, Buff, "Ok:", vbTextCompare) >= 1 Then
            IsConnected = True
            RaiseEvent Connected(Buff)
            Exit Sub
        End If
        
        'Send terminal name and keyword
        messIndex = Val(Buff)
        messIndex = messIndex Mod ListCount
        F = FreeFile
        On Error Resume Next
        Open KeyFileName For Input As F
        If Err.Number > 0 Then
            RaiseEvent Error(Err.Description)
            On Error GoTo 0
            Exit Sub
        End If
        On Error GoTo 0
        For Lp = 1 To messIndex
            Line Input #F, Buff
        Next Lp
        Line Input #F, Buff
        Close (F)
        Send TerminalName & " " & Buff
        Exit Sub
End If
    
'Handle messages
    HandleMessage
'    For messIndex = 0 To messNumber - 1
'        Buff = dMessage(messIndex)
'        HandleMessage Buff
'    Next messIndex

End Sub
Private Sub HandleMessage()
    Dim TermFrom As String
    Dim TermTo As String
    Dim rMessage As String
    Dim Place As Long
    Dim MessBuff As String

Do
'Get Message from InputBuffer
    Place = InStr(InputBuffer, vbLf)
    If Place < 1 Then Exit Sub
    MessBuff = Left(InputBuffer, Place - 1)
'Pars MessBuff
    dMessage = Split(MessBuff)
    dTerm = Split(dMessage(0), ">")
    TermFrom = dTerm(0)
    TermTo = dTerm(1)
    dMessage(0) = ""
    rMessage = Join(dMessage, " ")
    rMessage = Trim(rMessage)
'Try Raise Event
    If UserControl.EventsFrozen Then
        Timer1.Enabled = True
        Exit Sub
    End If

    Select Case Left(rMessage, 1)
        Case "_": RaiseEvent EventArrived(TermFrom, TermTo, rMessage)
        Case "@": RaiseEvent ReplyArrived(TermFrom, TermTo, rMessage)
        Case Else: RaiseEvent CommandArrived(TermFrom, TermTo, rMessage)
    End Select
'Shift buffer
    InputBuffer = Mid(InputBuffer, Place + 1)

Loop

End Sub
Private Sub Winsock1_Error(ByVal Number As Integer, Description As String, ByVal Scode As Long, ByVal Source As String, ByVal HelpFile As String, ByVal HelpContext As Long, CancelDisplay As Boolean)
    Dim Buff As String
    Select Case Number
    Case 10053
'        Winsock1.GetData Buff
        Winsock1.Close
        IsConnected = False
        RaiseEvent Disconnected
    Case 10061
        Winsock1.Close
        RaiseEvent Error("Er:" & Str(Number) & Description)
    Case Else
        RaiseEvent Error("Er:" & Str(Number) & Description)
    End Select
End Sub

Private Sub Winsock1_SendComplete()
    PauseSend = False
End Sub
