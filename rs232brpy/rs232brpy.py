#!/usr/bin/python3
# STARS Client rs232brpy
# 2026-06-02 15:23:55 Generated.
__author__ = 'Takashi Kosuge'
__version__ = '1.0'
__date__ = '2026-06-02 (Tue)'
#################################################################################
import sys
import time
import configparser
import stars

class rs232brpy():
    def __init__(self, node, host, key, port, serial, debug=False):
        #add 'global' variables here like...
        #self.something = ''
        
        self.serial = serial
        
        #STARS object
        self.st = stars.StarsInterface(node, host, key, port)
        
        # Use the follow value if you need interval function
        self.intervaltime = 0.5
        
        self.debug = debug
        
        #Enable debug print of stars
        if self.debug:
            self.st.setdebug(True)

    # Functions =================================================
    def _debugprint(self, pstr):
        if self.debug:
            print(pstr)

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
        
        #Command message
        if mess.nodeto == self.st.nodename:
            #Reply message to me
            if mess.command.startswith('@'):
                return
            
            #Event message to me
            if mess.command.startswith('_'):
                return
            
            if mess.message == 'hello':
                rt = "nice to meet you."
            
            elif mess.message == 'help':
                rt = "hello help getversion"
            
            elif mess.message == 'getversion':
                rt = __version__
            
            else:
                rt = "Er: Bad command or parameter."
            
            self.st.send(mess.nodefrom, "@{} {}".format(mess.command, rt))
            
        else:
            to = mess.nodeto.replace(self.st.nodename+'.', '')
            serial_mess = "{}>{} {}".format(mess.nodefrom, to, mess.message)
            self.serial.send(serial_mess)
            self._debugprint("[Serial out] "+serial_mess)
        
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

        # Interval or waiting for keyboard input
        #============================================================
        while True:
            if self.st.iscallbackrunning() is False:
                print("!!Callback stopped!!")
                break

            #time.sleep(self.intervaltime)
            
            # Read from serial
            while True:
                rt = self.serial.receive()
                if rt != "":
                    self._debugprint("[Serial in] {}".format(rt))
                    smess = stars.StarsMessage(rt)
                    if smess.nodefrom == '' or smess.nodeto == '' or smess.message == '':
                        self._debugprint("Serial message Error")
                        continue
                    self.st.send("{}.{}>{} {}".format(self.st.nodename, smess.nodefrom, smess.nodeto, smess.message))


            # If you need block intervel until gets some string from STDIN...
            """
            sbuf = sys.stdin.readline().rstrip('\n')
            if sbuf == 'quit':
                break
            elif sbuf == 'test':
                self.st.send(self.st.nodename, '_Test!!')

            #This sleep is for avoiding CPU load increasing in background.
            else:
                time.sleep(1)
            """

        #============================================================
        self.st.disconnect()
        sys.stdout.write('Bye.\n')


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read("rs232brpy.cfg")

    starshost = cfg["main"]["starsserver"]
    starsnode = cfg["main"]["mynodename"]
    starsport = cfg.getint("main", "starsport")
    starskey = cfg["main"]["keyfile"]
    #dpr       = cfg.getboolean("main", "debugprint")
    use_nport = cfg.getboolean("main", "use_nport")
    
    if use_nport:
        import nportserv
        serial = nportserv.nportserv(cfg["nport"]["host"], cfg.getint("nport", "port"))
        if not serial.connect():
            print("Error: {}".format(serial.error))
            exit()
    
    else:
        import pfipyserial
        serial = pfipyserial.PfiPySerial("rs232brpy.cfg")
    
    client = rs232brpy(starsnode, starshost, starskey, starsport, serial)
    print("Start RS232 Bridge Version: {} {}".format(__version__, __date__))
    client.run()
