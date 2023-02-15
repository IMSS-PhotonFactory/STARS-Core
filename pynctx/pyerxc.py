 #!/usr/bin/python3
"""
  STARS python program Tsuji Electronics Co.,Ltd. Encoder control
    Description: Connect to STARS server and commnicate with the device.
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
import math
from collections import OrderedDict,defaultdict
from singlestars import StarsInterface
from stars import StarsMessage

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJIENCODERFirmwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJIENCODERFirmwareInfo(str):
    """ PyStarsDeviceTSUJIENCODERFirmwareInfo: Encoder device info object.
    """
    def __init__(self, versionstr):
        self.versiondetected = False
        self.version = versionstr
        self.version_no   = 0
        self.version_date = ''
        self.device_name  = ''
        self.numberofchannel = 2
        self.digitnum = 7
        self.is_supported = {}
        self.value_maximum = {}
        self.value_minimum = {}
        self.value_maximum['PRESET']  = 8388607
        self.value_minimum['PRESET']  =-8388607
        self.is_supported['VERH']    = False
        self.is_supported['ZSET']    = False
        self.is_supported['SCALE']   = False
        self.is_supported['ENCSET']  = False
        self.is_supported['ENCSYNCTRGOUT']  = False
        self.has_error = True
        self.error = 'Uninitialized'
        m = re.search("^(\S+)\s+(\S+)\s+(\S+)\Z", versionstr)
        if m:
            try:
                self.version_no   = float(m.group(1))
                self.version_date = m.group(2)
                self.device_name  = m.group(3)
                m = re.search('^ER(2|4|x)C-04',self.device_name)
                if(m):
                    self.versiondetected = True
                    if(m.group(1) == 'x'):
                        self.versiondetected = False
                    else:
                        self.numberofchannel = int(m.group(1))
                    if(self.version_no >= 1.02):
                        self.is_supported['VERH'] = True
                        self.is_supported['ZSET'] = True
                    if(self.version_no >= 1.03):
                        self.digitnum = 10
                        self.value_maximum['PRESET']  = 2147483647
                        self.value_minimum['PRESET']  =-2147483648
                        self.is_supported['SCALE']   = True
                    self.has_error = False
                else:
                    m = re.search('^CT\d+-ER(\d+)',self.device_name)
                    if(m):
                        self.numberofchannel = int(m.group(1))
                        self.is_supported['VERH']  = True
                        self.is_supported['ZSET']  = True
                        m = re.search('^CT\d+-ER(\d+)T',self.device_name)
                        if(m):
                            self.is_supported['ENCSYNCTRGOUT']  = True
                        self.digitnum = 10
                        self.value_maximum['PRESET']  = 2147483647
                        self.value_minimum['PRESET']  =-2147483648
                        self.is_supported['SCALE']    = True
                        self.is_supported['ENCSET']   = True
                        self.has_error = False
                        self.versiondetected = True
                    else:
                        self.has_error = False
                        self.error = 'Unknown firmware version. (%s)' %(self.device_name)
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

    #---------------------------------------------
    # ENCSET COMMAND
    #---------------------------------------------
    def is_encodersetcommandsupported(self):
        return(self.is_supported['ENCSET'])

    def get_getencodersetcommand(self, ch):
        return('S2'+str(ch*2)+'S?')

    #---------------------------------------------
    # SCALE COMMAND
    #---------------------------------------------
    def is_scalecommandsupported(self):
        return(self.is_supported['SCALE'])

    def get_getscalevaluecommand(self, ch):
        return('D'+chr(65+ch))

    def get_setscaleoffsetcommand(self, ch, offset=0):
        min = -2147483647
        max =  2147483647
        val = offset
        if((val>max) or (val<min)):
            self.error = 'Invalid value range (range: %d - %d).' %(min,max)
            return('')
        return('OW'+chr(65+ch)+'%+011d' %(val))

    def get_getscaleoffsetcommand(self, ch):
        return('OR'+chr(65+ch))

    def get_setscalemultipliercommand(self, ch, multiplier=1):
        amin =    0.000001
        amax =  999.999999
        nmin = -999.999999
        nmax =   -0.000001
        val = multiplier
        if(val>=0):
            if((val>amax) or (val<amin)):
                self.error = 'Invalid value range (range: +-%lf - %lf)' %(amin,amax)
                return('')
        else:
            if((val>nmax) or (val<nmin)):
                self.error = 'Invalid value range (range: +-%lf - %lf)' %(amin,amax)
                return('')
        return('MW'+chr(65+ch)+'%+011.6f' %(val))

    def get_getscalemultipliercommand(self, ch):
        return('MR'+chr(65+ch))

    #---------------------------------------------
    # Z COMMAND
    #---------------------------------------------
    def is_zsetcommandsupported(self):
        return(self.is_supported['ZSET'])

    def get_setzsetcommand(self, ch, startstop=True):
        b=str(startstop).upper()
        if((b == 'TRUE') or (b == '1') or (b == 'C')):
            return('ZC'+chr(65+ch))
        return('ZN'+chr(65+ch))

    def get_setztimingcommand(self, ch, updown=True):
        b=str(updown).upper()
        if((b == 'TRUE') or (b == '1') or (b == 'U')):
            return('ZT'+chr(65+ch)+'U')
        return('ZT'+chr(65+ch)+'D')

    def get_getzstatuscommand(self, ch):
        return('ZS'+chr(65+ch))

    #---------------------------------------------
    # VALUE COMMAND
    #---------------------------------------------
    def get_getvaluecommand(self, ch):
        if(self.digitnum == 7):
            return('S2'+str(ch*2))
        elif(self.digitnum == 10):
            return('S3'+str(ch*2))
        self.error = 'Unsupported digitnum %d.' %(self.digitnum)
        return('')

    def get_presetcommand(self, ch, count):
        min = self.value_minimum['PRESET']
        max = self.value_maximum['PRESET']
        val = count
        if((val>max) or (val<min)):
            self.error = 'Invalid value range (range: %d - %d)' %(min,max)
            return('')
        if(self.digitnum == 7):
            return('S'+chr(65+ch)+'%+08d' %(val))
        elif(self.digitnum == 10):
            return('S'+chr(65+ch)+'%+011d' %(val))
        self.error = 'Unsupported digitnum %d.' %(self.digitnum)
        return('')

    #---------------------------------------------
    # ENCSYNCTRIGGER COMMAND
    #---------------------------------------------
    def is_encsynctriggeroutcommandsupported(self):
        return(self.is_supported['ENCSYNCTRGOUT'])

    def get_setencodersynctriggerenablecommand(self, ch, enflg=True):
        b=str(enflg).upper()
        if((b == 'TRUE') or (b == '1') or (b == 'E')):
            return('E'+chr(65+ch)+'TE')
        return('E'+chr(65+ch)+'TD')

    def get_getencodersynctriggerenablecommand(self, ch):
        return('E'+chr(65+ch)+'T?')

    def get_setencodersynctriggercountcommand(self, ch, count):
        min =-9999999999
        max = 9999999999
        val = count
        if((val>max) or (val<min)):
            self.error = 'Invalid value range (range: %d - %d)' %(min,max)
            return('')
        return('E'+chr(65+ch)+'TC'+'%+11d' %(val))

    def get_getencodersynctriggercountcommand(self, ch):
        return('E'+chr(65+ch)+'TC?')

    def get_getencodersynctriggerinternalcountcommand(self, ch):
        return('E'+chr(65+ch)+'TCC?')

    def get_setencodersynctriggerpulsewidthcommand(self, count):
        min = 10
        max = 1000
        val = count
        if((val>max) or (val<min)):
            self.error = 'Invalid value range (range: %d - %d (microseconds))' %(min,max)
            return('')
        val2 = str(count)
        if(val2[-1:]!="0"):
            self.error = 'value must be multiples of 10.'
            return('')
        return('ENCTW'+'%d' %(val))

    def get_getencodersynctriggerpulsewidthcommand(self):
        return('ENCTW?')

    def get_setencodersynctriggerpolaritycommand(self, polflg=True):
        b=str(polflg).upper()
        if((b == 'TRUE') or (b == '1') or (b == 'POS')):
            return('ENCTPPOS')
        return('ENCTPNEG')

    def get_getencodersynctriggerpolaritycommand(self):
        return('ENCTP?')


#----------------------------------------------------------------
# Class PyStarsDeviceTSUJIENCODERHardwareInfo
#----------------------------------------------------------------
class PyStarsDeviceTSUJIENCODERHardwareInfo(str):
    """ PyStarsDeviceTSUJIENCODERHardwareInfo: Encoder device hardware info object.
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
# Class PyStarsDeviceTSUJIENCODERStatus
#----------------------------------------------------------------
class PyStarsDeviceTSUJIENCODERStatus(str):
    """ PyStarsDeviceTSUJIENCODERStatus: Encoder status object.
    """
    def __init__(self, statusstr):
        self.status = statusstr
        self.has_error = True
        self.error = ''
        self.channel_no = -1
        self.zset_running = -1
        self.zset_cleartiming = ''
        m = re.search("^Z(\S)([CN])([UD])\Z", statusstr.upper())
        if m:
            try:
                no = ord(m.group(1)) - 65
                if(no>=0):
                    self.channel_no = no
                    buf = m.group(2)
                    if(buf == 'C'):
                        self.zset_running = 1
                    else:
                        self.zset_running = 0
                    buf = m.group(3)
                    self.zset_cleartiming = buf
                    self.has_error = False
                else:
                    rt="Analyzing status failure ('%s'). (Unknown channel:%d)" %(statusstr,no)
                    self.error = "%s" %(rt)
            except:
                rt="Analyzing status failure ('%s'). (%s)" %(statusstr, type(e))
                self.error = "%s" %(rt)
        else:
            rt="Status reply error ('%s'). Unexpected reply format." %(statusstr)
            self.error = "%s" %(rt)

#----------------------------------------------------------------
# Class PyStarsDeviceTSUJIENCODERDeviceCommand
#----------------------------------------------------------------
class PyStarsDeviceTSUJIENCODERDeviceCommandLevel():
    """ PyStarsDeviceTSUJIENCODERDeviceCommandLevel: Target codelist of device command.
    """
    CONTROLLER, CHANNEL = range(1,3)

class PyStarsDeviceTSUJIENCODERDeviceCommand():
    """ PyStarsDeviceTSUJIENCODERDeviceCommand: Device command object.
    """
    def __init__(self, commandtag, ishelponly=False, ischannelcommand=True, isglobalcommand=False, islockcommand=False, isunlockcommand=False, isreferencecommand=True, ismotioncommand=False, argnum = 0, replytag=None, isallowbusy=True, checkfunc=None, postfunc=None, postwaittime=0, helpstring="-"):
        self.commandtag  = commandtag
        self.ishelponly = ishelponly
        self.ischannelcommand = ischannelcommand
        self.islockcommand = islockcommand
        self.isunlockcommand = isunlockcommand
        self.isglobalcommand = isglobalcommand
        self.isreferencecommand = isreferencecommand
        self.ismotioncommand = ismotioncommand
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

class PyStarsDeviceTSUJIENCODER(nportserv.nportserv):
    """ Class PyStarsDeviceTSUJIENCODER: Derived from nportserv to control the device.
    """
    ##################################################################
    # Device control functions
    ##################################################################
    ## Device send
    def device_send(self,cmd):
        if(self.isconnected()==False):
            return 'Er: Disconnected'
        rt=self.send(cmd)
        if(rt==False):
            return 'Er: ' + dc.getlasterrortext()
        self._deviceCommandLastExecutedTime['LATEST'] = time.time()
        return 'Ok:'

    ## Device act
    def device_act(self,cmd,timeout=''):
        rt=self.device_send(cmd)
        if('Er:' in rt):
            return(rt)
        rt=self.device_receive(timeout)
        return rt

    ## Device recv
    def device_receive(self,timeout=''):
        if(self.isconnected()==False):
            return 'Er: Disconnected'
        if(timeout==''):
            timeout=self.gettimeout()
        rt=self.receive(timeout)
        if(rt is None):
            return 'Er: ' + self.getlasterrortext()
        #self._deviceCommandLastExecutedTime['LASTEST'] = time.time()
        return rt

    def device_init(self):
        rt = False
        max_chno = 0
        if(self._deviceFirmwareInfo is None):
            rt2 = self.device_act('VER?')
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            elif(rt2 == ''):
                rt2 = PyStarsDeviceTSUJIENCODERFirmwareInfo('')
                self._deviceFirmwareInfo = rt2
            else:
                rt2 = PyStarsDeviceTSUJIENCODERFirmwareInfo(rt2)
                if(rt2.has_error):
                    self.error = 'Er: %s' %(rt2.error)
                    return(rt)
                self._deviceFirmwareInfo = rt2
                max_chno = rt2.numberofchannel
        #Undetected version: try to detect number of channel
        if(self._deviceFirmwareInfo.versiondetected == False):
            #Test-read chB
            cmd = self._deviceFirmwareInfo.get_getvaluecommand(1)
            if(cmd == ''):
                self.error = 'Er: %s' %(self._deviceFirmwareInfo.error)
                return(rt)
            rt2 = self.device_act(cmd)
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            self._deviceFirmwareInfo.numberofchannel = 2
            #Test-read chD
            cmd = self._deviceFirmwareInfo.get_getvaluecommand(3)
            rt2 = self.device_act(cmd)
            if('Er:' in rt2):
                self.error = rt2
                return(rt)
            elif(rt2 == ''):
                pass
            else:
                self._deviceFirmwareInfo.numberofchannel = 4
            max_chno = self._deviceFirmwareInfo.numberofchannel
        if(self._deviceHardwareInfo is None):
            self._deviceHardwareInfo = PyStarsDeviceTSUJIENCODERHardwareInfo('')
            if(self._deviceFirmwareInfo.is_commandsupported('VERH') == True):
                rt2 = self.device_act('VERH?')
                if('Er:' in rt2):
                    self.error = rt2
                    return(rt)
                elif(rt2 == ''):
                    self._deviceFirmwareInfo.set_commandsupported('VERH', False)
                else:
                    rt2 = PyStarsDeviceTSUJIENCODERHardwareInfo(rt2)
                    if(rt2.has_error):
                        self.error = 'Er: %s' %(rt2.error)
                        return(rt)
                    self._deviceHardwareInfo = rt2
        #Read status
        for i in range(max_chno):
            cmd = self._deviceFirmwareInfo.get_getzstatuscommand(i)
            rt2 = self.device_act(cmd)
            if('Er' in rt2):
                self.error = rt2
                return(rt)
            rt2 = PyStarsDeviceTSUJIENCODERStatus(rt2)
            if(rt2.has_error):
                self.error = 'Er: %s' %(rt2.error)
                return(rt)
            self._deviceLastStatus[i] = rt2
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
    def devicecommandobject(self,starscommand):
        rt = None
        if(starscommand in self._deviceSTARSCommand):
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
        elif(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CONTROLLER):
            if(dobj.isglobalcommand == False):
                return("Er: Command not found. (func='exec_command', level=%s, starscommand=%s)" %(str(level),starscommand))
            if(len(addrlist) <= 0):
                addrlist = [-1]
        elif(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL):
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
                    if(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL):
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
                    if(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL):
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
            b = self.device_getisbusy()
            if(b == 1):
                return('Er: Busy.')
            self._device_setisbusy(0)
            for i in range(len(addrlist)):
                id = addrlist[i]
                id = '%02d' % int(id)
                if(int(id) >= 0):
                    if(cisallowbusy == False):
                        b = self.device_getflgbusy(id)
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
                    if(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CONTROLLER):
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

                if(level == PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL):
                    devcommand = devcommandtag[i]
                    replytag = replytagI[i]
                else:
                    devcommand = devcommandtag[i]
                    replytag = replytagI[i]

                if(devcommandtag[i] == ''):
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
                            rt3=self.device_receive(0.005)
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
    def device_getnumberofchannel(self):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        return(self._deviceFirmwareInfo.numberofchannel)

    def device_getvalue(self,channelnostr,averagecount=1,formula='',replyformat=''):
        rt = ''
        if(self._deviceFirmwareInfo is None):
            rt = "Er: Procedure 'device_init()' unprocessed."
            return(rt)
        c = 0
        cval = 0
        for i in range(averagecount):
            rt = self.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL,'GetRawValue',[],[channelnostr])
            if('Er:' in rt):
                return(rt)
            cval = cval + int(rt)
            c = c + 1
        if(c <= 0):
            rt = "No data. (averagecount:%d)" %(averagecount)
            return(rt)
        val = int(cval / c)
        valbuf = str(val)
        self._debugprint("get_value: calc(average) %lf : %d / %d\n" %(val, cval, c))

        if(formula != ''):
            cbuf = formula.replace("INPUT",str(val))
            val = eval(cbuf)
            valbuf = str(val)
            self._debugprint("get_value: calc(formula) %lf : %s\n" %(val, cbuf))
        if(replyformat != ''):
            valbuf = replyformat %(val)
            if(valbuf.startswith('-')):
                try:
                    if(float(valbuf) == 0.0):
                        valbuf = valbuf.replace('-','',1)
                except:
                    pass
            self._debugprint("get_value: calc(format) %lf using %s\n" %(val, replyformat))
        return(valbuf)

    def device_getlastencoderstatustimestamp(self,channelnostr):
        chstr=str(int(channelnostr))
        if('ENCSTATUS'+chstr in self._deviceCommandLastExecutedTime):
            return(self._deviceCommandLastExecutedTime['ENCSTATUS'+chstr])
        return(0)
       
    ## Device set busyflg
    def device_getflgbusy(self,channelnostr):
        b = self.device_getisbusy()
        if(b > 0):
           return(1)
        rt = self.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL,'GetEncoderStatus',[],[channelnostr])
        b = self._deviceLastStatus[int(channelnostr)].zset_running
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

    ##################################################################
    # Initialize
    ##################################################################
    def __init__(self, deviceHost, devicePost, inthandler=None):
        self._deviceInstance = nportserv.nportserv.__init__(self, deviceHost, devicePost)
        self.setdelimiter('\n')
        self.setdelimiter('\r\n')
        self.settimeout(2)

        ##################################################################
        # Define command definitions
        ##################################################################
        lc_deviceSTARSCommand = {}

        #Define Info returns parameters.(config)
        lc_deviceSTARSCommand['GetFirmwareVersion']   = PyStarsDeviceTSUJIENCODERDeviceCommand('VER?',  isglobalcommand=True, helpstring="Return the controller firmware version string.")
        lc_deviceSTARSCommand['GetHardwareVersion']   = PyStarsDeviceTSUJIENCODERDeviceCommand('VERH?', isglobalcommand=True, helpstring="Return the controller hardware version string.")

        lc_deviceSTARSCommand['GetEncoderStatus']     = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetencoderstatus',   postfunc='self._postgetencoderstatus',   helpstring="Return the string of encoder status.")
        lc_deviceSTARSCommand['GetHPMode']            = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetencoderstatus',   postfunc='self._postgethpmode',          helpstring="Return the encoder zclear timing mode (U:up, D:down).")
        lc_deviceSTARSCommand['GetEncoderSettings']   = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetencodersetting',                                           helpstring="Return the string of encoder settings.")
        lc_deviceSTARSCommand['GetValue']             = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetvalue',           postfunc='self._postgetvalue',           helpstring="Return the counter value calculated by stars software.")
        lc_deviceSTARSCommand['GetRawValue']          = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetvalue',           postfunc='self._postgetvalue',           helpstring="Return the encoder counter value.")
        lc_deviceSTARSCommand['GetCalcValue']         = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetscalevalue',      postfunc='self._postgetscalevalue',      helpstring="Return the encoder device calculation value.")
        lc_deviceSTARSCommand['GetCalcParameterM']    = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetscaleparameterm', postfunc='self._postgetscaleparameterm', helpstring="Return the multiplier parameter used by encoder device calculation.")
        lc_deviceSTARSCommand['GetCalcParameterO']    = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                                 checkfunc='self._checkgetscaleparametero', postfunc='self._postgetscaleparametero', helpstring="Return the offset parameter used by encoder device calculation.")

        lc_deviceSTARSCommand['Preset']               = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1,             checkfunc='self._checkpresetvalue',        helpstring="Preset the counter value.")
        lc_deviceSTARSCommand['ScanHome']             = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, ismotioncommand=True, checkfunc='self._checkzset',               helpstring="Enable the zclear mode.")
        lc_deviceSTARSCommand['StopScan']             = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False,                       checkfunc='self._checkzunset',             helpstring="Disable the zclear mode.")

        lc_deviceSTARSCommand['SetHPMode']            = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1,             checkfunc="self._checksethpmode",          helpstring="Set the encoder zclear timing mode (U:up, D:down).")
        lc_deviceSTARSCommand['SetCalcParameterM']    = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1,             checkfunc="self._checksetscaleparameterm", helpstring="Set the multiplier parameter used by encoder device calculation.")
        lc_deviceSTARSCommand['SetCalcParameterO']    = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1,             checkfunc="self._checksetscaleparametero", helpstring="Set the offset parameter used by encoder device calculation.")

        lc_deviceSTARSCommand['GetEncoderSyncTriggerEnable'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                     checkfunc='self._checkgetencodersynctriggerenable', postfunc='self._postgetencodersynctriggerenable',    helpstring="Return the encoder sync trigger enable or disable (Enable=1, Disable=0).")
        lc_deviceSTARSCommand['SetEncoderSyncTriggerEnable'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1, checkfunc='self._checksetencodersynctriggerenable', helpstring="Set the encoder sync trigger enable(=1) or disable(=0).")


        lc_deviceSTARSCommand['GetEncoderSyncTriggerIntervalCount'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                     checkfunc='self._checkgetencodersynctriggercount', postfunc='self._postgetencodersynctriggercount',    helpstring="Return the encoder sync trigger interval count.")
        lc_deviceSTARSCommand['GetEncoderSyncTriggerInternalCount'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-',                                     checkfunc='self._checkgetencodersynctriggerinternalcount', postfunc='self._postgetencodersynctriggerinternalcount',    helpstring="Return the encoder sync trigger internal count.")
        lc_deviceSTARSCommand['SetEncoderSyncTriggerCount'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', isreferencecommand=False, argnum=1, checkfunc='self._checksetencodersynctriggercount', helpstring="Set the encoder sync trigger count.")

        lc_deviceSTARSCommand['GetEncoderSyncTriggerPulseWidth'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', ischannelcommand=False, isglobalcommand=True, checkfunc='self._checkgetencodersynctriggerpulsewidth', postfunc='self._postgetencodersynctriggerpulsewidth',    helpstring="Return the encoder sync trigger pulse width.")
        lc_deviceSTARSCommand['SetEncoderSyncTriggerPulseWidth'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', ischannelcommand=False, isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetencodersynctriggerpulsewidth', helpstring="Set the encoder sync trigger pulse width.")

        lc_deviceSTARSCommand['GetEncoderSyncTriggerPolarity'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', ischannelcommand=False, isglobalcommand=True, checkfunc='self._checkgetencodersynctriggerpolarity', postfunc='self._postgetencodersynctriggerpolarity',    helpstring="Return the encoder sync trigger polarity.")
        lc_deviceSTARSCommand['SetEncoderSyncTriggerPolarity'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-', ischannelcommand=False, isglobalcommand=True, isreferencecommand=False, argnum=1, checkfunc='self._checksetencodersynctriggerpolarity', helpstring="Set the encoder sync trigger polarity.")

        lc_deviceSTARSCommand['SetAverageEnable'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-',  ishelponly=True, isreferencecommand=False, helpstring="Set the software average function enable or not.")
        lc_deviceSTARSCommand['GetAverageEnable'] = PyStarsDeviceTSUJIENCODERDeviceCommand('-',  ishelponly=True, helpstring="Get the software average function enable or not.")

        lc_deviceSTARSCommand['IsBusy']               = PyStarsDeviceTSUJIENCODERDeviceCommand('-',ishelponly=True,                                               helpstring="Return the encoder busy status.")
        lc_deviceSTARSCommand['hello']                = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=True,  isglobalcommand=True, helpstring="Return 'hello nice to meet you.'")
        lc_deviceSTARSCommand['help']                 = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=True,  isglobalcommand=True, helpstring="Return the list or the explanation of stars command.")
        lc_deviceSTARSCommand['getversion']           = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return this program version.")
        lc_deviceSTARSCommand['getversionno']         = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the version number of this program.")
        lc_deviceSTARSCommand['terminate']            = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Terminate this program.")
        lc_deviceSTARSCommand['listnodes']            = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the list of channels.")
        lc_deviceSTARSCommand['GetChannelList']       = PyStarsDeviceTSUJIENCODERDeviceCommand('', ishelponly=True, ischannelcommand=False, isglobalcommand=True, helpstring="Return the list of channels.")
        self._deviceSTARSCommand = lc_deviceSTARSCommand
        
        self._deviceBusyFlg              = {} #1: Busy 0:Stop
        self._deviceFirmwareInfo    = None
        self._deviceHardwareInfo    = None
        self._deviceLastStatus      = {}

        self._deviceCommandLastExecutedTime = {}
        self._deviceCommandLastWaitTime = 0
        self._inthandler = inthandler

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

#
    ##################################################################
    # Post functions(internal use)
    ##################################################################
    def _postbase(self,rt,devcommand):
        rt=self.processdevicereplystring(rt)
        if('Er:' in rt):
            return(rt)
        return(rt)

    def _postgethpmode(self,rt,devcommand):
        rt2 = self._postgetencoderstatus(rt,devcommand)
        if('Er:' in rt2):
            return(rt2)
        return(rt2.zset_cleartiming)

    def _postgetencoderstatus(self,rt,devcommand):
        rt2 = PyStarsDeviceTSUJIENCODERStatus(rt)
        if(rt2.has_error == True):
            return('Er: %s' %(rt2.error))
        else:
            chnum = rt2.channel_no 
            self._deviceLastStatus[chnum] = rt2
            self._deviceCommandLastExecutedTime['ENCSTATUS'+str(chnum)] = time.time()
        return(rt2)

    def _postgetvalue(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Count reply error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^R(\S)([+-]\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing read count failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
        return(rt2)

    def _postgetscalevalue(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Count reply error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^D(\S)([+-]\d+\.\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing read scaling value failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
        return(rt2)

    def _postgetscaleparameterm(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Multiplier reply error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^M(\S)([+-]\d+\.\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing read scaling multiplier param failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
        return(rt2)

    def _postgetscaleparametero(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Offset reply error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^O(\S)([+-]\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing read scaling offset param failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
        return(rt2)

    def _postgetencodersynctriggerenable(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Encoder sync trigger enable reply error ('%s'). Unexpected reply format." %(rt)
        if(rt.upper()=='EN'):
            rt2 = '1'
        elif(rt.upper()=='DS'):
            rt2 = '0'
        return(rt2)

    def _postgetencodersynctriggercount(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Encoder sync trigger count error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^E(\S)TC([+-]\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing encoder sync trigger count param failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
                rt2=str(int(rt2))
        return(rt2)

    def _postgetencodersynctriggerinternalcount(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Encoder sync trigger internal count error ('%s'). Unexpected reply format." %(rt)
        m = re.search("^E(\S)TCC([+-]\d+)\Z", rt.upper())
        if m:
            no = ord(m.group(1)) - 65
            rt2="Er: Analyzing encoder sync trigger internal count param failure ('%s'). (Unknown channel:%d)" %(rt,no)
            if(no>=0):
                rt2=m.group(2)
                rt2=str(int(rt2))
        return(rt2)

    def _postgetencodersynctriggerpulsewidth(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Encoder sync trigger pulse width ('%s'). Unexpected reply format." %(rt)
        m = re.search("^ENCTW(\d+)\Z", rt.upper())
        if m:
            rt2=m.group(1)
            rt2=str(int(rt2))
        return(rt2)

    def _postgetencodersynctriggerpolarity(self,rt,devcommand):
        if(rt == ''):
            return('Er: No data.')
        rt2="Er: Encoder sync trigger polarity ('%s'). Unexpected reply format." %(rt)
        if(rt == 'POS'):
            rt2=rt
        elif(rt == 'NEG'):
            rt2=rt
        return(rt2)

    ##################################################################
    # Check functions(internal use)
    ##################################################################
    # Return encoder value command
    def _checkgetvalue(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getvaluecommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder value command
    def _checkpresetvalue(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_presetcommand(int(id),int(rt2))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder hp mode set command
    def _checksethpmode(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkupdown('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setztimingcommand(int(id),rt2)
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder settings command
    def _checkgetencodersetting(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getencodersetcommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder z-clear enable command
    def _checkzset(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setzsetcommand(int(id),1)
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder z-clear disable command
    def _checkzunset(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setzsetcommand(int(id),0)
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)
        
    # Return encoder status command
    def _checkgetencoderstatus(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getzstatuscommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder scaled value command
    def _checkgetscalevalue(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getscalevaluecommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder multiplier parameter command
    def _checkgetscaleparameterm(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getscalemultipliercommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder offset parameter command
    def _checkgetscaleparametero(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getscaleoffsetcommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder multiplier parameter set command
    def _checksetscaleparameterm(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisfloat('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setscalemultipliercommand(int(id),float(rt2))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder offset parameter set command
    def _checksetscaleparametero(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setscaleoffsetcommand(int(id),int(rt2))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder scaled value command
    def _checkgetencodersynctriggerenable(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getencodersynctriggerenablecommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger enable command
    def _checksetencodersynctriggerenable(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkenable('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setencodersynctriggerenablecommand(int(id),rt2)
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger count command
    def _checkgetencodersynctriggercount(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getencodersynctriggercountcommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger count command
    def _checksetencodersynctriggercount(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setencodersynctriggercountcommand(int(id),int(rt2))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger count internal command
    def _checkgetencodersynctriggerinternalcount(self,cmd,args,id):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)
        dcmd = self._deviceFirmwareInfo.get_getencodersynctriggerinternalcountcommand(int(id))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger pulsewidth command
    def _checksetencodersynctriggerpulsewidth(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)

        (rt2,errormsg) = self._sub_checkisinteger('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setencodersynctriggerpulsewidthcommand(int(rt2))
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger pulsewidth command
    def _checkgetencodersynctriggerpulsewidth(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)

        dcmd = self._deviceFirmwareInfo.get_getencodersynctriggerpulsewidthcommand()
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger polatiry command
    def _checksetencodersynctriggerpolarity(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)

        (rt2,errormsg) = self._sub_checkpolarity('',args)
        if(rt2 == ''):
            return(rt2,errormsg)
        dcmd = self._deviceFirmwareInfo.get_setencodersynctriggerpolaritycommand(rt2)
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    # Return encoder sync trigger polarity command
    def _checkgetencodersynctriggerpolarity(self,cmd,args):
        rt = ''
        errormsg = "Er: Procedure 'device_init()' unprocessed."
        if(self._deviceFirmwareInfo is None):
            return(rt,errormsg)

        dcmd = self._deviceFirmwareInfo.get_getencodersynctriggerpolaritycommand()
        if(dcmd == ''):
            errormsg = 'Er: %s' %(self._deviceFirmwareInfo.error)
        else:
            rt = dcmd
        return(rt,errormsg)

    def _checkcmdargs(self,cmd,args):
        rt = ''
        errormsg=''
        return(cmd,"")

    # sub 
    def _sub_checkpolarity(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg="Er: Value must be 'POS' or 'NEG'."
        if(val == 'POS'):  val = 'POS'
        elif(val == 'NEG'): val = 'NEG'
        elif(val == '1'):  val = 'POS'
        elif(val == '0'):  val = 'NEG'
        elif(val == '+'):  val = 'POS'
        elif(val == '-'):  val = 'NEG'
        if(val == 'POL' or val == 'NEG'):
            rt=val
        if(rt == ''):
            return(rt,errormsg)
        if(cmd == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

    def _sub_checkenable(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg="Er: Value must be '1' or '0'."
        if(val == 'EN'):  val = 'E'
        elif(val == 'DS'): val = 'D'
        elif(val == '1'):  val = 'E'
        elif(val == '0'): val = 'D'
        if(val == 'E' or val == 'D'):
            rt=val
        if(rt == ''):
            return(rt,errormsg)
        if(cmd == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

    def _sub_checkupdown(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg="Er: Value must be 'U' or 'D'."
        if(val == 'UP'):  val = 'U'
        elif(val == 'DOWN'): val = 'D'
        elif(val == '1'):  val = 'U'
        elif(val == '0'): val = 'D'
        if(val == 'U' or val == 'D'):
            rt=val
        if(rt == ''):
            return(rt,errormsg)
        if(cmd == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

    def _sub_checkisfloat(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg = "Er: Bad parameters. (invalid format:%s)" %(val)
        if(val == ''):
            return(rt,errormsg)
        try:
            n = float(val)
            rt = str(n)
        except ValueError:
            pass
        if(cmd == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

    def _sub_checkisinteger(self,cmd,args):
        val = args[0].upper()
        rt = ''
        errormsg = "Er: Bad parameters. (invalid format:%s)" %(val)
        if(val == ''):
            return(rt,errormsg)
        try:
            n = float(val)
            if(n.is_integer()):
                rt = '%0.0lf' %(n)
        except ValueError:
            pass
        if(cmd == ''):
            return(rt,errormsg)
        return(cmd+" "+rt,errormsg)

#######################################
## STARS interval handler:
#######################################
def interval():
    global gb_StarsInstance
    global gb_DeviceInstance
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    now = time.time()

    # Check device connectection lost or not, and read buffer.
    if(dc.isconnected() == False):
        destsendstr="Terminate STARS %s. [Device disconnection]\n" %(st.nodename)
        _outputlog(WARN, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
        st.terminateMainloop()
        return

    # Check if device in lock state
    llock=dc.device_getisbusy()
    w=0
    if((llock)>=1):
        w = 1
    # Return if device in lock state.
    if(w == 1):
        return True

    #Check if stars think busy

    for channelname, channelnostr in gb_ChannelNameList.items():
        f=stars_getflgbusy(channelname,local=True)
        flap=now-dc.device_getlastencoderstatustimestamp(channelnostr)
        if(flap<0):
            flap = 0.25
        if(f == '0'):
            continue
        finterval = 0.25
        if(flap<finterval):
            continue
        b=stars_getflgbusy(channelname)
        #Changed to busy
        if(f != str(b)):
            stars_setlocalflgbusy(channelname,str(b))
    return True

##################################################################
# Callback functions:
##################################################################
## Device socket handler: DETECT
def device_sockhandler(sock, tm='', printflg=True):
    global gb_StarsInstance
    global gb_DeviceInstance
    st = gb_StarsInstance
    dc = gb_DeviceInstance
    if(printflg == True): 
        destsendstr="Device_detected %s." %(st.nodename)
        _outputlog(WARN, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
    rt = dc.isconnected()
    while rt==True:
        if(printflg==True):
            destsendstr="Device_reading."
            _outputlog(WARN, destsendstr)
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
                destsendstr="Device_read#%s#\n" %(rt)
                _outputlog(WARN, destsendstr)
                device_replyanalyzer(rt,printflg)
        else:
            break
        tm=0.005
    rt = dc.isconnected()
    if(rt == False):
        destsendstr="Terminate STARS %s. [Device disconnection]\n" %(st.nodename)
        _outputlog(WARN, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
        st.terminateMainloop()
        return(rt)
    if(printflg==True):
        destsendstr="Device_detected done %s.\n" %(st.nodename)
        _outputlog(WARN, destsendstr)
        rt=st.send('System _Msg '+destsendstr)
    return(rt)

## Device reply handler: DETECT
def device_replyanalyzer(recvdata, printflg=True):
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
    parameters = []
    if(allmess.parameters != ''):
        parameters = allmess.parameters.split(" ")

    _outputlog(INFO, 'STARS Recv[' + allmess.nodeto + "]:"+allmess)

    destsendstr='';
    rt = ''
    if(allmess.nodeto.startswith(st.nodename + '.')==True):
         channelname = allmess.nodeto.replace(st.nodename + '.', '', 1)
         if((channelname != '') and (channelname in gb_ChannelNameList)):
            address = gb_ChannelNameList[channelname]
            rt = sub_channelhandler(command, parameters, channelname, address)
            if(rt != ''):
                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
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
        if(message.startswith('@')==True):
            return
        elif(message.startswith('_')==True):
            return
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
        elif(message in ['listnodes']):
            rt=' '.join(gb_ChannelNameList.keys())
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif(message in ['GetChannelList']):
            rt=','.join(gb_ChannelNameList.keys())
            destsendstr = allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        elif((command in ['IsBusy','GetValue','GetRawValue']) and (gb_StarsIsUseGetMultiValues == True)):
            replylist=[]
        elif((command in ['IsBusy','GetValue','GetRawValue']) and (gb_StarsIsUseGetMultiValues == True)):
            replylist=[]
            argnum = 0
            if(len(parameters) == 0):
                pass
            elif(len(parameters)==len(gb_ChannelNameList.keys())):
                pass
            else:
                rt = 'Er: Bad command or parameters.'
            if('Er:' not in rt):
                rt = 'Er: Undefined channels.'
                for chname,id in gb_ChannelNameList.items():
                    if(len(parameters) == 0):
                        pass
                    elif(len(parameters)==len(gb_ChannelNameList.keys())):
                        if(parameters[i]=='-'):
                           id = -1
                        elif(parameters[i]=='0'):
                           id = -1
                        elif(parameters[i]=='1'):
                            pass
                        else:
                            rt = 'Er: Bad parameters.'
                            break
                    if(id == -1):
                        replylist.append('-')
                        rt = ' '.join(replylist)
                        continue
                    if(command == 'IsBusy'):
                        f=stars_getflgbusy(chname,local=True)
                        b=stars_getflgbusy(chname)
                        replylist.append(b)
                        rt = ' '.join(replylist)
                        if(f != str(b)):
                            stars_setlocalflgbusy(chname,str(b))
                    elif(command == 'GetValue'):
                        v=stars_getvalue(chname,isnoaverage=stars_getnoaverageflg(chname))
                        replylist.append(v)
                        rt = ' '.join(replylist)
                    else:
                        v=stars_getvalue(chname,israw=True,isnoaverage=stars_getnoaverageflg(chname))
                        replylist.append(v)
                        rt = ' '.join(replylist)

            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #### Global command:
        elif(dobjgb is not None):
            rt = 'Er: Bad parameters.'
            addrlist=[]
            channelnamelist=[]
            argnum      =dobjgb.argnum
            isallowbusy =dobjgb.isallowbusy
            ischeckcargnum=dobjgb.ischeckargnum
            ismotion=dobjgb.ismotioncommand
            if((ischeckcargnum == False) or (len(parameters)==argnum)):
                rt = 'Ok:'
                if(isallowbusy==False):
                    for chname in gb_ChannelNameList.keys():
                        b=stars_getflgbusy(chname,local=True)
                        if(b=="1"):
                            rt = 'Er: Busy.'
                            break
                if('Er:' not in rt):
                    rt=dc.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CONTROLLER,command,parameters,addrlist)
                if('Er:' not in rt):
                    if(ismotion==True):
                        for chname in gb_ChannelNameList.keys():
                            stars_setlocalflgbusy(chname,"1")
            destsendstr=allmess.nodeto + '>' + allmess.nodefrom+' @' + message + ' ' + rt
        #### Channel command + Logic for SingleValue
        elif((dobjmt is not None) and (gb_StarsIsUseGetMultiValues == False)):
            rt = 'Er: Bad parameters.'
            argnum  = dobjmt.argnum
            ischeckcargnum=dobjmt.ischeckargnum
            if((ischeckcargnum == False) or (len(parameters) == (argnum + 1))):
                val = parameters[0]
                parameters.pop(0)
                rt = "Er: Bad channel name or number. '%s'" %(val)
                channelname = ''
                if(val in gb_ChannelNameList):
                    channelname = val
                elif((max([ord(c) for c in val]) < 128) and (val.isdigit()==True)):
                    num = int(val)
                    if((0 <= num) and (num < len(gb_ChannelNameList.keys()))):
                        channelname = gb_ChannelNameList[num]
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
            argnum  =dobjmt.argnum
            isallowbusy =dobjmt.isallowbusy
            ischeckcargnum=dobjmt.ischeckargnum
            ismotion=dobjmt.ismotioncommand
            isreferencecommand=dobjmt.isreferencecommand
            if(((len(parameters)==0) and (argnum==0))):
                rt = 'Er: Undefined channels.'
                for chname in gb_ChannelNameList.keys():
                    rt = 'Ok:'
                    if(isallowbusy==False):
                        b=stars_getflgbusy(chname,local=True)
                        if(b=="1"):
                            rt = 'Er: Busy.'
                            break
                    addrlist.append(gb_ChannelNameList[chname])
 
                if('Er:' not in rt):
                    rt=dc.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL,command,parameters,addrlist)
                if(('Er:' not in rt)):
                    if(ismotion == True):
                        for chname in gb_ChannelNameList.keys():
                            stars_setlocalflgbusy(chname,"1")
                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
            elif(len(parameters)==len(gb_ChannelNameList.keys())):
                rt = 'Er: Undefined channels.'
                checklist=[True,False]
                for ischeckonly in checklist:
                    replylist = []
                    for chname,id in gb_ChannelNameList.items():
                        rt = 'Ok:'
                        parameters2=[]
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
                            if(isallowbusy==False):
                                b=stars_getflgbusy(chname,local=True)
                                if(b=="1"):
                                    rt = 'Er: Busy.'
                                    break
                        if(id == -1):
                            rt2 = '-'
                        else:
                            rt2=dc.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL,command,parameters2,[id],True,ischeckonly)
                            if('Er:' in rt2):
                                rt=rt2
                                break
                        if(ischeckonly == True):
                            continue
                        if(isreferencecommand==True):
                            replylist.append(rt2) 
                            rt = ' '.join(replylist)
                        if(ismotion == True):
                            if(id != -1):
                                stars_setlocalflgbusy(chname,"1")

                destsendstr = allmess.nodeto + '>' + allmess.nodefrom + ' @' + message + ' ' + rt
        else:
            rt = 'Er: Bad command or parameters.'
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
        _outputlog(INFO,'STARS Send[' + allmess.nodeto + "]:"+destsendstr)
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
    elif((command == 'SetAverageEnable') and (len(parameters) == 1)):
        rt = str(stars_setnoaverageflg(channelname,parameters[0]))
    elif((command == 'GetAverageEnable') and (len(parameters) == 0)):
        rt = str(stars_getnoaverageflg(channelname,asSTARS=True))
    elif((command == 'IsBusy') and (len(parameters) == 0)):
        rt = str(stars_getflgbusy(channelname))
    elif((command == 'TestFormula') and (len(parameters) == 1)):
        rt = stars_getvalue(channelname,calctestonly=parameters[0],isnoaverage=stars_getnoaverageflg(channelname))
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
        #*** Pre check if busy
        if(isallowbusy == False):
            rt = 'Er: Busy.'
            b = stars_getflgbusy(channelname,local=True)
            if(b == "1"):
                return(rt)
        #*** Exec
        if((command == 'GetValue') and (len(parameters) == 0)):
            rt=stars_getvalue(channelname,isnoaverage=stars_getnoaverageflg(channelname))
        elif((command == 'GetRawValue') and (len(parameters) == 0)):
            rt=stars_getvalue(channelname,israw=True,isnoaverage=stars_getnoaverageflg(channelname))
        else:
            rt=dc.exec_command(PyStarsDeviceTSUJIENCODERDeviceCommandLevel.CHANNEL,command,parameters,[address])
        if('Er:' in rt): return(rt)
        #*** Post send busy if motion
        if(ismotion == True):
            stars_setlocalflgbusy(channelname,"1")
    return(rt)

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

## Device timewait handler:
def device_timewaithandler(timebase,lap):
    global gb_StarsInstance
    st = gb_StarsInstance
    global gb_DeviceInstance
    dc = gb_DeviceInstance
    return(True)

## STARS set busyflg
def stars_setlocalflgbusy(channelname, f, force=False):
    global gb_StarsInstance
    global gb_DeviceInstance
    global gb_StarsLocalBusyFlg
    st = gb_StarsInstance
    dc = gb_DeviceInstance

    prevf=stars_getflgbusy(channelname,local=True)
    gb_StarsLocalBusyFlg[channelname]=f
    f=stars_getflgbusy(channelname,local=True)
    if((force==True) or (f is None) or ((f is not None) and (prevf != f))):
        destsendstr=st.nodename+'.'+channelname+'>System _ChangedIsBusy '+str(f)
        _outputlog(INFO, destsendstr)
        rt=st.send(destsendstr)
    return f

## STARS get busyflg
def stars_getflgbusy(channelname,local=False):
    global gb_ChannelNameList
    global gb_DeviceInstance
    global gb_StarsLocalBusyFlg
    #global gb_StarsLastStatusRefreshedTime
    dc = gb_DeviceInstance

    channelnostr='%02d' % int(gb_ChannelNameList[channelname])
    if(local==True):
        if(channelname not in gb_StarsLocalBusyFlg):
            gb_StarsLocalBusyFlg[channelname] = ''
        rt = gb_StarsLocalBusyFlg[channelname]
    else:
        rt = str(dc.device_getflgbusy(channelnostr))
        if('Er:' not in rt):
            pass
            #gb_StarsLastStatusRefreshedTime = time.time()
    return rt

def stars_setnoaverageflg(channelname,boolstring):
    global gb_InternalIgnoreAverageFlg
    if(boolstring=='1'):
        gb_InternalIgnoreAverageFlg[channelname]=False
        return('Ok:')
    elif(boolstring=='0'):
        gb_InternalIgnoreAverageFlg[channelname]=True
        return('Ok:')
    return('Er: Bad command or parameters.')

def stars_getnoaverageflg(channelname,asSTARS=False):
    global gb_InternalIgnoreAverageFlg
    rt = False
    if(channelname in gb_InternalIgnoreAverageFlg):
        rt=gb_InternalIgnoreAverageFlg[channelname]
    if(asSTARS == True):
        if(rt == False):
            return("1")
        return("0")
    return(rt)

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

def stars_getvalue(channelname, calctestonly=None, israw=False, isnoaverage=False):
    global gb_ChannelNameList
    global gb_DeviceInstance
    
    dc = gb_DeviceInstance
    channelnostr='%02d' % int(gb_ChannelNameList[channelname])
    rt = ''
    average_count=gb_ValueAverageCountList[channelname]
    if(isnoaverage == True):
        average_count = 1;
    formula = gb_ValueFormulaList[channelname]
    replyformat = gb_ValueFormatList[channelname]
    if(israw == True):
        formula     = ''
        replyformat = ''
        if(dc._deviceFirmwareInfo is None):
            replyformat = '%+08d'
        else:
            replyformat = '%+0'+str(dc._deviceFirmwareInfo.digitnum+1)+'d'
   
    if(calctestonly is not None):
        val = calctestonly
        valbuf = str(val)
        _outputlog(INFO,"stars_getvalue: calctest using input=%s,formula=%s,replyformat=%s" %(valbuf,formula,replyformat))
        if(formula != ''):
            cbuf = formula.replace("INPUT",str(val))
            val = eval(cbuf)
            valbuf = str(val)
            _outputlog(INFO,"stars_getvalue: calctest(formula) %lf : %s" %(val, cbuf))
        if(replyformat != ''):
            valbuf = replyformat %(val)
            _outputlog(INFO,"stars_getvalue: calctest(format) %lf using %s" %(val, replyformat))
        rt = valbuf
    else:
        rt = dc.device_getvalue(channelnostr,averagecount=average_count,formula=formula,replyformat=replyformat)
    return rt

##################################################################
# Define global parameters
##################################################################
# Global parameters.
gb_Debug = False
gb_StarsInstance = None
gb_DeviceInstance = None

gb_NumberOfChannels = -1
gb_ChannelNameList =  OrderedDict()

gb_ValueFormulaList = {}
gb_ValueFormatList  = {}
gb_ValueAverageCountList  = {}
# Internal of internal
gb_InternalIgnoreAverageFlg = {}

##################################################################
# Define internal parameters
##################################################################
# Internal parameters.
gb_ScriptName = os.path.splitext(os.path.basename(__file__))[0]
#ScriptPath = os.path.dirname(os.path.abspath(sys.argv[0]))
gb_StarsLocalBusyFlg   = {}
#gb_StarsLocalStatus    = {}
#gb_StarsLocalCurrent   = {}
#gb_StarsLastSendBusyFlg = {}
gb_StarsIsUseGetMultiValues = False
#gb_StarsLastStatusRefreshedTime = time.time()


#----------------------------------------------------------------
# Program pyexrc.py
#----------------------------------------------------------------
if __name__ == "__main__":
    ##################################################################
    # Import modules
    ##################################################################
    from pystarslib import pystarsutilconfig, pystarsutilargparser

    # Define: Appliction default parameters
    starsNodeName   = 'exrc'
    starsServerHost = '127.0.0.1'
    starsServerPort = 6057
    deviceHost = '192.168.1.123'
    devicePort = 7777

    ##################################################################
    # Define program arguments
    ##################################################################
    optIO=pystarsutilargparser.PyStarsUtilArgParser(numberOfDeviceServer=1)
    parser=optIO.generate_baseparser(prog=gb_ScriptName,version=__version__)
    parser.add_argument('--channelnamelist', dest="ChannelNameList", help='Name list of device channels.')
    parser.add_argument('--numberofchannels', type=int, dest="NumberOfChannels", help='Number of channels.(Optional, for unknown version.)')

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
    lc_numberOfChannels=-1
    lc_ChannelNameList=None
    lc_OptionList = None
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
        lc_numberOfChannels    = cfgIO.get(starsNodeName, 'NumberOfChannels'    , lc_numberOfChannels, int)
        lc_ChannelNameList     = cfgIO.get(starsNodeName, 'ChannelNameList'     , lc_ChannelNameList)
        try:
            lc_OptionList = cfgIO.gethandle().options(starsNodeName)
        except:
            lc_OptionList = None

    # Fix optional parameters
    starsServerHost = optIO.get(args.StarsServerHost,starsServerHost)
    starsServerPort = optIO.get(args.StarsServerPort,starsServerPort)
    deviceHost      = optIO.get(args.DeviceHost,deviceHost)
    devicePort      = optIO.get(args.DevicePort,devicePort)
    lc_numberOfChannels  = optIO.get(args.NumberOfChannels, lc_numberOfChannels)
    lc_ChannelNameList   = optIO.get(args.ChannelNameList,  lc_ChannelNameList)
    if(lc_ChannelNameList is None):
        lc_ChannelNameList=[]
    else:
        lc_ChannelNameList=lc_ChannelNameList.split(',')

    ##################################################################
    # Connect to device
    ##################################################################
    #Create device instance with devserver:devport 
    dc=PyStarsDeviceTSUJIENCODER(deviceHost, devicePort, device_timewaithandler)
    gb_DeviceInstance=dc

    #Set properties for device instance
    dc.setdebug(gb_Debug)
    if(gb_Debug == True):
        gb_DeviceInstance.printinfo()

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
        sys.stdout.write(dc.getlasterrortext()+'\n')
        exit(1)

    ##################################################################
    # Parse channel settings
    ##################################################################
    if(lc_numberOfChannels<=0):
        lc_numberOfChannels = dc.device_getnumberofchannel()
        if(len(lc_ChannelNameList)>0):
            lc_numberOfChannels = len(lc_ChannelNameList)
        elif(gb_NumberOfChannels>0):
            lc_numberOfChannels = gb_NumberOfChannels
        if(lc_numberOfChannels<=0):
            lc_numberOfChannels = 2

    for i in range(len(lc_ChannelNameList),lc_numberOfChannels,1):
        no=str(i)
        lc_ChannelNameList.append('ENC'+no)

    for i in range(lc_numberOfChannels):
        #Format number
        gb_ChannelNameList[lc_ChannelNameList[i]] = '%02d' % (i)

    for i in range(lc_numberOfChannels):
        chname=lc_ChannelNameList[i]
        if(lc_OptionList is None):
            gb_ValueFormulaList[chname] = ''
            gb_ValueFormatList[chname]  = ''
            gb_ValueAverageCountList[chname]  = 1
            gb_InternalIgnoreAverageFlg[chname] = False
            continue
        gb_ValueFormulaList[chname] = cfgIO.get(starsNodeName, chname+'.Formula'     , '')
        gb_ValueFormatList[chname]  = cfgIO.get(starsNodeName, chname+'.Format'      , '')
        gb_ValueAverageCountList[chname]  = cfgIO.get(starsNodeName, chname+'.AverageCount'      , 1, int)
        gb_InternalIgnoreAverageFlg[chname] = False
        if(gb_ValueFormulaList[chname] != ''):
            for key in sorted(lc_OptionList,reverse=True):
                val = cfgIO.get(starsNodeName,  key     , '')
                lchname=chname.lower()
                if(key.startswith(lchname+".")):
                    key2 = key.replace(lchname+".","").upper()
                    gb_ValueFormulaList[chname] = gb_ValueFormulaList[chname].replace(key2,val)


    gb_NumberOfChannels = lc_numberOfChannels
    if(gb_Debug==True):
        sys.stdout.write("starsNodeName#"+str(starsNodeName)+"#"+'\n')
        sys.stdout.write("starsServerHost#"+str(starsServerHost)+"#"+'\n')
        sys.stdout.write("starsServerPort#"+str(starsServerPort)+"#"+'\n')
        sys.stdout.write("deviceHost#"+str(deviceHost)+"#"+'\n')
        sys.stdout.write("devicePort#"+str(devicePort)+"#"+'\n')
        sys.stdout.write("numberOfChannels#"+str(gb_NumberOfChannels)+"#"+'\n')
        sys.stdout.write("ChannelNameList#"+str(gb_ChannelNameList)+"#"+'\n')
        for i in range(gb_NumberOfChannels):
            chname=list(gb_ChannelNameList.keys())[i]
            sys.stdout.write(chname+".formula#"     +str(gb_ValueFormulaList[chname])+"#"+'\n')
            sys.stdout.write(chname+".format#"      +str(gb_ValueFormatList[chname])+"#"+'\n')
            sys.stdout.write(chname+".averagecount#"+str(gb_ValueAverageCountList[chname])+"#"+'\n')

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
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Add callback handler
    rt=st.addcallback(handler)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)
    rt=st.addcallback(device_sockhandler,dc.gethandle(),'DETECT')
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Start Mainloop()
    rt=st.Mainloop(interval,0.01)
    if(rt==False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        exit(1)

    #Device close
    #*** sleep for callback terminate wait
    time.sleep(1)
    dc.disconnect()
    st.removecallback()
    st.disconnect()
    exit(0)
