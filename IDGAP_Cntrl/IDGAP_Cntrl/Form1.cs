using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Collections;
using System.Text.RegularExpressions;
using System.IO;
using STARS;
using STARS.WinForm;

namespace IDGAP_Cntrl
{
    public partial class Form1 : Form
    {
        private const int ResetCheck = 15000;
        private const int readIntervalStop = 5000;
        private const int readIntervalRun = 500;
        public Hashtable cfg;
        private StarsInterface stars;
        public float gapPresent;
        public float gapDestination;
        public float tprPresent=0;
        public float tprDestination;
        public bool isConnected;
        public bool isgapRunning;
        public bool istprRunning;
        public float gapmax = 0;
        public float gapmin = 0;
        public string gapmaxnode="";
        public string gapminnode="";
        public float tprmax = 0;
        public float tprmin = 0;
        public string tprnode = "";
        public string tprmaxnode = "";
        public string tprminnode = "";
        public bool isShowAlert;
        public bool isGapMovableWhenTprZero;
        public bool isTprUse;
        public bool isTprReadOnly;

        public Form1()

        {
            InitializeComponent();
        }
        
        private void Form1_Load(object sender, EventArgs e)
        {
            dispmessage("");
            cfg = LoadConfigData("IDGAP_Cntrl.ini");
            isConnected = true;
            isgapRunning = false;
            istprRunning = false;
            isShowAlert = false;
            isGapMovableWhenTprZero = false;
            isTprUse=true;
            isTprReadOnly = false;
            if (cfg["GapItemName"] != null)
            {
                labelGapPresent.Text = cfg["GapItemName"].ToString().Trim() + " Present";
            }
            if (cfg["TprUse"] != null)
            {
                if (cfg["TprUse"].ToString().Trim() == "1")
                {
                    isTprUse = true;
                }
                else
                {
                    isTprUse = false;
                }
            }
            if (isTprUse == false)
            {
                this.labelStatus.Location=new Point(this.labelStatus.Location.X,labelTprPresent.Location.Y-8);
                this.Size = new Size(this.Size.Width , this.Size.Height - this.labelStatus.Size.Height);
            }
            stars = new StarsInterface(cfg["NodeName"].ToString(), cfg["Server"].ToString());
            try
            {
                tprnode = "dummy";
                isTprReadOnly = false;
                if (isTprUse)
                {
                    if (cfg["TprReadOnly"] != null)
                    {
                        if (cfg["TprReadOnly"].ToString().Trim() == "1")
                        {
                            isTprReadOnly = true;
                        }
                        else
                        {
                            isTprReadOnly = false;
                        }
                    }
                    tprnode = cfg["TprNode"].ToString();
                }
                this.Text = cfg["Title"].ToString();
                gapmax = float.Parse(cfg["GapMax"].ToString());
                gapmin = float.Parse(cfg["GapMin"].ToString());
                if (isTprUse)
                {
                    tprmax = float.Parse(cfg["TprMax"].ToString());
                    tprmin = float.Parse(cfg["TprMin"].ToString());
                }
                stars.Connect();
                // lblGapPresent.Text = stMes.parameters;
                // txtDestination.Text = stMes.parameters;
                //stMes = stars.Receive();
                stars.Send(cfg["GapControllerNode"].ToString(), "hello"); // This Time use.
                stars.Send("System", "flgon " + cfg["GapControllerNode"].ToString()); // This Time use.
                stars.Send("System", "flgon " + cfg["GapNode"].ToString()); // This Time use.
                if (isTprUse)
                {
                    stars.Send("System", "flgon " + cfg["TprNode"].ToString()); // This Time use.
                }
                gapmaxnode = "dummy";
                gapminnode = "dummy";
                tprmaxnode = "dummy";
                tprminnode = "dummy";

                if (isTprUse)
                {
                    if (cfg["GapMovableWhenTprZero"] != null)
                    {
                        if (cfg["GapMovableWhenTprZero"].ToString().Trim() == "1")
                        {
                            isGapMovableWhenTprZero = true;
                        }
                    }
                }
                if (cfg["ShowAlert"] != null)
                {
                    if (cfg["ShowAlert"].ToString().Trim() == "1")
                    {
                        isShowAlert = true;
                    }
                }
                if ((cfg["GapMaxNode"] != null && cfg["GapMinNode"] != null))
                {
                    if ((cfg["GapMaxNode"].ToString().Trim() != "") && (cfg["GapMinNode"].ToString().Trim() != ""))
                    {
                        gapmaxnode = cfg["GapMaxNode"].ToString();
                        gapminnode = cfg["GapMinNode"].ToString();
                        stars.Send("System", "flgon " + cfg["GapMaxNode"].ToString()); // This Time use.
                        stars.Send("System", "flgon " + cfg["GapMinNode"].ToString()); // This Time use.
                        stars.Send(cfg["GapMinNode"].ToString(), "GetValue"); // This Time use.
                        stars.Send(cfg["GapMaxNode"].ToString(), "GetValue"); // This Time use.
                    }
                }
                if (isTprUse)
                {
                    if ((cfg["TprMaxNode"] != null && cfg["TprMinNode"] != null))
                    {
                        if ((cfg["TprMaxNode"].ToString() != "") && (cfg["TprMinNode"].ToString() != ""))
                        {
                            tprmaxnode = cfg["TprMaxNode"].ToString();
                            tprminnode = cfg["TprMinNode"].ToString();
                            stars.Send("System", "flgon " + cfg["TprMaxNode"].ToString()); // This Time use.
                            stars.Send("System", "flgon " + cfg["TprMinNode"].ToString()); // This Time use.
                            stars.Send(cfg["TprMinNode"].ToString(), "GetValue"); // This Time use.
                            stars.Send(cfg["TprMaxNode"].ToString(), "GetValue"); // This Time use.
                        }
                    }
                }
                Send_GetValue();

                timer1.Interval = ResetCheck;
                timer1.Enabled = false; // Don't Use

                StarsCbWinForm cbStars = new StarsCbWinForm(this, stars);
                cbStars.StartCbHandler(new StarsCbHandler(Stars_Handler));
            }
            catch (Exception se)
            {
                MessageBox.Show(se.Message);
                this.Close();
            }
            
        }

        private void Stars_Handler(object obj, StarsCbArgs cb)
        {
            txtLog_update(cb.allMessage);
            if ((cb.from == "System"))
            {
                if ((cb.parameters.Contains("Er: " + cfg["GapControllerNode"].ToString() + " is down.")))
                {
                    isConnected = false;
                    lblGapPresent.Text = cb.parameters;
                    lblTprPresent.Text = cb.parameters;
                }
                lockwhilerunning();
            }
            else if ((cb.from == cfg["GapControllerNode"].ToString()))
            {
                if (cb.command == "_Connected")
                {
                    isConnected = true;
                    stars.Send(cfg["GapControllerNode"].ToString(), "flushdata");
	                lockwhilerunning();
                }
                else if (cb.command == "_Disconnected")
                {
                    isConnected = false;
	                lockwhilerunning();
                }
                else if ((cb.parameters.Contains("Er: " + cfg["GapNode"].ToString() + " is down.")))
                {
                    isConnected = false;
                    lblGapPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
//                else if ((cb.parameters.Contains("Er: " + cfg["TprNode"].ToString() + " is down.")))
                else if ((cb.parameters.Contains("Er: " + tprnode + " is down.")))
                {
                    isConnected = false;
                    lblTprPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
                else if ((cb.parameters.Contains("Er: " + gapmaxnode + " is down.")))
                {
                    isConnected = false;
                    lblGapPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
                else if ((cb.parameters.Contains("Er: " + gapminnode + " is down.")))
                {
                    isConnected = false;
                    lblGapPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
                else if ((cb.parameters.Contains("Er: " + tprmaxnode + " is down.")))
                {
                    isConnected = false;
                    lblTprPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
                else if ((cb.parameters.Contains("Er: " + tprminnode + " is down.")))
                {
                    isConnected = false;
                    lblTprPresent.Text = cb.parameters;
	                lockwhilerunning();
                }
            }
            else if ((cb.from == cfg["GapNode"].ToString()))
            {
                if (cb.command == "@GetValue")
                {
                    lblGapPresent.Text = cb.parameters;
                    Regex theReg = new Regex("(-?[0-9.]+)");
                    Match theMatch = theReg.Match(cb.parameters);
                    if (theMatch.Success)
                    {
                        gapPresent = float.Parse(theMatch.Value.ToString());
	                    txtDestination.Text = cb.parameters;
                    }
                    else
                    {
                        lblGapPresent.Text = cb.parameters;
                    }
                }
                else if (cb.command == "@ResetBusy")
                {
                    if (isShowAlert)
                    {
                        MessageBox.Show("Gap or Tpr has not changed. Please check the insertion device.");
                    }
                }
                else if (cb.command == "@IsBusy")
                {
                    if (cb.parameters == "0")
                    {
                        if (timer1.Enabled)
                        {
                            txtLog_update("LockRecovery:inactivate");
                            timer1.Enabled = false;
                        }
                        isgapRunning = false;
                        //                    timer1.Interval = readIntervalStop;
                    }
                    else if (cb.parameters == "1")
                    {
                        if (!timer1.Enabled)
                        {
                            timer1.Enabled = true;
                            txtLog_update("LockRecovery:activate");
                        }
                        isgapRunning = true;
                        //                    timer1.Interval = readIntervalRun;
                    }
                    lockwhilerunning();
                }
                else if (cb.command == "_ChangedIsBusy")
                {
                    if (cb.parameters == "0")
                    {
                        if (timer1.Enabled)
                        {
                            txtLog_update("LockRecovery:inactivate");
                            timer1.Enabled = false;
                        }
                        isgapRunning = false;
                        //                    timer1.Interval = readIntervalStop;
                    }
                    else if (cb.parameters == "1")
                    {
                        if (!timer1.Enabled)
                        {
                            timer1.Enabled = true;
                            txtLog_update("LockRecovery:activate");
                        }
                        isgapRunning = true;
                        //                    timer1.Interval = readIntervalRun;
                    }
                    lockwhilerunning();
                }
                else if (cb.command == "_ChangedValue")
                {
                    lblGapPresent.Text = cb.parameters;
                    gapPresent = float.Parse(lblGapPresent.Text);
                    if (timer1.Enabled)
                    {
                        txtLog_update("LockRecovery:inactivate");
                        timer1.Enabled = false;
                    }
                    lockwhilerunning();
                }
            }else if ((cb.from == gapmaxnode)) {
                if (cb.command == "@GetValue")
                {
                    Regex theReg = new Regex("(-?[0-9.]+)");
                    Match theMatch = theReg.Match(cb.parameters);
                    if (theMatch.Success)
                    {
                        gapmax = float.Parse(theMatch.Value.ToString());
                    }
                }
                else if (cb.command == "_ChangedValue")
                {
                    if ((isShowAlert== true) && (float.Parse(cb.parameters) != gapmax))
                    {
                        MessageBox.Show(Form.ActiveForm,"Maximum limit of gap value is " + float.Parse(cb.parameters).ToString() + ".");
                    }
                    gapmax = float.Parse(cb.parameters);
                }
                txtLog_update("Gap maximum value has set to " + gapmax.ToString());
            }
            else if ((cb.from == gapminnode))
            {
                {
                    if (cb.command == "@GetValue")
                    {
                        Regex theReg = new Regex("(-?[0-9.]+)");
                        Match theMatch = theReg.Match(cb.parameters);
                        if (theMatch.Success)
                        {
                            gapmin = float.Parse(theMatch.Value.ToString());
                        }
                    }
                    else if (cb.command == "_ChangedValue")
                    {
                        if ((isShowAlert==true) && (float.Parse(cb.parameters) != gapmin))
                        {
                            MessageBox.Show(Form.ActiveForm,"Minimum limit of gap value is " + float.Parse(cb.parameters).ToString() + ".");
                        }
                        gapmin = float.Parse(cb.parameters);
                    }
                    txtLog_update("Gap minimum value has set to " + gapmin.ToString());
                }
            }
//            else if ((cb.from == cfg["TprNode"].ToString()))
            else if ((cb.from == tprnode))
            {
                if (cb.command == "@GetValue")
                {
                    lblTprPresent.Text = cb.parameters;
                    Regex theReg = new Regex("(-?[0-9.]+)");
                    Match theMatch = theReg.Match(cb.parameters);
                    if (theMatch.Success)
                    {
                        tprPresent = float.Parse(theMatch.Value.ToString());
	                    txtTprDestination.Text = cb.parameters;
                        //if (istprRunning && (gapPresent == gapDestination))
                        //{
                        //    istprRunning = false;
                        //    timer1.Interval = readIntervalStop;
                        //}
                        //lockwhilerunning();
                    }
                    else
                    {
                        lblTprPresent.Text = cb.parameters;
                    }
                }
                else if (cb.command == "@ResetBusy")
                {
                    if (isShowAlert){
                        MessageBox.Show("Gap or Tpr has not changed. Please check the insertion device.");
                    }
                }
                else if (cb.command == "@IsBusy")
                {
                    if (cb.parameters == "0")
                    {
                        if (timer1.Enabled)
                        {
                            txtLog_update("LockRecovery:inactivate");
                            timer1.Enabled = false;
                        }
                        istprRunning = false;
                        //                    timer1.Interval = readIntervalStop;
                    }
                    else if (cb.parameters == "1")
                    {
                        if (!timer1.Enabled)
                        {
                            timer1.Enabled = true;
                            txtLog_update("LockRecovery:activate");
                        }
                        istprRunning = true;
                        //                    timer1.Interval = readIntervalRun;
                    }
                    lockwhilerunning();
                }
                else if (cb.command == "_ChangedIsBusy")
                {
                    if (cb.parameters == "0")
                    {
                        if (timer1.Enabled)
                        {
                            txtLog_update("LockRecovery:inactivate");
                            timer1.Enabled = false;
                        }
                        istprRunning = false;
                        //                    timer1.Interval = readIntervalStop;
                    }
                    else if (cb.parameters == "1")
                    {
                        if (!timer1.Enabled)
                        {
                            timer1.Enabled = true;
                            txtLog_update("LockRecovery:activate");
                        }
                        istprRunning = true;
                        //                    timer1.Interval = readIntervalRun;
                    }
                    lockwhilerunning();
                }
                else if (cb.command == "_ChangedValue")
                {
                    lblTprPresent.Text = cb.parameters;
                    tprPresent = float.Parse(lblTprPresent.Text);
                    if (timer1.Enabled)
                    {
                        txtLog_update("LockRecovery:inactivate");
                        timer1.Enabled = false;
                    }
                    lockwhilerunning();
                }
            }
            else if ((cb.from == tprmaxnode))
            {
                if (cb.command == "@GetValue")
                {
                    Regex theReg = new Regex("(-?[0-9.]+)");
                    Match theMatch = theReg.Match(cb.parameters);
                    if (theMatch.Success)
                    {
                        tprmax = float.Parse(theMatch.Value.ToString());
                    }
                }
                else if (cb.command == "_ChangedValue")
                {
                    tprmax = float.Parse(cb.parameters);
                }
                txtLog_update("Tpr maximum value has set to " + tprmax.ToString());
            }
            else if ((cb.from == tprminnode))
            {
                {
                    if (cb.command == "@GetValue")
                    {
                        Regex theReg = new Regex("(-?[0-9.]+)");
                        Match theMatch = theReg.Match(cb.parameters);
                        if (theMatch.Success)
                        {
                            tprmin = float.Parse(theMatch.Value.ToString());
                        }
                    }
                    else if (cb.command == "_ChangedValue")
                    {
                        tprmin = float.Parse(cb.parameters);
                    }
                    txtLog_update("Tpr minimum value has set to " + tprmin.ToString());
                }
            }
        }

        private void Send_GetValue()
        {
            stars.Send(cfg["GapNode"].ToString(), "GetValue");
            stars.Send(cfg["GapNode"].ToString(), "IsBusy");
            if (isTprUse)
            {
                stars.Send(cfg["TprNode"].ToString(), "GetValue");
                stars.Send(cfg["TprNode"].ToString(), "IsBusy");
            }
        }

        private Hashtable LoadConfigData(string fileName)
        {
            Hashtable hash = new Hashtable();
            string buf;
            Regex theReg = new Regex(@"(\S+)\s*=\s*(\S.*)");
            Match  mat;
            StreamReader reader = new StreamReader(fileName);
            try
            {
                do
                {
                    buf=reader.ReadLine();
                    if (buf.StartsWith("#") == false)
                    {
                        mat = theReg.Match(buf);
                        hash.Add(mat.Groups[1].Value, mat.Groups[2].Value);
                    }
                }
                while (reader.Peek() != -1);
            }
            finally
            {
                reader.Close();
            }

            return hash;

        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            stars.Send(cfg["GapNode"].ToString(), "ResetBusy");
            if (isTprUse)
            {
                stars.Send(cfg["TprNode"].ToString(), "ResetBusy");
            }
        }

        private void btnSetValue_Click(object sender, EventArgs e)
        {
            Regex theReg = new Regex(@"(-?\d+\.*\d*)");
            Match theMatch = theReg.Match(txtDestination.Text);
            if (theMatch.Success && (theMatch.Value.ToString() != ""))
            {
                float theDest = float.Parse(theMatch.Value.ToString());
                if (theDest >= gapmin && theDest <= gapmax)
                {
                    gapDestination = theDest;
                    dispmessage("");
                    stars.Send(cfg["GapNode"].ToString(), "SetValue " + theDest.ToString());
                    txtLog_update(cfg["GapNode"].ToString() + " " + "SetValue "+theDest.ToString());
                    isgapRunning = true;
                    //timer1.Interval = readIntervalRun;
                    return;
                }
            }
            if (isShowAlert)
            {
                MessageBox.Show("Bad Value. Gap must be between " + gapmin.ToString() + " and " + gapmax.ToString() + ".");
            }
            txtLog_update("Bad Value. Gap must be between " + gapmin.ToString() + " and " + gapmax.ToString() + ".");
            //txtDestination.Text = lblGapPresent.Text;
        }

        private void btnTprSetValue_Click(object sender, EventArgs e)
        {
            Regex theReg = new Regex(@"(-?\d+\.*\d*)");
            Match theMatch = theReg.Match(txtTprDestination.Text);
            if (theMatch.Success && (theMatch.Value.ToString() != ""))
            {
                float theDest = float.Parse(theMatch.Value.ToString());
                if (theDest >= tprmin && theDest <= tprmax)
                {
                    tprDestination = theDest;
                    dispmessage("");
                    stars.Send(cfg["TprNode"].ToString(), "SetValue " + theDest.ToString());
                    txtLog_update(cfg["TprNode"].ToString() + " " + "SetValue " + theDest.ToString());
                    istprRunning = true;
                    //timer1.Interval = readIntervalRun;
                    return;
                }
            }
            if (isShowAlert)
            {
                MessageBox.Show("Bad Value. Tpr must be between " + tprmin.ToString() + " and " + tprmax.ToString() + ".");
            }
            txtLog_update("Bad Value. Tpr must be between " + tprmin.ToString() + " and " + tprmax.ToString() + ".");
            //txtTprDestination.Text = lblTprPresent.Text;
        }

        private void lockwhilerunning()
        {
            if (isgapRunning)
            {
                lblGapPresent.ForeColor = Color.Blue;
            }
            else
            {
                lblGapPresent.ForeColor = Color.Black;
            }
            if (istprRunning)
            {
                lblTprPresent.ForeColor = Color.Blue;
            }
            else
            {
                lblTprPresent.ForeColor = Color.Black;
            }

            if (!isConnected)
            {
                txtDestination.Enabled = isConnected;
                btnSetValue.Enabled = isConnected;
                txtTprDestination.Enabled = isConnected;
                btnTprSetValue.Enabled = isConnected;
            }
            else if (isgapRunning || istprRunning)
            {
                txtDestination.Enabled = false;
                btnSetValue.Enabled = false;
                txtTprDestination.Enabled = false;
                btnTprSetValue.Enabled = false;
            }
            else if ((isGapMovableWhenTprZero == false) && (tprPresent != 0))
            {
                txtDestination.Enabled = false;
                btnSetValue.Enabled = false;
                txtTprDestination.Enabled = true;
                btnTprSetValue.Enabled = true;
            }
            else if (isTprUse == false)
            {
                txtDestination.Enabled = true;
                btnSetValue.Enabled = true;
                txtTprDestination.Enabled = false;
                btnTprSetValue.Enabled = false;
            }  
            else
            {
                txtDestination.Enabled = true;
                btnSetValue.Enabled = true;
                txtTprDestination.Enabled = true;
                btnTprSetValue.Enabled = true;
            }
            if (isTprReadOnly)
            {
                txtTprDestination.ReadOnly = true;
                btnTprSetValue.Enabled = false;
            }
        }
        private void dispmessage(string msg)
        {
            labelStatus.Text = msg;
        }
        // reflesh log display field text
        private void txtLog_update(string message)
        {
            int pos;
            int maxlines = (int)(100 / 2);
            //labelStatus.Text = ev.parameters + Environment.NewLine + labelStatus.Text;
            pos = labelStatus.Lines.Length;
            if (pos > maxlines)
            {
                string[] mes = labelStatus.Lines;
                labelStatus.Text = System.String.Join("", mes, 0, maxlines);
            }
            else
            {
                labelStatus.Text = message + Environment.NewLine + labelStatus.Text;
            }
        }

    }
}