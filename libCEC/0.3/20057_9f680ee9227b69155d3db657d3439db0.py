# -*- coding: utf-8 -*-

version="0.3" 

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
        'Adds actions to control libCEC and creates events from CEC-traffic\nVersion ' + version
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5907",
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
        group4 = group3.AddGroup("TX-SR578","Commands for controlling Onkyo AVR TX-SR578")
        group4.AddActionsFromList(ACTIONSONKYOAVRTXSR578)
        group3.AddActionsFromList(ACTIONSAVR)
        self.Running = False
        self.AddActionsFromList(ACTIONSTV)
        self.AddActionsFromList(ACTIONSAVR)
        self.output = ""
        self.trace1  = re.compile(r"^TRAFFIC:\s*\[\s*\d*\]\s*[>>|<<]+(?<=>>|<<)(.*)",re.M)
        self.trace2  = re.compile(r"waiting for input\r", re.M)
        self.trace3  = re.compile(r"(?<=CEC Parser created - )(.*)", re.M)
        self.trace4  = re.compile(r"^ERROR:\s*\[\s*\d*\]\s+(.*)",re.M)
        self.prompt  = re.compile(r"\r", re.M)

    def __start__(self, clientpath, taskkill,waittillconnected):
        self.clientpath=clientpath
        self.taskkill=taskkill
        self.waittillconnected=waittillconnected
        try:
          eg.plugins.System.Execute(taskkill, u'/im cec-client.exe', 3, True, 2, u'', False, False)
          eg.plugins.System.Execute(taskkill, u'/im cec-tray.exe', 3, True, 2, u'', False, False)
          eg.plugins.System.Execute(taskkill, u'/im cecSharpTester.exe', 3, True, 2, u'', False, False)
        except:
	  print taskkill + " could not be started,\nplease configure plugin correctly"
          pass

        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        try:
          self.process = Popen( [self.clientpath,"-r", "-t", "r", "-t", "p", "-d","9"], stdin=PIPE, stdout=PIPE,startupinfo=info)
        except:
          print clientpath + " could not be started"
          raise

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadLoop,
            args=(self.stopThreadEvent, )
        )
        thread.start()
        print "CEC client started ("+ self.clientpath + " -r -t r -t p -d 9)"

    def __stop__(self):
        self.stopThreadEvent.set()
	self.command("q")
        self.Running = False
        print "CEC client friendly ended"

    def Configure(self, clientpath="c:\Program Files (x86)\Pulse-Eight\USB-CEC Adapter\cec-client.exe",taskkill=u'C:\\Windows\\System32\\taskkill.exe',waittillconnected=True):
        panel = eg.ConfigPanel()
        clientCtrl = eg.FileBrowseButton(
            panel,
            size=(320,-1),
            initialValue=clientpath,
            startDirectory=eg.folderPath.ProgramFiles,
            labelText="",
            fileMask = "CEC client Executable|cec-client.exe|All-Files (*.*)|*.*",
            buttonText=eg.text.General.browse,
        )
        panel.AddLabel("Path to libCEC CEC client (cec-client.exe)\n")
        panel.AddCtrl(clientCtrl)
        taskkillCtrl = eg.FileBrowseButton(
            panel,
            size=(320,-1),
            initialValue=taskkill,
            startDirectory="C:\\Windows\\System32",
            labelText="",
            fileMask = "taskkill Executable|taskkill.exe|All-Files (*.*)|*.*",
            buttonText=eg.text.General.browse,
        )
        panel.AddLabel("Path to Windows taskkill.exe\n")
        panel.AddCtrl(taskkillCtrl)
        waittillconnectedCtrl = wx.CheckBox(panel, -1, "wait with events until connected")
	waittillconnectedCtrl.SetValue(waittillconnected)
        panel.AddCtrl(waittillconnectedCtrl)

        while panel.Affirmed():
            panel.SetResult(clientCtrl.GetValue(), taskkillCtrl.GetValue(), waittillconnectedCtrl.GetValue())

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
              print "CEC client is waiting for inputs"
              self.Running = True
          
          m=self.trace3.search(self.output)
          if m:
              print "CEC client is of " + m.group(0)
          
          m=self.trace4.search(self.output)
          if m:
              print "CEC reported ERROR: " + m.group(0)
              self.TriggerEvent("ERROR")
              self.TriggerEvent(m.group(0))

          if self.Running or not self.waittillconnected:
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

#Here are the Onkyo AVR ( TX-SR578 ) codes I added into the plugin on my PC :)
#It would probably be better to replace the 'Select Input' descriptions with just 'Input 1, Input 2' etc. rather than the actual labels on the Onkyo amp. These may work with other brands?
ACTIONSONKYOAVRTXSR578=(
(hotKeys, 'avr.end', 'AVR End Keypress', 'Signals that the button has stopped being pressed. Use if you find the button being pressed multiple times', u'tx 15:45'),
(hotKeys, 'avr.up', 'AVR Up', 'Press up button or Tuner Up', u'tx 15:44:01'),
(hotKeys, 'avr.down', 'AVR Down', 'Press down button or Tuner down', u'tx 15:44:02'),
(hotKeys, 'avr.left', 'AVR Left', 'Press left button', u'tx 15:44:03'),
(hotKeys, 'avr.right', 'AVR Right', 'Press right button', u'tx 15:44:04'),
(hotKeys, 'avr.setmenu', 'AVR Setup Menu', 'Open Setup Menu', u'tx 15:44:0A'),
(hotKeys, 'avr.exit', 'AVR Exit', 'Exit from Menu', u'tx 15:44:0D'),
(hotKeys, 'avr.enter', 'AVR Enter', 'Enter or Select Item', u'tx 15:44:2B'),
(hotKeys, 'avr.soundfield', 'AVR Sound Field Toggle', 'Toggle between sound fields', u'tx 15:44:33'),
(hotKeys, 'avr.input', 'AVR Input Toggle', 'Toggle between AV inputs', u'tx 15:44:34'),
(hotKeys, 'avr.osd', 'AVR OSD', 'On Screen Display', u'tx 15:44:35'),
(hotKeys, 'avr.volumeup', 'AVR Volume Up', 'Volume Up', u'tx 15:44:41'),
(hotKeys, 'avr.volumedown', 'AVR Volume Down', 'Volume Down', u'tx 15:44:42'),
(hotKeys, 'avr.mute', 'AVR Mute Toggle', 'Toggle between Mute and Un-Mute', u'tx 15:44:43'),
(hotKeys, 'avr.muteon', 'AVR Mute On', 'Turn On Mute', u'tx 15:44:65'),
(hotKeys, 'avr.muteoff', 'AVR Mute Off', 'Turn Off Mute - Restore volume', u'tx 15:44:66'),
(hotKeys, 'avr.input1', 'AVR BD/DVD Select', 'Select Input - BD/DVD', u'tx 15:44:69:01'),
(hotKeys, 'avr.input2', 'AVR VCR/DVR Select', 'Select Input - VCR/DVR', u'tx 15:44:69:02'),
(hotKeys, 'avr.input3', 'AVR CBL/SAT Select', 'Select Input - CBL/SAT', u'tx 15:44:69:03'),
(hotKeys, 'avr.input4', 'AVR GAME Select', 'Select Input - GAME', u'tx 15:44:69:04'),
(hotKeys, 'avr.input5', 'AVR AUX Select', 'Select Input - AUX', u'tx 15:44:69:05'),
(hotKeys, 'avr.input6', 'AVR TUNER Select', 'Select Input - TUNER', u'tx 15:44:69:06'),
(hotKeys, 'avr.input7', 'AVR TV/CD Select', 'Select Input - TV/CD', u'tx 15:44:69:07'),
(hotKeys, 'avr.input8', 'AVR PORT Select', 'Select Input - PORT', u'tx 15:44:69:08'),
(hotKeys, 'avr.input1on', 'AVR BD/DVD Power', 'Select Input - BD/DVD', u'tx 15:44:6A:01'),
(hotKeys, 'avr.input2on', 'AVR VCR/DVR Power', 'Select Input - VCR/DVR', u'tx 15:44:6A:02'),
(hotKeys, 'avr.input3on', 'AVR CBL/SAT Power', 'Select Input - CBL/SAT', u'tx 15:44:6A:03'),
(hotKeys, 'avr.input4on', 'AVR GAME Power', 'Select Input - GAME', u'tx 15:44:6A:04'),
(hotKeys, 'avr.input5on', 'AVR AUX Power', 'Select Input - AUX', u'tx 15:44:6A:05'),
(hotKeys, 'avr.input6on', 'AVR TUNER Power', 'Select Input - TUNER', u'tx 15:44:6A:06'),
(hotKeys, 'avr.input7on', 'AVR TV/CD Power', 'Select Input - TV/CD', u'tx 15:44:6A:07'),
(hotKeys, 'avr.input8on', 'AVR PORT Power', 'Select Input - PORT', u'tx 15:44:6A:08'),
(hotKeys, 'avr.power', 'AVR Power Toggle', 'Toggle Power', u'tx 15:44:6B'),
(hotKeys, 'avr.poweroff', 'AVR Power Off', 'Power Off', u'tx 15:44:6C'),
(hotKeys, 'avr.poweron', 'AVR Power On', 'Power On', u'tx 15:44:6D'), 
)