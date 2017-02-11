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
# This plugin is based on the Network Event Receiver written by bitmonster
# DSNER means Dead Simple Network Event Receiver
# This plugin is intended to generate events in eg when anything is received from the network
# No password, no payload, just send it a string terminated by \n and it will 
# generate the corresponding event in eg.
# DNSES doesn't exists as plugins already exists to exchange data whith eg through the network
# You can use telnet to test it
#
# $LastChangedDate: 2010-12-16 12:00:00 +0200 (TH, 16 Dec 2010) $
# $LastChangedRevision: 0001 $
# $LastChangedBy: miljbee $

import eg

eg.RegisterPlugin(
    name = "DSNER",
    description = "Receives events from the Network.",
    version = "1.0." + "$LastChangedRevision: 0001 $".split()[1],
    author = "miljbee",
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQb1MiCRwAAAVVJREFUOMud"
        "kjFLw2AQhp8vif0fUlPoIgVx6+AgopNI3fwBViiIoOAgFaugIDhUtP4BxWDs4CI4d3MR"
        "cSyIQ1tDbcHWtjFI4tAWG5pE8ca7997vnrtP4BOZvW0dSBAcZ0pAMTEzPUs4GvMsVkvP"
        "6HktGWRAOBpjIXVNKOSWWdYXN7lFAAINhBCEQgqxyTHAAQQAD/dFbLurUYJYT7P7TI2C"
        "VavwIiZodyyaH6ZLo/RZVTXiOYVhGOh5jcpbq5eRAXAc5wdBVSPMLR16GtxdbgJgN95d"
        "OxicACG6bPH4uIu1UHjE7sFqR/NDVxhaoixLvFYbtDufNFtu1tzxgdeAaZfBU7ECTvd1"
        "WRlxsa4sp1ydkiRxkstmlEFRrWT4nrRer3vmlf6mb883fK8AoF1d+Bqc6Xkt+cufT6e3"
        "dnb9DJJrq+uYpunZ2WcFfA0ol8v8N5Qgvr/EN8Lzfbs+L0goAAAAAElFTkSuQmCC"
    ),
)

import wx
import asynchat
import asyncore
from hashlib import md5
import random
import socket


class Text:
    port = "TCP/IP Port:"
    eventPrefix = "Event Prefix:"
    tcpBox = "TCP/IP Settings"
    eventGenerationBox = "Event generation"
    
    
DEBUG = False
if DEBUG:
    log = eg.Print
else:
    def log(dummyMesg):
        pass
    

class ServerHandler(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""
    
    def __init__(self, sock, addr, plugin, server):
        log("Server Handler inited")
        self.plugin = plugin
        
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self, sock)

        # Set up input line terminator
        self.set_terminator('\n')

        # Initialize input data buffer
        self.data = ''
        self.state = self.state1
        self.ip = addr[0]
        self.payload = [self.ip]
                  
                
    def handle_close(self):
        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)
    
    
    def collect_incoming_data(self, data):
        """Put data read from socket to a buffer
        """
        # Collect data in input buffer
        log("<<" + repr(data))
        self.data = self.data + data


    if DEBUG:
        def push(self, data):
            log(">>", repr(data))
            asynchat.async_chat.push(self, data)
    
    
    def found_terminator(self):
        """
        This method is called by asynchronous engine when it finds
        command terminator in the input stream
        """   
        # Take the complete line
        line = self.data

        # Reset input buffer
        self.data = ''

        #call state handler
        self.state(line)


    def initiate_close(self):
        self.state = self.state1
        self.close()
 

    def state1(self, line):
        self.plugin.TriggerEvent(line.strip(), self.payload)
        self.initiate_close()
        
        
        
class Server(asyncore.dispatcher):
    
    def __init__ (self, port, handler):
        self.handler = handler

        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)
        
        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # restart the asyncore loop, so it notices the new socket
        eg.RestartAsyncore()

        # Set it to re-use address
        #self.set_reuse_addr()
        
        # Bind to all interfaces of this host at specified port
        self.bind(('', port))

        # Start listening for incoming requests
        #self.listen (1024)
        self.listen(5)


    def handle_accept (self):
        """Called by asyncore engine when new connection arrives"""
        # Accept new connection
        log("handle_accept")
        (sock, addr) = self.accept()
        ServerHandler(
            sock, 
            addr, 
            self.handler, 
            self
        )



class NetworkReceiver(eg.PluginBase):
    text = Text
    
    def __init__(self):
        self.AddEvents()
    
    def __start__(self, port, prefix):
        self.port = port
        self.info.eventPrefix = prefix
        try:
            self.server = Server(self.port, self)
        except socket.error, exc:
            raise self.Exception(exc[1])
        
        
    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None


    def Configure(self, port=1024, prefix="DSNER"):
        text = self.text
        panel = eg.ConfigPanel()
        
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st3))
        box1 = panel.BoxedGroup(text.tcpBox, (st1, portCtrl))
        box3 = panel.BoxedGroup(
            text.eventGenerationBox, (st3, eventPrefixCtrl)
        )
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box3, 0, wx.EXPAND|wx.TOP, 10),
        ])
        
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(), 
                eventPrefixCtrl.GetValue()
            )