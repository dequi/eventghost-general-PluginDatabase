# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Used Catscradler's original plugin to inspire this rewrite of the plugin
# it fixes dropped data issues that the original had as well as added all
# kinds of extras to it

import eg

eg.RegisterPlugin(
    name='X10 Remote with Mouse',
    author='K',
    version='0.6b',
    kind='remote',
    guid='{685A50E3-F3C1-4BEB-AACE-FB75053A8A8B}',
    canMultiLoad=True,
    description='plugin for the X10 Remote with Mouse\n\n'
                'Before enabling this plugin go to the '
                'Windows Device Manager disable the '
                'Microsoft Serial Mouse.\n\n'
                'This Plugin enable direct control of the '
                'mouse on a computer with optional event '
                'generation and event type selection.\n\n\n'
                '<a href="http://kbase.x10.com/wiki/JR20A">'
                'JR20A/MK19A</a>, '
                'connected via the serial port '
                '<a href="http://kbase.x10.com/wiki/JR21A">'
                'JR21A</a> receiver.'
                '\n\n<p>'
                '<img src="mouseremote.png" alt="X10 MouseRemote" />'
)

import eg.WinApi.serial
import threading
import win32event
import win32file
from time import sleep
from time import time
from copy import deepcopy as copy
from math import atan2, pi
from eg.WinApi.Dynamic import mouse_event

BUTTONS = {
       '0x44': {
           '0x3': 'Channel.-', 
           '0x2': 'Channel.+', 
           '0x7': 'Volume.-', 
           '0x6': 'Volume.+', 
           '0x5': 'Volume.Mute', 
           '0x2b': 'Input.PC', 
           '0x1d': 'Media.FastForward', 
           '0x1c': 'Media.Rewind', 
           '0xf': 'Power', 
           '0xe': 'Media.Stop', 
           '0xd': 'Media.Play'
       }, 
       '0x45': {
           '0x9': 'Number.9', 
           '0x8': 'Number.8', 
           '0x3': 'Number.3', 
           '0x2': 'Number.2', 
           '0x1': 'Number.1', 
           '0x0': 'Number.0', 
           '0x7': 'Number.7', 
           '0x6': 'Number.6', 
           '0x5': 'Number.5', 
           '0x4': 'Number.4', 
           '0x2d': 'Guide', 
           '0x2b': 'Shift', 
           '0xb': 'Input.Phone', 
           '0xa': 'Enter', 
           '0x1d': 'AB', 
           '0x1c': 'Disp', 
           '0xf': 'Last', 
           '0xe': 'Media.Pause'
       }, 
       '0x46': {
           '0x2b': 'Input.CD', 
           '0xb': 'Input.Web', 
           '0x13': 'Select'
       }, 
       '0x47': {
           '0xb': 'Input.DVD', 
           '0x3f': 'Media.Record'
       }
   }

MOUSEBUTTON = {
            ('0x40', '0x0', '0x0'): None,
            ('0x50', '0x0', '0x0'): 'Mouse.RightButton.Pressed',
            ('0x60', '0x0', '0x0'): 'Mouse.LeftButton.Pressed'
            }

class TriggerEventHandler:

    def __init__(
                self,
                handler,
                logbytes,
                mouseevents,
                prefix,
                triggerevent,
                longtimeout,
                longreset
                ):

        self.handler      = handler
        self.logbytes     = logbytes
        self.mouseevents  = mouseevents
        self.prefix       = prefix
        self.TriggerEvent = triggerevent
        self.longtimeout  = int(round(longtimeout*1000))
        self.longreset    = int(round(longreset*1000))
        self.savedtimeout = self.longtimeout
        self.savedevent   = None
        self.start        = 0
        self.mousebuttoncount = 0

    def MouseButtonEvent(self, suffix):
        if suffix is None:
            if self.mouseevents is True:
                try: self.TriggerEvent(prefix=self.prefix, **self.handler.mousebutton)
                except: self.TriggerEvent(**self.handler.mousebutton)
            yield 'Released'
        else:
            if self.handler.mousebutton is not None:
                if self.mouseevents is True:
                    try: self.TriggerEvent(prefix=self.prefix, **self.handler.mousebutton)
                    except: self.TriggerEvent(**self.handler.mousebutton)
                yield 'Released'
            if self.mouseevents is True:
                try: self.TriggerEvent(prefix=self.prefix, suffix=suffix)
                except: self.TriggerEvent(suffix=suffix)
            yield 'Pressed'

    def __call__(self, **kwargs):
        TriggerEvent = self.TriggerEvent
        longtimeout  = self.longtimeout
        savedevent   = self.savedevent
        start        = self.start
        stop         = int(round(time()*1000))

        if self.logbytes: print 'code spacing: ', stop-start, ' milliseconds'

        if stop-start >= self.longreset: longtimeout = self.savedtimeout
        if kwargs == savedevent:
            if stop-start < longtimeout: TriggerEvent = None
            longtimeout -= 60
        else: longtimeout = self.savedtimeout
        if longtimeout < 0: longtimeout = 0

        self.longtimeout = longtimeout
        self.start = stop
        self.savedevent = copy(kwargs)

        if kwargs['suffix'] is None:
            return (item for item in self.MouseButtonEvent(**kwargs))

        if kwargs['suffix'].find('Mouse') > -1:
            if kwargs['suffix'].find('Button') > -1:
                self.mousebuttoncount += 1
                if self.mousebuttoncount == 1:
                    return (item for item in self.MouseButtonEvent(**kwargs))
                if self.mousebuttoncount == 3:
                    self.mousebuttoncount = 0
                return False
            if self.mouseevents is False:
                if TriggerEvent is None: return False
                else: return True

        try: TriggerEvent(prefix=self.prefix, **kwargs)
        except: pass
        else: return True
        try: return TriggerEvent(**kwargs)
        except: return False
        else: return True

class SerialThread(threading.Thread):

    def __init__(
                self,
                serial,
                stopevent,
                logbytes,
                mousemove,
                mousemaxspeed,
                mouseacceleration,
                mouseevents,
                *args
                ):

        self.serial       = serial
        self.stopevent    = stopevent
        self.logbytes     = logbytes
        self.TriggerEvent = TriggerEventHandler(self, logbytes, mouseevents, *args)
        self.mousemove         = float(mousemove)
        self.mousemaxspeed     = float(mousemaxspeed)
        self.mouseacceleration = float(mouseacceleration)
        self.mouseevents       = mouseevents
        
        self.speed = float(mousemaxspeed)
        self.accel = float(mouseacceleration)

        serial.setRTS()

        super(SerialThread, self).__init__()
        self.EVENT         = threading.Event()
        self.comBytes      = ()
        self.lastDirection = None
        self.timer         = eg.ResettableTimer(self.MouseMoveTimeout)
        self.receiveQueue  = eg.plugins.Mouse.plugin.thread.receiveQueue
        self.mousebutton   = None

    def run(self):
        n = 1
        continueloop  = True
        waitingOnRead = False
        buf = win32file.AllocateReadBuffer(n)

        while continueloop:
            if self.EVENT.isSet():
                win32event.SetEvent(self.stopevent)

            if not waitingOnRead:
                win32event.ResetEvent(self.serial._overlappedRead.hEvent)
                hr, _ = win32file.ReadFile(self.serial.hComPort, buf, self.serial._overlappedRead)
                if hr == 997: waitingOnRead = True
                elif hr == 0: pass
                else: raise

            rc = win32event.MsgWaitForMultipleObjects((self.serial._overlappedRead.hEvent, self.stopevent),
                                                        0, 1000, win32event.QS_ALLINPUT)
            if rc == win32event.WAIT_OBJECT_0:
                n = win32file.GetOverlappedResult(self.serial.hComPort, self.serial._overlappedRead, 1)
                if n and not self.EVENT.isSet():
                    if self.logbytes: print hex(ord(buf[0]))
                    self.Decode(ord(buf[0]))
                waitingOnRead = False

            elif rc == win32event.WAIT_OBJECT_0+1: continueloop = False
            elif rc == win32event.WAIT_TIMEOUT: pass
            else: pass

        self.timer.Stop()
        self.serial.close()

    def MouseMoveTimeout(self):
        self.receiveQueue.put((-2,))
        self.lastDirection = None

    def MouseMoveEvent(self):
        try: return self.TriggerEvent(suffix='Mouse.MovingCursor', payload=copy(self.lastDirection))
        except: return False

    def MouseMoveCommand(self, x, y, angle):
        if self.MouseMoveEvent() and self.mousemove:
            self.receiveQueue.put((
                                angle,
                                3,
                                self.speed,
                                self.accel,
                                0
                                ))
            if self.speed < 60: self.speed += 0.50
            if self.accel < 30: self.accel += 0.25

    def MouseButton(self, suffix):
        res = self.TriggerEvent(suffix=suffix)
        if res is False: return res
        for item in res:
            if item == 'Released':
                if self.mousemove:
                    if self.mousebutton['suffix'].find('Left') > -1:
                        mouse_event(0x0004, 0, 0, 0, 0)
                    else: mouse_event(0x0010, 0, 0, 0, 0)
                self.mousebutton = None

            if item == 'Pressed':
                if self.mousemove:
                    if suffix.find('Left') > -1:
                        mouse_event(0x0002, 0, 0, 0, 0)
                    else: mouse_event(0x0008, 0, 0, 0, 0)
                self.mousebutton = dict(suffix='.'.join(suffix.split('.')[:-1]+['Released']))

    def Decode(self, data):
        if (data & 64): self.comBytes = ()
        self.comBytes += (hex(data),)
        if len(self.comBytes) == 3:
            comBytes = self.comBytes

            if self.logbytes: print 'completed command set: ', comBytes
            
            try: return self.TriggerEvent(suffix='Button.'+BUTTONS[comBytes[0]][comBytes[1]])
            except: pass
            try: return self.MouseButton(MOUSEBUTTON[comBytes])
            except: pass

            mousebytes = ()
            for strhex in comBytes:
                mousebytes += (int(strhex, 16),)

            x = ((mousebytes[0] & 3) << 6) + mousebytes[1]
            y = ((mousebytes[0] & 12) << 4) + mousebytes[2]
            if x >= 128: x -= 256
            if y >= 128: y -= 256
            lastDirection = dict(x=x, y=y, angle=(round((atan2(x, -y) / pi) * 180)) % 360)
            if self.lastDirection != lastDirection \
                            or self.lastDirection is None:
                self.speed = self.mousemaxspeed
                self.accel = self.mouseacceleration
                self.lastDirection = lastDirection
            self.MouseMoveCommand(**lastDirection)
            self.timer.Reset(100)


class X10RemoteMouse(eg.RawReceiverPlugin):

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.savedtriggerevent = self.TriggerEvent

    def __start__(
                self,
                port,
                longpresstimeout,
                prefix='X10-Mouse',
                enduringevent=False,
                logbytes=False,
                longpressreset=0.075,
                mousemove=True,
                mouseevents=True,
                mousemaxspeed=10,
                mouseacceleration=1
                ):

        if enduringevent:
            self.info.eventPrefix = prefix
        else: self.TriggerEvent = eg.TriggerEvent

        try:
            self.Serial = SerialThread(
                            eg.WinApi.serial.Serial(port, baudrate=1200, bytesize=7, stopbits=1, parity='N'),
                            win32event.CreateEvent(None, 1, 0, None),
                            logbytes,
                            mousemove,
                            mousemaxspeed,
                            mouseacceleration,
                            mouseevents,
                            prefix,
                            self.TriggerEvent,
                            longpresstimeout,
                            longpressreset,
                            )

        except Exception as err:
            self.Serial = None
            eg.PrintError(str([err]))
            eg.Print('X-10 Mouse Plugin Has Stopped')
        else:
            eg.Print('X-10 Mouse Plugin Has Started')
            self.Serial.start()

    def __stop__(self):
        eg.Print('X-10 Mouse Plugin Has Stopped')
        self.TriggerEvent = self.savedtriggerevent
        if self.Serial:
            self.Serial.EVENT.set()
            self.Serial.join(1.0)
        self.Serial = None
        sleep(.1)

    def __close__(self):
        if self.Serial:
            self.Serial.EVENT.set()
            self.Serial.join(0.1)

    def Configure(
                self,
                port=0,
                longpresstimeout=0.145,
                prefix='X10-Remote',
                enduringevent=False,
                logbytes=False,
                longpressreset=0.348,
                mousemove=True,
                mouseevents=True,
                mousemaxspeed=1,
                mouseacceleration=1
                ):

        panel           = eg.ConfigPanel()
        prefixCtrl      = panel.TextCtrl(prefix)
        portCtrl        = panel.SerialPortChoice(port)
        longtimerCtrl   = panel.SpinNumCtrl(longpresstimeout, min=.001, max=1.000, increment=0.001, fractionWidth=3)
        longresetCtrl   = panel.SpinNumCtrl(longpressreset, min=.001, max=60.000, increment=0.001, fractionWidth=3)
        enduringCtrl    = panel.CheckBox(enduringevent)
        logbytesCtrl    = panel.CheckBox(logbytes)
        mousemoveCtrl   = panel.CheckBox(mousemove)
        mouseeventsCtrl = panel.CheckBox(mouseevents)
        mousemaxCtrl    = panel.SpinIntCtrl(mousemaxspeed)
        mouseaccCtrl    = panel.SpinIntCtrl(mouseacceleration)

        eventboxsizer = wx.BoxSizer(wx.HORIZONTAL)

        pluginbox = panel.BoxedGroup(
                                    'Plugin Settings',
                                    ('Event Prefix:', prefixCtrl),
                                    ('COM Port:', portCtrl)
                                    )

        eventbox1 = panel.BoxedGroup(
                                    'Timeouts', 
                                    'This is for ignoring repeat codes generated by an\n'
                                    'accidental "Long Press" of the remote button. This\n'
                                    'set time will shrink if the button is held intent-\n'
                                    'ionally. That way no commands are missed, the Reset\n'
                                    'is the amount of time before the Delay is reset back\n'
                                    'to it\'s original set value. So it starts over.',
                                    ('Long Press Delay:', longtimerCtrl),
                                    ('Long Press Reset:', longresetCtrl)
                                    )

        eventbox2 = panel.BoxedGroup(
                                    'EventType', 
                                    'This option when checked will only produce one event\n'
                                    'for multiple presses of the same button. This is\n'
                                    'called an Enduring Event. When unchecked an event for\n'
                                    'each button press will be generated.',
                                    ('Enduring Event:', enduringCtrl)
                                    )

        eventboxsizer.Add(eventbox1, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        eventboxsizer.Add(eventbox2, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)

        eventbox = panel.BoxedGroup(
                                    'Event Settings',
                                    eventboxsizer
                                    )

        mousebox = panel.BoxedGroup(
                                    'Mouse Settings',
                                    ('Move Mouse:', mousemoveCtrl),
                                    ('Mouse Events:', mouseeventsCtrl),
                                    ('Mouse Max Speed:', mousemaxCtrl),
                                    ('Mouse Acceleration:', mouseaccCtrl)
                                    )
        debugbox = panel.BoxedGroup(
                                    'Debug Settings',
                                    ('Show Incoming Hex:', logbytesCtrl)
                                    )

        groupsizer = wx.BoxSizer(wx.HORIZONTAL)

        groupsizer.Add(pluginbox, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        groupsizer.Add(mousebox, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        groupsizer.Add(debugbox, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)


        panel.sizer.AddMany([
                            (groupsizer, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5),
                            (eventbox, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            portCtrl.GetValue(),
                            longtimerCtrl.GetValue(),
                            prefixCtrl.GetValue(),
                            enduringCtrl.GetValue(),
                            logbytesCtrl.GetValue(),
                            longresetCtrl.GetValue(),
                            mousemoveCtrl.GetValue(),
                            mouseeventsCtrl.GetValue(),
                            mousemaxCtrl.GetValue(),
                            mouseaccCtrl.GetValue()
                            )