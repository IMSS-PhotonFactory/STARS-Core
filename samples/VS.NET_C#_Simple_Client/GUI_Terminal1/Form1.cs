using System;
//using System.Collections.Generic;
//using System.ComponentModel;
//using System.Data;
//using System.Drawing;
//using System.Text;
using System.Windows.Forms;
using System.IO;
using STARS;
using STARS.WinForm;

namespace GUI_Terminal1
{
    /// <summary>
    /// Form1 Class
    /// </summary>
    public partial class Form1 : Form
    {
        /// <summary>This field is a stars interface.</summary>
        public StarsInterface stars;

        /// <summary>
        /// Form1 Initialized here.
        /// </summary>
        public Form1()
        {
            InitializeComponent();
        }

        /// <summary>Start Stars Connection here.</summary>
        /// <seealso cref="stars_received"/>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Form1_Load(object sender, EventArgs e)
        {
            string[] starsargs = new string[] { "csterm", "localhost" };
            string[] cmds;

            // Check Program Parameters
            cmds = System.Environment.GetCommandLineArgs();
            if (cmds.Length >= 3)
            {
                starsargs[1] = cmds[2];
                starsargs[0] = cmds[1];
            }
            else if (cmds.Length == 2)
            {
                starsargs[0] = cmds[1];
            }


            // Step1. Connect to Stars.
            stars = new StarsInterface(starsargs[0], starsargs[1]);
            try
            {
                stars.Connect();
            }
            catch (Exception se)
            {
                MessageBox.Show(se.Message);
                this.Close();
                return;
            }

            // Step2. Add the stars handler named 'stars_received' which is called when arriving stars messages.
            StarsCbWinForm cbStars = new StarsCbWinForm(this, stars);
            cbStars.StartCbHandler(new StarsCbHandler(stars_received));

        }

        /// <summary>This method is called when arriving stars messages.</summary>
        /// <param name="sender"></param>
        /// <param name="ev">Used to access the Stars object which contains received data.</param>
        /// <seealso cref="Form1_Load"/>
        private void stars_received(object sender, StarsCbArgs ev)
        {
            // Begin with '@' : Reply's arrived
            // No Message
            if (ev.Message.Trim() == "")
            {
                String mess;
                txtLog_update(ev.allMessage);
                logFile_update(ev.allMessage);
                mess = ev.from + " @" + ev.Message + " Er: Bad command.";
                stars.Send(mess);
                txtLog_update(mess);
                logFile_update(mess);
            }
            else if (ev.command[0] == '@')
            {
                lbReply_update(ev.allMessage);
                txtLog_update(ev.allMessage);
                logFile_update(ev.allMessage);
                // Begin with '_' : Event's arrived
            }else if(ev.command[0] == '_'){
                txtLog_update(ev.allMessage);
                logFile_update(ev.allMessage);
                // Command Request's arrived, to nodename
            }
            else if (ev.to == stars.nodeName)
            {
                String mess;
                txtLog_update(ev.allMessage);
                logFile_update(ev.allMessage);
                switch (ev.Message)
                {
                    case "hello":
                        mess = ev.from + " @" + ev.Message + " hello nice to meet you.";
                        break;
                    case "help":
                        mess = ev.from + " @" + ev.Message + " hello help.";
                        break;
                    default:
                        mess = ev.from + " @" + ev.Message + " Er: Bad command or parameter.";
                        break;
                }
                stars.Send(mess);
                txtLog_update(mess);
                logFile_update(mess);
            // Command Request's arrived, to nodename.XXXX... maybe
            } else
            {
                String mess;
                txtLog_update(ev.allMessage);
                logFile_update(ev.allMessage);
                mess = ev.from + " @" + ev.Message + " Er: " + ev.to + " is down.";
                stars.Send(mess);
                txtLog_update(mess);
                logFile_update(mess);
            }
            return;
        }


        /// <summary>Send button click method</summary>
        private void btSend_Click(object sender, EventArgs e)
        {
            String mess;
            mess = cbSend.Text;
            if (mess.Trim() == "")
            {
                return;
            }
            txtLog_update(mess);
            logFile_update(mess);
            lbReply_update("");
            stars.Send(mess);
            int si = cbSend.FindString(mess,-1);
            if (si < 0)
            {
                cbSend.Items.Add(mess);
            }
            else
            {
                cbSend.Items.RemoveAt(si);
                cbSend.Items.Add(mess);
                cbSend.SelectedItem = mess;
            }
        }

        /// <summary>Clear button click method</summary>
        private void btLogClear_Click(object sender, EventArgs e)
        {
            txtLog.Text = "";
        }

        /// <summary>Writetolog checkbox click method</summary>
        private void cbWrite2File_Click(object sender, EventArgs e)
        {
            if (cbWrite2File.Checked == true)
            {
                txtFilename.ReadOnly = false;
                if (txtFilename.Text.Trim() == "")
                {
                    txtFilename.Text = Application.StartupPath + "\\log" + String.Format("{0:yyyyMMdd}", DateTime.Now) + ".txt";
                }
            }
            else
            {
                txtFilename.ReadOnly = true;
            }
        }

        // reflesh reply field text
        private void lbReply_update(string message)
        {
            lbReply.Text = message;
        }

        // reflesh log display field text
        private void txtLog_update(string message)
        {
            int pos;
            pos = txtLog.Text.Length + message.Length + System.Environment.NewLine.Length - txtLog.MaxLength;
            if(pos > 0)
            {
                pos = txtLog.Text.IndexOf(System.Environment.NewLine, pos);
                if(pos > -1)
                {
                    String buf;
                    buf=txtLog.Text.Substring(pos + System.Environment.NewLine.Length,
                        txtLog.Text.Length - pos - System.Environment.NewLine.Length)
                             + message + System.Environment.NewLine;
                    txtLog.Clear();
                    txtLog.AppendText(buf);

                }else{
                    txtLog.Clear();
                    txtLog.AppendText(message + System.Environment.NewLine);
                }
            }
            else
            {
                txtLog.AppendText(message + System.Environment.NewLine);
            }
        }

        // reflesh numbers of log character
        private void txtLog_TextChanged(object sender, EventArgs e)
        {
            lbGuideMessageLog.Text = "Message Log (" + txtLog.Text.Length + " character)";
        }

        // write2logfile
        private void logFile_update(string message)
        {
            if (cbWrite2File.Checked == false)
            {
                return;
            }
            if (txtFilename.Text.Trim() == "")
            {
                cbWrite2File.Checked = false;
                return;
            }
            DateTime now = DateTime.Now;
            StreamWriter writer = null;
            try
            {
                writer = new StreamWriter(txtFilename.Text,true);
                writer.WriteLine(message);
                writer.Close();
            }
            catch (Exception e)
            {
                cbWrite2File.Checked = false;
                txtLog_update("Log Write Error!");
                txtLog_update(e.Message);
                txtFilename.ReadOnly = true;
                return;
            }
        }
    }
}

