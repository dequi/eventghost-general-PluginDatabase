# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2012 Walter Kraembring <krambriw>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

##############################################################################
#
# Acknowledgements: Part of code and some ideas are based on the serial plugin
#
##############################################################################
# Revision history:
#
# 2012-06-29  Walter Kraembring: Added support for the RFXMeter and RFXPower
#                                Added support for the La Crosse WS2300
# 2012-06-27  Walter Kraembring: Added support for websockets (requires the
#                                websocket suite plugin to be added to your
#                                configuration.)
#                                Added support for OWL CM119/160 and
#                                UV sensors UVN128, UV138, UVN800, TFA
# 2012-05-29  Walter Kraembring: Added support for RisingSun, RollerTrol and
#                                Viking 02811
#                                Bug fixed for AC (unit codes 1-16)
# 2012-05-09  Walter Kraembring: Suppress/Allow duplicated events selectable
# 2012-05-04  Walter Kraembring: X10 decoding of received bright/dim commands
#                                fixed.
# 2012-04-29  Walter Kraembring: This version supports:
#                                - Wind directions as text information
#                                 (S, N, E, W etc).
#                                - Rain total values are divided by 10
#                                 (requiresFW version 35 and later).
#                                - TEMP6 - TS15C.
#                                - UPM/ESIC wind & rain sensors.
# 2012-04-15  Walter Kraembring: This version is using the eg.SerialThread.
#                                Improved performance, simplified the code.
#                                Changed the calculation of temperature from
#                                temperature sensors.
# 2012-04-13  Walter Kraembring: Improved automatic naming of macros.
# 2012-04-11  Walter Kraembring: Added selection of supported protocols.
#                                Improved reading and decoding from COM port.
#                                Improved automatic naming of macros.
#                                Cosmetic bug fixing in some action
#                                configuration dialogs.
# 2012-04-02  Walter Kraembring: First official version.
##############################################################################

import eg
import time, os
from threading import Event, Thread

eg.RegisterPlugin(
    name = "RFXtrx",
    author = "krambriw",
    guid = "{72DCE030-68FF-49B9-835D-295D4CF048ED}",
    version = "1.5.1 beta II",
    canMultiLoad = True,
    kind = "external",
    description = (
        "RFXtrx communication through a virtual serial port."
        '<br\n><br\n>'
        '<center><img src="rfxtrx.png" /></center>'
    ),
    url = "http://www.eventghost.net/forum",
)



class Text:
    port = "Port:"
    logToFile = "Log events to file"
    debugInfo = "Show debug info"
    macroNames = "Automatic naming of macros"
    dupEvents = "Allow duplicated events"
    use_websockets = "Use websockets and select the assigned port number for the Websocket Suite server" 
    decode_50_0 = (
                "THR128/138, THC138, THC238/268, THN132, THWR288, THRN122, THN122, AW129/131, THWR800, "
    )
    decode_50_1 = (
                "RTHN318, La Crosse TX3, TX4, TX17, TS15C, Viking 02811, La Crosse WS2300 "
    )
    decode_51 = "La Crosse TX3, La Crosse WS2300 "
    decode_52_0 = (
                "THGN122/123, THGN132, THGR122/228/238/268, THGR810, THGN800, RTGR328, THGR328, WTGR800, "
    )
    decode_52_1 = (
                "THGR918, THGRN228, THGN500, TFA TS34C, Cresta, UPM/ESIC WT450H "
    )
    decode_54 = "BTHR918, BTHR918N, BTHR968 "
    decode_55 = "RGR126/682/918, PCR800, TFA, UPM RG700, La Crosse WS2300 "
    decode_56 = "WTGR800, WGR800, STR918, WGR918, TFA, UPM WDS500 "
    decode_57 = "UVN128, UV138, UVN800, TFA "
    decode_5A = "OWL CM119/160 "
    decode_71 = "RFXMeter, RFXPower "
    decode_10 = "X10 lighting, ARC, ELRO AB400D, Waveman, Chacon EMW200, IMPULS, RisingSun "
    decode_11 = "AC, HomeEasy EU, ANSLUT "
    decode_12 = "Koppla "
    decode_14_00 = "LightwaveRF, Siemens "
    decode_14_01 = "EMW100 GAO/Everflourish "
    decode_18_19 = "Harrison Curtain, RollerTrol "
    decode_20_0 = (
                "X10 security sensors, KD101, Visonic PowerCode sensors, Visonic CodeSecure sensors "
    )

    decodeError = "Decoding of message failed: "
    fwVersion = "RFXtrx Firmware Version: "
    messageL = "Wrong message length: "
    messageDbg = "Debug Info: "
    messageUC = "Message is incomplete: "
    messageUKnwn = "Unknown message: "
    messageWebSocketError = "Websocket error...check that the plugin is added to your configuration "
    messageWebSocketBroadcastError = "Websocket broadcast error...check the websocket configuration "
 

    disconnecting = "Stopping and disconnecting the RFXtrx device...please wait"
    cleanUpmonitoring = "Cleaning up monitoring tasks..."
    readyStopped = "Plugin successfully stopped"
    dt_threadStopped = "Date & Time thread ended"    
    ka_threadStopped = "Keep Alive thread ended"    
    keyAdded = "Key added to dictionary"

    textBoxName = "Enter a descriptive name for the action"
    textBoxProtocol = "Select the device protocol to be used"
    textBoxHouseCode = "Select the house code of the device"
    textBoxDeviceCode = "Select the device code of the device"
    textBoxCommand = "Select the command to send"

    textBoxAddress = "Type/paste the unit address to be used (from 00 00 00 01 to 03 FF FF FF)"
    textBoxDeviceUnit = "Select the unit code of the device"
    textBoxLevel = "Select the dim/bright level"

    textBoxSystem = "Select the system code to use"
    textChannel = "Check the boxes for the channels to use"
    textBoxDeviceID = "Select the proper ID selections"    
    
    txt_signal_back = "Recovered contact with sensor"
    txt_taskObj = "Lost contact with sensor"
    


class CurrentStateData(eg.PersistentData):
    current_state_memory = {}
    rfxSensors = {}



class RFXtrx(eg.RawReceiverPlugin):
    text = Text

    def __init__(self):
        self.current_state_memory = CurrentStateData.current_state_memory
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(WebRefresh)
        self.AddAction(send_AC)
        self.AddAction(send_ARC)
        self.AddAction(send_Waveman)
        self.AddAction(send_Chacon_EMW200)
        self.AddAction(send_IMPULS)
        self.AddAction(send_RisingSun)
        self.AddAction(send_Siemens_Lightwave_RF)
        self.AddAction(send_EMW100_GAO_Everflourish)
        self.AddAction(send_ELRO_AB400D)
        self.AddAction(send_Harrison_Curtain)
        self.AddAction(send_RollerTrol)
        self.AddAction(send_X10)
        self.AddAction(send_Koppla)
        self.AddAction(send_x10_security_remote)
        self.AddAction(send_KD101_smoke_detector)


    def __start__(
        self,
        port,
        bLogToFile,
        bDebug,
        b_50,
        b_51,
        b_52,
        b_54,
        b_55,
        b_56,
        b_57,
        b_5A,
        b_10,
        b_11,
        b_12,
        b_14_00,
        b_14_01,
        b_18_19,
        b_20,
        mMacroNames,
        bDupEvents,
        websocket_port_nbr,
        use_websockets, 
        b_71
    ):
        prefix="RFXtrx"
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.b_50 = b_50
        self.b_51 = b_51
        self.b_52 = b_52
        self.b_54 = b_54
        self.b_55 = b_55
        self.b_56 = b_56
        self.b_57 = b_57
        self.b_5A = b_5A
        self.b_71 = b_71
        self.b_10 = b_10
        self.b_11 = b_11
        self.b_12 = b_12
        self.b_14_00 = b_14_00
        self.b_14_01 = b_14_01
        self.b_18_19 = b_18_19
        self.b_20 = b_20
        
        self.decode_050_mem = {}
        self.decode_051_mem = {}
        self.decode_052_mem = {}
        self.decode_054_mem = {}
        self.decode_055_mem = {}
        self.decode_056_mem = {}
        self.decode_057_mem = {}
        self.decode_05A_mem = {}
        self.decode_071_mem = {}
        self.decode_010_mem = {}
        self.decode_011_mem = {}
        self.decode_012_mem = {}
        self.decode_014_00_mem = {}
        self.decode_014_01_mem = {}
        self.decode_018_019_mem = {}
        self.decode_020_mem = {}
        
        self.monitor_050_mem = {}
        self.monitor_051_mem = {}
        self.monitor_052_mem = {}
        self.monitor_054_mem = {}
        self.monitor_055_mem = {}
        self.monitor_056_mem = {}
        self.monitor_057_mem = {}
        self.monitor_05A_mem = {}
        self.monitor_071_mem = {}
        self.monitor_020_mem = {}

        self.mMacroNames = mMacroNames
        self.bDupEvents = bDupEvents
        self.use_websockets = use_websockets
        self.websocket_port_nbr = str(websocket_port_nbr)
        self.rfxSensors = CurrentStateData.rfxSensors

        self.keepAliveThreadEvent = Event()
        self.remain = 0.0
        keepAliveThread = Thread(target=self.keep_Alive, args=(self.keepAliveThreadEvent,))
        keepAliveThread.start()

        self.dateTimeThreadEvent = Event()
        dateTimeThread = Thread(target=self.date_Time, args=(self.dateTimeThreadEvent,))
        dateTimeThread.start()

        self.out = ''
        self.pl = 0
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 38400)
        self.serialThread.SetRts(True)
        self.serialThread.SetDtr(True)
        self.serialThread.Start()

        #Reset connection
        reset_str = "0D 00 00 00 00 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(reset_str, '', '')        
        eg.Wait(2.0)
        
        #Flush the COM port receive buffer
        self.serialThread.Flush()

        #Get device status
        get_status_str = "0D 00 00 01 02 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(get_status_str, '', '')        
        

    def __stop__(self):
        print self.text.disconnecting
        self.dateTimeThreadEvent.set()
        self.keepAliveThreadEvent.set()
        self.serialThread.Close()

        print self.text.cleanUpmonitoring
        for i in self.monitor_050_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_050_mem[i])
            except:
                pass
        for i in self.monitor_051_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_051_mem[i])
            except:
                pass
        for i in self.monitor_052_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_052_mem[i])
            except:
                pass
        for i in self.monitor_054_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_054_mem[i])
            except:
                pass
        for i in self.monitor_055_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_055_mem[i])
            except:
                pass
        for i in self.monitor_056_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_056_mem[i])
            except:
                pass
        for i in self.monitor_057_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_057_mem[i])
            except:
                pass
        for i in self.monitor_05A_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_05A_mem[i])
            except:
                pass
        for i in self.monitor_071_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_071_mem[i])
            except:
                pass
        for i in self.monitor_020_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_020_mem[i])
            except:
                pass
        eg.Wait(self.remain + 0.5)
        print self.text.readyStopped
                

    def date_Time(self,dateTimeThreadEvent):
        counter = int(time.strftime("%S", time.localtime()))
        while not dateTimeThreadEvent.isSet():
            if counter == 60:
                self.DateAndTimeInfo()
                counter = 1
            else:
                counter += 1
            time.sleep(1.0)
        print self.text.dt_threadStopped


    def keep_Alive(self,keepAliveThreadEvent): # Keep Alive Loop
        counter = 0
        while not keepAliveThreadEvent.isSet():
            if counter == 30:
                self.KeepAlive()
                counter = 0
            else:
                counter += 1
            time.sleep(1.0)
        print self.text.ka_threadStopped


    def DateAndTimeInfo(self):
        if self.use_websockets:
            currDate_Time = str(
                time.strftime(
                    "%w %Y-%m-%d %H:%M",
                    time.localtime()
                )
            )
            msg = "currDate_Time."+currDate_Time
            self.BroadcastMessage(msg)

        
    def KeepAlive(self):
        if self.use_websockets:
            msg = "KeepAlive"
            self.BroadcastMessage(msg)


    def StatusRefresh(self):
        if self.use_websockets:
            if len(self.current_state_memory) > 0:
                for i in self.current_state_memory:
                    msg = self.current_state_memory[i]
                    self.BroadcastMessage(msg)


    def SavePersistent(self, msg, m):
        #Make status data persistent if it has changed
        try:
            if msg != self.current_state_memory[m]:
                self.current_state_memory[m] = msg
                self.BroadcastMessage(msg)
        except KeyError:
            print self.text.keyAdded
            self.current_state_memory[m] = msg
            self.BroadcastMessage(msg)

       
    def BroadcastMessage(self, msg):
        try:
            p = eg.plugins.WebsocketSuite.BroadcastMessage(
                'All available interfaces',
                self.websocket_port_nbr,
                msg,
                2
            )
            if p<>0:
                print self.text.messageWebSocketBroadcastError
        except:
            print self.text.messageWebSocketError
            time.sleep(1.0)


    def OnReceive(self, serial):
        data = serial.Read(1)
        if len(str(self.out))==0:
            self.out = str(data.encode('hex'))
            self.pl = int(self.out, 16)
            time.sleep(0.002)
            data = serial.Read(self.pl)
            length = len(str(data.encode('hex')))
            if length == self.pl*2:
                for i in range(0,length):
                    self.out += str(data.encode('hex'))[i]
                if self.pl>3 and len(str(self.out)) == (self.pl+1)*2:
                    #We received a completed message
                    self.HandleChar(self.out)
                    if self.bDebug:
                        print (
                            self.text.messageDbg,
                            self.pl,
                            len(str(self.out)),
                            self.out
                        )
                else:
                    #Message is incompleted 
                    time.sleep(0.002)
                    if self.bDebug:
                        eg.PrintError (
                            self.text.messageUC+
                            str(self.pl)+' '+
                            str(len(str(self.out)))+' '+
                            self.out
                        )
        self.out = ''


    def HandleChar(self, ch):
        msg = []
        tmp = ''

        for i in ch:
            tmp+=i
            if len(tmp) == 2:
                msg.append(tmp)
                tmp=''

        if len(msg)-1 == int(msg[0], 16):

            if msg[0]== '04' and msg[1]== '02':
                self.decode_002(msg)
                return
            if msg[0]== '08' and msg[1]== '50':
                if self.b_50:
                    self.decode_050(msg)
                return
            if msg[0]== '08' and msg[1]== '51':
                if self.b_51:
                    self.decode_051(msg)
                return
            if msg[0]== '0a' and msg[1]== '52':
                if self.b_52:
                    self.decode_052(msg)
                return
            if msg[0]== '0d' and msg[1]== '54':
                if self.b_54:
                    self.decode_054(msg)
                return
            if msg[0]== '0b' and msg[1]== '55':
                if self.b_55:
                    self.decode_055(msg)
                return
            if msg[0]== '10' and msg[1]== '56':
                if self.b_56:
                    self.decode_056(msg)
                return
            if msg[0]== '09' and msg[1]== '57':
                if self.b_57:
                    self.decode_057(msg)
                return
            if msg[0]== '11' and msg[1]== '5a':
                if self.b_5A:
                    self.decode_05A(msg)
                return
            if msg[0]== '0a' and msg[1]== '71':
                if self.b_71:
                    self.decode_071(msg)
                return
            if msg[0]== '07' and msg[1]== '10':
                if self.b_10:
                    self.decode_010(msg)
                return
            if msg[0]== '0b' and msg[1]== '11':
                if self.b_11:
                    self.decode_011(msg)
                return
            if msg[0]== '08' and msg[1]== '12':
                if self.b_12:
                    self.decode_012(msg)
                return
            if msg[0]== '0a' and msg[1]== '14' and msg[2]== '00':
                if self.b_14_00:
                    self.decode_014_00(msg)
                return
            if msg[0]== '0a' and msg[1]== '14' and msg[2]== '01':
                if self.b_14_01:
                    self.decode_014_01(msg)
                return
            if msg[0]== '07' and msg[1]== '18':
                if self.b_18_19:
                    self.decode_018(msg)
                return
            if msg[0]== '09' and msg[1]== '19':
                if self.b_18_19:
                    self.decode_019(msg)
                return
            if msg[0]== '08' and msg[1]== '20':
                if self.b_20:
                    self.decode_020(msg)
                return
            if msg[1]== '01' and msg[4]== '02':
                self.decode_001(msg)
                return

            if self.bDebug:
                eg.PrintError(self.text.messageUKnwn + str(msg))
                #self.TriggerEvent(self.text.messageUKnwn + str(msg))
        else:
            eg.PrintError(self.text.messageL + str(msg))
            

    def replaceFunc(self, data):
        data = data.strip()
        if data == "CR":
            return chr(13)
        elif data == "LF":
            return chr(10)
        else:
            return None


    def WriteMsg(self, data, w_msg, w_key):
        if self.bDebug:
            print self.text.messageDbg, data
        data = data.replace(' ', '')
        data = eg.ParseString(data, self.replaceFunc)
        data = data.decode('hex')
        self.serialThread.SuspendReadEvents()
        self.serialThread.Write(str(data))
        self.serialThread.ResumeReadEvents()
        if self.use_websockets and w_msg <> '' and w_key <> '':
            self.SavePersistent(w_msg, w_key)
        


    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        logStr = timeStamp+"\t"+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\RFXtrx'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+
            self.name+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()

        
    def eventMonitor(self, monitored, decoded, base, timeout):
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            if decoded <> None:
                eg.TriggerEvent(
                    self.text.txt_signal_back+': '+base 
                )
        monitored = eg.scheduler.AddTask(
                timeout,
                eg.TriggerEvent,
                self.text.txt_taskObj+': '+base
        )
        return monitored
        

    def eventTrigger(self, decoded, base, pload):
        msg = str(base)+' : '+str(pload)
        try:
            if str(decoded)[:-2] <> pload[:-2] or self.bDupEvents:
                self.TriggerEvent(str(base), payload = str(pload))
                if self.bLogToFile:
                    self.LogToFile(msg)
                if self.use_websockets:
                    self.SavePersistent(msg, str(base))
        except:
            self.TriggerEvent(str(base), payload = str(pload))
            if self.bLogToFile:
                self.LogToFile(msg)
    

    def eventTrigger2(self, decoded, base, pload, value):
        msg = str(base)+' : '+str(pload)
        try:
            if str(decoded)[:-2] <> value[:-2] or self.bDupEvents:
                self.TriggerEvent(str(base), payload = str(pload))
                if self.bLogToFile:
                    self.LogToFile(msg)
                if self.use_websockets:
                    self.SavePersistent(msg, str(base))
        except:
            self.TriggerEvent(str(base), payload = str(pload))
            if self.bLogToFile:
                self.LogToFile(msg)


    def GetMacroIndex(self, label, name, my_macro_indx):
        if my_macro_indx == None:
            try:
                for index, m_name in enumerate(
                    eg.document.__dict__['root'].childs
                ):
                    if(
                        m_name.name.find('<') <> -1
                        and
                        m_name.name.find('>') <> -1
                    ):
                        my_macro_indx = index
                        break
            except:
                pass
            try:
                for index, m_name in enumerate(
                    eg.document.__dict__['root'].childs
                ):
                    if m_name.name == 'RFXtrx: '+label+': '+name:
                        my_macro_indx = index
                        break
            except:
                return my_macro_indx
        else:
            for index, m_name in enumerate(
                eg.document.__dict__['root'].childs
            ):
                if m_name.name == 'RFXtrx: '+label+': '+name:
                    my_macro_indx = index
        return my_macro_indx


    def SetMacroName(self, label, name, macro_indx):
        if macro_indx <> None and self.mMacroNames:
            new_name = (
                'RFXtrx: '
                +label
                +': '
                +name
            )
            eg.document.__dict__['root'].childs[macro_indx].name = new_name
            eg.document.__dict__['root'].childs[macro_indx].Refresh()


    def decode_001(self, msg):
        try:
            print(self.text.fwVersion+str(int(msg[6], 16)))
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_002(self, msg):
        if msg[0]=='04' and msg[1]=='02':
            if msg[2]=='00' or msg[2]=='01': 
                pass #message sent ok
            if msg[2]=='02' or msg[2]=='03': 
                eg.PrintError('NACK: ' + str(msg))
                
                
    def decode_050(self, msg):
        types = {
            '01': 'THR128/138, THC138',
            '02': 'THC238/268,THN132,THWR288,THRN122,THN122,AW129/131',
            '03': 'THWR800',
            '04': 'RTHN318',
            '05': 'La Crosse TX3, TX4, TX17',
            '06': 'TS15C',
            '07': 'Viking 02811',
            '08': 'La Crosse WS2300'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                    (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )

            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' signal: '+str(int(msg[8][0], 16))+
                    ' battery: '+str(int(msg[8][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_050_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_050_mem[base_msg]
                except:
                    pass
                self.monitor_050_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_050_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_051(self, msg):
        types = {
            '01': 'La Crosse TX3',
            '02': 'La Crosse WS2300'
        }
        statuses = {
            '00': 'dry',
            '01': 'comfort',
            '02': 'normal',
            '03': 'wet'        
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' humidity: '+str(int(msg[6], 16))+' %RH'+
                    ' status: '+statuses[msg[7]]+
                    ' signal: '+str(int(msg[8][0], 16))+
                    ' battery: '+str(int(msg[8][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_051_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_051_mem[base_msg]
                except:
                    pass
                self.monitor_051_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_051_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_052(self, msg):
        types = {
            '01': 'THGN122/123, THGN132, THGR122/228/238/268',
            '02': 'THGR810, THGN800',
            '03': 'RTGR328',
            '04': 'THGR328',
            '05': 'WTGR800',
            '06': 'THGR918, THGRN228, THGN500',
            '07': 'TFA TS34C, Cresta',
            '08': 'WT260, WT260H, WT440H, WT450, WT450H'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        statuses = {
            '00': 'dry',
            '01': 'comfort',
            '02': 'normal',
            '03': 'wet'        
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                    (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )
    
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' humidity: '+str(int(msg[8], 16))+' %RH'+
                    ' status: '+statuses[msg[9]]+
                    ' signal: '+str(int(msg[10][0], 16))+
                    ' battery: '+str(int(msg[10][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_052_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_052_mem[base_msg]
                except:
                    pass
                self.monitor_052_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_052_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_054(self, msg):
        types = {
            '01': 'BTHR918',
            '02': 'BTHR918N, BTHR968'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        statuses = {
            '00': 'dry',
            '01': 'comfort',
            '02': 'normal',
            '03': 'wet'        
        }
        forecasts = {
            '00': 'no forecast available',
            '01': 'sunny',
            '02': 'partly cloudy',
            '03': 'cloudy',        
            '04': 'rain'        
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            #Calculate the barometer value
            barometer = str(
            float(
                    (
                        int(msg[10], 16)*256+
                        int(msg[11], 16)
                    )
                )
            )
            
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' humidity: '+str(int(msg[8], 16))+' %RH'+
                    ' status: '+statuses[msg[9]]+
                    ' baro: '+barometer+' hPa'+
                    ' forecast: '+forecasts[msg[12]]+
                    ' signal: '+str(int(msg[13][0], 16))+
                    ' battery: '+str(int(msg[13][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_054_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_054_mem[base_msg]
                except:
                    pass
                self.monitor_054_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_054_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_055(self, msg):
        types = {
            '01': 'RGR126/682/918',
            '02': 'PCR800',
            '03': 'TFA',
            '04': 'UPM RG700',
            '05': 'La Crosse WS2300'
        }
        battery_statuses = {
            '0': '10%',
            '1': '20%',
            '2': '30%',
            '3': '40%',
            '4': '50%',
            '5': '60%',
            '6': '70%',
            '7': '80%',
            '8': '90%',
            '9': '100%'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
          
            #Get the battery status
            batt_level = battery_statuses[msg[11][1]]
    
            if int(dev_id) <> 0:
    
                if msg[2]== '01':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainrate: '+str(int(msg[6], 16)*256+
                            int(msg[7], 16))+' mm/hr'+
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                            int(msg[9], 16)*256+
                            int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
    
                if msg[2]== '02':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainrate: '+str((int(msg[6], 16)*256+
                            int(msg[7], 16))/100)+' mm/hr'+
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                            int(msg[9], 16)*256+
                            int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
    
                if msg[2]== '03' or msg[2]== '04':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                            int(msg[9], 16)*256+
                            int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_055_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_055_mem[base_msg]
                except:
                    pass
                self.monitor_055_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_055_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_056(self, msg):
        types = {
            '01': 'WTGR800',
            '02': 'WGR800',
            '03': 'STR918, WGR918',
            '04': 'TFA',
            '05': 'UPM WDS500',           
            '06': 'La Crosse WS2300'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        battery_statuses = {
            '0': '10%',
            '1': '20%',
            '2': '30%',
            '3': '40%',
            '4': '50%',
            '5': '60%',
            '6': '70%',
            '7': '80%',
            '8': '90%',
            '9': '100%'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
    
                wind_dir = float(int(msg[6], 16)*256 + int(msg[7], 16))
                strDirection = "---"

                if wind_dir > 348.75 or wind_dir < 11.26:
                    strDirection = "N"
                elif wind_dir < 33.76:
                    strDirection = "NNE"
                elif wind_dir < 56.26:
                    strDirection = "NE"
                elif wind_dir < 78.76:
                    strDirection = "ENE"
                elif wind_dir < 101.26:
                    strDirection = "E"
                elif wind_dir < 123.76:
                    strDirection = "ESE"
                elif wind_dir < 146.26:
                    strDirection = "SE"
                elif wind_dir < 168.76:
                    strDirection = "SSE"
                elif wind_dir < 191.26:
                    strDirection = "S"
                elif wind_dir < 213.76:
                    strDirection = "SSW"
                elif wind_dir < 236.26:
                    strDirection = "SW"
                elif wind_dir < 258.76:
                    strDirection = "WSW"
                elif wind_dir < 281.26:
                    strDirection = "W"
                elif wind_dir < 303.76:
                    strDirection = "WNW"
                elif wind_dir < 326.26:
                    strDirection = "NW"
                elif wind_dir < 348.76:
                    strDirection = "NNW"

                if msg[2]== '04':
                    #Get the correct sign
                    sign_bt = bin(int(msg[12], 16))[2:].zfill(8)            
                    sign = signs[sign_bt[0]]
                    
                    #Calculate the actual temperature
                    if sign == '+':
                        tempC = str(
                        float(
                            (
                                int(msg[12], 16)*256 +
                                int(msg[13], 16))/10.0
                            )
                        )
                    
                    if sign == '-':
                        tempC = str(
                        float(
                            (
                                (
                                    int(msg[12], 16) & int('7F', 16))*256 +
                                    int(msg[13], 16))/10.0
                                )
                        )
                 
                    #Get the correct chill sign
                    chill_sign_bt = bin(int(msg[14], 16))[2:].zfill(8)            
                    chill_sign = signs[chill_sign_bt[0]]
                    
                    #Calculate the actual chill
                    if chill_sign == '+':
                        chillC = str(
                        float(
                            (
                                int(msg[14], 16)*256 +
                                int(msg[15], 16))/10.0
                            )
                        )
                    
                    if chill_sign == '-':
                        chillC = str(
                        float(
                        (
                            (
                                int(msg[14], 16) & int('7F', 16))*256 +
                                int(msg[15], 16))/10.0
                            )
                        )
    
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' average speed: '+str(int(msg[8], 16)*256+
                            int(msg[9], 16)/10)+' m/s'+
                        ' gust: '+str((int(msg[10], 16)*256+
                            int(msg[11], 16))/10)+' m/s'+
                        ' temperature: '+temp_sign+tempC+' deg C'+
                        ' chill: '+chill_sign+chillC+' deg C'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )
    
                if msg[2]== '05':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' gust: '+str((int(msg[10], 16)*256+
                            int(msg[11], 16))/10)+' m/s'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )

                if msg[2]== '01' or msg[2]== '02' or msg[2]== '03':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' average speed: '+str(int(msg[8], 16)*256+
                            int(msg[9], 16)/10)+' m/s'+
                        ' gust: '+str((int(msg[10], 16)*256+
                            int(msg[11], 16))/10)+' m/s'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )

                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_056_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_056_mem[base_msg]
                except:
                    pass
                self.monitor_056_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_056_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_057(self, msg):
        types = {
            '01': 'UVN128, UV138',
            '02': 'UVN800',
            '03': 'TFA'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        try:
            uv_level = int(msg[6], 16)/10
            uv_risk = "----"

            if uv_level < 3:
                uv_risk = "Low"
            elif uv_level < 6:
                uv_risk = "Medium"
            elif uv_level < 8:
                uv_risk = "High"
            elif uv_level < 11:
                uv_risk = "Very High"
            else:
                uv_risk = "Dangerous"

            if msg[2]== '01' or msg[2]== '02':
               
                #Get the unit ID
                dev_id = str(int(msg[4], 16)*256 + int(msg[5], 16))
                
                if int(dev_id) <> 0:
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' UV level: '+str(uv_level)+
                        ' status: '+uv_risk+
                        ' signal: '+str(int(msg[9][0], 16))+
                        ' battery: '+str(int(msg[9][1], 16))
                    )

            if msg[2]== '03':

                #Get the correct sign
                sign_bt = bin(int(msg[7], 16))[2:].zfill(8)            
                sign = signs[sign_bt[0]]
                
                #Calculate the actual temperature
                if sign == '+':
                    tempC = str(
                    float(
                    (
                            int(msg[7], 16)*256 +
                            int(msg[8], 16))/10.0
                        )
                    )

                if sign == '-':
                    tempC = str(
                    float(
                    (
                        (
                            int(msg[7], 16) & int('7F', 16))*256 +
                            int(msg[8], 16))/10.0
                        )
                    )
                
                #Get the unit ID
                dev_id = str(int(msg[4], 16)*256 + int(msg[5], 16))
                
                if int(dev_id) <> 0:
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' temperature: '+sign+tempC+' deg C'+
                        ' UV level: '+str(uv_level)+
                        ' status: '+uv_risk+
                        ' signal: '+str(int(msg[9][0], 16))+
                        ' battery: '+str(int(msg[9][1], 16))
                    )

                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_057_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_057_mem[base_msg]
                except:
                    pass
                self.monitor_057_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_057_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_05A(self, msg):
        types = {
            '01': 'CM119/160'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            
            #Counter
            counter = str(int(msg[6], 16))
            
            #Instant power consumption in Watts
            instant = str("%.2f" %
                float(
                    eval('0x'+msg[7])*0x1000000+
                    eval('0x'+msg[8])*0x10000+
                    eval('0x'+msg[9])*0x100+
                    eval('0x'+msg[10])
                )
            )

            #Total energy usage in Wh
            f_usage = float(
                    eval('0x'+msg[11])*0x10000000000+
                    eval('0x'+msg[12])*0x100000000+
                    eval('0x'+msg[13])*0x1000000+
                    eval('0x'+msg[14])*0x10000+
                    eval('0x'+msg[15])*0x100+
                    eval('0x'+msg[16])
                ) / 223.666
                
            usage = str("%.2f" % f_usage)

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Counter: '+counter+
                    ' Instant power usage: '+instant+' W'+
                    ' Total energy usage: '+usage+' Wh'+
                    ' signal: '+str(int(msg[17][0], 16))+
                    ' battery: '+str(int(msg[17][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_05A_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_05A_mem[base_msg]
                except:
                    pass
                self.monitor_05A_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    600.0
                )
                self.decode_05A_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_071(self, msg):
        types = {
            '00':'RFXMeter normal data packet',
            '0f':'Identification packet'
        }
        firmware_version = (
            'RFXPower',
            'RFU',
            'RFU',
            'RFXMeter'
        )
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            dev_type = '----'

            if int(dev_id) <> 0:

                if msg[2] == '0f': #Identification packet
                    if int(msg[8], 16) <= int('3f', 16):
                        dev_type = firmware_version[0]
                    elif int(msg[8], 16) <= int('7f', 16):
                        dev_type = firmware_version[1]
                    elif int(msg[8], 16) <= int('bf', 16):
                        dev_type =firmware_version[2]
                    else:
                        dev_type = firmware_version[3]
    
                    self.rfxSensors[dev_id] = dev_type
    
                if msg[2] == '00': #Normal counter data packet
                    counter = (
                        (int(msg[6], 16) << 24) +
                        (int(msg[7], 16) << 16) +
                        (int(msg[8], 16) << 8) +
                        (int(msg[9], 16))
                    )
                    try:
                        dev_type = self.rfxSensors[dev_id]
                    except:
                        dev_type = 'RFXMeter' #default to RFXMeter
                    
                    #Look for RFXPower device
                    # -- Start JayTee
					#if self.rfxSensors[dev_id] == firmware_version[0]: 
                    #    counter = str(counter/1000)+' kWh'
                    #else:
                    #    counter = str(counter)
                    counter = str(counter/1000)+' kWh'
					# -- End JayTee
                    base_msg = (
                        'Type: '+dev_type+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' Counter: '+counter+
                        ' signal: '+str(int(msg[10][0], 16))
                    )
                    decode_param = None
                    mon_param = None

                    try:
                        decode_param = self.decode_071_mem[base_msg]
                    except:
                        pass
                    self.eventTrigger(
                        decode_param,
                        base_msg,
                        pload_msg
                    )
                    try:
                        mon_param = self.monitor_071_mem[base_msg]
                    except:
                        pass
                    self.monitor_071_mem[base_msg] = self.eventMonitor(
                        mon_param,
                        decode_param,
                        base_msg,
                        3900.0
                    )
                    self.decode_071_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_010(self, msg):
        types = {
            '00': 'X10 lighting',
            '01': 'ARC',
            '02': 'ELRO AB400D',
            '03': 'Waveman',
            '04': 'Chacon EMW200',
            '05': 'IMPULS',
            '06': 'RisingSun'
        }
        housecodes = {
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'E',
            '46': 'F',
            '47': 'G',
            '48': 'H',
            '49': 'I',
            '4a': 'J',
            '4b': 'K',
            '4c': 'L',
            '4d': 'M',
            '4e': 'N',
            '4f': 'O',
            '50': 'P'
        }            
        unitcodes = {
            '00': '00',
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'dim',
            '03': 'bright',            
            '05': 'all off',
            '06': 'all on',
            '07': 'chime'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]+
                ' command: '+commands[msg[6]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[7][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]
            )
            msg_value = (
                ' command: '+commands[msg[6]]+
                ' signal: '+str(int(msg[7][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_010_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_010_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_011(self, msg):
        types = {
            '00': 'AC',
            '01': 'HomeEasy EU',
            '02': 'ANSLUT'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'dim level',
            '03': 'group off',
            '04': 'group on',
            '05': 'group dim level'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' address: '+msg[4]+msg[5]+msg[6]+msg[7]+
                ' unit: '+unitcodes[msg[8]]+
                ' command: '+commands[msg[9]]
            )
            pload_msg = (
                ' level: '+str(int(msg[10][0], 16))+
                ' signal: '+str(int(msg[11][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' address: '+msg[4]+msg[5]+msg[6]+msg[7]+
                ' unit: '+unitcodes[msg[8]]
            )
            msg_value = (
                ' command: '+commands[msg[9]]+
                ' level: '+str(int(msg[10][0], 16))+
                ' signal: '+str(int(msg[11][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_011_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_011_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_012(self, msg):
        protocols = {
            'Koppla': '00'
        }
        systems = {
            '00': '01',
            '01': '02',
            '02': '03',
            '03': '04',
            '04': '05',
            '05': '06',
            '06': '07',
            '07': '08',
            '08': '09',
            '09': '10',
            '0A': '11',
            '0B': '12',
            '0D': '13',
            '0E': '14',
            '0F': '15',
        }            
        commands = {
            '00': 'Bright',
            '08': 'Dim',
            '10': 'On',
            '11': 'level 1',
            '12': 'level 2',
            '13': 'level 3',
            '14': 'level 4',
            '15': 'level 5',
            '16': 'level 6',
            '17': 'level 7',
            '18': 'level 8',
            '19': 'level 9',
            '1A': 'Off',
            '1C': 'Program'
        }
        try:
            base_msg = (
                'Type: '+protocols[msg[2]]+
                ' system: '+systems[msg[4]]+
                ' channel: '+str(int(msg[5], 16)*256+int(msg[6], 16))+
                ' command: '+commands[msg[7]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            msg_key = (
                'Type: '+protocols[msg[2]]+
                ' system: '+systems[msg[4]]+
                ' channel: '+str(int(msg[5], 16)*256+int(msg[6], 16))
            )
            msg_value = (
                ' command: '+commands[msg[7]]+
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_012_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_012_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_00(self, msg):
        types = {
            '00': 'LightwaveRF, Siemens'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'group Off',
            '03': 'mood1',            
            '04': 'mood2',
            '05': 'mood3',
            '06': 'mood4',
            '07': 'mood5',
            '08': 'reserved',
            '09': 'reserved',
            '0A': 'unlock',
            '0B': 'lock',
            '0C': 'all lock',
            '0D': 'close (inline relay)',
            '0E': 'stop (inline relay)',
            '0F': 'open (inline relay)',
            '10': 'set level'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' level: '+msg[9]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' level: '+msg[9]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_014_00_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_014_00_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_01(self, msg):
        types = {
            '01': 'EMW100 GAO/Everflourish'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'learn'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_014_01_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_014_01_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_018(self, msg):
        types = {
            '00': 'Harrison Curtain'
        }
        housecodes = {
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'E',
            '46': 'F',
            '47': 'G',
            '48': 'H',
            '49': 'I',
            '4a': 'J',
            '4b': 'K',
            '4c': 'L',
            '4d': 'M',
            '4e': 'N',
            '4f': 'O',
            '50': 'P'
        }            
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Program'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]+
                ' command: '+commands[msg[6]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[7][1], 16))+
                ' signal: '+str(int(msg[7][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]
            )
            msg_value = (
                ' command: '+commands[msg[6]]+
                ' battery: '+str(int(msg[7][1], 16))+
                ' signal: '+str(int(msg[7][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019(self, msg):
        types = {
            '00': 'RollerTrol'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Confirm'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+unitcodes[msg[5]]
            )
            msg_value = (
                ' command: '+commands[msg[6]]+
                ' battery: '+str(int(msg[7][1], 16))+
                ' signal: '+str(int(msg[7][0], 16))
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_020(self, msg):
        types = {
            '00': 'X10 security door/window sensor',
            '01': 'X10 security motion sensor',
            '02': 'X10 security remote',
            '03': 'KD101',
            '04': 'Visonic PowerCode door/window sensor',
            '05': 'Visonic PowerCode motion sensor',
            '06': 'Visonic CodeSecure',
            '07': 'Visonic PowerCode door/window sensor – auxiliary contact'
        }
        statuses = {
            '00': 'normal',
            '01': 'normal delayed',
            '02': 'alarm',
            '03': 'alarm delayed',
            '04': 'motion',
            '05': 'no motion',
            '06': 'panic',
            '07': 'end panic',
            '08': 'tamper',
            '09': 'arm away',
            '0A': 'arm away delayed',
            '0B': 'arm home',
            '0C': 'arm home delayed',
            '0D': 'disarm',
            '10': 'light 1 off',
            '11': 'light 1 on',
            '12': 'light 2 off',
            '13': 'light 2 on',
            '14': 'dark detected',
            '15': 'light detected',
            '16': 'battery low SD18, CO18',
            '17': 'pair KD101'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' status: '+statuses[msg[7]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]
            )
            msg_value = (
                ' status: '+statuses[msg[7]]+
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_020_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value
            )
            if (
                types[msg[2]]=='00' or
                types[msg[2]]=='01' or
                types[msg[2]]=='04' or
                types[msg[2]]=='05'
            ):
                try:
                    mon_param = self.monitor_020_mem[base_msg]
                except:
                    pass
                self.monitor_020_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    15000.0 #250 minutes timeout
                )
            self.decode_020_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def Configure(
        self,
        port = 0,
        bLogToFile = False,
        bDebug = False,
        b_50 = True,
        b_51 = True,
        b_52 = True,
        b_54 = True,
        b_55 = True,
        b_56 = True,
        b_57 = True,
        b_5A = True,
        b_10 = True,
        b_11 = True,
        b_12 = True,
        b_14_00 = True,
        b_14_01 = True,
        b_18_19 = True,
        b_20 = True,
        mMacroNames = True,
        bDupEvents = False,
        websocket_port_nbr = 1357,
        use_websockets = False,
        b_71 = True
    ):
        text = self.text
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(7, 7)
        font = panel.GetFont()
        p = font.GetPointSize()

        font.SetPointSize(8)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)

        portCtrl = panel.SerialPortChoice(port)
        panel.SetColumnFlags(1, wx.EXPAND)
        portSettingsBox = panel.BoxedGroup(
            "Port settings",
            (text.port, portCtrl),
        )
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(0))
        panel.sizer.Add(
            eg.HBoxSizer(portSettingsBox)
        )

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        staticBox = wx.StaticBox(panel, -1, self.text.logToFile)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(bLogToFileCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bDupEventsCtrl = wx.CheckBox(panel, -1, "")
        bDupEventsCtrl.SetValue(bDupEvents)
        staticBox = wx.StaticBox(panel, -1, self.text.dupEvents)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(bDupEventsCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        staticBox = wx.StaticBox(panel, -1, self.text.debugInfo)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(bDebugCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        mMacroNamesCtrl = wx.CheckBox(panel, -1, "")
        mMacroNamesCtrl.SetValue(mMacroNames)
        staticBox = wx.StaticBox(panel, -1, self.text.macroNames)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(mMacroNamesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bWebSocketCtrl.SetValue(use_websockets)
        staticBox = wx.StaticBox(panel, -1, self.text.use_websockets)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(bWebSocketCtrl, 1, wx.EXPAND)
        websocket_port_nbr_ctrl = panel.SpinIntCtrl(websocket_port_nbr, 1234, 1500)
        websocket_port_nbr_ctrl.SetInitialSize((30,-1))
        sizer2.Add(websocket_port_nbr_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        font.SetPointSize(7)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)

        b_50_Ctrl = wx.CheckBox(panel, -1, "")
        b_50_Ctrl.SetValue(b_50)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_50_0), (1,1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_50_1), (2,1))
        mySizer.Add(b_50_Ctrl, (1,0))

        b_51_Ctrl = wx.CheckBox(panel, -1, "")
        b_51_Ctrl.SetValue(b_51)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_51), (1,4))
        mySizer.Add(b_51_Ctrl, (1,3))

        b_52_Ctrl = wx.CheckBox(panel, -1, "")
        b_52_Ctrl.SetValue(b_52)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_52_0), (3,1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_52_1), (4,1))
        mySizer.Add(b_52_Ctrl, (3,0))

        b_54_Ctrl = wx.CheckBox(panel, -1, "")
        b_54_Ctrl.SetValue(b_54)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_54), (3,4))
        mySizer.Add(b_54_Ctrl, (3,3))

        b_55_Ctrl = wx.CheckBox(panel, -1, "")
        b_55_Ctrl.SetValue(b_55)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_55), (5,1))
        mySizer.Add(b_55_Ctrl, (5,0))

        b_56_Ctrl = wx.CheckBox(panel, -1, "")
        b_56_Ctrl.SetValue(b_56)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_56), (5,4))
        mySizer.Add(b_56_Ctrl, (5,3))

        b_10_Ctrl = wx.CheckBox(panel, -1, "")
        b_10_Ctrl.SetValue(b_10)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_10), (6,1))
        mySizer.Add(b_10_Ctrl, (6,0))

        b_11_Ctrl = wx.CheckBox(panel, -1, "")
        b_11_Ctrl.SetValue(b_11)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_11), (6,4))
        mySizer.Add(b_11_Ctrl, (6,3))

        b_12_Ctrl = wx.CheckBox(panel, -1, "")
        b_12_Ctrl.SetValue(b_12)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_12), (7,1))
        mySizer.Add(b_12_Ctrl, (7,0))

        b_14_00_Ctrl = wx.CheckBox(panel, -1, "")
        b_14_00_Ctrl.SetValue(b_14_00)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_14_00), (7,4))
        mySizer.Add(b_14_00_Ctrl, (7,3))

        b_14_01_Ctrl = wx.CheckBox(panel, -1, "")
        b_14_01_Ctrl.SetValue(b_14_01)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_14_01), (8,1))
        mySizer.Add(b_14_01_Ctrl, (8,0))

        b_18_19_Ctrl = wx.CheckBox(panel, -1, "")
        b_18_19_Ctrl.SetValue(b_18_19)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_18_19), (8,4))
        mySizer.Add(b_18_19_Ctrl, (8,3))

        b_20_Ctrl = wx.CheckBox(panel, -1, "")
        b_20_Ctrl.SetValue(b_20)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_20_0), (9,1))
        mySizer.Add(b_20_Ctrl, (9,0))

        b_5A_Ctrl = wx.CheckBox(panel, -1, "")
        b_5A_Ctrl.SetValue(b_5A)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_5A), (9,4))
        mySizer.Add(b_5A_Ctrl, (9,3))

        b_57_Ctrl = wx.CheckBox(panel, -1, "")
        b_57_Ctrl.SetValue(b_57)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_57), (10,1))
        mySizer.Add(b_57_Ctrl, (10,0))

        b_71_Ctrl = wx.CheckBox(panel, -1, "")
        b_71_Ctrl.SetValue(b_71)
        mySizer.Add(wx.StaticText(panel, -1, self.text.decode_71), (10,4))
        mySizer.Add(b_71_Ctrl, (10,3))

        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                bLogToFileCtrl.GetValue(),
                bDebugCtrl.GetValue(),
                b_50_Ctrl.GetValue(),                                
                b_51_Ctrl.GetValue(),                                
                b_52_Ctrl.GetValue(),                                
                b_54_Ctrl.GetValue(),                                
                b_55_Ctrl.GetValue(),                                
                b_56_Ctrl.GetValue(),                                
                b_57_Ctrl.GetValue(),                                
                b_5A_Ctrl.GetValue(),                                
                b_10_Ctrl.GetValue(),                                
                b_11_Ctrl.GetValue(),                                
                b_12_Ctrl.GetValue(),                                
                b_14_00_Ctrl.GetValue(),                                
                b_14_01_Ctrl.GetValue(),                                
                b_18_19_Ctrl.GetValue(),                                
                b_20_Ctrl.GetValue(),
                mMacroNamesCtrl.GetValue(),
                bDupEventsCtrl.GetValue(),
                websocket_port_nbr_ctrl.GetValue(),
                bWebSocketCtrl.GetValue(),
                b_71_Ctrl.GetValue()                                
            )



class send_X10(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'X10': '00'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'dim': '02',
            'bright': '03',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
       

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'X10'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off',
            'dim',
            'bright',
            'all on',
            'all off'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_X10', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_X10', nameCtrl.GetValue(), my_macro_indx
            )



class send_ARC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ARC': '01'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06',
            'chime': '07'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ARC'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off',
            'all on',
            'all off',
            'chime'
            
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ARC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ARC', nameCtrl.GetValue(), my_macro_indx
            )


class send_Waveman(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Waveman': '03'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Waveman'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Waveman', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Waveman', nameCtrl.GetValue(), my_macro_indx
            )


class send_Chacon_EMW200(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Chacon EMW200': '04'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Chacon EMW200'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on',
            'all off',
            'all on'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Chacon_EMW200', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Chacon_EMW200', nameCtrl.GetValue(), my_macro_indx
            )



class send_ELRO_AB400D(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ELRO AB400D': '02'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ELRO AB400D'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
            '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
            '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
            '63', '64'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off'            
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ELRO_AB400D', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ELRO_AB400D', nameCtrl.GetValue(), my_macro_indx
            )



class send_IMPULS(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'IMPULS': '05'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'IMPULS'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
            '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
            '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
            '63', '64'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_IMPULS', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_IMPULS', nameCtrl.GetValue(), my_macro_indx
            )



class send_RisingSun(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'RisingSun': '06'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RisingSun'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RisingSun', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RisingSun', nameCtrl.GetValue(), my_macro_indx
            )



class send_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        command,
        level,
        my_macro_indx
    ):
        protocols = {
            'AC': '00',
            'HomeEasy EU': '01',
            'ANSLUT': '02'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'set level': '02',
            'group Off': '03',
            'group On': '04',
            'Set group level': '05'
        }
        msg = (
            '0B 11 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(address)+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '0'+str(hex(int(level)))[2]+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            address+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            address+' '+
            unitcode+' '+
            command+' '+
            level
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        address="00 00 00 01",
        unitcode="",
        command="",
        level='0',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC',
            'HomeEasy EU',
            'ANSLUT'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'set level',
            'group Off',
            'group On',
            'Set group level'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(strings=list) 
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_AC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                addressCtrl.GetValue(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(), 
                levelCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_AC', nameCtrl.GetValue(), my_macro_indx
            )



class send_Koppla(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        systemcode,
        ch1,
        ch2,
        ch3,
        ch4,
        ch5,
        ch6,
        ch7,
        ch8,
        ch9,
        ch10,
        command,
        my_macro_indx
    ):
        channel_list_8_1 = []
        channel_list_9_10 = [0,0,0,0,0,0]
        str_8_1 = ''
        str_10_9 = '' 

        protocols = {
            'Koppla': '00'
        }
        systems = {
            '1': '00',
            '2': '01',
            '3': '02',
            '4': '03',
            '5': '04',
            '6': '05',
            '7': '06',
            '8': '07',
            '9': '08',
            '10': '09',
            '11': '0A',
            '12': '0B',
            '13': '0C',
            '14': '0D',
            '15': '0E',
            '16': '0F'
        }            
        commands = {
            'Bright': '00',
            'Dim': '08',
            'On': '10',
            'level 1': '11',
            'level 2': '12',
            'level 3': '13',
            'level 4': '14',
            'level 5': '15',
            'level 6': '16',
            'level 7': '17',
            'level 8': '18',
            'level 9': '19',
            'Off': '1A',
            'Program': '1C'
        }

        if ch8 == True:
            channel_list_8_1.append(1)
        elif ch8 == False:
            channel_list_8_1.append(0)
        if ch7 == True:
            channel_list_8_1.append(1)
        elif ch7 == False:
            channel_list_8_1.append(0)
        if ch6 == True:
            channel_list_8_1.append(1)
        elif ch6 == False:
            channel_list_8_1.append(0)
        if ch5 == True:
            channel_list_8_1.append(1)
        elif ch5 == False:
            channel_list_8_1.append(0)
        if ch4 == True:
            channel_list_8_1.append(1)
        elif ch4 == False:
            channel_list_8_1.append(0)
        if ch3 == True:
            channel_list_8_1.append(1)
        elif ch3 == False:
            channel_list_8_1.append(0)
        if ch2 == True:
            channel_list_8_1.append(1)
        elif ch2 == False:
            channel_list_8_1.append(0)
        if ch1 == True:
            channel_list_8_1.append(1)
        elif ch1 == False:
            channel_list_8_1.append(0)
        if ch10 == True:
            channel_list_9_10.append(1)
        elif ch10 == False:
            channel_list_9_10.append(0)
        if ch9 == True:
            channel_list_9_10.append(1)
        elif ch9 == False:
            channel_list_9_10.append(0)
        
        for item in channel_list_8_1:
            str_8_1+=str(item)
        for item in channel_list_9_10:
            str_10_9+=str(item)

        channel_8_1 = '0b'+ str_8_1       
        channel_10_9 = '0b'+ str_10_9
        
        bt_8_1 = str(hex(int('0b'+ str_8_1, 2))).split('x')[1].upper()
        bt_10_9 = str(hex(int('0b'+ str_10_9, 2))).split('x')[1].upper()
        
        if len(bt_8_1)<2:
            bt_8_1 = '0'+bt_8_1
        if len(bt_10_9)<2:
            bt_10_9 = '0'+bt_10_9

        msg = (
            '08 12 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(systems[systemcode])+' '+
            bt_8_1+' '+
            bt_10_9+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            systemcode+' '+
            bt_8_1+' '+
            bt_10_9
        )
        w_msg = (
            protocol+' '+
            systemcode+' '+
            bt_8_1+' '+
            bt_10_9+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        systemcode="",
        ch1 = False,
        ch2 = False,
        ch3 = False,
        ch4 = False,
        ch5 = False,
        ch6 = False,
        ch7 = False,
        ch8 = False,
        ch9 = False,
        ch10 = False,
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Koppla'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for system
        systemCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        systemCtrl.AppendItems(strings=list) 
        if list.count(systemcode)==0:
            systemCtrl.Select(n=0)
        else:
            systemCtrl.SetSelection(int(list.index(systemcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxSystem)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(systemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        systemCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        staticBox = wx.StaticBox(panel, -1, text.textChannel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        
        sizer3 = wx.GridBagSizer(10, 10)
        ch1_Ctrl = wx.CheckBox(panel, -1, "")
        ch1_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '1'), (0,0))
        sizer3.Add(ch1_Ctrl, (1,0))
        
        ch2_Ctrl = wx.CheckBox(panel, -1, "")
        ch2_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '2'), (0,1))
        sizer3.Add(ch2_Ctrl, (1,1))
        
        ch3_Ctrl = wx.CheckBox(panel, -1, "")
        ch3_Ctrl.SetValue(ch3)
        sizer3.Add(wx.StaticText(panel, -1, '3'), (0,2))
        sizer3.Add(ch3_Ctrl, (1,2))
        
        ch4_Ctrl = wx.CheckBox(panel, -1, "")
        ch4_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '4'), (0,3))
        sizer3.Add(ch4_Ctrl, (1,3))
        
        ch5_Ctrl = wx.CheckBox(panel, -1, "")
        ch5_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '5'), (0,4))
        sizer3.Add(ch5_Ctrl, (1,4))
        
        ch6_Ctrl = wx.CheckBox(panel, -1, "")
        ch6_Ctrl.SetValue(ch6)
        sizer3.Add(wx.StaticText(panel, -1, '6'), (0,5))
        sizer3.Add(ch6_Ctrl, (1,5))
        
        ch7_Ctrl = wx.CheckBox(panel, -1, "")
        ch7_Ctrl.SetValue(ch7)
        sizer3.Add(wx.StaticText(panel, -1, '7'), (0,6))
        sizer3.Add(ch7_Ctrl, (1,6))
        
        ch8_Ctrl = wx.CheckBox(panel, -1, "")
        ch8_Ctrl.SetValue(ch8)
        sizer3.Add(wx.StaticText(panel, -1, '8'), (0,7))
        sizer3.Add(ch8_Ctrl, (1,7))
        
        ch9_Ctrl = wx.CheckBox(panel, -1, "")
        ch9_Ctrl.SetValue(ch9)
        sizer3.Add(wx.StaticText(panel, -1, '9'), (0,8))
        sizer3.Add(ch9_Ctrl, (1,8))
        
        ch10_Ctrl = wx.CheckBox(panel, -1, "")
        ch10_Ctrl.SetValue(ch10)
        sizer3.Add(wx.StaticText(panel, -1, '10'), (0,9))
        sizer3.Add(ch10_Ctrl, (1,9))
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Bright',
            'Dim',
            'level 1',
            'level 2',
            'level 3',
            'level 4',
            'level 5',
            'level 6',
            'level 7',
            'level 8',
            'level 9',
            'Off',
            'Program'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Koppla', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                systemCtrl.GetStringSelection(),
                ch1_Ctrl.GetValue(),
                ch2_Ctrl.GetValue(),
                ch3_Ctrl.GetValue(),
                ch4_Ctrl.GetValue(),
                ch5_Ctrl.GetValue(),
                ch6_Ctrl.GetValue(),
                ch7_Ctrl.GetValue(),
                ch8_Ctrl.GetValue(),
                ch9_Ctrl.GetValue(),
                ch10_Ctrl.GetValue(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Koppla', nameCtrl.GetValue(), my_macro_indx
            )



class send_Siemens_Lightwave_RF(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        level,
        my_macro_indx
    ):
        protocols = {
            'LightwaveRF, Siemens': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group Off': '02',
            'mood1': '03',
            'mood2': '04',
            'mood3': '05',
            'mood4': '06',
            'mood5': '07',
            'reserved': '08',
            'reserved': '09',
            'unlock': '0A',
            'lock': '0B',
            'all lock': '0C',
            'close (inline relay)': '0D',
            'stop (inline relay)': '0E',
            'open (inline relay)': '0F',
            'set level': '10'
        }
        levels = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            str(levels[level])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command+' '+
            level
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        level='0',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'LightwaveRF, Siemens'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(strings=list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(strings=list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(strings=list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group Off',
            'mood1',
            'mood2',
            'mood3',
            'mood4',
            'mood5',
            'reserved',
            'reserved',
            'unlock',
            'lock',
            'all lock',
            'close (inline relay)',
            'stop (inline relay)',
            'open (inline relay)',
            'set level'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '20', '21', '22', '23', '24', '25',
            '26', '27', '28', '29', '30', '31'
        ]
        levelCtrl.AppendItems(strings=list) 
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            level = levelCtrl.GetStringSelection()
            if command <> 'set level':
                level = '0'
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Siemens_Lightwave_RF', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                command,
                level,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Siemens_Lightwave_RF', nameCtrl.GetValue(), my_macro_indx
            )



class send_EMW100_GAO_Everflourish(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'EMW100 GAO/Everflourish': '01'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'learn': '02'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'EMW100 GAO/Everflourish'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(strings=list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F'
        ]
        id_2_Ctrl.AppendItems(strings=list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(strings=list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'learn'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_EMW100_GAO_Everflourish',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_EMW100_GAO_Everflourish',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Harrison_Curtain(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Harrison Curtain': '00'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Program': '03'
        }
        msg = (
            '07 18 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Harrison Curtain'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(strings=list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Program'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Harrison_Curtain', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Harrison_Curtain', nameCtrl.GetValue(), my_macro_indx
            )



class send_RollerTrol(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'RollerTrol': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            'all units': '10'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm': '03'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RollerTrol'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(strings=list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(strings=list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(strings=list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', 'all units'
        ]
        deviceCtrl.AppendItems(strings=list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm'
        ]
        commandCtrl.AppendItems(strings=list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RollerTrol', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RollerTrol', nameCtrl.GetValue(), my_macro_indx
            )



class send_x10_security_remote(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'X10 security': '00'
        }
        statuses = {
            'panic': '06',
            'end panic': '07',
            'arm away': '09',
            'arm away delayed': '0A',
            'arm home': '0B',
            'arm home delayed': '0C',
            'disarm': '0D',
            'light 1 off': '10',
            'light 1 on': '11',
            'light 2 off': '12',
            'light 2 on': '13'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'X10 security'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(strings=list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(strings=list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'end panic', 'arm away',
            'arm away delayed', 'arm home', 'arm home delayed', 'disarm',
            'light 1 off', 'light 1 on', 'light 2 off', 'light 2 on'
        ]
        statusCtrl.AppendItems(strings=list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_x10_security_remote', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2, 
                id_3_Ctrl.GetStringSelection(), 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_x10_security_remote', nameCtrl.GetValue(), my_macro_indx
            )



class send_KD101_smoke_detector(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'KD101 smoke detector': '03'
        }
        statuses = {
            'panic': '06',
            'pair KD101': '17'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'KD101 smoke detector'
        ]
        protocolCtrl.AppendItems(strings=list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(strings=list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(strings=list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))

        sizer2.Add(id_2_Ctrl,  (0,1))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'pair KD101'
        ]
        statusCtrl.AppendItems(strings=list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_KD101_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3, 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_KD101_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class WebRefresh(eg.ActionClass):
        
    def __call__(self):
        #Refresh status with persistent data if available
        time.sleep(0.1)
        self.plugin.StatusRefresh()
        time.sleep(0.5)
        self.plugin.DateAndTimeInfo() 







