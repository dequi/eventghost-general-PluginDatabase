# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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

ur"""<rst>
Plugin for the **Deal Extreme USB PC Remote 2**.

|

.. image:: DXusbPCR.jpg
   :align: center

You can choose, whether *Numlock* is ignored or not.
If ignored, numpad-keys will always send digits,
regardless of the state of *Numlock*.

**Notice:** You need a special driver to use the remote with this plugin.
Please `download it here`__ and install it while the device is connected.

__ http://www.eventghost.org/downloads/USB-Remote-Driver.exe
"""

import eg
from threading import Timer


eg.RegisterPlugin(
    name = "Deal Extreme USB PC Remote 2",
    author = "Bitmonster & Pako & Cichmen",
    version = "1.0.2",
    kind = "remote",
    description = __doc__,
)

CODES = {
    263425:((263425,1967364,3802373,1,4,5,),(1,4,5), "Hotkey_A", "Hotkey_A"),
    328961:((328961,2032900,3867909,1,4,5,),(1,4,5), "Hotkey_B", "Hotkey_B"),
    394497:((394497,2098436,3933445,1,4,5,),(1,4,5), "Hotkey_C", "Hotkey_C"),
    460033:((460033,2163972,3998981,1,4,5,),(1,4,5), "Hotkey_D", "Hotkey_D"),
    33030:((33030,),(6,), "Power", "Power"),
    100867:((100867,3,),(3,), "E-mail", "E-mail"),
    140035:((140035,3,),(3,), "WWW", "WWW"),
    3998721:((3998721,1,),(1,), "Close", "Close"),
    8194:((8194,),(2,), "MouseLeft", "MouseLeft"),
    16386:((16386,),(2,), "MouseRight", "MouseRight"),
    46595:((46595,3,),(3,), "|<", "|<"),
    52483:((52483,3,),(3,), "Play/Pause", "Play/Pause"),
    46339:((46339,3,),(3,), ">|", ">|"),
    51971:((51971,5242881,5243140,328453,),(3,1,4,5,), "<<", "<<"),
    46851:((46851,3,),(3,), "Stop", "Stop"),
    51715:((51715,5177345,5177604,590597,),(3,1,4,5,), ">>", ">>"),
    59651:((59651,),(3,), "Volume+", "Volume+"),
    59907:((59907,),(3,), "Volume-", "Volume-"),
    143363:((143363,2622465,2097412,3,1,4,),(3,1,4,), "Full Screen", "Full Screen"),
    4915201:((4915201,),(1,), "Page+", "Page+"),
    5111809:((5111809,),(1,), "Page-", "Page-"),
    57859:((57859,3,),(3,), "Mute", "Mute"),
    526337:((526337,1,),(1,), "MyPC", "MyPC"),
    2752513:((2752513,),(1,), "Backspace", "Backspace"),
    1966081:((1966081,),(1,), "Num1", "Num1"),
    2031617:((2031617,),(1,), "Num2", "Num2"),
    2097153:((2097153,),(1,), "Num3", "Num3"),
    2162689:((2162689,),(1,), "Num4", "Num4"),
    2228225:((2228225,),(1,), "Num5", "Num5"),
    2293761:((2293761,),(1,), "Num6", "Num6"),
    2359297:((2359297,),(1,), "Num7", "Num7"),
    2424833:((2424833,),(1,), "Num8", "Num8"),
    2490369:((2490369,),(1,), "Num9", "Num9"),
    2555905:((2555905,),(1,), "Num0", "Num0"),
    2818049:((2818049,),(1,), "Tab", "Num1"),
    5373953:((5373953,),(1,), "Up_arrow", "Num2"),
    2049:((2049,1,),(1,), "Start", "Num3"),
    5242881:((5242881,),(1,), "Left_arrow", "Num4"),
    2621441:((2621441,),(1,), "Enter", "Num5"),
    5177345:((5177345,),(1,), "Right_arrow", "Num6"),
    1179905:((1179905,),(1,), "Open", "Num7"),
    5308417:((5308417,),(1,), "Down_arrow", "Num8"),
    2686977:((2686977,),(1,), "Escape", "Num9"),
    2819073:((2819073,1,),(1,), "SwitchWindows", "Num0"),
    460801:((460801,1,),(1,), "Desktop", "Desktop")
}


class Text:
    ignoreNumlock = "Ignore button Numlock"
    tooltip = """If this option is checked,
events from the Numpad-buttons of remote control
are always sent as a digits
(regardless of the state of Num Lock)."""

class DXusbPCR(eg.PluginBase):
    text = Text

    @eg.LogIt
    def __start__(self, ignoreNumLock):
        self.ignoreNumLock = ignoreNumLock
        self.timeout = 0.1
        self.timer = Timer(self.timeout, self.OnTimeout)
        self.status = 0
        self.keyData = ()
        self.codesIx = 0
        self.usb = eg.WinUsbRemote(
            "{745a17a0-74d3-11d0-b6fe-00a0c90f57da}",
            self.Callback,
            4,
            False,
         )
        if not self.usb.IsOk():
            raise self.Exceptions.DeviceNotFound

    def __stop__(self):
        self.usb.Close()

    def OnTimeout(self):
        self.EndLastEvent()
        self.status = 0
        self.codesIx = 0

#Status variable definition:
#---------------------------
#Status 0 = idle
#Status 1 = receive key-down code
#Status 2 = (waiting for or) receive key-up code
#Status 3 = mousepad Up
#Status 4 = mousepad Down

    def Callback(self, data):
        self.timer.cancel()
        #print data[3], data[2], data[1], data[0]

        if tuple(data[:2]) <> (2,0): #standard buttons (no mousepad)
            value = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
            if self.status == 0:
                if value in CODES:
                    self.keyData = CODES[value]
                    self.status = 1
                else: #flush
                    return
            if self.status == 1:
                if value == self.keyData[0][self.codesIx]:
                    self.codesIx += 1
                    if self.codesIx == len(self.keyData[0]):
                        keyName = self.keyData[3] if self.ignoreNumLock else self.keyData[2]
                        self.TriggerEnduringEvent(keyName)
                        self.status = 2
                        self.codesIx = 0
                else: #flush
                    self.status = 0
                    self.codesIx = 0
            else: #if self.status == 2
                try:
                    if value == self.keyData[1][self.codesIx]:
                        self.codesIx += 1
                        if self.codesIx == len(self.keyData[1]):
                            self.EndLastEvent()
                            self.status = 0
                            self.codesIx = 0
                    else: #flush
                        self.status = 0
                        self.codesIx = 0
                except:
                    self.EndLastEvent()
                    if value in CODES:
                        self.keyData = CODES[value]
                        #self.status = 1
                        if value == self.keyData[0][self.codesIx]:
                            self.codesIx += 1
                            if self.codesIx == len(self.keyData[0]):
                                keyName = self.keyData[3] if self.ignoreNumLock else self.keyData[2]
                                self.TriggerEnduringEvent(keyName)
                                self.status = 2
                                self.codesIx = 0
                        else: #flush
                            self.status = 0
                            self.codesIx = 0
                    else:
                        self.status = 0
                        self.codesIx = 0
        else: #mousepad Up/Down
            if self.status == 0:
                if 15 & data[3]:
                    if 240 & data[3]:
                        self.status = 3 #Up
                        self.TriggerEnduringEvent("MouseUp")
                    else:
                        self.status = 4 #Down
                        self.TriggerEnduringEvent("MouseDown")
                    self.timer = Timer(self.timeout, self.OnTimeout)
                    self.timer.start()

            elif self.status == 3: #mousepad Up
                if tuple(data[:2]) == (2,0) and (15 & data[3]) and (240 & data[3]):
                    self.timer = Timer(self.timeout, self.OnTimeout)
                    self.timer.start()
                else:
                    self.EndLastEvent()
                    self.status = 0
                    self.codesIx = 0

            elif self.status == 4:  #mousepad Down
                if tuple(data[:2]) == (2,0) and (240 ^ data[3]) > 240: #bits 4-7 = 0000
                    self.timer = Timer(self.timeout, self.OnTimeout)
                    self.timer.start()
                else:
                    self.EndLastEvent()
                    self.status = 0
                    self.codesIx = 0

            else: #maybe self.status == 2 for MouseLeft or MouseRight buttons
                self.EndLastEvent()
                self.status = 0
                self.codesIx = 0

    def Configure(self, ignoreNumLock=False):
        panel = eg.ConfigPanel()
        ignoreNumLock = panel.CheckBox(ignoreNumLock, self.text.ignoreNumlock)
        toolTip = wx.ToolTip(self.text.tooltip)
        ignoreNumLock.SetToolTip(toolTip)
        #toolTip.SetDelay(10000)

        panel.AddLine(ignoreNumLock)

        while panel.Affirmed():
            panel.SetResult(
                ignoreNumLock.GetValue(),
            )
