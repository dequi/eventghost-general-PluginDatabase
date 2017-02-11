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
#
# $LastChangedDate: 2013-10-25 $
# $LastChangedRevision: 002 $
# $LastChangedBy: rdgerken $

"""<rst>

**Envisalink Vista TPI Plugin**

Envisalink is a internet gateway for Honeywell Vista / ADEMCO security panels.


*Option/Setup*

Enter the TCP/IP address and the listening port of your Envisalink Gateway.  The 
default listening port is 4025. 

"""

import eg

eg.RegisterPlugin(
    name = "Envisalink Vista TPI",
    description = __doc__,
    author = "rdgerken",
    version = "1.0." + "$LastChangedRevision: 002 $".split()[1],
    kind = "external",
    canMultiLoad = True,
    createMacrosOnAdd = True
)

import wx
import asynchat
import socket
import asyncore
import threading
import re
from types import ClassType
                
class Text:
    tcpBox = "TCP/IP Settings"
    hostLabel = "Host:"
    portLabel = "Port:"
    userLabel = "Password:"
    passLabel = "Keypad Code:"
      
class EnvisalinkSession(asynchat.async_chat):
    """
    Handles an Envisalink TCP/IP session.
    """
     
    def __init__ (self, plugin, address):
        self.plugin = plugin

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('')
        
        # create and connect a socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.settimeout(2.0)
        try:
            self.connect(address)
        except:
            pass

    def handle_connect(self):
        """
        Called when the active opener's socket actually makes a connection. 
        """
        self.plugin.TriggerEvent("Connected")

    def handle_expt(self):
        # connection failed
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("NoConnection")
        self.close()

    def handle_close(self):
        """
        Called when the channel is closed.
        """
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("ConnectionLost")
        self.close()

    def collect_incoming_data(self, data):
        """
        Called with data holding an arbitrary amount of received data.
        """
        if self.plugin.debug:  
           print "Envisalink> " + data
        data = re.sub("([^0-9a-zA-Z:\,\.\~\#\>])", '', data)        
        arguments = data.rsplit(',')
        command = arguments[0]

        try:   
            if command.upper() == 'LOGIN:':
               self.plugin.DoCommand( self.plugin.envisalinkuser )

            #Virtual Keypad Update           
            if ( command.upper() == '00' ):
               partition   = arguments[1]
               icons = arguments[2]
               numeric = arguments[3]
               beeps = arguments[4]
               string = arguments[5]
               #Only send new event if there is an update - ignore high frequency duplicate updates from Envisalink TPI
               if (self.plugin.lastupdatevalue != 'VirtualKeypad.Partition' + partition + "." + string ):
                   self.plugin.lastupdatevalue = 'VirtualKeypad.Partition' + partition + "." + string
                   self.plugin.TriggerEvent(self.plugin.lastupdatevalue)
               if self.plugin.debug:
                   print "Envisalink> Icons=" + icons + " Numeric=" + numeric + " Beeps=" + beeps + " String=" + string 
               return

        except:
            print "Envisalink> Unexpected Response: " + data

    def found_terminator(self):
        """
        Called when the incoming data stream matches the termination 
        condition set by set_terminator.
        """

class NvAction(eg.ActionBase):  
    def __call__(self):
        self.plugin.DoCommand(self.plugin.envisalinkpass + self.command)

class Envisalink(eg.PluginBase):        
    text = Text

    def __init__(self):
        self.host = "localhost"
        self.port = 4025
        self.envisalinkuser = "user"
        self.envisalinkpass = "1234"
        self.isSessionRunning = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.session = None
        self.debug = False
        self.lastupdatevalue = ""

        group = self.AddGroup('Envisalink Virtual Keypad')
        className = 'ArmStay'
        clsAttributes = dict(name='Arm Stay', command = '3')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        className = 'ArmAway'
        clsAttributes = dict(name='Arm Away', command = '2')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        className = 'Off'
        clsAttributes = dict(name='Off', command = '1')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        self.AddAction(self.MyCommand)
        self.AddEvents()


    def __start__(
        self,
        host="192.168.1.4", 
        port=4025,
        envisalinkuser="user",
        envisalinkpass="1234",
        dummy1=None,
        dummy2=None,
        debug=False,
        lastupdatevalue = ""
    ):
        self.host = host
        self.port = port
        self.envisalinkuser = envisalinkuser
        self.envisalinkpass = envisalinkpass
        self.debug = debug
        self.lastupdatevalue = lastupdatevalue
            
        if not self.isSessionRunning:
            self.session = EnvisalinkSession(self, (self.host, self.port))
            self.isSessionRunning = True
            if self.debug:
               print "Envisalink> Session is Running" 
        
    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()

    @eg.LogIt

    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = EnvisalinkSession(self, (self.host, self.port))
           
            self.isSessionRunning = True
            if self.debug:
               print "Envisalink> Do Command Session is Running"
        try:
            if self.debug:
               print "Envisalink> Trying: " + cmdstr 
            self.session.sendall(cmdstr + "\r\n")
        except:
            self.isSessionRunning = False
            self.TriggerEvent('close')
            self.session.close()
        self.waitFlag.wait(2.0)
        self.waitStr = None
        self.waitFlag.set()

    def SetOSD(self, text):
        self.DoCommand("1200 " + text)

    def Configure(
        self,
        host="192.168.1.4",
        port=4025,
        envisalinkuser="user",
        envisalinkpass="1234",
        dummy1=None,
        dummy2=None,
        debug=False,
        lastupdatevalue=""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)       
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(envisalinkuser)
        passCtrl = panel.TextCtrl(envisalinkpass)
        debugCtrl = panel.CheckBox(debug, "")
        
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
            (text.userLabel, userCtrl),
            (text.passLabel, passCtrl),
            ('Debug', debugCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                userCtrl.GetValue(),
                passCtrl.GetValue(),
                None,
                None,
                debugCtrl.GetValue(),
            )

    class MyCommand(eg.ActionWithStringParameter):
        name = "Raw Command"
        def __call__(self, value):
            value = eg.ParseString(value)  
            self.plugin.DoCommand(value)