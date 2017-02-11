version="0.0.1"
# Plugins/NetworkWatcher/__init__.py
#
# Copyright (C)  2013 Pako  (lubos.ruckl@quick.cz)
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2010-10-03 08:51 GMT+1
#     - support url updated
# 0.0.0 by Pako 2010-10-02 18:23 GMT+1
#     - initial version

eg.RegisterPlugin(
    name = "Network watcher",
    author = "Pako",
    version = version,
    guid = "{344DE9EF-B649-405D-BC58-C87B248EBD3B}",
    canMultiLoad = False,
    createMacrosOnAdd = True,
    description = (
        "Generates events if an IP address is changed."
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5707",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACRUlEQVQ4y42TwU4TURiF"
        "vzszdICWihUakZYmLOiCBSgmLkxIKvEFcOHCFSb4FD6HLHDlTh9AMcG9XTQmpSEWFyKU"
        "ZArNFGqnmU5n5ndRmLSgiWd577nfPffPuYr/lIg0gVvXlkMDIAxDabVaNBoNRGTIoZRi"
        "enoaEUEpdYNrANRqNba3tzk6PeqbBnwSCrl0js1Xm2QymeuAwADY29vDHrVpvm5ybB4P"
        "OXJujsbbBuVymdnZ2RspDADHcXBnXXbv7dLROpds4AgO24esssr+/j5zc3MoFCOxEXK5"
        "HKZp9gEIKE2hrrILGB8Nkp+STLVHcWoWRfMLh5UKCPhmjPsPVth4udEHKE3hdb3osHIV"
        "E5UJnvdGePHD4a51gqk3iJ+cILpObWmJdwdVzs7O+oCZmRnCUsjih0Vi8RhhN6Rz4PCo"
        "Wufx1wvgYujd2tgY2spDfN/vA5aXl1k7WCNbzuJ5HkEQUDmucLvZBawbnVBhODzEUqnE"
        "zucdbNuONizLou04BAN9uJq/P9AJA+C0fkr1e5VerxeZRYT3bpdviQSappHJZEin04gI"
        "NRHM5ATxeLwPWMgvsP5sHcdxogS+72NZFj9dF03T+D01xa/xcQCSySRPCwUmJycxRMQL"
        "goD5+fmoxp7nsfVmi2KxSBAEKBT1ej2KHR+P07pokc/nMQBD13USiUR0e6fTwbZtzpvn"
        "f/1YbbONruu4rntZpGuKxWIUnhRI3UkRDkx8UNlsllQqhRIRF9Avyxup1+sRBME/v7em"
        "aRiG4f0BGA744LHgjnkAAAAASUVORK5CYII="
    ),  
)

from socket import gethostbyname_ex, gethostname
#===============================================================================
def GetAdresses():
    return [ia for ia in gethostbyname_ex(gethostname())[2] \
        if not (ia.startswith("127.") or ia.startswith("169."))]

#===============================================================================
class Text:
    label_1 = "Event prefix:"
    label_2 = "Polling period (s):"
    prefix = "Network"
    removed = "Removed"
    added = "Added"
    disconnected = "Disconnected"
    connected = "Connected"
#===============================================================================

class NetworkWatcher(eg.PluginBase):
    text = Text
    task = None
    oldAddrs = None


    def __init__(self):
        self.AddAction(GetConnected)
        self.AddAction(GetAddresses)


    def __start__(self, prefix = "", period = 0.5):
        self.info.eventPrefix = prefix if prefix != "" else self.text.prefix
        self.period = period
        self.task = eg.scheduler.AddTask(0.01, self.NetWatcher)


    def __stop__(self):
        if self.task:
            eg.scheduler.CancelTask(self.task)
        self.task = None
        self.oldAddrs = None


    def NetWatcher(self):
        self.task = 0
        newAddrs = GetAdresses()
        newA = set(newAddrs)
        oldA = set(self.oldAddrs) if self.oldAddrs is not None else set([])
        for ip in oldA.difference(newA):
            self.TriggerEvent(self.text.removed, payload = ip)
        for ip in newA.difference(oldA):
            self.TriggerEvent(self.text.added, payload = ip)
        if not newAddrs and (self.oldAddrs is None or self.oldAddrs):
            self.TriggerEvent(self.text.disconnected)
        elif not self.oldAddrs and newAddrs:
            self.TriggerEvent(self.text.connected)
        self.oldAddrs = newAddrs
        if self.task is not None:
            self.task = eg.scheduler.AddTask(self.period, self.NetWatcher)


    def Configure(self, prefix = "", period = 0.5):
        prefix = prefix if prefix != "" else self.text.prefix
        panel = eg.ConfigPanel()
        label_1 = wx.StaticText(panel, -1, self.text.label_1)
        label_2 = wx.StaticText(panel, -1, self.text.label_2)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        periodCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        Sizer = wx.GridBagSizer(10, 10)
        Sizer.Add(label_1, (0, 0), flag = wx.TOP, border = 3)
        Sizer.Add(prefixCtrl, (0, 1))
        Sizer.Add(label_2, (1, 0), flag = wx.TOP, border = 3)
        Sizer.Add(periodCtrl, (1, 1))
        panel.sizer.Add(Sizer, 1, wx.EXPAND | wx.ALL,10)


        while panel.Affirmed():
            panel.SetResult(
                prefixCtrl.GetValue(),
                periodCtrl.GetValue()
            )
#===============================================================================

class GetConnected(eg.ActionBase):
    name = "Get connected status"
    description = "Returns connected status."

    def __call__(self):
        return self.plugin.oldAddrs != []
#===============================================================================

class GetAddresses(eg.ActionBase):
    name = "Get addresses"
    description = "Returns list of all valid IP addresses."

    def __call__(self):
        return self.plugin.oldAddrs
#===============================================================================
