#! /usr/bin/python3
"""
  STARS starsbridge python program
    Description: Connect to 2 STARS server and bridge the stars commands between 2 servers.
    History:
       0.1b     Beta version     2016.06.17    Yasuko Nagatani
       1.0      1st release      2016.08.24    1st Installed for KEK-PF SAX-BL
"""

# Define: program info
__author__ = 'Yasuko Nagatani'
__version__ = '1.0'
__date__ = '2016-08-24'
__license__ = 'KEK'

###############################################################################
# Main: Init section
###############################################################################
if __name__ == '__main__':
    ##################################################################
    # Define: import modules
    ##################################################################
    from sys import argv,stderr,exit,_getframe
    import stars
    from time import sleep,localtime,mktime,strftime
    import re
    from optparse import OptionParser
    from os import path
    import threading

    try:
        from configparser import ConfigParser, SafeConfigParser,NoSectionError
    except ImportError:
        try:
            from ConfigParser import ConfigParser, SafeConfigParser,NoSectionError
        except ImportError:
            stderr.write('Install configparser for python 3.x')
            stderr.write(', ConfigParser for python 2.x')
            exit(1)

    from logging import disable,getLogger,Formatter,StreamHandler,FileHandler,NOTSET,DEBUG,INFO,WARN,WARNING,ERROR,CRITICAL,FATAL,basicConfig
    try:
        from logging import Handler,NullHandler
    except ImportError:
        class NullHandler(Handler):
            def emit(self, record):
                pass

    ##################################################################
    # Define: program parameters
    ##################################################################
    # Define: Program parameters
    ScriptName = path.splitext(path.basename(argv[0]))[0]
    ScriptPath = path.dirname(path.abspath(argv[0]))
    Subversion = '$Id: starsbridge 00 2006-08-09 13:15:41 +0900 (Wed, 09  Aug 2006) stars $'
    ScriptCommandList = 'getsubversion terminate'

    # Define: Appliction default parameters
    StarsServerHost1 = 'localhost'
    StarsNodeName1   = 'stbr'
    StarsServerPort1 = 6057
    StarsServerHost2 = 'localhost'
    StarsNodeName2   = 'stbr2'
    StarsServerPort2 = 6057

    ##################################################################
    # Define: program options
    ##################################################################
    _optparser = OptionParser()
    #_optparser.add_option("-q", "--quiet", action="store_true" , dest="verbose",default=False, help="don't print status messages to stdout. Prior to -d|--debug")
    _optparser.add_option("-d", "--debug" , action="store_true" , dest="debug"  ,default=False, help="print debug messages to stdout.")
    _optparser.add_option("--debuglevel"  , type="int"          , dest="debuglevelnum"        , help="set level number of debug messages. Use with -d|--debug option")
    _optparser.add_option("--logenable"   , action="store_true" , dest="logenable"            , help="enable print messages to file.")
    _optparser.add_option("--loglevel"    , type="int"          , dest="loglevelnum"          , help="set level number of log messages. Use with --logenable")
    _optparser.add_option("--logdir"                            , dest="logdir"               , help="set directory of logging file.")
    _optparser.add_option("--config"                            , dest="config"               , help="set config file. Default: "+ 'config'+'.cfg on program folder.')

    _optparser.add_option("--nodename1",   dest="StarsNodeName1"              , help="set stars nodename for bridge side 1")
    _optparser.add_option("--serverhost1", dest="StarsServerHost1"            , help="set stars server ip or hostname for bridge side 1")
    _optparser.add_option("--serverport1", type="int", dest="StarsServerPort1", help="set stars server port no for bridge side 1")
    _optparser.add_option("--nodename2",   dest="StarsNodeName2"              , help="set stars nodename for bridge side 2")
    _optparser.add_option("--serverhost2", dest="StarsServerHost2"            , help="set stars server ip or hostname for bridge side 2")
    _optparser.add_option("--serverport2", type="int", dest="StarsServerPort2", help="set stars server port no for bridge side 2")

    ##################################################################
    # program functions: print,config
    ##################################################################
    # Define: print function
    def _outputlog(level, mesg, outstderronly=False):
        head = ScriptName

        if(outstderronly == True):
            if(mesg[-1:] != '\n'):
               mesg=mesg+'\n'
            stderr.write(mesg)
        else:
            logger.log(level,'['+ head + '] ' + mesg)
        return(1)

    # Define: config function
    def _readconfig(cfg, section, param):
        try:
            val=cfg.get(section,param)
        except:
            _outputlog(INFO, 'Configration skipped section='+section+' item='+param+'\n')
            return(None)
        return(val)

    ##################################################################
    # Define stars extention class:
    ##################################################################
    # Class: Stars callback handler
    class _myCallbackThread(threading.Thread):
        """Thread for callback function. This function is internal.
        """
        def __init__(self, stars):
            threading.Thread.__init__(self)
            self.stars = stars
            self.stars._running = True
            self.stars._callbacktime = localtime()

        def run(self):
            while self.stars._running:
                rt = self.stars.receive(None)
                self.stars.callback(rt)
                self.stars._callbacktime = localtime()
                if rt == '':
                    break
            self.stars._running = False

    # Class: Stars callback start handler
    class myStarsInterface(stars.StarsInterface):
        def __init__(self, nodename, srvhost, keyfile, srvport):
            if(srvport is None):
                stars.StarsInterface.__init__(self, nodename, srvhost, keyfile)
            else:
                stars.StarsInterface.__init__(self, nodename, srvhost, keyfile, srvport)

        def mystart_cb_handler(self, callback):
            self.callback = callback
            th = _myCallbackThread(self)
            th.setDaemon(True)
            th.start()

    ##################################################################
    # Define stars local functions:
    ##################################################################
    ## Stars Connect
    def mystarsconnect(mynodename = '', mystarsserver = '', keyfile = '', srvport = None, outstderr = False):
        """ Stars connect local function
        """
        if(mynodename == ''):
            _outputlog(ERROR, 'Failed to connect to ' + mystarsserver + '. Undefined nodename.', outstderr)
            return(None)
#    if(keyfile == ''):
#        if(path.exists(mynodename+'.key') == False):
#            _outputlog(ERROR, 'Failed to connect to ' + mystarsserver + ' as ' + mynodename + '. Keyfile not found.[' + mynodename + '.key]', outstderr)
#            return(None)
        si = myStarsInterface(mynodename, mystarsserver, keyfile, srvport)
        # Connect to starsserver
        try:
            msg = si.connect()
            if(msg.count(' Er:')):
                _outputlog(ERROR,'Failed to connect to ' +  mystarsserver + ' as ' + mynodename + '. Message=[' + msg.strip() + ']', outstderr)
                mystarsdisconnect(si)
                return(None)
        except Exception:
            _outputlog(ERROR,'Failed to connect to ' +  mystarsserver + ' as ' + mynodename + '. Message=[' + si.error + ']', outstderr)
            return(None)
        _outputlog(INFO,'Connected to ' + mystarsserver + ' as ' + mynodename + '.')
        return(si)

    ## Stars Disconnect
    def mystarsdisconnect(si, outstderr=False):
        """ Stars disconnect local function
        """
        mystarsstopcallback(si)
        if(mystarsisconnect(si) == 1):
            try:
                si.disconnect()
                _outputlog(INFO,'Disconnected ' + si.nodename + ' from ' + si.srvhost, outstderr)
                del si.s
                del si
            except Exception:
                del si.s
                del si
            si = None
        return(1)

    ## Stars Stop callback
    def mystarsstopcallback(si):
        """ Stars stop callback local function
        """
        if(hasattr(si,'_running')):
            si._running = False
            sleep(0.2)
        return(1)

    ## Stars Isconnect
    def mystarsisconnect(si):
        """ Stars check connect or not local function
        """
        if(si == None):
            return(0);
        elif hasattr(si,'s'):
            return(1);
        return(0);

    ## Stars send function with try-exception
    def mystarssend(si, mess):
        """ Stars send local function
        """
        if(mystarsisconnect(si) == 1):
            try:
                _outputlog(INFO, mess)
                si.send(mess)
            except Exception:
                _outputlog(WARNING, '[' + si.nodename + '] '+ '[' + _getframe().f_code.co_name + '] Message=[' + mess + '] si.error=[' + si.error + ']')
                return(0)
        return(1)

    ## Stars message hander function for StarsServerHost1
    def sub_starshandler_server(si, di, allmess):
        """ Stars handler local function
        """
        destsendstr='';
        selfsendstr='';

        if allmess == '':
            _outputlog(WARNING, '[' + si.nodename + '] ' + '[' + _getframe().f_code.co_name + '] si.error=[' + si.error + ']')
            mystarsstopcallback(si)
            return(0)
        elif(allmess.parameters == ''):
            message = allmess.command
        else:
            message = allmess.command + ' ' + allmess.parameters
        _outputlog(INFO, '[' + si.nodename + '] ' + allmess)

        # Send from System
        if(allmess.nodefrom == 'System'):
            # Send to Me
            if allmess.nodeto == si.nodename:
                # Reply message: just ignore
                if message.startswith('@'):
                    _outputlog(DEBUG, '[' + si.nodename + '] Ignored current. ' + allmess)
                # Event message: ignore, event message from node system never comes
                elif message.startswith('_'):
                    _outputlog(DEBUG, '[' + si.nodename + '] Ignored current. ' + allmess)
                # Command message: ignore, command request from node system never comes
                else:
                    _outputlog(WARNING, '[' + si.nodename + '] Unexpected. ' + allmess)

            # Send back to client with System alias
            elif allmess.nodeto.startswith(si.nodename + '.System.'):
                buf = allmess.nodeto.replace(si.nodename + '.System.', '')
                if(buf == ''):
                    # Reply message: ignore, bad nodename.
                    # Event message: ignore, bad nodename
                    # Command message: ignore, bad nodename.
                    _outputlog(WARNING, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')
                else:
                    # Reply message from system: send back 
                    if message.startswith('@'):
                        if(message.startswith('@help ')):
                            destsendstr = di.nodename + '.System>' + buf + ' ' + message
                        else:
                            destsendstr = di.nodename + '.System>' + buf + ' ' + message
                    # Event message: ignore, event message from node system never comes
                    # Command message: ignore, command request from node system never comes
                    else:
                        _outputlog(WARNING, '[' + si.nodename + '] Unexpected. ' + allmess)

            # Send back to client
            elif allmess.nodeto.startswith(si.nodename + '.'):
                buf = allmess.nodeto.replace(si.nodename + '.', '')
                if(buf == ''):
                    # Reply message: ignore, bad nodename.
                    # Event message: ignore, bad nodename
                    # Command message: ignore, bad nodename.
                    _outputlog(WARNING, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')
                else:
                    # Reply message from system: send back 
                    if message.startswith('@'):
                        if(message.startswith('@help ')):
                            destsendstr = di.nodename + '.System>' + buf + ' ' + message + ' ' + ScriptCommandList
                        else:
                            destsendstr = di.nodename + '>' + buf + ' ' + message
                    # Event message: ignore, event message from node system never comes
                    # Command message: ignore, command request from node system never comes
                    else:
                        _outputlog(WARNING, '[' + si.nodename + '] Unexpected. ' + allmess)

            # Unknown dest
            else:
                # Reply message: ignore, bad nodename.
                # Event message: ignore, bad nodename
                # Command message: ignore, bad nodename.
                _outputlog(DEBUG, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')
        else:
            # Send to Me
            if allmess.nodeto == si.nodename:
                # Reply message @hello: send _Connected to System
                if message.startswith('@hello'):
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + '_Connected'
                # Other reply message: ignore
                elif message.startswith('@'):
                    _outputlog(DEBUG, '[' + si.nodename + '] Ignored current. ' + allmess)
                # Event message: send to System
                elif message.startswith('_'):
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + message
                # Command to me:
                elif message == 'terminate':
                    mystarsstopcallback(si)
                    return(0)
                # Command flgon: send to System
                elif allmess.command == 'flgon':
                    buf2 = allmess.parameters.strip()
                    if(buf2.startswith(si.nodename + '.')):
                        buf2 = buf2.replace(si.nodename + '.', '')
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + 'flgon ' + buf2
                # Command flgoff: send to System
                elif allmess.command == 'flgoff':
                    buf2 = allmess.parameters.strip()
                    if(buf2.startswith(si.nodename + '.')):
                        buf2.replace(si.nodename + '.', '')
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + 'flgoff ' + buf2
                # Command local: getversion
                elif message == 'getversion':
                    selfsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + __version__
                elif message == 'getsubversion':
                    #mybuf = Subversion.replace('$','')
                    mybuf = Subversion
                    selfsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + mybuf
                # Command message: send to System
                else:
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + message

            # Send to dest System
            elif allmess.nodeto == si.nodename + '.System':
                # Event message: ignore, reply to node system never comes
                if message.startswith('@'):
                    _outputlog(WARNING, '[' + si.nodename + '] Unexpected. ' + allmess)
                # Event message: send to System
                elif message.startswith('_'):
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + message
                # Command flgon: send to System
                elif allmess.command == 'flgon':
                    buf2 = allmess.parameters.strip()
                    if(buf2.startswith(si.nodename + '.')):
                        buf2 = buf2.replace(si.nodename + '.', '')
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + 'flgon ' + buf2
                # Command flgoff: send to System
                elif allmess.command == 'flgoff':
                    buf2 = allmess.parameters.strip()
                    if(buf2.startswith(si.nodename + '.')):
                        buf2.replace(si.nodename + '.', '')
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>System ' + 'flgoff ' + buf2
                # Command message: send to System
                else:
                    destsendstr = di.nodename + '.System.' + allmess.nodefrom + '>System ' + message

            # Send to dest System
            elif allmess.nodeto.startswith(si.nodename + '.System.'):
                buf = allmess.nodeto.replace(si.nodename + '.System.', '')
                # Event message: ignore, reply to node system never comes
                if message.startswith('@'):
                    _outputlog(WARNING, '[' + si.nodename + '] Unexpected. ' + allmess)
                # Event message: send to System
                elif message.startswith('_'):
                    destsendstr = di.nodename + '.System.' + allmess.nodefrom + '>' + buf + ' ' + message
                # Command message: send to System
                else:
                    destsendstr = di.nodename + '.System.' + allmess.nodefrom + '>' + buf + ' ' + message

            # Send to client with System alias
            elif allmess.nodeto.startswith(si.nodename + '.'):
                buf = allmess.nodeto.replace(si.nodename + '.', '')
                if(buf == ''):
                    # Reply message: ignore, bad nodename.
                    if message.startswith('@'):
                        _outputlog(WARNING, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')
                    # Event message: ignore, bad nodename
                    elif message.startswith('_'):
                        _outputlog(WARNING, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')
                    # Command message: ignore, bad nodename.
                    else:
                        selfsendstr = si.nodename + '>' + allmess.nodefrom + ' ' + message + ' Er: Bad node. Nodename[' + allmess.nodeto + ']'
                else:
                    # Reply message : send back 
                    # Event message: send back
                    # Command message: send back
                    destsendstr = di.nodename + '.' + allmess.nodefrom + '>' + buf + ' ' + message

            # Unknown dest
            else:
                # Reply message: ignore, bad nodename.
                # Event message: ignore, bad nodename
                # Command message: ignore, bad nodename.
                _outputlog(WARNING, '[' + si.nodename + '] Unexpected. toNode invalid. nodeto[' + allmess.nodeto + ']')

        if(destsendstr != ''):
            _outputlog(INFO, '[' + di.nodename + '] ' + destsendstr)
            rt = mystarssend(di, destsendstr)
            if(rt<=0):
                mystarsstopcallback(di)
        if(selfsendstr != ''):
            _outputlog(INFO, '[' + si.nodename + '] ' + selfsendstr)
            rt = mystarssend(si, selfsendstr)
            if(rt<=0):
                mystarsstopcallback(si)
        return(1)

    ## Stars message hander function for StarsServerHost1
    def starshandler_server1(allmess):
        """ Stars set handler for StarsServer1 local function
        """
        si = st
        di = st2
        sub_starshandler_server(si, di, allmess)

    ## Stars message hander function for StarsServerHost2
    def starshandler_server2(allmess):
        """ Stars set handler for StarsServer2 local function
        """
        si = st2
        di = st
        sub_starshandler_server(si, di, allmess)

    ##################################################################
    # Init: application parameters
    ##################################################################
    # Load options
    (_opthandle, args) = _optparser.parse_args()

    # Read config: Configfile name
    _confighandle = None
    if(_opthandle.config is not None):
        _configfile = _opthandle.config
        if(path.exists(_configfile) == True):
            if(path.isfile(_configfile) == True):
                _confighandle = SafeConfigParser()
                _confighandle.read(_configfile)
            else:
                stderr.write('Option --config: Config is not file. [' + _opthandle.config + ']')
                exit(1)
        else:
            stderr.write('Option --config: Config file not found. [' + _opthandle.config + ']')
            exit(1)
    else:
        #_configfile = ScriptPath + '/' + ScriptName + '.cfg'
        _configfile = ScriptPath + '/' + 'config.cfg'
        if(path.exists(_configfile) == True):
            if(path.isfile(_configfile) == True):
                _confighandle = SafeConfigParser()
                _confighandle.read(_configfile)

    # Read config: STARS section
    if(_confighandle is not None):
        # Read config: STARS section
        v=_readconfig(_confighandle, 'STARS', 'StarsServerHost1')
        if(v is not None):
            StarsServerHost1 = v
        v=_readconfig(_confighandle, 'STARS', 'StarsNodeName1')
        if(v is not None):
            StarsNodeName1=v
        v=_readconfig(_confighandle, 'STARS', 'StarsServerPort1')
        if(v is not None):
            StarsServerPort1=int(v)
        v=_readconfig(_confighandle, 'STARS', 'StarsServerHost2')
        if(v is not None):
            StarsServerHost2 = v
        v=_readconfig(_confighandle, 'STARS', 'StarsNodeName2')
        if(v is not None):
            StarsNodeName2=v
        v=_readconfig(_confighandle, 'STARS', 'StarsServerPort2')
        if(v is not None):
            StarsServerPort2=int(v)

    # Store STARS options
    if(_opthandle.StarsNodeName1 is not None):
        StarsNodeName1 = _opthandle.StarsNodeName1
    if(_opthandle.StarsServerHost1 is not None):
        StarsServerHost1 = _opthandle.StarsServerHost1
    if(_opthandle.StarsServerPort1 is not None):
        StarsServerPort1 = _opthandle.StarsServerPort1
    if(_opthandle.StarsNodeName2 is not None):
        StarsNodeName2 = _opthandle.StarsNodeName2
    if(_opthandle.StarsServerHost1 is not None):
        StarsServerHost2 = _opthandle.StarsServerHost2
    if(_opthandle.StarsServerPort1 is not None):
        StarsServerPort2 = _opthandle.StarsServerPort2

    # Set logging options
    _printsflg   = False
    _printslevel = DEBUG
    _printfflg   = False
    _printflevel = DEBUG
    _printflogdir=ScriptPath
    
    if(_opthandle.debug == True):
        _printslevel = DEBUG
        if(_opthandle.debuglevelnum is not None):
            _printslevel = _opthandle.debuglevelnum
        _printsflg = True

    if((_opthandle.logenable is not None) and (_opthandle.logenable == True)):
        if(_opthandle.logdir is not None):
            if(path.exists(_opthandle.logdir) == True):
                _printflogdir=_opthandle.logdir
                _printfflg = True
            else:
                stderr.write('Option --logdir: directory not found. [' + _opthandle.logdir + ']')
                exit(1)
        else:
            _printfflg = True
        if(_opthandle.loglevelnum is not None):
            _printflevel = _opthandle.loglevelnum

    LogfileName = _printflogdir + '/' + StarsNodeName1 + 'log' + strftime('%Y-%m-%d',localtime()) + '.txt'
    logger = getLogger(__name__)
    if((_printfflg == True) and (_printsflg == True)):
        if(_printflevel < _printslevel):
            logger.setLevel(_printflevel)
        else:
            logger.setLevel(_printslevel)

        fstream = FileHandler( LogfileName )
        fstream.setLevel(_printflevel)
        formatter = Formatter('[%(asctime)s]%(message)s')
        fstream.setFormatter(formatter)
        logger.addHandler(fstream)
        
        console = StreamHandler()
        console.setLevel(_printslevel)
        formatter = Formatter('[%(asctime)s]%(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)
            
    elif(_printsflg == True):
        logger.setLevel(_printslevel)

        console = StreamHandler()
        console.setLevel(_printslevel)
        formatter = Formatter('[%(asctime)s]%(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)
    elif(_printfflg == True):
        logger.setLevel(_printflevel)

        fstream = FileHandler( LogfileName )
        fstream.setLevel(_printflevel)
        formatter = Formatter('[%(asctime)s]%(message)s')
        fstream.setFormatter(formatter)
        logger.addHandler(fstream)
    else:
        logger.addHandler(NullHandler())

    ##################################################################
    # Main process: Start
    ##################################################################
    ### Init,stars
    st = mystarsconnect(StarsNodeName1, StarsServerHost1, '', StarsServerPort1, True)
    if(st is None):
        #mystarsdisconnect(st2)
        exit(1)

    st2 = mystarsconnect(StarsNodeName2, StarsServerHost2, '', StarsServerPort2, True)
    if(st2 is None):
        mystarsdisconnect(st)
        exit(1)

    #Read config: nodename section
    if(_confighandle is not None):
        # Read config of STARS section
        v=_readconfig(_confighandle, StarsNodeName1, 'autoflgonlist')
        if(v is not None):
            for item in v.splitlines():
                rt = mystarssend(st, st.nodename + '>System flgon ' + item)
        v=_readconfig(_confighandle, StarsNodeName1, 'postautoflgoncommandlist')
        if(v is not None):
            for item in v.splitlines():
                rt = mystarssend(st, item)
                
        v=_readconfig(_confighandle, StarsNodeName2, 'autoflgonlist')
        if(v is not None):
            for item in v.splitlines():
                rt = mystarssend(st2, st2.nodename + '>System flgon ' + item)
        v=_readconfig(_confighandle, StarsNodeName2, 'postautoflgoncommandlist')
        if(v is not None):
            for item in v.splitlines():
                rt = mystarssend(st2, item)

    st.mystart_cb_handler(starshandler_server1)
    st2.mystart_cb_handler(starshandler_server2)

    #_outputlog(INFO, 'Enter quit to quit.')

    ### Handle thread
    myintervalsec = 5
    sleepsec = 0.1
    cnt = 0
    timecheck1 = mktime(localtime())
    timecheck2 = mktime(localtime())

    while True:
        if(_printfflg == True):
            mybuf = _printflogdir + '/' + StarsNodeName1 + 'log' + strftime('%Y-%m-%d',localtime()) + '.txt'
            if(mybuf != LogfileName):
                for hdlr in logger.handlers:
                    if(type(hdlr) == FileHandler):
                        logger.removeHandler(hdlr)
                        fstream = FileHandler( mybuf )
                        fstream.setLevel(_printflevel)
                        formatter = Formatter('[%(asctime)s]%(message)s')
                        fstream.setFormatter(formatter)
                        logger.addHandler(fstream)
                        LogfileName=mybuf

        # Interval check
        if(cnt>=(myintervalsec/sleepsec)):
            timecheck1 = mktime(localtime())
            timecheck2 = mktime(localtime())
            if(hasattr(st,'_callbacktime')):
                if((timecheck1-mktime(st._callbacktime))>=myintervalsec):
                    rt = mystarssend(st, st.nodename + '.' + 'System' + '>System _alive')
                    if(rt <= 0):
                        mystarsstopcallback(st)
                        #break

            if(hasattr(st2,'_callbacktime')):
                if((timecheck2-mktime(st._callbacktime))>=myintervalsec):
                    rt = mystarssend(st2, st2.nodename + '.' + 'System' + '>System _alive')
                    if(rt <= 0):
                        mystarsstopcallback(st2)
                        #break
            cnt = 0

        # check thread running
        if(hasattr(st,'_running')):
            #_outputlog(DEBUG, 'Running1')
            if(st._running == False):
                break
        if(hasattr(st2,'_running')):
            #_outputlog(DEBUG, 'Running2')
            if(st2._running == False):
                break

        cnt = cnt + 1
        try:
            sleep(sleepsec)
        except KeyboardInterrupt:
            break
            

    ### Final
    mystarsdisconnect(st)
    mystarsdisconnect(st2)
    _outputlog(INFO, 'Bye.')
    exit(0)
