# -*- coding: utf-8 -*-
#
# plugins/Pioneer_AV_NET/__init__.py
# 
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import socket
import select
import re
from time import sleep
from threading import Event, Thread
numbers=["0","1","2","3","4","5","6","7","8","9"]
charDic={0:'',1:'',2:'',3:'',4:unichr(135),5:'[)',6:'(]',7:'I',8:'II',9:'< ',10:' >',11:'<3',12:'.',13:'.0',14:'.5',15:unichr(216),16:'0',17:'1',18:'2',19:'3',20:'4',21:'5',22:'6',23:'7',24:'8',25:'9',26:'A',27:'B',28:'C',29:'F',30:'M',31:unichr(175),140:'<-',141:'^',142:'->',143:'v',144:'+',145:' ',146:' '}
VSTArray=[2,4,5,6,7,8,10,11,12,13,14,16,17,22,24,25,30,32,33,38,40,42,44,45,50]
VSTDic={1:"Input_Terminal",2:"Input_Resolution",4:"Input_aspect",5:"Input_color_format",6:"Input_bit",7:"Input_extend_color space",8:"Output_Resolution",10:"Output_aspect",11:"Output_color_format",12:"Output_bit",13:"Output_extend_color space",14:"HDMI_1_Monitor_Recommend_Resolution_Information",16:"HDMI_1_Monitor_DeepColor",17:"HDMI_1_Monitor_Extend_Color_Space",22:"HDMI_2_Monitor_Recommend_Resolution_Information",24:"HDMI_2_Monitor_DeepColor",25:"HDMI_2_Monitor_Extend_Color_Space",30:"HDMI_3_Monitor_Recommend_Resolution_Information",32:"HDMI_3_Monitor_DeepColor",33:"HDMI_3_Monitor_Extend_Color_Space",38:"Input_3D_format",40:"Output_3D_format",42:"HDMI_OUT_4_Monitor_Recommend_Resolution_Information",44:"HDMI_OUT_4_Monitor_DeepColor",45:"HDMI_OUT_4_Monitor_Extend_Color_Space"}
ASTArray=[3,5,26,44,46,48,52,53,55,56]
ASTDic={1:"Audio_Input_Signal",3:"Audio_Input_Frequency",5:"Audio_Input_Channel_Format",26:"Audio_Output_Channel",44:"Audio_Output_Frequency",46:"Audio_Output_bit",48:"Reserved",52:"Working_PQLS",53:"Working_Auto_Phase_Control_Plus",55:"Working_Auto_Phase_Control_Plus_(Reverse_Phase)"}


eg.RegisterPlugin(
    name = "Pioneer_AV_NET",
    author = "Sem;colon",
    version = "0.8",
    kind = "external",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=10&t=3836",
    description = "Control Pioneer A/V Receivers via Ethernet (Tested with VSX-922)"
)

class Pioneer_AV_NET(eg.PluginBase):
    hosts={}
    instances=[]
    comms=["Log","Event","Don't show"]

    def __init__(self):
        self.AddAction(AddHost, "AddHost", "Add Host", "Creates a new connection.", None)
        self.AddAction(RemoveHost, "RemoveHost", "Remove Host", "Closes a connection.", None)
        self.AddAction(SendCommand, "SendCommand", "Send Command", "Sends some text through the connection.", None)

    def __start__(self):
        for i in range(0,len(self.instances)):
            self.hosts[self.instances[i]].startThread()
        
    def __stop__(self):
        for i in range(0,len(self.instances)):
            self.hosts[self.instances[i]].stopThreadEvent.set()
            self.hosts[self.instances[i]].Disconnect()
        
    def OnComputerSuspend(self):
        self.__stop__()
    
    def OnComputerResume(self):
        self.__start__()
        
    def makeHostString(self, host):
        if host=="":
            hoststr=""
        else:
            hoststr="."+host
        return hoststr

class Controller():
    
    def __init__(self, ip, port, timeout, host, comm, plugin):
        self.plugin=plugin
        self.plugin.instances.append(host)
        self.plugin.hosts[host]=self
        self.ip = ip
        self.port = int(port)
        self.timeout = float(timeout)
        self.host=host
        self.comm=comm
        self.FLDisplay=""
        self.connected=False
        self.startThread()
    
    def startThread(self):
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.Receive,
            args=(self.stopThreadEvent, )
        )
        thread.start()
    
    def isAlive(self, host, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host,port))
            sock.close()
            return True
        except:
            return False
        
    def Connect(self, ip, port, timeout, host):
        if self.connected==False and self.isAlive(ip, port, timeout):
            print 'Pioneer_AV_NET: Host "'+host+'" found on the network, trying to connect to '+ip+':'+str(port)+' ...'
            hoststr = self.plugin.makeHostString(host)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.settimeout(timeout)
                s.connect((ip, port))
                s.setblocking(False)
                self.socket = s
                self.connected=True
                self.plugin.TriggerEvent("Connected"+hoststr)
            except Exception as e:
                print "Pioneer_AV_NET: Failed to connect to " + ip + ":" + str(port), e
                
    
    def Disconnect(self):
        if self.connected:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.connected=False
            hoststr = self.plugin.makeHostString(self.host)
            self.plugin.TriggerEvent("Disconnected"+hoststr)
    
    def Receive(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            if self.connected:
                try:
                    ready = select.select([self.socket], [], [self.socket], self.timeout)
                    # the first element of the returned list is a list of readable sockets
                    if ready[0]:
                        hoststr = self.plugin.makeHostString(self.host)
                        self.timeoutTwoCounter = 0
                        # 1024 bytes should be enough for every received event
                        response = self.socket.recv(1024)
                        # splits the received string in substrings for every event
                        splitter="\r\n"
                        responseArray=response.split(splitter)
                        responseArrayLen=len(responseArray)-1
                        for i in range(0, responseArrayLen, 1):
                            response=responseArray[i]
                            if response!="":
                                if response[:2]=="FL":
                                    # data displayed on the receiver
                                    response1=response[:2]
                                    response2=response[2:]
                                    response3=""
                                    while response2!="":
                                        # converts hex to latin-1
                                        character=int(response2[:2], 16)
                                        if character<32 or (character>=140 and character<=146):
                                            character=charDic[character]
                                        else:
                                            character=unichr(character)
                                        response3=response3+character
                                        response2=response2[2:len(response2)]
                                    response4=unicode(response3.encode(eg.systemEncoding).decode(eg.systemEncoding))
                                    if self.comm=="Log":
                                        print "Pioneer_AV_NET.Display"+hoststr+": "+response4
                                    elif self.comm=="Event":
                                        self.plugin.TriggerEvent(response1+hoststr, payload=response4)
                                    self.plugin.FLDisplay=response4#saves the data to the variale "FLDisplay"
                                else:
                                    self.plugin.TriggerEvent(response+hoststr)
                                    if response[:3]=="AST" or response[:3]=="VST":
                                        responseArr=self.SST(response)
                                        responseArrLen=len(responseArr)
                                        if responseArrLen==1 and responseArr[0][0]=="none":
                                            print "Pioneer_AV_NET: Unknown Response: "+response
                                        else:
                                            for y in range(0, responseArrLen,1):
                                                ###Events without payload:###
                                                #self.plugin.TriggerEvent(responseArr[y][0]+responseArr[y][1]+hoststr)
                                                ###Events with payload:###
                                                self.plugin.TriggerEvent(responseArr[y][0]+hoststr, payload=responseArr[y][1])
                                    else:
                                        responseLen=len(response)
                                        for y in range(0, responseLen,1):
                                            if response[y] in numbers:
                                                response1=response[:y]
                                                response2=response[y:]
                                                self.plugin.TriggerEvent(response1+hoststr, payload=response2)
                                                break
                except Exception as e:
                    if not "[Errno 9]" in str(e):
                        print "Pioneer_AV_NET: ERROR:",e
                    self.Disconnect()
            else:
                self.Connect(self.ip, self.port, self.timeout, self.host)
                sleep(3)
            stopThreadEvent.wait(0.1)
    
    
    def SST(self, data):
        mode=data[:3]
        data=data[3:]
        dataLength=len(data)
        response=[]
        y=1
        if mode=="VST":
            for i in VSTArray:
                i2=i-1
                if dataLength>=i2:
                    if VSTDic[y]!="Reserved":
                        response.append([mode+"."+VSTDic[y],data[y-1:i2]])
                    y=i
                else:
                    break
        elif mode=="AST":
            for i in ASTArray:
                i2=i-1
                if dataLength>=i2:
                    if ASTDic[y]!="Reserved":
                        response.append([mode+"."+ASTDic[y],data[y-1:i2]])
                    y=i
                else:
                    break
        else:
            response=[["none"]]
        return response
        
class AddHost(eg.ActionBase):

    class text:
        tcpBox = "Connection Settings"
        ip = "Hostname/IP:"
        port = "Port:"
        timeout = "Timeout in s:"
        egBox = "EventGhost Settings"
        host = "Alias in EventGhost (unique!):"
        comm = "Show display changes as:"
    
    def __call__(self, ip, port=8102, timeout=1, host="", comm="Log"):
        if host in self.plugin.instances:
            print 'Pioneer_AV_NET: Host "'+host+'" already exists!'
            return False
        else:
            Controller(ip, port, timeout, host, comm, self.plugin)
            print 'Pioneer_AV_NET: Host "'+host+'" added!'
            return True

    def Configure(self, ip="", port=8102, timeout=1, host="", comm="Log"):
        text = self.text
        panel = eg.ConfigPanel()
        wx_ip = panel.TextCtrl(ip)
        wx_port = panel.SpinIntCtrl(port, min=0, max=65535)
        wx_timeout = panel.SpinNumCtrl(timeout)
        wx_host = panel.TextCtrl(host)
        wx_comm = wx.Choice(panel, -1, choices=self.plugin.comms)
        wx_comm.SetSelection(self.plugin.comms.index(comm))
        
        st_ip = panel.StaticText(text.ip)
        st_port = panel.StaticText(text.port)
        st_timeout = panel.StaticText(text.timeout)
        st_host = panel.StaticText(text.host)
        st_comm = panel.StaticText(text.comm)
        eg.EqualizeWidths((st_ip, st_port, st_timeout, st_host, st_comm))

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st_ip, wx_ip),
            (st_port, wx_port),
            (st_timeout, wx_timeout),
        )
        egBox = panel.BoxedGroup(
            text.egBox,
            (st_host, wx_host),
            (st_comm,wx_comm),
        )

        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(egBox, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                wx_ip.GetValue(),
                wx_port.GetValue(),
                wx_timeout.GetValue(),
                wx_host.GetValue(),
                wx_comm.GetStringSelection()
            )

class RemoveHost(eg.ActionBase):
    
    class text:
        hostName="Host:"
    
    def __call__(self, host=""):
        if host in self.plugin.instances:
            inst=self.plugin.instances.index(host)
            self.plugin.hosts[host].stopThreadEvent.set()
            self.plugin.hosts[host].Disconnect()
            del self.plugin.hosts[host]
            del self.plugin.instances[inst]
            print 'Pioneer_AV_NET: Host "'+host+'" removed!'
            return True
        else:
            print 'Pioneer_AV_NET: Host "'+host+'" does not exist!'
            return False
        
    
    def Configure(self, host=""):
        panel = eg.ConfigPanel()
        text = self.text
        st_host = panel.StaticText(text.hostName)
        wx_host = wx.Choice(panel, -1, choices=self.plugin.instances)
        if host in self.plugin.instances:
            wx_host.SetSelection(self.plugin.instances.index(host))

        panel.AddLine(st_host,wx_host)

        while panel.Affirmed():
            panel.SetResult(wx_host.GetStringSelection())
            
class SendCommand(eg.ActionBase):

    class text:
        commandBox = "Command Settings"
        command = "Code to send:"
        hostName="Host:"
    
    def __call__(self, Command, host=""):
        if host in self.plugin.instances:
            if self.plugin.hosts[host].connected:
                line = Command + "\x0D"
                ready = select.select([], [self.plugin.hosts[host].socket], [], self.plugin.hosts[host].timeout)
                if ready[1]:
                    self.plugin.hosts[host].socket.sendall(line)
                sleep(0.1)
            else:
                hoststr = self.plugin.makeHostString(host)
                self.plugin.TriggerEvent("Host_not_connected"+hoststr,Command)
        else:
            print 'Pioneer_AV_NET: Host "'+host+'" does not exist!'
        

    def Configure(self, Command="", host=""):
        panel = eg.ConfigPanel()
        text = self.text
        st_command = panel.StaticText(text.command)
        wx_command = panel.TextCtrl(Command)
        st_host = panel.StaticText(text.hostName)
        wx_host = wx.Choice(panel, -1, choices=self.plugin.instances)
        if host in self.plugin.instances:
            wx_host.SetSelection(self.plugin.instances.index(host))
        eg.EqualizeWidths((st_host, st_command))

        panel.AddLine(st_host,wx_host)
        panel.AddLine(st_command,wx_command)

        while panel.Affirmed():
            panel.SetResult(wx_command.GetValue(),wx_host.GetStringSelection())
