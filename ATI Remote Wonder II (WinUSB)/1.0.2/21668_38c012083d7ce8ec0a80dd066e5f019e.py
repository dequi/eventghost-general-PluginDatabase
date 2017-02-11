# -*- coding: utf-8 -*-
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

r"""<rst>
Plugin for the `ATI Remote Wonder II`__ remote.

|

.. image:: picture.jpg
   :align: center

__ http://ati.amd.com/products/remotewonder2/index.html
"""


import eg

eg.RegisterPlugin(name="ATI Remote Wonder II (WinUSB)",
                  description=__doc__,
                  url="http://www.eventghost.net/forum/viewtopic.php?t=915",
                  author="Bitmonster",
                  version="1.0.2",
                  kind="remote",
                  hardwareId="USB\\VID_0471&PID_0602",
                  guid="{74DBFE39-FEF6-41E5-A047-96454512B58D}",
                  )


from math import atan2, pi
from eg.WinApi.Dynamic import mouse_event
from copy import deepcopy as copy
from threading import Timer


class Text:
    EventBox = 'Event Settings'
    PrefixLbl = 'Prefix:'
    EnduringLbl = 'Enduring Events:'
    MouseBox = 'Mouse Settings'
    MouseSpeedLbl = 'Mouse Speed:'
    MouseAccelLbl = 'Mouse Acceleration:'
    MouseResetDesc = 'Unchecking this next option will keep the current speed\n' \
                     'and acceleration if you change the direction of the mouse.'
    MouseResetLbl = 'Direction Change Reset:'
    MouseTimeoutDesc = 'This is the amount of time it will take before the speed\n' \
                       'and acceleration reset back to their base values.'
    MouseTimeoutLbl = 'Reset Time:'
    MouseTimeoutSuf = 'seconds'
    MouseResDesc = 'Resolution Factor controls the amount of "wiggle room"\n' \
                   'you will have on the speed and acceleration.'
    MouseResLbl = 'Resolution Factor:'
    DebuggingBox = 'Debugging'
    DebuggingLbl = 'Show Incoming Data:'

    class EVENTS:
        CODES = {0  : "Num0",
                 1  : "Num1",
                 2  : "Num2",
                 3  : "Num3",
                 4  : "Num4",
                 5  : "Num5",
                 6  : "Num6",
                 7  : "Num7",
                 8  : "Num8",
                 9  : "Num9",
                 12 : "Power",
                 13 : "Mute",
                 16 : "VolumeUp",
                 17 : "VolumeDown",
                 32 : "ChannelUp",
                 33 : "ChannelDown",
                 40 : "FastForward",
                 41 : "FastRewind",
                 44 : "Play",
                 48 : "Pause",
                 49 : "Stop",
                 55 : "Record",
                 56 : "DVD",
                 57 : "TV",
                 84 : "Setup",
                 88 : "Up",
                 89 : "Down",
                 90 : "Left",
                 91 : "Right",
                 92 : "Ok",
                 120: "A",
                 121: "B",
                 122: "C",
                 123: "D",
                 124: "E",
                 125: "F",
                 130: "Checkmark",
                 142: "ATI",
                 150: "Stopwatch",
                 190: "Help",
                 208: "Hand",
                 213: "Resize",
                 249: "Info",
                 }
        DEVICES = {
            0: "AUX1",
            1: "AUX2",
            2: "AUX3",
            3: "AUX4",
            4: "PC",
        }
        MOUSE = {
            'LeftUp'   : 'Mouse.LeftUp',
            'LeftDown' : 'Mouse.LeftDown',
            'RightUp'  : 'Mouse.RightUp',
            'RightDown': 'Mouse.RightDown',
            'MoveStart': 'Mouse.MoveStart',
            'MoveStop' : 'Mouse.MoveStop'
        }


class MyTimer:

    def __init__(self, t, callback):
        self.t = t
        self.callback = callback
        self.timer = None

    def Start(self):
        self.Close()
        self.timer = Timer(self.t, self.callback)
        self.timer.start()

    def Close(self):
        try:
            self.timer.close()
        except:
            pass


class AtiRemoteWonder2(eg.PluginBase):

    text = Text

    def __init__(self):
        self.buttoncount = None
        self.mousecounter = None
        self.lastDirection = None
        self.currentdevice = None
        self.currentcode = None
        self.buttoncount = None

    def __start__(self,
                  mousemaxspeed=10,
                  mouseacceleration=1,
                  debugging=False,
                  mousereset=False,
                  mousetimeout=0.25,
                  mouseresolution=1.0,
                  enduring=False,
                  prefix='AtiRemoteWonder2'
                  ):

        if debugging:
            eg.PrintNotice('AtiRemoteWonder2: Debugging Active')

        self.prefix = prefix
        self.info.eventPrefix = prefix
        self.mousemaxspeed = float(mousemaxspeed) / mouseresolution
        self.mouseacceleration = float(mouseacceleration) / mouseresolution
        self.debugging = debugging
        self.mousereset = mousereset
        self.speed = mousemaxspeed
        self.accel = mouseacceleration
        self.enduring = enduring
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback1, 3).AddHardwareId(
            "ATI Remote Wonder II (Mouse)", "USB\\VID_0471&PID_0602&MI_00"
        )
        self.winUsb.Device(self.Callback2, 3).AddHardwareId(
            "ATI Remote Wonder II (Buttons)", "USB\\VID_0471&PID_0602&MI_01"
        )
        self.winUsb.Start()
        self.lastDirection = None
        self.currentDevice = None
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        self.receiveQueue = eg.plugins.Mouse.plugin.thread.receiveQueue

        self.Timer = MyTimer(mousetimeout, self.ResetMouse)

    def __stop__(self):
        self.Timer.Close()
        self.winUsb.Stop()
        self.timer.Stop()

    def Callback1(self, (device, x, y)):
        self.mousecounter += 1
        logging = (hex(device), hex(x), hex(y))

        if x > 127:
            x -= 256
        if y > 127:
            y -= 256

        degree = (round((atan2(x, -y) / pi) * 180)) % 360
        payload = dict(x=x, y=y, angle=degree)

        if self.mousecounter == 3:
            self.mousecounter = 0

            if payload != self.lastDirection:
                MOUSE = self.text.EVENTS.MOUSE
                if self.lastdirection is not None:
                    self.EndLastEvent()
                    pay = dict(olddirection=self.lastDirection,
                               newdirection=payload
                               )
                    self.TriggerEvent(suffix=MOUSE['MoveChange'], payload=copy(pay))

                self.TriggerEnduringEvent(suffix=MOUSE['MoveStart'], payload=copy(payload))

                if self.mousereset:
                    self.speed = self.mousemaxspeed
                    self.accel = self.mouseacceleration

                self.lastDirection = copy(payload)

            self.receiveQueue.put((degree, 3, self.speed, self.accel, 0))
            if self.speed < 60:
                self.speed += 0.25
            if self.accel < 30:
                self.accel += 0.10

        if self.debugging:
            res = ('hex values: ' + str(logging)[1:-1],
                   'direction: ' + str(payload)[1:-1],
                   'mouse code count: ' + str(self.mousecounter),
                   'speed: ' + str(self.speed),
                   'accel: ' + str(self.accel)
                   )
            for item in res:
                print('\t\t' + item)

        self.Timer.Start()
        self.timer.Reset(100)

    def Callback2(self, (device, event, code)):
        EVENTS = self.text.EVENTS
        TriggerEvent = self.TriggerEnduringEvent
        suffix = ''
        self.buttoncount += 1

        if code != self.currentcode or device != self.currentdevice:
            self.currentdevice = device
            self.currentcode = code
            self.buttoncount = 0

        if device in EVENTS.DEVICES:
            suffix += EVENTS.DEVICES[device]
        if code in EVENTS.CODES:
            suffix += '.' + EVENTS.CODES[code]

        if event == 1:
            if code == 169:
                suffix = EVENTS.MOUSE['LeftDown']
                mouse_event(0x0002, 0, 0, 0, 0)
            elif code == 170:
                suffix = EVENTS.MOUSE['RightDown']
                mouse_event(0x0008, 0, 0, 0, 0)
            elif code == 63 or len(suffix.split('.')) != 2:
                TriggerEvent = None
            elif not self.enduring:
                TriggerEvent = self.TriggerEvent
        elif event == 0:
            TriggerEvent = self.TriggerEvent
            if code == 169:
                suffix = EVENTS.MOUSE['LeftUp']
                self.EndLastEvent()
                mouse_event(0x0004, 0, 0, 0, 0)
            elif code == 170:
                suffix = EVENTS.MOUSE['RightUp']
                self.EndLastEvent()
                mouse_event(0x0010, 0, 0, 0, 0)
            else:
                TriggerEvent = None
                if self.enduring:
                    self.EndLastEvent()

        if TriggerEvent is not None:
            TriggerEvent(suffix=suffix, payload=suffix.split('.'))

        if self.debugging:
            res = ('hex values: ' + str((hex(device), hex(event), hex(code)))[1:-1],
                   'button code count: ' + str(self.buttoncount),
                   'event: ' + '.'.join([self.prefix] + payload),
                   'payload: ' + str(payload)
                   )
            for item in res:
                print('\t\t' + item)

    @eg.LogIt
    def OnTimeOut(self):
        self.receiveQueue.put((-2,))
        self.EndLastEvent()
        self.TriggerEvent(self.text.EVENTS.MOUSE['MoveStop'], payload=copy(self.lastDirection))
        self.lastDirection = None

    def ResetMouse(self):
        self.speed = self.mousemaxspeed
        self.accel = self.mouseacceleration
        self.mousecounter = 0

    def Configure(self,
                  mousemaxspeed=10,
                  mouseacceleration=1,
                  debugging=False,
                  mousereset=True,
                  mousetimeout=0.25,
                  mouseresolution=1.0,
                  enduring=False,
                  prefix='AtiRemoteWonder2'
                  ):
        text = self.text
        panel = eg.ConfigPanel()

        prefixCtrl = panel.TextCtrl(prefix)
        enduringCtrl = panel.CheckBox(enduring)
        resetCtrl = panel.CheckBox(mousereset)
        timerCtrl = panel.SpinNumCtrl(mousetimeout, min=0.0, max=120.0, increment=0.1)
        speedCtrl = panel.SpinIntCtrl(mousemaxspeed)
        accelCtrl = panel.SpinIntCtrl(mouseacceleration)
        resolCtrl = panel.SpinNumCtrl(float(mouseresolution), min=1.0, max=5.0, increment=0.25)
        debugCtrl = panel.CheckBox(debugging)

        box1 = panel.BoxedGroup(text.EventBox,
                                (text.PrefixLbl, prefixCtrl),
                                (text.EnduringLbl, enduringCtrl)
                                )
        box2 = panel.BoxedGroup(text.MouseBox,
                                (text.MouseSpeedLbl, speedCtrl),
                                (text.MouseAccelLbl, accelCtrl),
                                '',
                                text.MouseResetDesc,
                                (text.MouseResetLbl, resetCtrl),
                                '',
                                text.MouseTimeoutDesc,
                                (text.MouseTimeoutLbl, timerCtrl, text.MouseTimeoutSuf),
                                '',
                                text.MouseResDesc,
                                (text.MouseResLbl, resolCtrl)
                                )
        box3 = panel.BoxedGroup(text.DebuggingBox,
                                (text.DebuggingLbl, debugCtrl)
                                )

        texts = box1.GetColumnItems(0)
        texts += box2.GetColumnItems(0)
        texts += box3.GetColumnItems(0)
        widgets = box1.GetColumnItems(1)
        widgets += box2.GetColumnItems(1)
        widgets += box3.GetColumnItems(1)
        
        eg.EqualizeWidths(tuple(texts))
        eg.EqualizeWidths(tuple(widgets))

        panel.sizer.AddMany([(box1, 0, wx.EXPAND),
                             (box2, 0, wx.EXPAND),
                             (box3, 0, wx.EXPAND),
                             ])

        while panel.Affirmed():
            panel.SetResult(speedCtrl.GetValue(),
                            accelCtrl.GetValue(),
                            debugCtrl.GetValue(),
                            resetCtrl.GetValue(),
                            timerCtrl.GetValue(),
                            resolCtrl.GetValue(),
                            enduringCtrl.GetValue(),
                            prefixCtrl.GetValue()
                            )
