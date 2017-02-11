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
#
#
# Large portions of this plugin were adapted from the maX10 software
# written by Colin Bonstead (http://max10.sourceforge.net)
#
#
# $LastChangedDate: 2011-06-07 01:05:06 -0500 (Mon, 07 Jun 2011) $
# $LastChangedBy: Catscradler $


import eg

eg.RegisterPlugin(
    name="X10 MouseRemote",
    author="Catscradler, last modified by K",
    version="1.1b",
    kind="remote",
    canMultiLoad=True,
    description='Hardware plugin for the X10 MouseRemote\n\n'
                'Before enabling this plugin go to the '
                'Windows Device Manager and disable the '
                'Microsoft Serial Mouse.\n\n'
                '<a href="http://kbase.x10.com/wiki/JR20A">'
                'JR20A/MK19A</a>, '
                'connected via the serial port '
                '<a href="http://kbase.x10.com/wiki/JR21A">'
                'JR21A</a> receiver.'
                '\n\n<p>'
                '<img src="mouseremote.png" alt="X10 MouseRemote" />',
    icon="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
         "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
         "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
         "YII="
)

import eg.WinApi.serial
import threading
import win32event
import win32file

KEYTABLE = {
            43: "PC",
            -85: "CD",
            -117: "Web",
            -53: "DVD",
            75: "Phone",
            15: "Power",
            2: "ChPlus",
            3: "ChMinus",
            6: "VolPlus",
            7: "VolMinus",
            5: "Mute",
            13: "Play",
            14: "Stop",
            28: "RW",
            29: "FF",
            78: "Pause",
            64: "Pad0",
            65: "Pad1",
            66: "Pad2",
            67: "Pad3",
            68: "Pad4",
            69: "Pad5",
            70: "Pad6",
            71: "Pad7",
            72: "Pad8",
            73: "Pad9",
            74: "Enter",
            93: "AB",
            92: "Disp",
            -1: "Rec",
            79: "Last",
            -109: "Select",
            109: "Guide",
            107: "Shift"
            }


class SerialThread(threading.Thread):

    def __init__(self, prefix, timeout, triggerevent, serial, stopevent):

        serial.timeout = timeout
        serial.setRTS()

        self.prefix = prefix
        self.TriggerEvent = triggerevent
        self.serial = serial
        self.stopevent = stopevent

        super(SerialThread, self).__init__()
        self.EVENT = threading.Event()
        self.comBytes = []

    def run(self):
        continueloop = True
        n = 1
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
                if n and not self.EVENT.isSet(): self.plugin.Decode(ord(buf[0]))
                waitingOnRead = False

            elif rc == win32event.WAIT_OBJECT_0+1: continueloop = False
            elif rc == win32event.WAIT_TIMEOUT: pass
            else: pass

        self.serial.close()

    def Decode(self, data):
        res = None
        comBytes = self.comBytes
        if (data & 64): self.comBytes = []
        self.comBytes += [data]

        if len(self.comBytes) == 3:
            numlist = [0, 1, 2, 4, 8, 16]
            comBytes = self.comBytes
            x = ((comBytes[0] & 3) << 6) + comBytes[1]
            y = ((comBytes[0] & 12) << 4) + comBytes[2]
            if (x >= 128): x -= 256
            if (y >= 128): y -= 256

            if not comBytes[1] and not comBytes[2]:
                if comBytes[0] & 32: res = dict(suffix='MouseButtonLeft')
                elif comBytes[0] & 16: res = dict(suffix='MouseButtonRight')
                else: res = dict(suffix='MouseButtonRelease')

            elif y == 127:
                try: res = dict(suffix=KEYTABLE[x])
                except: pass

            elif abs(x) in numlist and abs(y) in numlist:
                res = dict(suffix='MouseMove', payload=dict(y=y, x=x))

            try: return self.TriggerEvent(prefix=self.prefix, **res)
            except: pass
            try: return self.TriggerEvent(**res)
            except: pass

class X10Mouse(eg.RawReceiverPlugin):

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)

    def __start__(self, port, timeout, prefix='X10-Mouse', enduringevent=False):
        try:            
            self.Serial = SerialThread(
                            prefix,
                            timeout,
                            self.TriggerEvent if enduringevent else eg.TriggerEvent,
                            eg.WinApi.serial.Serial(port, baudrate=1200, bytesize=7, stopbits=1, parity='N'),
                            win32event.CreateEvent(None, 1, 0, None)
                            )
        except:
            self.Serial = None
            print self.Exceptions.SerialOpenFailed
        else:
            self.Serial.start()

        self.info.eventPrefix = prefix

    def __stop__(self):
        if self.Serial:
            self.Serial.EVENT.set()
            self.Serial.join(1.0)
        self.Serial = None

    def __close__(self):
        if self.Serial:
            self.Serial.EVENT.set()
            self.Serial.join(1.0)

    def Configure(self, port=0, timeout=0.145, prefix='X10-Mouse', enduringevent=False):
        panel = eg.ConfigPanel()
        prefixCtrl = panel.TextCtrl(prefix)
        portCtrl = panel.SerialPortChoice(port)
        timeoutCtrl = panel.SpinNumCtrl(timeout, min=.001, max=1.000, increment=0.001)
        enduringCtrl = panel.CheckBox(enduringevent)
        panel.AddLine('Event Prefix:', prefixCtrl)
        panel.AddLine('COM Port:', portCtrl)        
        panel.AddLine(
                    'Command repeat timeout (measurement is in seconds so 0.100\n'
                    'is one tenth of a second. adjust upward if you are getting\n'
                    'unwanted double button presses)'
                    )
        panel.AddLine('Timeout:', timeoutCtrl, '(default=145)')
        panel.AddLine(
                    'This option when checked will only produce one event for\n'
                    'multiple presses of the same button. This is called an\n'
                    'Enduring Event. When unchecked an event for each button\n'
                    'press will be generated.'
                    )

        panel.AddLine('Enduring Event:', enduringCtrl)

        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                timeoutCtrl.GetValue(),
                prefixCtrl.GetValue(),
                enduringCtrl.GetValue()
            )