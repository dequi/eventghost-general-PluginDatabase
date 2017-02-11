# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

# This plugin is based on Bitmonster's Logitech UltraX plugin. Thank you Bitmonster.

ur"""<rst>
Plugin for the Logitech Cordless Keyboard
(only the media/internet keys).

.. image:: picture.gif
   :align: center
"""

import eg

eg.RegisterPlugin(
    name = "Logitech Cordless Keyboard",
    author = "topix",
    version = "1.0.0",
    kind = "remote",
    guid = "{53853B63-CAD6-40B4-BFA3-DDF28C65EB98}",
    description = __doc__,
	hardwareId = "USB\VID_046D&PID_C505",
)

BUTTON_CODES2 = {
    0: "ButtonReleased",
    1: "unknown",
    2: "Previous",
    3: "Next",
    4: "Stop",
    5: "PlayPause",
    6: "VolumeDown",
    7: "VolumeUp",
    8: "Mute",
    9: "unknown",
    10: "eMail",
    11: "Search",
    12: "Homepage",
    13: "Favorites",
    14: "unknown",
    15: "Media",
    16: "Shopping",
    17: "iTouch",
    18: "Financial",
    19: "PrivateSites",
	20: "Social",
	21: "WheelPressed",
	22: "Go",
	23: "GoBack",
}
BUTTON_CODES3 = {
    0: "PowerReleased",
    1: "PowerPressed",
}
# BUTTON_CODES4 = {
    # 1: "WheelUp",       # 1 - ??? (127?) depending on how fast the wheel is scrolled
    # 255: "WheelDown",   # 255 - ??? (128?) depending on how fast the wheel is scrolled
# }

class CordlessKeyboard(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "Logitech HID Keyboard",
            "USB\\VID_046D&PID_C505&MI_01",
            "{745a17a0-74d3-11d0-b6fe-00a0c90f57da}",
            self.ButtonsCallback,
            4,
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def ButtonsCallback(self, data):
        # print "button", data
        if data[0] == 2:
		    if data[1] > 0: self.TriggerEvent(BUTTON_CODES2[data[1]])
            # if data[1] == 0:
                # self.EndLastEvent()
            # else:
                # self.TriggerEnduringEvent(BUTTON_CODES2[data[1]])
        elif data[0] == 3:
            self.TriggerEvent(BUTTON_CODES3[data[1]])
        else:
            self.TriggerEvent("Wheel", payload=data[1])
