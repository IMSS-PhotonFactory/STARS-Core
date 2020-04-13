<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'フォームがコンポーネントの一覧をクリーンアップするために dispose をオーバーライドします。
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing AndAlso components IsNot Nothing Then
            components.Dispose()
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Windows フォーム デザイナで必要です。
    Private components As System.ComponentModel.IContainer

    'メモ: 以下のプロシージャは Windows フォーム デザイナで必要です。
    'Windows フォーム デザイナを使用して変更できます。  
    'コード エディタを使って変更しないでください。
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.txtFilename = New System.Windows.Forms.TextBox
        Me.cbWrite2File = New System.Windows.Forms.CheckBox
        Me.lbGuideMessageLog = New System.Windows.Forms.Label
        Me.txtLog = New System.Windows.Forms.TextBox
        Me.btLogClear = New System.Windows.Forms.Button
        Me.lbReply = New System.Windows.Forms.Label
        Me.cbSend = New System.Windows.Forms.ComboBox
        Me.lbGuideSend = New System.Windows.Forms.Label
        Me.btSend = New System.Windows.Forms.Button
        Me.SuspendLayout()
        '
        'txtFilename
        '
        Me.txtFilename.Location = New System.Drawing.Point(17, 285)
        Me.txtFilename.MaxLength = 8200
        Me.txtFilename.Name = "txtFilename"
        Me.txtFilename.ScrollBars = System.Windows.Forms.ScrollBars.Both
        Me.txtFilename.Size = New System.Drawing.Size(441, 21)
        Me.txtFilename.TabIndex = 35
        '
        'cbWrite2File
        '
        Me.cbWrite2File.AutoSize = True
        Me.cbWrite2File.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.cbWrite2File.Location = New System.Drawing.Point(14, 260)
        Me.cbWrite2File.Name = "cbWrite2File"
        Me.cbWrite2File.Size = New System.Drawing.Size(110, 19)
        Me.cbWrite2File.TabIndex = 34
        Me.cbWrite2File.Text = "Writelog to File:"
        Me.cbWrite2File.UseVisualStyleBackColor = True
        '
        'lbGuideMessageLog
        '
        Me.lbGuideMessageLog.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.lbGuideMessageLog.ForeColor = System.Drawing.SystemColors.ControlText
        Me.lbGuideMessageLog.Location = New System.Drawing.Point(14, 94)
        Me.lbGuideMessageLog.Name = "lbGuideMessageLog"
        Me.lbGuideMessageLog.Size = New System.Drawing.Size(177, 19)
        Me.lbGuideMessageLog.TabIndex = 33
        Me.lbGuideMessageLog.Text = "Message Log"
        '
        'txtLog
        '
        Me.txtLog.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.txtLog.ForeColor = System.Drawing.SystemColors.HotTrack
        Me.txtLog.Location = New System.Drawing.Point(17, 116)
        Me.txtLog.MaxLength = 8200
        Me.txtLog.Multiline = True
        Me.txtLog.Name = "txtLog"
        Me.txtLog.ReadOnly = True
        Me.txtLog.ScrollBars = System.Windows.Forms.ScrollBars.Both
        Me.txtLog.Size = New System.Drawing.Size(442, 129)
        Me.txtLog.TabIndex = 30
        '
        'btLogClear
        '
        Me.btLogClear.Location = New System.Drawing.Point(381, 92)
        Me.btLogClear.Name = "btLogClear"
        Me.btLogClear.Size = New System.Drawing.Size(75, 20)
        Me.btLogClear.TabIndex = 32
        Me.btLogClear.Text = "Clear Log"
        Me.btLogClear.UseVisualStyleBackColor = True
        '
        'lbReply
        '
        Me.lbReply.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.lbReply.ForeColor = System.Drawing.SystemColors.HotTrack
        Me.lbReply.Location = New System.Drawing.Point(15, 59)
        Me.lbReply.Name = "lbReply"
        Me.lbReply.Size = New System.Drawing.Size(444, 19)
        Me.lbReply.TabIndex = 31
        Me.lbReply.Text = "Recent Reply displayed here."
        '
        'cbSend
        '
        Me.cbSend.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.cbSend.FormattingEnabled = True
        Me.cbSend.Items.AddRange(New Object() {"System hello", "System listnodes"})
        Me.cbSend.Location = New System.Drawing.Point(14, 30)
        Me.cbSend.MaxLength = 80
        Me.cbSend.Name = "cbSend"
        Me.cbSend.Size = New System.Drawing.Size(356, 23)
        Me.cbSend.TabIndex = 29
        '
        'lbGuideSend
        '
        Me.lbGuideSend.AutoSize = True
        Me.lbGuideSend.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.lbGuideSend.ForeColor = System.Drawing.SystemColors.ControlText
        Me.lbGuideSend.Location = New System.Drawing.Point(12, 9)
        Me.lbGuideSend.Name = "lbGuideSend"
        Me.lbGuideSend.Size = New System.Drawing.Size(124, 15)
        Me.lbGuideSend.TabIndex = 28
        Me.lbGuideSend.Text = "Input stars message."
        '
        'btSend
        '
        Me.btSend.Location = New System.Drawing.Point(381, 33)
        Me.btSend.Name = "btSend"
        Me.btSend.Size = New System.Drawing.Size(75, 20)
        Me.btSend.TabIndex = 27
        Me.btSend.Text = "Send"
        Me.btSend.UseVisualStyleBackColor = True
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(7.0!, 15.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(473, 324)
        Me.Controls.Add(Me.txtFilename)
        Me.Controls.Add(Me.cbWrite2File)
        Me.Controls.Add(Me.lbGuideMessageLog)
        Me.Controls.Add(Me.txtLog)
        Me.Controls.Add(Me.btLogClear)
        Me.Controls.Add(Me.lbReply)
        Me.Controls.Add(Me.cbSend)
        Me.Controls.Add(Me.lbGuideSend)
        Me.Controls.Add(Me.btSend)
        Me.Font = New System.Drawing.Font("Arial", 9.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Margin = New System.Windows.Forms.Padding(3, 4, 3, 4)
        Me.Name = "Form1"
        Me.Text = "Stars Terminal"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Private WithEvents txtFilename As System.Windows.Forms.TextBox
    Private WithEvents cbWrite2File As System.Windows.Forms.CheckBox
    Private WithEvents lbGuideMessageLog As System.Windows.Forms.Label
    Private WithEvents txtLog As System.Windows.Forms.TextBox
    Private WithEvents btLogClear As System.Windows.Forms.Button
    Private WithEvents lbReply As System.Windows.Forms.Label
    Private WithEvents cbSend As System.Windows.Forms.ComboBox
    Private WithEvents lbGuideSend As System.Windows.Forms.Label
    Private WithEvents btSend As System.Windows.Forms.Button

End Class
