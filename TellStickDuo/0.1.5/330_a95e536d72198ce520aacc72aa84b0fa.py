#
# plugins/TellStickDuo/__init__.py
#
# Copyright (C) 2010 Telldus Technologies
#
##############################################################################
# Revision history:
#
# 2012-09-08  Improved the handling of repeated events for devices and sensors.
# 2012-08-14  Added actions for dimming Good Morning and Good Night lamps.
#             (works with AC devices like NEXA with support for setting dim
#             levels).
# 2012-07-01  Moving event callback initiators from init to start method.
#             Enabled UnregisterCallbacks in stop method.
# 2012-02-26  Changing the dim level now also updates the macro name with
#             correct % level.
#             Dimmer function 100% represents full dim level, 0% is off. 
# 2012-01-26  Checkboxes for selection of event types and blocking of repeats
#             did not work correctly.
# 2012-01-24  Added support for UP/DOWN/STOP actions.
# 2011-11-14  Using device names as keys instead of device id's.
#             Changed the slider for dim to show 0-100% dim level.
#             Improved the blocking of repeated events, blocking all repeated
#             events within the defined time frame except change events.
# 2011-10-28  Blocking repeated events: configuration option added.
# 2011-10-26  Blocking repeated events within 0.3 seconds.
# 2011-10-18  Added support for temperature/humidity sensors.
#             Events are now also generated if transmission exceptions occurs.
# 2011-03-26  Improved dll-call handlings.
# 2011-02-25  Improved the dimmer function (0% is off, 255% is on).
# 2010-12-14  Fixed to work with -translate switch in EG.
# 2010-09-17  Added settings to select events to be logged & beep on events.
#             Added settings for logfile name & path.
#             Added support for Tellstick Duo id number.
# 2010-05-10  Experimental with callbacks.

eg.RegisterPlugin(
    name = "TellStickDuo",
    guid = '{197BDE4F-0F1A-446C-B8EE-18FDB5077A56}',
    author = "Micke Prag & Walter Kraembring",
    version = "0.1.5",
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
TELLSTICK_LEARN        = 32
TELLSTICK_EXECUTE      = 64
TELLSTICK_UP           = 128
TELLSTICK_DOWN         = 256
TELLSTICK_STOP         = 512


import time, winsound, logging, os
from ctypes import(
	windll, WINFUNCTYPE, POINTER, string_at,
	wstring_at, c_char_p, c_int, c_ubyte, c_void_p	
)
from datetime import datetime
from win32gui import MessageBox
from threading import Event, Thread



class Text:
    init_exception_txt = "TelldusCore.dll not found."
    init_txt = "Initiating TellStick Duo..."
    starting_up_txt = "Starting up..."
    starting_txt = "Starting TellStick Duo..."
    disable_txt = "Disables TellStick Duo..."
    closing_txt = "Closing TellStick Duo..."
    restart_title = "Restart of EG needed"
    restart_eg = (
        "Please finish and save the configuration and then restart "
        +"EventGhost to enable the event receiving capabilities in "
        +"TellStick Duo."
    )

    ON_txt = "ON"
    OFF_txt = "OFF"
    DIM_txt = "DIM"
    BELL_txt = "BELL"
    UP_txt = "UP"
    DOWN_txt = "DOWN"
    STOP_txt = "STOP"

    log_device_events = "Check to log device events"
    log_delayRepeat = "Delay between events (0.1-15.0 s)"
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
        level_txt = "Dim level (%): "

    class Dim:
        dim_txt_1 = "Dim " 
        dim_txt_2 = " to "
        dim_txt_3 = "%"
        level_txt = "Dim level (%): "

    class GoodMorning:
        dim_txt_1 = "Good morning " 
        dim_txt_2 = "in "
        dim_txt_3 = " minutes"
        timeToWakeUp_txt = "Total snooze time (minutes): "

    class GoodNight:
        dim_txt_1 = "Good night " 
        dim_txt_2 = "in "
        dim_txt_3 = " minutes"
        timeToSleep_txt = "Total snooze time (minutes): "

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
    taskObj = None
 
    def __init__(self):
        self.AddAction(GoodMorning)
        self.AddAction(GoodNight)
        self.AddAction(TurnOn)
        self.AddAction(Dim)
        self.AddAction(TurnOff)
        self.AddAction(Bell)
        self.AddAction(MoveUp)
        self.AddAction(MoveDown)
        self.AddAction(Stop)
 

    def __start__(
        self,
        bDeviceEvents,
        bChangeEvents,
        bRawEvents,
        beepOnEvent,
        pathToLogfile,
        delayRepeat
    ):
        self.bDeviceEvents = bDeviceEvents
        self.bChangeEvents = bChangeEvents
        self.bRawEvents = bRawEvents
        self.beepOnEvent = beepOnEvent
        self.pathToLogfile = pathToLogfile
        self.delayRepeat = delayRepeat

        self.oldDeviceEventCollection = []
        self.oldDeviceSensorEventCollection = []

        self.bTaskAddedRaw = False
        self.oldDeviceEventRaw = ''

        self.taskObj = None
        self.taskObjSensors = None
        self.taskObjRaw = None
        
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

        self.dll = None
        self.callbackId_0 = None
        self.callbackId_1 = None
        self.callbackId_2 = None
        self.callbackId_3 = None
        try:
            self.dll = windll.LoadLibrary("TelldusCore.dll")
        except: 
            raise eg.Exception(self.text.init_exception_txt)
        self.handle = self.dll._handle
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
        try:
            self.callbackId_0 = self.dll.tdRegisterDeviceEvent(
                                            self.deviceEventProc,
                                            0
                                )        
        except: 
            print self.text.restart_title
            MessageBox(0, self.text.restart_eg, self.text.restart_title, 0)
        try:
            self.callbackId_1 = self.dll.tdRegisterDeviceChangeEvent(
                                            self.deviceChangeEventProc,
                                            0
                                )        
        except: 
            pass
        try:
            self.callbackId_2 = self.dll.tdRegisterRawDeviceEvent(
                                            self.deviceRawEventProc,
                                            0
                                )        
        except: 
            pass
        try:
            self.callbackId_3 = self.dll.tdRegisterSensorEvent(
                                            self.sensorEventProc,
                                            0
                                )        
        except: 
            pass

        print self.text.init_txt

        logging.info(timeStamp+": "+self.text.starting_up_txt)
        print self.text.starting_txt


    def __stop__(self):
        unReg_0 = self.dll.tdUnregisterCallback( self.callbackId_0 )
        unReg_1 = self.dll.tdUnregisterCallback( self.callbackId_1 )
        unReg_2 = self.dll.tdUnregisterCallback( self.callbackId_2 )
        unReg_3 = self.dll.tdUnregisterCallback( self.callbackId_3 )
        self.CancelTasks()
        print self.text.disable_txt
        
   
    def __close__(self):
        self.__stop__()
#        unReg_0 = self.dll.tdUnregisterCallback( self.callbackId_0 )
#        unReg_1 = self.dll.tdUnregisterCallback( self.callbackId_1 )
#        unReg_2 = self.dll.tdUnregisterCallback( self.callbackId_2 )
#        unReg_3 = self.dll.tdUnregisterCallback( self.callbackId_3 )
        try:
            self.dll.tdClose()
        except:
            pass
        del self.dll
        print self.text.closing_txt


    def CancelTasks(self):
        try:
            eg.scheduler.CancelTask(self.taskObj)
        except ValueError:
            pass
        try:
            eg.scheduler.CancelTask(self.taskObjSensors)
        except ValueError:
            pass
        try:
            eg.scheduler.CancelTask(self.taskObjRaw)
        except ValueError:
            pass


    def ClearFlagRaw(self):
        #print "Clear FlagRaw", self.bTaskAddedRaw
        self.bTaskAddedRaw = False


    def RemoveEventFromCollection(self, item):
        try:
            self.oldDeviceEventCollection.remove(item)
        except:
            pass


    def RemoveSensorEventFromCollection(self, item):
        try:
            self.oldDeviceSensorEventCollection.remove(item)
        except:
            pass


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
        elif (method == TELLSTICK_DOWN):
            strMethod = self.text.DOWN_txt
        elif (method == TELLSTICK_UP):
            strMethod = self.text.UP_txt
        elif (method == TELLSTICK_STOP):
            strMethod = self.text.STOP_txt
        else:
            return
        deviceType = (c_char_p(self.dll.tdGetModel(deviceId))).value

        eventStr = (
            deviceName
            +'.'
            +strMethod
            +'.'
            +str(deviceType)
            +'.'
            +str(deviceId)
        )

        if(self.bDeviceEvents):
            if self.delayRepeat > 0:
                if eventStr not in self.oldDeviceEventCollection:
                    self.oldDeviceEventCollection.append(eventStr)
                    #Schedule the event removal task
                    self.taskObj = eg.scheduler.AddTask(
                        self.delayRepeat,
                        self.RemoveEventFromCollection,
                        eventStr
                    )
                else:
                    return

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
            
        eventStr = (
            strProtocol
            +'.'
            +strModel
            +'.'
            +str(id)
            +'.'
            +dType
            +'.'
            +strValue
        )

        if(self.bDeviceEvents):
            if self.delayRepeat > 0:
                if eventStr not in self.oldDeviceSensorEventCollection:
                    self.oldDeviceSensorEventCollection.append(eventStr)
                    #Schedule the sensor event removal task
                    self.taskObjSensors = eg.scheduler.AddTask(
                        self.delayRepeat,
                        self.RemoveSensorEventFromCollection,
                        eventStr
                    )
                else:
                    return

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


    def deviceRawEventCallback(self, p1, i1, i2, p3):
        strData = string_at(p1)
        if (strData == ""):
            return

        if(self.bRawEvents):
            if(
                (strData <> self.oldDeviceEventRaw)
                    or
                (strData == self.oldDeviceEventRaw
                    and
                 self.bTaskAddedRaw == False)
            ):
                self.bTaskAddedRaw = True
                try:
                    eg.scheduler.CancelTask(self.taskObjRaw)
                    #print "taskObjRaw cancelled"
                except ValueError:
                    pass
                self.oldDeviceEventRaw = strData
    
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
    
                if self.bTaskAddedRaw:
                    self.taskObjRaw = eg.scheduler.AddTask(
                        self.delayRepeat,
                        self.ClearFlagRaw
                    )
                else:
                    self.bTaskAddedRaw = False


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


    def getId(self, deviceName, method):
        self.method = method
        try:
            numDevices = self.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.dll.tdGetDeviceId(i)
            methods = self.dll.tdMethods(
                id,
                TELLSTICK_TURNON
                | TELLSTICK_TURNOFF
                | TELLSTICK_BELL
                | TELLSTICK_TOGGLE
                | TELLSTICK_DIM
                | TELLSTICK_DOWN
                | TELLSTICK_UP
                | TELLSTICK_STOP
            )
            if (methods & self.method):
                name = (c_char_p(self.dll.tdGetName(id))).value
                if (name == deviceName):
                    return id        


    def sendCommand(self, id, command, level):
        ret = None
        if command == 'On' or command == 'Off':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if command == 'On':
                    ret = self.dll.tdTurnOn(id)
                else:
                    ret = self.dll.tdTurnOff(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    raise eg.Exception(self.text.exception_txt)
                    self.TriggerEvent(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Dim':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if level == 0:
                    ret = self.dll.tdTurnOff(id)
                if level > 0 and level < 256 :
                    ret = self.dll.tdDim(id, level)
                if level == 256:
                    ret = self.dll.tdDim(id, level)
#                    ret = self.dll.tdTurnOn(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    raise eg.Exception(self.text.exception_txt)
                    self.TriggerEvent(self.text.exception_txt)
                if (ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Bell':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                ret = self.dll.tdBell(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    raise eg.Exception(self.text.exception_txt)
                    self.TriggerEvent(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Up' or command == 'Down':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if command == 'Up':
                    ret = self.dll.tdUp(id)
                else:
                    ret = self.dll.tdDown(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    raise eg.Exception(self.text.exception_txt)
                    self.TriggerEvent(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Stop':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                ret = self.dll.tdStop(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    raise eg.Exception(self.text.exception_txt)
                    self.TriggerEvent(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break


    def Configure(
        self,
        bDeviceEvents = True,
        bChangeEvents = True,
        bRawEvents = False,
        beepOnEvent = False,
        pathToLogfile = '/tmp/logging_tellstick_duo.txt',
        delayRepeat = 0.3,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer_1 = wx.GridBagSizer(5, 5)

        delayRepeatCtrl = panel.SpinNumCtrl(
            delayRepeat,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.0,
            max = 15.0,
            increment = 0.1
        )
        delayRepeatCtrl.SetValue(delayRepeat)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_delayRepeat
            ),
            (1,0)
        )
        mySizer_1.Add(delayRepeatCtrl, (1,1))

        bDeviceEventsCtrl = wx.CheckBox(panel, -1, "")
        bDeviceEventsCtrl.SetValue(bDeviceEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_device_events
            ),
            (2,0)
        )
        mySizer_1.Add(bDeviceEventsCtrl, (2,1))

        bChangeEventsCtrl = wx.CheckBox(panel, -1, "")
        bChangeEventsCtrl.SetValue(bChangeEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_change_events
            ),
            (3,0)
        )
        mySizer_1.Add(bChangeEventsCtrl, (3,1))

        bRawEventsCtrl = wx.CheckBox(panel, -1, "")
        bRawEventsCtrl.SetValue(bRawEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_raw_events
            ),
            (4,0)
        )
        mySizer_1.Add(bRawEventsCtrl, (4,1))
       
        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(beepOnEvent)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.beep_device_events
            ),
            (5,0)
        )
        mySizer_1.Add(bSoundCtrl, (5,1))

        pathToLogfileCtrl = wx.TextCtrl(panel, -1, pathToLogfile)
        pathToLogfileCtrl.SetInitialSize((200,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.path_txt
            ),
           (6,0)
        )
        mySizer_1.Add(pathToLogfileCtrl,(6,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            bDeviceEvents = bDeviceEventsCtrl.GetValue()
            bChangeEvents = bChangeEventsCtrl.GetValue()
            bRawEvents = bRawEventsCtrl.GetValue()
            beepOnEvent = bSoundCtrl.GetValue()
            pathToLogfile = pathToLogfileCtrl.GetValue()
            delayRepeat = delayRepeatCtrl.GetValue()
            panel.SetResult(
                bDeviceEvents,
                bChangeEvents,
                bRawEvents,
                beepOnEvent,
                pathToLogfile,
                delayRepeat
            )

         

class DeviceBase(object):

    def GetLabel(self, deviceName):
        return (
            self.name 
            + " " 
            + str(deviceName)
        )


    def Configure(self, deviceName=''):
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
                            | TELLSTICK_DOWN
                            | TELLSTICK_UP
                            | TELLSTICK_STOP
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (name == deviceName):
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
                deviceName = (
                    (c_char_p(self.plugin.dll.tdGetName(device))).value
                )
                panel.SetResult(deviceName)
            else:
                deviceName = ''

            

class TurnOn(DeviceBase, eg.ActionClass):
    name = "Turn on"
    description = "Turns on a TellStick device."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'On', None)



class TurnOff(DeviceBase, eg.ActionClass):
    name = "Turn off"
    description = "Turns off a TellStick device."
    iconFile = "lamp-off"
    method = TELLSTICK_TURNOFF

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Off', None)



class MoveDown(DeviceBase, eg.ActionClass):
    name = "Move down"
    description = "Start moving down."
    iconFile = "down"
    method = TELLSTICK_DOWN

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Down', None)



class MoveUp(DeviceBase, eg.ActionClass):
    name = "Move up"
    description = "Start moving up."
    iconFile = "up"
    method = TELLSTICK_UP

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Up', None)



class Stop(DeviceBase, eg.ActionClass):
    name = "Stop movement"
    description = "Stops the movement."
    iconFile = "stop"
    method = TELLSTICK_STOP

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Stop', None)



class Bell(DeviceBase, eg.ActionClass):
    name = "Bell"
    description = "Sends bell to a TellStick device."
    iconFile = "bell"
    method = TELLSTICK_BELL

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Bell', None)



class Dim(eg.ActionClass):
    name = "Dim"
    description = "Dims a TellStick device."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, level):
        level = int(level*256/100)
        id = self.plugin.getId(deviceName, self.method)
        self.plugin.sendCommand(id, 'Dim', level)


    def GetLabel(self, deviceName, level):
        percent = int(level)
        return (
            self.text.dim_txt_1 
            + str(deviceName)
            + self.text.dim_txt_2
            + str(percent)
            + self.text.dim_txt_3
        )


    def Configure(self, deviceName = '', level=50):
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
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (name == deviceName):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.levelCtrl = wx.Slider(
                            panel,
                            -1,
                            level,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1
                    + self.name
                    + self.plugin.text.no_device_txt_2
                    + self.plugin.text.no_device_txt_3
                ), (1,0)
            )

        mySizer.Add(deviceCtrl, (1,1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.level_txt
            ), (3,0)
        ) 
        mySizer.Add(self.levelCtrl, (3,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                deviceName = (
                    (c_char_p(self.plugin.dll.tdGetName(device))).value
                )
                level = self.levelCtrl.GetValue()
                panel.SetResult(deviceName, level)
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Dim')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: Dim '
                            +deviceName
                            +' to '
                            +str(level)
                            +'%'
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class GoodMorning(eg.ActionClass):
    name = "GoodMorning"
    description = "Dims a TellStick device stepwise delayed until full level."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, timeToWakeUp):
        self.increase = int(256/(timeToWakeUp*3))
        self.id = self.plugin.getId(deviceName, self.method)
        self.finished = Event()
        self.GoodMorning = Thread(
            target=self.GoodMorningThread,
            name="GoodMorning"
        )
        self.GoodMorning.start()


    def GetLabel(self, deviceName, level):
        percent = int(level)
        return (
            self.text.dim_txt_1 
            + self.text.dim_txt_2
            + str(percent)
            + self.text.dim_txt_3
            + '. Device: '
            + str(deviceName)
        )


    def GoodMorningThread(self):
        while not self.finished.isSet():
            level=1
            while level < 256:
                #print level
                self.plugin.sendCommand(self.id, 'Dim', level)
                level += self.increase
                self.finished.wait(20.0)
            self.finished.set()
            time.sleep(0.1)
            self.plugin.sendCommand(self.id, 'Dim', 255)
            print "Good Morning action finished"
            

    def Configure(self, deviceName = '', timeToWakeUp = 15):
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
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (name == deviceName):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.timeToWakeUpCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToWakeUp,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1
                    + self.name
                    + self.plugin.text.no_device_txt_2
                    + self.plugin.text.no_device_txt_3
                ), (1,0)
            )
       
        mySizer.Add(deviceCtrl, (1,1))
        
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.timeToWakeUp_txt
            ), (3,0)
        ) 
        mySizer.Add(self.timeToWakeUpCtrl, (3,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                deviceName = (
                    (c_char_p(self.plugin.dll.tdGetName(device))).value
                )
                timeToWakeUp = self.timeToWakeUpCtrl.GetValue()
                panel.SetResult(deviceName, timeToWakeUp)
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Good morning')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: '
                            +'Good morning in '
                            +str(timeToWakeUp)
                            +' minutes.'
                            +' Device: '
                            +deviceName
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class GoodNight(eg.ActionClass):
    name = "GoodNight"
    description = "Dims a TellStick device stepwise delayed until turned off."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, timeToSleep):
        self.decrease = int(256/(timeToSleep*3))
        self.id = self.plugin.getId(deviceName, self.method)
        self.finished = Event()
        self.GoodNight = Thread(
            target=self.GoodNightThread,
            name="GoodNight"
        )
        self.GoodNight.start()


    def GetLabel(self, deviceName, level):
        percent = int(level)
        return (
            self.text.dim_txt_1 
            + self.text.dim_txt_2
            + str(percent)
            + self.text.dim_txt_3
            + '. Device: '
            + str(deviceName)
        )


    def GoodNightThread(self):
        while not self.finished.isSet():
            level=255
            while level > 0:
                #print level
                self.plugin.sendCommand(self.id, 'Dim', level)
                level -= self.decrease
                self.finished.wait(20.0)
            self.finished.set()
            time.sleep(0.1)
            self.plugin.sendCommand(self.id, 'Dim', 0)
            print "Good Night action finished"
            

    def Configure(self, deviceName = '', timeToSleep = 15):
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
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.tdGetName(id))).value
                if (name == deviceName):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.timeToSleepCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToSleep,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1
                    + self.name
                    + self.plugin.text.no_device_txt_2
                    + self.plugin.text.no_device_txt_3
                ), (1,0)
            )
       
        mySizer.Add(deviceCtrl, (1,1))
        
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.timeToSleep_txt
            ), (3,0)
        ) 
        mySizer.Add(self.timeToSleepCtrl, (3,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                deviceName = (
                    (c_char_p(self.plugin.dll.tdGetName(device))).value
                )
                timeToSleep = self.timeToSleepCtrl.GetValue()
                panel.SetResult(deviceName, timeToSleep)
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Good night')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: '
                            +'Good night in '
                            +str(timeToSleep)
                            +' minutes.'
                            +' Device: '
                            +deviceName
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''
