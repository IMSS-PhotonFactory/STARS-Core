using System;
using System.Collections;
using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Text;

namespace STARS
{
    
    //STARS Message Class
    /// <summary>Class for StarsMessage.</summary>
    /// <remarks>This class is used to store the data of Stars Message.</remarks>
    public class StarsMessage
    {
        /// <summary>Used to indicate the 'fromnode', the element of Stars Message.</summary>
        public string from;
        /// <summary>Used to indicate the 'tonode', the element of Stars Message.</summary>
        public string to;
        /// <summary>Used to indicate the 'command', a part of 'Message' element of Stars Message.</summary>
        public string command;
        /// <summary>Used to indicate the 'parameters', a part of 'Message' element of Stars Message.</summary>
        public string parameters;

        /// <summary>Constructor for StarsMessage.</summary>
        /// <remarks>Parameters for constructor are reflected to class fields and properties.</remarks>
        /// <param name="from">Used to indicate the 'fromnode', the element of Stars Message.</param>
        /// <param name="to">Used to indicate the 'tonode', the element of Stars Message.</param>
        /// <param name="command">Used to indicate the 'command', a part of 'Message' element of Stars Message.</param>
        /// <param name="parameters">Used to indicate the 'parameters', a part of 'Message' element of Stars Message.</param>
        public StarsMessage(string from, string to, string command, string parameters)
        {
            this.from = from;
            this.to = to;
            this.command = command;
            this.parameters = parameters;
        }

        /// <summary>Constructor for StarsMessage.</summary>
        /// <remarks>Class fields and properties are cleared. (Method Clear() called)</remarks>
        public StarsMessage()
        {
            this.Clear();
        }

        /// <summary>Method for Clear.</summary>
        /// <remarks>Clear class fields and properties of StarsMessage.</remarks>
        public void Clear()
        {
            this.from = "";
            this.to = "";
            this.command = "";
            this.parameters = "";

        }

        /// <summary>Used to indicate the whole Stars Message.</summary>
        public string allMessage
        {
            get
            {
                if (parameters.Length == 0)
                {
                    return from + ">" + to + " " + command;
                }
                else
                {
                    return from + ">" + to + " " + command + " " + parameters;
                }
            }
        }

        /// <summary>Used to indicate the 'Message', the element of Stars Message.</summary>
        public string Message
        {
            get
            {
                if (parameters.Length == 0)
                {
                    return command;
                }
                else
                {
                    return command + " " + parameters;
                }
            }
        }

        /// <summary>Returns strings array from parameters.</summary>
        public string[] ParamStrArray(char spc)
        {
            return parameters.Split(spc);
        }

        public short[] ParamShortArray(char spc)
        {
            return StarsConvParams.ToShortArray(parameters, spc);
        }

        public ushort[] ParamUShortArray(char spc)
        {
            return StarsConvParams.ToUShortArray(parameters, spc);
        }

        public int[] ParamIntArray(char spc)
        {
            return StarsConvParams.ToIntArray(parameters, spc);
        }

        public uint[] ParamUIntArray(char spc)
        {
            return StarsConvParams.ToUIntArray(parameters, spc);
        }

        public long[] ParamLongArray(char spc)
        {
            return StarsConvParams.ToLongArray(parameters, spc);
        }

        public ulong[] ParamULongArray(char spc)
        {
            return StarsConvParams.ToULongArray(parameters, spc);
        }

        public float[] ParamFloatArray(char spc)
        {
            return StarsConvParams.ToFloatArray(parameters, spc);
        }

        public double[] ParamDoubleArray(char spc)
        {
            return StarsConvParams.ToDoubleArray(parameters, spc);
        }

        public decimal[] ParamDecimalArray(char spc)
        {
            return StarsConvParams.ToDecimalArray(parameters, spc);
        }

        public bool[] ParamBoolArray(char spc)
        {
            return StarsConvParams.ToBoolArray(parameters, spc);
        }

    }


    //This class is used for Callback
    /// <summary>Class for StarsCbArgs.</summary>
    /// <remarks>
    /// This class is used for Callback.
    /// </remarks>
    public class StarsCbArgs : EventArgs
    {
        /// <summary>Used to indicate the 'fromnode', the element of Stars Message.</summary>
        public string from;
        /// <summary>Used to indicate the 'tonode', the element of Stars Message.</summary>
        public string to;
        /// <summary>Used to indicate the 'command', a part of 'Message' element of Stars Message.</summary>
        public string command;
        /// <summary>Used to indicate the 'parameters', a part of 'Message' element of Stars Message.</summary>
        public string parameters;

        /// <summary>Constructor for StarsCbArgs.</summary>
        /// <remarks>Parameters for constructor are reflected to class fields and properties.</remarks>
        /// <param name="from">Used to indicate the 'fromnode', the element of Stars Message.</param>
        /// <param name="to">Used to indicate the 'tonode', the element of Stars Message.</param>
        /// <param name="command">Used to indicate the 'command', a part of 'Message' element of Stars Message.</param>
        /// <param name="parameters">Used to indicate the 'parameters', a part of 'Message' element of Stars Message.</param>
        public StarsCbArgs(string from, string to, string command, string parameters)
        {
            this.from = from;
            this.to = to;
            this.command = command;
            this.parameters = parameters;
        }

        /// <summary>Method for Clear.</summary>
        /// <remarks>Clear class fields and properties of StarsMessage.</remarks>
        public void Clear()
        {
            this.from = "";
            this.to = "";
            this.command = "";
            this.parameters = "";

        }

        /// <summary>Used to indicate the whole Stars Message.</summary>
        public string allMessage
        {
            get
            {
                if (parameters.Length == 0)
                {
                    return from + ">" + to + " " + command;
                }
                else
                {
                    return from + ">" + to + " " + command + " " + parameters;
                }
            }
        }

        /// <summary>Used to indicate the 'Message', the element of Stars Message.</summary>
        public string Message
        {
            get
            {
                if (parameters.Length == 0)
                {
                    return command;
                }
                else
                {
                    return command + " " + parameters;
                }
            }
        }

        /// <summary>Returns strings array from parameters.</summary>
        public string[] ParamStrArray(char spc)
        {
            return parameters.Split(spc);
        }

        public short[] ParamShortArray(char spc)
        {
            return StarsConvParams.ToShortArray(parameters, spc);
        }

        public ushort[] ParamUShortArray(char spc)
        {
            return StarsConvParams.ToUShortArray(parameters, spc);
        }

        public int[] ParamIntArray(char spc)
        {
            return StarsConvParams.ToIntArray(parameters, spc);
        }

        public uint[] ParamUIntArray(char spc)
        {
            return StarsConvParams.ToUIntArray(parameters, spc);
        }

        public long[] ParamLongArray(char spc)
        {
            return StarsConvParams.ToLongArray(parameters, spc);
        }

        public ulong[] ParamULongArray(char spc)
        {
            return StarsConvParams.ToULongArray(parameters, spc);
        }

        public float[] ParamFloatArray(char spc)
        {
            return StarsConvParams.ToFloatArray(parameters, spc);
        }

        public double[] ParamDoubleArray(char spc)
        {
            return StarsConvParams.ToDoubleArray(parameters, spc);
        }

        public decimal[] ParamDecimalArray(char spc)
        {
            return StarsConvParams.ToDecimalArray(parameters, spc);
        }

        public bool[] ParamBoolArray(char spc)
        {
            return StarsConvParams.ToBoolArray(parameters, spc);
        }
    }

    //STARS Convert Parameters;
    /// <summary>Class for parameter conversion.</summary>
    /// <remarks>This class is used internally to convert parameter strings to array.</remarks>
    public static class StarsConvParams
    {
        //ToShort ==========================================
        public static short[] ToShortArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            short[] vArray = new short[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToInt16(strArray[lp]);
                }
            }
            catch
            {
                return new short[0];
            }
            return vArray;
        }

        //ToUShort ==========================================
        public static ushort[] ToUShortArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            ushort[] vArray = new ushort[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToUInt16(strArray[lp]);
                }
            }
            catch
            {
                return new ushort[0];
            }
            return vArray;
        }

        //ToInt ==========================================
        public static int[] ToIntArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            int[] vArray = new int[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToInt32(strArray[lp]);
                }
            }
            catch
            {
                return new int[0];
            }
            return vArray;
        }

        //ToUInt ==========================================
        public static uint[] ToUIntArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            uint[] vArray = new uint[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToUInt32(strArray[lp]);
                }
            }
            catch
            {
                return new uint[0];
            }
            return vArray;
        }

        //ToLong ==========================================
        public static long[] ToLongArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            long[] vArray = new long[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToInt64(strArray[lp]);
                }
            }
            catch
            {
                return new long[0];
            }
            return vArray;
        }

        //ToULong ==========================================
        public static ulong[] ToULongArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            ulong[] vArray = new ulong[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToUInt64(strArray[lp]);
                }
            }
            catch
            {
                return new ulong[0];
            }
            return vArray;
        }

        //ToFloat ==========================================
        public static float[] ToFloatArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            float[] vArray = new float[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToSingle(strArray[lp]);
                }
            }
            catch
            {
                return new float[0];
            }
            return vArray;
        }

        //ToDouble ==========================================
        public static double[] ToDoubleArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            double[] vArray = new double[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToDouble(strArray[lp]);
                }
            }
            catch
            {
                return new double[0];
            }
            return vArray;
        }

        //ToDecimal ==========================================
        public static decimal[] ToDecimalArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            decimal[] vArray = new decimal[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    vArray[lp] = System.Convert.ToDecimal(strArray[lp]);
                }
            }
            catch
            {
                return new decimal[0];
            }
            return vArray;
        }

        //ToBool ==========================================
        public static bool[] ToBoolArray(string str, char sp)
        {
            string[] strArray = str.Split(sp);
            int l = strArray.Length;
            bool[] vArray = new bool[l];
            int lp;
            try
            {
                for (lp = 0; lp < l; lp++)
                {
                    if (System.Convert.ToInt32(strArray[lp]) == 0)
                    {
                        vArray[lp] = false;
                    }
                    else
                    {
                        vArray[lp] = true;
                    }
                }
            }
            catch
            {
                return new bool[0];
            }
            return vArray;
        }

    }

    //STARS Exception;
    /// <summary>Class for StarsException.</summary>
    /// <remarks>This class is called when Stars Exception occurred.</remarks>
    public class StarsException : System.ApplicationException
    {
        /// <summary>
        ///  Constructor for StarsException.
        /// </summary>
        /// <remarks>
        /// Automatically called for Stars Exception.
        /// </remarks>
        /// <param name="message">Using inherited message.</param>
        public StarsException(string message)
            : base(message)
        {
        }
    }

    /// <summary>Delegate for StarsCbHandler.</summary>
    /// <remarks>For using Callback.</remarks>
    /// <param name="obj">Object.</param>
    /// <param name="ev">StarsCbArgs which contains Stars Message.</param>
    public delegate void StarsCbHandler(object obj, StarsCbArgs ev);


    //STARS Interface
    //STARS Message Class
    /// <summary>Class for StarsInterface.</summary>
    /// <remarks>This class is used to talk with Stars Server.</remarks>
    public class StarsInterface
    {
        private const int defaultTimeout = 5000;

        /// <summary>Used to indicate the nodename of Stars client.</summary>
        public string nodeName;
        /// <summary>Used to indicate the Stars Server hostname. (default: 'localhost')</summary>
        public string svrHost;
        /// <summary>Used to indicate the Stars Server portno. (default: 6057)</summary>
        public int svrPort;
        /// <summary>Used to indicate the certification keyfile's name. (default: 'nodeName'.key)</summary>
        public string keyFile;

        /// <summary>If keyWords is not "", these keywards that splited with blank character instead of keyfile.</summary>
        public string keWords;

        private Socket sock;

        //These variables are used for Read messages.
        private byte[] readBuffer;
        private int readCount;
        private int processedCount;
        private ArrayList readArray;
        private int processedLevel;  //shows progress of message processing
                                     //(Processed.. 0=Nothing, 1=From, 2=To, 3=Command, 4=Parameter)
        private ArrayList [] mesProcArray; //Buffer for message processing.


        /// <summary>Constructor for StarsInterface.</summary>
        /// <remarks>Parameters for constructor are reflected to class fields and properties.</remarks>
        /// <param name="nodeName">Used to indicate the nodename of Stars client.</param>
        /// <param name="svrHost">Used to indicate the Stars Server hostname.</param>
        /// <param name="keyFile">Used to indicate the certification keyfile's name.</param>
        /// <param name="svrPort">Used to indicate the Stars Server portno.</param>
        public StarsInterface(string nodeName, string svrHost, string keyFile, int svrPort)
        {
            this.nodeName = nodeName;
            this.svrHost = svrHost;
            this.keyFile = keyFile;
            this.svrPort = svrPort;
            this.keWords = "";
            sock = null;
            readBuffer = new byte[1024];
            readCount = 0;
            processedCount = 0;
            readArray=new ArrayList();
            processedLevel = 0;
            mesProcArray = new ArrayList[4];
            int lp;
            for (lp = 0; lp <= 3; lp++) { mesProcArray[lp] = new ArrayList(); }
        }
        
        /// <summary>Constructor for StarsInterface.</summary>
        /// <remarks>Parameters for constructor are reflected to class fields and properties.</remarks>
        /// <param name="nodeName">Used to indicate the nodename of Stars client.</param>
        /// <param name="svrHost">Used to indicate the Stars Server hostname.</param>
        /// <param name="keyFile">Used to indicate the certification keyfile's name.</param>
        public StarsInterface(string nodeName, string svrHost, string keyFile)
            : this(nodeName, svrHost, keyFile, 6057)
        {
        }

        /// <summary>Constructor for StarsInterface.</summary>
        /// <remarks>Parameters for constructor are reflected to class fields and properties.</remarks>
        /// <param name="nodeName">Used to indicate the nodename of Stars client.</param>
        /// <param name="svrHost">Used to indicate the Stars Server hostname.</param>
        public StarsInterface(string nodeName, string svrHost)
            : this(nodeName, svrHost, nodeName + ".key", 6057)
        {
        }

        //Connect to stars server (send terminal name and keyword).
        /// <summary>Method for Connect.</summary>
        /// <remarks>Start connecting to Stars Server.</remarks>
        public void Connect()
        {
            //Read keyword
            ArrayList keyword;
            try
            {
                keyword = GetKeywords();
            }
            catch (Exception e)
            {
                StarsException eStars = new StarsException("Could not open keyword file.: " + e.Message);
                throw eStars;
            }

            //Establish TCP/IP Socket
            try
            {
                sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

// This method is old one.
//                sock.Connect(new IPEndPoint(Dns.Resolve(svrHost).AddressList[0], svrPort));
// This method will be used on .NET version 2.0 or later. 2014-05-15 replaced from this version of stars interface.
                sock.Connect(svrHost, svrPort);

            }
            catch (Exception e)
            {
                StarsException eStars = new StarsException("Could not establish TCP/IP connection.: " + e.Message);
                throw eStars;
            }
            sock.Blocking = true;


            //Get random number.
            StarsMessage rdBuf = Receive();
            int rNum = int.Parse(rdBuf.from);

            //Get keyword and send to STARS server.
            string bufKeyword = (string)keyword[(rNum % keyword.Count)];
            tcpSendString(nodeName + " " + bufKeyword);
            rdBuf = Receive();
            if (rdBuf.command != "Ok:")
            {
                StarsException eStars = new StarsException("Could not connect to server.: " + rdBuf.Message);
                throw eStars;
            }
        }

        //Read keyword list from file.
        private ArrayList GetKeywords()
        {
            ArrayList keyword;
            if (this.keWords != "")
            {
                keyword = new ArrayList(this.keWords.Split(' '));
            }
            else
            {
                keyword = new ArrayList();
                StreamReader reader = new StreamReader(keyFile);
                try
                {
                    do
                    {
                        keyword.Add(reader.ReadLine());
                    }
                    while (reader.Peek() != -1);
                }
                finally
                {
                    reader.Close();
                }
            }
            return keyword;
        }


        /// <summary>Method for Disconnect.</summary>
        /// <remarks>Disconnect from Stars Server.</remarks>
        public void Disconnect()
        {
 
            sock.Close();
        }

        //STARS Send
        /// <summary>Method for Send.</summary>
        /// <remarks>
        /// Send Stars Message to Stars Server.
        /// Indicate the 'fromnode', 'tonode' and 'Message' of Stars Message.
        /// </remarks>
        /// <param name="sndFrom">Used to indicate the 'fromnode', the element of Stars Message.</param>
        /// <param name="sndTo">Used to indicate the 'tonode', the element of Stars Message.</param>
        /// <param name="sndCommand">Used to indicate the 'Message', the element of Stars Message.</param>
        public void Send(string sndFrom, string sndTo, string sndCommand)
        {
            string sndBuf = sndFrom + ">" + sndTo + " " + sndCommand;
            tcpSendString(sndBuf);
        }

        /// <summary>Method for Send.</summary>
        /// <remarks>
        /// Send Stars Message to Stars Server.
        /// Indicate the 'tonode' and 'Message' of Stars Message.
        /// </remarks>
        /// <param name="sndTo">Used to indicate the 'tonode', the element of Stars Message.</param>
        /// <param name="sndCommand">Used to indicate the 'Message', the element of Stars Message.</param>
        public void Send(string sndTo, string sndCommand)
        {
            string sndBuf = sndTo + " " + sndCommand;
            tcpSendString(sndBuf);
        }

        /// <summary>Method for Send.</summary>
        /// <remarks>
        /// Send Stars Message to Stars Server.
        /// Indicate the text of Stars Message.
        /// </remarks>
        /// <param name="sndCommand">Used to indicate the text of Stars Message.</param>
        public void Send(string sndCommand)
        {
            tcpSendString(sndCommand);
        }

        //Send strings TCP/IP socket.
        private void tcpSendString(string sndBuf)
        {
            sndBuf = sndBuf + "\n";
            byte[] byteBuffer = Encoding.ASCII.GetBytes(sndBuf);
            sock.Send(byteBuffer);

        }
                
        //STARS Receive
        /// <summary>Method for Receive.</summary>
        /// <remarks>
        /// Receive Stars Message form Stars Server with timeout indicating.
        /// </remarks>
        /// <param name="timeout">Used to indicate the timeout milliseconds.</param>
        public StarsMessage Receive(int timeout)
        {
            StarsMessage rdMes;
            rdMes = ReceiveCommon(timeout);
            return rdMes;
        }

        //STARS Receive
        /// <summary>Method for Receive.</summary>
        /// <remarks>Receive Stars Message form Stars Server.</remarks>
        public StarsMessage Receive()
        {
            StarsMessage rdMes;
            rdMes = ReceiveCommon(defaultTimeout);
            return rdMes;
        }

        private StarsMessage ReceiveCommon(int timeout)
        {
            StarsMessage rdMes = new StarsMessage();

            
            while (!ProceessMessage(ref rdMes))
            {
                //Error happens on WindowsCE 2008-04-10
                // The error will be ignored. I'm not sure that the solution is right. T.Kosuge
                try
                {
                    sock.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReceiveTimeout, timeout);
                }
                catch { }


                try
                {
                    readCount = sock.Receive(readBuffer, SocketFlags.None);
                    processedCount = 0;
                }
                catch (Exception e)
                {
                    //Clear buffers with error.
                    readCount = 0;
                    processedCount = 0;
                    for (int lp = 0; lp < 4; lp++) { mesProcArray[lp].Clear(); }
                    processedLevel = 0;

                    StarsException eStars = new StarsException("Receive error.: " + e.Message);
                    sock.Blocking = true;
                    throw eStars;
                }
                if (readCount < 1)
                {
                    StarsException eStars = new StarsException("Could not read.: " + readCount.ToString());
                    throw eStars;
                }
            }
            return rdMes;
        }


        private bool ProceessMessage(ref StarsMessage rdMess)
        {
            byte [] delimiter = {0x3e, 0x20, 0x20, 0x0a};
            rdMess.Clear();
            byte nret = 0;
            int lp;
            while (processedCount < readCount)
            {
                nret = readBuffer[processedCount];
                processedCount++;
                if (nret == 0x0d) { continue; }
                if (nret == 0x0a)
                {
                    rdMess.from = Array2String(mesProcArray[0]);
                    rdMess.to = Array2String(mesProcArray[1]);
                    rdMess.command = Array2String(mesProcArray[2]);
                    rdMess.parameters = Array2String(mesProcArray[3]);
                    for (lp = 0; lp < 4; lp++) { mesProcArray[lp].Clear(); }
                    processedLevel = 0;
                    return true;
                }
                if (nret == delimiter[processedLevel]) { processedLevel++; continue; }
                mesProcArray[processedLevel].Add(nret);
            }
            processedCount = 0;
            readCount = 0;
            return false;
        }

        private string Array2String(ArrayList al)
        {
            byte[] bBuf = new byte[al.Count];
            for (int i = 0; i < al.Count; i++)
            {
                bBuf[i] = (byte)al[i];
            }
            Encoding encode = Encoding.Default;
            //Changed for windows CE. 2008-04-02
            //return encode.GetString(bBuf);
            return encode.GetString(bBuf, 0, al.Count);
        }
        
        //Callback
        private StarsCbHandler CbHandler;
        private StarsMessage cbMessage;

        /// <summary>Method for StartCbHandler.</summary>
        /// <remarks>Add Stars handler.</remarks>
        /// <param name="cb">Indicate 'new StarsCbHandler(starshandlername)'.</param>
        public void StartCbHandler(StarsCbHandler cb)
        {
            CbHandler = cb;
            cbMessage = new StarsMessage();
            try
            {
                sock.BeginReceive(readBuffer, 0, readBuffer.Length, SocketFlags.None, new AsyncCallback(ReceivedMessage), null);
            }
            catch
            {
                return;
            }
        }

        private void ReceivedMessage(IAsyncResult asyncResult)
        {
            // Added try and catch 2008-04-10 by T.Kosuge.
            try
            {
                readCount = sock.EndReceive(asyncResult);
            }
            catch
            {
                return;
            }

            // Added checking readCount for mono.
            // (seems mono doesn't throw exception of EndReceive) 2017-06-05 T. Kosuge
            if (readCount <= 0)
            {
                return;
            }

            processedCount = 0;

            while (ProceessMessage(ref cbMessage))
            {
                if (CbHandler != null)
                {
                    StarsCbArgs ev = new StarsCbArgs(cbMessage.from, cbMessage.to, cbMessage.command, cbMessage.parameters);
                    CbHandler(this, ev);
                }
            }
            sock.BeginReceive(readBuffer, 0, readBuffer.Length, SocketFlags.None, new AsyncCallback(ReceivedMessage), null);
        }

        //This is Finalize
        /// <summary>This is Finalize.</summary>
        /// <remarks>Disconnect from Stars Server. (Method Disconnect() called)</remarks>
        ~StarsInterface()
        {
            if (sock != null)
            {
                Disconnect();
            }
        }

    }
}
