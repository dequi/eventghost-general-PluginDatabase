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
# $LastChangedDate: 2009-01-18 12:19:23 +0100 (So, 18 Jan 2009) $
# $LastChangedRevision: 779 $
# $LastChangedBy: bitmonster $
#
#
# 0.4 - 2011-08-10
#   - get password in plugin-configure (not realy, just pseudo)
#
# 0.3 - 2009-07-02
# - first public beta version
#


import eg

eg.RegisterPlugin(
    name        = "FRITZ!Box",
    version     = "0.4." + "$LastChangedRevision: 779 $".split()[1],
    author      = "Statistiker",
    #kind        = "program",
    description = (
                    "<p>Receives events from an AVM FRITZ!Box over TCP/IP.</p>"
    ),
    help        = (
                    '<p>To receive network messages form the FRITZ!Box, '
                    'you have to enable the Callmonitor on the FRITZ!Box.</p>'
                    '<p>enable CallMonitor:  call <b>#96*5*</b>'
                    '<br>disable CallMonitor: call <b>#96*4*</b></p>'
    ),    

)

import wx
import socket
import asynchat
import asyncore


class Text:
    host = "Host:"
    port = "Port:"
    password = "Password:"
    eventPrefix = "Event Prefix:"
    eventGenerationBox = "Event generation"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    #class Map:
     #   parameterDescription = "Event name to send:"

DEBUG = False
if DEBUG:
    log = eg.Print
else:
    def log(dummyMesg):
        pass

        
class ServerHandler(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""
    
    def __init__(self, sock, addr, plugin, server):
        log("_enter_ServerHandler__init__")        
        self.plugin = plugin
        
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self, sock)

        # Set up input line terminator
        self.set_terminator('\r')

        # Initialize input data buffer
        self.data = ''
        self.state = self.state1
        self.ip = addr[0]
        self.payload = [self.ip]
        log("_leave_ServerHandler__init__")

    def handle_close(self):
        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)
    
    
    def collect_incoming_data(self, data):
        """Put data read from socket to a buffer
        """
        # Collect data in input buffer
        log("<<" + repr(data))
        self.data = self.data + data        

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
        
        
    def state1(self, line):
        log("ServerHandler state1 start")
        line = line.decode(eg.systemEncoding)
        line.strip()
        log("line: " + line)
        part = line.split(";")
        
        for i in range(0, len(part)-1): 
            #log("Line [%d]: %s" % i, part[i])
            log("Line [%d]: %s" % (i,part[i]))
                        
        self.payload = []
        
        if part[1] == "CALL":
            log("### CALL")
            self.payload.append(part[0]) # date and time 
            log("date: " + part[0])
            self.payload.append(part[2]) # connectionID
            log("connectionID: " + part[2])
            self.payload.append(part[3]) # substation
            log("substation: " + part[3])
            self.payload.append(part[4]) # caller number
            log("caller number: " + part[4])
            self.payload.append(part[5]) # called number (MSN)
            log("called number (MSN): " + part[5])
            self.payload.append(part[6]) # isdn
            log("service: " + part[6])
            self.plugin.TriggerEvent(u'Call', self.payload)
        if part[1] == "RING":
            log("### RING")
            self.payload.append(part[0]) # date and time    
            self.payload.append(part[2]) # connectionID      
            self.payload.append(part[3]) # caller number
            self.payload.append(part[4]) # called MSN            
            self.payload.append(part[5]) # isdn
            self.plugin.TriggerEvent(u'Ring', self.payload)
        if part[1] == "DISCONNECT":
            log("### DISCONNECT")
            self.payload.append(part[0]) # date and time 
            self.payload.append(part[2]) # connectionID
            self.payload.append(part[3]) # duration in sec
            self.plugin.TriggerEvent(u'Disconnect', self.payload)
        if part[1] == "CONNECT":
            log("### CONNECT")
            self.payload.append(part[0]) # date and time 
            self.payload.append(part[2]) # connectionID
            self.payload.append(part[3]) # substation
            self.payload.append(part[4]) # number
            self.plugin.TriggerEvent(u'Connect', self.payload)



class tcp_client(asyncore.dispatcher):

    def __init__(self, host,port,handler):

        log("_enter_tcp_client__init")
        self.host = host
        self.port = port
        self.handler = handler
        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)
        
        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # restart the asyncore loop, so it notices the new socket
        eg.RestartAsyncore()
        
        self.connect( (self.host, self.port) )
        log("_leave_tcp_client__init__")
      
        
    def handle_connect(self):
        log("FRITZ!Box TCP client connect done.")
        ServerHandler(
            self,
            self.host, 
            self.handler, 
            self
        )        
        pass

    def handle_write(self):
        pass
        #print "handle_write"


    def handle_read(self):
        data = self.recv(8192)
 

    def handle_accept (self):
        log("tcp_client handle_accept")
        """Called by asyncore engine when new connection arrives"""


        
class FritzBox(eg.PluginBase):
    canMultiLoad = True
    text = Text
    
    def __init__(self):
        pass
        
        
    def __start__(self, host, port, password, prefix):
        self.host = host
        self.port = port
        self.password = password
        self.info.eventPrefix = prefix
        log("FRITZ!Box start")
        log("host = " + host)
        log("port = %d" % port)
        try:
            self.server = tcp_client(self.host,self.port,self)
            log("FritzBox __start__  self.server")
        except socket.error, exc:
            raise self.Exception(exc[1])
            print "exception ### "


    def Configure(self, host="fritz.box", port=1012, password="", prefix="FritzBox"):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)

        eventPsswrdCtrl = panel.TextCtrl(password)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        
        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st4 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st4))
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st1, hostCtrl),
            (st2, portCtrl),
        )     

        box3 = panel.BoxedGroup(
            text.eventGenerationBox, (st4, eventPrefixCtrl)
        )
        
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(box3, 0, wx.TOP|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(),
                eventPsswrdCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )



			
            