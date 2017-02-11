import eg
import urllib
import json

#from VeraClient import *
#from VeraDevice import *
#from VeraAsyncDispatcher import *

eg.RegisterPlugin(
    name = "MiCasaVerde Vera",
    author = "Created by Rick Naething / Last Updated by Brandon Simonsen (m19bradon)",
    version = "0.0.6b",
    kind = "other",
    description = "Control Over Devices on Vera"
)

#-----------------------------------------------------------------------------
class Vera(eg.PluginBase):

    def __init__(self):
        self.AddAction(SetSwitchPower)
        self.AddAction(TogglePower)
        self.AddAction(SetDimming)
        self.AddAction(RunScene)
        self.HTTP_API   = VERA_HTTP_API()
        #self.dispatcher = VeraAsyncDispatcher()
        self.vera       = []
        self.verbose = True
        eg.RestartAsyncore()

    def Configure(self, ip="127.0.0.1", port="3480", verbose=True):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, ip)
        textControl2 = wx.TextCtrl(panel, -1, port)
        checkbox = panel.CheckBox(verbose, 'Verbose Outputs')
        panel.sizer.Add(wx.StaticText(panel, -1, "IP address of Vera"))
        panel.sizer.Add(textControl)
        panel.sizer.Add(textControl2)
        panel.sizer.Add(checkbox)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(), textControl2.GetValue(), checkbox.GetValue())

    def __start__(self, ip='127.0.0.1', port='3480', verbose=True):
        self.ip = ip
        self.port = port
        self.verbose = verbose
        self.HTTP_API.connect(ip=ip, port=port)
        #self.vera       = VeraClient(ip, self.veraCallback, self.veraDebugCallback, self.dispatcher)

    def __stop__(self):
        pass

    def __close__(self):
        pass            
        
    # def veraCallback(self, msg, state=tuple()):
    #     # msg is either a string or a VeraDevice
    #     if isinstance(msg, VeraDevice):
    #         room = 'No Room'
    #         if msg.room in self.vera.rooms:
    #             room = self.vera.rooms[msg.room]
    #         event = room + '.' + str(msg)
    #     else:
    #         event = msg
    #     self.TriggerEvent(event)
    
    # def veraDebugCallback(self, msg, msg2=False):
    #     if self.verbose:
    #         event = 'DEBUG.' + msg
    #         self.TriggerEvent(event)

#-----------------------------------------------------------------------------      
class VERA_HTTP_API:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "3480"
        return

    def connect(self, ip=None, port=None):
        if ip: self.ip = ip
        if port: self.port = port
        print 'HTTP API connected'

    def send(self, url):
        try:
            #responce = urllib.urlopen('http://'+self.ip+':'+self.port+url).readlines()
            consumer = urllib.urlopen('http://'+self.ip+':'+self.port+url)
            responce = consumer.readlines()
            consumer.close()
        except IOError:
            eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+ url)
        else:
            return

    def close(self):
        print 'HTTP API connection closed'

#-----------------------------------------------------------------------------
class RunScene(eg.ActionBase):
    name = "Run Scene"
    description = "Runs a Vera Scene"

    def __call__(self, device):
        url = "/data_request?id=lu_action&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum="
        url += str(device)
        responce = self.plugin.HTTP_API.send(url)

    def Configure(self, device=1):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        panel.AddLine("Set Device", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())
        
#-----------------------------------------------------------------------------
class SetDimming(eg.ActionBase):
    name = "Set Light Level"
    description = "Sets a light to a percentage (%)."

    def __call__(self, device, percentage):
        url = "/data_request?id=lu_action&DeviceNum="
        url += str(device)
        url += "&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget="
        url += str(percentage)
        responce = self.plugin.HTTP_API.send(url)

    def GetLabel(self, device, percentage):
        return "Set Dimmable Light: " + str(device) + ": " + str(percentage)

    def Configure(self, device=1, percentage=100):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        valueCtrl = panel.SpinNumCtrl(percentage, min=0, max=100)
        panel.AddLine("Set Device", deviceCtrl)
        panel.AddLine("Dim to", valueCtrl, "percent.")
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue(), valueCtrl.GetValue())
        
#-----------------------------------------------------------------------------
class SetSwitchPower(eg.ActionBase):
    name = "Set Binary Power"
    description = "Turn a switch on or off"
    functionList = ["Off", "On"]
    
    def __call__(self, device, value):
        url = "/data_request?id=lu_action&DeviceNum="
        url += str(device)
        url += "&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue="
        url += str(value)
        responce = self.plugin.HTTP_API.send(url)

    def GetLabel(self, device, value):
        return "Set Binary Power Device: " + str(device) + ": " + self.functionList[value]

    def Configure(self, device=1, value=1):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        functionCtrl = wx.Choice(panel, -1, choices=self.functionList)
        functionCtrl.SetSelection(value)
        panel.AddLine("Set Device", deviceCtrl)
        panel.AddLine("Value", functionCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue(), functionCtrl.GetSelection())

#-----------------------------------------------------------------------------
#This class should toggle any binary zwave device.
class TogglePower(eg.ActionBase):
    name = "Toggle Binary Power"
    description = "Toggles the power on and off"
    
    def __call__(self, device):
        url = "/data_request?id=lu_action&DeviceNum="
        url += str(device)
        url += "&serviceId=urn:micasaverde-com:serviceId:HaDevice1&action=ToggleState"
        responce = self.plugin.HTTP_API.send(url)

    def GetLabel(self, device):
        return "Toggle Binary Power Device: " + str(device)

    def Configure(self, device=1):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.SpinIntCtrl(device)
        panel.AddLine("Set Device", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())