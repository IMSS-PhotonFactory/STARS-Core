#! /usr/bin/python3
"""
  STARS python program Tsuji Electronics Co.,Ltd. Counter-Timer data receiver module.
    History:
       0.1     Beta           2018.8.20      Yasuko Nagatani

"""

# Define: program info
__author__ = 'Yasuko Nagatani'
__version__ = '0.1'
__date__ = '2018-8-20'
__license__ = 'MIT'

#----------------------------------------------------------------
# Import modules
#----------------------------------------------------------------
import sys
import os
import nportserv
import re
import time
from singlestars import StarsInterface
from stars import StarsMessage
import threading
import time

#----------------------------------------------------------------
# Class(Internal) Process to monitor data coming.
#----------------------------------------------------------------
class _CallbackThread(threading.Thread):
    def __init__(self, nportinstance):
        threading.Thread.__init__(self)
        self.nportinstance = nportinstance
        self.nportinstance._callbackrunning = False
        self.nportinstance._callbacktime = time.localtime()
        self.nportinstance.sendcommand = ''
        self.nportinstance.replymessage = ''
        self.nportinstance._downloadisbusy = False

    def run(self):
        self.nportinstance._callbackrunning = True
        self.nportinstance.setdebug(False)
        rt = True
        while self.nportinstance._callbackrunning:
            self.nportinstance.setdebug(False)
            rt = self.nportinstance.receive(0.01,None,None)
            if(rt is None):
                break
            if(rt == ''):
                if(self.nportinstance.sendcommand != ''):
                    self.nportinstance.setdebug(True)
                    rt=self.nportinstance.send(self.nportinstance.sendcommand)
                    if(rt==False):
                        self.nportinstance.replymessage = None
                        rt = None
                        break
                    if(self.nportinstance.sendcommand[-1] == '?'):
                        rt=self.nportinstance.receive(delimiter='\r\n')
                        if(rt==None):
                            self.nportinstance.replymessage = None
                            break
                        self.nportinstance.replymessage = rt
                    else:
                        self.nportinstance.replymessage = 'Ok:'
                    #print("RCV#"+self.nportinstance.sendcommand+"#"+self.nportinstance.replymessage+"\n")
                    self.nportinstance.sendcommand = ''
                continue
            self.nportinstance._callbacktime = time.localtime()
            self.nportinstance.callback(rt,self.nportinstance)
        if((rt is not None)):
            if(self.nportinstance._downloadisbusy == True):
                self.nportinstance._downloadisbusy = False
                self.nportinstance.send('STOP')
        self.nportinstance.sendcommand = ''
        self.nportinstance._callbackrunning = False

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERGateStatus
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERGateStatus(str):
    """ PyStarsDeviceTSUJICOUNTERTIMERGateStatus: Channel status object.
    """
    def __init__(self, statusstr):
        self.status = statusstr
        self.has_error = True
        self.error = ''
        self.gate_converting = 0
        self.gate_running = 0

        m = re.search("^(GATE|TIMER|GATE EDGE) MODE ON\Z", statusstr.upper())
        if m:
            self.gate_running = 1
            self.has_error = False
        elif(statusstr.upper() == 'NOW HEX CONVERSION'):
            self.gate_converting = 1
            self.gate_running = 1
            self.has_error = False
        elif(statusstr.upper() == 'GATE MODE OFF'):
            self.has_error = False
        else:
            rt="Status reply error ('%s'). Unexpected reply format." %(statusstr)
            self.error = "%s" %(rt)

class PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommandLevel:
    CONTROLLER, CHANNEL = range(1,3)

class PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand():
    """ PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand: Device command object.
    """
    def __init__(self, commandtag, ishelponly=False, ischannelcommand=False, isglobalcommand=True, islockcommand=False, isunlockcommand=False, isreferencecommand=True, ismotioncommand=False, readeod = '', argnum = 0, replytag=None, isallowbusy=True, checkfunc=None, postfunc=None, postwaittime=0, helpstring="-"):
        self.commandtag  = commandtag
        self.ishelponly = ishelponly
        self.ischannelcommand = ischannelcommand
        self.islockcommand = islockcommand
        self.isunlockcommand = isunlockcommand
        self.isglobalcommand = isglobalcommand
        self.isreferencecommand = isreferencecommand
        self.ismotioncommand = ismotioncommand
        self.readeod = readeod
        if(replytag == ''):
            self.replytag = None
        else:
            self.replytag = replytag
        self.ischeckargnum = True
        self.argnum = argnum
        if(argnum is None):
            self.argnum = -1
        if(self.argnum<0):
            self.ischeckargnum = False
        self.isallowbusy = isallowbusy
        self.checkfunc = checkfunc
        self.postfunc = postfunc
        self.postwaittime = postwaittime
        self.helpstring = helpstring

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADER
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADER(nportserv.nportserv):
    ## Device recv
    def device_receive(self, timeout='',eod=''):
        rt = ''
        if(self.isconnected()==False):
            return 'Er: Disconnected'
        if(timeout==''):
            timeout=self.gettimeout()
        if(eod == ''):
            rt=self.receive(timeout)
            if(rt is None):
                return 'Er: ' + self.getlasterrortext()
        else:
            while(1):
                rt2=self.receive(timeout,delimiter=eod)
                if(rt2 is None):
                    return 'Er: ' + self.getlasterrortext()
                if(rt2 == ''):
                    continue
                rt = rt + rt2
                break
        return rt

    def start_nb_handler(self, callback):
        self.callback = callback
        th = _CallbackThread(self)
        th.setDaemon(True)
        th.start()

    def iscallbackrunning(self):
        return(self._callbackrunning)

    def device_init(self, useAsSTARSClient=False):
        self._callbackrunning = False
        if(useAsSTARSClient==True):
            lc_deviceSTARSCommand = self._deviceSTARSCommand
            lc_deviceSTARSCommand['hello']                =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return 'hello nice to meet you.'")
            lc_deviceSTARSCommand['help']                 =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the list or the explanation of stars command.")
            lc_deviceSTARSCommand['getversion']           =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return this program version.")
            lc_deviceSTARSCommand['getversionno']         =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the version number of this program.")
            lc_deviceSTARSCommand['terminate']            =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Terminate this program.")
            lc_deviceSTARSCommand['IsBusy']               =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the busy status.")
            lc_deviceSTARSCommand['Stop']                 =PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Stop the controller immediately.")
            self._deviceSTARSCommand = lc_deviceSTARSCommand

    ##################################################################
    # Initialize
    ##################################################################
    def __init__(self, deviceHost, devicePost, inthandler=None):
        self._deviceInstance = nportserv.nportserv.__init__(self, deviceHost, devicePost)
        #self.setsenddelimiter('\n')
        self.setrecvdelimiter('')
        self.settimeout(2)

        ##################################################################
        # Define command definitions
        ##################################################################
        lc_deviceSTARSCommand = {}

        #-------------------#
        # Download commands #
        #-------------------#
        lc_deviceSTARSCommand['GateDownloadStart']     = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, ismotioncommand=True, helpstring="Start the gate synchronous data acquisition download.")
        lc_deviceSTARSCommand['GateEdgeDownloadStart'] = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, ismotioncommand=True, helpstring="Start the gate edge synchronous data acquisition download.")
        lc_deviceSTARSCommand['TimerDownloadStart']    = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, ismotioncommand=True, helpstring="Start the gate timer synchronous data acquisition download.")
        lc_deviceSTARSCommand['GateDownloadStop']      = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Stop the download of gate synchronous data acquisition.")
        lc_deviceSTARSCommand['GateEdgeDownloadStop']  = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Stop the download of gate edge synchronous data acquisition.")
        lc_deviceSTARSCommand['TimerDownloadStop']     = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Stop the download of timer synchronous data acquisition.")
        lc_deviceSTARSCommand['DelayStop']             = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Stop the controller after delay(sec).")
        lc_deviceSTARSCommand['IsDownloadBusy']        = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Return the download busy status.")
        lc_deviceSTARSCommand['GetDownloadedCount']    = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADERDeviceCommand('', ishelponly=True, ischannelcommand=False,  isglobalcommand=True, helpstring="Return the count of downloaded data after download started.")

        self._deviceSTARSCommand = lc_deviceSTARSCommand

    ##################################################################
    # Command functions
    ##################################################################
    def devicecommandobject(self,starscommand):
        rt = None
        if(starscommand in self._deviceSTARSCommand):
            rt = self._deviceSTARSCommand[starscommand]
        return(rt)

#######################################
## STARS interval handler:
#######################################
def interval():
    download_interval()

def download_interval():
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_DeviceDownloadInstance
    global gb_DeviceSendDateisgaterunning;
    st = gb_StarsInstance
    if(gb_DeviceDownloadInstance._callbackrunning == False):
        st.terminateMainloop()
        return
    device_checkstopdelay()
    if(gb_DeviceInstance is None):
        return
    modinterval=3
    if(device_getdownloadflgbusy()==1):
        modinterval=0.2
    if((time.time()-gb_DeviceReplyDateisgaterunning)>=modinterval):
        if(gb_DeviceSendDateisgaterunning<=gb_DeviceReplyDateisgaterunning):
            #### Check Counter is converting.
            rt=gb_DeviceInstance.send('GSTS?')
            if(rt==False):
                return
            gb_DeviceSendDateisgaterunning=time.time()
    return

##################################################################
# Define functions for stars 
##################################################################
# Define: print function
#from logging import NOTSET,DEBUG,INFO,WARN,WARNING,ERROR,CRITICAL,FATAL
DEBUG = 10
INFO = 20
WARN = 30
def _outputlog(level, mesg, outstderronly=False):
    global gb_ScriptName
    global gb_Debug
    head = gb_ScriptName
        
    if(gb_Debug==False):
        if(level<=INFO):
            return 1
    if(outstderronly == True):
        if(mesg[-1:] != '\n'):
           mesg=mesg+'\n'
        sys.stderr.write(mesg)
    else:
        if(mesg[-1:] != '\n'):
           mesg=mesg+'\n'
        sys.stderr.write(mesg)
        #logger.log(level,'['+ head + '] ' + mesg)
    return 1

##################################################################
# Define Device control class:
#    use global var: gb_DeviceInstance
#                  : gb_DeviceSendDateisgaterunning, gb_DeviceReplyDateisgaterunning
#                  : gb_DeviceDownloadInstance
#                  : gb_DeviceDownloadBusyFlg, gb_DeviceDownloadCount
#                  : gb_DeviceDownloadSafeStopCmd
#                  : gb_DeviceDownloadDataBuffer
#                  : gb_DeviceDownloadStopDate
##################################################################
##------------------------------------
## Device download_start
##------------------------------------
def device_downloadstart(st,cmd,checkcmd):
    global gb_DeviceDownloadInstance
    global gb_DeviceDownloadDataBuffer
    global gb_DeviceDownloadStopDate
    global gb_DeviceDownloadCount
    global gb_DeviceDownloadIsHex

    dc = gb_DeviceDownloadInstance
    if(dc._callbackrunning==False):
        return 'Er: Download port lost connection.'

    if(device_getdownloadflgbusy()==1):
        return 'Er: Download is busy.'

    # Download START
    dc.replymessage=''
    dc.sendcommand=cmd
    time.sleep(0.011)

    rt = device_downloaddevicecmdsend(checkcmd,"")
    if('Er:' in rt):
        return(rt)
    elif(rt.startswith('H')):
        gb_DeviceDownloadIsHex = True
    elif(rt.startswith('D')):
        gb_DeviceDownloadIsHex = False
    else:
        return("Er: Unexpected reply to '%s'. (reply='%s')" %(checkcmd,rt))

    rt = device_downloaddevicecmdsend(cmd,"")
    if('Er:' in rt):
        return(rt)

    dc._downloadisbusy = True
    device_setdownloadflgbusy(1)
    gb_DeviceDownloadCount=-1
    gb_DeviceDownloadSafeStopCmd='STOP'
    gb_DeviceDownloadDataBuffer=''
    gb_DeviceDownloadStopDate=0
    gb_DeviceDownloadCount=0
    return 'Ok:'

def device_downloaddevicecmdsend(cmd,param):
    global gb_DeviceDownloadInstance
    dc = gb_DeviceDownloadInstance
    dc.replymessage=''
    dc.sendcommand=cmd+param
    time.sleep(0.011)

    while(True):
        if(dc.sendcommand != ''):
            time.sleep(0.01)
            continue
        if(dc.replymessage is None):
            return 'Er: ' + dc.getlasterrortext()
        elif(dc.replymessage == ''):
            return 'Er: ' + dc.getlasterrortext()
        elif(re.compile("^Er:").match(dc.replymessage) is not None):
            return dc.replymessage
        break
    return dc.replymessage
    return 'Ok:'
##------------------------------------
## Device download_stop
##------------------------------------
def device_downloadstop(st,cmd,delaytime=0):
    global gb_DeviceDownloadInstance
    global gb_DeviceDownloadStopDate
    global gb_DeviceDownloadSafeStopCmd
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    if(dc is None):
        #return("Er: Bad command or parameter.") 
        dc = gb_DeviceDownloadInstance
    if(delaytime == 0):
        # Simple STOP
        rt=dc.send(cmd)
        if(rt == False):
            return 'Er: ' + dc.getlasterrortext()
        device_setdownloadflgbusy(0)
        return 'Ok:'
    # Delay STOP
    gb_DeviceDownloadStopDate=-1*delaytime
    gb_DeviceDownloadSafeStopCmd=cmd
    return 'Ok:'

##------------------------------------
## Device DownloadFlgBusy
##------------------------------------
def device_getdownloadflgbusy():
    global gb_DeviceDownloadBusyFlg
    return gb_DeviceDownloadBusyFlg

def device_setdownloadflgbusy(f):
    global gb_DeviceDownloadBusyFlg
    global gb_StarsInstance
    st = gb_StarsInstance
    if(f != gb_DeviceDownloadBusyFlg):
        gb_DeviceDownloadBusyFlg=f
        if __name__ == "__main__":
            destsendstr = st.nodename + '>System' +' _ChangedIsBusy %s' %(str(f))
        destsendstr = st.nodename + '>System' +' _ChangedDownloadIsBusy %s' %(str(f))
        _outputlog(INFO,'STARS Send[' +st.nodename + "]:"+destsendstr)
        rt=st.send(destsendstr)
    return gb_DeviceDownloadBusyFlg

def device_getdownloadcount():
    global gb_DeviceDownloadCount
    if(gb_DeviceDownloadCount<=0):
        return(0)
    return gb_DeviceDownloadCount

def device_setdownloadcount(i):
    global gb_DeviceDownloadCount
    gb_DeviceDownloadCount = n
    return('Ok:')

def device_incrementdownloadcount(i):
    global gb_DeviceDownloadCount
    if(gb_DeviceDownloadCount<=0):
        gb_DeviceDownloadCount=i
    else:
        gb_DeviceDownloadCount=gb_DeviceDownloadCount+i
    return(gb_DeviceDownloadCount)
##################################################################
# Define stars extention class:
##################################################################
def device_recvdatahandler(rmesg, dc):
    global gb_DeviceDownloadDataBuffer
    global gb_StarsInstance
    global gb_StarsChildNodeofData
    st = gb_StarsInstance
    _outputlog(INFO,"*** device_recvdatahandler %s***\n" %(rmesg))
    rtmsg=gb_DeviceDownloadDataBuffer+rmesg;
    sender = st.nodename + '.' + gb_StarsChildNodeofData
    while(rtmsg!=''):
        dp = rtmsg.find('\n')
        if dp < 0:
            break
        rtmess = rtmsg[:dp]
        rtmsg = rtmsg[dp+1:]
        #SendEvent
        rtmess = rtmess.replace('\n', '')
        rtmess = rtmess.replace('\r', '')
        if(rtmess == 'OK'):
            continue
        if(rtmess == 'NG'):
            continue
        rtmess = rtmess.replace(' ,', ',')
        rtmess = rtmess.replace(', ', ',')
        rtlist = rtmess.split(',')
        rtmess = ','.join(rtlist)
        if(gb_DeviceDownloadIsHex == True):
            destsendstrH = sender + '>System' +' _ChangedHexValue '+ rtmess
            for i in range(0, len(rtlist)):
                try:
                    rtlist[i]=str(int(rtlist[i],16)).rjust(5, '0')
                except Exception as e:
                    destsendstr = st.nodename + '>System' +' _DataError Not hex->'+ rtlist[i]
                    _outputlog(INFO,'STARS Send[' +st.nodename + "]:"+destsendstr)
                    continue
            rtmess = ','.join(map(str,rtlist))
            rtdata = '\t'.join(map(str,rtlist))
            destsendstr = sender + '>System' +' _ChangedValue '+ rtmess
        else:
            destsendstr = sender + '>System' +' _ChangedValue '+ rtmess
            for i in range(0, len(rtlist)):
                try:
                    rtlist[i]='%010X' % int(rtlist[i])
                except Exception as e:
                    destsendstrH = st.nodename + '>System' +' _DataError Not decimal->'+ rtlist[i]
                    _outputlog(INFO,'STARS Send[' +st.nodename + "]:"+destsendstrH)
                    continue
            rtmess = ','.join(map(str,rtlist))
            rtdata = '\t'.join(map(str,rtlist))
            destsendstrH = sender + '>System' +' _ChangedHexValue '+ rtmess

        _outputlog(INFO,'STARS Send[' +sender + "]:"+destsendstrH)
        _outputlog(INFO,'STARS Send[' +sender + "]:"+destsendstr)
        rt=st.send(destsendstrH)
        if(rt == False):
            st.terminateMainloop()
            return(False)
        rt=st.send(destsendstr)
        if(rt == False):
            st.terminateMainloop()
            return(False)
        device_incrementdownloadcount(1)
    gb_DeviceDownloadDataBuffer=rtmsg;
    return(True)

def device_detectcontrolhandler(dcsock):
    global gb_DeviceInstance
    global gb_DeviceDownloadCount
    dc = gb_DeviceInstance
    _outputlog(INFO,"*** device_detectcontrolhandler ***\n")
    while(True):
        if(gb_DeviceDownloadInstance._callbackrunning == False):
           st.terminateMainloop()
           return(False)
        rt = dc.receive(1,None,None)
        if(rt is None):
            st.terminateMainloop()
            return(False)
        if(rt == ''):
            break
        #Check reply isrunning
        device_checkgateisrunning(rt)
    return(True)

def device_checkgateisrunning(rt):
    global gb_DeviceReplyDateisgaterunning;
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_DeviceDownloadInstance
    dc = gb_DeviceInstance
    dc2 = gb_DeviceDownloadInstance
    st = gb_StarsInstance
    if(rt is None):
        return(rt)
    if(rt == ''):
        return(rt)
    #Check reply isrunning
    s = PyStarsDeviceTSUJICOUNTERTIMERGateStatus(rt)
    if(s.has_error == False):
        _outputlog(INFO,"*** device_replyisgaterunning %s ***\n" %(rt))
        gb_DeviceReplyDateisgaterunning=time.time()
        if(s.gate_running == 1):
            if(gb_DeviceDownloadCount<0):
                gb_DeviceDownloadCount=0
        else:
            dc2._downloadisbusy = False
            device_setdownloadflgbusy(0)
        return(True)
    return(False)

## Handle message from STARS server
def device_checkstopdelay():
    global gb_StarsInstance
    st = gb_StarsInstance
    global gb_DeviceDownloadStopDate
    #global gb_DeviceInstance
    #dc = gb_DeviceInstance

    if(gb_DeviceDownloadStopDate>0):
        if((time.time()-gb_DeviceDownloadStopDate)>=0):
            _outputlog(INFO,"*** Stop by GSTS? ***\n")
            device_downloadstop(st,gb_DeviceDownloadSafeStopCmd)
            gb_DeviceDownloadStopDate = 0
    elif(gb_DeviceDownloadStopDate<0):
        stoptimeout=gb_DeviceDownloadStopDate*(-1)
        gb_DeviceDownloadStopDate=time.time()+stoptimeout


## STARS socket handler
def handler(allmess,sock):
    global gb_StarsInstance
    global gb_DeviceDownloadInstance
    st = gb_StarsInstance

    if allmess == '':
        st.terminateMainloop(True)
        return
    _outputlog(INFO, 'STARS Recv[' +st.nodename + "]:"+allmess)

    rt = ''
    if(gb_DeviceDownloadInstance is not None):
        rt = sub_downloaderhandler(allmess,sock)
    if(rt == ''):
        rt = sub_mainhandler(allmess,sock)

    if(allmess.command.startswith('@')==True):
        return
    elif(allmess.command.startswith('_')==True):
        return

    if(rt != ''):
        destsendstr = rt
        _outputlog(INFO,'STARS Send[' + allmess.nodeto + "]:"+destsendstr)
        rt=st.send(destsendstr)
        if(rt==False):
            st.terminateMainloop()
    return

def sub_mainhandler(allmess,sock):
    global gb_ScriptName
    global gb_StarsInstance
    st = gb_StarsInstance

    if allmess == '':
        st.terminateMainloop()
        return
    elif(allmess.parameters == ''):
        message = allmess.command
    else:
        message = allmess.command + ' ' + allmess.parameters
    command   = allmess.command
    parameters = []
    if(allmess.parameters != ''):
        parameters = allmess.parameters.split(" ")

    destsendstr='';
    rt = ''

    if(allmess.nodeto == st.nodename):
        if(message.startswith('@')==True):
            pass
        elif(message.startswith('_')==True):
            pass
        elif(message == 'getversion'):
            rt = gb_ScriptName + ' '+__version__+','+__date__+','+__author__
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
        elif(message == 'getversionno'):
            rt = __version__
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
        elif(message == 'hello'):
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' Nice to meet you.'
        elif(message == 'help'):
            rt = stars_getdevicecommandhelpstring('ALL','')
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(command == 'help' and len(parameters) == 1):
            rt = stars_getdevicecommandhelpstring('ALL',parameters[0])
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message == 'terminate'):
            st.terminateMainloop()
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' Ok:'
        elif(message == 'IsBusy'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + str(device_getdownloadflgbusy())
        elif(message == 'Stop'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstop(st,'STOP')
        else:
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' Er: Bad command or parameters.'
    else:
        destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' Er: Bad command or parameters.'
    return(destsendstr)

def sub_downloaderhandler(allmess,sock):
    global gb_ScriptName
    global gb_StarsInstance
    global gb_DeviceInstance
    st = gb_StarsInstance

    if allmess == '':
        st.terminateMainloop(True)
        return
    elif(allmess.parameters == ''):
        message = allmess.command
    else:
        message = allmess.command + ' ' + allmess.parameters

    command   = allmess.command
    parameters = []
    if(allmess.parameters != ''):
        parameters = allmess.parameters.split(" ")

    destsendstr=''
    if(allmess.nodeto == st.nodename):
        if(message == 'GetDownloadedCount'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + str(device_getdownloadcount())
        elif(message == 'IsDownloadBusy'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + str(device_getdownloadflgbusy())
        elif(allmess.command == 'TimerDownloadStart'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstart(st,'TSDSTRT', 'TSDL?')
        elif(message == 'TimerDownloadStop'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstop(st,'TSDSTOP')

        elif(message == 'GateDownloadStart'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstart(st,'GSDSTRT', 'XSDL?')
        elif(message == 'GateDownloadStop'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstop(st,'XSDSTOP')

        elif(message == 'GateEdgeDownloadStart'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstart(st,'XSDSTRT', 'XSDL?')
        elif(message == 'GateEdgeDownloadStop'):
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstop(st,'XSDSTOP')

        elif((command == 'DelayStop') and (len(parameters) == 1)):
            if(re.compile("^[\d]+\Z").match(parameters[0]) == False):
                destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' Er: Bad command or parameters.'
            else:
                stoptimeout=float(parameters[0])
                destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + device_downloadstop(st,'STOP',stoptimeout)
    return(destsendstr)

def stars_getdevicecommandhelpstring(level,starscommand):
    global gb_DeviceDownloadInstance
    dc = gb_DeviceDownloadInstance

    if(starscommand == ''):
        clist = []
        keylist = sorted(dc._deviceSTARSCommand.keys())
        for key in (keylist):
            dobj = dc.devicecommandobject(key)
            if(level == 'ALL'):
                clist.append(key)
            elif((level == 'CTL') and (dobj.isglobalcommand)):
                clist.append(key)
            elif((level == 'CH') and (dobj.ischannelcommand)):
                clist.append(key)
        rt = ' '.join(clist)
    else:
        rt = "Er: No help of '%s'." %(starscommand)
        dobj = dc.devicecommandobject(starscommand)
        if(dobj):
            if(level == 'ALL'):
                rt = dobj.helpstring
            elif((level == 'CTL') and (dobj.isglobalcommand)):
                rt = dobj.helpstring
            elif((level == 'CH') and (dobj.ischannelcommand)):
                rt = dobj.helpstring
    return(rt)

##################################################################
# Define program parameters
##################################################################
# Global parameters.
gb_Debug = False
gb_StarsInstance  = None
gb_DeviceInstance = None
gb_DeviceDownloadInstance = None

##################################################################
# Define internal parameters
##################################################################
# Internal parameters.
gb_ScriptName = os.path.splitext(os.path.basename(__file__))[0]
#ScriptPath = os.path.dirname(os.path.abspath(sys.argv[0]))

gb_DeviceSendDateisgaterunning=time.time()-3
gb_DeviceReplyDateisgaterunning=time.time()-2

gb_DeviceDownloadBusyFlg=0
gb_DeviceDownloadCount=-1
gb_DeviceDownloadSafeStopCmd='STOP'
gb_DeviceDownloadDataBuffer=''
gb_DeviceDownloadStopDate=0
gb_DeviceDownloadIsHex=False
gb_StarsChildNodeofData='data'

#----------------------------------------------------------------
# Program pyctxdownloader.py
#----------------------------------------------------------------
if __name__ == "__main__":
    ##################################################################
    # Import modules
    ##################################################################
    from pystarslib import pystarsutilconfig, pystarsutilargparser
    from pynctx import PyStarsDeviceTSUJICOUNTERTIMER

    # Define: Appliction default parameters
    starsNodeName   = 'pyctxdownloader'
    starsServerHost = '127.0.0.1'
    starsServerPort = 6057
    deviceHost = '192.168.1.123'
    devicePort = 7777
    downloadstatuscheckenable = True

    ##################################################################
    # Define program arguments
    ##################################################################
    optIO=pystarsutilargparser.PyStarsUtilArgParser(numberOfDeviceServer=1)
    parser=optIO.generate_baseparser(prog=gb_ScriptName,version=__version__)
    #parser.add_argument('--downloadstatuscheckenable', type=bool, dest="DownloadStatusCheckEnable", help='Enable the download status checker functon.')

    ##################################################################
    # Parse program arguments and config settings
    ##################################################################
    args=parser.parse_args()
    gb_Debug=args.debug
    if(gb_Debug==True):
        sys.stdout.write(str(args)+'\n')

    # Fix StarsNodename
    starsNodeName = optIO.get(args.StarsNodeName,starsNodeName)
    # Read configfile if detected
    configFileName = optIO.get(args.Config,None)
    if(configFileName is not None):
        cfgIO= pystarsutilconfig.PyStarsUtilConfig(configFileName,gb_Debug)
        if(cfgIO.gethandle() is None):
            sys.stdout.write(cfgIO.getlasterrortext()+'\n')
            exit(1)
        if(not optIO.has_value(args.StarsNodeName)):
            starsNodeName = cfgIO.get('', 'StarsNodeName', starsNodeName)
        if(gb_Debug == False):
            gb_Debug        = cfgIO.get(starsNodeName, 'Debug'          , gb_Debug, bool)
        starsServerHost = cfgIO.get(starsNodeName, 'StarsServerHost', starsServerHost)
        starsServerPort = cfgIO.get(starsNodeName, 'StarsServerPort', starsServerPort, int)
        deviceHost      = cfgIO.get(starsNodeName, 'DeviceHost'     , deviceHost)
        devicePort      = cfgIO.get(starsNodeName, 'DevicePort'     , devicePort, int)
        #downloadstatuscheckenable = cfgIO.get(starsNodeName, 'DownloadStatusCheckEnable', downloadstatuscheckenable, bool)

    # Fix optional parameters
    starsServerHost = optIO.get(args.StarsServerHost,starsServerHost)
    starsServerPort = optIO.get(args.StarsServerPort,starsServerPort)
    deviceHost      = optIO.get(args.DeviceHost,deviceHost)
    devicePort      = optIO.get(args.DevicePort,devicePort)
    #downloadstatuscheckenable = optIO.get(args.DownloadStatusCheckEnable, downloadstatuscheckenable)

    if(gb_Debug==True):
        sys.stdout.write("starsNodeName#"+str(starsNodeName)+"#"+'\n')
        sys.stdout.write("starsServerHost#"+str(starsServerHost)+"#"+'\n')
        sys.stdout.write("starsServerPort#"+str(starsServerPort)+"#"+'\n')
        sys.stdout.write("deviceHost#"+str(deviceHost)+"#"+'\n')
        sys.stdout.write("devicePort#"+str(devicePort)+"#"+'\n')

    ##################################################################
    # Connect to device
    ##################################################################
    #Create device instance with devserver:devport
    if(downloadstatuscheckenable == True):
        gb_DeviceInstance = PyStarsDeviceTSUJICOUNTERTIMER(deviceHost, devicePort)
        gb_DeviceInstance.setdebug(gb_Debug)

    gb_DeviceDownloadInstance = PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADER(deviceHost, devicePort)
    gb_DeviceDownloadInstance.setdebug(gb_Debug)
    ##################################################################
    # Connect to device : data recv control
    ##################################################################
    rt=gb_DeviceDownloadInstance.connect()
    if(rt==False):
        sys.stdout.write(gb_DeviceDownloadInstance.getlasterrortext()+'\n')
        exit(1)
    if(gb_Debug == True):
        gb_DeviceDownloadInstance.printinfo()

    #rt=gb_DeviceDownloadInstance.send('TSDSTOP')
    #rt=gb_DeviceDownloadInstance.send('XSDSTOP')
    #rt=gb_DeviceDownloadInstance.send('GSDSTOP')

    while(True):
        rt=gb_DeviceDownloadInstance.device_receive(1)
        if('Er:' in rt):
            sys.stdout.write(gb_DeviceDownloadInstance.getlasterrortext()+'\n')
        if(rt == ''):
              break
        break

    #Initialize device variables
    rt=gb_DeviceDownloadInstance.device_init(useAsSTARSClient=True)
    if(rt == False):
        sys.stdout.write(gb_DeviceDownloadInstance.getlasterrortext()+'\n')
        exit(1)

    device_checkstopdelay()

    ##################################################################
    # Connect to device : main control
    ##################################################################
    if(gb_DeviceInstance is not None):
        rt = gb_DeviceInstance.connect()
        if(rt==False):
            sys.stdout.write(gb_DeviceInstance.getlasterrortext()+'\n')
            exit(1)

        while(True):
            rt=gb_DeviceInstance.device_receive(1)
            if('Er:' in rt):
                sys.stdout.write(gb_DeviceInstance.getlasterrortext()+'\n')
            if(rt == ''):
                break
        #Initialize device variables
        rt=gb_DeviceInstance.device_init()
        if(rt == False):
            sys.stdout.write(gb_DeviceInstance.getlasterrortext()+'\n')
            exit(1)
    ##################################################################
    # Connect to stars
    ##################################################################
    st  = StarsInterface(starsNodeName, starsServerHost, '', starsServerPort)
    gb_StarsInstance = st

    #Set properties for Stars instance
    st.setdebug(gb_Debug)

    rt = st.setdefaultreceivetimeout(3)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Connect to Stars
    rt=st.connect()
    if(rt==False):
        sys.stdout.write(st.error+'\n')
        exit(1)

    #Add device data handler
    gb_DeviceDownloadInstance.start_nb_handler(device_recvdatahandler)

    if(gb_DeviceInstance is not None):
        #Add device callback handler
        rt=st.addcallback(device_detectcontrolhandler,gb_DeviceInstance.gethandle(),'DETECT')
        if(rt==False):
            stdout.write(gb_DeviceInstance.getlasterrortext()+'\n')
            exit(1)

    #Add callback handler
    rt=st.addcallback(handler)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Start Mainloop()
    rt=st.Mainloop(interval,0.01)
    gb_DeviceDownloadInstance._callbackrunning = False
    if(rt==False):
        stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Device close
    #*** sleep for callback terminate wait
    time.sleep(0.1)
    if(gb_DeviceInstance is not None):
        gb_DeviceInstance.disconnect()
    gb_DeviceDownloadInstance.disconnect()
    st.removecallback()
    st.disconnect()
    exit(0)
