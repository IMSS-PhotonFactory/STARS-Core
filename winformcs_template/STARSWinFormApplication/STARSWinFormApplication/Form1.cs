using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Configuration;
using STARS;
using STARS.WinForm;


namespace STARSWinFormApplication
{
    public partial class Form1 : Form
    {

        private StarsInterface stars;
        private string myNodeName;
        private string starsServerName;
        private string keyFileName;
        private int starsPort;
        
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // LoadSettings
            // Settings are written in app.config file.
            myNodeName = ConfigurationManager.AppSettings["myNodeName"];
            starsServerName = ConfigurationManager.AppSettings["starsServerName"];
            keyFileName = ConfigurationManager.AppSettings["keyFileName"];
            starsPort = System.Convert.ToInt32(ConfigurationManager.AppSettings["starsPort"]);

            // Connect to Stars.
            stars = new StarsInterface(myNodeName, starsServerName, keyFileName, starsPort);
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

            // Send Stars Message "System gettime".
            stars.Send("System gettime");

            // Get reply of system time from StarsServer and Show it at messagebox.
            StarsMessage rcvMesg = stars.Receive();
            MessageBox.Show("Reply by using ReceiveMethod: " + rcvMesg.allMessage);

            // Add the stars handler named 'handler' which is called when arriving stars messages.
            StarsCbHandler cb = new StarsCbHandler(handler);
            StarsCbWinForm cbStars = new StarsCbWinForm(this, stars);

            // Callback mode started. Not to use stars.Receive() method.
            cbStars.StartCbHandler(cb);
        }


        private void handler(object sender, STARS.StarsCbArgs ev)
        {
            // Receiving Stars message by callback mode. Show reply at messagebox.
            MessageBox.Show("Reply via callback: " + ev.allMessage);
            return;
        }

    }
}