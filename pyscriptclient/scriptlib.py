#!/usr/bin/python3
#################################################################################
# STARS Script client library
#################################################################################

# Define: program info
__author__ = 'T.Kosuge'
__version__ = '1.0'
__date__ = '2024-07-31'
import sys
import time
import datetime
import configparser
import stars
import re

class ScriptLib():
    """Library for script cliet of STARS
        Arguments:
            offline   [True|False] The script client doesn't connect STARS serve if this value is True.
            remote    Works with remote mode with \"remote\" client name.
    """
    def __init__(self, fn = 'scriptclient.cfg', offline = False, remote = None, debug = False):
        """fn: config filename \'scriptclient.cfg\' is used if omited.
           offline: Run with offline mode. If True, the client will not make connection with STARS srever.
           remote:  If set a client name, the script client sends print message to the client.
           debug:   Run with debug mode.
        """

        #add 'global' variables here like...
        #self.something = ''
        self.debug = debug
        self.scrconf = fn       # config file name of scriptclient
        self.conf = {}
        self.load_config(fn)

        self.remote = remote
        self.error = ""         # message of previous error
        self.previous_to = ""   # previous destination for wait_for
        self.connected = False  # flag, is the client connected the server.
        self.offline = offline  # work without STARS connection.
        self.data_file = ''      # data file name for output.
        self.file_init = True    # File initialize flag. The file will be open with 'w' if True.

        #STARS object
        self.st = stars.StarsInterface(
            self.conf[fn]["stars"]["mynodename"],
            self.conf[fn]["stars"]["starsserver"],
            self.conf[fn]["stars"]["keyfile"],
            int(self.conf[fn]["stars"]["starsport"]))

        if self.debug:
            self.st.setdebug(True)

        if not self.offline:
            self.connect()


        # Use the follow value if you need interval function
        #self.intervaltime = 0.5

        #Enable debug print
        #self.st.setdebug(True)

    # Functions =================================================
    def _debugprint(self, estr):
        """Print messages for debugging.
        """
        self.st._debugprint("{}\n".format(estr))


    def add_suffix(self, filename):
        """Add suffix to data file name.
        """
        ts = self.get_localtime()
        ts = ts.replace(" ", "_")
        ts = ts.replace(":", "")
        if filename == '':
            return "{}.txt".format(ts)
        else:
            return "{}_{}.txt".format(filename, ts)


    def write_file(self, mess, end='\n'):
        """Write message to data file. self.data_file must be configured previously.
           If currentdata is configured in cfg file current file will be created.
        """
        datadir = self.conf[self.scrconf]["file"]["datadir"]
        currentdata = self.conf[self.scrconf]["file"]["currentdata"]
        if self.file_init:
            wmode = 'w'
            self.file_init = False
        else:
            wmode = 'a'
        if len(datadir) > 0 and datadir[-1] != '/':
            datadir = datadir + '/'
        if currentdata != '':
            with open(datadir + currentdata, wmode) as f:
                f.write(mess + end)
        with open(datadir + self.data_file, wmode) as f:
            f.write(mess + end)
        self.print(mess, end=end)


    def load_config(self, fname):
        """Load parameters from config file with config parser.
        """
        cfg = configparser.ConfigParser()
        cfg.read(fname)
        self.conf[fname] = cfg


    def save_config(self, fname):
        """Save paramaters of fname to the file.
        """
        with open(fname, 'w') as f:
            self.conf[fname].write(f)


    def connect(self):
        """Connect to STARS server.
        """
        if self.st.connect():
            self.connected = True
        else:
            self.error = "Could not connect to STARS server."
            return None


    def send_command(self, node_to, message=''):
        """Send message to STARS server and wait for reply.
              Parameters:
                send_command(node_to, message)
                    or
                send_command(message)
              Returns:
                STARS Message or None (some error).
        """
        if self.send_event(node_to, message):
            return self.wait_for(r'^@', True)


    def send_event(self, node_to, message=''):
        """ Send message to STARS server without receiving.
              Parameters:
                send_event(node_to, message)
                    or
                send_event(message)
              Returns:
                (bool) True if sended, otherwise False.
        """
        if not self.connected:
            self.error = "Not connected."
            return False
        if message == '':
            self.previous_to = node_to.split()[0]
            msg = node_to
        else:
            self.previous_to = node_to
            msg = "{} {}".format(node_to, message)
        return self.st.send(msg)


    def wait_for(self, message, silent = False):
        """
        Wait for message from previous destination client which is pointed by \"send_command\" or \"send_event\".
        list of [\"from\", \"message (regex)\"] will be used if the argument type is list.
        This returns STARS Message of last message or returns None (timeout or error).
        """
        if not self.connected:
            self.error = "Not connected."
            return None
        if type(message) is str:
            if self.previous_to == "":
                self.error = "Previous destination not found."
                return None
            msg = [[self.previous_to, message]]
        elif type(message is list):
            msg = message
        else:
            self.error = "Bad type."
            return None

        while len(msg) > 0:
            rtmsg = self.st.receive(int(self.conf[self.scrconf]["stars"]["timeout"]))
            if rtmsg != '' and not silent:
                self.print("\r{}".format(rtmsg.allmessage))
            if rtmsg.command == "Break":
                self.send_event(rtmsg.nodefrom, "@Break Ok:")
                self.die("Break")
            if rtmsg.command == "_Break":
                self.die("Break")
            if rtmsg == '':
                self.error = "Timeout"
                return None
            for l in range(len(msg)):
                if rtmsg.nodefrom == msg[l][0] and re.search(msg[l][1], rtmsg.message) != None:
                    del msg[l]
                    break
        return rtmsg


    def sleep(self, stime):
        """ Sleep.
              sleep for stime (sec).
        """
        time.sleep(stime)


    def get_localtime(self):
        """Get localtime text YYYY-MM-DD hh:mm:ss
        """
        tm = datetime.datetime.now()
        return tm.strftime("%Y-%m-%d %H:%M:%S")


    def print(self, bufstr, end='\n'):
        """Print message screen
            Print message without delimiter to secreen or send message remote client if remote is set.
        """
        if self.remote != None:
            buf = bufstr.replace("\n", "")
            buf = buf.replace("\r", "")
            self.send_event(self.remote, "_Msg {}".format(buf))
        else:
            print(bufstr, end=end)


    def yes_no(self, bufstr, default=False):
        """ Get Yes or No
            Returns:
                Yes = True, No = False, Error = None
        """
        ans = default

        if self.remote != None:
            buf = bufstr.replace("\n", "")
            buf = buf.replace("\r", "")
            self.send_event(self.remote, "GetYesNo {}".format(buf))
            while True:
                stmsg = self.wait_for(r'^@GetYesNo')
                if stmsg == None:
                    if self.error != 'Timeout':
                        return None
                else:
                    return stmsg.parameters.upper() == 'Y'
        else:
            if ans:
                buf = "([y]/n)"
            else:
                buf = "(y/[n])"
            print("{} {} > ".format(bufstr, buf), end='')
            buf = input()
            return buf.upper() == 'Y'


    def die(self, bufstr='terminated'):
        """ Terminate the script
                bufstr   print out this string on the screen or remote node.
        """
        if self.remote != None:
            buf = bufstr.replace("\n", "")
            buf = buf.replace("\r", "")
            self.send_event(self.remote, "_Died {}".format(buf))
            print()
        else:
            print(bufstr)
        sys.exit()

    def exit(self, bufstr='terminated'):
        """ Terminate the script
                bufstr   print out this string on the screen or remote node.
        """
        self.die(bufstr)


if __name__ == '__main__':
    st = ScriptLib()
    for k in st.conf["scriptclient.cfg"]:
        for s in st.conf["scriptclient.cfg"][k]:
            print("[{}] {} = {}".format(k, s, st.conf["scriptclient.cfg"][k][s]))
