using System;
//using System.Collections.Generic;
//using System.Text;
using STARS;


namespace ConsoleTerminal1
{
    /// <summary>Represents an Stars Console Application Main class.</summary>
    class Program
    {
        /// <summary>This field is a stars interface.</summary>
        private static StarsInterface stars;

        /// <summary>Here is Application Entrance.</summary>
        /// <seealso cref="Stars_Message_Received"/>
        /// <param name="args">Used to indicate command parameters.</param>
        /// <example>
        /// <code>
        /// // Step1. Connect to Stars.
        ///     stars = new StarsInterface("csterm", "localhost");
        ///     try
        ///     {
        ///         stars.Connect();
        ///     }
        ///     catch (Exception e)
        ///     {
        ///         Console.WriteLine(e.Message);
        ///         return;
        ///     }
        ///     
        /// // Step2. Add the stars handler named 'Stars_Message_Received' which is called when arriving stars messages.
        ///     stars.StartCbHandler(new StarsCbHandler(Stars_Message_Received));
        /// 
        /// // Step3. Waiting for the input from console.
        ///     Console.WriteLine("Input 'exit' to exit.");
        ///     String buf;
        ///     while (true)
        ///     {
        ///         buf = Console.ReadLine();
        ///         if(buf == "exit")
        ///         {
        ///             break;
        ///         }
        ///     }
        ///
        ///</code>
        ///</example>

        static void Main(string[] args)
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
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return;
            }

            // Step2. Add the stars handler named 'Stars_Message_Received' which is called when arriving stars messages via TCP/IP socket.
            stars.StartCbHandler(new StarsCbHandler(Stars_Message_Received));

            // Step3. Waiting for the input from console.
            //  until entering 'Quit' or 'Exit'.
            Console.WriteLine("Input Stars Message, for example 'System hello', or 'help' for help.");
            String buf;
            while (true)
            {
                buf = Console.ReadLine();
                if (buf == "")
                {
                    continue;
                }
                switch (buf.ToUpper())
                {
                    case "QUIT":
                        break;
                    case "EXIT":
                        break;
                    case "HELP":
                        Console.WriteLine("Enter [help|quit|exit|'Stars Message to be sended']");
                        continue;
                    default:
                        Console.WriteLine("SEND#" + buf + "#");
                        stars.Send(buf);
                        continue;
                }
                break;
            }
            return;
        }
        // This is Stars Handler called when arriving Stars Messages.
        // 
        /// <summary>This method is called when arriving stars messages.</summary>
        /// <param name="sender"></param>
        /// <param name="cb">Used to access the Stars object which contains received data.</param>
        /// <seealso cref="Main"/>
        /// <example>
        /// <code>
        /// static private void Stars_Message_Received(object sender, StarsCbArgs cb)
        /// {
        ///    //To check arriving "hello" 
        ///    if(cb.Message == "hello")
        ///    {
        ///        // Send Stars reply message to sender.
        ///        stars.Send(cb.from + " @" + cb.Message " hello nice to meet you");
        ///    }
        /// </code>
        /// </example>
        /// 
        static private void Stars_Message_Received(object sender, StarsCbArgs cb)
        {
            // No Message
            if (cb.Message.Trim() == "")
            {
                Console.WriteLine("RECV#{0}", cb.allMessage + "#");
                string sendbuf;
                sendbuf = cb.from + " @" + cb.Message + " Er: Bad command.";
                stars.Send(sendbuf);
                Console.WriteLine("RPLY#" + sendbuf);
            }
            // Event has come.
            else if (cb.command[0] == '_')
            {
                Console.WriteLine("EVNT#{0}", cb.allMessage);
            }
            // Reply has come.
            else if (cb.command[0] == '@')
            {
                Console.WriteLine("RECV#{0}", cb.allMessage);
            }
            // Command Request's arrived, to nodename
            else if (cb.to == stars.nodeName)
            {
                Console.WriteLine("RECV#{0}", cb.allMessage + "#");
                string sendbuf;

                //Check request and send reply message
                switch (cb.Message)
                {
                    case "hello":
                        sendbuf = cb.from + " @" + cb.Message + " hello nice to meet you";
                        stars.Send(sendbuf);
                        Console.WriteLine("RPLY#" + sendbuf);
                        break;
                    case "help":
                        sendbuf = cb.from + " @" + cb.Message + " hello help";
                        stars.Send(sendbuf);
                        Console.WriteLine("RPLY#" + sendbuf);
                        break;
                    default:
                        sendbuf = cb.from + " @" + cb.Message + " Er: Bad command or parameter.";
                        stars.Send(sendbuf);
                        Console.WriteLine("RPLY#" + sendbuf);
                        break;
                }
            }
            // Command Request's arrived, to nodename.XXXX... maybe
            else
            {
                Console.WriteLine("RECV#{0}", cb.allMessage + "#");
                string sendbuf;
                sendbuf = cb.from + " @" + cb.Message + " Er: " + cb.to + " is down.";
                stars.Send(sendbuf);
                Console.WriteLine("RPLY#" + sendbuf);
            }
            return;
        }
    }
}
