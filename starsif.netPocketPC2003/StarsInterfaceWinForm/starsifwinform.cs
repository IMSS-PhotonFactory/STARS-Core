using System;
using System.Text;
using System.Net.Sockets;
using STARS;
using System.Windows.Forms;

namespace STARS.WinForm
{
    /// <summary>Class for StarsCbWinForm.</summary>
    /// <remarks>This class is stars.NET for Forms Application.</remarks>
    public class StarsCbWinForm
    {
        private Form frmObject;
        private StarsInterface st;

        private StarsCbHandler CbHandlerWinForm;

        /// <summary>Method for StartCbHandler.</summary>
        /// <remarks>Add Stars handler for Forms Application.</remarks>
        /// <param name="cb">Indicate 'new StarsCbHandler(starshandlername)'.</param>
        /// <example>
        /// <code>
        /// public StarsInterface stars;
        /// private void Form1_Load(object sender, EventArgs e)
        /// {
        ///     stars = new StarsInterface(starsargs[0], starsargs[1]);
        ///     try
        ///     {
        ///            stars.Connect();
        ///     }
        ///     catch (Exception se)
        ///     {
        ///         MessageBox.Show(se.Message);
        ///         this.Close();
        ///     }
        ///     StarsCbWinForm cbStars = new StarsCbWinForm(this, stars);
        ///     cbStars.StartCbHandler(new StarsCbHandler(stars_received));
        /// </code>
        /// </example>
        public void StartCbHandler(StarsCbHandler cb)
        {
            CbHandlerWinForm = cb;
            st.StartCbHandler(new StarsCbHandler(CbWinForm));
        }

        /// <summary>Constructor for StarsCbWinForm.</summary>
        /// <remarks>Make object for enable access to forms from stars.</remarks>
        /// <param name="frmObject">Indicate 'Form' Object.</param>
        /// <param name="st">Indicate 'Stars' Object.</param>
        /// <example>
        /// <code>
        /// public StarsInterface stars;
        /// private void Form1_Load(object sender, EventArgs e)
        /// {
        ///     stars = new StarsInterface(starsargs[0], starsargs[1]);
        ///     try
        ///     {
        ///            stars.Connect();
        ///     }
        ///     catch (Exception se)
        ///     {
        ///         MessageBox.Show(se.Message);
        ///         this.Close();
        ///     }
        ///     StarsCbWinForm cbStars = new StarsCbWinForm(this, stars);
        ///     cbStars.StartCbHandler(new StarsCbHandler(stars_received));
        /// </code>
        /// </example>
        public StarsCbWinForm(Form frmObject, StarsInterface st)
        {
            this.frmObject = frmObject;
            this.st = st;
        }

        private void CbWinForm(object obj, StarsCbArgs cb)
        {
            object[] args = { obj, cb };
            frmObject.Invoke(new StarsCbHandler(CbHandlerWinForm), args);
            //            frmObject.Invoke(new StarsCbHandler(CbHandlerWinForm), obj, cb);
        }
    }

    /*    public class StarsInterfaceWinForm : StarsInterface
        {
            private Form frmObject;

            public StarsInterfaceWinForm(string nodeName, string svrHost, string keyFile, int svrPort, Form obj)
                : base(nodeName, svrHost, keyFile, svrPort)
            {
                frmObject = obj;
            }

            public StarsInterfaceWinForm(string nodeName, string svrHost, string keyFile, Form obj)
                : base(nodeName, svrHost, keyFile, 6057)
            {
                frmObject = obj;
            }

            public StarsInterfaceWinForm(string nodeName, string svrHost, Form obj)
                : base(nodeName, svrHost, nodeName + ".key", 6057)
            {
                frmObject = obj;
            }

            private StarsCbHandler CbHandlerWinForm;

            public new void StartCbHandler(StarsCbHandler cb)
            {
                CbHandlerWinForm = cb;
                base.StartCbHandler(new StarsCbHandler(StarsCbWinForm));
            }

            private void StarsCbWinForm(object obj, StarsCbArgs cb)
            {
                frmObject.Invoke(new StarsCbHandler(CbHandlerWinForm), obj, cb);
            }

        }
    */

}
