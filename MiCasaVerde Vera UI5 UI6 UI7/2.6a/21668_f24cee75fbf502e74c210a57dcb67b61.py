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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, gave me inspiration at the least.
# This plugin is currently being tested by the members of the EventGhost Forum, m19brandon, blaher, kgschlosser (the artist that is K)
# WinoOutWest, loveleejohn, kkl... I thank these people for being the first to tell me the errors which I am hoping are solved,
# but if not you know where to find me.


import eg

eg.RegisterPlugin(
    name = "MiCasaVerde Vera UI5 UI6 UI7",
    description = "Control of the MiCasaVerde Vera UI5 UI6 UI7",
    author = "K",
    version = "2.6a",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    kind = "external",
    guid = '{321D9F7C-6961-4C62-B6E0-86C950A25279}',
    icon= (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAQCAYAAAB3AH1ZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAA"
        "A7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAAJaSURBVEhL5ZNbiIxhGMe/8xwNw7BNs1NryipJ29"
        "RO0V6QNqE2yqF1yq5DO7usZbNklLiQGxkXbC4lbpQLFw6L4oKUKIcLN5Jib9QKUUrx+898o7nB52KkPPXrOb7v87zv937Gvy4uOFX"
        "z70nMsqwS3DdN6ybcNk3zDv52chqoseJ53iya9UEvjUehjL0WRkhPqVY1WGi2X7iu2+Y4znx/iHV+uqHi0mgXeoaxo7DF6G8frDDQ"
        "vpK7mUOul5yHXgOHoIif0kLsblQTuodbbEUP++y0bXuRSjKZjHRE9T8VTnsBLtH4qDFQ+FZha34zsedsdgB9A63mG7FHWfIGUvjj+"
        "NfhWCQSacbfA3vhILEnqs3lcpOptdXnV9IKX+xsotPoL7zj9I/ZZBuxcU7SyUbPKlW+4D8i34eeIL/YD0vMRCIxNZ1Op0Kh0ELyHx"
        "Wrpn4jFJ+BMZqXjJ62VdivaFKE9aQ/4T+sgf+e+DD2BO+lQ+vRBfyncA/uqg6+krKUDyLN8Nme5C1l8yHsF+BywuVs9DIWizXVQ84"
        "h/mMA7Mus2ydboj/rTwfQJsfhAeZbNttQjRpxeE38CH9IHubpwSlBrH6Ac3BNOZiNrRv9QCr4AMg0Fp2HU9j1D6eFWBmuwhjDXVEQ"
        "+ywDza1U8CjxT8ItuMjNdUGZeLA3EI1G8/F4fDqmGmtqLczV7HA4nE0mk1nfr6HaKLkFrNWvWYvPVE5/BjrYABR3cXWDDDLCqQ7zn"
        "buJreA1n4AlNOlQDbpEzSa0OE2uRTnWLlOMmiL2EHo17GbrYAP8R2IY3wGjEGZSjHVwLgAAAABJRU5ErkJggg=="
        )
    
)

import os
import sys
import json
import time
import socket
import random
import datetime
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

ACTIONDICT = {
    'DimmSt': {'Dev': ['Dimmable Light'],'Var': [''],'Sts': ['wx'],'Cho': []},
    'Dimmer': {'Dev': ['Dimmable Light'],'Var': ['prct'],'Sts': ['wx','SpinIntCtrl(prct,max=100)'],'Cho': []},
    'Toggle': {'Dev': ['Dimmable Light','Switch'],'Var': [''],'Sts': ['wx'],'Cho': []},
    'Scenes': {'Dev': ['scenes'],'Var': [''],'Sts': ['wx'],'Cho': []},
    'Alarms': {'Dev': [],'Var': ['stat'],'Sts': ['wx'],'Cho': ["DISARM","ARM"]},
    'RampDm': {'Dev': ['Dimmable Light'],'Var': ['strt','stop','incr','sped'], 'Sts': ['wx','SpinIntCtrl(strt,max=100)',
                'SpinIntCtrl(stop,max=100)','SpinNumCtrl(incr,increment=0.25)',
                'SpinNumCtrl(sped,increment=0.25)'],'Cho': []},
    'Switch': {'Dev': ['Dimmable Light','Switch'],'Var': ['stat'],'Sts': ['wx','wx'],'Cho': ["Off","On"]},
    'FanMod': {'Dev': ['Thermostat'],'Var': ['mode'],'Sts': ['wx','wx'],'Cho': [
                "Auto","PeriodicOn","ContinuousOn","FollowSchedule"]},
    'OppMod': {'Dev': ['Thermostat'],'Var': ['mode'],'Sts': ['wx','wx'],'Cho': [
                "Off","CoolOn","HeatOn","AutoChangeOver"]},
    'HStTmp': {'Dev': ['Thermostat'],'Var': ['temp'],'Sts': ['wx','SpinIntCtrl(temp,'],'Cho': []},
    'CStTmp': {'Dev': ['Thermostat'],'Var': ['temp'],'Sts': ['wx','SpinIntCtrl(temp,'],'Cho': []}
    }


class Text:
    PrefixBox = 'Event Prefix Settings'
    PrefixText = 'Event Prefix: '
    VeraBox = 'Vera IP and Port Settings'
    VeraIPText = 'IP: '
    VeraPortText = 'Port: '
    ToggleBox = 'Toggle a Light or Binary Switch to Opposite of Current State'
    DimmStBox = 'Get Dimmer Level'
    ScenesBox = 'Run A Scene'
    ScenesText = 'Scene: '
    RampDmBox = 'Ramp Dimmer Up or Down'
    StrtText = 'Start Percent: '
    StopText = 'Stop Percent: '
    IncrText = 'Brightness Steps: '
    SpedText ='Speed: '
    DimmerBox = 'Set the Dim Level of a Dimmable Switch'
    DimmerText = 'Level: '
    SwitchBox = 'Turn a Light or Binary Switch On or Off'
    SwitchText = 'ON or OFF: '
    FanModBox = 'HVAC Fan Mode'
    FanModText = 'Fan Mode: '
    OppModBox = 'HVAC Opperating Mode'
    OppModText = 'Opperating Mode: '
    HStTmpBox = 'HVAC Heat Set Temperature'
    HStTmpText = 'Set Teperature: '
    CStTmpBox = 'HVAC Cool Set Temperature'
    CStTmpText = 'Set Teperature: '
    AlarmsBox = 'Arm or Disarm Alarm'
    AlarmsText = 'Arm or Disarm: '
    DeviceText = 'Device: '
    MinEvtText = 'Reduce Events: '
    EvtPayText = 'Generate Payload Data: '
    UpdateBox = 'How Fast to get Device Updates from Vera, Remember Faster Uses MORE CPU'
    UpSpeedText = 'Seconds: '
    WattBox = 'Calculate KiloWatt Hours and Cost'
    CostText = 'Cost per KiloWatt Hour: '
    MonthText = 'Month: '
    WattDevText = 'Device: (leave 0 for all Devices)'
    WattsFPBox = 'Watts Saved Data'
    WattsFPText = 'Watts File: '
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
    class CalculateWatts:
        name = 'Energy Usage'
        description = 'Calculate Monthly Energy Consumption and Cost'
    class ToggleVacationMode:
        name = 'Vacation Mode'
        description = 'Randomly turn on and off lights while you are not home'
    class VeraDeviceList:
        name = 'Vera Device List'
        description = 'Returns the parsed data recieved from the vera unit'

class DimmerStatus(eg.ActionBase):

    text = Text

    def __call__(self, devc=0):
        return self.plugin.ActionCall(dict(SendType='DimmSt', Device=devc, Func=self.plugin.DimmerStatus))

    def Configure(self, devc=" "):
        panel = eg.ConfigPanel()    
        exec(self.plugin.ActionConfig('DimmSt', devc))
        ConfigCode(self.text, panel)

class RampDimmer(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, strt=0, stop=0, incr=0.0, sped=0.0):
        self.plugin.ActionCall(dict(
            SendType='Dimmer',Device=devc,Func=self.plugin.RampThread.Start,
            strt=strt, stop=stop, incr=incr, sped=sped))

    def Configure(self, devc=" ", strt=0, stop=0, incr=0.0, sped=0.0):
        panel = eg.ConfigPanel()    
        exec(self.plugin.ActionConfig('RampDm', devc))
        ConfigCode(self.text, panel, strt=strt, stop=stop, incr=incr, sped=sped)

class Scene(eg.ActionBase):

    text = Text

    def __call__(self, devc=0):
        self.plugin.ActionCall(dict(SendType='Scenes',Device=devc,Func=self.plugin.VERA_HTTP_API.send))

    def Configure(self, devc=" "):
        panel = eg.ConfigPanel()    
        exec(self.plugin.ActionConfig('Scenes', devc))
        ConfigCode(self.text, panel)

class Dimmer(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, prct=0):

        self.plugin.ActionCall(dict(SendType='Dimmer',Device=devc,Func=self.plugin.VERA_HTTP_API.send,prct=prct))

    def Configure(self, devc=" ", prct=0):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('Dimmer', devc))
        ConfigCode(self.text, panel, prct=prct)

class Switch(eg.ActionBase):

    text = Text
    
    def __call__(self, devc=0, stat=0):
        self.plugin.ActionCall(dict(SendType='Switch',Device=devc,Func=self.plugin.VERA_HTTP_API.send,stat=stat))
        
    def Configure(self, devc=" ", stat="Off"):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('Switch', devc))
        ConfigCode(self.text, panel, stat=stat)

class Toggle(eg.ActionBase):

    text = Text
    
    def __call__(self, devc=0):
        self.plugin.ActionCall(dict(SendType='Toggle',Device=devc,Func=self.plugin.VERA_HTTP_API.send))

    def Configure(self, devc=" "):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('Toggle', devc))
        ConfigCode(self.text, panel)

class FanMode(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, mode=0):
        self.plugin.ActionCall(dict(SendType='FanMod',Device=devc,Func=self.plugin.VERA_HTTP_API.send,mode=mode))

    def Configure(self, devc=" ", mode="Auto"):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('FanMod', devc))
        ConfigCode(self.text, panel, mode=mode)

class OppMode(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, mode=2):
        self.plugin.ActionCall(dict(SendType='OppMod',Device=devc,Func=self.plugin.VERA_HTTP_API.send,mode=mode))

    def Configure(self, devc=" ", mode="HeatOn"):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('OppMod', devc))
        ConfigCode(self.text, panel, mode=mode)

class HSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, temp=70):
        self.plugin.ActionCall(dict(SendType='HStTmp',Device=devc,Func=self.plugin.VERA_HTTP_API.send,temp=temp))

    def Configure(self, devc=" ", temp=70):
        if self.plugin.DefaultThermalUnit == 'C' and temp == 70:
            temp = (temp - 32) * 5.0/9.0
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('HStTmp', devc))
        ConfigCode(self.text, panel, temp=temp)

class CSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, devc=0, temp=70):
        self.plugin.ActionCall(dict(SendType='CStTmp',Device=devc,Func=self.plugin.VERA_HTTP_API.send,temp=temp))

    def Configure(self, devc=" ", temp=70):
        if self.plugin.DefaultThermalUnit == 'C' and temp == 70:
            temp = (temp - 32) * 5.0/9.0
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('CStTmp', devc))
        ConfigCode(self.text, panel, temp=temp)

class Alarm(eg.ActionBase):

    text = Text

    def __call__(self, stat=1):
        self.plugin.ActionCall(dict(SendType='Alarms',Func=self.plugin.VERA_HTTP_API.send,stat=stat))

    def Configure(self, stat="ARM"):
        panel = eg.ConfigPanel()
        exec(self.plugin.ActionConfig('Alarms'))
        ConfigCode(self.text, panel, stat=stat)

class CalculateWatts(eg.ActionBase):

    text = Text

    def __call__(self, device=0, cost=0.12, month=0):

        device = False if device == 0 else str(device)
        month = datetime.date.today().month if month == 0 else month

        self.plugin.CalculateWatts(device, float(cost), month)

    def Configure(self, device=0, cost=0.12, month=0):

        text = self.text
        panel = eg.ConfigPanel()
        month = datetime.date.today().month if month == 0 else month

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinNumCtrl(cost, increment=0.01, min=0.01)
        st3 = panel.SpinIntCtrl(month, min=1, max=12)

        box1 = panel.BoxedGroup(
                            text.WattBox,
                            (text.WattDevText, st1),
                            (text.CostText, st2),
                            (text.MonthText, st3)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue()
                            )


class ToggleVacationMode(eg.ActionBase):

    text = Text

    def __call__(self):
        if self.plugin.VacationMode:
            self.plugin.VacationMode = False
        else:
            self.plugin.VacationMode = True
        self.plugin.Vacation()
        return self.plugin.VacationMode

class VeraDeviceList(eg.ActionBase):

    text = Text

    def __call__(self):
        return dc(self.plugin.VDL)

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
        self.AddAction(CalculateWatts)
        self.AddAction(ToggleVacationMode)
        self.AddAction(VeraDeviceList)

        self.VDL = {'Counters':{}, 'Event':{}, 'NewItems': {}, 'Items': {}}
        self.ItemLog = []
        self.VacationRunList = []
        self.Startup = True
        self.VacationMode = False
        self.Watts = {}

    def __start__(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera', minimalEvents=False, genPayload = True, inc=0.10, wattsFilePath='C:\\'):
        self.MinimalEvents = minimalEvents
        self.GenPayload = genPayload
        self.UpSpeed = inc
        self.info.eventPrefix = prefix
        self.prefix = prefix

        if wattsFilePath != 'C:\\':
            self.wattsFilePath = wattsFilePath
        else:
            self.wattsFilePath = False
            PN("Start", "No Location to load/save watts file")

        self.RampThreadDict = {}
        self.HTTPStartup = True
        self.HTTPConnected = False
        self.Server = Server(self)
        self.server = self.Server.Start(ip=ip, port=port)
        self.VERA_HTTP_API = VERA_HTTP_API(self)
        self.RampThread = RampThread(self)
        self.LoadWattsFile()

    def __close__(self):

        self.SaveWattsFile()
        self.RampThread.Stop()

    def __stop__(self):

        if self.VacationMode:
            self.VacationMode = False
            self.Vacation()
        self.SaveWattsFile()
        self.RampThread.Stop()
        if self.server:
            self.Server = self.Server.Close(self.server)

    def Vacation(self, CountDown=False):

        if CountDown:
            PN('Vacation Mode Running', 'Next Event CountDown', 
                ' Scheduled Off Time', str((CountDown[0]-60)/60)+' Min', ' Next Scheduled Run', str((CountDown[1]-60)/60)+' Min')
            if CountDown[0] != 0 and CountDown[1] != 0:
                self.VacationRunList.append(eg.scheduler.AddTask(60, self.Vacation, [CountDown[0]-60, CountDown[1]-60]))

        elif self.VacationMode:
            dimmers = dc(self.VDL['Vacation']['Dimmer'])
            switches = dc(self.VDL['Vacation']['Switch'])
            Combined = dimmers
            Combined.extend(switches)
            random.shuffle(Combined,random.random)
            ranIDX = random.randrange(0, len(Combined), 1)

            Func = False
            ranOffTime = random.randrange(0, 2000, 1)
            ranNewRunTime = random.randrange(0, 1000, 1)

            for switch in switches:
                if Combined[ranIDX] == switch:
                    Func = eg.plugins.Vera.Toggle
            if Func:
                Func(str(Combined[ranIDX]))
                self.VacationRunList.append(eg.scheduler.AddTask(ranOffTime, Func, str(Combined[ranIDX])))
            else:
                ranBrightness = random.randrange(0, 101, 1)
                Func = eg.plugins.Vera.Dimmer
                Func(str(Combined[ranIDX]), ranBrightness)
                self.VacationRunList.append(eg.scheduler.AddTask(ranOffTime, Func, str(Combined[ranIDX]), 0))
            self.VacationRunList.append(eg.scheduler.AddTask(ranNewRunTime, self.Vacation))

            PN('Vacation Mode Running','Triggered Device',Combined[ranIDX],
                ' Scheduled Off Time',str(ranOffTime/60)+' Min', ' Next Scheduled Run', str(ranNewRunTime/60)+' Min')
            self.VacationRunList.append(eg.scheduler.AddTask(60, self.Vacation, [ranOffTime, ranNewRunTime]))
        else:
            PN('Shutting Down Vacation Mode')
            for task in self.VacationRunList:
                try: eg.scheduler.CancelTask(task)
                except: pass
            self.VacationRunList = []

    def ActionCall(self, kwargs):

        SendType = kwargs['SendType']
        Func = kwargs['Func']
        Device = False
        try:
            Device = kwargs['Device']
            del(kwargs['Device'])
        except: pass
        try: kwargs['stat'] = "1" if kwargs['stat'] == 'On' or kwargs['stat'] == 'ARM' else "0"
        except: pass
        try: kwargs['prct'] = str(kwargs['prct'])
        except: pass
        try: kwargs['temp'] = str(kwargs['temp'])
        except: pass
        del(kwargs['Func'])

        devc = False

        if Device:
            for Type in ['Dimmable Light', 'Switch', 'Thermostat', 'scenes']:
                for name, devID in self.ACL[Type]:
                    if str(Device) == devID or str(Device) == name:
                        devc = devID
        if devc:
            kwargs['devc'] = devc
            for Kind in ['Dimmer', 'Switch', 'Scenes']:
                if SendType == Kind: self.RampThread.CheckRamp(devc)

        if (SendType and devc) or SendType == 'Alarms':
            return Func(**kwargs)


    def ActionConfig(self, SendType, device=False):

        devc = " "

        StsList = ACTIONDICT[SendType]['Sts']
        DevList = ACTIONDICT[SendType]['Dev']
        VarList = ACTIONDICT[SendType]['Var']
        VChoice = ACTIONDICT[SendType]['Cho']

        DChoice = [" "]

        if device:
            for DevType in DevList:
                for name, devID in self.ACL[DevType]:
                    if str(device) == devID or str(device) == name:
                        devc = name
                    DChoice.append(name)
            DChoice.sort()

        VarCode = 'def ConfigCode(text, panel, prct=False, mode=False,'
        VarCode += 'temp=False, strt=False, stop=False, incr=False, sped=False, stat=False):\n\t'
        ConfigCode = '\n\t'
        SetSelectCode = '\n\t'
        EqualizeCode = '\n\teg.EqualizeWidths(('
        BoxCode = '\n\tbox1=panel.BoxedGroup(text.'+SendType+'Box,'
        SetResultCode = '\n\twhile panel.Affirmed():\n\t\tpanel.SetResult('

        def WXCode(st, choice, item):
            Code = ''
            cList = ['=wx.Choice(parent=panel, pos=(10,10))\n\t','.AppendItems(strings=',')\n\tif not isinstance("',
                    '", int):\n\t\tif ','.count("','")==0:\n\t\t\t','.Select(n=0)\n\t\telse:\n\t\t\t',
                    '.SetSelection(int(','.index("','")))\n\telse:\n\t\t','.SetSelection("','")\n\t']
            vList = [st, st, choice, item, choice, item, st, st, choice, item, st, item]
            for i in range(12):
                Code += vList[i]+cList[i]
            ResultCode = st+'.GetStringSelection(),'
            return Code, ResultCode

        def EGCode(st, item):
            Code = st+'=panel.'+item
            if item.find('temp') > -1:
                minTemp = 50
                maxTemp = 90
                if self.DefaultThermalUnit == 'C':
                    minTemp = (minTemp - 32) * 5.0/9.0
                    maxTemp = (maxTemp - 32) * 5.0/9.0
                Code += 'min='+str(minTemp)+', max='+str(maxTemp)+')'
            Code += '\n\t'
            ResultCode = st+'.GetValue(),'
            return Code, ResultCode

        for i in range(len(StsList)):
            st = 'st'+str(i+1)
            EqualizeCode += st+','

            vName = VarList[i] if i == 0 else VarList[i-1]

            BoxCode += '(text.DeviceText,'+st+'),' if i == 0 and device and DevList != ['scenes'] \
                                else '(text.'+SendType+'Text,'+st+'),' if len(VarList) < 2 \
                                else '(text.'+vName.capitalize()+'Text,'+st+'),'

            Code, ResultCode = WXCode(st, str(DChoice), devc) if StsList[i] == 'wx' and i == 0 and device\
                                else WXCode(st, str(VChoice), vName) if StsList[i] == 'wx' \
                                else EGCode(st, StsList[i])
            ConfigCode+= Code
            SetResultCode += ResultCode
                
        EqualizeCode += '))\n'
        BoxCode += ')\n\tpanel.sizer.Add(box1, 0, wx.EXPAND)\n'
        SetResultCode += ')\n'

        return VarCode+ConfigCode+SetSelectCode+EqualizeCode+BoxCode+SetResultCode

    def DimmerStatus(self, SendType, devc):
        return float(self.VDL['devices'][devc]['level'])

    def CalculateWatts(self, DevID, Cost, Month):

        if DevID:
            try:
                DevWatts = dc(self.Watts[DevID])
                DevKWH = 0
                if DevWatts != []:
                    for i in range(len(DevWatts)):
                        if len(DevWatts[i]) == 7:
                            DevKWH += DevWatts[i][6] if DevWatts[i][1][1] == Month else 0
                    DevUsage = float(DevKWH) * Cost
                print "Device ID: ", DevID, ", KiloWatt Hours Used: ", DevKWH, ", Cost Month to Date: ", DevUsage
                return [DevKWH, DevUsage]
            except:
                eg.PrintNotice("MicasaVerdeVera: CalculateWatts: Unknown Device ID: "+DevID)
        else:
            DeviceUsage = {}
            CombinedKWH = 0
            for DevID, Data in self.Watts.iteritems():
                DevKWH = 0
                if Data == []: continue
                else:
                    for i in range(len(Data)):
                        if len(Data[i]) == 7:
                            DevKWH += Data[i][6] if Data[i][1][1] == Month else 0
                    CombinedKWH += DevKWH
                    DeviceUsage[DevID] = [DevKWH, float(DevKWH)*Cost]
            AllUsage = float(CombinedKWH)*Cost

            print "Device ID: AllDevices,  KiloWatt Hours Used: ", CombinedKWH, ", Cost Month to Date: ", AllUsage

            return [CombinedKWH, AllUsage, DeviceUsage]

    def Configure(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera', minimalEvents=False, genPayload = True, inc=0.10, wattsFilePath='C:\\'):

        text = self.text

        panel = eg.ConfigPanel()

        st1 = panel.TextCtrl(ip)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(prefix)
        st4 = panel.CheckBox(minimalEvents)
        st5 = panel.CheckBox(genPayload)
        st6 = panel.SpinNumCtrl(inc, increment=0.05, min=0.10)
        st7 = panel.FileBrowseButton(wattsFilePath)
 
        eg.EqualizeWidths((st1, st2, st3, st4, st5, st6, st7))
                
        box1 = panel.BoxedGroup(
                            text.VeraBox,
                            (text.VeraIPText, st1),
                            (text.VeraPortText, st2)
                            )
        box2 = panel.BoxedGroup(
                            text.PrefixBox,
                            (text.PrefixText,st3),
                            (text.MinEvtText,st4),
                            (text.EvtPayText,st5)
                            )
        box3 = panel.BoxedGroup(
                            text.UpdateBox,
                            (text.UpSpeedText,st6)
                            )
        box4 = panel.BoxedGroup(
                            text.WattsFPBox,
                            (text.WattsFPText,st7)
                            )

        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND),
            (box3, 0, wx.EXPAND),
            (box4, 0, wx.EXPAND)
            ])

        while panel.Affirmed():
            panel.SetResult(
                        st1.GetValue(),
                        st2.GetValue(),
                        st3.GetValue(),
                        st4.GetValue(),
                        st5.GetValue(),
                        st6.GetValue(),
                        st7.GetValue()
                        )

    def LoadWattsFile(self):
        if self.wattsFilePath:
            f = False
            try:
                f = open(self.wattsFilePath, 'r')
                Data = ''.join(f.readlines())
                f.close()
                if Data != '':
                    try: self.Watts = eval(Data)
                    except: PE("LoadWattsFile", "EVAL", sys.exc_info())
            except IOError:
                self.SaveWattsFile()

    def SaveWattsFile(self):
        if self.wattsFilePath:
            f = False
            try:
                f = open(self.wattsFilePath, 'w') 
                f.write(str(self.Watts))
                f.close()
            except: PE("SaveWattsFile", "Open", sys.exc_info())


    def ReadWatts(self, DevID, Watts):
        def NewUsage(Wattage):
            StartTime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.time(datetime.datetime.now()))
            StartTime = time.mktime(StartTime.timetuple())
            DateStamp = datetime.date.today()
            return [Wattage, [DateStamp.day, DateStamp.month], float(StartTime)]
            
        if DevID not in self.Watts:
            currData = []
            if Watts > 0:
                currData = [NewUsage(Watts)]
            self.Watts[DevID] = currData

        elif self.Watts[DevID] == [] and Watts != 0:
            currData = [NewUsage(Watts)]
            self.Watts[DevID] = currData
        elif DevID in self.Watts and self.Watts[DevID] != []:
            currData = self.Watts[DevID]
            currWatts = currData[len(currData)-1]
            WattsUsed = currWatts[0]
            DateStamp = currWatts[1]
            StartTime = currWatts[2]

            if len(currWatts) == 3:
                Today = datetime.date.today()
                if WattsUsed != Watts or DateStamp != [Today.day, Today.month]:
                    EndTime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.time(datetime.datetime.now()))
                    EndTime = time.mktime(EndTime.timetuple())
                    ActiveTime = float(EndTime)-float(StartTime)
                    HoursActive = ((ActiveTime/60)/60)
                    KiloWattHours = ((HoursActive*WattsUsed)/1000)        
                    newData = [WattsUsed,DateStamp,StartTime,EndTime,ActiveTime,HoursActive,KiloWattHours]
                    self.Watts[DevID][len(self.Watts[DevID])-1] = newData
                    if Watts > 0:
                        newData = NewUsage(Watts)
                        self.Watts[DevID].append(newData)
            elif Watts != 0:
                newData = NewUsage(Watts)
                self.Watts[DevID].append(newData)
        self.SaveWattsFile()

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

        ACL = {}
        VDL = {'Counters':{}, 'Event':{}, 'NewItems': {}, 'Items': {}}

        mType =[['devices', 0],['scenes',1],['rooms',2],
                ['categories',3],['sections',4]]

        if "temperature" in tmp:
            self.DefaultThermalUnit = tmp['temperature']

        def BuildEvt(evtData, Type):
            ID = str(evtData['id'])
            midfix = [['room'], ['name'], ['category']]
            for i in range(3):
                S=False
                try: S = evtData[midfix[i][0]]
                except: S = None
                if S == None:
                    S = Type if i == 2 else ID if Type == 'device' and i == 1 else None
                midfix[i].append(S)
            return ID, midfix

        def BuildAct(ID, evtData):
            config = ['Dimmable Light', 'Switch', 'Thermostat', 'scenes']
            for Type in config:
                if evtData[2][1] and evtData[2][1] == Type:
                    try: config = [evtData[0][1]+', '+evtData[1][1]+', '+ID, ID]
                    except:
                        try: config = [evtData[0][1]+', '+ID, ID]
                        except:
                            try: config = [evtData[1][1]+', '+ID, ID]
                            except: config =  [ID, ID]
                    if Type in ACL:
                        for device in ACL[Type]:
                            config = False if config == device else config
                        if config: ACL[Type].append(dc(config))
                    else:
                        ACL[Type] = [dc(config)]

        def BuildVacation(ID, evtData):
            vaca = ['Dimmable Light', 'Switch']
            if 'Vacation' not in VDL:
                VDL['Vacation']={'Dimmer':[], 'Switch':[]}
            if evtData[2][1] and evtData[2][1] == vaca[0]:
                VDL['Vacation']['Dimmer'].append(ID)
            if evtData[2][1] and evtData[2][1] == vaca[1]:
                VDL['Vacation']['Switch'].append(ID)
               
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
                            if self.Startup and 'watts' in oldData:
                                self.ReadWatts(str(oldData['id']), int(oldData['watts']))

                            if Type == 'devices' or Type == 'scenes':
                                ID, midfix = BuildEvt(oldData, Type)
                                BuildAct(ID, midfix)
                                BuildVacation(ID, midfix)
                                VDL['Items'][ID] = dict(midfix)

                                for i in range(3): midfix[i] = midfix[i][1]
                                midfix = [['.'.join([midfix[0] ,midfix[1].replace(' Weather','')])] \
                                            if midfix[0] != None else [midfix[1]], midfix[2]]
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
            self.Startup = False
        else:
            OI = dc(self.VDL['Items'])
            OC = dc(self.VDL['Counters'])
            self.EventDetector(
                            dc(VDL['devices']),
                            dc(VDL['scenes']),
                            dc(self.VDL['devices']),
                            dc(self.VDL['scenes'])
                            )
   
        NI, NC  = NewItemsReporting(NI, NC, OI, OC)
        VDL['NewItems'] = NI
        VDL['Counters'] = NC
                
        self.VDL = dc(VDL)
        self.ACL = dc(ACL)

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
                                            if newItem == 'watts':
                                                self.ReadWatts(newID, int(newValue))

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

    def Start(self, **kwargs):
        try:
            device = kwargs['devc']
            self.RunningRamp = True
            t = threading.Thread(name='Ramp-'+str(device), target=self.RunRamp, kwargs=kwargs,)
            t.start()
            self.plugin.RampThreadDict[str(device)] = t
        except: t = PE("RampThread", "Start", sys.exc_info())
        finally: return t

    def RunRamp(self, SendType, devc, strt, stop, incr, sped):
        inc = float('-'+str(incr)) if strt > stop else float(incr)
        stp = float(stop+1) if stop > strt else float(stop-1)
        strt = float(strt)
        sped = float(sped)

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
            for i in frange(strt, stp, inc):
                self.plugin.VERA_HTTP_API.send(SendType=SendType, devc=devc, prct=str(i))
                time.sleep(sped)
            self.RunningRamp = False

    def CheckRamp(self, devce):
        if str(devce) in self.plugin.RampThreadDict:
            self.Stop(self.plugin.RampThreadDict[str(devce)])
            del self.plugin.RampThreadDict[str(devce)]
            PN('RampThread', 'CheckRamp', 'RampStopped', devce)

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

    def __init__ (self, plugin):

        self.plugin = None
        self.VERA_HTTP_API = VERA_HTTP_API(plugin)
        self.DataThreadList = []
        self.ServerThread = None
        self.RunningUpdate=False
        self.DataThread=False
        self.plugin = plugin

    def Start(self, ip, port):

        self.lock = threading.Lock()
        self.DataThread=True
        self.RunningUpdate = self.ConnectHTTPAPI(ip, port)
        if self.RunningUpdate: return self.StartServerThread()
        else: return False

    def ConnectHTTPAPI(self, ip, port):

        return self.VERA_HTTP_API.connect(ip=ip, port=port)

    def StartServerThread(self):
        try:
            self.t = threading.Thread(name='Vera-Receive', target=self.RequestUpdate)
            self.t.start()
        except: self.t = PE("Server", "StartServerThread", sys.exc_info())
        finally: return self.t

    def RequestUpdate(self):
        while self.RunningUpdate:
            try:
                data = self.VERA_HTTP_API.send('ComRoomList')
                log("Server", 'RequestUpdate', repr(data))
                if data: self.EvalData(data)
                time.sleep(self.plugin.UpSpeed)
            except:
                PE("Server", "RequestUpdate", sys.exc_info())
                time.sleep(15)

    def EvalData(self, data):
        log("Server", 'EvalData', repr(data))
        try: self.DataReadThread(dc(json.loads(data)))
        except: PE("Server", "EvalData", sys.exc_info(), [data])
                
    def DataReadThread(self, data):
        try: self.plugin.UpdateDevices(data)
        except: PE("Server", "DataReadThread", sys.exc_info())
        finally: return
        
    def Close(self, t):
        self.RunningUpdate = False
        PN('Server', 'Server ShutDown')
        return None
        
 
class VERA_HTTP_API:

    def __init__(self, plugin):
        self.plugin = plugin

    def connect(self, ip=None, port=None):
        self.plugin.VeraIP = ip
        self.plugin.VeraPort = port

        self.plugin.HTTPConnected = PN("VERA_HTTP_API", "Connection Successful") if self.send('ComRoomList') \
                            else PE("VERA_HTTP_API", "Connection Failure", "IP", ip, "Port", port)

        self.plugin.HTTPStartup = False

        return self.plugin.HTTPConnected
    
    def send(self, SendType, stat=False, devc=False, mode=False, temp=False, prct=False):

        if not self.plugin.HTTPConnected and not self.plugin.HTTPStartup: return False

        stat == '1' if stat and stat == 'On' else '0' if stat else False

        self.IPPort = str(self.plugin.VeraIP)+":"+str(self.plugin.VeraPort)
        self.HostData = dc(URLS.DATA['HostData'])
        self.HostData[3][1] = self.IPPort
        self.HostData[3] = "".join(self.HostData[3])

        Request = ''
        SendType = dc(URLS.DATA[SendType])
        for line in SendType:
            Request += line+devc if line[-11:] == '&DeviceNum=' or line[-10:] == '&SceneNum=' else line
        Request += prct if prct else stat if stat else temp if temp else mode if mode else ''
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
        sock.connect((self.plugin.VeraIP, self.plugin.VeraPort))
        sock.settimeout(5.0)
        sock.sendall(url)
        answer = sock.recv(4096)
        while answer:
            Response += answer
            answer = sock.recv(4096)
        sock.close()

        try:
            Response = Response[39:]
            Response = Response[10:] if Response[:10] == 'ion/json\r\n' else Response          
        except: Response = PE("VERA_HTTP_API", "SendData", sys.exc_info(), [Response])

        return Response

class URLS:
        DATA = {
        'Dimmer'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget=" ],
        'Switch'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue="],
        'Toggle'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:micasaverde-com:serviceId:HaDevice1&action=ToggleState"],
        'Scenes'       : ["GET /data_request?id=lu_action&serviceId=urn:micasaverde-com:","serviceId:HomeAutomationGateway1&action=RunScene&SceneNum="],
        'FanMod'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_FanOperatingMode1&action=SetMode&NewMode="],                                                                                                                                                         
        'OppMod'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_UserOperatingMode1&action=SetModeTarget&NewModeTarget="],                                                                                                                                        
        'CStTmp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Cool&action=SetCurrentSetpoint&NewCurrentSetpoint="], 
        'HStTmp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Heat&action=SetCurrentSetpoint&NewCurrentSetpoint="],
        'Alarms'       : ["GET /data_request?id=action&output_format=xml&Category=4&serviceId=urn:micasaverde-com:","serviceId:SecuritySensor1&action=SetArmed&newArmedValue="],
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