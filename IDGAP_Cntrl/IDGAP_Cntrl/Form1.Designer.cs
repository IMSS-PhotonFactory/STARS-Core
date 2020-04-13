namespace IDGAP_Cntrl
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナ変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージ リソースが破棄される場合 true、破棄されない場合は false です。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナで生成されたコード

        /// <summary>
        /// デザイナ サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディタで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.labelGapPresent = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.txtDestination = new System.Windows.Forms.TextBox();
            this.btnSetValue = new System.Windows.Forms.Button();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.labelStatus = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.labelTprPresent = new System.Windows.Forms.Label();
            this.lblTprPresent = new System.Windows.Forms.Label();
            this.btnTprSetValue = new System.Windows.Forms.Button();
            this.txtTprDestination = new System.Windows.Forms.TextBox();
            this.lblGapPresent = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // labelGapPresent
            // 
            this.labelGapPresent.Location = new System.Drawing.Point(9, 28);
            this.labelGapPresent.Name = "labelGapPresent";
            this.labelGapPresent.Size = new System.Drawing.Size(84, 12);
            this.labelGapPresent.TabIndex = 1;
            this.labelGapPresent.Text = "Gap Present";
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(335, 30);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(31, 12);
            this.label2.TabIndex = 2;
            this.label2.Text = "mm";
            // 
            // txtDestination
            // 
            this.txtDestination.Location = new System.Drawing.Point(92, 24);
            this.txtDestination.Name = "txtDestination";
            this.txtDestination.Size = new System.Drawing.Size(57, 19);
            this.txtDestination.TabIndex = 3;
            this.txtDestination.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // btnSetValue
            // 
            this.btnSetValue.Location = new System.Drawing.Point(159, 25);
            this.btnSetValue.Name = "btnSetValue";
            this.btnSetValue.Size = new System.Drawing.Size(60, 19);
            this.btnSetValue.TabIndex = 4;
            this.btnSetValue.Text = "Set";
            this.btnSetValue.UseVisualStyleBackColor = true;
            this.btnSetValue.Click += new System.EventHandler(this.btnSetValue_Click);
            // 
            // timer1
            // 
            this.timer1.Interval = 3000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // labelStatus
            // 
            this.labelStatus.Location = new System.Drawing.Point(11, 113);
            this.labelStatus.Multiline = true;
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.ReadOnly = true;
            this.labelStatus.Size = new System.Drawing.Size(349, 48);
            this.labelStatus.TabIndex = 5;
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(335, 80);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(31, 12);
            this.label3.TabIndex = 8;
            this.label3.Text = "mm";
            // 
            // labelTprPresent
            // 
            this.labelTprPresent.Location = new System.Drawing.Point(9, 76);
            this.labelTprPresent.Name = "labelTprPresent";
            this.labelTprPresent.Size = new System.Drawing.Size(84, 12);
            this.labelTprPresent.TabIndex = 7;
            this.labelTprPresent.Text = "Tpr Present";
            // 
            // lblTprPresent
            // 
            this.lblTprPresent.Font = new System.Drawing.Font("MS UI Gothic", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblTprPresent.Location = new System.Drawing.Point(213, 65);
            this.lblTprPresent.Name = "lblTprPresent";
            this.lblTprPresent.Size = new System.Drawing.Size(120, 38);
            this.lblTprPresent.TabIndex = 6;
            this.lblTprPresent.Text = "N/A";
            this.lblTprPresent.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // btnTprSetValue
            // 
            this.btnTprSetValue.Location = new System.Drawing.Point(159, 75);
            this.btnTprSetValue.Name = "btnTprSetValue";
            this.btnTprSetValue.Size = new System.Drawing.Size(60, 19);
            this.btnTprSetValue.TabIndex = 10;
            this.btnTprSetValue.Text = "Set";
            this.btnTprSetValue.UseVisualStyleBackColor = true;
            this.btnTprSetValue.Click += new System.EventHandler(this.btnTprSetValue_Click);
            // 
            // txtTprDestination
            // 
            this.txtTprDestination.Location = new System.Drawing.Point(92, 73);
            this.txtTprDestination.Name = "txtTprDestination";
            this.txtTprDestination.Size = new System.Drawing.Size(57, 19);
            this.txtTprDestination.TabIndex = 9;
            this.txtTprDestination.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // lblGapPresent
            // 
            this.lblGapPresent.Font = new System.Drawing.Font("MS UI Gothic", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.lblGapPresent.Location = new System.Drawing.Point(213, 14);
            this.lblGapPresent.Name = "lblGapPresent";
            this.lblGapPresent.Size = new System.Drawing.Size(120, 38);
            this.lblGapPresent.TabIndex = 0;
            this.lblGapPresent.Text = "N/A";
            this.lblGapPresent.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(372, 173);
            this.Controls.Add(this.labelStatus);
            this.Controls.Add(this.btnTprSetValue);
            this.Controls.Add(this.txtTprDestination);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.labelTprPresent);
            this.Controls.Add(this.lblTprPresent);
            this.Controls.Add(this.btnSetValue);
            this.Controls.Add(this.txtDestination);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.labelGapPresent);
            this.Controls.Add(this.lblGapPresent);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelGapPresent;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txtDestination;
        private System.Windows.Forms.Button btnSetValue;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.TextBox labelStatus;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label labelTprPresent;
        private System.Windows.Forms.Label lblTprPresent;
        private System.Windows.Forms.Button btnTprSetValue;
        private System.Windows.Forms.TextBox txtTprDestination;
        private System.Windows.Forms.Label lblGapPresent;
    }
}

