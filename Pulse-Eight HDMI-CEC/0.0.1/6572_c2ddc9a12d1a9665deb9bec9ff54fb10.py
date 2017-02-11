import eg
import os

eg.RegisterPlugin(
    name = "Pulse-Eight HDMI-CEC",
    author = "barnabas1969",
    version = "0.0.1",
    kind = "external",
    description = "Pulse-Eight HDMI-CEC adapter plugin."
)


from threading import Event, Thread
from ctypes import *
from _ctypes import LoadLibrary, FreeLibrary

class Text:
    init_exception_load_DLL = "Error loading the DLL!"
    class Action1:
        name = "Print a message for Action1"
        description = "This is the description for Action1's messages."
        message1 = "This is the first message for Action1"


cec_device_type_list = [c_int, c_int, c_int, c_int, c_int]
cec_logical_addresses = [c_int, c_int, c_int, c_int, c_int,
                         c_int, c_int, c_int, c_int, c_int,
                         c_int, c_int, c_int, c_int, c_int,
                         c_int]


class g_config:
    clientVersion             = c_uint32                # the version of the client that is connecting 
    strDeviceName             = c_char                  # the device name to use on the CEC bus, must be 13 characters 
    deviceTypes               = cec_device_type_list    # the device type(s) to use on the CEC bus for libCEC 
    bAutodetectAddress        = c_uint8                 # (read only) set to 1 by libCEC when the physical address was autodetected 
    iPhysicalAddress          = c_uint16                # the physical address of the CEC adapter 
    baseDevice                = c_int                   # the logical address of the device to which the adapter is connected. only used when iPhysicalAddress = 0 or when the adapter doesn't support autodetection 
    iHDMIPort                 = c_uint8                 # the HDMI port to which the adapter is connected. only used when iPhysicalAddress = 0 or when the adapter doesn't support autodetection 
    tvVendor                  = c_uint64                # override the vendor ID of the TV. leave this untouched to autodetect 
    wakeDevices               = cec_logical_addresses   # list of devices to wake when initialising libCEC or when calling PowerOnDevices() without any parameter. 
    powerOffDevices           = cec_logical_addresses   # list of devices to power off when calling StandbyDevices() without any parameter. 
    #
    serverVersion             = c_uint32                # the version number of the server. read-only 
    #
    # player specific settings
    bGetSettingsFromROM       = c_uint8                 # true to get the settings from the ROM (if set, and a v2 ROM is present), false to use these settings. 
    bUseTVMenuLanguage        = c_uint8                 # use the menu language of the TV in the player application 
    bActivateSource           = c_uint8                 # make libCEC the active source on the bus when starting the player application 
    bPowerOffScreensaver      = c_uint8                 # put devices in standby mode when activating the screensaver 
    bPowerOnScreensaver       = c_uint8                 # wake devices when deactivating the screensaver 
    bPowerOffOnStandby        = c_uint8                 # put this PC in standby mode when the TV is switched off. only used when bShutdownOnStandby = 0  
    bSendInactiveSource       = c_uint8                 # send an 'inactive source' message when stopping the player. added in 1.5.1 
    #
    callbackParam             = None                    # the object to pass along with a call of the callback methods. NULL to ignore 
    callbacks                 = None
    #    callbacks                 = ICECCallbacks           # the callback methods to use. set this to NULL when not using callbacks 
    #
    logicalAddresses          = cec_logical_addresses   # (read-only) the current logical addresses. added in 1.5.3 
    iFirmwareVersion          = c_uint16                # (read-only) the firmware version of the adapter. added in 1.6.0 
    bPowerOffDevicesOnStandby = c_uint8                 # put devices in standby when the PC/player is put in standby. added in 1.6.0 
    bShutdownOnStandby        = c_uint8                 # shutdown this PC when the TV is switched off. only used when bPowerOffOnStandby = 0. added in 1.6.0 
    strDeviceLanguage         = c_char                  # the menu language used by the client. 3 character ISO 639-2 country code. see http://http://www.loc.gov/standards/iso639-2/ added in 1.6.2 
    iFirmwareBuildDate        = c_uint32                # (read-only) the build date of the firmware, in seconds since epoch. if not available, this value will be set to 0. added in 1.6.2 
    bMonitorOnly              = c_uint8                 # won't allocate a CCECClient when starting the connection when set (same as monitor mode). added in 1.6.3 
    cecVersion                = c_int                   # CEC spec version to use by libCEC. defaults to v1.4. added in 1.8.0 
    adapterType               = c_int                   # type of the CEC adapter that we're connected to. added in 1.8.2 
    iDoubleTapTimeoutMs       = c_uint8                 # prevent double taps withing this timeout. defaults to 200ms. added in 2.0.0 
    comboKey                  = c_int                   # key code that initiates combo keys. defaults to CEC_USER_CONTROL_CODE_F1_BLUE. CEC_USER_CONTROL_CODE_UNKNOWN to disable. added in 2.0.5 
    iComboKeyTimeoutMs        = c_uint32                # timeout until the combo key is sent as normal keypress 


class P8CEC(eg.PluginBase):

    text = Text

    def __init__(self):
        print "Initializing P8 HDMI-CEC"
        self.counter = 0    # Initialize variables here!
        self.AddAction(IncrementCounter)
        self.AddAction(DecrementCounter)
        self.AddAction(PrintString)
        group1 = self.AddGroup(
            "My first group",
            "My first group description"
        )
        group1.AddAction(Action1)
        group2 = self.AddGroup(
            "My second group",
            "My second group description"
        )
        group2.AddAction(Action2)

    def __start__(self, myString):
        print "Loading Pulse-Eight HDMI-CEC library"
        self.dll = None
        try:
            self.dllPath = os.path.join(os.getenv('ProgramFiles(x86)')+'\\Pulse-Eight\\USB-CEC Adapter\\', "libcec.dll")
        except:
            self.dllPath = os.path.join(os.getenv('ProgramFiles')+'\\Pulse-Eight\\USB-CEC Adapter\\', "libcec.dll")
            pass
        try:
            self.dll = LoadLibrary(self.dllPath)
            self.cec = CDLL("libcec.dll", RTLD_GLOBAL, handle=self.dll)
        except: 
            raise eg.Exception(self.text.init_exception_load_DLL)
        #
        #        print self.dllPath
        #        try:
        #            # This needs to be a parameter from the plugin configuration:
        #            self.dll = windll.LoadLibrary(self.dllPath)
        #        except: 
        #            raise eg.Exception(self.text.init_exception_load_DLL)
        #
        print "Attempting to initialize the device..."
        mytest = c_bool
        mytest = self.cec.CECInitialise(g_config)
        print mytest
        print "result above."
        #self.dll.CecInitialise() ???
        self.stopReceiveCecEvents = Event()
        thread = Thread(
            target=self.ReceiveCecEvents,
            args=(self.stopReceiveCecEvents, )
        )
        thread.start()

    def __stop__(self):
        print "P8CEC is stopped."
        self.stopReceiveCecEvents.set()
        FreeLibrary(self.dll)

    def __close__(self):
        print "P8CEC is closed."

    def Configure(self, myString=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, myString)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())

    def ReceiveCecEvents(self, stopReceiveCecEvents):
        while not stopReceiveCecEvents.isSet():
            self.TriggerEvent("MyTimerEvent")
            stopReceiveCecEvents.wait(10.0)
            # If the data received from the CEC bus is a button press, we may
            # want to trigger an enduring event.  Then, after the button
            # release is received, we will need to end the event (or trigger
            # a new one).  Here's an example:
            # if <some criteria like a button press>:
            #     self.TriggerEnduringEvent("MySuffix"[, myPayload])
            # ( elif <criteria for the button release>:
            #     self.EndLastEvent() )*
            # else:
            #     self.TriggerEvent("MySuffix"[, myPayload])


class PrintString(eg.ActionBase):

    def __call__(self, myString):
        print myString

    def Configure(self, myString=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, myString)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())


class IncrementCounter(eg.ActionBase):
    name = "Increment Counter"
    description = "Increment counter."

    def __call__(self):
        self.plugin.counter += 1
        print self.plugin.counter


class DecrementCounter(eg.ActionBase):
    name = "Decrement Counter"
    description = "Decrement counter."

    def __call__(self):
        self.plugin.counter -= 1
        print self.plugin.counter


class Action1(eg.ActionBase):

    def __call__(self):
        print self.text.message1
        print "Action1 called"


class Action2(eg.ActionBase):

    def __call__(self):
        print "Action2 called"


