#!/usr/bin/python3
"""
  STARS python program Tsuji Electronics Co.,Ltd. Stepping motor controller for PM16C-16
    Description: Connect to STARS server and commnicate with the device.

    History:
       0.0     Beta(1st)           2021.12.14      Yasuko Nagatani
"""

# Define: program info
__author__ = 'Yasuko Nagatani'
__version__ = '0.1'
__date__ = '2022-04-12'
__license__ = 'MIT'

#----------------------------------------------------------------
# Import modules
#----------------------------------------------------------------
import sys
from os import path,access,sep,W_OK
import time
import re
from collections import OrderedDict,defaultdict
import numpy as np
from logging import disable,getLogger,Formatter,StreamHandler,FileHandler,NullHandler,NOTSET,DEBUG,INFO,WARN,WARNING,ERROR,CRITICAL,FATAL,basicConfig
from singlestars import StarsInterface
import nportserv

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERFirmwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERFirmwareInfo(str):
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERFirmwareInfo: Device info object.
    """
    def __init__(self, versionstr):
        self.versiondetected = False
        self.version = versionstr
        self.version_no   = 0
        self.version_date = ''
        self.device_name  = ''
        self.numberofchannel = 16
        self.is_supported = {}
        self.value_minimum = {}
        self.value_maximum = {}
        self.is_supported['VERH']    = False
        self.is_supported['ALL_REP'] = False
        self.is_supported['TMGFX']   = False
        self.value_maximum['POSITION']  = 2147483647
        self.value_minimum['POSITION']  =-2147483647
        self.value_maximum['SPEED']  = 5000000
        self.value_minimum['SPEED']  = 1
        self.accratecodelist=[1000,  910,  820,  750,  680,  620,  560,  510,  470,  430,  390,  360,  330,  300,  270,  240,  220,  200,  180,  160, 150, 130, 120, 110, 100,   91,   82,   75,   68,   62,   56,   51,   47,   43,   39,   36,   33,   30,   27,   24,   22,   20,   18,   16,  15,  13,  12,  11,  10
,  9.1,  8.2,  7.5,  6.8,  6.2,  5.6,  5.1,  4.7,  4.3,  3.9,  3.6,  3.3,  3.0,  2.7,  2.4,  2.2,  2.0,  1.8,  1.6, 1.5, 1.3, 1.2, 1.1, 1.0, 0.91, 0.82, 0.75, 0.68, 0.62, 0.56, 0.51, 0.47, 0.43, 0.39, 0.36, 0.33, 0.30, 0.27, 0.24, 0.22, 0.20, 0.18, 0.16,0.15,0.13,0.12,0.11,0.10,0.091,0.082,0.075,0.068,0.062,0.056,0.051,0.047,0.043,0.039,0.036,0.033,0.030,0.027,0.024,0.022,0.020,0.018,0.016]
        self.has_error = True
        self.error = 'Uninitialized'
        self.is_pm16c16  = False
        m = re.search("^(\S+)\s+(\S+)\s+(\S+)\Z", versionstr)
        if m:
            try:
                self.version_no   = float(m.group(1))
                self.version_date = m.group(2)
                self.device_name  = m.group(3)
                m = re.search('^PM16C-16',self.device_name)
                if(m):
                    self.is_pm16c16  = True
                    self.versiondetected = True
                    self.has_error = False
                else:
                    self.versiondetected = False
                    self.has_error = True
                    rt="Unexpected version reply.('%s'). " %(versionstr)
                    self.error = "%s" %(rt)
            except:
                rt="Unexpected version reply.('%s'). " %(versionstr)
                self.error = "%s" %(rt)
        else:
            rt="Unexpected version reply.('%s'). " %(versionstr)
            self.error = "%s" %(rt)

        if self.is_pm16c16:
            self.is_supported['VERH']    = True
            self.is_supported['ALL_REP'] = True
            if(self.version_no>=1.01):
                self.is_supported['TMGFX'] = True

    def is_commandsupported(self, command):
        if(command == ''): return(False)
        if(command in self.is_supported): return(self.is_supported[command])
        return(True)

    def set_commandsupported(self, command, b):
        if(command == ''): return(False)
        self.is_supported[command] = b
        return(True)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERHardwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERHardwareInfo(str):
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERHardwareInfo: Device hardware info object.
    """
    def __init__(self, hwversionstr):
        self.versiondetected = False
        self.hardwareversion = hwversionstr
        self.hardwareversion_no = 0
        self.has_error = True
        self.error = 'Uninitialized'
        m = re.search("^HD-VER\s(\d+)\Z", hwversionstr.upper())
        if m:
            try:
                self.versiondetected = True
                self.hardwareversion_no   = float(m.group(1))
                self.has_error = False
            except:
                rt="Analyzing hardware version failure ('%s'). (%s)" %(hwversionstr, type(e))
                self.error = "%s" %(rt)
        else:
            m = re.search("^HD-VER\.(\d+)\Z", hwversionstr.upper())
            if m:
                try:
                    self.versiondetected = True
                    self.hardwareversion_no   = float(m.group(1))
                    self.has_error = False
                except:
                    rt="Analyzing hardware version failure ('%s'). (%s)" %(hwversionstr, type(e))
                    self.error = "%s" %(rt)
            else:
                rt="Hardware version reply error ('%s'). Unexpected reply format." %(hwversionstr)
                self.error = "%s" %(rt)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(STSx?)
#----------------------------------------------------------------
class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(str):
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus: Status object.
    """
    def __init__(self, statusstr):
        self.statusdetected = False
        self.status = statusstr
        self.channel_no   = 0
        self.RL = '-'
        self.PSN = '-'
        self.LS = '-'
        self.MT = '-'
        self.position = '-'
        self.isremote = '-'
        self.busyflag = '-'
        self.holdoffstatus = '-'
        self.holdonstatus = '-'
        self.limitstatus = '-'
        self.has_error = True
        self.error = 'Uninitialized'
        m = re.search("^([RL])(\S)(\S)(\S)(\S\S)(.+)\Z", statusstr)
        if m:
            try:
                self.RL  = m.group(1)
                self.channel_no   = int(m.group(2),16)
                self.PSN = m.group(3)
                self.LS = m.group(4)
                self.MT = m.group(5)
                self.position = int(m.group(6))
                self.isremote = '0'
                if(self.RL == 'R'):
                    self.isremote = '1'
                self.busystatus = str(int(self.MT,16)&0x1)
                self.holdoffstatus = str((int(self.LS,16)&0b1000)>>3)
                self.holdonstatus = str(int(self.holdoffstatus) ^0x1)
                self.limitstatus = str(int(self.LS,16)&0b0111)
                self.statusdetected = True
                self.has_error = False
            except:
                rt="Unexpected version reply.('%s'). " %(versionstr)
                self.error = "%s" %(rt)
        else:
            rt="Unexpected version reply.('%s'). " %(versionstr)
            self.error = "%s" %(rt)

    def is_commandsupported(self, command):
        if(command == ''):
            return(False)
        if(command in self.is_supported):
            return(self.is_supported[command])
        return(True)

    def set_commandsupported(self, command, b):
        if(command == ''):
            return(False)
        self.is_supported[command] = b
        return(True)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand
#----------------------------------------------------------------
class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel():
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel: Target codelist of device command.
    """
    CONTROLLER, CHANNEL = range(1,3)

class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand():
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand: Device command object.
    """
    def __init__(self, commandtag, ishelponly=False, ischannelcommand=True, isglobalcommand=False, islockcommand=False, isunlockcommand=False, isreferencecommand=True, ismotioncommand=False, argnum = 0, replytag=None, isallowbusy=True, isallowlocal=None, checkfunc=None, postfunc=None, postwaittime=0, helpstring="-", globalcommandtag=''):
        self.commandtag  = commandtag
        self.ishelponly = ishelponly
        self.ischannelcommand = ischannelcommand
        self.islockcommand = islockcommand
        self.isunlockcommand = isunlockcommand
        self.isglobalcommand = isglobalcommand
        self.isreferencecommand = isreferencecommand
        self.ismotioncommand = ismotioncommand
        if(isglobalcommand and (globalcommandtag == '')):
            self.globalcommandtag  = commandtag
        else:
              self.globalcommandtag  = globalcommandtag
        if(isallowlocal is None):
            self.isallowlocal = isreferencecommand
        else:
            self.isallowlocal = isallowlocal

        if(replytag == ''):
            self.replytag = None
        else:
            self.replytag = replytag
        self.ischeckargnum = True
        self.argnum = argnum
        if(argnum is None): self.argnum = -1
        if(self.argnum<0):  self.ischeckargnum = False
        self.isallowbusy = isallowbusy
        self.checkfunc = checkfunc
        self.postfunc = postfunc
        self.postwaittime = postwaittime
        self.helpstring = helpstring

class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLER(nportserv.nportserv):
    """ Class PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERPMC: Derived from nportserv to control the device.
    """
    ##################################################################
    # Device control functions
    ##################################################################
    ## Device send
    def device_send(self,cmd):
        if(self.isconnected()==False): return 'Er: Disconnected'
        rt=self.send(cmd)
        if(rt==False): return 'Er: ' + self.getlasterrortext()
        self._deviceCommandLastExecutedTime['LATEST'] = time.time()
        if(self._cmdhandler is not None): rt=self._cmdhandler("[Send]"+cmd)
        return 'Ok:'

    ## Device act
    def device_act(self,cmd,timeout=''):
        rt=self.device_send(cmd)
        if('Er:' in rt): return(rt)
        rt=self.device_receive(timeout)
        return rt

    ## Device recv
    def device_receive(self,timeout=''):
        if(self.isconnected()==False): return 'Er: Disconnected'
        if(timeout==''): timeout=self.gettimeout()
        while(True):
            rt=self.receive(timeout)
            if(rt is None):
                if(self._cmdhandler is not None): self._cmdhandler("[Recv]<None>")
                return 'Er: ' + self.getlasterrortext()
            if(self._cmdhandler is not None): self._cmdhandler("[Recv]"+rt)
            if(rt.startswith('STOP') and len(rt)==5):
               pass
            else:
               break
        #self._deviceCommandLastExecutedTime['LASTEST'] = time.time()
        return rt

    def device_init(self):
        rt = False
        max_motorno = 0
        #Read firmware version
        if(self._deviceFirmwareInfo is None):
            rt2 = self.device_act('VER?')
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            else:
                rt2 = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERFirmwareInfo(rt2)
                if(rt2.has_error):
                    self.error = 'Er: %s' %(rt2.error)
                    return(rt)
                self._deviceFirmwareInfo = rt2
                max_motorno = rt2.numberofchannel
        if(self._deviceFirmwareInfo.versiondetected == False):
            self.error = 'Er: %s' %(rt2.error)
            return(rt)

        #Read hardware version
        if(self._deviceHardwareInfo is None):
            self._deviceHardwareInfo = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERHardwareInfo('')
            if(self._deviceFirmwareInfo.is_commandsupported('VERH') == True):
                rt2 = self.device_act('VERH?')
                if('Er:' in rt2):
                    self.error = rt2
                    return(rt)
                elif(rt2 == ''):
                    self._deviceFirmwareInfo.set_commandsupported('VERH', False)
                else:
                    rt2 = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERHardwareInfo(rt2)
                    if(rt2.has_error):
                        self.error = 'Er: %s' %(rt2.error)
                        return(rt)
                    self._deviceHardwareInfo = rt2

        rt=self._command_config()
        return(rt)

    def processdevicereplystring(self,replystr):
        rt= replystr
        if(rt == ''):
            rt='Er: No reply.'
        elif('Er:' in rt):
            pass
        elif(rt == 'OK'):
            rt='Ok:'
        elif(rt == 'NG'):
            rt='Er: Command execution error.'
        elif('ERROR' in rt):
            if('COMMAND' in rt):
                rt='Er: Invalid command.'
            elif('PARAMETER' in rt):
                rt='Er: Invalid parameter.'
            else:
                rt='Er: ' + rt
        return(rt)

    ##################################################################
    # Command functions
    ##################################################################
    def _command_config(self):
        if(self._deviceFirmwareInfo is None): return(False)

        ##################################################################
        # Define command definitions
        ##################################################################
        lc_cmdctl = {}
        lc_cmdcha = {}

        #Ctrl command
        lc_cmdctl['Remote']             = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('REM',      isglobalcommand=True, isreferencecommand=False, isallowbusy=False, isallowlocal=True, postfunc='self._postsetcommand', helpstring="Remote mode change.")
        lc_cmdctl['Local']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('LOC',      isglobalcommand=True, isreferencecommand=False, isallowbusy=False, isallowlocal=True, postfunc='self._postsetcommand', helpstring="Local mode change.")
        lc_cmdctl['SetFunction']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('-',        isglobalcommand=True, isreferencecommand=False, isallowbusy=False, isallowlocal=True, argnum=1, checkfunc="self._checksetremlocbyarg", postfunc='self._postsetcommand', helpstring="Change remote/local mode. (0:local 1:remote)")
        lc_cmdctl['Standby']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('PAUSE ON', isglobalcommand=True, isreferencecommand=False, isallowbusy=False, helpstring="Send before motion start for synchronous start of multi channels.")
        lc_cmdctl['SyncRun']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('PAUSE OFF',isglobalcommand=True, isreferencecommand=False,                    helpstring="Send after motion start for synchronous start of multi channels.")
        lc_cmdctl['Stop']               = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ASSTP',    isglobalcommand=True, isreferencecommand=False, isallowlocal=True, helpstring="Stop all moving motors.")
        lc_cmdctl['StopEmergency']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('AESTP',    isglobalcommand=True, isreferencecommand=False, isallowlocal=True, helpstring="Fast stop all moving motors.")

        lc_cmdctl['GetFunction']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS0?',    isglobalcommand=True, postfunc='self._postgetremote', helpstring="Retun the remote/local mode. (0:local 1:remote)")
        lc_cmdctl['IsStandby']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('PAUSE?',   isglobalcommand=True, postfunc='self._postgetonoff',  helpstring="Return synchronous start state of multi channels enable or not.")
        lc_cmdctl['GetFirmwareVersion'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('VER?',     isglobalcommand=True, helpstring="Return the controller firmware version string.")
        lc_cmdctl['GetRomVersion']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('VER?',     isglobalcommand=True, helpstring="Return the controller firmware version string.")
        lc_cmdctl['GetHardwareVersion'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('VERH?',    isglobalcommand=True, helpstring="Return the controller hardware version string.")

        lc_cmdctl['GetDispChannel']               = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH?',  isglobalcommand=True, helpstring="Return the no. of channels in hex assigned to the control window Apos to Dpos by 4 letters string.")
        lc_cmdctl['SetDispChannel']               = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH%s', isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel',   helpstring="Assign the channels to the control window Apos to Dpos by 4 letters string, each letter is the channel no. in hex or '-' for the auto selection.")
        lc_cmdctl['GetTimingOutChannelFixEnable'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGFX?',  isglobalcommand=True, checkfunc='self._checksettimingout', replytag='OFF', postfunc='self._postgettimingoutfixchannel',  helpstring="Return the timing output channel control fix state.")
        lc_cmdctl['SetTimingOutChannelFixEnable'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGFX %s',isglobalcommand=True, isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing output channel control fix state enable or not.")

        if(self._deviceFirmwareInfo.is_commandsupported('TMGFX') == True):
            lc_cmdctl['GetTimingOutChannel'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGCH?', isglobalcommand=True, checkfunc='self._checksetchannel', helpstring="Return the no. of channels in hex assigned to the timing output from TP0 to TP3 by 4 letters string.")
            lc_cmdctl['SetTimingOutChannel'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGCH%s',isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channels of the timing output from TP0 to TP3 by 4 letters string, each letter is the channel no. in hex or '-' for the auto selection.")
            lc_cmdctl['Select']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGCH%s',isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channels of the timing output from TP0 to TP3 by 4 letters string, each letter is the channel no. in hex or '-' for the auto selection.")
            lc_cmdcha['Select']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGCH%s',isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channel of the timing output by A to TP0, B to TP1, C to TP2 or D to TP3.")
        else:
            lc_cmdctl['GetTimingOutChannel'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH?', isglobalcommand=True, checkfunc='self._checksetchannel', helpstring="Return the no. of channels in hex assigned to both the timing output TP0 to TP3 and  the control window from Pos.A to Pos.D by 4 letters string.")
            lc_cmdctl['SetTimingOutChannel'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH%s',isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channels to the timing output from TP0 to TP3 and also to the control window from Pos.A to Pos.D by 4 letters string, each letter is the channel no. in hex or '-' for the auto selection.")
            lc_cmdctl['Select']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH%s',         isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channels to the timing output from TP0 to TP3 and also to the control window from Pos.A to Pos.D by 4 letters string, each letter is the channel no. in hex or '-' for the auto selection.")
            lc_cmdcha['Select']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETCH%s',         isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetchannel', helpstring="Assign the channel to both the timing output and the control window by A(pos and TP0), B(pos and TP1), C(pos and TP2), D(pos and TP3).")
        lc_cmdcha['GetSelected']             = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', isglobalcommand=True, checkfunc='self._checksetchannel', helpstring="Return 'A' to 'D' if assigned to the timing output TP0 to TP3, or return N.")

        if(self._deviceFirmwareInfo.is_pm16c16):
            lc_cmdctl['GetValue']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('PS_16?',  isglobalcommand=True, postfunc='self._postgetvalue',       helpstring="Return the position value of all channels.")
            lc_cmdctl['IsBusy']           = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS_16?', isglobalcommand=True, postfunc='self._postgetbusystatus',  helpstring="Return the busy status of all channels.")
            lc_cmdctl['GetLimitStatus']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('LS_16?',  isglobalcommand=True, postfunc='self._postgetlimitstatus', helpstring="Return the limit status of all channels.")
            lc_cmdctl['GetHoldStatus']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('LS_16?',  isglobalcommand=True, postfunc='self._postgetholdstatus',  helpstring="Return the hold status of all channels.")
            lc_cmdctl['GetLANSRQFlag']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('LN_SRQ?G',isglobalcommand=True, postfunc='self._postgetlansrq',      helpstring="Return the lan srq flag of all channels.")
            lc_cmdctl['ResetLANSRQFlag']  = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('LN_SRQG0',isglobalcommand=True, isreferencecommand=False,            helpstring="Reset the lan srq flag of all channels.")
        if(self._deviceFirmwareInfo.is_commandsupported('ALL_REP') == True):
            lc_cmdctl['GetAllReplyEnable']= PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ALL_REP?',  isglobalcommand=True, postfunc='self._postgetonoff', helpstring="Return the all reply state.")
            lc_cmdctl['SetAllReplyEnable']= PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ALL_REP %s',isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc="self._checksetonoff", helpstring="Set the all reply state enable or not.")

        lc_cmdctl['GetChannelStatus']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS?',    isglobalcommand=True, helpstring="Return the reply of STS? command. (Deprecated for any use other than checking local status of PM16C-16.)")

        #Motor command
        lc_cmdcha['Stop']              = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SSTP%s',   checkfunc='self._checkchsetcommand', isreferencecommand=False, isallowlocal=True, helpstring="Stop the moving motor.")
        lc_cmdcha['StopEmergency']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ESTP%s',   checkfunc='self._checkchsetcommand', isreferencecommand=False, isallowlocal=True, helpstring="Fast stop the moving motor.")
        lc_cmdcha['GetValue']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS%s?',   checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the position value.")
        lc_cmdcha['IsBusy']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS%s?',   checkfunc='self._checkchsetcommand', postfunc='self._postgetbusystatus',          helpstring="Return the busy status.")
        lc_cmdcha['GetCancelBacklash'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('B%s?',     checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the cancel backlash.")
        lc_cmdcha['GetLimitStatus']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS%s?',   checkfunc='self._checkchsetcommand', postfunc='self._postgetlimitstatus',         helpstring="Return the limit status.")
        lc_cmdcha['GetHoldStatus']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STS%s?',   checkfunc='self._checkchsetcommand', postfunc='self._postgetholdstatus',          helpstring="Return the hold status.")
        lc_cmdcha['GetSpeedSelected']  = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPD?%s',   checkfunc='self._checkchsetcommand', postfunc='self._postgetspeedselection',      helpstring="Return the speed selection 'H/M/L'.")
        lc_cmdcha['GetHold']           = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('HOLD?%s',  checkfunc='self._checkchsetcommand', postfunc='self._postgetonoff',               helpstring="Return the hold on/off set.")
        lc_cmdcha['GetMotorSetup']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETMT?%s', checkfunc='self._checkchsetcommand',                                              helpstring="Return the motor setup.")
        lc_cmdcha['GetLimits']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETLS?%s', checkfunc='self._checkchsetcommand',                                              helpstring="Return the LS setting.")
        lc_cmdcha['GetHPMode']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETHP?%s', checkfunc='self._checkchsetcommand',                                              helpstring="Return the HP find information set.")
        lc_cmdcha['GetStopMode']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STOPMD?%s',checkfunc='self._checkchsetcommand',                                              helpstring="Return the stop mode setting.")
        lc_cmdcha['GetDigitalCwLs']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('FL?%s',    checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the cw digital limit position.")
        lc_cmdcha['GetDigitalCcwLs']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('BL?%s',    checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the ccw digital limit position.")
        lc_cmdcha['GetHPOffset']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SHPF?%s',  checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the home position offset.")
        lc_cmdcha['GetHomePosition']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SHP?%s',   checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the home position.")
        lc_cmdcha['GetHighSpeed']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDH?%s',  checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the high speed value.")
        lc_cmdcha['GetMiddleSpeed']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDM?%s',  checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the middle speed value.")
        lc_cmdcha['GetLowSpeed']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDL?%s',  checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the low speed value.")
        lc_cmdcha['GetAccRateCode']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('RTE?%s',   checkfunc='self._checkchsetcommand', postfunc='self._postgetaccratecode',         helpstring="Return the acc rate code.")
        lc_cmdcha['GetAccRate']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('RTE?%s',   checkfunc='self._checkchsetcommand', postfunc='self._postgetaccratevalue',        helpstring="Return the acc rate value.")
        lc_cmdcha['GetJogPulse']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETJG?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',               helpstring="Return the acc rate value.")
        lc_cmdcha['Preset']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('PS%s%s',    isreferencecommand=False, isallowbusy=False,                       argnum=1, checkfunc='self._checksetrange',     helpstring="Preset the position value.")
        lc_cmdcha['SetValue']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ABS%s%s%s', isreferencecommand=False, isallowbusy=False, ismotioncommand=True, argnum=1, checkfunc='self._checkmoveposition', helpstring="Move to the absolute position.")
        lc_cmdcha['SetValueREL']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('REL%s%s%s', isreferencecommand=False, isallowbusy=False, ismotioncommand=True, argnum=1, checkfunc='self._checkmoveposition', helpstring="Move to the relative position.")
        lc_cmdcha['SetCancelBacklash'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('B%s%s',     isreferencecommand=False, isallowbusy=False,                       argnum=1, checkfunc='self._checksetrange',     helpstring="Cancel backlash set.")
        lc_cmdcha['JogCw']             = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('JOGP%s',    isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Jog move to the Cw position.")
        lc_cmdcha['JogCcw']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('JOGN%s',    isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Jog move to the Ccw position.")
        lc_cmdcha['ScanCw']            = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SCANP%s',   isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Accelerative scan to the Cw position.")
        lc_cmdcha['ScanCcw']           = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SCANN%s',   isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Accelerative scan to the Ccw position.")
        lc_cmdcha['ScanCwConst']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('CSCANP%s',  isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Constant speed scan to the Cw position.")
        lc_cmdcha['ScanCcwConst']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('CSCANN%s',  isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Constant speed scan to the Ccw position.")
        lc_cmdcha['ScanCwHome']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SCANHP%s',  isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Accelerative scan to the Cw position if HP switch then stop.")
        lc_cmdcha['ScanCcwHome']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SCANHN%s',  isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Accelerative scan to the Ccw position if HP switch then stop.")
        lc_cmdcha['ScanHome']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('FDHP%s',    isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkchsetcommand', helpstring="Find home position (start auto find sequence).")
        lc_cmdcha['ReScanHome']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('GTHP%s',    isreferencecommand=False, isallowbusy=False, ismotioncommand=True, checkfunc='self._checkrescanhome',   helpstring="Go to home position if it exists.")
        lc_cmdcha['SetSpeedCurrent']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPC%s%s',   isreferencecommand=False,                    argnum=1, checkfunc='self._checksetspeedcurrent', helpstring="Change speed while moving.")
        lc_cmdcha['SpeedLow']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDL%s',    isreferencecommand=False, isallowbusy=False          , checkfunc='self._checkchsetcommand',    helpstring="Change to low speed.")
        lc_cmdcha['SpeedMiddle']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDM%s',    isreferencecommand=False, isallowbusy=False          , checkfunc='self._checkchsetcommand',    helpstring="Change to middle speed.")
        lc_cmdcha['SpeedHigh']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDH%s',    isreferencecommand=False, isallowbusy=False          , checkfunc='self._checkchsetcommand',    helpstring="Change to high speed.")
        lc_cmdcha['SetHold']           = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('HOLD%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetonoff', helpstring="Hold on/off set.")
        lc_cmdcha['SetMotorSetup']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETMT%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checkchsetup',  helpstring="Change the motor drive setting by 4 letters string ABCD(=A:1/drive enable 0/disable B:1/hold on 0/hold off C:0/const 1/trapezoidal 2/S character D:0/Pulse-Pulse 1/Pulse-Direction.")
        lc_cmdcha['SetLimits']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETLS%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checkchsetup',  helpstring="Change the LS settingby 8 letters string  DYYY0yyy(=D:digital limit enable/1, disable/0 Y:LS(HP/Ccw/CW) enable/1, disable/0 y:LS(HP/Ccw/CW) N.C/1, N.O/0.")
        lc_cmdcha['SetHPMode']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETHP%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checkchsetup',  helpstring="HP find information set by 4 letters string 0XYZ(=X:found/1,not found/0 Y:found dir. 0/cw,1/ccw Z:auto start dir. 0/cw,1/ccw).")
        lc_cmdcha['SetStopMode']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('STOPMD%s%s',isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checkchsetup',  helpstring="Set PB and LS stop mode by 2 letters string AB(=A:0/LS slow stop 1/LS fast stop B:0/PB slow stop 1/PB fast stop).")
        lc_cmdcha['SetDigitalCwLs']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('FL%s%s',    isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetrange', helpstring="Cw digital limit position set.")
        lc_cmdcha['SetDigitalCcwLs']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('BL%s%s',    isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetrange', helpstring="Ccw digital limit position set.")
        lc_cmdcha['SetHPOffset']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SHPF%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetrange', helpstring="Home position offset set.")
        lc_cmdcha['SetHomePosition']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SHP%s%s',   isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksethpvalue', helpstring="Home position data set.")
        lc_cmdcha['SetHighSpeed']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDH%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetspeedvalue',  helpstring="High speed set.")
        lc_cmdcha['SetMiddleSpeed']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDM%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetspeedvalue',  helpstring="Middle speed set.")
        lc_cmdcha['SetLowSpeed']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SPDL%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetspeedvalue',  helpstring="Low speed set.")
        lc_cmdcha['SetAccRateCode']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('RTE%s%s',   isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetaccratecode', helpstring="Acc rate code set.")
        lc_cmdcha['SetAccRate']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('RTE%s%s',   isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetaccratevalue',helpstring="Acc rate code set by value(=ms/1000pps).")
        lc_cmdcha['SetJogPulse']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('SETJG%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksetrange',       helpstring="Jog pulse set for manual PB.")

        lc_cmdcha['SetTimingOutMode']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGM%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing out mode 0-5(0/disable 1/gate 2/200ns pulse out 3/10us pulse out 4/100us pulse out  5/1ms pulse out).")
        lc_cmdcha['SetTimingOutStart']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGS%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing out start position.")
        lc_cmdcha['SetTimingOutEnd']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGE%s%s', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing out end position.")
        lc_cmdcha['SetTimingOutInterval'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGI%s%s',isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing out interval.")
        lc_cmdcha['SetTimingOutReady']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMG%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc='self._checksettimingout', helpstring="Set the timing out ready 1:Ready 0:Clear.")

        lc_cmdcha['GetTimingOutMode']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGM?%s', checkfunc='self._checkchsetcommand', helpstring="Return the timing out mode.")
        lc_cmdcha['GetTimingOutStart']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGS?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',   helpstring="Return the timing out start position.")
        lc_cmdcha['GetTimingOutEnd']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGE?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',   helpstring="Return the timing out end position.")
        lc_cmdcha['GetTimingOutInterval'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGI?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetvalue',helpstring="Return the timing out interval.")
        lc_cmdcha['GetTimingOutReady']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('TMGR?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetonoff',   helpstring="Return the timing out ready state.")

        lc_cmdcha['SetAutoChangeSpeed']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ACS%s%s',  isreferencecommand=False, isallowbusy=False, argnum=-1, checkfunc='self._checksetacscontrol', helpstring="Set the no. of the auto change speed data.")
        lc_cmdcha['SetAutoChangeSpeedReady'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ACS%s%s',  isreferencecommand=False, isallowbusy=False, argnum=1,  checkfunc='self._checksetonoff',      helpstring="Set the auto change speed ready 1:Ready 0:Clear.")
        lc_cmdcha['GetAutoChangeSpeed']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ACS?%s%s', checkfunc='self._checksetacscontrol', argnum=1, postfunc='self._postsetacscontrol',           helpstring="Return no. of the auto change speed data.")
        lc_cmdcha['GetAutoChangeSpeedReady'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('ACSP?%s', checkfunc='self._checkchsetcommand', postfunc='self._postgetonoff',                            helpstring="Return the auto change ready state.")

        lc_cmdctl['hello']          = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return 'hello Nice to meet you.'")
        lc_cmdctl['help']           = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the list or the explanation of stars command.")
        lc_cmdctl['getversion']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return this program version.")
        lc_cmdctl['getversionno']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the version number of this program.")
        lc_cmdctl['terminate']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Terminate this program.")
        lc_cmdctl['listnodes']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the list of channels.")
        lc_cmdctl['flushdatatome']  = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Send the stars events to the sender node.")
        lc_cmdctl['flushdata']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Send the stars events to the node 'System'.")
        lc_cmdctl['GetMotorList']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the list of the motor name.'")
        lc_cmdctl['GetChannelList'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the list of the motor name.'")
        lc_cmdctl['GetMotorName']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the motor name of the specifed motor no.'")
        lc_cmdctl['GetCtlIsBusy']   = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return 0 (PM16C-04 series emulation).'")
        lc_cmdctl['SendRawCommand'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Send the device native command. (Use with program option --rawenable)")
        lc_cmdctl['GetAccRateList'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring='Return the acc rate list.')
        lc_cmdcha['hello']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Return 'hello Nice to meet you.'")
        lc_cmdcha['help']        = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Return the list or the explanation of stars command.")
        lc_cmdcha['GetMotorNumber'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Return the motor no.'")
        lc_cmdcha['GetAccRateList'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring='Return the acc rate list.')

        lc_cmdctl['_ChangedCtlIsBusy'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Event message of 'GetCtlIsBusy' command. (Use with program option --pm16c04compatible)")
        lc_cmdctl['_ChangedFunction']  = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Event message of 'GetFunction' command.")
        lc_cmdcha['_ChangedIsBusy'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Event message of 'IsBusy' command.")
        lc_cmdcha['_ChangedValue']  = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Event message of 'GetValue' command.")
        lc_cmdcha['_ChangedLimitStatus'] = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, helpstring="Event message of 'GetLimitStatus' command.  (Use with program option --limitstatuschannellist")

        lc_cmdctl['SetLogDir']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Set the log output directory.")
        lc_cmdctl['GetLogDir']         = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the log output directory.")
        lc_cmdctl['SetLogEnable']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Set the log output state enable or not.")
        lc_cmdctl['IsLogEnabled']      = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the log output state.")
        lc_cmdctl['SetDebugEnable']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Set the debug print output state enable or not.")
        lc_cmdctl['IsDebugEnabled']    = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the debug print output state.'")
        lc_cmdctl['SetLogLevel']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Set the log output detail level.(DEBUG:10,INFO:20,WARN:30,FATAL:40)")
        lc_cmdctl['GetLogLevel']       = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the log output detail level.")
        lc_cmdctl['SetDebugLevel']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Set the debug print output detail level.(DEBUG:10,INFO:20,WARN:30,FATAL:40)")
        lc_cmdctl['GetDebugLevel']     = PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommand('', ishelponly=True, isglobalcommand=True, helpstring="Return the debug print output detail level.")

        #
        self._deviceSTARSCommandCtrl    = lc_cmdctl
        self._deviceSTARSCommandChannel = lc_cmdcha
        return(True)

    def devicecommandobject(self,starscommand,level):
        rt = None
        if(level is None):
            pass
        elif(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER):
            if(starscommand in self._deviceSTARSCommandCtrl.keys()):
                rt = self._deviceSTARSCommandCtrl[starscommand]
        elif(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL):
            if(starscommand in self._deviceSTARSCommandChannel.keys()):
                rt = self._deviceSTARSCommandChannel[starscommand]
        return(rt)

    def get_commandlastexecutedtime(self):
        return(self._deviceCommandLastExecutedTime['LATEST']);

    def get_commandlastwaittime(self):
        return(self._deviceCommandLastWaitTime);

    def exec_command(self,level,starscommand,parameters,addrlist,busyCheck=True,checkOnly=False):
        dobj = self.devicecommandobject(starscommand,level)
        if(dobj is None):
            return("Er: Command undefined. (func='exec_command', starscommand=%s)" %(starscommand))
        elif(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER):
            if(dobj.isglobalcommand == False):
                return("Er: Command not found. (func='exec_command', level=%s, starscommand=%s)" %(str(level),starscommand))
            if(len(addrlist) <= 0):
                addrlist = [-1]
        elif(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL):
            if(dobj.ischannelcommand == False):
                return("Er: Command not found. (func='exec_command', level=%s, starscommand=%s)" %(str(level),starscommand))
            if(len(addrlist) <= 0):
                return("Er: No address. (func='exec_command', starscommand=%s)" %(starscommand))
        else:
            return("Er: Bad level assigned. (func='exec_command', level=%s, starscommand=%s)" %(str(level),starscommand))

        #Basic check
        paramarg = []
        devcommandtag = []
        replytagI = []

        cargnum=dobj.argnum
        ischeckcargnum=dobj.ischeckargnum
        ccommandtag = dobj.commandtag
        creplytag = dobj.replytag
        ctw  =dobj.postwaittime
        cisallowbusy=dobj.isallowbusy
        cisallowlocal=dobj.isallowlocal

        listflg = False
        if(len(parameters) > 0):
            if(isinstance(parameters[0], list) == True):
                listflg = True
        if(listflg == True):
            if(ischeckcargnum and (len(addrlist) != len(parameters))):
                return("Er: Program error. [func='exec_command', len(addrlist):%d != len(parameters):%d)]." %(len(addrlist),len(parameters)))
            for i in range(len(addrlist)):
                if(ischeckcargnum and (cargnum != len(parameters[i]))): return('Er: Bad parameters(address=%s,parameters=%s).' %(addrlist[i], str(parameters[i])))
                paramarg.append(parameters[i])
                devcommandtag.append(ccommandtag)
                if(dobj.checkfunc is not None):
                    if(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL):
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i], checkOnly)
                    else:
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i], checkOnly)
                    if(devcommandtag[i] == ''): return(errormsg)
                replytagI.append(creplytag)
        else:
            if(ischeckcargnum and (cargnum != len(parameters))): return('Er: Bad parameters.')
            for i in range(len(addrlist)):
                paramarg.append(parameters)
                devcommandtag.append(ccommandtag)
                if(dobj.checkfunc is not None):
                    if(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL):
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i], checkOnly)
                    else:
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i], checkOnly)
                    if(devcommandtag[i] == ''): return(errormsg)
                replytagI.append(creplytag)

        if(checkOnly):
            if(listflg == True):
                return(devcommandtag)
            else:
                return(devcommandtag[0])

        if(self._deviceFirmwareInfo is None):
            rt2 = self.device_init()
            if(rt2 == False):
                rt = self.error
                return(rt)

        setbflg=False
        #check busy if required
        if(busyCheck==True):
            busyCheck=False
            cuselocalbusy= False
            b = self.device_getisbusy()
            if(b == 1):
                return('Er: Busy.')
            self._device_setisbusy(0)
            for i in range(len(addrlist)):
                id = addrlist[i]
                id = '%0d' % int(id)
                if(int(id) >= 0):
                    if(cisallowbusy == False):
                        b = self.device_getflgbusy(id)
                        if(b == 1):
                            return('Er: Busy.')
                else:
                    if(cisallowbusy == False):
                        b = self.device_getflgbusy()
                        if(b == 1):
                            return('Er: Busy.')

            #set busy because for long process
            if(cuselocalbusy == True):
                setbflg=True
                cuselocalbusy=False

        rt='Er: No execution'

        rt2=''
        if((len(addrlist)>0)):
            for i in range(len(addrlist)):
                id = addrlist[i]
                id = '%0d' % int(id)
                if(int(id) < 0):
                    if(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER):
                        pass
                    else:
                        continue

                #wait sec since last command executed.
                tw=ctw
                tw2=self.get_commandlastwaittime()
                rtw=self._timewait(self.get_commandlastexecutedtime(),tw2)
                #cancel break
                if(rtw==False):
                    rt2='Operation canceled.'
                    break
                #execute command
                self._set_commandlastwaittime(tw)

                if(level == PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL):
                    devcommand = devcommandtag[i]
                    replytag = replytagI[i]
                else:
                    devcommand = devcommandtag[i]
                    replytag = replytagI[i]

                if(devcommandtag[i] == '' or devcommandtag[i] == '-'):
                    rt='Ok:'
                    if(dobj.postfunc is not None):
                        rt=eval(dobj.postfunc)(rt,replytag)
                    else:
                        rt=self._postbase(rt,replytag)
                    rt2=rt
                elif(dobj.isreferencecommand==True):
                    rt=self.device_send(devcommand)
                    #error break
                    if('Er:' in rt):
                        rt2=rt
                        break
                    tt = 0
                    rnum = 5
                    while(True):
                        if(tt>rnum):
                            rt3=self.device_receive(0.01)
                            if(rt == ''):
                                rt2 = 'Er: Timeout.'
                                break
                        else:
                            rt3=self.device_receive('')
                            if(rt3 == ''):
                                tt = tt + 1
                                continue
                        if('Er:' in rt3):
                            rt2 = rt3
                            break
                        if((rt3 == 'OK') or (rt3 == 'NG')):
                            continue
                        if(replytag is not None):
                            rt3=self._postbase(rt3,devcommand)
                        if(dobj.postfunc is not None):
                            rt3=eval(dobj.postfunc)(rt3,devcommand)
                            if(dobj.isreferencecommand==False):
                                if('Er:' not in rt3):
                                    rt3 = 'Ok:'
                        else:
                            rt3=self._postbase(rt3,devcommand)
                            if(dobj.isreferencecommand==False):
                                if('Er:' not in rt3):
                                    rt3 = 'Ok:'
                        if('Er:' in rt3):
                            rt2 = rt3
                            break
                        rt = rt3
                        break
                    if('Er:' in rt2):
                        break
                    if(rt2 == ''): rt2=rt
                    else: rt2=rt2+' '+rt
                else:
                    sendcmd = devcommand.split('\t')
                    for i in range(len(sendcmd)):
                        timeout=1.0
                        devcommand = sendcmd[i]
                        rt=self.device_send(devcommand)
                        #error break
                        if('Er:' in rt):
                            rt2=rt
                            break
                        tt = 0
                        rnum = 0
                        ###
                        while(True):
                            rt3=self.device_receive(timeout)
                            if(rt3 == ''):
                                 rt3 = 'Ok:'
                            if('Er:' in rt3):
                                rt2 = rt3
                                break
                            if(replytag is not None):
                                rt3=self._postbase(rt3,devcommand)
                            if(dobj.postfunc is not None):
                                rt3=eval(dobj.postfunc)(rt3,devcommand)
                                if(dobj.isreferencecommand==False):
                                    if('Er:' not in rt3):
                                         rt3 = 'Ok:'
                            else:
                                rt3=self._postbase(rt3,devcommand)
                                if(dobj.isreferencecommand==False):
                                    if('Er:' not in rt3):
                                        rt3 = 'Ok:'
                            if('Er:' in rt3):
                                rt2 = rt3
                                break
                            rt = rt3
                            break
                        ###
                        if('Er:' in rt2):
                            break
  
                    if('Er:' in rt2):
                        break
                    if(rt2 == ''): rt2=rt
                    else: rt2=rt2+' '+rt
            rt=rt2

        #release busy if not lock command
        if(setbflg==True):
            self._device_setisbusy(ctw)
        return(rt)

    ##################################################################
    # Device functions
    ##################################################################
    def device_getnumberofchannel(self):
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.numberofchannel)

    ## Device set busyflg
    def device_getflgbusy(self,channelnostr=None):
        b = self.device_getisbusy()
        if(b > 0):
           return(1)
        if(channelnostr is None):
            rt = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'IsBusy',[],[])
            if('Er:' in rt):
                return None
            if('1' in self._deviceLastBusyStatus.values()):
                b = 1
            else:
                b = 0
        else:
            rt = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,'IsBusy',[],[channelnostr])
            b = self._deviceLastBusyStatus[channelnostr]
        return(b)

    ## Device set busyflg
    def _device_setisbusy(self,f,tag='TIMEWAIT'):
        self._deviceBusyFlg[tag] = f
        if(self._inthandler is not None):
            rt=self._inthandler(time.time(),0)

    ## Device read busyflg
    def device_getisbusy(self,tag='TIMEWAIT'):
        if(tag in self._deviceBusyFlg):
            if(tag == 'TIMEWAIT'):
                if(self._deviceBusyFlg[tag]>0):
                    ct=time.time()
                    te=self.get_commandlastexecutedtime()
                    if(ct<te):
                        self._debugprint("device_getisbusy: Changed to stop by time swap. (current=%d, lastexecuted=%d)\n" %(ct, te))
                        self._deviceBusyFlg[tag]=0
                        return(0)
                    tlap=ct-te
                    if(tlap<self._deviceBusyFlg[tag]):
                        return(1)
            elif(self._deviceBusyFlg[tag]>=1):
                return(1)
        return(0)

    def device_getacccodelist(self):
        if(self._deviceFirmwareInfo is None): return([])
        return(self._deviceFirmwareInfo.accratecodelist)

    def device_getposition(self,channelnostr=None):
        if(channelnostr is None):
            rt = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'GetValue',[],[])
            return rt
        else:
            rt = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,'GetValue',[],[channelnostr])
            return(rt)
        return(b)

    def device_getcancelbacklash(self,channelnostr=None):
        if(channelnostr is None):
            return("Er: Invalid channelno '%s'" %(channelnostr))
        else:
            rt = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,'GetCancelBacklash',[],[channelnostr])
            return(rt)
        return(b)

    ##################################################################
    # Initialize
    ##################################################################
    def __init__(self, deviceHost, devicePost, inthandler=None, cmdhandler=None):
        self._deviceInstance = nportserv.nportserv.__init__(self, deviceHost, devicePost)
        self.setdelimiter('\n')
        self.setdelimiter('\r\n')
        self.settimeout(2)

        self._inthandler = inthandler
        self._cmdhandler = cmdhandler
        self._deviceBusyFlg              = {} #1: Busy 0:Stop
        self._deviceFirmwareInfo    = None
        self._deviceHardwareInfo    = None
        self._deviceLastBusyStatus      = {}
        self._deviceLastChannelStatus    = {}

        self._deviceCommandLastExecutedTime = {}
        self._deviceCommandLastWaitTime = 0


    ##################################################################
    # Internal Functions
    ##################################################################
    def _set_commandlastwaittime(self,t):
        self._deviceCommandLastWaitTime=t;

    def _timewait(self,timebase,lap):
        if(self._inthandler is not None):
            rt=self._inthandler(timebase,lap)
            return(True)
        if(lap<=0): return(True)
        self._debugprint("TimeWaitStart:%f\n" %lap)
        clap = 0
        while(True):
            ctime=time.time()
            l=ctime-timebase
            timebase=ctime
            if(l<=0):
                continue
            clap=clap+l
            l=lap-clap
            if(l<=0): break
            elif(l>0.1):
                #print("sleep")
                time.sleep(0.1)
        self._debugprint("TimeWaitEnd:%f\n" %clap)
        return(True)

    ##################################################################
    # Post functions(internal use)
    ##################################################################
    def _postbase(self,rt,devcommand):
        rt=self.processdevicereplystring(rt)
        if('Er:' in rt): return(rt)
        return(rt)

    def _postsetcommand(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        if(rt == 'NG'):
           if(devcommand in ['REM','LOC']):
               rt = 'Er: Busy.'
               return(rt)
        elif(rt == 'OK'):
           if(devcommand in ['REM','LOC']):
               rt=self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'GetFunction',[],[])
               if('Er:' in rt):
                   return(rt)
               if((devcommand == 'REM') and (rt != '1')):
                   rt = 'Er: Busy.'
               elif((devcommand == 'LOC') and (rt != '0')):
                   rt = 'Er: Busy.'
               else:
                   rt = 'Ok:'
        return(self._postbase(rt,devcommand))

    def _postgetbusystatus(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2 = rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        fsts = lambda x: str(int(x,16)&0x1)
        if(devcommand == 'STS_16?'):
            if('/' in rt2):
                rts=rt2.split('/')
                if(len(rts[1]) == 32):
                    rts2=re.split('(..)',rts[1])[1::2]
                    rts=list(map(fsts,rts2))
                    rt=','.join(rts)
                    for i in range(16):
                        self._deviceLastBusyStatus[str(i)]=rts[i]
        elif(len(devcommand) == 5 and devcommand.startswith('STS') and devcommand[4]=='?'):
            sptr=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(rt2)
            if(sptr.statusdetected == True):
                self._deviceLastBusyStatus[str(sptr.channel_no)]=sptr.busystatus
                self._deviceLastChannelStatus[str(sptr.channel_no)]=sptr
                ch = str(hex(sptr.channel_no))[2:].upper()
                if(ch == devcommand[3]):
                    rt=str(sptr.busystatus)
        else:
            rt="Er: Unexpected caller %s to '%s' in _postgetbusystatus()." %(rt2, devcommand);
        return(rt)

    def _postgetlimitstatus(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2 = rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        fsts = lambda x: str(int(x,16)&0b0111)
        if(devcommand == 'LS_16?'):
            rts=list(rt2)
            if(len(rts) == 16):
                rt=','.join(list(map(fsts,rts)))
        elif(len(devcommand) == 5 and devcommand.startswith('STS') and devcommand[4]=='?'):
            sptr=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(rt2)
            if(sptr.statusdetected == True):
                self._deviceLastChannelStatus[str(sptr.channel_no)]=sptr
                ch = str(hex(sptr.channel_no))[2:].upper()
                if(ch == devcommand[3]):
                    rt = str(sptr.limitstatus)
        else:
            rt="Er: Unexpected caller %s to '%s' in _postgetlimitstatus()." %(rt2, devcommand);
        return(rt)


    def _postgetvalue(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2 = rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        fval = lambda x: str(int(x))
        if(devcommand == 'PS_16?'):
            rts=rt2.split('/')
            if(len(rts) == 16):
                rt=','.join(list(map(fval,rts)))
        elif(len(devcommand) == 5 and devcommand.startswith('STS') and devcommand[4]=='?'):
            sptr=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(rt2)
            if(sptr.statusdetected == True):
                self._deviceLastChannelStatus[str(sptr.channel_no)]=sptr
                ch = str(hex(sptr.channel_no))[2:].upper()
                if(ch == devcommand[3]):
                    rt = str(sptr.position)
        elif(devcommand.startswith('SHP?')):
            if('NO' in rt2):
                #rt = "Er: %s" %(rt2)
                rt = '-'
            else:
                (rt2,errormsg)=self._sub_checkisinteger('',[rt2])
                if(rt2 != ''):
                    rt = rt2
        else:
            (rt2,errormsg)=self._sub_checkisinteger('',[rt2])
            if(rt2 != ''):
                rt = rt2
        return(rt)

    def _postgetholdoffstatus(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2 = rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        fsts = lambda x: str((int(x,16)&0b1000)>>3)
        if(devcommand == 'LS_16?'):
            rts=list(rt2)
            if(len(rts) == 16):
                rt=','.join(list(map(fsts,rts)))
        elif(len(devcommand) == 5 and devcommand.startswith('STS') and devcommand[4]=='?'):
            sptr=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERChannelStatus(rt2)
            if(sptr.statusdetected == True):
                self._deviceLastChannelStatus[str(sptr.channel_no)]=sptr
                ch = str(hex(sptr.channel_no))[2:].upper()
                if(ch == devcommand[3]):
                    rt = str(sptr.holdoffstatus)
        else:
            rt="Er: Unexpected caller %s to '%s' in _postgetholdoffstatus()." %(rt2, devcommand);
        return(rt)


    def _postgetholdstatus(self,rt,devcommand):
        rt = self._postgetholdoffstatus(rt,devcommand)
        if('Er:' in rt): return(rt)
        rt2 = rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        fsts = lambda x: str(int(x,16)^0x1)
        if(devcommand == 'LS_16?'):
            rts=rt2.split(',')
            if(len(rts) == 16):
                rt=','.join(list(map(fsts,rts)))
        elif(len(devcommand) == 5 and devcommand.startswith('STS') and devcommand[4]=='?'):
            if(rt2 == '0'):
                rt = '1'
            elif(rt2 == '1'):
                rt = '0'
            else:
                rt="Er: Unexpected reply '%s' to '%s' by _postgetholdoffstatus()." %(rt2,devcommand);
        else:
            rt="Er: Unexpected caller %s to '%s' in _postgetholdstatus()." %(rt2, devcommand);
        return(rt)

    def _postgetspeedselection(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2=rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        if(len(rt2) == 4 and rt2.endswith('SPD')):
            rt = rt2[0]
        else:
            (rt2,errormsg)=self._sub_checkisinteger('',[rt2])
            if(rt2 != ''):
                rt = rt2
        return(rt)

    def _postgetaccratevalue(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt = self._postgetaccratecode(rt,devcommand)
        if('Er:' in rt): return(rt)
        rt2=rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        cd = int(rt2)
        l = len(self._deviceFirmwareInfo.accratecodelist)
        if(0<=cd and cd<l):
            rt=self._deviceFirmwareInfo.accratecodelist[cd]
            rt=str(rt)
        return(rt)

    def _postgetaccratecode(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None): return('',errormsg)
        rt2=rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        (rt2,errormsg) = self._sub_checkisinteger('',[rt2])
        if(rt2 != ''):
            cd = int(rt2)
            rt=str(cd)
        return(rt)

    def _postsetacscontrol(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        rt2=rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        if(len(rt2) <= 5):
            pass
        elif(devcommand.startswith('ACS?')):
            if(rt2[:4] == devcommand[4:]):
                rt2 = rt2[5:]
                if(rt2[-1] == '/'):
                    rt2 = rt2[:-1]
                rts=rt2.split('/')
                rt = ' '.join(rts)
        return(rt)

    def _postgetlansrq(self,rt,devcommand):
        if('Er:' in rt): return(rt)
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None): return('',errormsg)
        rt2=rt
        rt="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        if(devcommand == 'LN_SRQ?G'):
            if(len(rt2) == 4):
                rt2=int(rt2,16)
                rt2=format(rt2, '0%db' % (self._deviceFirmwareInfo.numberofchannel))
                rt2=rt2[::-1]
                rt=','.join(list(rt2))
                return(rt)
        else:
            if((rt2 == '0') or (rt2 == '1')):
                return(rt)
        return(rt)

    def _postgettimingoutfixchannel(self,rt,devcommand):
        if(rt == 'Ok:'):
            if(devcommand is not None):
                rt = devcommand
        rt2 = self._postgetonoff(rt, devcommand)
        return(rt2)

    def _postgetremote(self,rt,devcommand):
        rt2="Er: Unexpected reply %s to '%s'" %(rt, devcommand);
        if(rt.startswith('R')):
            rt2='1'
        elif(rt.startswith('L')):
            rt2='0'
        return(rt2)
    def _postgetonoff(self,rt,devcommand):
        rt = rt.upper()
        if(rt == ''):
            return('Er: No Reply.')
        elif(rt == 'EN'):  rt = '1'
        elif(rt == 'DS'):  rt = '0'
        elif(rt == 'ON'):  rt = '1'
        elif(rt == 'OFF'): rt = '0'
        elif(rt == 'YES'): rt = '1'
        elif(rt == 'NO'):  rt = '0'
        elif(rt == 'READY'):  rt = '1'
        elif(rt == 'NOT READY'):  rt = '0'
        else:
            return("Er: Unexpected reply '%s'." %(rt))
        return(rt)
    ##################################################################
    # Check functions(internal use)
    ##################################################################
    #Simple set channel only
    def _checkchsetcommand(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        rt = cmd % (ch)
        return(rt,'')

    #HP research
    def _checkrescanhome(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        rt = ''
        rt2=self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,'GetHomePosition',[],[id])
        if('Er:' in rt2): return(rt,rt2)
        if(rt2 == '-'):  return(rt,'Er: NO H.P')
        rt = cmd % (ch)
        return(rt,'')


    # ACS control
    def _checksetacscontrol(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        errormsg = 'Er: Bad parameters.'
        params=args
        rts=[]
        if(len(args)==0):
            return(rt,errormsg)
        buf='/'.join(args)
        if(buf.endswith('/')):
            buf = buf[:-1]
            if(len(buf)<=0):
                return(rt,errormsg)
        params=buf.split('/')
        lnum = len(params)
        if(cmd.startswith('ACS?')):
            if(lnum not in [1]):
                return(rt,errormsg)
        elif(cmd.startswith('ACS%')):
            if(lnum not in [2,4,5]):
                return(rt,errormsg)
        else:
            return(rt,errormsg)
        #Check dnos
        (rt2,errormsg2) = self._sub_checkisinteger('',[params[0]])
        if(rt2 == ''):
            errormsg = 'Er: Bad parameters. data no. range is from %ld to %ld.' %(0, 127)
            return(rt,errormsg)
        num = int(rt2)
        if((num<0) or (num>127)):
            errormsg = 'Er: Bad parameters. data no. range is from %ld to %ld.' %(0, 127)
            return(rt,errormsg)
        rts.append('{:03}'.format(num))
        if(lnum == 1):
            rt = cmd % (ch,'/'.join(rts))
            return(rt,errormsg)
        #Check chg
        acmd = params[1].upper()
        #Case chg == 'END'
        if(lnum == 2):
            if(acmd not in ['END']):
                return(rt,errormsg)
            rts.append(acmd)
            rt = cmd % (ch,'/'.join(rts))
            return(rt,'')
        adata = params[2]
        (rt2,errormsg2) = self._sub_checkisinteger('',[adata])
        if(rt2 == ''):
            return(rt,errormsg2)
        num = int(rt2)
        min = self._deviceFirmwareInfo.value_minimum['POSITION']
        max = self._deviceFirmwareInfo.value_maximum['POSITION']
        #Case chg == 'TIM', 'ADD', 'ACC', 'DEC'
        if(acmd in ['TIM']):
            min = 0
            max = 65535
        elif(acmd in ['ADD']):
            pass
        elif(acmd in ['ACC','DEC']):
            min = self._deviceFirmwareInfo.value_minimum['SPEED']
            max = self._deviceFirmwareInfo.value_maximum['SPEED']
        else:
            return(rt,errormsg)
        if(min>num or num>max):
            errormsg = 'Er: Bad parameters. %s data range is from %ld to %ld.' %(acmd, min, max)
            return(rt,errormsg)
        rts.append(acmd)
        rts.append(str(num))
        #Check fnc
        amotion = params[3].upper()
        #Case fnc == 'NOP', 'FST', 'SLW'
        if(lnum == 4):
            if(amotion not in ['NOP','FST','SLW']):
                return(rt,errormsg)
            rts.append(amotion)
            rt = cmd % (ch,'/'.join(rts))
            return(rt,'')
        #Case fnc == 'RTE', 'SPD'
        elif(lnum == 5):
            if(amotion in ['RTE']):
                min = 0
                max = 115
                acdlist=self.device_getacccodelist()
                if(len(acdlist) != (max+1)):
                    errormsg = "Er: Unexpected RTE setup length '%s' in _checksetacscontroll()." %(len(acslist))
                    return(rt,errormsg)
            elif(amotion in ['SPD']):
                min = self._deviceFirmwareInfo.value_minimum['SPEED']
                max = self._deviceFirmwareInfo.value_maximum['SPEED']
            else:
                return(rt,errormsg)
            aspd = params[4]
            (rt2,errormsg2) = self._sub_checkisinteger('',[aspd])
            if(rt2 == ''):
                return(rt,errormsg2)
            num = int(rt2)
            if(min>num or num>max):
                errormsg = 'Er: Bad parameters. %s data range is from %ld to %ld.' %(amotion, min, max)
                return(rt,errormsg)
            rts.append(amotion)
            rts.append(str(num))
            rt = cmd % (ch,'/'.join(rts))
            return(rt,errormsg)
        else:
            return(rt,errormsg)
        return(rt,errormsg)

    # Channel control
    def _checksetchannel(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        rt = ''
        cmds = cmd.split('\t')
        issetch = False
        rts = []
        busylist = None
        setchlist = None
        remchlist = ''
        for cmd2 in cmds:
            errormsg = 'Er: Bad parameters.'
            # Query Disp Channel
            if(cmd2 in ['SETCH?']):
                rts.append(cmd2)
                continue
            # Query Timingout Channel
            elif(cmd2 in ['TMGCH?']):
                rt2=self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'GetTimingOutChannelFixEnable',[],[])
                if('Er:' in rt2):
                    return(rt, rt2)
                # if Timingout Channel Fix disabled ---> use disp channel
                if(rt2 == '0'):
                    cmd2 = cmd2.replace('TMG','SET')
                rts.append(cmd2)
            # Change Disp Channel|Timingout Channel
            elif(cmd2[0:6] in ['SETCH%','TMGCH%']):
                #Check setchannels params
                val = args[0].upper()
                if(setchlist is None):
                    if(len(val) != 4):
                        return(rt, errormsg)
                    #elif(val.count('-') == 4):
                    #    return(rt, errormsg)
                    elif(len(val) != len(set(val))):
                        valc=val.replace('-','')
                        if(len(valc) != len(set(valc))):
                            return(rt, errormsg)
                    for i in range(len(val)):
                        v = val[i]
                        if(v == '-'):
                            pass
                        else:
                            (id,errordummy)=self._sub_checkishex('',[v])
                            if(id == ''):
                                return(rt,errormsg)
                            id2=int(id)
                            if((0 <= id2) and (id2 < self.device_getnumberofchannel())):
                                pass
                            else:
                                return(rt,errormsg)
                #Load busyflg
                if(busylist is None):
                    rt2 = self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'IsBusy',[],[])
                    if('Er:' in rt2):
                        return(rt,rt2)
                    busylist = self._deviceLastBusyStatus
                #Check current channels
                selchcmd = cmd2[0:5]+'?'
                if(selchcmd == 'TMGCH?'):
                    rt2=self.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'GetTimingOutChannelFixEnable',[],[])
                    if('Er:' in rt2):
                        return(rt,rt2)
                    # if Timingout Channel Fix disabled ---> use disp channel
                    if(rt2 == '0'):
                        if(issetch):
                            continue
                        selchcmd = selchcmd.replace('TMG','SET')
                        cmd2 = cmd2.replace('TMG','SET')
                if(selchcmd.startswith('SETCH')):
                    issetch = True
                rt2 = self.device_act(selchcmd)
                if('Er:' in rt2):
                    return(rt,rt2)
                elif(len(rt2) != 4):
                    errormsg = "Er: Unexpected reply '%s' to '%s' in _checksetchannel()." %(rt2,selchcmd)
                    return(rt,errormsg)
                selchlist = rt2
                if(setchlist is None):
                    setchlist = val
                    remchlist = selchlist
                    for i in range(len(setchlist)):
                        if(setchlist[i] == '-'):
                            continue
                        setid = str(int(setchlist[i],16))
                        hex_setid = str(setchlist[i])
                        #Check sellist
                        if(setid in busylist):
                            if((issetch==False) and (busylist[setid] == '1')):
                                errormsg = 'Er: Busy'
                                return(rt,errormsg)
                        if(hex_setid in remchlist):
                           remchlist=remchlist.replace(hex_setid,'')
                #Decide set channels and check sel channels if not busy.
                for i in range(len(selchlist)):
                    if(setchlist[i] == '-'):
                        if(len(remchlist)<=0):
                            errormsg = "Er: Unexpected error no remlist at loop(%d) in _checksetchannel()." %(i)
                        setchlist=setchlist.replace('-',remchlist[0],1)
                        remchlist=remchlist[1:]
                    selid = str(int(selchlist[i],16))
                    hex_selid = str(selchlist[i])
                    #Check setlist
                    if(selid in busylist):
                        if(busylist[selid] == '1'):
                            errormsg = 'Er: Busy'
                            return(rt,errormsg)
                    else:
                        errormsg = "Er: Unexpected id parameter '%s' in _checksetchannel()." %(selid)
                val = ''.join(setchlist)
                rts.append(cmd2 % (val))
            else: 
                return(rt,errormsg)
        rt = '\t'.join(rts)
        return(rt,errormsg)

    # Timing out Mode
    def _checksettimingout(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        cmd2 = cmd[0:4]
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        val = ''
        errormsg = "Er: Unexpected cmd parameter '%s' in _checksettimingout()." %(cmd)
        # Query Timingout channel enabled/disabled
        if(cmd in ['TMGFX?']):
            if(self._deviceFirmwareInfo.is_commandsupported('TMGFX') == True):
                rt = cmd
            else:
                rt = '-'
        # Change Timingout channel enabled/disabled
        elif(cmd[0:6] in ['TMGFX ']):
            if(self._deviceFirmwareInfo.is_commandsupported('TMGFX') == True):
                (rt2,errormsg) = self._checksetonoff(cmd,args,id,checkonly)
                if(rt2 == ''):
                   return(rt2,errormsg)
                rt = rt2
            else:
                (rt2,errormsg) = self._checksetonoff(cmd,args,id,checkonly)
                if(rt2 == ''):
                   return(rt2,errormsg)
                if('DS' in rt2):
                    rt = '-'
                else:
                    errormsg='Er: Only value 0(=OFF) is supported at this device.'
                    return(rt,errormsg)
        elif(cmd2 in ['TMGI','TMGS','TMGE']):
            (rt2,errormsg) = self._checksetrange(cmd,args,id,checkonly)
            if(rt2 == ''):
                return(rt2,errormsg)
            rt = rt2
            (val,errormsg) = self._sub_checkisinteger('',args)
        elif(cmd2 in ['TMGM']):
            val = args[0]
            errormsg='Er: Bad parameters. Value is 0 to 5.'
            if(val in ['0','1','2','3','4','5']):
                rt = cmd % (ch, val)
        elif(cmd2 in ['TMG%']):
            (rt2,errormsg) = self._checksetonoff('',args,id,checkonly)
            if(rt2 == ''):
                return(rt2,errormsg)
            if(rt2 == '1'):
               rt = cmd %('R',ch)
            else:
               rt = cmd %('C',ch)
        else:
            return(rt,errormsg)
        return(rt,errormsg)

    # Return motion command
    def _checkmoveposition(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',[args[0]])
        if(rt2 == ''): return(rt,errormsg)
        val = int(rt2)
        min = self._deviceFirmwareInfo.value_minimum['POSITION']
        max = self._deviceFirmwareInfo.value_maximum['POSITION']
        cbk = ''
        cpos = 0
        if(len(args) >= 3):
            (rt2,errormsg) = self._sub_checkisinteger('',[args[3]])
            if('Er:' in rt2):
                return(rt,rt2)
            cpos = int(rt2)
        else:
            rt2=self.device_getposition(str(int(id)))
            if('Er:' in rt2):
                return(rt,rt2)
            cpos = int(rt2)
        rval=val
        if(cmd.startswith('REL')):
            rval=cpos+val
            if((min<=rval) and (rval<=max)):
                pass
            else:
                errormsg = 'Er: Out of range.'
                return(rt,errormsg)
        if((min<=rval) and (rval<=max)):
            pass
        else:
            errormsg = 'Er: Out of range.'
            return(rt,errormsg)

        if(len(args) >= 2):
            rt2 = args[1]
            if(rt2 == ''):
                cbk=''
            elif(rt2 in ['B','S']):
                cbk=rt2
            else:
                errormsg = "Er: Invalid backlash mode in cmd '%s'." %(cmd)
                return('',errormsg)
        else:
            rt2=self.device_getcancelbacklash(str(int(id)))
            if('Er:' in rt2):
                return(rt,rt2)
            cb = int(rt2)
            if((cb > 0) and ((rval-cpos) > 0)):
                cbk = 'B'
            elif((cb < 0) and ((rval-cpos) < 0)):
                cbk = 'B'
        rt = cmd % (ch,cbk,str(val))
        addcmd = 'LN_SRQ%s1' %(ch)
        rt = addcmd + '\t' + rt
        return(rt,errormsg)

    # Return motion command
    def _checksethpvalue(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        if(args[0] == '-'):
            return('-','')
        (rt2,errormsg) = self._checksetrange(cmd,args,id,checkonly)
        return(rt2,errormsg)

    # Return speed set command
    def _checksetspeedcurrent(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''): return(rt2,errormsg)
        val = int(rt2)
        min = self._deviceFirmwareInfo.value_minimum['SPEED']
        max = self._deviceFirmwareInfo.value_maximum['SPEED']
        if((min<=val) and (val<=max)):
            rt = cmd % (ch,rt2)
        else:
            errormsg = 'Er: Speed range is from %ld to %ld.' %(min, max)
        rt2 = self.device_getflgbusy(id)
        if(rt2 == '0'):
            rt = '-'
        return(rt,errormsg)

    # Return speed set command
    def _checksetspeedvalue(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''): return(rt2,errormsg)
        val = int(rt2)
        min = self._deviceFirmwareInfo.value_minimum['SPEED']
        max = self._deviceFirmwareInfo.value_maximum['SPEED']
        if((min<=val) and (val<=max)):
            rt = cmd % (ch,rt2)
        else:
            errormsg = 'Er: Speed range is from %ld to %ld.' %(min, max)
        return(rt,errormsg)

    # Return acc rate code set command
    def _checksetaccratecode(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''): return(rt2,errormsg)
        val = int(rt2)
        min = 0
        max=len(self._deviceFirmwareInfo.accratecodelist)-1
        if((min<=val) and (val<=max)):
            rt = cmd % (ch,rt2)
        else:
            errormsg = 'Er: Acc code is from %ld to %ld.' %(min, max)
        return(rt,errormsg)

    # Return acc rate code set command
    def _checksetaccratevalue(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        rt = ''
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisfloat('',args)
        if(rt2 == ''): return(rt2,errormsg)
        val = float(rt2)
        min = 0
        rt2 = len(self._deviceFirmwareInfo.accratecodelist)-1
        for i in range(1,len(self._deviceFirmwareInfo.accratecodelist)):
            if(self._deviceFirmwareInfo.accratecodelist[i]<val):
                #rt2=self._deviceFirmwareInfo.accratecodelist[i-1]
                rt2 = i-1
                break
        rt2 = str(rt2).zfill(3)
        rt = cmd % (ch,rt2)
        return(rt,errormsg)

   # Return setup etc. command
    def _checkchsetup(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        val = args[0].upper()
        rt=''
        if(cmd.startswith('SETMT')):
            errormsg='Er: Bad parameters.'
            if(len(val)==4):
                if(val[0] in ['0','1']):
                    if(val[1] in ['0','1']):
                        if(val[2] in ['0','1','2']):
                            if(val[3] in ['0','1','2']):
                                rt = val
        elif(cmd.startswith('SETLS')):
            errormsg='Er: Bad parameters.'
            if(len(val)==8):
                if(val[4] == '0'):
                    rt = val
                    for v in list(val):
                        if(v not in ['0','1']):
                            rt = ''
                            break
        elif(cmd.startswith('SETHP')):
            errormsg='Er: Bad parameters.'
            if(len(val)==4):
                if(val[0] == '0'):
                    rt = val
                    for v in list(val):
                        if(v not in ['0','1']):
                            rt = ''
                            break
        elif(cmd.startswith('STOPMD')):
            errormsg='Er: Bad parameters.'
            if(len(val)==2):
                rt = val
                for v in list(val):
                    if(v not in ['0','1']):
                        rt = ''
                        break
        if(rt == ''):
            return(rt,errormsg)
        rt = cmd % (ch,rt)
        return(rt,errormsg)

    def _checksetrange(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None): return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''): return(rt,errormsg)
        val = int(rt2)
        min = self._deviceFirmwareInfo.value_minimum['POSITION']
        max = self._deviceFirmwareInfo.value_maximum['POSITION']
        valname = 'Pulse'
        if(cmd.startswith('B%')):
            min = -9999
            max =  9999
            valname = 'Backlash'
        elif(cmd.startswith('SETJG')):
            min = 1
            max = 9999
            valname = 'Jog pulse'
        elif(cmd.startswith('TMGI')):
            min = 1
            valname = 'Timing out interval'
        if((min<=val) and (val<=max)):
            if(cmd.startswith('B%')):
                rt2 = '{:+05}'.format(val)
            rt = cmd % (ch,rt2)
        else:
            errormsg = 'Er: Bad parameters. %s range is from %ld to %ld.' %(valname, min, max)
        return(rt,errormsg)
    def _checksetonoff(self,cmd,args,id,checkonly):
        ch = str(hex(int(id)))[2:].upper()
        (val,errormsg) = self._sub_checksetonoff('',args)
        if(val == ''): return(val,errormsg)
        rt=val
        errormsg = "Er: Unexpected cmd parameter '%s' in _checkchsetonoff()." %(cmd)
        if(cmd.startswith('HOLD')):
            if(val == '1'):
                rt = cmd %(ch,'ON')
            else:
                rt = cmd %(ch,'OFF')
        elif(cmd.startswith('ALL_REP')):
            if(val == '1'):
                rt = cmd %('EN')
            else:
                rt = cmd %('DS')
        elif(cmd.startswith('TMGFX')):
            if(val == '1'):
                rt = cmd %('EN')
            else:
                rt = cmd %('DS')
        elif(cmd.startswith('ACS')):
            if(val == '1'):
                rt = cmd %('P', ch)
            else:
                rt = cmd %('C', ch)
        return(rt,errormsg)
    def _checksetremlocbyarg(self,cmd,args,id,checkonly):
        val=args[0].upper()
        rt = ''
        errormsg='Er: Bad parameters.'
        if(val == '1'):
            rt = 'REM'
        elif(val == '0'):
            rt = 'LOC'
        elif(val in ['REM','LOC']):
            rt = val
        return(rt,errormsg)

    def _sub_checksetonoff(self,cmd,args):
        val=args[0].upper()
        rt = ''
        errormsg='Er: Bad parameters.'
        if(val in ['1','0']):
            pass
        elif(val == 'EN'):
            val = '1'
        elif(val == 'DS'):
            val = '0'
        elif(val == 'ON'):
            val = '1'
        elif(val == 'OFF'):
            val = '0'
        if(val == '1' or val == '0'):
            rt = val
        if(cmd == ''): return(rt,errormsg)
        return(cmd+" "+rt,errormsg)
    def _sub_checkishex(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg = "Er: Bad parameters. Not hex.(%s)" %(val)
        if(val == ''): return(rt,errormsg)
        try:
            n = int(val,16)
            rt = str(n)
        except ValueError:
            return('',errormsg)
        if(cmd == ''): return(rt,errormsg)
        return(cmd+" "+rt,errormsg)
    def _sub_checkisfloat(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg = "Er: Bad parameters. Not float.(%s)" %(val)
        if(val == ''): return(rt,errormsg)
        try:
            n = float(val)
            rt = str(n)
        except ValueError:
            return('',errormsg)
        if(cmd == ''): return(rt,errormsg)
        return(cmd+" "+rt,errormsg)
    def _sub_checkisinteger(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg = "Er: Bad parameters. Not integer.(%s)" %(val)
        if(val == ''): return(rt,errormsg)
        try:
            n = float(val)
            if(n.is_integer()):
                rt = '%0.0lf' %(n)
        except ValueError:
            return('',errormsg)
        if(cmd == ''): return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

#######################################
## STARS interval handler:
#######################################
def interval():
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_ChannelNameList
    global gb_LogDir
    global gb_LogEnable
    global gb_Debug
    global gb_LogLevel
    global gb_DebugLevel

    st = gb_StarsInstance
    dc = gb_DeviceInstance
    channelnamelist = list(gb_ChannelNameList.keys())
    now = time.time()

    # Check device connectection lost or not, and read buffer.
    if(dc.isconnected() == False):
        destsendstr = 'Device disconnected.'
        _outputlog(WARN, destsendstr)
        _outputlog(WARN, 'Terminating STARS.')
        st.terminateMainloop()
        rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
        return False
    
    # Check log switch
    v_logerrormax = 20
    if(st._isloggererrordetectedtimes <= v_logerrormax):
        rt = setup_logger(st.nodename)
        if(rt == 'Ok:'):
            st._isloggererrordetectedtimes = 0
        else:
            st._isloggererrordetectedtimes = st._isloggererrordetectedtimes + 1
            destsendstr = 'Logger error detected.'
            rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
            destsendstr = destsendstr + rt
            rt=stars_sendevent(eventmessage='_Msg '+destsendstr)

    keepalivetime = 1800
    # set for TEST
    #keepalivetime = 100
    llap = now - st._lastsendtime
    if(llap<0): llap = keepalivetime
    if(llap>=keepalivetime):
        _outputlog(WARN,"*** Sending keepalive to STARS. ***")
        rt=stars_sendevent(eventmessage='_alive')
        if(rt == False):
            _outputlog(WARN, 'Terminating STARS.')
            st.terminateMainloop()
            return False
        st._lastsendtime = now
        if(st._isloggererrordetectedtimes > v_logerrormax):
            rt = setup_logger(st.nodename)
            if(rt == 'Ok:'):
                st._isloggererrordetectedtimes = 0

    # Check if device in lock state
    llock=dc.device_getisbusy()
    # Return if device in lock state.
    if(llock == 1):
        return True

    # Load cache
    destsendstr = '%s in interval(). [%s]'
    listptr=[]
    listptr_pre=[]
    for starscommand in ['IsBusy','GetValue','GetLimitStatus']:
        buf=stars_getdevicechannelvalue(channelname='',local=True, starscommand=starscommand)
        if('Er' in buf):
            destsendstr=destsendstr %(buf,starscommand)
            rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
            return False
        listptr_pre.append(np.array(buf.split(',')))

    # Check rem/local
    isremote = st._deviceisremote
    rinterval = 2.0
    starscommand = 'GetFunction'
    rlap=now-st._lasttgetvaluetimestamp[starscommand]
    if(rlap<0): rlap = rinterval
    allstop=np.all(listptr_pre[0]=='0')
    changed2remote = False
    if((isremote != '1') or allstop):
        if(rlap>=rinterval):
            buf=stars_getdevicecontrollervalue(local=False, starscommand=starscommand)
            if('Er' in buf):
                destsendstr=destsendstr %(buf,starscommand)
                rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
                return False
            elif(buf in ['0','1']):
                st._lasttgetvaluetimestamp[starscommand] = now
                if(isremote != buf):
                    st._deviceisremote = buf
                    isremote = st._deviceisremote
                    if(st._deviceisremote == '1'):
                        changed2remote = True
                        _outputlog(INFO,"*** Device changed to remote. ***")
                    else:
                        _outputlog(INFO,"*** Device changed to local. ***")
                    stars_sendevent(childnode='', eventmessage='_ChangedFunction '+st._deviceisremote)
            else:
                destsendstr=destsendstr %("Unexpected reply '" + buf + "'",starscommand)
                stars_sendevent(eventmessage='_Msg '+destsendstr)
                return False

    if(changed2remote):
        starscommand = 'ResetLANSRQFlag'
        rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,starscommand,['1'],[])
        if('Er' in buf):
            destsendstr=destsendstr %(buf,starscommand)
            rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
            #return False
        st._lasttgetvaluetimestamp[starscommand] = now

    # Force ALLREPEN
    if((isremote == '1') and (dc._deviceFirmwareInfo.is_commandsupported('ALL_REP') == True)):
        ainterval = 2.0
        autorepenenable = st._deviceautorepenenable
        starscommand = 'GetAllReplyEnable'
        alap=now-st._lasttgetvaluetimestamp[starscommand]
        if(alap<0):
            alap = ainterval
        if((autorepenenable != '1') or (alap>=ainterval)):
            buf=stars_getdevicecontrollervalue(local=False, starscommand=starscommand)
            if('Er' in buf):
                destsendstr=destsendstr %(buf,starscommand)
                rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
                return False
            elif(buf in ['0','1']):
                st._lasttgetvaluetimestamp[starscommand] = now
                st._deviceautorepenenable = buf
                if(buf != '1'):
                    _outputlog(INFO,"*** Device set all reply enable. ***")
                    starscommand = 'SetAllReplyEnable'
                    rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,starscommand,['1'],[])
                    if('Er' in buf):
                        destsendstr=destsendstr %(buf,starscommand)
                        rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
                    #return False
                st._lasttgetvaluetimestamp[starscommand] = now
            else:
                destsendstr=destsendstr %("Unexpected reply '" + buf + "'",starscommand)
                rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
                return False

    # Refresh values
    testtimes = 1.0
    finterval = 0.1*testtimes
    vinterval = 0.5*testtimes
    if(isremote == '0'):
        finterval = 0.2*testtimes
        vinterval = 1.0*testtimes
    flap=now-st._lasttgetvaluetimestamp['IsBusy']
    vlap=now-st._lasttgetvaluetimestamp['GetValue']
    if(flap<0): flap = finterval
    if(vlap<0): vlap = vinterval
    starscommandlist = []
    if((vlap>=vinterval) or changed2remote):
        starscommandlist = ['IsBusy','GetValue','GetLimitStatus']
    elif(flap>=finterval):
        starscommandlist = ['IsBusy']
    if(len(starscommandlist)>0):
        for starscommand in starscommandlist:
            buf=stars_getdevicechannelvalue(channelname='',local=False, starscommand=starscommand)
            if('Er' in buf):
                destsendstr=destsendstr %(buf,starscommand)
                rt=st.send(st.nodename+'._Alert>System _Msg '+destsendstr)
                return False
            st._lasttgetvaluetimestamp[starscommand] = now
            listptr.append(np.array(buf.split(',')))
        clist = []
        f_compare = (listptr_pre[0] == listptr[0])
        flist=np.where(f_compare!=True)
        flist = list(flist[0])
        clist=flist
        vlist = []
        llist = []
        if(len(listptr) > 1):
            v_compare = (listptr_pre[1] == listptr[1])
            vlist=np.where(v_compare!=True)
            vlist = list(vlist[0])
            clist = clist + vlist
            l_compare = (listptr_pre[2] == listptr[2])
            llist=np.where(l_compare!=True)
            llist = list(llist[0])
            clist = clist + llist
        if(len(clist)>0):
            clist=list(set(clist))
            clist.sort()
        
        #Busy changed
        ltrg='0'
        for i in clist:
            if(i in flist):
                if(listptr[0][i] == '1'):
                    stars_setlocalcurrent([channelnamelist[i]],[listptr[0][i]], starscommand='IsBusy')
                    buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='IsBusy')
                    listptr_pre[0][i] = buf
                #To stop
                elif(listptr[0][i] == '0'):
                    if(ltrg=='0'):
                        if(len(listptr) <= 1):
                            #Read values not yet
                            for starscommand in ['GetValue','GetLimitStatus']:
                                buf=stars_getdevicechannelvalue(channelname='',local=False, starscommand=starscommand)
                                if('Er' in buf):
                                    destsendstr=destsendstr %(buf,starscommand)
                                    rt=st.send(st.nodename+'._Alert>System _Msg '+destsendstr)
                                    return False
                                listptr.append(np.array(buf.split(',')))
                                st._lasttgetvaluetimestamp[starscommand] = now
                        stars_setlocalcurrent([channelnamelist[i]],[listptr[1][i]], starscommand='GetValue',force=True)
                        buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='GetValue')
                        listptr_pre[1][i] = buf
                        buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='GetLimitStatus')
                        listptr_pre[2][i] = buf
                        stars_setlocalcurrent([channelnamelist[i]],[listptr[0][i]], starscommand='IsBusy')
                        buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='IsBusy')
                        listptr_pre[0][i] = buf
                continue
            elif(i in vlist):
                if(listptr[0][i] == '0'):
                    listptr[0][i] = '1'
                    stars_setlocalcurrent([channelnamelist[i]],[listptr[0][i]], starscommand='IsBusy')
                    buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='IsBusy')
                    listptr_pre[0][i] = buf
                stars_setlocalcurrent([channelnamelist[i]],[listptr[1][i]], starscommand='GetValue')
                buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='GetValue')
                listptr_pre[1][i] = buf
                stars_setlocalcurrent([channelnamelist[i]],[listptr[2][i]], starscommand='GetLimitStatus')
                buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='GetLimitStatus')
                listptr_pre[2][i] = buf
            elif(i in llist):
                stars_setlocalcurrent([channelnamelist[i]],[listptr[2][i]], starscommand='GetLimitStatus')
                buf=stars_getdevicechannelvalue(channelname=channelnamelist[i],local=True, starscommand='GetLimitStatus')
                listptr_pre[2][i] = buf

    return True

##################################################################
# Callback functions:
##################################################################
## Device raw command control handler:
## Device socket handler: DETECT

def device_sockhandler(sock, tm='', printflg=True):
    global gb_StarsInstance
    global gb_DeviceInstance
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    if(printflg == True): 
        destsendstr="Device_detected %s." %(st.nodename)
        _outputlog(INFO, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
    rt = dc.isconnected()
    while rt==True:
        if(printflg==True):
            destsendstr="Device_reading."
            _outputlog(INFO, destsendstr)
        rt = dc.receive(tm)
        if(rt is None):
            #For reset bug?
            #dc.disconnect()
            destsendstr="Device_disconnected %s." %(st.nodename)
            _outputlog(WARN, destsendstr)
            rt=st.send('System _Msg '+destsendstr)
            dc.disconnect()
            st.terminateMainloop()
            break
        elif(rt != ''):
            if(printflg==True):
                destsendstr="Device_read#%s#" %(rt)
                _outputlog(INFO, destsendstr)
                device_replyanalyzer(rt,printflg)
        else:
            break
        tm=0.005
    rt = dc.isconnected()
    if(rt == False):
        destsendstr="Terminate STARS %s. [Device disconnection]" %(st.nodename)
        _outputlog(WARN, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
        st.terminateMainloop()
        return(rt)
    if(printflg==True):
        destsendstr="Device_detected done %s." %(st.nodename)
        _outputlog(INFO, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
    return(rt)

## Device reply handler: DETECT
def device_replyanalyzer(recvdata, printflg=True):
    global gb_ChannelNameList
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    channelnamelist = list(gb_ChannelNameList.keys())
    if(recvdata.startswith('STOP') and len(recvdata)==5):
        id=int(recvdata[4],16)
        starscommand = 'IsBusy'
        rt=stars_getdevicechannelvalue(channelnamelist[id],local=False,starscommand=starscommand)
        if('Er' in rt):
           _outputlog(WARN, "Unexpected reply '%s' in [%s]." %(rt,starscommand))
        else:
            rt2=str(dc._deviceLastChannelStatus[str(id)].position)
            stars_setlocalcurrent([channelnamelist[id]],[rt2], starscommand='GetValue')
            rt2=dc._deviceLastChannelStatus[str(id)].limitstatus
            stars_setlocalcurrent([channelnamelist[id]],[rt2], starscommand='GetLimitStatus')
            stars_setlocalcurrent([channelnamelist[id]],[rt], starscommand=starscommand)
    return(False)


## STARS socket handler
def handler(allmess,sock):
    global gb_ScriptName
    global gb_StarsInstance
    global gb_ChannelNameList
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    st = gb_StarsInstance

    if allmess == '':
        st.terminateMainloop()
        return
    elif(allmess.parameters == ''):
        message = allmess.command
    else:
        message = allmess.command + ' ' + allmess.parameters
    command   = allmess.command
    parameter = allmess.parameters
    parameters = []
    if(allmess.parameters != ''):
        parameters = allmess.parameters.split(" ")
    _outputlog(INFO, '[STARS Recv]' + allmess)

    destsendstr='';
    rt = ''
    if(allmess.nodeto.startswith(st.nodename + '.')==True):
         channelname = allmess.nodeto.replace(st.nodename + '.', '', 1)
         if((channelname != '') and (channelname in gb_ChannelNameList)):
            address = gb_ChannelNameList[channelname]
            rt = sub_channelhandler(command, parameters, channelname, address)
            if(rt != ''):
                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' '+rt
         else:
            if(message.startswith('@')==True):
                return
            elif(message.startswith('_')==True):
                return
            else:
                rt = "Er: Bad node. '%s'" %(channelname)
                destsendstr = st.nodename + '>' + allmess.nodefrom + ' @' + message + ' '+rt
    elif(allmess.nodeto == st.nodename):
        dobjmt = stars_devicecommandobject('CH',   command)
        dobjgb = stars_devicecommandobject('CTL',  command)
        rt2 = sub_commonhandler(command, parameter)
        if(message.startswith('@')==True):
            return
        elif(message.startswith('_')==True):
            return
        elif(rt2 != ''):
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt2
        elif(command == 'GetCtlIsBusy'):
            rt='0'
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
        elif(command == 'GetAllReplyEnable'):
            rt=stars_allreplyenable(command, parameters)
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
        elif(command == 'SetAllReplyEnable'):
            rt=stars_allreplyenable(command, parameters)
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
        elif(command == 'SendRawCommand'):
            if(st._devicerawenable):
                cmd=allmess.parameters.strip()
                rt = stars_sendrawcommand(cmd,allmess.nodefrom)
            else:
                rt = 'Er: Start this program with --rawenable option.'
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt
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
        elif(message in ['GetMotorList','listnodes']):
            rt=' '.join(gb_ChannelNameList.keys())
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message in ['GetChannelList']):
            rt=','.join(gb_ChannelNameList.keys())
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif((command == 'GetMotorNumber') and (len(parameters) == 1)):
            rt = 'Er: Bad parameters.'
            rts=list(gb_ChannelNameList.keys())
            if(parameter[0] in rts):
                rt = str(rts.index(parameter[0]))
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif((command == 'GetMotorName') and (len(parameters) == 1)):
            rt = 'Er: Bad parameters.'
            rt2 = dc._sub_checkisinteger('',parameters)
            if(rt2 != ''):
                id=int(parameters[0])
                rts=list(gb_ChannelNameList.keys())
                if(id>=0 and id<len(rts)):
                    rt=rts[id]
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message == 'GetAccRateList'):
            rts=dc.device_getacccodelist()
            rts2 = [str(n) for n in rts]
            rt=' '.join(rts2)
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message == 'flushdata'):
            stars_flushdata()
            rt = 'Ok:'
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message == 'flushdatatome'):
            stars_flushdata('',allmess.nodefrom)
            rt = 'Ok:'
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #elif(message == 'GetChannelTargetNoList'):
        #    rt=','.join(gb_ChannelNameList.values())
        #    destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + rt
        elif(command in ['Remote','Local','SetFunction']):
            rt=dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,command,parameters,[])
            if('Er' not in  rt):
                starscommand = 'GetFunction'
                rt2=stars_getdevicecontrollervalue(local=False, starscommand=starscommand)
                if('Er' not in  rt):
                    st._deviceisremote = rt2
                    stars_sendevent(childnode='', eventmessage='_ChangedFunction '+st._deviceisremote, to='System')
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif((command == 'Select') and (len(parameters)==2)):
            rt = 'Er: Bad parameters.'
            posch = parameters[0].upper()
            if(posch in ['A','B','C','D']):
                idx = ord(posch)-65
                rt2 = dc._sub_checkisinteger('',[parameters[1]])
                if(rt2 != ''):
                    id=int(parameters[1])
                    rts=list(gb_ChannelNameList.keys())
                    if(id>=0 and id<len(rts)):
                        ch=hex(int(id))[2:]
                        chlist = ['-','-','-','-']
                        chlist[idx] = ch
                        rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,command,["".join(chlist)],[])
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif((command == 'Select') and (len(parameters)==1) and (len(parameter)==4)):
            rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,command,[parameters],[])
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(command in ['GetValue','GetLimitStatus','IsBusy']):
            rt = 'Er: Bad parameters.'
            values=[]
            islocal=False
            if((len(parameters)==0)):
            #if(gb_StarsIsUseGetMultiValues and (len(parameters)==0)):
                rt=stars_getdevicechannelvalue('',local=islocal,starscommand=command)
                if('Er:' not in rt):
                    values=rt.split(',')
            elif(gb_StarsIsUseGetMultiValues and (len(parameters)==len(gb_ChannelNameList.keys()))):
                rt='Ok:'
                for val in parameters:
                    if(val not in ['0','1','-']):
                        rt = 'Er: Bad parameters.'
                        break
                if('Er:' not in rt):
                    rt=stars_getdevicechannelvalue('',local=islocal,starscommand=command)
                if('Er:' not in rt):
                    values=rt.split(',')
                    rets=[]
                    for i in range(len(parameters)):
                        if(parameters[i] == '1'):
                            rets.append(values[i])
                        else:
                            rets.append('-')
                    rt=','.join(rets)
            elif(len(parameters)==1):
                parameters2 = parameters[0].split(',')
                if(gb_StarsIsUseGetMultiValues or (len(parameters2)==1)):
                    rt='Ok:'
                    for i in range(len(parameters2)):
                        val=parameters2[i]
                        if((max([ord(c) for c in val]) < 128) and (val.isdigit()==True)):
                            if(val in gb_ChannelNameList.values()):
                                parameters2[i]=int(val)
                            else:
                                rt = 'Er: Bad parameters.'
                                break
                        elif(val in gb_ChannelNameList.keys()):
                            parameters2[i] = int(gb_ChannelNameList[val])
                        else:
                            rt = 'Er: Bad parameters.'
                            break
                else:
                    rt = "Er: Bad parameters."
                if('Er:' not in rt):
                    rt=stars_getdevicechannelvalue('',local=False,starscommand=command)
                if('Er:' not in rt):
                    values=rt.split(',')
                    rets=[]
                    for i in range(len(parameters2)):
                        rets.append(values[parameters2[i]])
                    rt=','.join(rets)
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #### motor command:
        elif((dobjmt is not None) and (message not in ['Stop','StopEmergency'])):
            rt = 'Er: Bad parameters.'
            addrlist=[]
            argnum  =dobjmt.argnum
            isallowbusy =dobjmt.isallowbusy
            ischeckcargnum=dobjmt.ischeckargnum
            ismotion=dobjmt.ismotioncommand
            isreferencecommand=dobjmt.isreferencecommand
            ischeckcargnum=dobjmt.ischeckargnum
            isallowlocal =dobjmt.isallowlocal
            islocal=False
            parameters2 = parameters
            if(len(parameters)==1):
                parameters2=parameters[0].split(",")
            # Reference all
            if(gb_StarsIsUseGetMultiValues and (argnum==0) and len(parameters)==0):
                rt = 'Ok:'
                if((isallowlocal==False) and (st._deviceisremote == '0')):
                    rt = 'Er: Local.'
                else:
                    for channelname in gb_ChannelNameList.keys():
                        if(isallowbusy==False):
                            b=stars_getflgbusy(channelname,local=True)
                            if(b=="1"):
                                rt = 'Er: Busy.'
                                break
                        addrlist.append(gb_ChannelNameList[channelname])
                if('Er:' not in rt):
                    rt=stars_getdevicechannelvalue(channelname='',local=islocal,starscommand=command)
                    if(('Er:' not in rt)):
                        if(ismotion == True):
                            for channelname in gb_ChannelNameList.keys():
                                stars_setlocalflgbusy(channelname,"1")
                        rts=rt.split(' ')
                        if(isreferencecommand==True):
                            rt=','.join(rts)
                        else:
                            rt=rts[0]
            # Reference filter
            elif(gb_StarsIsUseGetMultiValues and (argnum in [0,1]) and (len(parameters2)==len(gb_ChannelNameList.keys()))):
                checklist=[True,False]
                replylist = []
                rt = 'Ok:'
                for ischeckonly in checklist:
                    if('Er:' in rt):
                        break
                    for channelname in gb_ChannelNameList.keys():
                        id=gb_ChannelNameList[channelname]
                        i=int(id)
                        parameters3=''
                        rt2='-'
                        if(argnum==0):
                            if(parameters2[i]=='-'):
                                id = -1
                            elif(parameters2[i]=='0'):
                                id = -1
                            elif(parameters2[i]=='1'):
                                pass
                            else:
                                rt = 'Er: Bad parameters.'
                                break
                        elif(argnum==1):
                            if(parameters2[i]=='-'):
                                id = -1
                            parameters3=parameters2[i]
                        if((isallowlocal==False) and (st._deviceisremote == '0')):
                            rt = 'Er: Local.'
                            break
                        if(id != -1):
                            if(isallowbusy==False):
                                b=stars_getflgbusy(channelname,local=True)
                                if(b=="1"):
                                    rt = 'Er: Busy.'
                                    break
                            if(ischeckonly == True):
                                continue
                            rt2=stars_getdevicechannelvalue(channelname=channelname,local=islocal,starscommand=command,parameters=parameters3)
                            if('Er:' in rt2):
                                rt=rt2
                                break
                        if(ischeckonly == True):
                            continue
                        if(isreferencecommand==True):
                            replylist.append(rt2) 
                            rt = ' '.join(replylist)
                        if(id != -1):
                           if(ismotion == True):
                                stars_setlocalflgbusy(channelname,"1")
            # Reference by channelnames: check 1st parameter is channelname or no.
            elif(len(parameters)>=1):
                channelnamelist=parameters[0].split(",")
                parameters2 = parameters
                parameters2.pop(0)
                if(len(channelnamelist)==1):
                    channelname=channelnamelist[0]
                    address = -1
                    if(channelname in gb_ChannelNameList.keys()):
                        address = gb_ChannelNameList[channelname]
                        rt = sub_channelhandler(command, parameters2, channelname, address)
                    elif(channelname in gb_ChannelNameList.values()):
                        address = channelname
                        keylist = [k for k, v in gb_ChannelNameList.items() if v == address]
                        channelname = keylist[0]
                        rt = sub_channelhandler(command, parameters2, channelname, address)
                    else:
                        rt = 'Er: Bad parameters.'
                    if(rt != ''):
                        destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
                elif(gb_StarsIsUseGetMultiValues and (argnum in [0,1]) and (len(parameters2)==argnum)):
                    addrlist=[]
                    valuelist=[]
                    rt = 'Ok:'
                    if(argnum == 1):
                        valuelist=parameters2[0].split(",")
                        if(len(valuelist) != len(channelnamelist)):
                            rt = 'Er: Bad parameters.'
                    if('Er:' not in rt):
                        for i in range(len(channelnamelist)):
                            channelname=''
                            val = channelnamelist[i]
                            if(val in gb_ChannelNameList.keys()):
                                channelname = val
                            elif(val in gb_ChannelNameList.values()):
                                address = val
                                keylist = [k for k, v in gb_ChannelNameList.items() if v == address]
                                channelname = keylist[0]
                            else:
                                rt = 'Er: Bad parameters.'
                                break
                            channelnamelist[i]=channelname
                    if(len(channelnamelist) != len(list(set(channelnamelist)))):
                        rt = 'Er: Duplicate channels assigned.'
                    if('Er:' not in rt):
                        checklist=[True,False]
                        replylist = []
                        for ischeckonly in checklist:
                            if('Er:' in rt):
                                break
                            for i in range(len(channelnamelist)):
                                rt = 'Ok:'
                                channelname=channelnamelist[i]
                                id=gb_ChannelNameList[channelname]
                                valuelist2=[]
                                if(argnum == 1):
                                    valuelist2.append(valuelist[i])
                                if((isallowlocal==False) and (st._deviceisremote == '0')):
                                    rt = 'Er: Local.'
                                    break
                                if(isallowbusy==False):
                                    b=stars_getflgbusy(channelname,local=True)
                                    if(b=="1"):
                                        rt = 'Er: Busy.'
                                        break
                                rt2=dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,command,valuelist2,[id],checkOnly=ischeckonly)
                                if('Er:' in rt2):
                                    rt=rt2
                                    break
                                if(ischeckonly == True):
                                    continue
                                if(isreferencecommand==True):
                                    replylist.append(rt2) 
                                    rt = ','.join(replylist)
                                if(ismotion == True):
                                    stars_setlocalflgbusy(channelname,"1")
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
        #### 
        #### global command:
        elif(dobjgb is not None):
            rt = 'Er: Bad parameters.'
            argnum      =dobjgb.argnum
            isallowbusy =dobjgb.isallowbusy
            ischeckcargnum=dobjgb.ischeckargnum
            ismotion=dobjgb.ismotioncommand
            isallowlocal =dobjgb.isallowlocal
            if(len(parameters)==argnum):
                rt = 'Ok:'
                if((isallowlocal==False) and (st._deviceisremote == '0')):
                    rt = 'Er: Local.'
                elif(isallowbusy==False):
                    for channelname in gb_ChannelNameList.keys():
                        b=stars_getflgbusy(channelname,local=True)
                        if(b=="1"):
                            rt = 'Er: Busy.'
                            break
                if('Er:' not in rt):
                    rt=dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,command,parameters,[])
                if('Er:' not in rt):
                    if(ismotion==True):
                        for channelname in gb_ChannelNameList.keys():
                            stars_setlocalflgbusy(channelname,"1")
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        else:
            rt = 'Er: Bad command or parameters.'
            if(len(parameters)>=1):
                channelnamelist=parameters[0].split(",")
                parameters2 = parameters
                parameters2.pop(0)
                if(len(channelnamelist)==1):
                    channelname=channelnamelist[0]
                    address = -1
                    if(channelname in gb_ChannelNameList.keys()):
                        address = gb_ChannelNameList[channelname]
                        rt2 = sub_channelhandler(command, parameters2, channelname, address)
                    elif(channelname in gb_ChannelNameList.values()):
                        address = channelname
                        keylist = [k for k, v in gb_ChannelNameList.items() if v == address]
                        channelname = keylist[0]
                        rt2 = sub_channelhandler(command, parameters2, channelname, address)
                    if(rt2 != ''):
                        rt = rt2
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
    else:
        if(message.startswith('@')==True):
            return
        elif(message.startswith('_')==True):
            return
        else:
            rt = "Er: Bad node. '%s'" %(channelname)
            destsendstr = st.nodename + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
    if((st._pm16c04Compatible) and (command == 'GetHomePosition')):
        if('Er:' not in destsendstr):
           if(destsendstr.endswith(' -')==True):
               destsendstr = destsendstr.replace(' -',' Er: NO H.P')
    if(destsendstr != ''):
        st._lastsendtime = time.time()
        _outputlog(INFO,'[STARS Send]'+destsendstr)
        rt=st.send(destsendstr)
        if(rt==False):
            st.terminateMainloop()
    return

## STARS socket handler
def sub_channelhandler(command, parameters, channelname, address):
    global gb_StarsInstance
    global gb_DeviceInstance
    st = gb_StarsInstance
    dc = gb_DeviceInstance

    rt = ''
    dobjmt = stars_devicecommandobject('CH', command)
    if(command.startswith('@')==True):
        return(rt)
    elif(command.startswith('_')==True):
        return(rt)
    elif((command == 'hello') and (len(parameters) == 0)):
        rt = 'Nice to meet you.'
    #Not yet certified.
    elif((command == 'help') and (len(parameters) == 0)):
        rt = stars_getdevicecommandhelpstring('CH','')
    #Not yet certified.
    elif((command == 'help') and (len(parameters) == 1)):
        rt = stars_getdevicecommandhelpstring('CH', parameters[0])
    elif((command == 'GetMotorNumber') and (len(parameters) == 0)):
        rt = address
    elif((command in ['Select']) and (len(parameters)==1)):
        rt = 'Er: Bad parameters.'
        posch = parameters[0].upper()
        if(posch in ['A','B','C','D']):
            ch=hex(int(address))[2:].upper()
            idx = ord(posch)-65
            chlist = ['-','-','-','-']
            chlist[idx] = ch
            rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,command,["".join(chlist)],[])
    elif((command == 'GetSelected') and (len(parameters)==0)):
        rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,'GetTimingOutChannel',[],[])
        if('Er:' not in rt):
            ch=hex(int(address))[2:].upper()
            pos=rt.find(ch)
            if(pos<0):
                rt = 'N'
            else:
                rt = chr(pos+65)
    elif(command == 'GetAccRateList'):
        rts=dc.device_getacccodelist()
        rts2 = [str(n) for n in rts]
        rt=' '.join(rts2)
    elif(dobjmt is None):
        rt = 'Er: Bad command or parameters.'
    ### Valid command
    else:
        argnum = dobjmt.argnum
        ischeckcargnum=dobjmt.ischeckargnum
        #*** Check parameter num
        if((ischeckcargnum==True) and len(parameters) != argnum):
            rt = 'Er: Bad parameters.'
            return(rt)
        isallowbusy = dobjmt.isallowbusy
        ismotion = dobjmt.ismotioncommand
        isallowlocal = dobjmt.isallowlocal
        #*** Pre check if busy
        if((isallowlocal==False) and (st._deviceisremote == '0')):
            rt = 'Er: Local.'
        elif(isallowbusy == False):
            b = stars_getflgbusy(channelname,local=True)
            if(b == "1"):
                rt = 'Er: Busy.'
                return(rt)
        if('Er:' not in rt):
            if(command in ['GetValue','GetLimitStatus','IsBusy']):
                rt=stars_getdevicechannelvalue(channelname,local=False,starscommand=command)
            else:
                rt=dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,command,parameters,[address])
        if('Er:' in rt): return(rt)
        if(command in ['GetValue','GetLimitStatus','IsBusy']):
            rt2=stars_getdevicechannelvalue(channelname,local=True,starscommand=command)
            if(rt2 != rt):
                if(command == 'GetValue'):
                    b = stars_getdevicechannelvalue(channelname,local=True,starscommand='IsBusy')
                    if(b == '0'):
                        stars_setlocalcurrent([channelname],['1'],'IsBusy',True)
                stars_setlocalcurrent([channelname],[rt],command,False)
        elif(command == 'Preset'):
            rt2=stars_getdevicechannelvalue(channelname,local=False,starscommand='GetValue')
            if('Er:' not in rt2):
                stars_setlocalcurrent([channelname],['1'],'IsBusy',True)
                stars_setlocalcurrent([channelname],[rt2],'GetValue',True)
                stars_setlocalcurrent([channelname],['0'],'IsBusy',True)
        #*** Post send busy if motion
        if(ismotion == True):
          stars_setlocalflgbusy(channelname,"1")
    return(rt)

def sub_commonhandler(command, parameter):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_LogDir
    global gb_LogEnable
    global gb_Debug
    global gb_LogLevel
    global gb_DebugLevel

    st = gb_StarsInstance
    dc = gb_DeviceInstance
    rt = ''
    if(command == 'SetLogEnable'):
        (rt2, rt)= dc._sub_checksetonoff('',[parameter])
        if(rt2 == '0'):
            rt = setup_logger(st.nodename, p_fflg=False)
        elif(rt2 == '1'):
            rt = setup_logger(st.nodename, p_fflg=True)
    elif(command == 'SetLogLevel'):
        (rt2, rt)= dc._sub_checkisinteger('',[parameter])
        if(rt2 != ''):
            if(int(rt2)<0):
                rt = 'Er: Bad parameters.'
            else:
                setup_logger(st.nodename, p_flevel=int(rt2))
                rt = 'Ok:'
    elif(command == 'SetLogDir' and parameter != ''):
        rt = setup_logger(st.nodename, p_logdir=parameter)
    elif(command == 'SetDebugEnable'):
        (rt2, rt)= dc._sub_checksetonoff('',[parameter])
        if(rt2 == '0'):
            rt = 'Ok:'
            setup_logger(st.nodename, p_sflg=False)
            setDebug(gb_Debug)
        elif(rt2 == '1'):
            setup_logger(st.nodename, p_sflg=True)
            setDebug(gb_Debug)
            rt = 'Ok:'
    elif(command == 'SetDebugLevel'):
        (rt2, rt)= dc._sub_checkisinteger('',[parameter])
        if(rt2 != ''):
            if(int(rt2)<0):
                rt = 'Er: Bad parameters.'
            else:
                setup_logger(st.nodename, p_slevel=int(rt2))
                setDebug(gb_Debug)
                rt = 'Ok:'
    elif(command == 'IsLogEnabled'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = '0'
            if(gb_LogEnable):
                rt = '1'
    elif(command == 'GetLogDir'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = gb_LogDir
    elif(command == 'IsDebugEnabled'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = '0'
            if(gb_Debug):
                rt = '1'
    elif(command == 'GetLogLevel'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = str(gb_LogLevel)
    elif(command == 'GetDebugLevel'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = str(gb_DebugLevel)
    elif(command == 'GetCurrentLogFileName'):
        rt = 'Er: Bad command or parameters.'
        if(parameter == ''):
            rt = gb_LogFileName
    return(rt)

##################################################################
# Define functions for stars 
##################################################################
def stars_sendrawcommand(command, commandsender):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_ChannelNameList
    global gb_SendRawCommandALLREPDS
    global gb_SendRawCommandLNSRQ
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    sender = st.nodename
    cmd=command.strip().upper()
    isrep = dc._deviceFirmwareInfo.is_commandsupported('ALL_REP')
    isskip = False
    if('?' in cmd):
        isrep = True
    elif(re.match('S(14|[246])', cmd)):
        isrep = True
    elif(cmd == 'ALL_REP EN'):
        pass
    elif(st._isallrepenable==False):
        isrep = False
    elif(sender in gb_SendRawCommandALLREPDS):
        isrep = False

    if(cmd == 'ALL_REP DS'):
        st._isallrepenable = False
        #if(dc._deviceFirmwareInfo.is_commandsupported('ALL_REP') == True):
        #    gb_SendRawCommandALLREPDS[sender] = True
        isskip = True

    rt = 'Ok:'
    if(cmd==''):
        return(rt)
    if(isskip == True):
        return(rt)
    rt2 = dc.device_act(cmd)
    if('Er:' in rt2):
        rt = rt2
        return(rt)
    elif(cmd == 'ALL_REP EN'):
        if(rt2 == 'OK'):
            st._isallrepenable=True
            if(dc._deviceFirmwareInfo.is_commandsupported('ALL_REP') == True):
                if(sender in gb_SendRawCommandALLREPDS):
                    del gb_SendRawCommandALLREPDS[sender]
    elif((cmd.startswith('LN_SRQ') and (len(cmd) == 8))):
        vallist=list(gb_ChannelNameList.values())
        if(rt2 == 'OK'):
            if(cmd[6:7] == 'G1'):
                #G1: Tsuji taisyogai
                #gb_SendRawCommandLNSRQ[sender] = {}
                #for id in vallist:
                #    ch=hex(int(id))[2:]
                #    gb_SendRawCommandLNSRQ[sender][ch] = True
                pass
            elif(cmd[6:7] == 'G0'):
                if(sender in gb_SendRawCommandLNSRQ):
                    del gb_SendRawCommandLNSRQ[sender]
            elif(cmd[7]=='1'):
                if(sender not in gb_SendRawCommandLNSRQ):
                    gb_SendRawCommandLNSRQ[sender] = {}
                gb_SendRawCommandLNSRQ[sender][cmd[6]] = True
            elif(cmd[7]=='0'):
                if(sender in gb_SendRawCommandLNSRQ):
                    if(cmd[6] in gb_SendRawCommandLNSRQ[sender]):
                        del gb_SendRawCommandLNSRQ[sender][cmd[6]]
    if(rt2 == ''):
        pass
    else:
        if(isrep):
            rt = rt + ' ' + rt2
    if(cmd == 'REST'):
        st.terminateMainloop()
    return(rt)

def stars_allreplyenable(starscommand, parameters):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_SendRawCommandALLREPDS
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    if(dc._deviceFirmwareInfo.is_commandsupported('ALL_REP') == False):
        return('Er: Bad command or parameters.')
    sender = st.nodename
    if(starscommand == 'SetAllReplyEnable'):
        # Check command parameters
        rts = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER, starscommand, parameters, [], checkOnly=True)
        rt=''.join(rts)
        if('Er:' in rt):
            return(rt)
        cmd = rt
        # Check rem/local
        isremote = st._deviceisremote
        if(isremote != '1'):
           return('Er: local')
        if('DS' in cmd):
            st._isallrepenable = False
            #gb_SendRawCommandALLREPDS[sender] = True
        else:
            st._isallrepenable = True
            if(sender in gb_SendRawCommandALLREPDS):
                del gb_SendRawCommandALLREPDS[sender]
        return('Ok:')
    elif(starscommand == 'GetAllReplyEnable'):
        if(sender in gb_SendRawCommandALLREPDS):
            return('0')
        else:
            return('1')

def stars_devicecommandobject(level,starscommand,isincludeusehelponly=False):
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    if(level=='CTL'):
        level=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER
    elif(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER):
        level=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL
    dobj = dc.devicecommandobject(starscommand,level)
    if(dobj):
        if((isincludeusehelponly==False) and (dobj.ishelponly==True)):
            return(None)
        return(dobj)
    return(None)

def stars_getdevicecommandhelpstring(level,starscommand):
    global gb_DeviceInstance
    dc = gb_DeviceInstance

    #Search help content.
    if(starscommand != ''):
        rt = "Er: Command '%s' not found." %(starscommand)
        dobj = None
        dobjch = None
        if(level == 'ALL'):
            dobj = dc.devicecommandobject(starscommand,PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER)
            if(dobj is None):
                dobjch = dc.devicecommandobject(starscommand,PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL)
                if(dobjch is not None):
                    rt = dobjch.helpstring
                    rt = rt[:-1] + ' of the specified channal.'
                    return(rt)
        elif(level == 'CTL'):
            dobj = dc.devicecommandobject(starscommand,PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER)
        elif(level == 'CH'):
            dobjch = dc.devicecommandobject(starscommand,PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL)
        if(dobj and dobjch):
            rt = "" + dobj.helpstring + '|' + dobjch.helpstring
            return(rt)
        elif(dobj):
            rt = dobj.helpstring
            return(rt)
        elif(dobjch):
            rt = dobjch.helpstring
            return(rt)

    #Make help list.
    clist = []
    if(level == 'ALL'):
        clist.extend(list(dc._deviceSTARSCommandCtrl.keys()))
        clist.extend(list(dc._deviceSTARSCommandChannel.keys()))
        clist = sorted(list(set(clist)))
        clist.remove('GetChannelStatus')
    elif(level == 'CTL'):
        clist.extend(list(dc._deviceSTARSCommandCtrl.keys()))
        clist = sorted(list(set(clist)))
        clist.remove('GetChannelStatus')
    elif(level == 'CH'):
        clist.extend(list(dc._deviceSTARSCommandChannel.keys()))
        clist = sorted(list(set(clist)))
        clist.remove('GetChannelStatus')

    l_start = clist
    if(starscommand == ''):
        #Return help list.
        #l_start = [s for s in clist if not s.startswith('_')]
        rt = ' '.join(l_start)
    elif(starscommand.startswith('-')):
        l_start = [s for s in clist if not s.startswith(starscommand[1:])]
        if(len(l_start)>0):
            rt = ' '.join(l_start)
    else:
        l_start = [s for s in clist if s.startswith(starscommand)]
        if(len(l_start)>0):
            rt = ' '.join(l_start)
    return(rt)

def stars_sendevent(childnode='_Alert', eventmessage='_Msg', to='System'):
    global gb_StarsInstance
    st = gb_StarsInstance
    destsendstr=''
    if(childnode == ''):
        destsendstr=st.nodename + '>' + to + ' ' + eventmessage
    else:
        destsendstr=st.nodename + '.' + childnode + '>' + to + ' ' + eventmessage
    if(destsendstr != ''):
        _outputlog(INFO,'[STARS Send]'+destsendstr)
        rt=st.send(destsendstr)
        return(rt)
    return(True)

def stars_flushdata(channelname='', to='System'):
    global gb_LimitEventEnableChannelList
    global gb_StarsInstance
    st = gb_StarsInstance
    global gb_ChannelNameList
    channelnamelist = gb_ChannelNameList.keys()
    if(channelname == ''):
        stars_sendevent(childnode=channelname, eventmessage='_ChangedFunction ' +st._deviceisremote, to=to)
        if(st._pm16c04Compatible):
            stars_sendevent(childnode=channelname, eventmessage='_ChangedCtlIsBusy 0', to=to)
    elif(channelname in gb_ChannelNameList.keys()):
        channelnamelist = [channelname]
    for channelname in channelnamelist:
        id = int(gb_ChannelNameList[channelname])
        b=stars_getdevicechannelvalue(channelname,local=True,starscommand='IsBusy')
        v=stars_getdevicechannelvalue(channelname,local=True,starscommand='GetValue')
        stars_sendevent(childnode=channelname, eventmessage='_ChangedIsBusy '+b, to=to)
        stars_sendevent(childnode=channelname, eventmessage='_ChangedValue '+v, to=to)
        if(gb_LimitEventEnableChannelList[id]==True):
            l=stars_getdevicechannelvalue(channelname,local=True,starscommand='GetLimitStatus')
            stars_sendevent(childnode=channelname, eventmessage='_ChangedLimitStatus '+l, to=to)


## STARS set busyflg
def stars_setlocalflgbusy(channelname, f, force=False):
    stars_setlocalcurrent([channelname],[f],'IsBusy',force)
    return rt

def stars_setlocalcurrent(channellist, valuelist, starscommand='GetValue',force=False):
    global gb_ChannelNameList
    global gb_StarsLocalCurrent
    global gb_StarsLocalStatus
    global gb_StarsLocalBusyFlg
    global gb_LimitEventEnableChannelList
    global gb_StarsInstance
    st = gb_StarsInstance

    sendedrt = False
    if(len(channellist) != len(valuelist)):
        return(sendedrt)
    if(starscommand not in ['GetValue','GetLimitStatus','IsBusy']):
        return sendedrt
    for i in range(len(channellist)):
        if(valuelist[i] is None):
            continue
        current=valuelist[i]
        channelname=channellist[i]
        id = int(gb_ChannelNameList[channelname])
        prev=stars_getdevicechannelvalue(channelname,local=True,starscommand=starscommand)
        eventmessage=''
        issendskip = False
        if(starscommand == 'GetValue'):
            gb_StarsLocalCurrent[id] = current
            eventmessage='_ChangedValue'
        elif(starscommand == 'GetLimitStatus'):
            gb_StarsLocalStatus[id] = current
            if(gb_LimitEventEnableChannelList[id]==False):
                issendskip = True
            eventmessage='_ChangeLimitStatus'
        elif(starscommand == 'IsBusy'):
            gb_StarsLocalBusyFlg[id] = current
            eventmessage='_ChangedIsBusy'
        current=stars_getdevicechannelvalue(channelname,local=True,starscommand=starscommand)
        if(issendskip==False):
            if((force) or (prev is None) or ((prev is not None) and (prev != current))):
                stars_sendevent(childnode=channelname,eventmessage=eventmessage+' '+current)
                sendedrt = True
    return sendedrt

def stars_getflgbusy(channelname='',local=True):
    rt = stars_getdevicechannelvalue(channelname, local, starscommand='IsBusy')
    return(rt)

def stars_getdevicechannelvalue(channelname='',local=False, starscommand='GetValue',parameters=''):
    global gb_ChannelNameList
    global gb_DeviceInstance
    global gb_StarsLocalCurrent
    global gb_StarsLocalStatus
    global gb_StarsLocalBusyFlg
    dc = gb_DeviceInstance

    channellist=channelname.split(',')
    values=parameters.split(',')
    addrlist=[]
    dobj = stars_devicecommandobject('CTL',starscommand)
    rt = "Er: Unexpected channelname parameter '%s' in stars_getdevicechannelvalue" % channelname
    if(local==False):
        if((dobj is not None) and (channelname == '') and (parameters == '')):
            rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,starscommand,[],[])
        else:
            if(channelname == ''):
                addrlist = [int(id) for id in gb_ChannelNameList.values()]
            else:
                iskey=False
                isval=False
                for i in range(len(channellist)):
                    channelname=channellist[i]
                    if(channelname in gb_ChannelNameList.keys()):
                        if(isval):
                            break
                        else:
                            id=int(gb_ChannelNameList[channelname])
                        iskey=True
                    elif(channelname in gb_ChannelNameList.values()):
                        if(iskey):
                            break
                        else:
                            id=int(channelname)
                        isval=True
                    addrlist.append(id)
                if(len(addrlist)!=len(channellist)):
                    addrlist=[]
            if(len(addrlist)>0):
                if(parameters==''):
                    rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,starscommand,[],addrlist)
                elif(len(values)==len(addrlist)):
                    rts=[]
                    for i in range(len(addrlist)):
                        rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CHANNEL,starscommand,[values[i]],[addrlist[i]])
                        if('Er:' in rt):
                             break
                        rts.append(rt)
                        rt=','.join(rts)

    elif(channelname in gb_ChannelNameList.keys()):
        i=int(gb_ChannelNameList[channelname])
        if(starscommand == 'GetValue'):
            return(gb_StarsLocalCurrent[i]);
        elif(starscommand == 'GetLimitStatus'):
            return(gb_StarsLocalStatus[i]);
        elif(starscommand == 'IsBusy'):
            return(gb_StarsLocalBusyFlg[i]);
        rt = "Er: Unexpected starscommand parameter '%s' in stars_getdevicechannelvalue" % starscommand
    elif(channelname == ''):
        if(starscommand == 'GetValue'):
            return(','.join(gb_StarsLocalCurrent))
        elif(starscommand == 'GetLimitStatus'):
            return(','.join(gb_StarsLocalStatus))
        elif(starscommand == 'IsBusy'):
            return(','.join(gb_StarsLocalBusyFlg))
        rt = "Er: Unexpected starscommand parameter '%s' in stars_getdevicechannelvalue" % starscommand
        return(rt)
    return(rt)

def stars_getdevicecontrollervalue(local=False, starscommand='GetFunction'):
    global gb_DeviceInstance
    dc = gb_DeviceInstance

    rt = "Er: Unexpected starscommand parameter '%s' in stars_getdevicecontrollervalue" % starscommand
    if(local==False):
        rt = dc.exec_command(PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel.CONTROLLER,starscommand,[],[])
    else:
        pass
    return(rt)

##################################################################
# Define global parameters
##################################################################
# Global parameters.
gb_StarsInstance = None
gb_DeviceInstance = None
gb_ChannelNameList = OrderedDict()
gb_LimitEventEnableChannelList = []
gb_StarsLocalBusyFlg   = []
gb_StarsLocalStatus    = []
gb_StarsLocalCurrent   = [] 
gb_StarsIsUseGetMultiValues = True
gb_SendRawCommandALLREPDS = {}
gb_SendRawCommandLNSRQ = {}

##################################################################
# Define internal parameters
##################################################################
# Internal parameters.
gb_ScriptName = path.splitext(path.basename(__file__))[0]
gb_ScriptPath = path.dirname(path.abspath(sys.argv[0]))
gb_Debug = False
gb_LogEnable = False
gb_LogDir = ''
gb_LogFileName = ''
gb_DebugLevel  = INFO
gb_LogLevel    = INFO
logger = None

##################################################################
# Set logging options
##################################################################
def setDebug(b):
    global gb_Debug
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_DebugLevel
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    gb_Debug = b
    if(gb_DebugLevel>5): b = False
    if(dc is not None):  dc.setdebug(b)
    if(st is not None):  st.setdebug(b)
    return(b)

def setup_logger(p_logprefix, p_logdir=None, p_fflg=None, p_sflg=None, p_flevel=None, p_slevel=None, p_recover=True):
    global logger
    global gb_LogFileName
    global gb_LogEnable
    global gb_LogDir
    global gb_LogLevel
    global gb_Debug
    global gb_DebugLevel
    global gb_ScriptName
    global gb_ScriptPath
    head = gb_ScriptName
    ischange=False
    if(p_logdir is None): p_logdir = gb_LogDir
    if(p_fflg is None):   p_fflg = gb_LogEnable
    if(p_sflg is None):   p_sflg = gb_Debug
    if(p_flevel is None):
        p_flevel = gb_LogLevel
    elif(p_flevel > FATAL):
        p_flevel = FATAL
    elif(p_flevel < NOTSET):
        p_flevel = NOTSET
    if(p_slevel is None):
        p_slevel = gb_DebugLevel
    elif(p_slevel > FATAL):
        p_slevel = FATAL
    elif(p_slevel < NOTSET):
        p_slevel = NOTSET

    if(p_logdir[-1] not in ['/',sep]):
        p_logdir = p_logdir + sep
    logfilename = p_logdir + p_logprefix + 'log' + time.strftime('%Y-%m-%d',time.localtime()) + '.txt'
    logfilename = path.abspath(logfilename)
    if(path.exists(p_logdir)==True or path.isdir(p_logdir)==True or access(p_logdir, W_OK) == True):
       if(path.exists(logfilename)==True):
            if(path.isfile(logfilename)==False):
                errormsg = "Er: Log filename '"+logfilename+"' is not a file."
                return(errormsg)
    else:
        p_logdir=path.dirname(logfilename)
        errormsg = "Er: Log Directory '"+p_logdir+"' not found."
        return(errormsg)


    rt = 'Ok:'
    if(logfilename != gb_LogFileName):
        ischange = True
    if(gb_LogEnable != p_fflg):
        ischange = True
    if(gb_Debug != p_sflg):
        ischange = True
    if(gb_LogLevel != p_flevel):
        ischange = True
    if(gb_DebugLevel != p_slevel):
        ischange = True
    if(p_recover ==False):
        pass
    elif(ischange==False):
        return(rt)
    try:
        if(logger is None):
            logger = getLogger(__name__)
        for hdlr in logger.handlers[:]:
            logger.removeHandler(hdlr)
        fmt = '[%(asctime)s][%(threadName)s] %(message)s'
        if((p_fflg == True) and (p_sflg == True)):
            if(p_flevel==0):
                logger.setLevel(p_slevel)
            elif(p_slevel==0):
                logger.setLevel(p_flevel)
            elif(p_flevel<=p_slevel):
                logger.setLevel(p_flevel)
            else:
                logger.setLevel(p_slevel)
            fstream = FileHandler( logfilename )
            fstream.setLevel(p_flevel)
            formatter = Formatter(fmt)
            fstream.setFormatter(formatter)
            logger.addHandler(fstream)
            console = StreamHandler()
            console.setLevel(p_slevel)
            formatter = Formatter(fmt)
            console.setFormatter(formatter)
            logger.addHandler(console)

        elif(p_fflg == True):
            logger.setLevel(p_flevel)
            fstream = FileHandler( logfilename )
            fstream.setLevel(p_flevel)
            formatter = Formatter(fmt)
            fstream.setFormatter(formatter)
            logger.addHandler(fstream)

        elif(p_sflg == True):
            logger.setLevel(p_slevel)
            console = StreamHandler()
            console.setLevel(p_slevel)
            formatter = Formatter(fmt)
            console.setFormatter(formatter)
            logger.addHandler(console)
        else:
            logger.addHandler(NullHandler())
        gb_LogFileName = logfilename
        gb_LogEnable = p_fflg
        gb_Debug = p_sflg
        gb_LogLevel = p_flevel
        gb_DebugLevel = p_slevel
        gb_LogDir=path.dirname(gb_LogFileName)
        disable(NOTSET)
    except PermissionError:
        errormsg="Er: Permission denied at log directory '%s'." %(p_logdir)
        if(p_recover==True):
            if(ischange == True):
                rt = setup_logger(p_logprefix, p_recover=False)
                if(rt != 'Ok:'):
                    rt = setup_logger(p_logprefix, p_fflg=False, p_recover=False)
        return(errormsg)
    except Exception as e:
        errormsg="Er: logger error raised.[%s]" %sys.exc_info()[0]
        logger.exception('Er: logger error detected.')
        if(p_recover==True):
            if(ischange == True):
                rt = setup_logger(p_logprefix, p_recover=False)
        return(errormsg)
    return(rt)

##################################################################
# program functions: print,config
##################################################################
# Define: print function
def _outputlog(level, mesg, outstderronly=False):
    global logger
    if(outstderronly == True):
        if(mesg[-1:] != '\n'):
           mesg=mesg+'\n'
        stderr.write(mesg)
    else:
        try:
            if(logger is not None):
                if(len(logger.handlers)>0):
                    logger.log(level, mesg)
        except Exception as e:
            pass
    return(1)

def devcmdhandler(mesg):
    global gb_StarsInstance
    st = gb_StarsInstance
    if(mesg is not None):
        if(st is not None):
            setup_logger(st.nodename)
        _outputlog(DEBUG, mesg)
#----------------------------------------------------------------
# Program pyexrc.py
#----------------------------------------------------------------
if __name__ == "__main__":
    ##################################################################
    # Import modules
    ##################################################################
    
    from pystarslib import pystarsutilconfig, pystarsutilargparser

    # Define: Appliction default parameters
    starsNodeName   = 'pm16c16'
    starsServerHost = 'localhost'
    starsServerPort = 6057
    deviceHost = '192.168.1.55'
    devicePort = 7777

    ##################################################################
    # Define program arguments
    ##################################################################
    optIO=pystarsutilargparser.PyStarsUtilArgParser(numberOfDeviceServer=1,useRawEnable=True,useLogOutput=True,useLogOutputLevel=True,useDebugLevel=True)
    parser=optIO.generate_baseparser(prog=gb_ScriptName,version=__version__)
    parser.add_argument('--channelnamelist',       dest="ChannelNameList",        help='Mame list of the motor channels.')
    parser.add_argument('--limitstatuschannellist',dest="LimitStatusChannelList", help='Channel list of enabling the STARS event _ChangedLimitStatus.')
    parser.add_argument('--pm16c04compatible',action='store_true', default=False, help=pystarsutilargparser.SUPPRESS)
    parser.add_argument('--allreplyenable',action='store_true', default=False, help=pystarsutilargparser.SUPPRESS)

    ##################################################################
    # Parse program arguments and config settings
    ##################################################################
    args=parser.parse_args()
    gb_Debug=args.debug
    if(gb_Debug==True):
        gb_DebugLevel  = DEBUG
        gb_LogLevel    = DEBUG
        sys.stdout.write(str(args)+'\n')
    # Get starsNodeName
    starsNodeName = optIO.get(args.StarsNodeName,starsNodeName)
    gb_LogDir= gb_ScriptPath

    #local parameters
    lc_DeviceCommandEnable = False
    lc_ChannelNameList = None
    lc_LimitStatusEventEnable = False
    lc_LimitStatusEventEnableChannelList = None
    lc_pm16c04Compatible = False
    lc_LogDir = gb_LogDir
    lc_AllReplyEnable = False

    # Read configfile if detected
    configfilename = None
    if(path.isfile('./config.cfg')):
        configfilename = './config.cfg'
    configFileName = optIO.get(args.Config,configfilename)

    if(configFileName is not None):
        cfgIO= pystarsutilconfig.PyStarsUtilConfig(configFileName,gb_Debug)
        if(cfgIO.gethandle() is None):
            sys.stdout.write(cfgIO.getlasterrortext()+'\n')
            exit(1)
        if(not optIO.has_value(args.StarsNodeName)):
            starsNodeName = cfgIO.get('', 'StarsNodeName', starsNodeName)
        if(gb_Debug == False):
            gb_Debug = cfgIO.get(starsNodeName, 'Debug', gb_Debug, bool)
        starsServerHost = cfgIO.get(starsNodeName, 'StarsServerHost', starsServerHost)
        starsServerPort = cfgIO.get(starsNodeName, 'StarsServerPort', starsServerPort, int)
        deviceHost      = cfgIO.get(starsNodeName, 'DeviceHost'     , deviceHost)
        devicePort      = cfgIO.get(starsNodeName, 'DevicePort'     , devicePort, int)
        # Program parameters
        lc_DeviceCommandEnable = cfgIO.get(starsNodeName, 'RawEnable', lc_DeviceCommandEnable, bool)
        lc_ChannelNameList = cfgIO.get(starsNodeName, 'ChannelNameList', lc_ChannelNameList)
        lc_LimitStatusEventEnableChannelList = cfgIO.get(starsNodeName, 'LimitStatusChannelList', lc_LimitStatusEventEnableChannelList)
        lc_pm16c04Compatible = cfgIO.get(starsNodeName, 'PM16C04Compatible', lc_pm16c04Compatible, bool)
        lc_AllReplyEnable = cfgIO.get(starsNodeName, 'AllReplyEnable', lc_AllReplyEnable, bool)
        if(gb_Debug==True):
            gb_DebugLevel  = DEBUG
            gb_LogLevel    = DEBUG
        gb_LogLevel = cfgIO.get(starsNodeName, 'LogLevel', gb_LogLevel, int)
        gb_DebugLevel = cfgIO.get(starsNodeName, 'DebugLevel', gb_DebugLevel, int)
        gb_LogEnable = cfgIO.get(starsNodeName, 'LogEnable', gb_LogEnable, bool)
        lc_LogDir = cfgIO.get(starsNodeName, 'LogDir', lc_LogDir)

    # Fix optional parameters
    starsServerHost = optIO.get(args.StarsServerHost,starsServerHost)
    starsServerPort = optIO.get(args.StarsServerPort,starsServerPort)
    deviceHost      = optIO.get(args.DeviceHost,deviceHost)
    devicePort      = optIO.get(args.DevicePort,devicePort)
    if(lc_DeviceCommandEnable == False):
        lc_DeviceCommandEnable = optIO.get(args.rawenable,False)
    lc_ChannelNameList = optIO.get(args.ChannelNameList,lc_ChannelNameList)
    lc_LimitStatusEventEnableChannelList = optIO.get(args.LimitStatusChannelList,lc_LimitStatusEventEnableChannelList)
    if(lc_pm16c04Compatible == False):
        lc_pm16c04Compatible = optIO.get(args.pm16c04compatible,False)
    if(lc_AllReplyEnable == False):
        lc_AllReplyEnable = optIO.get(args.allreplyenable,False)
    gb_DebugLevel = optIO.get(args.debuglevelnum, gb_DebugLevel)
    gb_LogLevel   = optIO.get(args.loglevelnum, gb_LogLevel)
    if(gb_LogEnable == False):
        gb_LogEnable = optIO.get(args.logenable,False)
    lc_LogDir= optIO.get(args.logdir, lc_LogDir)

    # Check1 program parameters
    if(lc_ChannelNameList is None):
        lc_ChannelNameList=[]
    else:
        lc_ChannelNameList=lc_ChannelNameList.split(',')
        if(len(lc_ChannelNameList) != len(set(lc_ChannelNameList))):
            sys.stdout.write('Duplicate name in ChannelNameList.\n')
            exit(1)
    if(lc_LimitStatusEventEnableChannelList is None):
        lc_LimitStatusEventEnableChannelList=[]
    elif(lc_LimitStatusEventEnableChannelList == ''):
        lc_LimitStatusEventEnableChannelList=[]
    elif(lc_LimitStatusEventEnableChannelList == '*'):
        lc_LimitStatusEventEnable = True
        lc_LimitStatusEventEnableChannelList=[]
    else:
        lc_LimitStatusEventEnableChannelList=lc_LimitStatusEventEnableChannelList.split(',')
        lc_LimitStatusEventEnableChannelList = set(lc_LimitStatusEventEnableChannelList)

    ##################################################################
    # Load logging parameters
    ##################################################################
    logger = None
    rt = setup_logger(starsNodeName, p_logdir=lc_LogDir, p_fflg=gb_LogEnable, p_sflg=gb_Debug, p_flevel=gb_LogLevel, p_slevel=gb_DebugLevel, p_recover=False)
    if(rt != 'Ok:'):
        sys.stdout.write(rt+'\n')
        exit(1)
    ##################################################################
    # Connect to device
    ##################################################################
    #Create device instance with devserver:devport 
    dc=PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLER(deviceHost, devicePort, cmdhandler=devcmdhandler)
    gb_DeviceInstance=dc

    #Set properties for device instance
    dc.setdebug(gb_Debug)
    if(gb_Debug == True): dc.printinfo()

    #Connect to device
    rt = dc.connect()
    if(rt==False):
        sys.stdout.write(dc.getlasterrortext()+'\n')
        exit(1)
    while(True):
        rt=dc.device_receive(1)
        if('Er:' in rt):
            sys.stdout.write(dc.getlasterrortext()+'\n')
        if(rt == ''):
              break

    #Initialize device variables
    rt=dc.device_init()
    if(rt == False):
        dc.disconnect()
        sys.stdout.write(dc.getlasterrortext()+'\n')
        exit(1)

    ##################################################################
    # Parse parameter settings
    ##################################################################
    lc_numberOfChannels = dc.device_getnumberofchannel()
    if(len(lc_ChannelNameList)>lc_numberOfChannels):
        del lc_ChannelNameList[lc_numberOfChannels:]
    for i in range(len(lc_ChannelNameList),lc_numberOfChannels,1):
        channelname='ch'+str(i)
        if(channelname not in lc_ChannelNameList):
            lc_ChannelNameList.append(channelname)
        else:
            sys.stdout.write("Channel name generating error '%s' duplicate\n" %(channelname))
            dc.disconnect()
            exit(1)
    if(lc_numberOfChannels<=2):
        gb_StarsIsUseGetMultiValues = False
    #elif(lc_pm16c04Compatible):
    #    gb_StarsIsUseGetMultiValues = False

    if('_Alert' in lc_ChannelNameList):
        sys.stdout.write("Sorry. Channel name '_Alert' is reserved by this program.\n")
        dc.disconnect()
        exit(1)

    for i in range(lc_numberOfChannels):
        channelname = lc_ChannelNameList[i]
        gb_ChannelNameList[channelname] = str(i)
        gb_LimitEventEnableChannelList.append(lc_LimitStatusEventEnable)
        gb_StarsLocalBusyFlg.append(None)
        gb_StarsLocalStatus.append(None)
        gb_StarsLocalCurrent.append(None)
        if(channelname in lc_LimitStatusEventEnableChannelList):
            gb_LimitEventEnableChannelList[i]=True
            lc_LimitStatusEventEnableChannelList.remove(channelname)
        elif(str(i) in lc_LimitStatusEventEnableChannelList):
            gb_LimitEventEnableChannelList[i]=True
            lc_LimitStatusEventEnableChannelList.remove(str(i))
    for ch in lc_LimitStatusEventEnableChannelList:
        sys.stderr.write("Warning!! LimitStatusChannelList parameter '"+ ch +"' not found in the channel list. Ignored.\n")

    if(gb_Debug==True):
        sys.stdout.write("starsNodeName#"+str(starsNodeName)+"#"+'\n')
        sys.stdout.write("starsServerHost#"+str(starsServerHost)+"#"+'\n')
        sys.stdout.write("starsServerPort#"+str(starsServerPort)+"#"+'\n')
        sys.stdout.write("deviceHost#"+str(deviceHost)+"#"+'\n')
        sys.stdout.write("devicePort#"+str(devicePort)+"#"+'\n')
        sys.stdout.write("numberOfChannels#"+str(len(gb_ChannelNameList.keys()))+"#"+'\n')
        sys.stdout.write("ChannelNameList#"+str(list(gb_ChannelNameList.keys()))+"#"+'\n')
        for channelname in gb_ChannelNameList:
            i = int(gb_ChannelNameList[channelname])
            sys.stdout.write(channelname+".limitstatuseventenable#"+str(gb_LimitEventEnableChannelList[i])+"#"+'\n')
        sys.stdout.write("RawEnable#"+str(lc_DeviceCommandEnable)+"#"+'\n')

    ##################################################################
    # Connect to stars
    ##################################################################
    st  = StarsInterface(starsNodeName, starsServerHost, '', starsServerPort)
    gb_StarsInstance = st

    #Set properties for Stars instance
    setDebug(gb_Debug)
    st._lastsendtime = time.time()
    st._lasttgetvaluetimestamp = {}
    st._devicerawenable = lc_DeviceCommandEnable
    st._deviceisremote = '0'
    st._deviceautorepenenable = '0'
    st._pm16c04Compatible = lc_pm16c04Compatible
    st._isallrepenable = lc_AllReplyEnable
    st._isloggererrordetectedtimes = 0
    rt = st.setdefaultreceivetimeout(3)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        dc.disconnect()
        exit(1)

    #Enable ALL_REP EN
    while(True):
        rt = dc.device_receive(timeout=0.05)
        if('Er:' in rt):
            sys.stdout.write(rt+'\n')
            dc.disconnect()
            exit(1)
        elif(rt==''):
            break
    now = time.time()
    starscommand = 'GetAllReplyEnable'
    if(dc._deviceFirmwareInfo.is_commandsupported('ALL_REP') == True):
        rt = dc.device_act('ALL_REP EN',timeout=1.0)
        if('Er:' in rt):
            sys.stdout.write(rt+'\n')
            dc.disconnect()
            exit(1)
        elif(rt == 'OK'):
            st._deviceisremote = '1'
        elif(rt == 'NG'):
            pass
        elif(rt == ''):
            pass
        else:
            sys.stdout.write("Er: Unexpected reply '" + rt +"' to command 'ALL_REP EN'.\n")
            dc.disconnect()
            st.disconnect()
            exit(1)
    st._lasttgetvaluetimestamp[starscommand] = now

    #Connect to Stars
    rt=st.connect()
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        dc.disconnect()
        exit(1)

    starscommand = 'GetFunction'
    rt=stars_getdevicecontrollervalue(local=False, starscommand=starscommand)
    if('Er:' in rt):
        sys.stdout.write(rt+'\n')
        dc.disconnect()
        st.disconnect()
        exit(1)
    st._deviceisremote = rt
    stars_sendevent(childnode='', eventmessage='_ChangedFunction '+st._deviceisremote, to='System')
    st._lasttgetvaluetimestamp[starscommand] = now

    for starscommand in ['IsBusy','GetValue','GetLimitStatus']:
        rt=stars_getdevicechannelvalue('',local=False,starscommand=starscommand)
        if('Er' in rt):
            sys.stdout.write(rt+'\n')
            dc.disconnect()
            st.disconnect()
            exit(1)
        stars_setlocalcurrent(channellist=list(gb_ChannelNameList.keys()),valuelist=rt.split(','), starscommand=starscommand)
        rt=stars_getdevicechannelvalue('',local=True,starscommand=starscommand)
        st._lasttgetvaluetimestamp[starscommand]=now
    if(st._pm16c04Compatible):
        stars_sendevent(childnode='', eventmessage='_ChangedCtlIsBusy 0')

    #Add callback handler
    rt=st.addcallback(handler)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        dc.disconnect()
        st.disconnect()
        exit(1)
    rt=st.addcallback(device_sockhandler,dc.gethandle(),'DETECT')
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        dc.disconnect()
        st.disconnect()
        exit(1)
    st.send('System flgon '+st.nodename+'._Alert')

    _outputlog(WARN,"*** start transaction. ***")

    #Start Mainloop()
    try:
        rt=st.Mainloop(interval,0.01)
        if(rt==False):
            sys.stdout.write(st.getlasterrortext()+'\n')
            dc.disconnect()
            st.disconnect()
            exit(1)
    except Exception as e:
        pass

    _outputlog(WARN,"*** Normal end transaction. ***\n")

    #Device close
    #*** sleep for callback terminate wait
    time.sleep(1)
    _outputlog(WARN,"*** Bye device. ***\n")
    st.removecallback(dc.gethandle())
    dc.disconnect()
    #st.removecallback()
    #Close sessions
    st.disconnect()
    _outputlog(WARN,"*** Bye STARS. ***\n")
    time.sleep(0.1)
    exit(0)
