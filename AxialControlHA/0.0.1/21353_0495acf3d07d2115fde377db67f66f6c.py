import eg
from urllib import urlopen
import requests
import json
import httplib

eg.RegisterPlugin(
    name = "AxialControlHA",
    author = "yokel22",
    version = "0.0.1",
    iconFile = "Icon",
    kind = "program",
    canMultiLoad=True,
    description = "This is a plugin for AxialControl Home Automation Software (Formerly called InControl). <a href='http://www.axialcontrol.com'>AxialControl Homepage</a>",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6786876867"
)

class AxialControlHA(eg.PluginBase):
    """ A plugin to control AxialControl Home Automation Software"""
    
    def __init__(self):
        self.host = "192.168.1.116:1178"
        self.password = "password"
        self.connected = False
        self.getdevices = ""
        info = self.AddGroup(
            "Information Retrieval",
            "Actions for Information Retrieval"
        )
        info.AddAction(ListLights)
        info.AddAction(ListDimmers)
        info.AddAction(ListOutlets)
        info.AddAction(ListLocks)
        info.AddAction(ListEnergyDisplayers)
        info.AddAction(ListLevelDisplayers)
        info.AddAction(ListMotion)
        info.AddAction(ListGarageDoorOpeners)
        info.AddAction(ListAllDevices)
        info.AddAction(ListScenes)

        actions = self.AddGroup(
            "Actions",
            "Actions to change device states"
        )
        actions.AddAction(TurnSwitchOn)
        actions.AddAction(TurnSwitchOff)
        actions.AddAction(ToggleSwitch)
        actions.AddAction(TurnOutletOn)
        actions.AddAction(TurnOutletOff)
        actions.AddAction(ToggleOutlet)
        actions.AddAction(SetDimmerLevel)
        actions.AddAction(ActivateScene)
        
        
    def Configure(self, host="192.168.1.116:1178", password="password"):

        panel    = eg.ConfigPanel()    
        st1 = panel.StaticText("")
        st2 = panel.StaticText("")
        eg.EqualizeWidths((st1, st2))
        hostCtrl = wx.TextCtrl(panel,-1, host)
        passwordCtrl = wx.TextCtrl(panel,-1, password)

        panel.AddLine("AxialControlHA Server IP:Port", hostCtrl)
        panel.AddLine("AxialControlHA server password  ", passwordCtrl) 

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )
            
    def __start__(self, host, password):
        
        self.host = host
        self.password = password
        
        # Check for Server Connection
        r = self.getDevices()

        if r==False:
            print "Connection error, wrong IP or Server not accessible"
            r = ''

        else:
            print "Now Connected to AxialControlHA Server."
                            
    def __stop__ (self):
        pass

    def req(self, page, method='GET', body=''):
        data = False
        if body!='': body = json.dumps(body)
        
        server = httplib.HTTPConnection(self.host)
        try:
            server.request(method, page, body)
        except:
            print "Connectionerror 1"
            data = False
        else:
            try:
                response = server.getresponse()
                
            except:
                print "Connectionerror 2"
                data = False
            else:
                if response.status == 200:
                    try:
                        data = response.read()
                    except:
                        print "Connectionerror 4"
                        data = False
                    else:
                        data = json.loads(data)
                else:
                    print "Connectionerror 3"
                    data = False
            return data
            server.close()
            
    def putCmd(self, url, payload):
        headers = {'content-type': 'application/json' }
        send = requests.put(url, data=json.dumps(payload), headers=headers)

        return send

    def getCmd(self, url):
        headers = {'content-type': 'application/json' }
        payload = {   }
        send = requests.get(url, data=json.dumps(payload), headers=headers)
        
    def postCmd(self, url, payload):
        headers = {'content-type': 'application/json' }
        send = requests.post(url, data=json.dumps(payload), headers=headers)
        
    def getDevices(self):
        self.adress = 'http://' + self.host + '/zwave/devices?password=' + self.password
        data = self.req(self.adress)

        self.switchdict = {}
        self.outletdict = {}
        self.dimmerdict = {}
        self.thermostatdict = {}
        self.unknowndict = {}
        self.binarydict = {}
        self.zoneplayerdict = {}
        self.motiondict = {}
        self.multileveldict = {}
        self.lockdict = {}
        self.leveldisplayerdict = {}
        self.ipcamdicy = {}
        self.energymonitordict = {}
        self.alarmdict = {}
        self.fandict = {}
        self.nestawaydict = {}
        self.garagedooropenerdict = {}
        self.devices = []

        for x in data:
            DeviceName = x['deviceName']
            DeviceType = x['deviceType']
            Visible = x['visible']
            RoomID = str(x['roomId'])
            DisplayOrder = str(x['displayOrder'])
            NodeID = str(x['nodeId'])
            Battery = str(x['bl'])
            Name = x['name']
            CurrLevel = str(x['level'])
            LastChange = str(x['lastLevelUpdate'])
            DeviceID = str(x['deviceId'])

            if DeviceType == 0 and Visible == True:
                self.switchdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 1 and Visible == True:
                self.dimmerdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 2 and Visible == True:
                self.outletdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 3 and Visible == True:
                self.thermostatdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 5 and Visible == True:
                self.unknowndict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 6 and Visible == True:
                self.binarydict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 7 and Visible == True:
                self.zoneplayerdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 8 and Visible == True:
                self.motiondict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 9 and Visible == True:
                self.multileveldict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 10 and Visible == True:
                self.lockdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 11 and Visible == True:
                self.leveldisplayerdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 13 and Visible == True:
                self.ipcamdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 14 and Visible == True:
                self.energymonitordict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 15 and Visible == True:
                self.alarmdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 16 and Visible == True:
                self.fandict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 19 and Visible == True:
                self.nestawaydict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}
            if DeviceType == 20 and Visible == True:
                self.garagedooropenerdict[Name] = {'deviceID':DeviceID,'value':CurrLevel,'lastUpdate':LastChange,'type':DeviceType, 'batteryLevel':Battery, 'roomID':RoomID}

        self.devices = {'Switch':self.switchdict, 'Dimmer':self.dimmerdict, 'Outlet':self.outletdict, 'Thermostat':self.thermostatdict, 'Unknown':self.unknowndict, 'Binary':self.binarydict, 'Motion':self.motiondict, 'MultiLevel':self.multileveldict, 'Lock':self.lockdict, 'LevelDisplayer':self.leveldisplayerdict, 'EnergyMonitor':self.energymonitordict, 'Alarm':self.alarmdict, 'Fan':self.fandict, 'NestAwayMode':self.nestawaydict, 'GarageDoorOpener':self.garagedooropenerdict}

        return self.devices

    def getScenes(self):
        url = 'http://' + self.host + '/zwave/getScenes'
        payload = { "password": self.password, "sceneName": "", "activate": 1 }
        self.scenesdict = {}

        scrape = self.putCmd(url, payload)
        parsed_json = json.loads(scrape.content)
        
        for scene in parsed_json:
            visible = scene['mobileVisible']

            if visible == True:
                sceneID = scene['sceneId']
                name = scene['sceneName']
                self.scenesdict[name] = {'sceneID':sceneID}        

        return self.scenesdict

    
class ListLights(eg.ActionBase):
    name = "Get Switches"
    description = "Returns Switches Dictionary"

    def __call__(self):
        cmd = self.plugin.getDevices()
        items = self.plugin.switchdict

        return items

class ListDimmers(eg.ActionBase):
    name = "Get Dimmers"
    description = "Returns Dimmers Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.dimmerdict

        return items

class ListOutlets(eg.ActionBase):
    name = "Get Outlets"
    description = "Returns Outlets Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.outletdict

        return items

class ListLocks(eg.ActionBase):
    name = "Get Locks"
    description = "Returns Locks Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.lockdict

        return items

class ListLevelDisplayers(eg.ActionBase):
    name = "Get Level Displayers"
    description = "Returns LevelDisplayers Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.leveldisplayerdict

        return items

class ListMotion(eg.ActionBase):
    name = "Get Motion Sensors"
    description = "Returns Motion Sensors Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.motiondict

        return items

class ListEnergyDisplayers(eg.ActionBase):
    name = "Get Energy Displayers"
    description = "Returns EnergyDisplayers Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.energymonitordict

        return items

class ListGarageDoorOpeners(eg.ActionBase):
    name = "Get Garage Door Openers"
    description = "Returns Garage Door Openers Dictionary"
    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.garagedooropenerdict

        return items

class ListAllDevices(eg.ActionBase):
    name = "Get All Devices"
    description = "Returns All Devices Dictionary"

    def __call__(self):

        cmd = self.plugin.getDevices()
        items = self.plugin.devices

        return items  

class ListScenes(eg.ActionBase):
    name = "Get Scenes"
    description = "Returns Scenes Dictionary"

    def __call__(self):

        a = self.plugin.getScenes()
        scenes = self.plugin.scenesdict

        return scenes


class TurnSwitchOn(eg.ActionBase):
    name = "Turn On Switch"
    description = "Sets Selected Switch to On"

    class text:
        label_tree="Turn Light Switch On: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        payload = { "password": self.plugin.password, "deviceId": device, "powered": "true" }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree+deviceName
    
    def Configure(self, deviceID="Device ID", deviceName = ''):
        panel = eg.ConfigPanel()
    
        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())

class TurnSwitchOff(eg.ActionBase):
    name = "Turn Off Switch"
    description = "Sets Selected Switch to Off"

    class text:
        label_tree="Turn Light Switch Off: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        payload = { "password": self.plugin.password, "deviceId": device, "powered": "false" }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, device, deviceName):
        return self.text.label_tree+deviceName
    
    def Configure(self, deviceID="Device ID", deviceName = ''):
        panel = eg.ConfigPanel()
    
        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())
            
class ToggleSwitch(eg.ActionBase):
    name = "Toggle Switch"
    description = "Toggles Selected Switch On/Off"

    class text:
        label_tree="Toggle Light Switch: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        cmd = self.plugin.getDevices()

        state = self.plugin.switchdict[deviceName]['value']
        if state == "255":
            powered = "false"
        else:
            powered = "true"

        payload = { "password": self.plugin.password, "deviceId": device, "powered": powered }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, deviceID, deviceName ):
        return self.text.label_tree+deviceName
    
    def Configure(self, deviceID="Device ID", deviceName='', value=''):
        panel = eg.ConfigPanel()
    
        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID'],
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())
            
class TurnOutletOn(eg.ActionBase):
    name = "Turn On Outlet"
    description = "Sets Selected Outlet to On"
    
    class text:
        label_tree="Turn Outlet On: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        payload = { "password": self.plugin.password, "deviceId": device, "powered": "true" }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree+deviceName
    
    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()
    
        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Outlet",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())

class TurnOutletOff(eg.ActionBase):
    name = "Turn Off Outlet"
    description = "Sets Selected Outlet to Off"
    
    class text:
        label_tree="Turn Outlet Off: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        payload = { "password": self.plugin.password, "deviceId": device, "powered": "false" }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree+device
    
    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()
    
        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Outlet",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())

class ToggleOutlet(eg.ActionBase):
    name = "Toggle Outlet"
    description = "Toggles Selected Outlet On/Off"

    class text:
        label_tree="Toggle Outlet: "
        label_conf="Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.host + '/zwave/setDevicePower'
        cmd = self.plugin.getDevices()

        state = self.plugin.outletdict[deviceName]['value']
        if state == "255":
            powered = "false"
        else:
            powered = "true"

        payload = { "password": self.plugin.password, "deviceId": device, "powered": powered }

        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)    

    def GetLabel(self, deviceID, deviceName ):
        return self.text.label_tree+deviceName
    
    def Configure(self, deviceID="Device ID", deviceName='', value=''):
        panel = eg.ConfigPanel()
    
        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID'],
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceNameCtrl.GetStringSelection())
 
class ActivateScene(eg.ActionBase):
    name = "Activate Scene"
    description = "Activates Selected AxialControl Scene"

    class text:
        label_tree="Activate Scene: "
        label_conf="Scene Name"
        
    def __call__(self, scene): 
        url = 'http://' + self.plugin.host + '/zwave/activateScene'
        payload = { "password": self.plugin.password, "sceneName": scene, "activate": 1 }
        send = self.plugin.putCmd(url, payload)
        eg.StopMacro(ignoreReturn=True)

    def GetLabel(self, scene):
        return self.text.label_tree+scene

    def Configure(self, scene="Scene Name"):
        a = self.plugin.getScenes()
        keyChoicesList = sorted(self.plugin.scenesdict.keys())
        keySelection = keyChoicesList[0]
        panel = eg.ConfigPanel()
        choiceKeyCtrl = panel.Choice(keyChoicesList.index(keySelection), keyChoicesList)
        panel.AddLine("Select Scene: ", choiceKeyCtrl)
        while panel.Affirmed():
            panel.SetResult(
                choiceKeyCtrl.GetStringSelection()
            )
            
class SetDimmerLevel(eg.ActionBase):
    name = "Set Dimmer Level"
    description = "Sets Selected Dimmer to Selected Value"

    class text:
        label_tree="Set Dimmer Switch Level: "
        label_conf="Device Name"

    def __call__(self, device, deviceValue, deviceName):
        if deviceValue == 0:
            powered = "False"
        else:
            powered = "True"
        self.adress = 'http://' + self.plugin.host + '/zwave/setDeviceState?NODEID=' + device + '&Powered=' + powered + '&Level=' + str(deviceValue) + '&Password=' + self.plugin.password
        r = self.plugin.getCmd(self.adress)
        eg.StopMacro(ignoreReturn=False)    

    def GetLabel(self, deviceID, deviceValue, deviceName):
        return self.text.label_tree+deviceName+' '+str(deviceValue)+'%'
    
    def Configure(self, deviceID="Device ID", deviceValue=66, deviceName=''):
        panel = eg.ConfigPanel()
    
        dimmerDict = self.plugin.dimmerdict
        deviceNameChoices = sorted(dimmerDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = dimmerDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)
        deviceValueCtrl = panel.SpinIntCtrl(
            deviceValue,
            max=100,
        )
        
        deviceBox = panel.BoxedGroup(
            "Choose Dimmer Switch",
            ("Name: ", deviceNameCtrl),
            ("device ID: ", deviceIDCtrl),
            ("Value: ", deviceValueCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                dimmerDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()
        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(deviceIDCtrl.GetValue(), deviceValueCtrl.GetValue(), deviceNameCtrl.GetStringSelection())

