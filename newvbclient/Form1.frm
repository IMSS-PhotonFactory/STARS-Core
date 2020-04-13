VERSION 5.00
Object = "{DEB3D9DA-3109-427F-8394-5B5CCCB1E014}#18.0#0"; "StarsInterface.ocx"
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   ScaleHeight     =   3195
   ScaleWidth      =   4680
   StartUpPosition =   3  'Windows ‚ÌŠù’è’l
   Begin StarsInterface.StarsControl StarsControl1 
      Left            =   180
      Top             =   120
      _ExtentX        =   873
      _ExtentY        =   873
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Form_Load()
    StarsControl1.Connect "<<ClientName>>", "<<StarsServer>>"
    Form1.Caption = "<<ClientName>>"
End Sub
Private Sub StarsControl1_Error(Message As String)
    MsgBox Message
End Sub
