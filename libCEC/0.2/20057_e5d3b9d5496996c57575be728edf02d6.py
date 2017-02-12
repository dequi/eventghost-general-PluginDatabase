# -*- coding: utf-8 -*-

version="0.2" 

# plugins/libCEC/__init__.py
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

eg.RegisterPlugin(
    name = "libCEC",
    author = "Karsten Gleu",
    version = version,
    kind = "program",
    guid = "{92113271-92D9-43BE-B7F2-C1369F3ABACD}",
    description = (
        'Adds actions to control libCEC. and creates events from CEC-traffic'
    ),
    createMacrosOnAdd = False,
)

from threading import Event, Thread
from subprocess import *
import re
import os
import subprocess

findCEC = eg.WindowMatcher(u'cec-client.exe', None, None, None, None, 1, False, 0.0, 0)

class CEC(eg.PluginClass):

    def __init__(self):
        group1 = self.AddGroup("raw","raw commands")
        group1.AddAction(inputsend,'inputsend','clientinput','passes input directly to CEC Client')
        group1.AddAction(send,'send','tx','sends string via CEC Bus')
        group2 = self.AddGroup("TV", "commands for controlling TV")
        group2.AddActionsFromList(ACTIONSTV)
        group3 = self.AddGroup("Avr", "commands for controlling Audio Video Receiver")
        group3.AddActionsFromList(ACTIONSAVR)
        self.Running = False
        self.AddActionsFromList(ACTIONSTV)
        self.AddActionsFromList(ACTIONSAVR)
        self.output = ""
        self.trace1  = re.compile(r"^TRAFFIC:\s*\[\s*\d*\]\s*[>>|<<]+(?<=>>|<<)(.*)",re.M)
        self.trace2  = re.compile(r"waiting for input\r", re.M)
        self.prompt  = re.compile(r"\r", re.M)

    def __start__(self):
        eg.plugins.System.Execute(u'C:\\Windows\\System32\\taskkill.exe', u'/im cec-client.exe', 3, True, 2, u'', False, False)
        eg.plugins.System.Execute(u'C:\\Windows\\System32\\taskkill.exe', u'/im cec-tray.exe', 3, True, 2, u'', False, False)
        eg.plugins.System.Execute(u'C:\\Windows\\System32\\taskkill.exe', u'/im cecSharpTester.exe', 3, True, 2, u'', False, False)
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        self.process = Popen( ["c:\Program Files (x86)\Pulse-Eight\USB-CEC Adapter\cec-client.exe"], stdin=PIPE, stdout=PIPE,startupinfo=info)

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadLoop,
            args=(self.stopThreadEvent, )
        )
        thread.start()
        print "CEC client started"

    def __stop__(self):
        self.stopThreadEvent.set()
	self.command("q")
        self.Running = False
        print "CEC client friendly ended"

    def ThreadLoop(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
          while not self.prompt.search(self.output):
            c = self.process.stdout.read(1)
            if c == "":
                self.stopThreadEvent.set()
                self.PrintError("CEC-Client under my controll died, sorry for that")
                print 
                break
            self.output += c

          # Now we're at a prompt; clear the output buffer and return its contents
          tmp=u""
          #print self.output
          m=self.trace2.search(self.output)
          if m:
              print "cec-client.exe connected sucesfully"
              self.Running = True

          if self.Running:
            m=self.trace1.search(self.output)
            if m:
              n=re.compile(r"(?<=<<)(.*)").search(m.group(0))
              if n:
                 tmp=n.group(0)
                 self.TriggerEvent("traffictx:" + tmp)
            if m:
              n=re.compile(r"(?<=>>)(.*)").search(m.group(0))
              if n:
                 tmp=n.group(0)
                 self.TriggerEvent("traffic:" + tmp)
          self.output = ""

    def command(self, command):
        if self.Running:
          self.process.stdin.write(command + "\n")
        else:
          print "CEC Client not accepting inputs"

class send(eg.ActionClass):

    def __call__(self,myString):
        print "CEC BusTX:" + myString
        self.plugin.command("tx "+myString)

    def Configure(self, myString=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, myString)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())

class inputsend(eg.ActionClass):

    def __call__(self,myString):
        print "CEC ClientInut:" + myString
        self.plugin.command(myString)

    def Configure(self, myString=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, myString)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())

class hotKeys(eg.ActionClass):
    
    def __call__(self):
        self.plugin.command(self.value)

ACTIONSTV = (
#  (hotKeys, 'class', 'CommandName', 'CommandDescr', u'parameter'),
  (hotKeys, 'TvOn', 'TvON', 'TvOn', u'on 0'),
  (hotKeys, 'TvOff', 'TvOff', 'TvOff', u'standby 0'),
  (hotKeys, 'TVPowerRequest', 'GetTVPowerStatus', 'If TV is present, it will create a Traffic event for the power status', u'tx 10:8f'),
)

ACTIONSAVR = (
  (hotKeys, 'volup', 'volup', 'increase volume', u'volup'),
  (hotKeys, 'voldown', 'voldown', 'reduce volume', u'voldown'),
  (hotKeys, 'AmpOn', 'AmpOn', 'Activate AVR', u"on 5"),
  (hotKeys, 'AmpOff', 'AmpOff', 'Standby AVR', u'standby 5'),
  (hotKeys, 'Mute', 'Mute', 'Mute AVR', u'tx 05:44:43'),
  (hotKeys, 'AmpRequest', 'GetAVRPowerStatus', 'If AVR is present, it will create a Traffic event for the power status', u'tx 05:8f'),
)
