VERSION 5.00
Object = "{DEB3D9DA-3109-427F-8394-5B5CCCB1E014}#18.0#0"; "StarsInterface.ocx"
Begin VB.Form Main 
   Caption         =   "STARS Sample"
   ClientHeight    =   5085
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   7695
   LinkTopic       =   "Form1"
   ScaleHeight     =   5085
   ScaleWidth      =   7695
   StartUpPosition =   3  'Windows ÇÃä˘íËíl
   Begin VB.TextBox Send_Txt 
      BackColor       =   &H8000000B&
      Height          =   270
      Left            =   3240
      TabIndex        =   15
      Top             =   1080
      Width           =   4095
   End
   Begin VB.TextBox To_Txt 
      Height          =   270
      Left            =   4920
      TabIndex        =   11
      Text            =   "Text1"
      Top             =   3600
      Width           =   2415
   End
   Begin VB.TextBox From_Txt 
      Height          =   270
      Left            =   4920
      TabIndex        =   10
      Text            =   "Text1"
      Top             =   2760
      Width           =   2415
   End
   Begin VB.TextBox Event_Txt 
      Height          =   270
      Left            =   1680
      TabIndex        =   5
      Text            =   "Text3"
      Top             =   3000
      Width           =   2655
   End
   Begin VB.TextBox Command_Txt 
      Height          =   270
      Left            =   1680
      TabIndex        =   4
      Text            =   "Text2"
      Top             =   2400
      Width           =   2655
   End
   Begin VB.TextBox Reply_Txt 
      Height          =   270
      Left            =   1680
      TabIndex        =   3
      Text            =   "Text1"
      Top             =   3600
      Width           =   2655
   End
   Begin VB.TextBox Error_Txt 
      Height          =   270
      Left            =   1680
      TabIndex        =   1
      Text            =   "Text1"
      Top             =   4560
      Width           =   5655
   End
   Begin StarsInterface.StarsControl StarsControl1 
      Left            =   6720
      Top             =   240
      _ExtentX        =   873
      _ExtentY        =   873
   End
   Begin VB.CommandButton Send_Cmd 
      Caption         =   "Send"
      Height          =   495
      Left            =   720
      TabIndex        =   0
      Top             =   840
      Width           =   1935
   End
   Begin VB.Label Label8 
      BackColor       =   &H8000000B&
      BackStyle       =   0  'ìßñæ
      Caption         =   "Message To Send"
      Height          =   255
      Left            =   3240
      TabIndex        =   16
      Top             =   720
      Width           =   1815
   End
   Begin VB.Label Label7 
      Caption         =   "Send Message"
      BeginProperty Font 
         Name            =   "ÇlÇr ÇoÉSÉVÉbÉN"
         Size            =   12
         Charset         =   128
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   375
      Left            =   240
      TabIndex        =   14
      Top             =   240
      Width           =   1935
   End
   Begin VB.Label Label6 
      BackStyle       =   0  'ìßñæ
      Caption         =   "Receive Message"
      BeginProperty Font 
         Name            =   "ÇlÇr ÇoÉSÉVÉbÉN"
         Size            =   12
         Charset         =   128
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H000000FF&
      Height          =   375
      Left            =   240
      TabIndex        =   13
      Top             =   1800
      Width           =   2115
   End
   Begin VB.Label Label5 
      Caption         =   "tonode name"
      Height          =   255
      Index           =   1
      Left            =   4920
      TabIndex        =   12
      Top             =   3240
      Width           =   1695
   End
   Begin VB.Label Label5 
      Caption         =   "fromnode name"
      Height          =   255
      Index           =   0
      Left            =   4920
      TabIndex        =   9
      Top             =   2400
      Width           =   1695
   End
   Begin VB.Label Label4 
      Caption         =   "Reply Arrived"
      Height          =   255
      Left            =   60
      TabIndex        =   8
      Top             =   3600
      Width           =   1515
   End
   Begin VB.Label Label3 
      Caption         =   "Event Message Arrived"
      Height          =   375
      Left            =   60
      TabIndex        =   7
      Top             =   2940
      Width           =   1515
   End
   Begin VB.Label Label2 
      Caption         =   "Command Request Arrived"
      Height          =   435
      Left            =   60
      TabIndex        =   6
      Top             =   2340
      Width           =   1575
   End
   Begin VB.Line Line2 
      X1              =   120
      X2              =   7560
      Y1              =   1560
      Y2              =   1560
   End
   Begin VB.Line Line1 
      X1              =   120
      X2              =   7560
      Y1              =   4200
      Y2              =   4200
   End
   Begin VB.Label Label1 
      Caption         =   "Error Message Arrived"
      BeginProperty Font 
         Name            =   "ÇlÇr ÇoÉSÉVÉbÉN"
         Size            =   9.75
         Charset         =   128
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   240
      TabIndex        =   2
      Top             =   4500
      Width           =   1335
   End
End
Attribute VB_Name = "Main"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'     VB6 STARS Sample Program
'                                     2005.04.15 Made by Kazuyuki Nigorikawa
'                                     2006.01.24 Translated To English by Yasuko Nagatani
'
' # Checked on Project-Component-StarsInterface and
'   Place STARS ActiveX On Form
'


'èâä˙ê›íË
Private Sub Form_Load()
    'Connect To Stars Server
    'Specify NodeName And Stars Server location
    'Arguments
    'Nodename(String)ÅAStars Server Name(String)ÅAStars Server PortÅALocation Of key File(String)
    
 '   StarsControl1.Connect "Pappy1", "localhost", 6057, "c:\stars\sample\Pappy1.key"
    StarsControl1.Connect "Pappy1", "localhost", 6057

End Sub

Private Sub Send_Cmd_Click()

    Dim Send_Command  As String

    If Send_Txt.Text = "" Then
        Send_Command = "System hello"       'Default message [System hello]:Test Command For Access Stars Server
    Else
        Send_Command = Send_Txt.Text
    End If
    StarsControl1.Send Send_Command     'Send Action
    Send_Txt.Text = Send_Command
    
End Sub

'Command Request Arrived(Message neither start with @ or _)
Private Sub StarsControl1_CommandArrived(TermFrom As String, TermTo As String, Message As String)
    
    Command_Txt.Text = Message
    From_Txt.Text = TermFrom
    To_Txt.Text = TermTo

End Sub

'Event Message Arrived(Message start with _)
Private Sub StarsControl1_EventArrived(TermFrom As String, TermTo As String, Message As String)
    
    Event_Txt.Text = Message
    From_Txt.Text = TermFrom
    To_Txt.Text = TermTo

End Sub

'Reply Message Arrived(Message start with @)
Private Sub StarsControl1_ReplyArrived(TermFrom As String, TermTo As String, Message As String)
    
    Reply_Txt.Text = Message
    From_Txt.Text = TermFrom
    To_Txt.Text = TermTo

End Sub

'Error Arrived Sended By WinSock
Private Sub StarsControl1_Error(Message As String)
    
    Error_Txt.Text = Message

End Sub
