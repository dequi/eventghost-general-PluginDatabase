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
Plugin for the PHX01RN USB Remote
"""

import eg

eg.RegisterPlugin(
    name="PHX01RN",
    description=__doc__,
    author="Bitmonster",
    version="1.0.0",
    kind="remote",
    guid="{0B5511F9-6E8D-447D-9BD7-340E2C3548DD}",
    hardwareId = "USB\\VID_0755&PID_2626",
)

REMOTE_BUTTONS = {
    (4, 0, 61, 0): ("Close", 0),
    (1, 0, 8, 0): ("Video", 0),
    (3, 0, 23, 0): ("TV", 0),
    (1, 0, 4, 0): ("Radio", 0),
    (1, 0, 12, 0): ("Pictures", 0),
    (1, 0, 16, 0): ("Music", 0),
    (3, 0, 16, 0): ("DvdMenu", 0),
    (0, 0, 30, 0): ("Num1", 0),
    (0, 0, 31, 0): ("Num2", 0),
    (0, 0, 32, 0): ("Num3", 0),
    (0, 0, 33, 0): ("Num4", 0),
    (0, 0, 34, 0): ("Num5", 0),
    (0, 0, 35, 0): ("Num6", 0),
    (0, 0, 36, 0): ("Num7", 0),
    (0, 0, 37, 0): ("Num8", 0),
    (0, 0, 38, 0): ("Num9", 0),
    (0, 0, 39, 0): ("Num0", 0),
    (2, 0, 37, 0): ("Star", 0),
    (2, 0, 32, 0): ("Dash", 0),
    (0, 0, 41, 0): ("Clear", 0),
    (4, 0, 40, 0): ("Fullscreen", 0),
    (1, 0, 21, 0): ("Record", 0),
    (12, 0, 40, 0): ("Menu", 0),
    (8, 0, 7, 0): ("Desktop", 0),
    (0, 0, 75, 0): ("ChannelUp", 0),
    (0, 0, 78, 0): ("ChannelDown", 0),
    (0, 0, 40, 0): ("Ok", 0),
    (0, 0, 79, 0): ("Right", 1),
    (0, 0, 80, 0): ("Left", 1),
    (0, 0, 81, 0): ("Down", 1),
    (0, 0, 82, 0): ("Up", 1),
    (0, 0, 42, 0): ("Back", 0),
    (0, 0, 101, 0): ("More", 0),
    (3, 129, 0, 0): ("Power", 0),
    (2, 35, 2, 0): ("WWW", 0),
    (2, 36, 2, 0): ("Previous", 0),
    (2, 37, 2, 0): ("Next", 0),
    (2, 138, 1, 0): ("E-Mail", 0),
    (2, 179, 0, 0): ("Forward", 0),
    (3, 0, 5, 0): ("Rewind", 0),
    (2, 181, 0, 0): ("NextTrack", 0),
    (2, 182, 0, 0): ("PreviousTrack", 0),
    (2, 183, 0, 0): ("Stop", 0),
    (2, 205, 0, 0): ("Play", 0),
    (2, 226, 0, 0): ("Mute", 0),
    (2, 233, 0, 0): ("VolumeUp", 1),
    (2, 234, 0, 0): ("VolumeDown", 1),
    (1, 1, 0, 0): ("MouseLeftButton", 0),
    (1, 2, 0, 0): ("MouseRightButton", 0),
}

REMOTE_MOUSE = {
    (1, 0, 0, 254): ("MouseUp", 0),
    (1, 0, 0, 252): ("MouseUp", 0),
    (1, 0, 0, 248): ("MouseUp", 0),
    (1, 0, 0, 2): ("MouseDown", 0),
    (1, 0, 0, 4): ("MouseDown", 0),
    (1, 0, 0, 8): ("MouseDown", 0),
    (1, 0, 2, 0): ("MouseRight", 0),
    (1, 0, 4, 0): ("MouseRight", 0),
    (1, 0, 8, 0): ("MouseRight", 0),
    (1, 0, 254, 0): ("MouseLeft", 0),
    (1, 0, 252, 0): ("MouseLeft", 0),
    (1, 0, 248, 0): ("MouseLeft", 0),
}

STOP_CODES = set([
    (1, 0, 0, 0),
    (2, 0, 0, 0),
])

class PHX01RN(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 4).AddHardwareId(
            "PHX01RN USB Receiver (keyboard)", "USB\\VID_0755&PID_2626&MI_00"
        )
        self.winUsb.Device(self.Callback, 4).AddHardwareId(
            "PHX01RN USB Receiver (mouse)", "USB\\VID_0755&PID_2626&MI_01"
        )
        self.winUsb.Start()
        self.lastMouse = None

    def __stop__(self):
        self.winUsb.Stop()

    def Callback(self, data):
#        print data
        if (data in REMOTE_BUTTONS) and (not self.lastMouse):
            suffix, bType = REMOTE_BUTTONS[data]
            self.TriggerEnduringEvent(suffix)
        elif data in REMOTE_MOUSE:
            suffix, bType = REMOTE_MOUSE[data]
            if suffix != self.lastMouse:
                self.TriggerEnduringEvent(suffix)
                self.lastMouse = suffix
        elif data in STOP_CODES:
#            print "EndLastEvent"
            self.lastMouse = None
            self.EndLastEvent()

