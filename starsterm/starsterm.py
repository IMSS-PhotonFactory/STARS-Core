#!/usr/bin/python3
# STARS Client starsterm
# 2024-07-24 16:55:20 Generated.
#################################################################################
# Define: program info
__author__ = 'T.Kosuge'
__version__ = '1.1'
__date__ = '2025-09-16'
__license__ = 'MIT'

import time
import configparser
import argparse
import re
import stars

class starsterm():
    def __init__(self, args, cfg):
        #add 'global' variables here like...
        #self.something = ''
        self.cmd = cfg["commands"]

        if args.nodename == None:
            node = input("Nodename: ")
            key = ""
        else:
            node = args.nodename
            key = node + ".key"

        if args.server == None:
            host = cfg["main"]["starsserver"]
        else:
            host = args.server

        if args.port == None:
            port = cfg.getint("main", "starsport")
        else:
            port = args.port

        #STARS object
        self.st = stars.StarsInterface(node, host, key, port)

        if key == "":
            self.set_keywords(input("Keyword: "))

        # Use the follow value if you need interval function
        self.intervaltime = 0.5

        #Enable debug print
        #self.st.setdebug(True)

    # Functions =================================================
    def set_keywords(self, keywords):
        self.st.keywords = keywords

    def get_keywords(self):
        return self.st.keywords

    #handle commands from stdin, command starts with ">".
    def _cmd_handler(self, cmd):
        if cmd == 'h':
            print("* The message will be sent to STARS server.")
            print("* Previous message will be sent if press just <Enter> key.")
            print("* \">string [param(s)_$1..$9]\" calls shortcut.")
            print("== Short cuts ==")
            for k in self.cmd:
                print(">{:10s} {}".format(k, self.cmd[k]))
            return None
        else:
            params = cmd.split(' ')
            plen = len(params)
            if plen == 0:
                return None
            if not params[0] in self.cmd:
                print("Short cut \"{}\" is not found".format(params[0]))
                return None
            mess = self.cmd[params[0]]
            for pn in range(1, plen):
                if pn > 9:
                    break
                mess = mess.replace("${}".format(pn), params[pn])
            if re.search('r\$\d+', mess):
                print("Error: parameter is not enough.: {}".format(mess))
                return None
            return mess

    # Callback function
    #============================================================
    def cb_handler(self, mess):
        print(mess.allmessage)

        try:
            if mess == '':
                print("!!cb_handler() got " + self.st.getlasterrortext())
                print("Press enter.")
                return
        except:
            return

    def run(self):
        prompt = "Enter STARS messge. (Enter \">h\" if you need help.)"
        prev_mess = ""
        # Connect to STARS server
        rtflag = self.st.connect()
        if rtflag is False:
            print("Connection error: " + self.st.getlasterrortext() + "\nBye.")
            exit(1)
        print("Connected.\n" + prompt)

        #============================================================
        # Start receive waiting thread
        self.st.start_cb_handler(self.cb_handler)
        # Wait 0.5 seconds to make return value of iscallbackrunning() True
        time.sleep(0.5)

        # Interval or waiting for keybord input
        #============================================================
        while True:
            if self.st.iscallbackrunning() is False:
                print("!!Callback stopped!!")
                break

            sbuf = input()
            if re.match(">", sbuf):
                mess = self._cmd_handler(sbuf[1:])
                if(mess == None):
                    print(prompt)
                    prev_mess = ""
                else:
                    print(mess)
                    self.st.send(mess)
                    prev_mess = mess
            elif sbuf == "":
                if prev_mess != "":
                    print(prev_mess)
                    self.st.send(prev_mess)
            else:
                self.st.send(sbuf)
                prev_mess = sbuf

        #============================================================
        self.st.disconnect()
        print('Bye.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nodename', nargs = '?', help = "MyNodename. \"nodename.key\" will be used as a keyword file.")
    parser.add_argument('-s', '--server', help = "hostname or IP address of STARS server")
    parser.add_argument('-p', '--port', type = int, help = "STARS port number")

    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("starsterm.cfg")

    #dpr       = cfg.getboolean("main", "debugprint")
    print("STARS terminal client Ver. {}".format(__version__))
    client = starsterm(args, cfg)
    client.run()
