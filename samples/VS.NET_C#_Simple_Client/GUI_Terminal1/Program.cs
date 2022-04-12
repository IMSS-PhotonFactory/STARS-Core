using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace GUI_Terminal1
{
    static class Program
    {
        /// <summary>
        /// Application Entry Point.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
