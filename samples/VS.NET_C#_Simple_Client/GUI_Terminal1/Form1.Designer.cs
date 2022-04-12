namespace GUI_Terminal1
{
    partial class Form1
    {
        /// <summary>
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// </summary>
        /// <param name="disposing">manage resource dispose true not false</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer Generates Code

        /// <summary>
        /// </summary>
        private void InitializeComponent()
        {
            System.Windows.Forms.Label lbGuideSend;
            this.cbSend = new System.Windows.Forms.ComboBox();
            this.btSend = new System.Windows.Forms.Button();
            this.lbReply = new System.Windows.Forms.Label();
            this.txtLog = new System.Windows.Forms.TextBox();
            this.btLogClear = new System.Windows.Forms.Button();
            this.lbGuideMessageLog = new System.Windows.Forms.Label();
            this.cbWrite2File = new System.Windows.Forms.CheckBox();
            this.txtFilename = new System.Windows.Forms.TextBox();
            lbGuideSend = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lbGuideSend
            // 
            lbGuideSend.AutoSize = true;
            lbGuideSend.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            lbGuideSend.ForeColor = System.Drawing.SystemColors.ControlText;
            lbGuideSend.Location = new System.Drawing.Point(10, 10);
            lbGuideSend.Name = "lbGuideSend";
            lbGuideSend.Size = new System.Drawing.Size(124, 15);
            lbGuideSend.TabIndex = 2;
            lbGuideSend.Text = "Input stars message.";
            // 
            // cbSend
            // 
            this.cbSend.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbSend.FormattingEnabled = true;
            this.cbSend.Items.AddRange(new object[] {
            "System hello",
            "System listnodes"});
            this.cbSend.Location = new System.Drawing.Point(12, 31);
            this.cbSend.MaxLength = 80;
            this.cbSend.Name = "cbSend";
            this.cbSend.Size = new System.Drawing.Size(356, 23);
            this.cbSend.TabIndex = 17;
            // 
            // btSend
            // 
            this.btSend.Location = new System.Drawing.Point(379, 34);
            this.btSend.Name = "btSend";
            this.btSend.Size = new System.Drawing.Size(75, 20);
            this.btSend.TabIndex = 0;
            this.btSend.Text = "Send";
            this.btSend.UseVisualStyleBackColor = true;
            this.btSend.Click += new System.EventHandler(this.btSend_Click);
            // 
            // lbReply
            // 
            this.lbReply.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbReply.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.lbReply.Location = new System.Drawing.Point(13, 60);
            this.lbReply.Name = "lbReply";
            this.lbReply.Size = new System.Drawing.Size(444, 19);
            this.lbReply.TabIndex = 19;
            this.lbReply.Text = "Recent Reply displayed here.";
            // 
            // txtLog
            // 
            this.txtLog.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtLog.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.txtLog.Location = new System.Drawing.Point(15, 117);
            this.txtLog.MaxLength = 8200;
            this.txtLog.Multiline = true;
            this.txtLog.Name = "txtLog";
            this.txtLog.ReadOnly = true;
            this.txtLog.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtLog.Size = new System.Drawing.Size(442, 129);
            this.txtLog.TabIndex = 18;
            this.txtLog.TextChanged += new System.EventHandler(this.txtLog_TextChanged);
            // 
            // btLogClear
            // 
            this.btLogClear.Location = new System.Drawing.Point(379, 93);
            this.btLogClear.Name = "btLogClear";
            this.btLogClear.Size = new System.Drawing.Size(75, 20);
            this.btLogClear.TabIndex = 23;
            this.btLogClear.Text = "Clear Log";
            this.btLogClear.UseVisualStyleBackColor = true;
            this.btLogClear.Click += new System.EventHandler(this.btLogClear_Click);
            // 
            // lbGuideMessageLog
            // 
            this.lbGuideMessageLog.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbGuideMessageLog.ForeColor = System.Drawing.SystemColors.ControlText;
            this.lbGuideMessageLog.Location = new System.Drawing.Point(12, 95);
            this.lbGuideMessageLog.Name = "lbGuideMessageLog";
            this.lbGuideMessageLog.Size = new System.Drawing.Size(177, 19);
            this.lbGuideMessageLog.TabIndex = 24;
            this.lbGuideMessageLog.Text = "Message Log";
            // 
            // cbWrite2File
            // 
            this.cbWrite2File.AutoSize = true;
            this.cbWrite2File.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbWrite2File.Location = new System.Drawing.Point(12, 261);
            this.cbWrite2File.Name = "cbWrite2File";
            this.cbWrite2File.Size = new System.Drawing.Size(110, 19);
            this.cbWrite2File.TabIndex = 25;
            this.cbWrite2File.Text = "Writelog to File:";
            this.cbWrite2File.UseVisualStyleBackColor = true;
            this.cbWrite2File.Click += new System.EventHandler(this.cbWrite2File_Click);
            // 
            // txtFilename
            // 
            this.txtFilename.Location = new System.Drawing.Point(15, 286);
            this.txtFilename.MaxLength = 8200;
            this.txtFilename.Name = "txtFilename";
            this.txtFilename.ReadOnly = true;
            this.txtFilename.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtFilename.Size = new System.Drawing.Size(441, 19);
            this.txtFilename.TabIndex = 26;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(463, 311);
            this.Controls.Add(this.txtFilename);
            this.Controls.Add(this.cbWrite2File);
            this.Controls.Add(this.lbGuideMessageLog);
            this.Controls.Add(this.txtLog);
            this.Controls.Add(this.btLogClear);
            this.Controls.Add(this.lbReply);
            this.Controls.Add(this.cbSend);
            this.Controls.Add(lbGuideSend);
            this.Controls.Add(this.btSend);
            this.Name = "Form1";
            this.Text = "Stars Terminal";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox cbSend;
        private System.Windows.Forms.Button btSend;
        private System.Windows.Forms.Label lbReply;
        private System.Windows.Forms.TextBox txtLog;
        private System.Windows.Forms.Button btLogClear;
        private System.Windows.Forms.Label lbGuideMessageLog;
        private System.Windows.Forms.CheckBox cbWrite2File;
        private System.Windows.Forms.TextBox txtFilename;
    }
}

