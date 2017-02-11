#
# plugins/TellStickDuo/__init__.py
#
# Copyright (C) 2010 Telldus Technologies
#
##############################################################################
# Revision history:
#
# 2011-10-18  Added support for temperature/humidity sensors
#             Events are now also generated if transmission exceptions occurs
# 2011-03-26  Improved dll-call handlings
# 2011-02-25  Improved the dimmer function (0% is off, 255% is on)
# 2010-12-14  Fixed to work with -translate switch in EG
# 2010-09-17  Added settings to select events to be logged & beep on events
#             Added settings for logfile name & path
#             Added support for Tellstick Duo id number
# 2010-05-10  Experimental with callbacks

eg.RegisterPlugin(
    name = "TellStickDuo",
    guid = '{197BDE4F-0F1A-446C-B8EE-18FDB5077A56}',
    author = "Micke Prag & Walter Krambring",
    version = "0.0.6",
    kind = "external",
    url = "http://www.eventghost.org/forum",
    description = 'Plugin for TellStick Duo',
    help = """
        <a href="http://www.telldus.se">Telldus Homepage</a>
        
        <center><img src="TellStickDuo.png" /></center>
    """,
)

TELLSTICK_SUCCESS      = 0
TELLSTICK_TURNON       = 1
TELLSTICK_TURNOFF      = 2
TELLSTICK_BELL         = 4
TELLSTICK_TOGGLE       = 8
TELLSTICK_DIM          = 16

import time, winsound, logging, os
from ctypes import(
	windll, WINFUNCTYPE, POINTER, string_at,
	wstring_at, c_char_p, c_int, c_ubyte, c_void_p,
)
from datetime import datetime



class Text:
    init_exception_txt = "TelldusCore.dll not found."
    init_txt = "Initiating TellStick Duo..."
    starting_up_txt = "Starting up..."
    starting_txt = "Starting TellStick Duo..."
    disable_txt = "Disables TellStick Duo..."
    closing_txt = "Closing TellStick Duo..."

    ON_txt = "ON"
    OFF_txt = "OFF"
    DIM_txt = "DIM"
    BELL_txt = "BELL"

    log_device_events = "Check to log device events"
    log_change_events = "Check to log change events"
    log_raw_events = "Check to log raw events"
    beep_device_events = "Check to beep on device events"

    path_txt = "Enter path and logfile name"
    device_txt = "Device:"
    retry_txt = "Retry nbr: "
    exception_txt = "An error occurred while trying to transmit"
    no_device_txt_1 =  "There is no device supporting '"
    no_device_txt_2 =  "'"
    no_device_txt_3 =  " . Click CANCEL to close dialogue"

    class Dim:
        dim_txt_1 = "Dim " 
        dim_txt_2 = " to "
        dim_txt_3 = "%"
        level_txt = "Level:"


DEVICEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        c_int,
                                        c_int,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_void_p
                     )

SENSOREVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        POINTER(c_ubyte),
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        c_void_p
                     )

DEVICECHANGEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        c_int,
                                        c_int,
                                        c_int,
                                        c_int,
                                        c_void_p
                    )

RAWDEVICEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        c_void_p
                     )



class TellStickDuo(eg.PluginClass):
    text = Text
 
    def __init__(self):
        self.AddAction(TurnOn)
        self.AddAction(Dim)
        self.AddAction(TurnOff)
        self.AddAction(Bell)
        self.bRawEvents = False
        self.dll = None
        self.callbackId_0 = None
        self.callbackId_1 = None
        self.callbackId_2 = None
        self.callbackId_3 = None
        try:
            self.dll = windll.LoadLibrary("TelldusCore.dll")
        except: 
            raise eg.Exception(self.text.init_exception_txt)
        self.dll.tdInit()
        self.deviceEventProc = DEVICEEVENTPROC(
                                        self.deviceEventCallback
                               )
        self.deviceChangeEventProc = DEVICECHANGEEVENTPROC(
                                            self.deviceChangeEventCallback
                                     )
        self.deviceRawEventProc = RAWDEVICEEVENTPROC(
                                        self.deviceRawEventCallback
                                  )
        self.sensorEventProc = SENSOREVENTPROC(
                                        self.sensorEventCallback
                               )
        self.callbackId_0 = self.dll.tdRegisterDeviceEvent(
                                        self.deviceEventProc,
                                        0
                            )        
#        self.callbackId_1 = self.dll.tdRegisterDeviceChangeEvent(
#                                        self.deviceChangeEventProc,
#                                        0
#                            )        
        self.callbackId_2 = self.dll.tdRegisterRawDeviceEvent(
                                        self.deviceRawEventProc,
                                        0
                            )        
        self.callbackId_3 = self.dll.tdRegisterSensorEvent(
                                        self.sensorEventProc,
                                        0
                            )        

        print self.text.init_txt


    def __start__(
        self,
        bDeviceEvents,
        bChangeEvents,
        bRawEvents,
        beepOnEvent,
        pathToLogfile
    ):
        self.bDeviceEvents = bDeviceEvents
        self.bChangeEvents = bChangeEvents
        self.bRawEvents = bRawEvents
        self.beepOnEvent = beepOnEvent
        self.pathToLogfile = pathToLogfile

        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileHandle = None
        pl = self.pathToLogfile.split('/')
        if(
            not os.path.exists('/'+str(pl[1])+'/')
            and
            not os.path.isdir('/'+str(pl[1])+'/')
        ):
            os.mkdir('/'+str(pl[1])+'/')
        fileHandle = open(self.pathToLogfile, 'a')
        fileHandle.close()

        LOG_FILENAME = self.pathToLogfile
        logging.basicConfig(
            filename=LOG_FILENAME,
            filemode='a',
            level=logging.DEBUG
        )
        logging.info(timeStamp+": "+self.text.starting_up_txt)
        print self.text.starting_txt


    def __stop__(self):
        print self.text.disable_txt
        

    def __close__(self):
        unReg_0 = self.dll.tdUnregisterCallback( self.callbackId_0 )
        unReg_1 = self.dll.tdUnregisterCallback( self.callbackId_1 )
        unReg_2 = self.dll.tdUnregisterCallback( self.callbackId_2 )
        unReg_3 = self.dll.tdUnregisterCallback( self.callbackId_3 )
        self.dll.tdClose()
        print self.text.closing_txt


    def deviceEventCallback(self, deviceId, method, p1, i3, p2):
        deviceName = (c_char_p(self.dll.tdGetName(deviceId))).value
        if (method == TELLSTICK_TURNON):
            strMethod = self.text.ON_txt
        elif (method == TELLSTICK_TURNOFF):
            strMethod = self.text.OFF_txt
        elif (method == TELLSTICK_DIM):
            strMethod = self.text.DIM_txt
        elif (method == TELLSTICK_BELL):
            strMethod = self.text.BELL_txt
        else:
            return
        deviceType = (c_char_p(self.dll.tdGetModel(deviceId))).value
        if self.bDeviceEvents:
            self.TriggerEvent(
                deviceName
                +'.'
                +strMethod,
                payload=(
                    str(deviceType)
                    +'.'
                    +str(deviceId)
                )
            )
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logging.info(
                timeStamp
                +": "
                +deviceName
                +'.'
                +strMethod
                +'.'
                +str(deviceType)
                +'.'
                +str(deviceId)
            )
            if self.beepOnEvent:
                winsound.Beep(1000, 200)                


    def sensorEventCallback(
        self,
        protocol,
        model,
        id,
        dataType,
        value,
        timestamp,
        callbackId,
        context
    ):
        if self.bDeviceEvents:
            TELLSTICK_TEMPERATURE = 1
            TELLSTICK_HUMIDITY = 2
            strProtocol = string_at(protocol)
            strModel = string_at(model)
            strValue = string_at(value)
            dType = ''
            if(dataType == TELLSTICK_TEMPERATURE):
                dType = "Temperature:"
            elif(dataType == TELLSTICK_HUMIDITY):
                dType = "Humidity:"
            
            self.TriggerEvent(
                strProtocol
                +'.'
                +strModel
                +'.'
                +str(id)
                +'.'
                +dType,
                payload=(
                    strValue
                    +'|'
                    +str(datetime.fromtimestamp(timestamp))
                )
            )

            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logging.info(
                timeStamp
                +": "
                +strProtocol
                +'.'
                +strModel
                +'.'
                +str(id)
                +'.'
                +dType
                +'.'
                +strValue
            )
            if self.beepOnEvent:
                winsound.Beep(1000, 200)                


    def deviceChangeEventCallback(self, deviceId, changeEvent, i3, i4, p1):
        deviceName = (c_char_p(self.dll.tdGetName(deviceId))).value
        deviceType = (c_char_p(self.dll.tdGetModel(deviceId))).value
        if self.bChangeEvents:
            self.TriggerEvent(
                "ChangeEvent: "
                + str(deviceType)
                + str(deviceName)
                + str(changeEvent)
            )
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logging.info(
                timeStamp
                + ": ChangeEvent: "
                + str(deviceType)
                + str(deviceName)
                + str(changeEvent)
            )


    def deviceRawEventCallback(self, p1, i1, i2, p3):
        strData = string_at(p1)
        if (strData == ""):
            return
        if self.bRawEvents:
            self.TriggerEvent(
                "RawEvent: "
                + strData
                + "Duo_ID:"
                + str(i2)
            )
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logging.info(
                timeStamp
                + ": RawEvent: "
                + strData
                + "Duo_ID:"
                + str(i2)
            )
  

    def Configure(
        self,
        bDeviceEvents = True,
        bChangeEvents = True,
        bRawEvents = False,
        beepOnEvent = False,
        pathToLogfile = '/tmp/logging_tellstick_duo.txt',
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer_1 = wx.GridBagSizer(5, 5)

        bDeviceEventsCtrl = wx.CheckBox(panel, -1, "")
        bDeviceEventsCtrl.SetValue(bDeviceEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_device_events
            ),
            (1,0)
        )
        mySizer_1.Add(bDeviceEventsCtrl, (1,1))

        bChangeEventsCtrl = wx.CheckBox(panel, -1, "")
        bChangeEventsCtrl.SetValue(bChangeEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_change_events
            ),
            (2,0)
        )
        mySizer_1.Add(bChangeEventsCtrl, (2,1))

        bRawEventsCtrl = wx.CheckBox(panel, -1, "")
        bRawEventsCtrl.SetValue(bRawEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_raw_events
            ),
            (3,0)
        )
        mySizer_1.Add(bRawEventsCtrl, (3,1))
       
        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(beepOnEvent)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.beep_device_events
            ),
            (4,0)
        )
        mySizer_1.Add(bSoundCtrl, (4,1))

        pathToLogfileCtrl = wx.TextCtrl(panel, -1, pathToLogfile)
        pathToLogfileCtrl.SetInitialSize((300,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.path_txt
            ),
           (5,0)
        )
        mySizer_1.Add(pathToLogfileCtrl,(5,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            bDeviceEvents = bDeviceEventsCtrl.GetValue()
            bChangeEvents = bChangeEventsCtrl.GetValue()
            bRawEvents = bRawEventsCtrl.GetValue()
            beepOnEvent = bSoundCtrl.GetValue()
            pathToLogfile = pathToLogfileCtrl.GetValue()
            panel.SetResult(
                bDeviceEvents,
                bChangeEvents,
                bRawEvents,
                beepOnEvent,
                pathToLogfile
            )

         

class DeviceBase(object):

    def GetLabel(self, device):
        return (
            self.name 
            + " " 
            + (c_char_p(self.plugin.dll.tdGetName(device))).value
        )


    def Configure(self, device=0):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_TURNON
                            | TELLSTICK_TURNOFF
                            | TELLSTICK_BELL
                            | TELLSTICK_TOGGLE
                            | TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (id == device):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)

        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)

        if (len(deviceList) > 0):
            panel.sizer.Add(
                wx.StaticText(panel, -1, self.plugin.text.device_txt), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        else:
            panel.sizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1
                    + self.name
                    + self.plugin.text.no_device_txt_2
                    + self.plugin.text.no_device_txt_3
                ), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        panel.sizer.Add(deviceCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                panel.SetResult(device)
            else:
                device = 0

            

class TurnOn(DeviceBase, eg.ActionClass):
    name = "Turn on"
    description = "Turns on a TellStick device."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def __call__(self, device):
        for i in range(5):
            if i>0:
                print self.plugin.text.retry_txt, i
            ret = self.plugin.dll.tdTurnOn(device)
            if (ret != TELLSTICK_SUCCESS and i == 4):
                raise eg.Exception(self.plugin.text.exception_txt)
                self.plugin.TriggerEvent(self.plugin.text.exception_txt)
            if(ret == TELLSTICK_SUCCESS):
                break



class TurnOff(DeviceBase, eg.ActionClass):
    name = "Turn off"
    description = "Turns off a TellStick device."
    iconFile = "lamp-off"
    method = TELLSTICK_TURNOFF

    def __call__(self, device):
        for i in range(5):
            if i>0:
                print self.plugin.text.retry_txt, i
            ret = self.plugin.dll.tdTurnOff(device)
            if (ret != TELLSTICK_SUCCESS and i == 4):
                raise eg.Exception(self.plugin.text.exception_txt)
                self.plugin.TriggerEvent(self.plugin.text.exception_txt)
            if(ret == TELLSTICK_SUCCESS):
                break



class Bell(DeviceBase, eg.ActionClass):
    name = "Bell"
    description = "Sends bell to a TellStick device."
    iconFile = "bell"
    method = TELLSTICK_BELL

    def __call__(self, device):
        for i in range(5):
            if i>0:
                print self.plugin.text.retry_txt, i
            ret = self.plugin.dll.tdBell(device)
            if (ret != TELLSTICK_SUCCESS and i == 4):
                raise eg.Exception(self.plugin.text.exception_txt)
                self.plugin.TriggerEvent(self.plugin.text.exception_txt)
            if(ret == TELLSTICK_SUCCESS):
                break



class Dim(eg.ActionClass):
    name = "Dim"
    description = "Dims a TellStick device."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, device, level):
        for i in range(5):
            if i>0:
                print self.plugin.text.retry_txt, i
            if level == 0:
                ret = self.plugin.dll.tdTurnOff(device)
            if level > 0 and level < 255 :
                ret = self.plugin.dll.tdDim(device, level)
            if level == 255:
                ret = self.plugin.dll.tdTurnOn(device)
            if (ret != TELLSTICK_SUCCESS and i == 4):
                raise eg.Exception(self.plugin.text.exception_txt)
                self.plugin.TriggerEvent(self.plugin.text.exception_txt)
            if(ret == TELLSTICK_SUCCESS):
                break


    def GetLabel(self, device, level):
        percent = int((level*100)/256)
        return (
            self.text.dim_txt_1 
            + (c_char_p(self.plugin.dll.tdGetName(device))).value
            + self.text.dim_txt_2
            + str(percent)
            + self.text.dim_txt_3
        )


    def Configure(self, device=0, level=128):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_TURNON
                            | TELLSTICK_TURNOFF
                            | TELLSTICK_BELL
                            | TELLSTICK_TOGGLE
                            | TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (id == device):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)

        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        levelCtrl = wx.Slider(panel, -1, level, 0, 255)

        if (len(deviceList) > 0):
            panel.sizer.Add(
                wx.StaticText(panel, -1, self.plugin.text.device_txt), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        else:
            panel.sizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1
                    + self.name
                    + self.plugin.text.no_device_txt_2
                    + self.plugin.text.no_device_txt_3
                ), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )

        panel.sizer.Add(deviceCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.level_txt), 
            0, 
            wx.ALIGN_CENTER_VERTICAL
        )
        panel.sizer.Add(levelCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                level = levelCtrl.GetValue()
                panel.SetResult(device, level)
            else:
                device = 0
