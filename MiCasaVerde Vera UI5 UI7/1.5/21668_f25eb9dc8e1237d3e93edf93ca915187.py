# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# This plugin is a Telnet server and an HTTP client that sends and receives MiCasaVerde UI5 and UI7 light states.
# This plugin is based on the Vera plugins by Rick Naething
#
# $LastChangedDate: 2015-10-10 20:51:00 -0700 $
# $LastChangedRevision: 9b $
# $LastChangedBy: K $


import eg

eg.RegisterPlugin(
    name = "MiCasaVerde Vera UI5 UI7",
    description = "Control of Dimmers and Switches on the MiCasaVerde Vera UI5 UI7",
    author = "K",
    version = "1.5",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    kind = "other",
    guid = '{321D9F7C-6961-4C62-B6E0-86C950A25279}'
    
)

import sys
import time
import socket
import threading
from copy import deepcopy as dc

DEBUG = False
if DEBUG:
    def log(*args):
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], str) or isinstance(args[i], unicode):
                args[i] += ': '
            else:
                args[i] = str(args[i])
        print "MiCasaVerde: "+"".join(args)

else:
    def log(*args): pass

def PE(*args):
    args = list(args)
    for i in range(len(args)):
        if isinstance(args[i], str) or isinstance(args[i], unicode):
            args[i] += ': '
        else:
            args[i] = str(args[i])
    eg.PrintError("MiCasaVerde: "+"".join(args))
    return False

def PN(*args):
    args = list(args)
    for i in range(len(args)):
        if isinstance(args[i], str) or isinstance(args[i], unicode):
            args[i] += ': '
        else:
            args[i] = str(args[i])
    eg.PrintNotice("MiCasaVerde: "+"".join(args))
    return True

class Text:
    PrefixBox = 'Event Prefix Settings'
    Prefix = 'Event Prefix: '
    VeraBox = 'Vera IP and Port Settings'
    VeraIP = 'IP: '
    VeraPort = 'Port: '
    DimmerBox = 'Set the Dim Level of a Dimmable Switch'
    ToggleBox = 'Toggle a Light or Binary Switch to Opposite of Current State'
    SwitchBox = 'Turn a Light or Binary Switch On or Off'
    SceneBox = 'Run A Scene'
    DeviceText = 'Device: '
    SceneText = 'Scene: '
    PercentText = 'Level: '
    StateText = 'ON or OFF: '
    FanModeBox = 'HVAC Fan Mode'
    FanModeText = 'Fan Mode: '
    OppModeBox = 'HVAC Opperating Mode'
    OppModeText = 'Opperating Mode: '
    HSetTempBox = 'HVAC Heat Set Temperature'
    CSetTempBox = 'HVAC Cool Set Temperature'
    TempText = 'Set Teperature: '
    AlarmBox = 'Arm or Disarm Alarm'
    AlarmText = 'Arm or Disarm: '
    MinEvtText = 'Reduce Events: '
    StatusBox = 'Get Dimmer Level'
    EvtPayText = 'Generate Payload Data: '
    RampBox = 'Ramp Dimmer Up or Down'
    StartText = 'Start Percent: '
    StopText = 'Stop Percent: '
    IncText = 'Brightness Steps: '
    SpeedText ='Speed: '
    class Scene:
        name = 'Run Scene'
        description = 'Runs a Vera Scene'
    class Dimmer:
        name = 'Set Light Level'
        description = 'Set the Dim Level of a Dimmable Switch'
    class Switch:
        name = 'Switch Power'
        description = 'Turn a Light or Binary Switch ON or OFF'
    class Toggle:
        name = 'Toggle Power'
        description = 'Toggle a Light or Binary Switch to Opposite of Current State'
    class FanMode:
        name = 'HVAC Fan Mode'
        description = 'Change the fan Mode on your HVAC Unit'
    class OppMode:
        name = 'HVAC Opperating Mode'
        description = 'Change the Opperating Mode of your HVAC Unit'
    class HSetTemp:
        name = 'HVAC Heat Set Temp'
        description = 'Change the Heat Set Temperature on your HVAC Unit'
    class CSetTemp:
        name = 'HVAC Cool Set Temp'
        description = 'Change the Cool Set Temperature on your HVAC Unit'
    class Alarm:
        name = 'Alarm Control'
        description = 'Arm or Disarm your Security System'
    class DimmerStatus:
        name = 'Level of a Dimmer'
        description = 'Get the Current Level of a Dimmer Switch'
    class RampDimmer:
        name = 'Ramp Dimmable Light'
        description = 'Control the Speed and Brightness as a Dimmer Turns on or Off'

class DimmerStatus(eg.ActionBase):

    text = Text

    def __call__(self, device=0):

        return int(self.plugin.VDL['devices'][str(device)]['level'])

    def Configure(self, device=0):

        text = self.text
        panel = eg.ConfigPanel()
        
        st1 = panel.SpinIntCtrl(device, max=200)

        box1 = panel.BoxedGroup(
                            text.StatusBox,
                            (text.DeviceText, st1)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class RampDimmer(eg.ActionBase):

    text = Text

    def __call__(self, device=0, start=0, stop=0, inc=0.0, speed=0.0):

        self.plugin.RampThread.CheckRamp(device)
        self.plugin.RampDimmer(device, start, stop, inc, speed)

    def Configure(self, device=0, start=0, stop=0, inc=0.0, speed=0.0):

        text = self.text
        panel = eg.ConfigPanel()
        
        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(start, max=100)
        st3 = panel.SpinIntCtrl(stop, max=100)
        st4 = panel.SpinNumCtrl(inc, increment=0.25)
        st5 = panel.SpinNumCtrl(speed, increment=0.25)

        box1 = panel.BoxedGroup(
                            text.RampBox,
                            (text.DeviceText, st1),
                            (text.StartText, st2),
                            (text.StopText, st3),
                            (text.IncText, st4),
                            (text.SpeedText, st5)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue()
                            )

class Scene(eg.ActionBase):

    text = Text

    def __call__(self, scene=0):
        self.plugin.Scene(scene)


    def Configure(self, scene=0):

        text = self.text
        panel = eg.ConfigPanel()
        
        st1 = panel.SpinIntCtrl(scene, max=200)

        box1 = panel.BoxedGroup(
                            text.SceneBox,
                            (text.SceneText, st1)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class Dimmer(eg.ActionBase):

    text = Text

    def __call__(self, device=0, percent=0):
        self.plugin.RampThread.CheckRamp(device)
        self.plugin.Dimmer(device, percent)

    def Configure(self, device=0, percent=0):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(percent, max=100)
 
        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.DimmerBox,
                            (text.DeviceText, st1),
                            (text.PercentText, st2)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Switch(eg.ActionBase):

    text = Text
    
    def __call__(self, device=0, state=0):
        self.plugin.RampThread.CheckRamp(device)
        self.plugin.Switch(device, state)
        

    def Configure(self, device=0, state=0):

        text = self.text

        panel = eg.ConfigPanel()
        choices = ['OFF', 'ON']

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(state, choices=choices)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.SwitchBox,
                            (text.DeviceText, st1),
                            (text.StateText, st2)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Toggle(eg.ActionBase):

    text = Text
    
    def __call__(self, device=0):
        self.plugin.RampThread.CheckRamp(device)
        self.plugin.Toggle(device)

    def Configure(self, device=0):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)

        box1 = panel.BoxedGroup(
                            text.ToggleBox,
                            (text.DeviceText, st1)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class FanMode(eg.ActionBase):

    text = Text

    def __call__(self, device=0, mode=1):
        self.plugin.FanMode(device, mode)

    def Configure(self, device=0, mode=1):

        text = self.text
        panel = eg.ConfigPanel()
        choices = ['Auto', 'PeriodicOn', 'ContinuousOn', 'FollowSchedule']

        
        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(mode, choices=choices)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.FanModeBox,
                            (text.DeviceText, st1),
                            (text.FanModeText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class OppMode(eg.ActionBase):

    text = Text

    def __call__(self, device=0, mode=0):
        self.plugin.OppMode(device, mode)

    def Configure(self, device=0, mode=0):

        text = self.text

        panel = eg.ConfigPanel()
        choices = ['Off', 'CoolOn', 'HeatOn', 'AutoChangeOver']

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(mode, choices=choices)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.OppModeBox,
                            (text.DeviceText, st1),
                            (text.OppModeText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class HSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, device=0, temp=70):
        self.plugin.HSetTemp(device, temp)

    def Configure(self, device=0, temp=70):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(temp, min=50, max=90)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.HSetTempBox,
                            (text.DeviceText, st1),
                            (text.TempText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                st1.GetValue(),
                st2.GetValue()
                )

class CSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, device=0, temp=70):
        self.plugin.CSetTemp(device, temp)

    def Configure(self, device=0, temp=70):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(temp, min=50, max=90)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.CSetTempBox,
                            (text.DeviceText, st1),
                            (text.TempText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Alarm(eg.ActionBase):

    text = Text

    def __call__(self, state=0):
        self.plugin.Alarm(state)

    def Configure(self, state=0):

        text = self.text
        panel = eg.ConfigPanel()
        choices = ['DISARM', 'ARM']

        st1 = panel.Choice(state, choices=choices)
                
        box1 = panel.BoxedGroup(
                            text.AlarmBox,
                            (text.AlarmText, st1)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class Vera(eg.PluginBase):

    text=Text

    def __init__(self):

        self.AddEvents()
        self.AddAction(Switch)
        self.AddAction(Toggle)
        self.AddAction(Dimmer)
        self.AddAction(Scene)
        self.AddAction(FanMode)
        self.AddAction(OppMode)
        self.AddAction(HSetTemp)
        self.AddAction(CSetTemp)
        self.AddAction(Alarm)
        self.AddAction(DimmerStatus)
        self.AddAction(RampDimmer)

        self.VERA_HTTP_API = VERA_HTTP_API()
        self.Server = Server()
        self.RampThread = RampThread(self)
        self.RampThreadDict = {}
        self.server = None
        self.prefix=None
        self.VDL = {}
        self.ADD = []
        self.ItemLog = []
        self.MinimalEvents = False
        self.GenPayload = True

    def Dimmer(self, device, percent):
        self.VERA_HTTP_API.send(SendType='Dimmer', device=str(device), percent=str(percent))

    def Toggle(self, device):
        self.VERA_HTTP_API.send(SendType='Toggle', device=str(device))

    def Scene(self, scene):
        self.VERA_HTTP_API.send(SendType='Scene', scene=str(scene))

    def Switch(self, device, state):
        self.VERA_HTTP_API.send(SendType='Switch', device=str(device), state=str(state))

    def FanMode(self, device, mode):
        choices = ['Auto', 'PeriodicOn', 'ContinuousOn', 'FollowSchedule']
        mode = choices[mode]

        self.VERA_HTTP_API.send(SendType='FanMode', device=str(device), mode=str(mode))

    def OppMode(self, device, mode):
        choices = ['Off', 'CoolOn', 'HeatOn', 'AutoChangeOver']
        mode = choices[mode]

        self.VERA_HTTP_API.send(SendType='OppMode', device=str(device), mode=str(mode))

    def HSetTemp(self, device, temp):
        self.VERA_HTTP_API.send(SendType='HSetTemp', device=str(device), temp=str(temp))

    def CSetTemp(self, device, temp):
        self.VERA_HTTP_API.send(SendType='CSetTemp', device=str(device), temp=str(temp))

    def Alarm(self, state):
        self.VERA_HTTP_API.send(SendType='Alarm', state=str(state))

    def RampDimmer(self, device, start, stop, inc, speed):
        self.RampThread.Start(device=device, start=start, stop=stop, inc=inc, speed=speed)

    def Configure(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera', minimalEvents=False, genPayload = True):

        text = self.text

        panel = eg.ConfigPanel()

        st1 = panel.TextCtrl(ip)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(prefix)
        st4 = panel.CheckBox(minimalEvents)
        st5 = panel.CheckBox(genPayload)
 
        eg.EqualizeWidths((st1, st2, st3, st4, st5))
                
        box1 = panel.BoxedGroup(
                            text.VeraBox,
                            (text.VeraIP, st1),
                            (text.VeraPort, st2)
                            )
        box2 = panel.BoxedGroup(
                            text.PrefixBox,
                            (text.Prefix,st3),
                            (text.MinEvtText,st4),
                            (text.EvtPayText,st5)
                            )

        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND)
            ])

        while panel.Affirmed():
            panel.SetResult(
                        st1.GetValue(),
                        st2.GetValue(),
                        st3.GetValue(),
                        st4.GetValue(),
                        st5.GetValue()
                        )

    def __start__(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera', minimalEvents=False, genPayload = True):

        self.MinimalEvents = minimalEvents
        self.GenPayload = genPayload
        self.info.eventPrefix = prefix
        self.prefix = prefix
        self.Startup = True

        if self.server:
            self.server = self.Server.Close(self.server)

        self.server = self.Server.Start(ip=ip, port=port, plugin=self)
        self.VERA_HTTP_API.connect(ip=ip, port=port)

    def __stop__(self):

        if self.server:
            self.server = self.Server.Close(self.server)

        self.RampThread.Stop()

    def SendEvent(self, DevID, EventItems, deviceItems):
        
        Event = self.VDL['Event'][DevID][0][0]
        Category = self.VDL['Event'][DevID][1]
        bPayload = self.VDL['Items'][DevID]
        Allowable = ALLOWEDEVENTS.VARS
        Translate = ALLOWEDEVENTS.TRANSLATE
        EventData = None
        GenEvt = False

        for i in range(len(EventItems)):
            if EventItems[i][0] == 'comment': continue
            elif self.MinimalEvents and EventItems[i][0] not in Allowable: continue
            else: pass

            Item = EventItems[i][0]
            Value = EventItems[i][1]
            Val = Value

            if (Category == 'Dimmable Light' or Category == 'Switch') and Item == 'status':
                if Val == '1': Val = 'On'
                elif Val == '0': Val = 'Off'

            foundWord = False
            for words in Translate:
                if words[0] == Item:
                    Item = words[1]
                    foundWord = True
            if not foundWord:
                Item = Item.title()

            if self.GenPayload:
                payload = {'key1': self.prefix }
                if bPayload['room'] != '' and bPayload['room'] != None:
                    payload['key2'] = bPayload['room']
                if bPayload['name'] != '' and bPayload['name'] != None:
                    payload['key3'] = bPayload['name']
                payload['value'] = dc(deviceItems)

                EventData = dict(suffix=str(Event)+'.'+str(Category).title() +'.'+str(Item)+'.'+str(Val), payload=payload)
            else:
                EventData = dict(suffix=str(Event)+'.'+str(Category).title()+'.'+str(Item)+'.'+str(Val))
            self.TriggerEvent(**EventData)

    def UpdateDevices(self, vData):

        tmp = vData
        self.CFGDList = {}
        VDL = {'Counters':{}, 'Event':{}, 'NewItems': {}, 'Items': {}}
        if self.Startup: self.VDL = dc(VDL)

        mType =[['devices', 0],['scenes',1],['rooms',2],
                ['categories',3],['sections',4]]

        def BuildEvt(evtData, Type):
            ID = str(evtData['id'])
            midfix = [['room'], ['name'], ['category']]
            for i in range(3):
                S=False
                try: S = evtData[midfix[i][0]]
                except: S = 'None'
                if S == 'None' or None:
                    S = Type if i == 2 else ID if Type == 'device' and i == 1 else None
                midfix[i].append(S)
            return ID, midfix

        def NewItemScan(n, o):
            nItems = dc(n)
            oItems = dc(o)
            mKeys = []
            for nK, nV in nItems.iteritems():
                for oK, oV in oItems.iteritems():
                    if (nK == oK) and (nV == oV):
                        mKeys.append(nK)

            for dK in mKeys:
                del(nItems[dK])

            if nItems == {}: nItems = False
            return dc(nItems), dc(oItems)

        def NewItemsReporting(NI, NC, OI, OC):
            nItems, oItems = NewItemScan(NI, OI)
            nCounters, oCounters = NewItemScan(NC, OC)
            rItem = dc(nItems)
            rCount = NC if nCounters else dc(oCounters)
            noUp = False if nCounters or nItems else True
            
            if nCounters:
                eg.PrintNotice('MicasaVerde: OldCounters: '+str(oCounters))
                eg.PrintNotice('MicasaVerde: NewCounters: '+str(nCounters))

            if nItems:
                self.ItemLog.insert(0, [time.strftime("%c"), nItems])
                eg.PrintNotice('MicasaVerde: NewItems: '+str(nItems))

            return rItem, rCount

        def DeviceMerge(Type):
            typeList = {}
            typeList=dict(mType)
            if Type in typeList:
                Value=tmp[Type]
                for i in range(len(Value)):
                    oldData = dc(Value[i])
           
                    def Merge(Key, dataDict, Key2):
                        typeList={}
                        typeList=dict(mType[:2])
                        if Type in typeList:
                            for i in range(len(dataDict)):
                                mData = dc(dataDict[i])
                                if 'id' in mData:
                                    if mData['id'] == Key:
                                        return dc(mData[Key2])
                    typeList={}
                    typeList=dict(mType[:2])
                    if Type in typeList:
                        if 'room' in oldData:
                            roomName = Merge(oldData['room'], tmp['rooms'],'name')
                            oldData['roomID'] = oldData[str('room')]
                            oldData['room'] = str(roomName)

                    typeList={}
                    typeList=dict(mType[:1])
                    if Type in typeList:
                        if 'category' in oldData:
                            catName = Merge(oldData['category'], tmp['categories'],'name')
                            oldData['catID'] = oldData[str('category')]
                            oldData['category'] = str(catName)

                    typeList = {}
                    typeList=dict(mType)
                    if Type in typeList:
                        if 'id' in oldData:
                            if Type == 'devices' or Type == 'scenes':
                                ID, midfix = BuildEvt(oldData, Type)
                                VDL['Items'][ID] = dict(midfix)

                                for i in range(3): midfix[i] = midfix[i][1]
                                midfix = [['.'.join([midfix[0] ,midfix[1].replace(' Weather','')])] if midfix[0] != None else [midfix[1]], midfix[2]]
                                midfix[0][0] = midfix[0][0].replace(' ', '-').replace(':', '')

                                VDL['Event'][ID] = midfix
                            VDL['Counters'][Type] += 1
                            VDL[Type][str(oldData['id'])]=dc(oldData)

        for Type, idx in mType:
            VDL[Type] ={}
            VDL['Counters'][Type] = 0
            DeviceMerge(Type)
            del(tmp[Type])
            mType[idx][0] = str(idx)

        VDL['system']=dc(tmp)
        tmp = {}

        NI = dc(VDL['Items'])
        NC = dc(VDL['Counters'])
        OI = {}
        OC = {}

        if self.Startup:
            OI = {}
            OC = {}
        else:
            OI = dc(self.VDL['Items'])
            OC = dc(self.VDL['Counters'])
   
        NI, NC  = NewItemsReporting(NI, NC, OI, OC)

        VDL['NewItems'] = NI
        VDL['Counters'] = NC

        if not self.Startup:
            self.EventDetector(
                            dc(VDL['devices']),
                            dc(VDL['scenes']),
                            dc(self.VDL['devices']),
                            dc(self.VDL['scenes'])
                            )
        else: self.Startup = False

        self.VDL = dc(VDL)

    def EventDetector(self, newDevice, newScene, oldDevice, oldScene):

        def IterItem(new, old):
            IDCounter = [0, 0]
            ItemCounter = [0, 0]

            for newID, newItems in new.iteritems():
                IDCounter[0] += 1
                IDMatch = False
                ItemsMatch = False
                for oldID, oldItems in old.iteritems():
                    if newID == oldID:
                        IDCounter[1] += 1
                        if newItems != oldItems:
                            EventItems = []
                            for newItem, newValue in newItems.iteritems():
                                ItemCounter[0] += 1
                                for oldItem, oldValue in oldItems.iteritems():
                                    if newItem == oldItem:
                                        ItemCounter[1] += 1
                                        if newValue != oldValue:
                                            EventItems.append([newItem, newValue])
                            if EventItems != []:
                                self.SendEvent(newID, dc(EventItems), dc(newItems))

        IterItem(newDevice, oldDevice)
        IterItem(newScene, oldScene)


class RampThread():

    def __init__(self, plugin):

        self.plugin = plugin
        self.RunningRamp = False
        return

    def Start(self, device, start, stop, inc, speed):
        try:
            self.RunningRamp = True
            t = threading.Thread(name='Ramp-'+str(device), target=self.RunRamp, args=(device, start, stop, inc, speed),)
            t.start()
            self.plugin.RampThreadDict[str(device)] = t
        except:
            PE("RampThread", "Start", sys.exc_info())
        finally:
            return

    def RunRamp(self, device, strt, stp, incr, spd):
        inc = float('-'+str(incr)) if strt > stp else float(incr)
        stop = float(stp+1) if stp > strt else float(stp-1)
        start = float(strt)
        speed = float(spd)

        def frange(x, y, jump):
            if str(jump)[:1] == '-':
                while x > y:
                    yield x
                    x += jump
            else:
                while x < y:
                    yield x
                    x += jump

        while self.RunningRamp:
            for i in frange(start, stop, inc):
                self.plugin.Dimmer(device, i)
                time.sleep(speed)
            self.RunningRamp = False

    def CheckRamp(self, device):
        if str(device) in self.plugin.RampThreadDict:
            self.Stop(self.plugin.RampThreadDict[str(device)])
            del self.plugin.RampThreadDict[str(device)]
            PN('RampThread', 'CheckRamp', 'RampStopped', device)

    def Stop(self, t=False):
        if t:
            t.join()
            self.RunningRamp = False
        else:
            for key in self.plugin.RampThreadDict.keys():
                self.plugin.RampThreadDict[key].join()
                self.plugin.RunningRamp = False
                del self.plugin.RampThreadDict[key]

class Server():

    def __init__ (self):

        self.plugin = None
        self.VERA_HTTP_API = VERA_HTTP_API()
        self.DataThreadList = []
        self.ServerThread = None
        self.RunningUpdate=False
        self.DataThread=False
        return

    def Start(self, ip, port, plugin):

        self.lock = threading.Lock()
        self.plugin = plugin
        self.DataThread=True
        self.RunningUpdate = self.ConnectHTTPAPI(ip, port)
        if self.RunningUpdate:
            return self.StartServerThread()
        else:
            return None

    def ConnectHTTPAPI(self, ip, port):

        self.VeraPort = port
        self.VeraIP = ip

        return self.VERA_HTTP_API.connect(ip=self.VeraIP, port=self.VeraPort)

    def StartServerThread(self):
        t=None
        try:
            t = threading.Thread(name='Vera-Receive', target=self.RequestUpdate)
            t.start()  
            self.ServerThread = t
        except:
            t = None
            PE("Server", "StartServerThread", sys.exc_info())
        finally:
            return t

    def RequestUpdate(self):
        while self.RunningUpdate:
            try:
                data = self.VERA_HTTP_API.send('ComRoomList')
                log("Server", 'RequestUpdate', repr(data))
                if data:
                    self.EvalData(data)
            except:
                PE("Server", "RequestUpdate", sys.exc_info())
            finally:
                time.sleep(0.1)

    def EvalData(self, data):
        eData = False
        log("Server", 'EvalData', repr(data))

        try:
            eData = dc(json.loads(data))
        except:
            err1=sys.exc_info()
            try:
                eData = eval(data)
            except:
                PE("Server", "EvalData", "Error 1", err1, "Error 2", sys.exc_info())
                eData = False
        finally:
            if eData:
                self.DataReadThread(eData)

    def DataReadThread(self, data):
        try:
            if not self.DataThread: return
            t =  threading.Thread(name='Vera-ProcessData', target=self.plugin.UpdateDevices, args=(data,))
            t.start()
            self.DataThreadList.append(t)
        except:
            PE("Server", "DataReadThread", sys.exc_info())
        finally: return
        
    def Close(self, t):
        for thread in self.DataThreadList:
            thread.join()
            self.DataThread = False
        self.DataThreadList = []

        try:
            t.join()
        except: pass

        finally:
            self.RunningUpdate = False
            PN('Server', 'Server ShutDown')
            return None
        
 
class VERA_HTTP_API:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 3480
        self.CONNECTED = False
        self.Startup = True
        return

    def connect(self, ip=None, port=None):
        self.CONNECTED = self.Startup
        self.ip = str(ip) if ip else self.ip
        self.port = port if port else self.port

        self.IPPort = str(self.ip)+":"+str(self.port)
        self.HostData = dc(URLS.DATA['HostData'])
        self.HostData[3][1] = self.IPPort
        self.HostData[3] = "".join(self.HostData[3])

        self.CONNECTED = PN("VERA_HTTP_API", "Connection Successful") if self.send('ComRoomList') \
                            else PE("VERA_HTTP_API", "Connection Failure", "IP", ip, "Port", port)

        return self.CONNECTED
    
    def send(self, SendType, device=False, percent=False, state=False, scene=False, temp=False, mode=False):
        Request=self.Startup
        self.Startup = False

        Request = PE("VERA_HTTP_API", "Connection Failure", "IP", self.ip, "Port", self.port) \
                    if not self.CONNECTED and not self.Startup else ''
        if Request == '':
            SendType = dc(URLS.DATA[SendType])
            for line in SendType:
                Request += line+str(device) if line[-11:] == '&DeviceNum=' \
                        else line

            Request += str(percent) if percent \
                        else str(state) if state \
                        else str(scene) if scene \
                        else str(temp) if temp \
                        else str(mode) if mode \
                        else ''

            Request += " HTTP/1.1"
            Request = [Request, "Host: "+self.IPPort]
            Request.extend(self.HostData)
            Request = "\r\n".join(Request)
            Request = self.SendData(Request)

            return Request

    def SendData(self, url):

        Response = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5.0)
        sock.connect((self.ip, self.port))
        sock.settimeout(5.0)
        sock.sendall(url)
        answer = sock.recv(4096)
        while answer:
            Response += answer
            answer = sock.recv(4096)

        sock.close()

        try:
            if Response[:15] == "HTTP/1.1 200 OK":
                try:
                    Response = Response[39:]
                except:
                    log("VERA_HTTP_API", "SendData 1", sys.exc_info(), Response)
                    Response = False
            else:
                log("VERA_HTTP_API", "SendData 2", Response)
                Response = False
        except:
            log("VERA_HTTP_API", "SendData 3", sys.exc_info(), Response)
            Response = False
        return Response

class URLS:
        DATA = {
        'Dimmer'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget=" ],
        'Switch'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue="],
        'Toggle'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:micasaverde-com:serviceId:HaDevice1&action=ToggleState"],
        'Scene'       : ["GET /data_request?id=lu_action&serviceId=urn:micasaverde-com:","serviceId:HomeAutomationGateway1&action=RunScene&SceneNum="],
        'FanMode'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_FanOperatingMode1&action=SetMode&NewMode="],                                                                                                                                                         
        'OppMode'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_UserOperatingMode1&action=SetModeTarget&NewModeTarget="],                                                                                                                                        
        'CSetTemp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Cool&action=SetCurrentSetpoint&NewCurrentSetpoint="], 
        'HSetTemp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Heat&action=SetCurrentSetpoint&NewCurrentSetpoint="],
        'Alarm'       : ["GET /data_request?id=action&output_format=xml&Category=4&serviceId=urn:micasaverde-com:","serviceId:SecuritySensor1&action=SetArmed&newArmedValue="],
        'AllVeraData' : ["GET /data_request?id=user_data","&output_format=json"],
        'DevStatus'   : ["GET /data_request?id=status","&output_format=json&DeviceNum="],                                                                                                      
        'AllDevStatus': ["GET /data_request?id=status","&output_format=json"],                                                                                                                          
        'ComRoomList' : ["GET /data_request?id=sdata","&output_format=json"],                                                                                                                         
        'SimRoomList' : ["GET /data_request?","id=invoke"],
        'JSON-XML'    : ["json, xml"],                                                                                     
        'LiveEnergy'  : ["GET /data_request?","id=live_energy_usage"],
        'HostData'    : ["User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
                         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                         "Accept-Encoding: gzip, deflate",
                         ["Referer: http://", "", "/data_request?id=sdata&output_format=xml"],
                         "",""]
        }

class ALLOWEDEVENTS:
    VARS = [
            'watts',   'status',        'level',     'temperature', 'humidity',
            'fanmode', 'coolsp',        'fan',       'mode',        'hvacstate', 
            'solar',   'windcondition', 'windchill', 'pressure',    'feels',
            'dew',     'winddirection', 'condition', 'windgust',    'uv',
            'heatsp',  'windspeed'
            ]
    TRANSLATE = [
                ['fanmode', 'FanMode'],    ['coolsp','CoolSetPoint'], ['winddirection','WindDirection'],
                ['windchill','WindChill'], ['windgust','WindGust'],   ['windcondition', 'WindCondition'],
                ['hvacstate','HVACState'], ['windspeed','WindSpeed'], ['heatsp','HeatSetPoint']
                ]


        