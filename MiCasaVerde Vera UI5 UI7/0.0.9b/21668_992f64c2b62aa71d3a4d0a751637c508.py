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



#*********************************THIS CODE HAS TO BE ADDED TO THE VERA*************************************
#
#     In the apps tab under Develop Apps there is a link to Edit Startup Lua.
# This code has to be copied and pasted into the Startup Lua.
# You will have to change the http server and the port as such.
#
# http://192.168.1.40:9999
#     The above is the IP address of the machine hosting EventGhost
# followed with a : and the receiving port number you specified in the Configure panel for this plugin
# The code that has to be replaced will be encapsulated in <>.
# 
#     Please be sure to copy and paste the code in it's entirety and remove all of the #'s at the 
# begining of each line
#
#*********************************COPY AND PASTE CODE BELOW*************************************
#
#
#    -- Set up all variable-watches for delayed start
#    function setWatch()   
#       luup.log("Starting Variable Watches")
#
#    -- Light Switches
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:SwitchPower1","Status",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:Dimming1","LoadLevelStatus",nil)
#
#    -- Security Sensors
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:SecuritySensor1","Armed",nil)
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:SecuritySensor1","Tripped",nil)
#
#    -- HVAC and Temp Sensors and Humidity Sensors
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:HVAC_UserOperatingMode1","ModeStatus",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:HVAC_FanOperatingMode1","Mode",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:TemperatureSensor1","CurrentTemperature",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:TemperatureSetpoint1_Heat","CurrentSetpoint",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:TemperatureSetpoint1_Cool","CurrentSetpoint",nil)
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:HumiditySensor1","CurrentLevel",nil)
#
#    -- Door Locks
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:DoorLock1","Status",nil)
#
#    -- Window Coverings
#       luup.variable_watch("EventGhostReporting","urn:upnp-org:serviceId:WindowCovering1","Status",nil)
#
#    -- Light Sensors
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:LightSensor1","CurrentLevel",nil)
#
#    -- Power Metering
#       luup.variable_watch("EventGhostReporting","urn:micasaverde-com:serviceId:EnergyMetering1","Watts",nil)
#
#    -- Day or Night Plugin
#       luup.variable_watch("EventGhostReporting","urn:rts-services-com:serviceId:DayTime","Status",nil)
#
#    -- World Weather Plugin
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","Condition",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","LocationUsedText",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","WindCondition",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","WindDirection",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","WindSpeed",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","WindGust",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","HeatIndex",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","WindChill",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","Solar",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","UV",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","Pressure",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","DewPoint",nil)
#       luup.variable_watch("EventGhostReporting","urn:upnp-micasaverde-com:serviceId:Weather1","FeelsLike",nil)
#
#    end
#    -- Wait for 60 seconds after restart then run setWatch
#    luup.call_delay("setWatch",60)
#
#    -- Send an event to EventGhost via the web server plugin
#    function sendToEG(post)
#       luup.log("Send Event to EventGhost")
#       local http = require("socket.http")
#       http.TIMEOUT=4
#       result, statuscode = socket.http.request("<http://EventGhost IP Adress:Port/>?" .. post)
#       luup.log("Status: " .. statuscode)
#    end
#
#    function EventGhostReporting(device, service, variable, lastvalue, newvalue)
#       luup.log("Switch Power Status Change")
#       luup.log("Device: " .. device)
#       luup.log("Service: " .. service)
#       luup.log("Variable: " .. variable)
#       luup.log("Last Value: " .. lastvalue)
#       luup.log("New Value: " .. newvalue)
#       strPost = "{'device_id':'" .. device .. "','service_name':'" .. service .. "','variable_name':'" .. variable .. "','old_state':'" .. lastvalue .. "','new_state':'" .. newvalue .. "'}"
#       luup.log(strPost)
#       sendToEG(strPost)
#    end
#
#*********************************END COPY AND PASTE CODE*************************************

import eg

DEVICELIST = False

if DEVICELIST:    
    deviceList = {

#  DeviceID:[     Room,     Device Name]
        '3':['Outside Front','Flood'],
        '4':['Outside Back','Flood'],
        '5':['Outside Back','Lower Deck'],
        '6':['Outside Front','Porch'],
        '7':['Office','Desk Recessed'],
        '8':['Office','Desk Recessed'],
        '9':['Theatre','Track'],
        '10':['Theatre','Overhead'],
        '11':['Hallway','Overhead'],
        '12':['Kitchen','Overhead'],
        '13':['Kitchen','Under Cabinet'],
        '14':['Dining Room','Track'],
        '15':['Outside Back','Upper Deck'],
        '16':['Living Room','Track'],
        '17':['Master Suite','Bedroom Overhead'],
        '18':['Master Suite','Bathroom Mirrors'],
        '41':['Programming','Day or Night'],
        '45':['Thermostat','House'],
        '46':['World Weather','Forcast'],
        '47':['World Weather','Current Temperature'],
        '48':['World Weather','Low Temperature'],
        '49':['World Weather','High Temperature'],
        '50':['World Weather','Humidity']
    }
else:
    deviceList = {}

#from VeraClient import *
#from VeraDevice import *
#from VeraAsyncDispatcher import *

eg.RegisterPlugin(
    name = "MiCasaVerde Vera UI5 UI7",
    description = "Control of Dimmers and Switches on the MiCasaVerde Vera UI5 UI7",
    author = "Created by Rick Naething / Last Updated by Brandon Simonsen (m19bradon) & Kevin Schlosser (kgschlosser)",
    version = "0.0." + "$LastChangedRevision: 9b $".split(' ')[1],
    canMultiLoad = True,
    kind = "other",
    guid = '{321D9F7C-6961-4C62-B6E0-86C950A25279}'
    
)

#---------------------------To-Do----------------------------#
# Update the configure panel for the plugin
# Close Telnet port after receiving data???

#---------------------------K Code---------------------------#
import ast
import sys
import asynchat
import asyncore
import socket
import threading
import time
#------------------------------------------------------------#

import urllib
import json

#---------------------------K Code---------------------------#
DEBUG = False
if DEBUG:
    log = eg.Print
else:
    def log(dummyMesg1,dummyMesg2=None):
        pass

class ServerHandler(asynchat.async_chat):

    def __init__(self, sock, addr, plugin, server):

        log("Server Thread Started")
        self.plugin = plugin
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator('\n')
        self.data = ''
        self.VeraDB = {}


    def handle_close(self):

        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)


    def collect_incoming_data(self, data):
        
        log("Incoming: " + repr(data))
        self.data = self.data + data


    if DEBUG:
        def push(self, data):

            log("Outgoing: ", repr(data))
            asynchat.async_chat.push(self, data)


    def ProcessInData(self, pData):

        if pData[:6] == 'GET /?':
            log('Incoming Data: ',repr(pData))
            pData = str(pData[6:-9])
            log('Incoming Data Modified: ', repr(pData))

            try:
                self.SendEvent(ast.literal_eval(pData))
            except:
                eg.PrintError("Error 6: Evaluating in data: " + str(sys.exc_info()))


    def SendEvent(self,sendPayload):

        devID = '.'+deviceList[sendPayload['device_id']][0]+'.' \
            +deviceList[sendPayload['device_id']][1]+'.' \
                if DEVICELIST else '.DeviceID-'+sendPayload['device_id']+'.'

        serviceName = sendPayload['service_name'].split(':')
        newState = sendPayload['new_state']
        var = sendPayload['variable_name']

        kwargs = dict(prefix='Vera',suffix='',payload=sendPayload)

        if serviceName[3] == 'SwitchPower1':
            kwargs['suffix'] = 'Switch'+devID

            kwargs['suffix'] += 'Off' if newState == '0' \
                                    else 'On'

        elif serviceName[3] == 'Dimming1':
            kwargs['suffix'] = 'Dimmer'+devID+'DimLevel-'+newState

        elif serviceName[3] == 'SecuritySensor1':
            kwargs['suffix'] = 'Security'+devID

            if var == 'Armed':
                kwargs['suffix'] += 'Disarmed' if newState == '0' \
                                        else 'Armed'

            elif var == 'Tripped':
                if newState == '1':
                    kwargs['suffix'] += 'Tripped'

                else:
                    return

        elif serviceName[3] == 'HVAC_UserOperatingMode1':
            kwargs['suffix'] = 'HVAC'+devID+'Mode-'+newState

        elif serviceName[3] == 'HVAC_FanOperatingMode1':
            kwargs['suffix'] = 'HVAC'+devID+'FanMode-'+newState

        elif serviceName[3] == 'TemperatureSensor1':
            kwargs['suffix'] = 'Temperature'+devID+'Current-'+newState

        elif serviceName[3] == 'TemperatureSetpoint1_Heat':
            kwargs['suffix'] = 'HVAC'+devID+'HeatSetTemperature-'+newState

        elif serviceName[3] == 'TemperatureSetpoint1_Cool':
            kwargs['suffix'] = 'HVAC'+devID+'CoolSetTemperature-'+newState

        elif serviceName[3] == 'HumiditySensor1':
            kwargs['suffix'] = 'Humidity'+devID+'Current-'+newState

        elif serviceName[3] == 'DoorLock1':
            kwargs['suffix'] = 'Doorlock'+devID

            kwargs['suffix'] += 'Unlocked' if newState == '0' \
                                    else 'Locked'

        elif serviceName[3] == 'WindowCovering1':
            kwargs['suffix'] = 'WindowCovering'+devID

            kwargs['suffix'] += 'Closed' if newState == '0' \
                                    else 'Open'

        elif serviceName[3] == 'LightSensor':
            kwargs['suffix'] = 'LightSensor'+devID

            kwargs['suffix'] += 'Dark' if newState == '0' \
                                    else 'Light'

        elif serviceName[3] == 'EnergyMetering1':
            kwargs['suffix'] = 'Energy'+devID+'WattsUsed-'+newState

        elif serviceName[3] == 'DayTime':
            kwargs['suffix'] = 'DayTime'+devID

            kwargs['suffix'] += 'Night' if newState == '0' \
                                    else 'Day'

        elif serviceName[3] == 'Weather1':
            kwargs['suffix'] = 'WorldWeather'+devID+var

        else:
            kwargs['suffix'] = 'NewDevice'+devID[-1:]

        eg.TriggerEvent(**kwargs)

    def found_terminator(self):

        inData = self.data
        self.data = ''
        self.ProcessInData(inData)


    def initiate_close(self):
        try:
            self.close_when_done()
        except:
            eg.PrintError("Error 1: Closing Socket: " + str(sys.exc_info()))
        
        self.plugin.EndLastEvent()
        try:
            self.close()
        except:
            eg.PrintError("Error 2: Closing Socket: " + str(sys.exc_info()))


class Server(asyncore.dispatcher):

    def __init__ (self, port, handler):
        try:
            self.handler = handler
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            eg.RestartAsyncore()
            self.bind(('', int(port)))
            self.listen(5)
        except:
            eg.PrintError("Error 3: Server Init: " + str(sys.exc_info()))

    def handle_accept (self):
        
        log("Incoming connection")
        try:
            (sock, addr) = self.accept()
            ServerHandler(
                sock,
                addr,
                self.handler,
                self
            )
        except:
            eg.PrintError("Error 4: Accept Connection: " + str(sys.exc_info()))

#------------------------------------------------------------#

#-----------------------------------------------------------------------------
class Vera(eg.PluginBase):

    def __init__(self):

        self.AddEvents()
        self.AddAction(SetSwitchPower)
        self.AddAction(TogglePower)
        self.AddAction(SetDimming)
        self.AddAction(RunScene)
        self.AddAction(RampUp)
        self.AddAction(RampDown)
        self.HTTP_API   = VERA_HTTP_API()
        #self.dispatcher = VeraAsyncDispatcher()
        self.vera       = []
        self.verbose = True
        self.server = None
        eg.RestartAsyncore()


    def Configure(self, ip="127.0.0.1", port1="3480", verbose=True, port2="3480"):

        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, ip)
        textControl2 = wx.TextCtrl(panel, -1, port1)
        textControl3 = wx.TextCtrl(panel, -1, port2)
        checkbox = panel.CheckBox(verbose, 'Verbose Outputs')
        panel.sizer.Add(wx.StaticText(panel, -1, 'IP address of Vera'))
        panel.sizer.Add(textControl)
        panel.sizer.Add(textControl2)
        panel.sizer.Add(checkbox)
        panel.sizer.Add(textControl3)
        while panel.Affirmed():
            panel.SetResult(
                        textControl.GetValue(),
                        textControl2.GetValue(),
                        checkbox.GetValue(),
                        textControl3.GetValue())


    def __start__(self, ip='127.0.0.1', port1='3480', verbose=True, port2="3480"):

        self.ip = ip
        self.port1 = port1
        self.verbose = verbose
        self.lock = threading.Lock()
        self.port2 = port2
        self.info.eventPrefix = 'Vera'
        self.prefix='Vera'

        try:
            self.server = Server(self.port2, self)

        except socket.error, exc:
            eg.PrintError("Error 5: Vera Start")
            raise self.Exception(exc[1])

        self.HTTP_API.connect(ip=ip, port1=port1)
        #self.vera       = VeraClient(ip, self.veraCallback, self.veraDebugCallback, self.dispatcher)


    def __stop__(self):

        if self.server:
            self.server.close()
        self.server = None


    def __close__(self):

        if self.server:
            self.server.close()
        self.server = None           
        
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
        self.port1 = "3480"
        return

    def connect(self, ip=None, port1=None):
        if ip: self.ip = ip
        if port1: self.port1 = port1
        print 'HTTP API connected'

    def send(self, url):
        try:
            #responce = urllib.urlopen('http://'+self.ip+':'+self.port+url).readlines()
            consumer = urllib.urlopen('http://'+self.ip+':'+self.port1+url)
            responce = consumer.readlines()
            consumer.close()
        except IOError:
            eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port1+'\n'+ url)
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


class RampDown(eg.ActionBase):
    name = "Ramp Down a Dimmer"
    description = "Dim the lights on a dimmer at a desired speed"

    def __call__(self,startLevel,endLevel,deviceID,speed):

        if startLevel <= endLevel:
            eg.PrintNotice("the Starting Level has to be greater than the End Level")
            return

        for level in range(startLevel,endLevel):
            time.sleep(speed)
            eg.plugins.Vera.SetDimming(deviceID,level)


class RampUp(eg.ActionBase):
    name = "Ramp Up a Dimmer"
    description = "Raise the lights on a dimmer at a desired speed"

    def __call__(self,startLevel,endLevel,deviceID,speed):

        if startLevel >= endLevel:
            eg.PrintNotice("the Starting Level has to be less than the End Level")
            return

        for level in range(endLevel,startLevel):
            time.sleep(speed)
            eg.plugins.Vera.SetDimming(deviceID,level)