#! /usr/bin/python3
"""
  STARS python program Tsuji Electronics Co.,Ltd. Counter-Timer control
    Description: Connect to STARS server and commnicate with the device.
    History:
       0.1     Beta           2018.8.20      Yasuko Nagatani
       0.2     Beta           2023.1.20      Yasuko Nagatani
"""

# Define: program info
__author__ = 'Yasuko Nagatani'
__version__ = '0.2'
__date__ = '2023-1-20'
__license__ = 'MIT'

#----------------------------------------------------------------
# Import modules
#----------------------------------------------------------------
import sys
from os import path,access,sep,W_OK
import time
import re
from collections import OrderedDict,defaultdict
from logging import disable,getLogger,Formatter,StreamHandler,FileHandler,NullHandler,NOTSET,DEBUG,INFO,WARN,WARNING,ERROR,CRITICAL,FATAL,basicConfig
from singlestars import StarsInterface
from stars import StarsMessage
import nportserv

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERFirmwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERFirmwareInfo(str):
    """ PyStarsDeviceTSUJICOUNTERTIMERFirmwareInfo: Counter-Timer device info object.
    """
    def __init__(self, versionstr):
        self.versiondetected = False
        self.version = versionstr
        self.version_no   = 0
        self.version_date = ''
        self.device_name  = ''
        self.numberofchannel = 0
        self.numberofcounter = 0
        self.numberofencoder = 0
        self.value_maximum = {}
        self.is_supported = {}
        self.value_maximum['SCPR']   = 0
        self.value_maximum['SCPRF']  = 0
        self.value_maximum['STPR']   = 0
        self.value_maximum['STPRF']  = 0
        self.value_maximum['GXDN']   = 9999
        self.value_maximum['GTRUN']  = 0
        self.value_maximum['GTOFF']  = 0
        self.value_maximum['TSDT']   = 9999
        self.is_supported['GATE']     = False
        self.is_supported['DOWNLOAD'] = False
        self.is_supported['GT_ACQ']  = False
        self.is_supported['RDALH']   = False
        self.is_supported['ALL_REP'] = False
        self.is_supported['LCD']     = False
        self.is_supported['CTMR']    = False
        self.is_supported['VERH']    = False
        self.is_supported['GATEIN']  = False
        self.is_supported['ROMIN10']  = False
        self.is_supported['IPMODE']   = False
        self.has_error = True
        self.error = 'Uninitialized'
        m = re.search("^(\S+)\s+(\S+)\s+(\S+)\Z", versionstr)
        if m:
            try:
                self.version_no   = float(m.group(1))
                self.version_date = m.group(2)
                self.device_name  = m.group(3)

                # Counter 32bit
                self.value_maximum['SCPR']  = 4294967
                self.value_maximum['SCPRF'] = 4294967295
                
                # Timer 40bit
                self.value_maximum['STPR']  = 1099511627
                self.value_maximum['STPRF'] = 1099511627775
                
                if(re.search('NCT08-02',self.device_name)):
                    # Counter 48bit
                    self.value_maximum['SCPR']  = 281474976710
                    self.value_maximum['SCPRF'] = 281474976710655
                    self.numberofchannel = 8
                    self.numberofcounter = 8
                    if(self.version_no >= 1.02):
                        self.is_supported['RDALH'] = True
                    self.versiondetected = True
                elif(re.search('NCT08-01A',self.device_name)):
                    # Counter 48bit
                    self.value_maximum['SCPR']  = 281474976710
                    self.value_maximum['SCPRF'] = 281474976710655
                    self.numberofchannel = 8
                    self.numberofcounter = 8
                    if(self.version_no >= 1.02):
                        self.is_supported['RDALH'] = True
                    self.versiondetected = True
                elif(re.search('NCT08-01B',self.device_name)):
                    self.numberofchannel = 8
                    self.numberofcounter = 8
                    if(self.version_no >= 1.02):
                        self.is_supported['RDALH'] = True
                    if(self.version_no >= 1.02):
                        self.is_supported['ALL_REP'] = True
                    self.versiondetected = True
                    self.is_supported['GATE']  = True
                    self.value_maximum['GTRUN']  = 4294967295
                    self.value_maximum['GTOFF']  = 4294967295
                elif(re.search('NCT08-01',self.device_name)):
                    self.numberofchannel = 8
                    self.numberofcounter = 8
                    self.versiondetected = True
                    # Timer 32bit
                    self.value_maximum['STPR']  = 4294967
                    self.value_maximum['STPRF'] = 4294967295
                else:
                    #CT08-ER2T
                    m = re.search('CT(\d+)-ER(\d+)',self.device_name)
                    if(m):
                        self.versiondetected = True
                        self.numberofchannel = int(m.group(1))*2
                        self.numberofcounter = int(m.group(1))
                        self.numberofencoder = int(m.group(2))
                        if(self.version_no >= 1.08):
                            self.is_supported['GT_ACQ'] = True
                        self.is_supported['RDALH'] = True
                        if(self.version_no >= 1.02):
                            self.is_supported['ALL_REP'] = True
                        self.is_supported['LCD']   = True
                        self.is_supported['GATE']  = True
                        self.value_maximum['GXDN'] = 29999
                        if(self.numberofchannel >= 32):
                            self.value_maximum['GXDN'] = 14999
                        self.value_maximum['GTRUN']  = 4294967295
                        self.value_maximum['GTOFF']  = 4294967295
                        self.is_supported['ROMIN10']  = True
                        self.is_supported['DOWNLOAD'] = True
                    else:
                        m = re.search("CT(\d+)",self.device_name)
                        if(m):
                            self.versiondetected = True
                            self.numberofchannel = int(m.group(1))
                            self.numberofcounter = int(m.group(1))
                            if(self.version_no >= 1.08):
                                self.is_supported['GT_ACQ'] = True
                            self.is_supported['RDALH'] = True
                            exit
                            if(self.version_no >= 1.02):
                                self.is_supported['ALL_REP'] = True
                            self.is_supported['LCD']    = True
                            self.is_supported['GATE']  = True
                            self.value_maximum['GXDN'] = 55999
                            if(self.numberofchannel >= 64):
                                self.value_maximum['GXDN'] = 7999
                            elif(self.numberofchannel >= 48):
                                self.value_maximum['GXDN'] = 9999
                            elif(self.numberofchannel >= 32):
                                self.value_maximum['GXDN'] = 14999
                            elif(self.numberofchannel >= 16):
                                self.value_maximum['GXDN'] = 29999
                            self.value_maximum['GTRUN']  = 4294967295
                            self.value_maximum['GTOFF']  = 4294967295
                            self.is_supported['ROMIN10']  = True
                            self.is_supported['DOWNLOAD'] = True
                            if(self.device_name.endswith("-01F")):
                                self.is_supported['IPMODE']   = True
                        else:
                            pass
                if(self.numberofchannel>0):
                    self.has_error = False
                else:
                    rt="Unexpected version reply.('%s'). " %(versionstr)
                    self.error = "%s" %(rt)
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

    def get_valuemaximum(self, command):
        if(command == ''):
            return(-1)
        if(command in self.value_maximum):
            return(self.value_maximum[command])
        return(-1)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERHardwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERHardwareInfo(str):
    """ PyStarsDeviceTSUJICOUNTERTIMERHardwareInfo: Counter-Timer device hardware info object.
    """
    def __init__(self, hwversionstr):
        self.versiondetected = False
        self.hardwareversion = hwversionstr
        self.hardwareversion_no = 0
        self.has_error = True
        self.error = 'Uninitialized'
        self.is_supported = {}
        self.is_supported['GATEIN']  = False
        m = re.search("^HD-VER\s(\d+)\Z", hwversionstr.upper())
        if m:
            try:
                self.versiondetected = True
                self.hardwareversion_no   = float(m.group(1))
                self.has_error = False
                if(self.hardwareversion_no>=4):
                    self.is_supported['GATEIN']  = True
            except:
                rt="Analyzing hardware version failure ('%s'). (%s)" %(hwversionstr, type(e))
                self.error = "%s" %(rt)
        else:
            rt="Hardware version reply error ('%s'). Unexpected reply format." %(hwversionstr)
            self.error = "%s" %(rt)
    def is_commandsupported(self, command):
        if(command == ''):
            return(False)
        if(command in self.is_supported):
            return(self.is_supported[command])
        return(True)
        

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERStatus
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERStatus(str):
    """ PyStarsDeviceTSUJICOUNTERTIMERStatus: Channel status object.
    """
    def __init__(self, statusstr):
        self.status = statusstr
        self.has_error = True
        self.error = ''
        self.remote_mode = 1
        self.single_mode = 1
        self.timerstop_mode = 0
        self.counterstop_mode = 0
        self.nonstop_mode = 0
        self.count_running = 0
        m = re.search("^R_SN_([TCN])_([OF])\Z", statusstr.upper())
        if m:
            try:
                buf = m.group(1)
                if(buf == 'T'):
                    self.timerstop_mode = 1
                elif(buf == 'C'):
                    self.counterstop_mode = 1
                else:
                    self.nonstop_mode = 1
                buf = m.group(2)
                if(buf == 'O'):
                    self.count_running = 1
                self.has_error = False
            except:
                rt="Analyzing status failure ('%s'). (%s)" %(statusstr, type(e))
                self.error = "%s" %(rt)
        else:
            rt="Status reply error ('%s'). Unexpected reply format." %(statusstr)
            self.error = "%s" %(rt)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand
#----------------------------------------------------------------
class PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel:
    """ PyStarsDeviceTSUJISTEPPINGMOTORCONTROLLERDeviceCommandLevel: Target codelist of device command.
    """
    CONTROLLER, CHANNEL = range(1,3)

class PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand():
    """ PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand: Device command object.
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
        if(argnum is None): self.argnum = -1
        if(self.argnum<0):  self.ischeckargnum = False
        self.isallowbusy = isallowbusy
        self.checkfunc = checkfunc
        self.postfunc = postfunc
        self.postwaittime = postwaittime
        self.helpstring = helpstring

class PyStarsDeviceTSUJICOUNTERTIMER(nportserv.nportserv):
    """ Class PyStarsDeviceTSUJICOUNTERTIMER: Derived from nportserv to control the device.
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
    def device_receive(self,timeout='',eod=''):
        rt = ''
        if(self.isconnected()==False): return 'Er: Disconnected'
        if(timeout==''): timeout=self.gettimeout()
        if(eod is None):
            while(1):
                rt2=self.receive(timeout,delimiter='')
                if(rt2 is None):
                    return 'Er: ' + self.getlasterrortext()
                rt2 = rt2.replace('\r','')
                rt2 = rt2.replace('\n','\t')
                if(rt2 == ''):
                    break
                rt = rt + rt2
                timeout=1
            if(len(rt)>0):
                if(rt[-1]  == '\t'):
                    rt = rt.rstrip('\t')
            return(rt)
        if(eod == ''):
            rt=self.receive(timeout)
            if(rt is None):
                if(self._cmdhandler is not None): self._cmdhandler("[Recv]<None>")
                return 'Er: ' + self.getlasterrortext()
            if(self._cmdhandler is not None): self._cmdhandler("[Recv]"+rt)
        else:
            while(1):
                rt2=self.receive(timeout,delimiter=eod)
                if(rt2 is None): return 'Er: ' + self.getlasterrortext()
                if(rt2 == ''):
                    continue
                rt = rt + rt2
                break
        #self._deviceCommandLastExecutedTime['LASTEST'] = time.time()
        return rt

    def device_init(self):
        rt = False
        #Read firmware version
        if(self._deviceFirmwareInfo is None):
            rt2 = self.device_act('VER?')
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            elif(rt2 == ''):
                self.error = "Er: No reply. (command 'VER?')"
                return(rt)
            else:
                rt2 = PyStarsDeviceTSUJICOUNTERTIMERFirmwareInfo(rt2)
                if(rt2.has_error):
                    self.error = 'Er: %s' %(rt2.error)
                    return(rt)
                self._deviceFirmwareInfo = rt2
        if(self._deviceHardwareInfo is None):
            self._deviceHardwareInfo = PyStarsDeviceTSUJICOUNTERTIMERHardwareInfo('')
            if(self._deviceFirmwareInfo.is_commandsupported('VERH') == True):
                rt2 = self.device_act('VERH?')
                if('Er:' in rt2):
                    self.error = rt2
                    return(rt)
                elif(rt2 == ''):
                    self._deviceFirmwareInfo.set_commandsupported('VERH', False)
                else:
                    rt2 = PyStarsDeviceTSUJICOUNTERTIMERHardwareInfo(rt2)
                    if(rt2.has_error):
                        self.error = 'Er: %s' %(rt2.error)
                        return(rt)
                    self._deviceHardwareInfo = rt2
                    self._deviceFirmwareInfo.set_commandsupported('VERH', True)
                if(self._deviceFirmwareInfo.is_commandsupported('GATEIN') == False):
                    if(self._deviceHardwareInfo.is_commandsupported('GATEIN') == True):
                        rt2 = self.device_act('GATEIN?')
                        if('Er:' in rt2):
                            pass
                        elif(rt2 == ''):
                            pass
                        else:
                            self._deviceFirmwareInfo.set_commandsupported('GATEIN', True)

        if(self._deviceLastStatus is None):
            rt2 = self.device_act('MOD?')
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            elif(rt2 == ''):
                self.error = "Er: No reply. (command 'MOD?')"
                return(rt)
            else:
                rt2 = PyStarsDeviceTSUJICOUNTERTIMERStatus(rt2)
                if(rt2.has_error):
                    self.error = 'Er: %s' %(rt2.error)
                    return(rt)
                self._deviceLastStatus = rt2
        self._command_config()
        return(True)

    def processdevicereplystring(self,replystr):
        rt= replystr
        if(rt == ''):
            rt='Er: No reply.'
        elif('Er:' in rt):
            pass
        elif(rt == 'OK'):
            rt='Ok:'
        elif(rt == 'NG'):
            rt='Er: Unknown command.'
        return(rt)

    ##################################################################
    # Command functions
    ##################################################################
    def _command_config(self):
        if(self._deviceFirmwareInfo is None): return(False)

        ##################################################################
        # Define command definitions
        ##################################################################
        lc_cmd = {}

        #Define Info returns parameters.(config)
        #----------------#
        # Basic commands #
        #----------------#
        lc_cmd['GetFirmwareVersion'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('VER?', helpstring="Return the controller firmware version string.")
        lc_cmd['IsOverflow']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('ALM?',  ischannelcommand=True, argnum=-1, checkfunc='self._checkisoverflow', postfunc='self._postisoverflow' , helpstring="Return the counter overflow status.")
        lc_cmd['GetValue']        = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('RDAL?', ischannelcommand=True, argnum=-1, checkfunc='self._checkgetvalue',   postfunc='self._postgetvalue'   , helpstring="Return the counter values.")
        lc_cmd['GetHexValue']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('RDAL?', ischannelcommand=True, argnum=-1, checkfunc='self._checkgetvalue',   postfunc='self._postgethexvalue', helpstring="Return the counter values by hex format.")
        lc_cmd['GetStatus']       = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('MOD?',  postfunc='self._postgetstatus',   helpstring="Return the controller status.")
        lc_cmd['GetStopMode']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('MOD?',  postfunc="self._postgetstopmode", helpstring="Return the count stop mode. (T: enable timer stop, C: enable count stop, N: disable auto stop)")
        lc_cmd['GetCountPresetK'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('CPR?',  postfunc='self._postretval', helpstring="Return the counter preset value (unit: Kcts).")
        lc_cmd['GetCountPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('CPRF?', postfunc='self._postretval', helpstring="Return the counter preset value (unit: cts).")
        lc_cmd['GetTimerPresetK'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TPR?',  postfunc='self._postretval', helpstring="Return the timer preset value (unit: millseconds).")
        lc_cmd['GetTimerPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TPRF?', postfunc='self._postretval', helpstring="Return the timer preset value (unit: microseconds).")
        lc_cmd['CounterReset']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('CLAL',  ischannelcommand=True, isreferencecommand=False, argnum=-1, checkfunc='self._checkclearvalue', helpstring="Clear the counter and timer values.")
        lc_cmd['SetStopMode']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('-',     isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc="self._checkstopmode", helpstring="Set the count stop mode. (T: enable timer stop, C: enable count stop, N: disable auto stop)")
        lc_cmd['SetCountPresetK'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SCPR',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc="self._checkcountertimervalue", helpstring="Define the counter preset value (unit: Kcts).")
        lc_cmd['SetCountPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SCPRF', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc="self._checkcountertimervalue", helpstring="Define the counter preset value (unit: cts).")
        lc_cmd['SetTimerPresetK'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('STPR',  isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc="self._checkcountertimervalue", helpstring="Define the timer preset value (unit: millseconds).")
        lc_cmd['SetTimerPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('STPRF', isreferencecommand=False, isallowbusy=False, argnum=1, checkfunc="self._checkcountertimervalue", helpstring="Define the timer preset value (unit: microseconds).")
        lc_cmd['Stop']            = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('STOP' , isreferencecommand=False, isunlockcommand=True    , helpstring="Stop counting action.")
        lc_cmd['CountStart']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('STRT' , isreferencecommand=False, isallowbusy=False, ismotioncommand=True, helpstring="Start counting action.")
        lc_cmd['Reset']           = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('REST' , isreferencecommand=False, isallowbusy=False, islockcommand=True, postwaittime=30, helpstring="Change to the cold-start state.")

        #-------------------#
        # Optional commands #
        #-------------------#
        lc_cmd['GetHardwareVersion'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('VERH?', checkfunc="self._checkhardwareversion", helpstring="Return the controller hardware version string.")
        lc_cmd['GetGateEnable']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GATEIN?',  checkfunc="self._checkgateincommand", postfunc='self._postgetonoff', helpstring="Return the gate in state. (0:disable 1:enable)")
        lc_cmd['SetGateEnable']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GATEIN', checkfunc="self._checksetgateinenable", isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate in state. (0:disable 1:enable)")
        lc_cmd['GetRunOutputAutoMinimumWidthEnable']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('MIN10U?', checkfunc="self._checkmin10command", postfunc='self._postgetonoff', helpstring="Return the run output minimum width auto corrention state. (0:disable 1:enable)")
        lc_cmd['SetRunOutputAutoMinimumWidthEnable'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('MIN10U', checkfunc="self._checksetmin10enable", isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the run output minimum width auto corrention state. (0:disable, 1:enable)")
        lc_cmd['GetAllReplyEnable'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('ALL_REP?', checkfunc="self._checkallrepcommand", postfunc='self._postgetonoff', helpstring="Return the all reply state. (0:disable 1:enable)")
        lc_cmd['SetAllReplyEnable'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('ALL_REP', checkfunc="self._checksetallrepenable", isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the all reply state. (0:disable, 1:enable)")
        lc_cmd['GetCountInputSignalSelection'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('IN?', argnum=-1,  checkfunc="self._checkgetinputselection", postfunc='self._postgetinputselection', helpstring="Return the input mode settings.")
        lc_cmd['SetCountInputSignalSelection'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('-'  , argnum=-1, isreferencecommand=False, isallowbusy=False, checkfunc="self._checksetinputselection", helpstring="Set the input mode settings.(inputmode: TTL_Hi|TTL_HI|THI, TTL_50|T50, NIM)")

        #----------------------#
        # LCD Display commands #
        #----------------------#
        lc_cmd['SetLCDBgLightEnable'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('BK'     , isreferencecommand=False, checkfunc="self.checklcdbgenable", helpstring="Turn the LCD backlight on/off. (0:off 1:on)")
        lc_cmd['ShowLCDTimerPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SD_TP'  , isreferencecommand=False, argnum=1, checkfunc='self._checklcddispcommand', helpstring="Show the timer preset value on the LCD. (0,U: on the upper line, 1,D: on the lower line)")
        lc_cmd['ShowLCDCountPreset']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SD_CP'  , isreferencecommand=False, argnum=1, checkfunc='self._checklcddispcommand', helpstring="Show the count preset value on the LCD. (0,U: on the upper line, 1,D: on the lower line)")
        lc_cmd['ShowLCDTimer']        = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SD_TM'  , isreferencecommand=False, argnum=1, checkfunc='self._checklcddispcommand', helpstring="Show the timer value current on the LCD. (0,U: on the upper line, 1,D: on the lower line)")
        lc_cmd['ShowLCDChannelNo']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('SD_'    , isreferencecommand=False, argnum=2, checkfunc='self._checklcddispchannel', helpstring="Show the timer value current on LCD. (Two parameters required: First=> 0,U: on the upper line, 1,D: on the lower line: Second=> channel number)")

        #-------------------#
        # Download commands #
        #-------------------#
        lc_cmd['GetGateSyncDownloadFormat']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('XSDL?',  checkfunc='self._checkgatesyncdownloadcommand', postfunc='self._postgetgatesyncdownloadformat', helpstring="Return the gate synchronous download format. (return fromch toch timer_selected_or_not(1:selected 0:ignored) hex_or_decimal(H:hex D:Decimal)")
        lc_cmd['GetTimerSyncDownloadFormat'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TSDL?',  checkfunc='self._checkgatesyncdownloadcommand', postfunc='self._postgetgatesyncdownloadformat', helpstring="Return the timer synchronous download channels. (return fromch toch timer_selected_or_not(1:selected 0:ignored) hex_or_decimal(H:hex D:Decimal)")
        lc_cmd['GetTimerSyncDownloadInterval'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TSDT?',  checkfunc='self._checkgatesyncdownloadcommand', postfunc="self._postgetgatesynctimerdownloadinterval", helpstring="Return the timer synchronous download interval.")

        lc_cmd['SetGateSyncDownloadFormat']  = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('XSDL',  checkfunc='self._checksetgatesyncdownloadformat',argnum=-1, helpstring="Set the gate synchronous download channels. (At least 3 parameters required, 1 parameter optional. (Parameters: fromch toch timer_selected_or_not(1:selected 0:ignored [H|D(H:Hex D:Decimal, STARS sets H as default.)])")
        lc_cmd['SetTimerSyncDownloadFormat'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TSDL',  checkfunc='self._checksetgatesyncdownloadformat',argnum=-1, helpstring="Set the gate synchronous download channels. (At least 3 parameters required, 1 parameter optional. (Parameters: fromch toch timer_selected_or_not(1:selected 0:ignored [H|D(H:Hex D:Decimal, STARS sets H as default.)])")
        lc_cmd['SetTimerSyncDownloadInterval'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('TSDT',  checkfunc='self._checksetgatesynctimerdownloadinterval',argnum=1, helpstring="Set the gate synchronous download interval.")

        #---------------#
        # Gate commands #
        #---------------#
        lc_cmd['GetGateSyncStatus']               = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSTS?',   checkfunc='self._checkgatecommand'    , helpstring="Return the gate synchronous data acquisition status.")
        lc_cmd['GetGateSyncData']                 = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDAL?',  checkfunc='self._checkgetgatesyncdata', readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return all the gate synchronous data acquisition data.")
        lc_cmd['GetGateSyncHexData']              = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDALH?', checkfunc='self._checkgetgatesyncdata', readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return all the gate synchronous data acquisition data in hex values.")
        lc_cmd['GetGateSyncDataAddressFromTo']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDRD?',  checkfunc='self._checkgetgatesyncdata', argnum=2, readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return the gate synchronous data acquisition data address from to.")
        lc_cmd['GetGateSyncHexDataAddressFromTo'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDRDH?', checkfunc='self._checkgetgatesyncdata', argnum=2, readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return the gate synchronous data acquisition data in hex values from to.")
        lc_cmd['GetGateSyncDataChannelFromToAddressFromTo']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSCRD?',  checkfunc='self._checkgetgatesyncdata', argnum=5, readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return the gate synchronous data acquisition data channel and address from to.")
        lc_cmd['GetGateSyncHexDataChannelFromToAddressFromTo'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSCRDH?', checkfunc='self._checkgetgatesyncdata', argnum=5, readeod=None, postfunc='self._postgetgatesyncdata', helpstring="Return the gate synchronous data acquisition data in hex channel and address from to.")

        lc_cmd['GetGateSyncStartAddress']   = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDN?',  checkfunc='self._checkgatecommand', helpstring="Get the gate synchronous data acquisition current data number.")
        lc_cmd['GetGateSyncEndAddress']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSED?',  checkfunc='self._checkgatecommand', helpstring="Get the gate synchronous data acquisition end data number.")
        lc_cmd['SetGateSyncStartAddress']   = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSDN',   checkfunc='self._checksetgateaddress', isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate synchronous data acquisition data number.")
        lc_cmd['SetGateSyncEndAddress']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSED',   checkfunc='self._checksetgateaddress', isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate synchronous data acquisition end data number.")
        lc_cmd['GateSyncStartAddressReset'] = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('CLGSDN', checkfunc='self._checkgatecommand',    isreferencecommand=False, isallowbusy=False,           helpstring="Clear the gate synchronous data number.")
        lc_cmd['GateSyncDataReset']         = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('CLGSAL', checkfunc='self._checkgatecommand',    isreferencecommand=False, isallowbusy=False, islockcommand=True, postwaittime=30, helpstring="Clear all the gate synchronous acquired data. (It takes about 30 seconds.)")

        lc_cmd['GateSyncGateModeStart']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GSTRT' , checkfunc='self._checkgatecommand', isreferencecommand=False, isallowbusy=False, ismotioncommand=True, helpstring="Start the gate synchronous data acquisition.")
        lc_cmd['GateSyncEdgeModeStart']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GESTRT', checkfunc='self._checkgatecommand', isreferencecommand=False, isallowbusy=False, ismotioncommand=True, helpstring="Start the gate edge synchronous data acquisition.")
        lc_cmd['GateSyncTimerModeStart']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GTSTRT', checkfunc='self._checkgatecommand', isreferencecommand=False, isallowbusy=False, ismotioncommand=True, helpstring="Start the gate timer synchronous data acquisition.")
        lc_cmd['SetGateSyncTimerOnTime']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GTRUN' , checkfunc='self._checksetgatetimervalue', isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate timer synchronous run time (unit: microseconds).")
        lc_cmd['SetGateSyncTimerOffTime']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GTOFF' , checkfunc='self._checksetgatetimervalue', isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate timer synchronous off time (unit: microseconds).")
        lc_cmd['GetGateSyncTimerOnTime']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GTRUN?', checkfunc='self._checkgatecommand', helpstring="Return the gate timer synchronous run time (unit: microseconds).")
        lc_cmd['GetGateSyncTimerOffTime']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GTOFF?', checkfunc='self._checkgatecommand', helpstring="Return the gate timer synchronous off time (unit: microseconds).")

        lc_cmd['SetGateSyncDataMode']        = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GT_ACQ' , checkfunc="self._checksetgatedatamode", isreferencecommand=False, isallowbusy=False, argnum=1, helpstring="Set the gate synchronous data differential/full. (D(IFF):differential F(ULL):full)")
        lc_cmd['GetGateSyncDataMode']        = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('GT_ACQ?', checkfunc="self._checkgetgatedatamode", helpstring="Get the gate synchronous data acquisition end data number.")


        lc_cmd['hello']                =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=True,  isglobalcommand=True, helpstring="Return 'hello nice to meet you.'")
        lc_cmd['help']                 =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=True,  isglobalcommand=True, helpstring="Return the list or the explanation of stars command.")
        lc_cmd['getversion']           =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return this program version.")
        lc_cmd['getversionno']         =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the version number of this program.")
        lc_cmd['terminate']            =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Terminate this program.")
        lc_cmd['listnodes']            =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the list of motors.")
        lc_cmd['GetChannelList']         =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the list of channels.")
        lc_cmd['IsBusy']               =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=True,  isglobalcommand=True, helpstring="Return the busy status.")
        lc_cmd['GetNumberOfChannels'] =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the number of counter-encoder channels.")
        lc_cmd['GetNumberOfCounters'] =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the number of counter channels.")
        lc_cmd['GetNumberOfEncoders'] =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the number of encoder channels.")
        lc_cmd['SendRawCommand'] =PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Execute device command.")

        lc_cmd['SetLogDir']         = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Set the log output directory.")
        lc_cmd['GetLogDir']         = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Return the log output directory.")
        lc_cmd['SetLogEnable']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Set the log output state enable or not.")
        lc_cmd['IsLogEnabled']      = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Return the log output state.")
        lc_cmd['SetDebugEnable']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Set the debug print output state enable or not.")
        lc_cmd['IsDebugEnabled']    = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Return the debug print output state.'")
        lc_cmd['SetLogLevel']       = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Set the log output detail level.(DEBUG:10,INFO:20,WARN:30,FATAL:40)")
        lc_cmd['GetLogLevel']       = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Return the log output detail level.")
        lc_cmd['SetDebugLevel']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Set the debug print output detail level.(DEBUG:10,INFO:20,WARN:30,FATAL:40)")
        lc_cmd['GetDebugLevel']     = PyStarsDeviceTSUJICOUNTERTIMERDeviceCommand('', ishelponly=True, helpstring="Return the debug print output detail level.")

        self._deviceSTARSCommand = lc_cmd
        return(True)


    def devicecommandobject(self,starscommand):
        rt = None
        if(starscommand in self._deviceSTARSCommand.keys()):
            rt = self._deviceSTARSCommand[starscommand]
        return(rt)

    def get_commandlastexecutedtime(self):
        return(self._deviceCommandLastExecutedTime['LATEST']);

    def get_commandlastwaittime(self):
        return(self._deviceCommandLastWaitTime);

    def exec_command(self,level,starscommand,parameters,addrlist,busyCheck=True,checkOnly=False):
        dobj = self.devicecommandobject(starscommand)
        if(dobj is None):
            return("Er: Command undefined. (func='exec_command', starscommand=%s)" %(starscommand))
        elif(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER):
            if(dobj.isglobalcommand == False):
                return("Er: Command not found. (func='exec_command', level=%s, starscommand=%s)" %(str(level),starscommand))
            if(len(addrlist) <= 0):
                addrlist = [-1]
        elif(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL):
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
        
        readeod = dobj.readeod
        cargnum=dobj.argnum
        ischeckcargnum=dobj.ischeckargnum
        ccommandtag = dobj.commandtag
        creplytag = dobj.replytag
        ctw  =dobj.postwaittime
        cisallowbusy=dobj.isallowbusy

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
                    if(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL):
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i])
                    else:
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i])
                    if(devcommandtag[i] == ''): return(errormsg)
                replytagI.append(creplytag)
        else:
            if(ischeckcargnum and (cargnum != len(parameters))): return('Er: Bad parameters.')
            for i in range(len(addrlist)):
                paramarg.append(parameters)
                devcommandtag.append(ccommandtag)
                if(dobj.checkfunc is not None):
                    if(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL):
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i], addrlist[i])
                    else:
                        (devcommandtag[i], errormsg) = eval(dobj.checkfunc)(devcommandtag[i], paramarg[i])
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

            if(dobj.isunlockcommand):
                cuselocalbusy=True
            elif(dobj.islockcommand):
                cuselocalbusy=True
            elif(dobj.ismotioncommand):
                cuselocalbusy=True

            b = self.device_getisbusy()
            if(b == 1):
                return('Er: Device is busy.')
            self._device_setisbusy(0)
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
                id = '%02d' % int(id)
                if(int(id) < 0):
                    if(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER):
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

                if(level == PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER):
                    devcommand = ''+devcommandtag[i]
                    replytag = replytagI[i]
                else:
                    devcommand = devcommandtag[i]
                    replytag = replytagI[i]

                if(devcommandtag[i] == ''):
                    rt='Ok:'
                    if(dobj.postfunc is not None):
                        rt=eval(dobj.postfunc)(rt,devcommand)
                    else:
                        rt=self._postbase(rt,devcommand)
                    rt2=rt
                elif(dobj.isreferencecommand==True):
                    sendcmd = devcommand.split('\t')
                    for i in range(len(sendcmd)):
                        devcommand = sendcmd[i]
                        rt=self.device_send(devcommand)
                        #error break
                        if('Er:' in rt):
                            rt2=rt
                            break
                        tt = 0
                        rnum = 0
                        while(True):
                            if(tt>rnum):
                                rt3=self.device_receive(0.005,readeod)
                                if(rt == ''):
                                    rt2 = 'Er: Timeout.'
                                    break
                            else:
                                rt3=self.device_receive('',readeod)
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
                        else: rt2=rt2+','+rt
                else:
                    sendcmd = devcommand.split('\t')
                    for i in range(len(sendcmd)):
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
                            rt3=self.device_receive(0.005)
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
    def get_ismotorrunning(self):
        if(self._deviceLastStatus is None):
            return True
        return(self._deviceLastStatus.count_running)

    def device_getnumberofcounter(self):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.numberofcounter)

    def device_getnumberofencoder(self):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.numberofencoder)

    def device_getnumberofchannel(self):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.numberofchannel)

    def device_isdownloadsupported(self):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.is_supported['DOWNLOAD'])

    ## Device set busyflg
    def device_getflgbusy(self):
        b=self.device_getisbusy()
        if(b > 0):
           return(1)
        lst1=dc.get_ismotorrunning()
        b = lst1
        if(b >= 1): return(1)
        return(0)

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
        self._deviceFirmwareInfo = None
        self._deviceHardwareInfo = None
        self._deviceLastStatus   = None

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
        if('Er:' in rt):
            return(rt)
        return(rt)

    def _postgetstatus(self,rt,devcommand):
        rt2 = PyStarsDeviceTSUJICOUNTERTIMERStatus(rt)
        if(rt2.has_error == True):
            return('Er: %s' %(rt2.error))
        else:
            self._deviceLastStatus = rt2
            self._deviceCommandLastExecutedTime['STATUS'] = time.time()
        return(rt2)

    def _postgetstopmode(self,rt,devcommand):
        rt2 = self._postgetstatus(rt,devcommand)
        if('Er:' in rt2):
            return(rt2)
        if(rt2.timerstop_mode == 1):
            return('T')
        elif(rt2.counterstop_mode == 1):
            return('C')
        elif(rt2.nonstop_mode == 1):
            return('N')
        return('Er: Unknown status')

    def get_laststatustimestamp(self):
        if('STATUS' in self._deviceCommandLastExecutedTime):
            return(self._deviceCommandLastExecutedTime['STATUS'])
        return(0)

    def _postgethexvalue(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        elif(devcommand.endswith('H?')):
            datas=rt.split(' ')
            rt = ','.join(datas)
        else:
            datas=rt.split(' ')
            for i in range(len(datas)):
                datas[i]="%X" %(int(datas[i]))
            rt = ','.join(datas)
        return(rt)

    def _postisoverflow(self,rt,devcommand):
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        maxch = self._deviceFirmwareInfo.numberofchannel
        m = None
        if(rt == ''):
            return('Er: No data.')
        olist = []
        m = re.search("^OVER([\S]+)\Z", rt.upper())
        if(m):
           buf=m.group(1)
           l = len(buf)
           if(l<6):
                return('Er: Un expected reply. (%s)' %(rt))
           l = l - 2
           buf = buf[0:l]
           buf2 = buf[l:l+2]
           tm = '0'
           if(buf2 == 'TM'):
               tm = '1'
           flen = l / 2 * 8
           if(maxch>flen):
                return('Er: Un expected reply. (Too short:%s maxch:%d)' %(rt,flen))
           buf=format(int(buf,16),'0%db' %(flen))
           buf=buf[::-1]
           olist = list(buf)
           olist = olist[0:maxch]
           olist.append(tm)
           rt = ','.join(olist)
        return(rt)

    def _postgetinputselection(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        else:
            #CH  0 -  7 : TTL_Hi  TTL_Hi  TTL_Hi  TTL_Hi  TTL_Hi  TTL_Hi  TTL_Hi  TTL_Hi
            m = re.search('CH\s*(\d+)\s*-\s*(\d+)\s*:\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)',rt)
            if(m):
                datas = [m.group(i) for i in range (3,11)]
                rt = ','.join(datas)
                rt = m.group(1) + '-' + m.group(2) + ' ' + rt
            else:
                return('Er: Un expected reply. (%s to %s)' %(rt,devcommand))
        return(rt)

    def _postgetgatesynctimerdownloadinterval(self,rt,command):
        rt2 = rt.uppper().replace("MS")
        try:
            float(rt2)
        except ValueError:
            pass
        else:
            if(float(rt2).is_integer()):
                 rt=str(int(rt2))
        return(rt)

    def _postgetgatesyncdownloadformat(self,rt,command):
        m = re.search("^(H|D)_(\d+)_(\d+)_(\d+)\Z", rt.upper())
        if(m):
            fmt=m.group(1)
            lch=int(m.group(2))
            hch=int(m.group(3))
            tm=int(m.group(4))
            return("%d %d %d %s" %(lch,hch,tm,fmt))
        return("Er: Un expected reply. (rt='%s')" %(rt))


    def _postgetgatesyncdata(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt = rt.replace('\r','')
        rt = rt.replace('\n','\t')
        datas=rt.split('\t')
        for i in range(len(datas)):
            datas[i]=datas[i].replace(' ','')
        rt = '\t'.join(datas)
        return(rt)

    def _postgetvalue(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        elif('H?' in devcommand):
            datas=rt.split(' ')
            for i in range(len(datas)):
                datas[i]=str(int(datas[i],16))
            rt = ','.join(datas)
        else:
            datas=rt.split(' ')
            for i in range(len(datas)):
                datas[i]=str(int(datas[i]))
            rt = ','.join(datas)
        return(rt)

    def _postretval(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        else:
            rt=str(int(rt))
        return(rt)

    def _postgetonoff(self,rt,devcommand):
        rt = rt.upper()
        if(rt == ''):
            return('Er: No data.')
        elif(rt == 'EN'):  rt = '1'
        elif(rt == 'DS'):  rt = '0'
        else:
            return('Er: Un expected reply.')
        return(rt)

    ##################################################################
    # Check functions(internal use)
    ##################################################################
    def _checkcmdargs(self,cmd,args):
        rt = ''
        errormsg=''
        return(cmd,"")

    def _sub_checkvaluerange(self,val,minnum,maxnum):
        rt = ''
        errormsg='Er: Value must be between %d and %d.' %(minnum, maxnum)
        sign = ''
        if(max([ord(c) for c in val]) < 128):
            if(val.startswith('-')==True):
                val=val.lstrip('-')
                sign='-'
            elif(val.startswith('+')):
                val=val.lstrip('+')
            if(val.isdigit()==True):
                num = int(sign+val)
                if((minnum<=num) and (num<=maxnum)):
                    rt='%d' % (num)
                    errormsg=''
        return(rt,errormsg)

    def _checkstopmode(self,cmd,args):
        rt = ''
        errormsg="Er: Bad parameters."
        val=args[0].upper()
        if(val == 'T'):
            rt = 'ENTS'
        elif(val == 'N'):
            rt = 'DSAS'
        elif(val == 'C'):
            rt = 'ENCS'
        if(rt == ''):
            return(rt,errormsg)
        return(rt,errormsg)

    def _checkonoff(self,cmd,args):
        val=args[0].upper()
        rt = ''
        errormsg='Er: Value must be 0 or 1.'
        if(val == 'EN'):  val = '1'
        elif(val == 'DS'):  val = '0'
        elif(val == 'ON'):  val = '1'
        elif(val == 'OFF'): val = '0'
        if(val == '0' or val == '1'):
            rt=val
        if(rt == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

    def _checkisoverflow(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        arglen=len(args)
        maxch = self._deviceFirmwareInfo.numberofchannel
        if(maxch>8):
            cmd = 'ALMX'
        errormsg="Er: Bad parameters."
        if(arglen == 0):
            rt = cmd
            pass
        elif(arglen == 1):
            val = args[0].upper()
            m = re.search("^([\d]+)-([\d]+)\Z",val)
            if(m):
                lch = int(m.group(1))
                hch = int(m.group(2))
                tm = 0
                if((0<=lch) and (hch<=maxch)):
                    if(lch<=hch):
                       rt = cmd
            elif(val == 'TM'):
                rt = cmd
            else:
                try:
                    ch = int(val)
                    if(ch == maxch):
                        rt = cmd
                    elif((ch >= 0) and (ch < maxch)):
                        rt = cmd
                except ValueError:
                    pass
        return(rt,errormsg)

    def _checkclearvalue(self,cmd,args):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            errormsg = "Er: Procedure 'device_init()' unprocessed."
            return(rt,errormsg)
        arglen=len(args)
        maxch = self._deviceFirmwareInfo.numberofchannel
        errormsg="Er: Bad parameters."
        if(arglen == 0):
            rt = cmd
            pass
        elif(arglen == 1):
            val = args[0].upper()
            m = re.search("^([\d]+)-([\d]+)\Z",val)
            if(m):
                lch = int(m.group(1))
                hch = int(m.group(2))
                tm = 0
                if((0<=lch) and (hch<=maxch)):
                    if(lch == hch):
                        if(hch == maxch):
                            rt='CLTM'
                        else:
                            rt='CLCT%02d' %(hch)
                    else:
                        if(hch == maxch):
                            hch = hch -1
                            tm = 1
                        if(lch<=hch):
                           rt='CLCT%02d%02d' %(lch,hch)
                        if(tm == 1):
                            rt=rt+'\tCLTM'
            elif((val == 'TM') or (val == 'TIMER')):
                rt='CLTM'
            elif((val == 'PC') or (val == 'PRESETCOUNT')):
                rt='CLPC'
            else:
                try:
                    float(val)
                except ValueError:
                    pass
                else:
                    if(float(val).is_integer()):
                        ch = int(val)
                        if(ch == maxch):
                            rt = 'CLTM'
                        elif((ch >= 0) and (ch < maxch)):
                            rt = 'CLCT%02d' %(ch)
        return(rt,errormsg)

    def _checkcountertimervalue(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        arglen=len(args)
        max = self._deviceFirmwareInfo.get_valuemaximum(cmd)
        errormsg="Undefined command '%s'." %(cmd)
        if(max<0):
            return(rt,errormsg)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            val=args[0]
            (rt,errormsg)=self._sub_checkvaluerange(val,0,max)
            if(rt != ''):
                return(cmd+rt,errormsg)
        return(rt,errormsg)

    def _checkgetvalue(self,cmd,args,id='-1'):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        ishex = self._deviceFirmwareInfo.is_commandsupported('RDALH')
        arglen=len(args)
        maxch = self._deviceFirmwareInfo.numberofchannel
        errormsg="Er: Bad parameters."
        if(arglen == 0):
            if(int(id)<0):
                rt = cmd
            val = id
        else:
            if(int(id)>=0):
                return(rt,errormsg)
            val = args[0].upper()

        if(rt == ''):
            m = re.search("^([\d]+)-([\d]+)\Z",val)
            if(m):
                lch = int(m.group(1))
                hch = int(m.group(2))
                tm = 0
                if((0<=lch) and (hch<=maxch)):
                    if(lch == hch):
                        if(hch == maxch):
                            rt='TMR?'
                        else:
                            rt='CTR?%02d' %(hch)
                    else:
                        if(hch == maxch):
                            hch = hch -1
                            tm = 1
                        if(lch<=hch):
                            if(self._deviceFirmwareInfo.is_commandsupported('CTMR') == True):
                                rt='CTMR?%02d%02d%02d' %(lch,hch,tm)
                            else:
                                rt='CTR?%02d%02d' %(lch,hch)
                                if(tm == 1):
                                    rt=rt+'\tTMR?'
            elif((val == 'TM') or (val == 'TIMER')):
                rt='TMR?'
            else:
                try:
                    ch = int(val)
                    if(ch == maxch):
                        rt = 'TMR?'
                    elif((ch >= 0) and (ch < maxch)):
                        rt = 'CTR?%02d' %(ch)
                except ValueError:
                    pass
        if(rt != ''):
            if(ishex):
                rt = rt.replace('?','H?')
        return(rt,errormsg)

    def _checkhardwareversion(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('VERH')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    def _checksetgateinenable(self,cmd,args):
        (rt,errormsg)=self._checkgateincommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            (rt,errormsg)=self._checkonoff('',args)
            if(rt != ''):
                rt = rt.replace(' 0','_DS')
                rt = rt.replace(' 1','_EN')
                rt = cmd + rt
        return(rt,errormsg)

    def _checkgateincommand(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('GATEIN')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    def _checksetallrepenable(self,cmd,args):
        (rt,errormsg)=self._checkallrepcommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            (rt,errormsg)=self._checkonoff('',args)
            if(rt != ''):
                rt = rt.replace(' 0','_DS')
                rt = rt.replace(' 1','_EN')
                rt = cmd + rt
        return(rt,errormsg)

    def _checkallrepcommand(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('ALL_REP')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    def _checksetmin10enable(self,cmd,args):
        (rt,errormsg)=self._checkmin10command(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            (rt,errormsg)=self._checkonoff('',args)
            if(rt != ''):
                rt = rt.replace(' 0','_DS')
                rt = rt.replace(' 1','_EN')
                rt = cmd + rt
        return(rt,errormsg)

    def _checkmin10command(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd) 
        if(self._deviceFirmwareInfo.is_commandsupported('ROMIN10')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    #********** Checker for Gate commands **************
    def _checkgetgatesyncdata(self,cmd,args):
        (rt,errormsg)=self._checkgatecommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        max = self._deviceFirmwareInfo.get_valuemaximum('GXDN')
        errormsg="Undefined command '%s'." %(cmd)
        if(max<0):
            return(rt,errormsg)
        arglen=len(args)
        rt = ''
        addhex = '?'
        cmd2 = cmd
        if(cmd2.endswith('H?')):
            addhex = 'H?'
            cmd2 = cmd2.replace('H?','?')
        maxch = self._deviceFirmwareInfo.numberofchannel
        if(maxch>8):
            cmd2 = cmd2.replace('?','X?')
        cmd2 = cmd2.replace('?',addhex)
        errormsg="Er: Bad parameters."
        srow=""
        lrow=""
        if(arglen == 0):
            if(cmd2.startswith("GSDAL")==False):
                return(rt,errormsg)
            rt = cmd2
        else:
            if(arglen==2):
                if(cmd2.startswith("GSDRD")==True):
                    srow=args[0]
                    lrow=args[1]
                else:
                    return(rt,errormsg)
            elif(arglen==5):
                if(cmd2.startswith("GSCRD")==True):
                    srow=args[3]
                    lrow=args[4]
                    try:
                        fch = int(args[0])
                        tch = int(args[1])
                        tm  = int(args[2])
                        if((0>fch) and (fch>(maxch-1))):
                            return(rt,errormsg)
                        if((0>tch) and (tch>(maxch-1))):
                            return(rt,errormsg)
                        if(fch>tch):
                            return(rt,errormsg)
                        if((0>tm) and (tm>1)):
                            return(rt,errormsg)
                        if(maxch>8):
                            cmd2 = cmd2 + "%02d%02d%02d"  %(fch,tch,tm)
                        else:
                            cmd2 = cmd2 + "%0d%0d%0d" %(fch,tch,tm)
                    except ValueError:
                        return(rt,errormsg)
                else:
                    return(rt,errormsg)
            else:
                return(rt,errormsg)
            (rt,errormsg)=self._checksetgateaddress('-',[srow])
            if(rt == ''):
                return(rt,errormsg)
            (rt,errormsg)=self._checksetgateaddress('-',[lrow])
            if(rt == ''):
                return(rt,errormsg)
            sval=int(srow)
            lval=int(lrow)
            if(sval > lval):
                errormsg="'Address from to bad order. (%s < %s)" %(srow, lrow)
                return(rt,errormsg)
            cmds = []
            if(lval < 10000):
                cmds.append(cmd2 + "%04d%04d" %(sval,lval))
            else:
                errormsg = 'Er: Data number exceeding 10000 should be multiples of 1000.'
                lrow=str(lval)
                if(lrow.endswith('000')==True):
                    if(sval < 10000):
                        cmds.append(cmd2 + "%04d" %(sval) + "04d" %(9999))
                        cmds.append(cmd2 + "%04d" %(10) + "04d" %(int(lrow[:-3])) + 'K')
                    else:
                        srow=str(sval)
                        if(srow.endswith('000')==True):
                            cmds.append(cmd2 + "%04d" %(int((srow[:-3]))) + "04d" %(int(lrow[:-3])) + 'K')
            if(len(cmds)>0):
                rt = '\t'.join(cmds)
                return(rt,errormsg)
        return(rt,errormsg)

    def _checksetgatedatamode(self,cmd,args):
        (rt,errormsg)=self._checkgatecommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('GT_ACQ')==False):
            return(rt,errormsg)
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            val=args[0]
            m= re.search("^(DIF|D|DIFF|FUL|F|FULL)\Z", val.upper())
            if(m):
               if(val.upper().startswith('D')):
                   rt = cmd + '_DIF'
               else:
                   rt = cmd + '_FUL'
        return(rt,errormsg)

    def _checkgetgatedatamode(self,cmd,args):
        (rt,errormsg)=self._checkgatecommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('GT_ACQ')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    def _checksetgateaddress(self,cmd,args):
        (rt,errormsg)=self._checkgatecommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        max = self._deviceFirmwareInfo.get_valuemaximum('GXDN')
        errormsg="Undefined command '%s'." %(cmd)
        if(max<0):
            return(rt,errormsg)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            val=args[0]
            (rt,errormsg)=self._sub_checkvaluerange(val,0,max)
            if(rt != ''):
                return(cmd+rt,errormsg)
        return(rt,errormsg)

    def _checksetgatetimervalue(self,cmd,args):
        (rt,errormsg)=self._checkgatecommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        max = self._deviceFirmwareInfo.get_valuemaximum(cmd)
        errormsg="Undefined command '%s'." %(cmd)
        if(max<0):
            return(rt,errormsg)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            val=args[0]
            (rt,errormsg)=self._sub_checkvaluerange(val,0,max)
            if(rt != ''):
                return(cmd+rt,errormsg)
        return(rt,errormsg)

    def _checkgatecommand(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('GATE')==False):
            return(rt,errormsg)
        rt = cmd
        return(rt,errormsg)

    #********** Checker for LCD **************
    def _checklcdbgenable(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('LCD')==False):
            return(rt,errormsg)
        (rt,errormsg)=self._checkonoff('',args)
        if(rt != ''):
            rt = rt.replace(' 0','OFF')
            rt = rt.replace(' 1','ON')
            rt = cmd + rt
        return(rt,errormsg)

    def _checklcddispchannel(self,cmd,args):
        (rt,errormsg)=self._checklcddispcommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        cmd = rt
        rt = ''
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen != 2):
            return(rt,errormsg)
        val = args[0].upper()
        if((val == 'TM') or (val == 'TIMER')):
            rt = 'TM'
        elif((val == 'TP') or (val == 'TIMERPRESET')):
            rt = 'TP'
        elif((val == 'CP') or (val == 'COUNTPRESET')):
            rt = 'CP'
        else:
            try:
                float(val)
            except ValueError:
                pass
            else:
                if(float(val).is_integer()):
                    ch = int(val)
                    maxch = self._deviceFirmwareInfo.numberofchannel
                    if(ch == maxch):
                        rt = 'TM'
                    elif((ch >= 0) and (ch < maxch)):
                        rt = '%02d' %(ch)
        if(rt != ''):
            rt = cmd + rt
        return(rt,errormsg)

    def _checklcddispcommand(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('LCD')==False):
            return(rt,errormsg)
        arglen=len(args)
        errormsg="Er: Bad parameters."
        if(arglen>=1):
            val=args[0].upper()
            if((val == '0') or (val == 'U')):
                rt = cmd.replace('_','U')
            elif((val == '1') or (val == 'L')):
                rt = cmd.replace('_','L')
        return(rt,errormsg)

    #********** Checker for InputSelection commands **************
    def _checkgetinputselection(self,cmd,args):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            errormsg = "Er: Procedure 'device_init()' unprocessed."
            return(rt,errormsg)
        arglen=len(args)
        errormsg = "Er: Bad parameters."
        if(arglen < 1):
            return(rt,errormsg)
        (rt2, errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''):
            return(rt,errormsg)
        n = int(rt2)
        maxch = self._deviceFirmwareInfo.numberofcounter
        validparams=range(0,maxch,8)
        l=len(validparams)
        if(l<=0):
            errormsg="Er: Unexpected value for numberofcounter %s detected." %(maxch)
            return(rt,errormsg)
        elif(n not in validparams):
            msgvalidparams=[str(i) for i in validparams]
            msg=msgvalidparams[0]
            if(l>1):
                buf=','.join(msgvalidparams[:-1])
                msg='One of ' + buf + ' or ' + msgvalidparams[-1]
            errormsg="Er: Bad parameters. %s is valid." %(msg)
            return(rt,errormsg)
        rt = cmd + ' %02d' %(n)
        return(rt,errormsg)

    def _checksetinputselection(self,cmd,args):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            errormsg = "Er: Procedure 'device_init()' unprocessed."
            return(rt,errormsg)
        arglen=len(args)
        maxch = self._deviceFirmwareInfo.numberofcounter
        validparams=range(0,maxch,2)
        l=len(validparams)
        if(l<=0):
            errormsg="Er: Unexpected value for numberofcounter %s detected." %(maxch)
            return(rt,errormsg)
        errormsg="Er: Bad parameters."
        ipcmd = args[0].upper()
        ipcmdstr = args[0]
        target = ['ALL']
        if(arglen == 2):
            ipcmd = args[1].upper()
            ipcmdstr = args[1]
            chbuf = args[0].upper()
            m = re.search("^([\d]+)-([\d]+)\Z",chbuf)
            if(m):
                lch = int(m.group(1))
                hch = int(m.group(2))
                if((0<=lch) and (lch<maxch) and (0<=hch) and (hch<maxch)):
                   sq,sr=divmod(lch,2)
                   eq,er=divmod(hch,2)
                   if((sr==0) and (er==1) and (lch<=hch)):
                       pass
                   else:
                       errormsg="Er: Bad parameters. (Channel no. format n1-n2, even for n1, odd for n2 and n1<=n2)"
                       return(rt,errormsg)
                else:
                    errormsg="Er: Bad parameters. (Channel no. from 0 to %d)" %(maxch-1)
                    return(rt,errormsg)
                target = [str(i) for i in range(lch, hch, 2)]
            else:
                (rt2, errormsg) = self._sub_checkisinteger('',args)
                if(rt2 == ''):
                    return(rt,errormsg)
                n = int(rt2)
                if(n not in validparams):
                    msgvalidparams=[str(i) for i in validparams]
                    msg=msgvalidparams[0]
                    if(l>1):
                        buf=','.join(msgvalidparams[:-1])
                        msg='One of ' + buf + ' or ' + msgvalidparams[-1]
                        errormsg="Er: Bad parameters. %s is valid." %(msg)
                        return(rt,errormsg)
                target = [str(n)]
        elif(arglen==1):
            pass
        else:
            errormsg="Er: Bad parameters."
            return(rt,errormsg)
        if(ipcmd in ['TTL_HI']):
            ipcmd = 'THI'
        elif(ipcmd in ['TTL_50']):
            ipcmd = 'T50'
        if(ipcmd in ['THI','T50','NIM']):
            cmds=[ipcmd + ' ' + t for t in target]
            rt = '\t'.join(cmds)
        else:
            errormsg="Er: Bad parameters. '%s'" %(ipcmdstr)
            return(rt,errormsg)
        return(rt,errormsg)

    #********** Checker for Download commands **************
    def _checksetgatesyncdownloadformat(self,cmd,args):
        (rt,errormsg)=self._checkgatesyncdownloadcommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        arglen=len(args)
        rt = ''
        errormsg="Er: Bad parameters."
        maxch = self._deviceFirmwareInfo.numberofchannel
        cmd2 = cmd
        addhex = 'H'
        if(maxch>8):
            cmd2 = cmd2 + 'X'
        if((arglen == 1) or (arglen == 2)):
            if(arglen == 2):
                val = args[1].upper()
                if(val=='H'):
                    pass
                elif(val=='D'):
                    addhex = ''
                else:
                    return(rt,errormsg)
            val = args[0].upper()
            m = re.search("^([\d]+)-([\d]+)\Z",val)
            cmd2 = cmd2 + addhex
            if(m):
                lch = int(m.group(1))
                hch = int(m.group(2))
                if(hch == maxch):
                    hch = hch -1 
                    tm = 1
                if((0<=lch) and (hch<maxch)):
                    if(lch>hch):
                        return(rt,errormsg)
            else:
                try:
                    ch = int(val)
                    if(ch == maxch):
                        return(rt,errormsg)
                    elif((ch >= 0) and (ch < maxch)):
                        lch=ch
                        hch=ch
                    else:
                        return(rt,errormsg)
                except ValueError:
                    return(rt,errormsg)
            if(maxch>8):
                cmd2 = cmd2 + "%02d%02d%02d" %(lch,hch,tm)
            else:
                cmd2 = cmd2 + "%0d%0d%0d" %(lch,hch,tm)
            rt = cmd2
        elif((arglen == 3) or (arglen == 4)):
            if(arglen == 4):
                val = args[3].upper()
                if(val=='H'):
                    pass
                elif(val=='D'):
                    addhex = ''
                else:
                    return(rt,errormsg)
                try:
                    lch = int(args[0])
                    hch = int(args[1])
                    tm  = int(args[2])
                    if((0>lch) and (hch>(maxch-1))):
                        return(rt,errormsg)
                    if((0>hch) and (hch>(maxch-1))):
                        return(rt,errormsg)
                    if(lch>hch):
                        return(rt,errormsg)
                    if((0>tm) and (tm>1)):
                        return(rt,errormsg)
                    if(maxch>8):
                        cmd2 = cmd2 + "%02d%02d%02d"  %(lch,hch,tm)
                    else:
                        cmd2 = cmd2 + "%0d%0d%0d" %(lch,hch,tm)
                except ValueError:
                    return(rt,errormsg)
            rt = cmd2
        return(rt,errormsg)

    def _checksetgatesynctimerdownloadinterval(self,cmd,args):
        (rt,errormsg)=self._checkgatesyncdownloadcommand(cmd,args)
        if(rt == ''):
            return(rt,errormsg)
        rt = ''
        arglen=len(args)
        max = self._deviceFirmwareInfo.get_valuemaximum(cmd)
        errormsg="Undefined command '%s'." %(cmd)
        if(max<0):
            return(rt,errormsg)
        errormsg="Er: Bad parameters."
        if(arglen == 1):
            val=args[0]
            (rt,errormsg)=self._sub_checkvaluerange(val,0,max)
            if(rt != ''):
                return(cmd+"%03d" %(val) ,errormsg)
            
        return(rt,errormsg)

    def _checkgatesyncdownloadcommand(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        errormsg="Er: Unsupported command on this device. (cmd='%s')" %(cmd)
        if(self._deviceFirmwareInfo.is_commandsupported('DOWNLOAD')==False):
            return(rt,errormsg)
        rt = cmd
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
    global gb_DeviceInstance
    global gb_DeviceDownloadInstance
    global gb_EncDeviceInstance
    dc = gb_DeviceInstance

    if(gb_DeviceDownloadInstance is not None):
        b = pyctxdownloader.device_getdownloadflgbusy()
        if(b==1):
            f=stars_getflgbusy(local=True)
            #Changed to busy
            if(f != str(b)):
                stars_setlocalflgbusy(str(b))
            pyctxdownloader.download_interval()
            return
    counter_interval()
    if(gb_EncDeviceInstance is not None):
        pyerxc.interval()

def counter_interval():
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_DeviceDownloadInstance
    global gb_LogDir
    global gb_LogEnable
    global gb_Debug
    global gb_LogLevel
    global gb_DebugLevel

    st = gb_StarsInstance
    dc = gb_DeviceInstance
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

    #Check if device in lock state
    llock=dc.device_getisbusy()
    w = 0
    if((llock)>=1):
        w = 1
    # Return if device in lock state.
    if(w == 1):
       return True

    f=stars_getflgbusy(local=True)

    # Check download is running
    #if(gb_DeviceDownloadInstance is not None):
    #    b = pyctxdownloader.device_getdownloadflgbusy()
    #    if(b==1):
    #        # Busy 
    #        if(f != str(b)):
    #            stars_setlocalflgbusy(str(b))
    #        return

    lst1=dc.get_ismotorrunning()
    b = 0
    if(f == '1'):
        b = 1
    if(lst1>=1):
        b = 1

    # Refresh status.
    flap=now-dc.get_laststatustimestamp()
    if(flap<0):
        flap = 0.10
    if(b == 0):
        finterval = 5
    else:
        finterval = 0.10
    if(flap<finterval):
       return True

    #Refresh status
    rt=stars_getstatus()
    if('Er' in rt):
        destsendstr="Error detected in 'GetStatus'.[%s]" %(rt)
        _outputlog(WARN, destsendstr)
        rt=stars_sendevent(eventmessage='_Msg '+destsendstr)

        return False

    #Recheck status
    llock=dc.device_getisbusy()
    lst1=dc.get_ismotorrunning()
    b = 0
    w = 0
    if(llock>=1):
        w = 1
    # Return if device in lock state.
    if(w == 1):
       return True
    if((lst1)>=1):
        b = 1
    if(b == 1):
        #Changed to busy
        if(f != str(b)):
            stars_setlocalflgbusy(str(b))
    else:
        #Changed to stopped.
        if(f != str(b)):
            stars_setlocalflgbusy(str(b))
            #Send current pos as STARS event if required.
            if(True):
                rt=stars_getvalues("GetValue",[],-1)
                if('Er' in rt):
                    destsendstr="Error detected in 'GetValue'.[%s]" %(rt)
                    _outputlog(WARN, destsendstr)
                    rt=stars_sendevent(eventmessage='_Msg '+destsendstr)
                    return False
                lpos=rt
                stars_setlocalvalue(str(lpos))
    return True

##################################################################
# Callback functions:
##################################################################
## Device raw command control handler:
## Device socket handler: DETECT

def device_sockhandler(sock, tm='', printflg=True):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_DeviceDownloadInstance
    global gb_EncDeviceInstance
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
            if(gb_DeviceDownloadInstance):
                pyctxdownloader.device_checkgateisrunning(rt)
            if(gb_EncDeviceInstance is not None):
                pyerxc.device_replyanalyzer(rt,printflg)
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
    return(False)

## STARS socket handler
def handler(allmess,sock):
    global gb_EncDeviceInstance

    if allmess == '':
        st.terminateMainloop()
        return

    if(gb_EncDeviceInstance is not None):
        checknodename = pyerxc.gb_StarsInstance.nodename
        if((allmess.nodeto==checknodename) or allmess.nodeto.startswith(checknodename+".")):
            pyerxc.handler(allmess,sock)
            return
    sub_mainhandler(allmess,sock)
    return

def sub_mainhandler(allmess,sock):
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
                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
         ##elif((gb_DeviceInstance is not None) and (channelname != '') and (channelname in gb_EncChannelNameList)):
         #elif((gb_EncDeviceInstance is not None) and (channelname != '') and (channelname in gb_EncChannelNameList)):
         #   address = gb_EncChannelNameList[channelname]
         #   rt = pyerxc.sub_channelhandler(command, parameters, channelname, address)
         #   if(rt != ''):
         #       destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
         else:
            if(message.startswith('@')==True):
                return
            elif(message.startswith('_')==True):
                return
            else:
                rt = "Er: Bad node. '%s'" %(channelname)
                destsendstr = st.nodename + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
    elif(allmess.nodeto == st.nodename):
        dobjmt = stars_devicecommandobject('CH',   command)
        dobjgb = stars_devicecommandobject('CTL',  command)
        rt2 = sub_commonhandler(command, parameter)
        if(gb_DeviceDownloadInstance):
            rt = pyctxdownloader.sub_downloaderhandler(allmess,sock)
            if(rt != ''):
                destsendstr = rt
        rt = ''
        if(destsendstr != ''):
            pass
        elif(message.startswith('@')==True):
            return
        elif(message.startswith('_')==True):
            return
        elif(rt2 != ''):
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' '+rt2
        elif(command == 'SendRawCommand' and len(parameters) > 0):
            if(st._devicerawenable):
                cmd=allmess.parameters.strip()
                dc.device_send(cmd);
                rt=dc.receive(0.05);
                if(rt == ''):
                    if('?' not in cmd):
                        rt = 'Ok:'
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
        elif(message in ['listnodes', 'GetChannelList', 'GetCounterList']):
            rt=','.join(gb_ChannelNameList.keys())
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message in ['GetNumberOfChannels','GetNumberOfCounters','GetNumberOfEncoders']):
            rt = stars_getcustominfo(message)
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + str(rt)
        elif(message == 'IsBusy'):
            rt = str(stars_getflgbusy(True))
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message == 'Stop'):
            if(gb_DeviceDownloadInstance is not None):
                pyctxdownloader.device_downloadstop(st,'STOP')
            rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,command,parameters,[])
            if('Er:' not in rt):
                rt = 'Ok:'
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #### Global command: "Concept standby" ignored.
        elif(dobjgb is not None):
            rt = 'Er: Bad parameters.'
            addrlist=[]
            channelnamelist=[]
            argnum      =dobjgb.argnum
            ischeckcargnum=dobjgb.ischeckargnum
            isallowbusy =dobjgb.isallowbusy
            ismotion=dobjgb.ismotioncommand
            islock=dobjgb.islockcommand
            if((ischeckcargnum == False) or (ischeckcargnum and len(parameters)==argnum)):
                rt = 'Ok:'
                if(isallowbusy==False):
                    b=stars_getflgbusy(True)
                    if(b=="1"):
                        rt = 'Er: Busy.'
                if('Er:' not in rt):
                    if(command in ['GetValue','IsOverflow','GetCountInputSignalSelection']):
                        id = "-1"
                        rt = stars_getvalues(command,parameters,id)
                    else:
                        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,command,parameters,addrlist)
                if('Er:' not in rt):
                    if((ismotion==True) or (islock==True)):
                        stars_setlocalflgbusy("1")
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #### Channel command + Logic for SingleValue
        elif((dobjmt is not None) and (gb_StarsIsUseGetMultiValues == False)):
            rt = 'Er: Bad parameters.'
            argnum  = dobjmt.argnum
            ischeckcargnum=dobjmt.ischeckargnum
            if((ischeckcargnum == False and len(parameters)>=1) or (ischeckcargnum and len(parameters) == (argnum + 1))):
                val = parameters[0]
                parameters.pop(0)
                rt = "Er: Bad motor name or number. '%s'" %(val)
                channelname = ''
                if(val in gb_ChannelNameList):
                    channelname = val
                elif((max([ord(c) for c in val]) < 128) and (val.isdigit()==True)):
                    num = int(val)
                    if((0 <= num) and (num < len(gb_ChannelNameList.keys()))):
                        channelname = list(gb_ChannelNameList.keys())[num]
                        address = gb_ChannelNameList[channelname]
                if(channelname != ''):
                    address = gb_ChannelNameList[channelname]
                    rt = sub_channelhandler(command, parameters, channelname, address)
            if(rt != ''):
                destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt

        #### Channel command + Logic for MultiValue 
        elif(dobjmt is not None):
            rt = 'Er: Bad parameters.'
            addrlist=[]
            channelnamelist=[]
            argnum  =dobjmt.argnum
            ischeckcargnum=dobjmt.ischeckargnum
            isallowbusy =dobjmt.isallowbusy
            ismotion=dobjmt.ismotioncommand
            if(ischeckcargnum and (len(parameters)==0) and (argnum==0)):
                rt = 'Er: Undefined motors.'
                for chname in gb_ChannelNameList.keys():
                    rt = 'Ok:'
                    if(isallowbusy==False):
                        b=stars_getflgbusy(True)
                        if(b=="1"):
                            rt = 'Er: Busy.'
                            break
                    addrlist.append(gb_ChannelNameList[chname])
                    channelnamelist.append(chname)
                if('Er:' not in rt):
                    if(isstandby()==True):
                        (st,rt)=addsyncruncommand(command,parameters,addrlist,motormamelist,True)
                if('Er:' not in rt):
                    (sts,rt)=addsyncruncommand(command,parameters,addrlist,motormamelist,True)
                    if(sts == True):
                        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL,command,parameters,addrlist,True,isstandby())
                if('Er:' not in rt):
                    if(ismotion == True):
                        for i in range(len(channelnamelist)):
                            stars_setlocalflgbusy(channelnamelist[i],"1")
                    if(isstandby()==True):
                        (st,rt)=addsyncruncommand(command,parameters,addrlist,motormamelist)
            elif(ischeckcargnum and len(parameters)==len(gb_ChannelNameList.keys())):
                rt = 'Er: Undefined motors.'
                for chname,id in gb_ChannelNameList.items():
                    rt = 'Ok:'
                    parameters2=[]
                    channelnamelist=[]
                    rt = 'Ok:'
                    if(argnum==0):
                        if(parameters[i]=='-'):
                           id = -1
                        elif(parameters[i]=='0'):
                           id = -1
                        elif(parameters[i]=='1'):
                            pass
                        else:
                            rt = 'Er: Bad parameters.'
                            break
                    elif(argnum==1):
                        if(parameters[i]=='-'):
                            id = -1
                        parameters2.append(parameters[i])
                    if(id != -1):
                        channelnamelist.append(chname)
                        if(isallowbusy==False):
                            b=stars_getflgbusy(True)
                            if(b=="1"):
                                rt = 'Er: Busy.'
                                break
                    (sts,rt)=addsyncruncommand(command,parameters2,[id],motormamelist,True)
                    if(sts == True):
                        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL,command,parameters,addrlist,True,isstandby())
                
                for id in gb_ChannelNameList.values():
                    addrlist.append(id)
                if(addrlist>0):
                    checklist=[True,False]
                    if(isstandby()==True):
                        checklist=[True]
                    for ischeckonly in checklist:
                        if('Er:' not in rt):
                            if(ismotion == True):
                                stars_setlocalflgbusy(channelname,"1")
                            if(isstandby()==True):
                                (st,rt)=addsyncruncommand(command,parameters,addrlist,ismotion)

                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
        else:
            rt = 'Bad command or parameters.'
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
    else:
        if(message.startswith('@')==True):
            return
        elif(message.startswith('_')==True):
            return
        else:
            rt = "Er: Bad node. '%s'" %(channelname)
            destsendstr = st.nodename + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
    if(destsendstr != ''):
        _outputlog(INFO,'[STARS Send]' + destsendstr)
        rt=st.send(destsendstr)
        if(rt==False):
            st.terminateMainloop()
    return

## STARS socket handler
def sub_channelhandler(command, parameters, channelname, address):
    global gb_DeviceInstance
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
    elif((command == 'IsBusy') and (len(parameters) == 0)):
        rt = str(stars_getflgbusy(True))
    elif(dobjmt is None):
        rt = 'Er: Bad command or parameters.'
    ### Valid command
    else:
        argnum = dobjmt.argnum
        ischeckcargnum=dobjmt.ischeckargnum
        #*** Check parameter num
        if(ischeckcargnum and (len(parameters) != argnum)):
            rt = 'Er: Bad parameters.'
            return(rt)
        isallowbusy = dobjmt.isallowbusy
        ismotion = dobjmt.ismotioncommand
        #*** Pre check if busy
        if(isallowbusy == False):
            rt = 'Er: Busy.'
            b = stars_getflgbusy(True)
            if(b == "1"):
                return(rt)
        #*** Pre standby
        ischeckonly = False
        #*** Exec
        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CHANNEL,command,parameters,[address],True,ischeckonly)
        if('Er:' in rt): return(rt)
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

## STARS set busyflg
def stars_setlocalflgbusy(f, force=False):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_StarsLocalBusyFlg
    st = gb_StarsInstance
    dc = gb_DeviceInstance

    prevf=stars_getflgbusy(local=True)
    gb_StarsLocalBusyFlg['CTL']=f
    f=stars_getflgbusy(local=True)
    if((force==True) or (f is None) or ((f is not None) and (prevf != f))):
        destsendstr=st.nodename+'>System _ChangedIsBusy '+str(f)
        _outputlog(INFO, destsendstr)
        rt=st.send(destsendstr)
    return f

## STARS get busyflg
def stars_getflgbusy(local=False):
    global gb_ChannelNameList
    global gb_DeviceInstance
    global gb_StarsLocalBusyFlg
    dc = gb_DeviceInstance

    if(local==True):
        tag = 'CTL'
        if(tag not in gb_StarsLocalBusyFlg):
            gb_StarsLocalBusyFlg[tag] = ''
        rt = gb_StarsLocalBusyFlg[tag]
    else:
        rt = str(dc.device_getflgbusy())
    return rt

## STARS set current
def stars_setlocalvalue(v, force=False):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_StarsLocalCurrent
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    prevv=stars_getvalue(local=True)
    gb_StarsLocalCurrent['CTL']=v
    v=stars_getvalue(local=True)
    if((force==True) or (v is None) or ((v is not None) and (prevv != v))):
        #destsendstr=st.nodename+'.'+channelname+'>System _ChangedValue '+str(v)
        destsendstr=st.nodename+'>System _ChangedValue '+str(v)
        _outputlog(INFO, destsendstr)
        rt=st.send(destsendstr)
    return v


## STARS get current
def stars_getvalue(local=False):
    global gb_ChannelNameList
    global gb_DeviceInstance
    global gb_StarsLocalCurrent
    dc = gb_DeviceInstance

    if(local==True):
        tag = 'CTL'
        if(tag not in gb_StarsLocalCurrent):
            gb_StarsLocalCurrent[tag] = ''
        rt = gb_StarsLocalCurrent[tag]
    else:
        rt = dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,'GetValue',[],[])
        #rt=dc.get_lastposition(motornostr)
    return rt

def stars_devicecommandobject(level,starscommand,isincludeusehelponly=False):
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    dobj = dc.devicecommandobject(starscommand)
    if(dobj):
        if((isincludeusehelponly==False) and (dobj.ishelponly==True)):
            return(None)
        elif((level == 'ALL') or (level=='CTL')):
            if(dobj.isglobalcommand==True):
                return(dobj)
        elif((level == 'ALL') or (level=='CH')):
            if(dobj.ischannelcommand==True):
                return(dobj)
    return(None)

def stars_getdevicecommandhelpstring(level,starscommand):
    global gb_DeviceInstance
    dc = gb_DeviceInstance

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

def stars_getstatus():
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    rt = dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,'GetStatus',[],[])
    return rt

def stars_postisoverflow(args,rt):
    
    return rt


def stars_getvalues(command,parameters,id):
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    if(dc._deviceFirmwareInfo is None):
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        return(startch,endch,errormsg)
    maxch = dc._deviceFirmwareInfo.numberofchannel
    if(command == 'GetCountInputSignalSelection'):
        maxch = dc._deviceFirmwareInfo.numberofcounter - 1
    (startch,endch,errormsg)=stars_channelargparser(parameters,id,maxch)
    if(startch == -1):
        return(errormsg)
    chnum = endch - startch + 1
    if(command == 'GetValue'):
        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,command,parameters,[id])
        if('Er:' in rt):
            return(rt)
        datas=rt.split(',')
        if(len(datas) == chnum):
            gb_CheckOverflowValue = -1
            if(gb_CheckOverflowValue is not None):
                rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,"IsOverflow",[],[])
                if('Er:' in rt):
                    return(rt)
                datao=rt.split(',')
                if(len(datao)==(maxch+1)):
                    c = 0
                    for i in range(startch,endch+1,1):
                        if(datao[i] == '1'):
                            datas[c] = str(gb_CheckOverflowValue)
                        c = c + 1
                else:
                    return("Unexpected reply. (reply=%s,different number of items between %d and %d)" %(rt,len(datas),chnum))
            rt = ','.join(datas)
            return(rt)
    elif(command == 'IsOverflow'):
        rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,"IsOverflow",[],[id])
        if('Er:' in rt):
            return(rt)
        datao=rt.split(',')
        if(len(datao)==(maxch+1)):
            datas = datao[startch:endch+1]
            rt = ','.join(datas)
            return(rt)
    elif(command == 'GetCountInputSignalSelection'):
        sq,sr=divmod(startch,8)
        eq,er=divmod(endch,8)
        datas=[]
        for n in range(sq, eq+1):
            chstart = n*8
            chend = n*8+7
            rt=dc.exec_command(PyStarsDeviceTSUJICOUNTERTIMERDeviceCommandLevel.CONTROLLER,"GetCountInputSignalSelection",[str(chstart)],[-1])
            #0-7 TTL_Hi,TTL_Hi,TTL_Hi,TTL_Hi,TTL_Hi,TTL_Hi,TTL_Hi,TTL_Hi
            if('Er:' in rt):
                return(rt)
            bufs=rt.split(' ')
            if(len(bufs) == 2):
                if(bufs[0] == str(chstart) + '-' + str(chend)):
                    datao=bufs[1].split(',')
                    if((n == sq) and (n == eq)):
                        datas.extend(datao[sr:er+1])
                    elif(n == sq):
                        datas.extend(datao[sr:])
                    elif(n == eq):
                        datas.extend(datao[:er+1])
                    else:
                        datas.extend(datao)
                else:
                    return("Unexpected reply. (reply=Channel %s to 'IN? %d'))" %(bufs[0], chstart))
            else:
                return("Unexpected reply. (reply=%s)" %(rt))
            
        rt = ','.join(datas)
        return(rt)
    return("Unexpected reply. (reply=%s,different number of items between %d and %d)" %(rt,len(datas),chnum))


def stars_channelargparser(args, id, maxch=None):
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    startch=-1
    endch=-1
    arglen=len(args)
    if(dc._deviceFirmwareInfo is None):
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        return(startch,endch,errormsg)
    if(maxch is None):
        maxch = dc._deviceFirmwareInfo.numberofchannel
    errormsg="Er: Bad parameters."
    val = ''
    if(arglen == 0):
        if(int(id)<0):
            startch = 0
            endch = maxch
            timerch = 1
            return(startch,endch,errormsg)
        else:
            val = id
    else:
        if(int(id)>=0):
            return(startch,endch,errormsg)
        val = args[0].upper()
    m = re.search("^([\d]+)-([\d]+)\Z",val)
    if(m):
        lch = int(m.group(1))
        hch = int(m.group(2))
        tm = 0
        if((0<=lch) and (hch<=maxch)):
            if(lch == hch):
                startch = hch
                endch = hch
            elif(lch<=hch):
                startch = lch
                endch = hch
    elif((val == 'TM') or (val == 'TIMER')):
        startch = maxch
        endch = maxch
    else:
        try:
            ch = int(val)
            if((0<=ch) and (ch<=maxch)):
                startch = ch
                endch = ch
        except ValueError:
            pass
    return(startch,endch,errormsg)

def stars_getcustominfo(command):
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    rt="Er: Unexpected call at stars_getcustominfo('%s')."
    if(command in ['GetNumberOfChannels']):
        rt = dc._deviceFirmwareInfo.numberofchannel
    elif(command in ['GetNumberOfCounters']):
        rt = dc._deviceFirmwareInfo.numberofcounter
    elif(command in ['GetNumberOfEncoders']):
        rt = dc._deviceFirmwareInfo.numberofencoder
    return(rt)

##################################################################
# Define global parameters
##################################################################
# Global parameters.
gb_StarsInstance  = None
gb_DeviceInstance = None
gb_ChannelNameList    = OrderedDict()
gb_StarsLocalBusyFlg   = {}
gb_StarsLocalCurrent   = {}
gb_StarsIsUseGetMultiValues = False  # Do not change

#(Optional) parameters for encoder module
gb_EncDebug = False
gb_EncDeviceInstance = None
gb_NumberOfEncChannels   = 0
gb_EncChannelNameList    = OrderedDict()
gb_EncValueFormulaList = {}
gb_EncValueFormatList  = {}
gb_EncValueAverageCountList  = {}

#(Optional) parameters for downloader module
gb_DeviceDownloadInstance = None

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
# Program pynctx.py
#----------------------------------------------------------------
if __name__ == "__main__":
    ##################################################################
    # Import modules
    ##################################################################
    from pystarslib import pystarsutilconfig, pystarsutilargparser
    import pyerxc
    import pyctxdownloader
    import copy

    # Define: Appliction default parameters
    starsNodeName   = 'nctx'
    starsServerHost = '127.0.0.1'
    starsServerPort = 6057
    deviceHost      = '192.168.1.123'
    devicePort      = 7777

    ##################################################################
    # Define program arguments
    ##################################################################
    optIO=pystarsutilargparser.PyStarsUtilArgParser(numberOfDeviceServer=1,useRawEnable=True,useLogOutputLevel=True,useDebugLevel=True)
    parser=optIO.generate_baseparser(prog=gb_ScriptName,version=__version__)
    parser.add_argument('--channelnamelist', dest="ChannelNameList", help='Name list of counter channels.')
    parser.add_argument('--encoderchannelnamelist', dest="EncoderChannelNameList", help='Name list of encoder channels.(optional,valid if encoder module supported device).')

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
    lc_ChannelNameList=None
    lc_LogDir = gb_LogDir

    lc_EncChannelNameList=None
    lc_OptionList = None

    lc_EncFuncEnable=True
    lc_DownloaderFuncEnable=False
    lc_EncExternalFile=''
    cfgEIO = None
    lc_OptionEList = None

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
            gb_Debug    = cfgIO.get(starsNodeName, 'Debug'          , gb_Debug, bool)
        starsServerHost = cfgIO.get(starsNodeName, 'StarsServerHost', starsServerHost)
        starsServerPort = cfgIO.get(starsNodeName, 'StarsServerPort', starsServerPort, int)
        deviceHost      = cfgIO.get(starsNodeName, 'DeviceHost'     , deviceHost)
        devicePort      = cfgIO.get(starsNodeName, 'DevicePort'     , devicePort, int)
        # Program parameters
        lc_DeviceCommandEnable = cfgIO.get(starsNodeName, 'RawEnable', lc_DeviceCommandEnable, bool)
        lc_ChannelNameList        = cfgIO.get(starsNodeName, 'ChannelNameList'            , lc_ChannelNameList)
        lc_EncChannelNameList     = cfgIO.get(starsNodeName, 'EncoderChannelNameList'     , lc_EncChannelNameList)
        lc_EncFuncEnable = cfgIO.get(starsNodeName, 'EncoderFunctionEnable' , lc_EncFuncEnable)
        lc_DownloaderFuncEnable = cfgIO.get(starsNodeName, 'DownloaderFunctionEnable' , lc_DownloaderFuncEnable)
        lc_EncExternalFile =  cfgIO.get(starsNodeName, 'EncoderExternalConfig' , lc_EncExternalFile)
        try:
            lc_OptionList = cfgIO.gethandle().options(starsNodeName)
        except:
            lc_OptionList = None
        if(gb_Debug==True):
            gb_DebugLevel  = DEBUG
            gb_LogLevel    = DEBUG
        gb_LogLevel = cfgIO.get(starsNodeName, 'LogLevel', gb_LogLevel, int)
        gb_DebugLevel = cfgIO.get(starsNodeName, 'DebugLevel', gb_DebugLevel, int)
        gb_LogEnable = cfgIO.get(starsNodeName, 'LogEnable', gb_LogEnable, bool)
        lc_LogDir = cfgIO.get(starsNodeName, 'LogDir', lc_LogDir)

    # Load if  Encoder external file assigned.
    if(lc_EncExternalFile != ''):
        cfgEIO= pystarsutilconfig.PyStarsUtilConfig(lc_EncExternalFile,gb_Debug)
        if(cfgEIO.gethandle() is None):
            sys.stdout.write(cfgEIO.getlasterrortext()+'\n')
            exit(1)
        lc_EncChannelNameList     = cfgEIO.get(starsNodeName, 'ChannelNameList'     , lc_EncChannelNameList)
        try:
            lc_OptionEList = cfgEIO.gethandle().options(starsNodeName)
        except:
            lc_OptionEList = None

    # Fix optional parameters
    starsServerHost = optIO.get(args.StarsServerHost,starsServerHost)
    starsServerPort = optIO.get(args.StarsServerPort,starsServerPort)
    deviceHost      = optIO.get(args.DeviceHost,deviceHost)
    devicePort      = optIO.get(args.DevicePort,devicePort)
    if(lc_DeviceCommandEnable == False):
        lc_DeviceCommandEnable = optIO.get(args.rawenable,False)
    lc_ChannelNameList        = optIO.get(args.ChannelNameList,            lc_ChannelNameList)
    lc_EncChannelNameList     = optIO.get(args.EncoderChannelNameList,     lc_EncChannelNameList)
    gb_DebugLevel = optIO.get(args.debuglevelnum, gb_DebugLevel)
    gb_LogLevel   = optIO.get(args.loglevelnum, gb_LogLevel)
    if(gb_LogEnable == False):
        gb_LogEnable = optIO.get(args.logenable,False)
    lc_LogDir= optIO.get(args.logdir, lc_LogDir)

    lc_ChannelNameList        = lc_ChannelNameList.split(',')        if(lc_ChannelNameList is not None) else []
    lc_EncChannelNameList     = lc_EncChannelNameList.split(',')     if(lc_EncChannelNameList is not None) else []

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
    dc=PyStarsDeviceTSUJICOUNTERTIMER(deviceHost, devicePort, cmdhandler=devcmdhandler)
    gb_DeviceInstance=dc

    #Set properties for device instance
    dc.setdebug(gb_Debug)
    if(gb_Debug == True): gb_DeviceInstance.printinfo()

    #Connect to device
    rt = dc.connect()
    if(rt==False):
        sys.stdout.write(dc.getlasterrortext()+'\n')
        exit(1)
    cnt=0
    while(True):
        rt=dc.device_receive(1)
        if('Er:' in rt):
            sys.stdout.write(dc.getlasterrortext()+'\n')
        if(rt == ''):
              break
        if(cnt>=100):
            break
        cnt=cnt+1

    #Initialize device variables
    rt=dc.device_init()
    if(rt == False):
        dc.disconnect()
        sys.stdout.write(dc.getlasterrortext()+'\n')
        exit(1)

    if(gb_Debug==True):
        sys.stdout.write("starsNodeName#"+str(starsNodeName)+"#"+'\n')
        sys.stdout.write("starsServerHost#"+str(starsServerHost)+"#"+'\n')
        sys.stdout.write("starsServerPort#"+str(starsServerPort)+"#"+'\n')
        sys.stdout.write("deviceHost#"+str(deviceHost)+"#"+'\n')
        sys.stdout.write("devicePort#"+str(devicePort)+"#"+'\n')
        sys.stdout.write("EncoderFunctionEnable#"+str(lc_EncFuncEnable)+"#"+'\n')
        sys.stdout.write("DownloaderFunctionEnable#"+str(lc_DownloaderFuncEnable)+"#"+'\n')

    ##################################################################
    # Parse channel settings
    ##################################################################
    maxch = dc.device_getnumberofchannel()
    maxcounter = dc.device_getnumberofcounter()
    #Generate default channel name
    prevchi = -1
    chtag='CH'
    for i in range(maxcounter):
        chno=str(i)
        chname=chtag+chno
        if(i<len(lc_ChannelNameList)):
            chname=lc_ChannelNameList[i]
            m = re.search("([\d]+)\Z",chname)
            if(m):
                buf=m.group(1)
                if(len(chname)>len(buf)):
                    chtag=chname[0:len(chname)-len(buf)]
                prevchi = int(m.group(1))
        elif(prevchi != -1):
            prevchi = prevchi + 1
            chname=chtag+str(prevchi)
        if(chname in gb_ChannelNameList.keys()):
            dc.disconnect()
            sys.stdout.write("Channel name duplicate error '%s'.\n" %(chname))
        gb_ChannelNameList[chname] = '%02d' % (int(chno))

    ##########################################################################
    # Optional check if encoder module support then parse settings of encoder 
    ##########################################################################
    encnum=dc.device_getnumberofencoder()
    if(encnum<=0):
        lc_EncFuncEnable=False
    #if(encnum>0):
    if(lc_EncFuncEnable==True):
        for i in range(encnum):
            encno=str(i)
            encname='ENC'+encno
            if(i<len(lc_EncChannelNameList)):
                encname=lc_EncChannelNameList[i]
            chi = maxcounter+i
            chno=str(chi)
            chname=chtag+chno
            if(chi<len(lc_ChannelNameList)):
                chname=lc_ChannelNameList[chi]
                m = re.search("([\d]+)\Z",chname)
                if(m):
                    buf=m.group(1)
                    if(len(chname)>len(buf)):
                        chtag=chname[0:len(chname)-len(buf)]
                    prevchi = int(m.group(1))
            elif(prevchi != -1):
                prevchi = prevchi + 1
                chname=chtag+str(prevchi)
                if(i<len(lc_EncChannelNameList)):
                    chname=encname
            elif(i<len(lc_EncChannelNameList)):
                chname=encname
            if(chname in gb_ChannelNameList.keys()):
                dc.disconnect()
                sys.stdout.write("Channel name duplicate error '%s'.\n" %(chname))
            gb_ChannelNameList[chname] = '%02d' % (int(chno))
            gb_EncChannelNameList[encname] = '%02d' % (int(encno))

        for chname in gb_EncChannelNameList.keys():
            if(lc_OptionList is None):
                gb_EncValueFormulaList[chname] = ''
                gb_EncValueFormatList[chname]  = ''
                gb_EncValueAverageCountList[chname]  = 1
                continue
            gb_EncValueFormulaList[chname] = cfgIO.get(starsNodeName, chname+'.Formula'     , '')
            gb_EncValueFormatList[chname]  = cfgIO.get(starsNodeName, chname+'.Format'      , '')
            gb_EncValueAverageCountList[chname]  = cfgIO.get(starsNodeName, chname+'.AverageCount'      , 1, int)
            if(cfgEIO is not None):
                gb_EncValueFormulaList[chname] = cfgEIO.get(starsNodeName, chname+'.Formula', gb_EncValueFormulaList[chname])
                gb_EncValueFormatList[chname]  = cfgEIO.get(starsNodeName, chname+'.Format', gb_EncValueFormatList[chname] )
                gb_EncValueAverageCountList[chname]  = cfgEIO.get(starsNodeName, chname+'.AverageCount', gb_EncValueAverageCountList[chname] , int)
            if(gb_EncValueFormulaList[chname] != ''):
                if(cfgEIO is not None):
                    for key in sorted(lc_OptionEList,reverse=True):
                        val = cfgEIO.get(starsNodeName,  key     , '')
                        lchname=chname.lower()
                        if(key.startswith(lchname+".")):
                            key2 = key.replace(lchname+".","").upper()
                            gb_EncValueFormulaList[chname] = gb_EncValueFormulaList[chname].replace(key2,val)

                for key in sorted(lc_OptionList,reverse=True):
                    #print("key "+ str(key))
                    val = cfgIO.get(starsNodeName,  key     , '')
                    lchname=chname.lower()
                    if(key.startswith(lchname+".")):
                        key2 = key.replace(lchname+".","").upper()
                        gb_EncValueFormulaList[chname] = gb_EncValueFormulaList[chname].replace(key2,val)

        gb_NumberOfEncChannels = encnum

        if(gb_Debug==True):
            sys.stdout.write("numberOfEncoderChannels#"+str(encnum)+"#"+'\n')
            sys.stdout.write("EncoderChannelNameList#"+str(gb_EncChannelNameList)+"#"+'\n')
            for i in range(encnum):
                chname=list(gb_EncChannelNameList.keys())[i]
                sys.stdout.write(chname+".formula#"     +str(gb_EncValueFormulaList[chname])+"#"+'\n')
                sys.stdout.write(chname+".format#"      +str(gb_EncValueFormatList[chname])+"#"+'\n')
                sys.stdout.write(chname+".averagecount#"+str(gb_EncValueAverageCountList[chname])+"#"+'\n')

        # Set program setting parameters to pyerxc globals.
        pyerxc.gb_NumberOfChannels = gb_NumberOfEncChannels
        pyerxc.gb_ChannelNameList = gb_EncChannelNameList

        # Define: Encoder calc parameters
        pyerxc.gb_ValueFormulaList = gb_EncValueFormulaList
        pyerxc.gb_ValueFormatList = gb_EncValueFormatList
        pyerxc.gb_ValueAverageCountList = gb_EncValueAverageCountList

        pyerxc.gb_Debug = gb_Debug
        
        # Connect to encoder module
        #Create device instance for encoder
        gb_EncDeviceInstance=pyerxc.PyStarsDeviceTSUJIENCODER(deviceHost, devicePort)
        gb_EncDeviceInstance.setdebug(gb_Debug)
        gb_EncDeviceInstance.readable   = dc.readable
        gb_EncDeviceInstance.s          = dc.s
        #Initialize device variables
        rt=gb_EncDeviceInstance.device_init()
        if(rt == False):
            sys.stdout.write(gb_EncDeviceInstance.getlasterrortext()+'\n')
            dc.disconnect()
            exit(1)
        if(gb_Debug): gb_EncDeviceInstance.printinfo()
        pyerxc.gb_DeviceInstance = gb_EncDeviceInstance

    # Genetate chname:last
    for i in range(maxcounter+encnum,maxch+1):
        chno=str(i)
        chname=chtag+chno
        if(i<len(lc_ChannelNameList)):
            chname=lc_ChannelNameList[i]
            m = re.search("([\d]+)\Z",chname)
            if(m):
                buf=m.group(1)
                if(len(chname)>len(buf)):
                    chtag=chname[0:len(chname)-len(buf)]
        elif(i == maxch and ('TMR' not in gb_ChannelNameList.keys())):
            chname='TMR'
        elif(prevchi != -1):
            prevchi = prevchi + 1
            chname=chtag+str(prevchi)
        if(chname in gb_ChannelNameList.keys()):
            dc.disconnect()
            sys.stdout.write("Channel name duplicate error '%s'.\n" %(chname))
            exit(1)
        gb_ChannelNameList[chname] = '%02d' % (int(chno))

    if(gb_Debug==True):
        sys.stdout.write("numberOfChannels#"+str(maxch)+"#"+'\n')
        sys.stdout.write("ChannelNameList#"+str(gb_ChannelNameList.keys())+"#"+'\n')

    ##########################################################################
    # Optional check if download func support then generate instance 
    ##########################################################################
    #if(dc.device_isdownloadsupported()):
    if(dc.device_isdownloadsupported()==False):
        lc_DownloaderFuncEnable=False
    #if(dc.device_isdownloadsupported()):
    if(lc_DownloaderFuncEnable):
        pyctxdownloader.gb_Debug = gb_Debug

        gb_DeviceDownloadInstance = pyctxdownloader.PyStarsDeviceTSUJICOUNTERTIMERDOWNLOADER(deviceHost, devicePort)
        gb_DeviceDownloadInstance.setdebug(gb_Debug)

        rt=gb_DeviceDownloadInstance.connect()
        if(rt==False):
            sys.stdout.write(gb_DeviceDownloadInstance.getlasterrortext()+'\n')
            dc.disconnect()
            exit(1)
        if(gb_Debug == True): gb_DeviceDownloadInstance.printinfo()

        rt=gb_DeviceDownloadInstance.device_init()
        if(rt == False):
            sys.stdout.write(gb_DeviceDownloadInstance.getlasterrortext()+'\n')
            if(gb_DeviceDownloadInstance):
                gb_DeviceDownloadInstance.disconnect()
            dc.disconnect()
            exit(1)
        pyctxdownloader.gb_DeviceDownloadInstance = gb_DeviceDownloadInstance
        pyctxdownloader.device_checkstopdelay()

        #Set device instance for ctxdownloader
        pyctxdownloader.gb_DeviceInstance = copy.copy(gb_DeviceInstance)

    ##################################################################
    # Connect to stars
    ##################################################################
    st  = StarsInterface(starsNodeName, starsServerHost, '', starsServerPort)
    gb_StarsInstance = st

    #Set properties for Stars instance
    setDebug(gb_Debug)
    st._devicerawenable = lc_DeviceCommandEnable
    st._isloggererrordetectedtimes=0

    rt = st.setdefaultreceivetimeout(3)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        if(gb_DeviceDownloadInstance):
            gb_DeviceDownloadInstance.disconnect()
        dc.disconnect()
        exit(1)

    #Connect to Stars
    rt=st.connect()
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        if(gb_DeviceDownloadInstance):
            gb_DeviceDownloadInstance.disconnect()
        dc.disconnect()
        exit(1)
    
    # setup enc module if use.
    if(encnum>0):
        pyerxc.gb_StarsInstance = copy.copy(st)
        pyerxc.gb_StarsInstance.nodename = st.nodename + '.enc'

    # setup downloader module if use.
    if(gb_DeviceDownloadInstance):
        pyctxdownloader.gb_StarsInstance = copy.copy(st)
        pyctxdownloader.gb_StarsInstance.nodename = st.nodename
        gb_DeviceDownloadInstance.start_nb_handler(pyctxdownloader.device_recvdatahandler)

    #Add callback handler
    rt=st.addcallback(handler)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        if(gb_DeviceDownloadInstance):
            gb_DeviceDownloadInstance.disconnect()
        dc.disconnect()
        st.disconnect()
        exit(1)
    rt=st.addcallback(device_sockhandler,dc.gethandle(),'DETECT')
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        if(gb_DeviceDownloadInstance):
            gb_DeviceDownloadInstance.disconnect()
        dc.disconnect()
        st.disconnect()
        exit(1)
    st.send('System flgon '+st.nodename+'._Alert')

    _outputlog(WARN,"*** start transaction. ***")

    #Start Mainloop()
    try:
        rt=st.Mainloop(interval,0.01)
        if(gb_DeviceDownloadInstance):
            gb_DeviceDownloadInstance._callbackrunning = False
        if(rt==False):
            sys.stdout.write(st.getlasterrortext()+'\n')
    except Exception as e:
        pass

    _outputlog(WARN,"*** Normal end transaction. ***\n")

    #Device close
    #*** sleep for callback terminate wait
    time.sleep(1)
    if(gb_DeviceDownloadInstance):
        time.sleep(1)
        gb_DeviceDownloadInstance.disconnect()
    _outputlog(WARN,"*** Bye device. ***\n")
    st.removecallback(dc.gethandle())
    dc.disconnect()
    #st.removecallback()
    #Close sessions
    st.disconnect()
    _outputlog(WARN,"*** Bye STARS. ***\n")
    time.sleep(0.1)
    exit(0)
