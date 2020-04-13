#
#STARS Python Interface
#2016-05-25 (Wed) T.Kosuge
#

import sys
import socket
import threading


DEFAULT_PORT    = 6057
DEFAULT_TIMEOUT =   10
TCP_BUFFER_SIZE = 4096


class StarsMessage(str):
    """STARS Message object
    """
    def __init__(self, message):
        self.allmessage = message
        try:
            mess   = message.split(' ', 2)
            fromto = mess[0].split('>')
            self.nodefrom   = fromto[0]
            self.nodeto     = fromto[1]
            self.command    = mess[1]
            if len(mess) > 2:
                self.parameters = mess[2]
            else:
                self.parameters = ''
        except:
            self.nodefrom   = ''
            self.nodeto     = ''
            self.command    = ''
            self.parameters = ''


class _CallbackThread(threading.Thread):
    """Thread for callback function. This function is internal.
    """
    def __init__(self, stars):
        threading.Thread.__init__(self)
        self.stars = stars

    def run(self):
        while True:
            rt = self.stars.receive(None)
            self.stars.callback(rt)
            if rt == '':
                break


class StarsInterface():
    """STARS Interface
    """
    def __init__(self, nodename, srvhost, keyfile = '', srvport = DEFAULT_PORT):
        self.nodename = nodename
        self.srvhost  = srvhost
        if keyfile == '':
            self.keyfile = nodename + '.key'
        else:
            self.keyfile  = keyfile
        self.srvport    = srvport
        self.keywords   = ''
        self.error      = ''
        self.readbuffer = ''


    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.srvhost, self.srvport))
        keynum = int(self.s.recv(TCP_BUFFER_SIZE).decode())
        node_and_key = self.nodename + ' ' + self._get_keyword(keynum) + '\n'
        self.s.sendall(node_and_key.encode())
        return self.s.recv(TCP_BUFFER_SIZE).decode()


    def disconnect(self):
        self.s.close()


    def _get_keyword(self, keynum):
        k = []
        if self.keywords != '':
            k = self.keywords.split()
        else:
            f = open(self.keyfile)
            k = f.readlines()
            f.close()
        p = k[keynum % len(k)]
        p = p.replace('\n', '')
        p = p.replace('\r', '')
        return p


    def send(self, arg1, arg2 = '', arg3 = ''):
        msg = ''
        if arg2 != '':
            if arg3 !='':
                msg = arg1 + '>' + arg2 + ' ' + arg3
            else:
                msg = arg1 + ' ' + arg2
        else:
            msg = arg1
        msg += '\n'
        self.s.sendall(msg.encode())


    def _process_message(self, msg):
        self.readbuffer += msg
        dp = self.readbuffer.find('\n')
        if dp < 0:
            return ''
        rtmess = self.readbuffer[:dp]
        self.readbuffer = self.readbuffer[dp+1:]
        return rtmess


    def receive(self, timeout = DEFAULT_TIMEOUT, exception = False):
        self.s.settimeout(timeout)
        while True:
            msg = ''
            if self.readbuffer == '':
                try:
                    msg = self.s.recv(TCP_BUFFER_SIZE).decode()
                except Exception:
                    if exception:
                        raise
                    else:
                        self.error = 'STARS recv Error: ' + str(sys.exc_info()[1])
                        return StarsMessage('')
            rtmsg = self._process_message(msg)
            if rtmsg != '':
                rtmsg = rtmsg.replace('\r', '')
                return StarsMessage(rtmsg)


    def start_cb_handler(self, callback):
        self.callback = callback
        th = _CallbackThread(self)
        th.setDaemon(True)
        th.start()

