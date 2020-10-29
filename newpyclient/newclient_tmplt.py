#!/usr/bin/python3
# STARS Client <<client_name>>
# <<Modified>>
#################################################################################
import sys
import time
import configparser
import stars

class <<client_name>>():
    def __init__(self, node, host, key, port):
        #add 'global' variables here like...
        #self.something = ''

        #STARS object
        self.st = stars.StarsInterface(node, host, key, port)

        # Use the follow value if you need interval function
        #self.intervaltime = 0.5

        #Enable debug print
        #self.st.setdebug(True)

    # Functions =================================================
    def _get_value(self):
        return "Ok:"

    def _set_value(self, sval):
        if sval == '':
            return "Er: Bad parameter."
        return "Ok: " + sval

    # Callback function
    #============================================================
    def cb_handler(self, mess):
        try:
            if mess == '':
                print("!!cb_handler() got " + self.st.getlasterrortext() + "\n")
                return
        except:
            return

        #Reply message
        if mess.command.startswith('@'):
            return

        #Event message
        if mess.command.startswith('_'):
            return

        #Command message
        if mess.nodeto == self.st.nodename:
            if mess.message == 'hello':
                rt = "nice to meet you."

            elif mess.message == 'help':
                rt = "hello help GetValue SetValue"

            elif mess.message == 'GetValue':
                rt = self._get_value()

            elif mess.command == 'SetValue':
                rt = self._set_value(mess.parameters)

            else:
                rt = "Er: Bad command or parameter."

            self.st.send(mess.nodefrom, "@{} {}".format(mess.command, rt))

        else:
            to = mess.nodeto.replace(self.st.nodename+'.', '')
            self.st.send(self.st.nodename, mess.nodefrom,
                 "@{} Er: {} is down.".format(mess.message, to))

    def run(self):
        # Connect to STARS server
        rtflag = self.st.connect()
        if rtflag is False:
            print(self.st.getlasterrortext()+ "\nBye.")
            exit(1)

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

            """
            time.sleep(self.intervaltime)
            # If you need interval funciton write codes here and comment out codes below

            """

            sbuf = sys.stdin.readline().rstrip('\n')
            if sbuf == 'quit':
                break
            elif sbuf == 'test':
                self.st.send(self.st.nodename, '_Test!!')

            #This sleep is for avoiding CPU load increasing in background.
            else:
                time.sleep(1)

        #============================================================
        self.st.disconnect()
        sys.stdout.write('Bye.\n')


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read("<<client_name>>.cfg")

    starshost = cfg["main"]["starsserver"]
    starsnode = cfg["main"]["mynodename"]
    starsport = cfg.getint("main", "starsport")
    starskey = cfg["main"]["keyfile"]
    #dpr       = cfg.getboolean("main", "debugprint")

    client = <<client_name>>(starsnode, starshost, starskey, starsport)
    client.run()
