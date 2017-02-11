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

ur"""<rst>
Plugin for the `Emprex USB MCE Remote Control for Windows\u00ae Media Center`__.

|

.. image:: picture.jpg
   :align: center

__ http://www.emprex.com/02_products_02.php?id=303
"""

import eg

eg.RegisterPlugin(
    name = "Emprex MCE USB",
    author = "doveman",
    version = "1.0.0",
    kind = "remote",
    guid = "{745a17a0-74d3-11d0-b6fe-00a0c90f57da}",
    description = __doc__,
    hardwareId = "USB\\VID_046E&PID_5577",
)


BUTTON_CODES = {
	(2, 178, 0, 0, 0, 0, 0): 'Record',
	(2, 177, 0, 0, 0, 0, 0): 'Pause',
	(2, 183, 0, 0, 0, 0, 0): 'Stop',
	(2, 180, 0, 0, 0, 0, 0): 'Rewind',
	(2, 176, 0, 0, 0, 0, 0): 'Play',
	(2, 179, 0, 0, 0, 0, 0): 'FFwd',
	(2, 182, 0, 0, 0, 0, 0): 'Skip <',
	(2, 181, 0, 0, 0, 0, 0): 'Skip >',
	(2,  36, 2, 0, 0, 0, 0): 'Back',
	(2,   9, 2, 0, 0, 0, 0): 'Info',
	(2, 233, 0, 0, 0, 0, 0): 'Vol+',
	(2, 234, 0, 0, 0, 0, 0): 'Vol-',
	(2, 226, 0, 0, 0, 0, 0): 'Mute',
	(2, 156, 0, 0, 0, 0, 0): 'Ch +',
	(2, 157, 0, 0, 0, 0, 0): 'Ch -',
	(2, 141, 0, 0, 0, 0, 0): 'Guide',
	(3,  13, 0, 0, 0, 0, 0): 'MCE',
	(3,  72, 0, 0, 0, 0, 0): 'Rec TV',
	(3,  37, 0, 0, 0, 0, 0): 'Live TV',
	(3,  36, 0, 0, 0, 0, 0): 'DVD Menu',
	(3,  71, 0, 0, 0, 0, 0): 'Music',
	(3,  73, 0, 0, 0, 0, 0): 'Pics',
	(3,  74, 0, 0, 0, 0, 0): 'Video',
	(3,  80, 0, 0, 0, 0, 0): 'Radio',
	(3,  90, 0, 0, 0, 0, 0): 'Teletext',
	(3,  91, 0, 0, 0, 0, 0): 'Red',
	(3,  92, 0, 0, 0, 0, 0): 'Green',
	(3,  93, 0, 0, 0, 0, 0): 'Yellow',
	(3,  94, 0, 0, 0, 0, 0): 'Blue',
	(1,   2, 0, 0, 0, 0, 0): 'Power',
}

KEYPAD_CODES = {
    (0, 0, 30, 0, 0, 0, 0): "Num1",
    (0, 0, 31, 0, 0, 0, 0): "Num2",
    (0, 0, 32, 0, 0, 0, 0): "Num3",
    (0, 0, 33, 0, 0, 0, 0): "Num4",
    (0, 0, 34, 0, 0, 0, 0): "Num5",
    (0, 0, 35, 0, 0, 0, 0): "Num6",
    (0, 0, 36, 0, 0, 0, 0): "Num7",
    (0, 0, 37, 0, 0, 0, 0): "Num8",
    (0, 0, 38, 0, 0, 0, 0): "Num9",
    (0, 0, 39, 0, 0, 0, 0): "Num0",
    (0, 0, 40, 0, 0, 0, 0): "Ok",
    (0, 0, 41, 0, 0, 0, 0): "Clear",
    (0, 0, 79, 0, 0, 0, 0): "Right",
    (0, 0, 80, 0, 0, 0, 0): "Left",
    (0, 0, 81, 0, 0, 0, 0): "Down",
    (0, 0, 82, 0, 0, 0, 0): "Up",
    (2, 0, 37, 0, 0, 0, 0): "Star",
    (2, 0, 32, 0, 0, 0, 0): "Dash",
}


class Emprex(eg.PluginBase):

    def __start__(self):
        self.buffer = []
        self.expectedLength = 0
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.KeypadCallback, 8, True).AddHardwareId(
            "Emprex MCE USB (Keypad)", "USB\\VID_046E&PID_5577&MI_00"
        )
        self.winUsb.Device(self.ButtonsCallback, 8).AddHardwareId(
            "Emprex MCE USB (Buttons)", "USB\VID_046E&PID_5577&MI_01"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()
           

    def KeypadCallback(self, data):
        data = data[:-1]
        if data == (0, 0, 0, 0, 0, 0, 0):
            self.EndLastEvent()
        else:
            self.TriggerEnduringEvent(KEYPAD_CODES[data])
            
    def ButtonsCallback(self, data):
        data = data[:-1]
        if data == (2, 0, 0, 0, 0, 0, 0) or data == (3, 0, 0, 0, 0, 0, 0) or data == (1, 0, 0, 0, 0, 0, 0):
            self.EndLastEvent()
        else:
            self.TriggerEnduringEvent(BUTTON_CODES[data])            