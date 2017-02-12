version = "0.1.0"
# This file is part of EventGhost.
# Copyright (C) 2008 Pako <lubos.ruckl@quick.cz>
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
#
#



eg.RegisterPlugin(
    name = "Multitap",
    author = "Pako",
    version = version,
    kind = "other",
    createMacrosOnAdd = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUAAAAAAICAgIDA"
        "wMD///8AJXNWVlZiYmJubm56enoAMZY2AJVAAKxXAO5Ic///SEi4/0j/qiWGhoaSkpKe"
        "np6qqqqoub22trbCwsLe//7y8vL///+enp6goKS2traO/6v/q47/1I7AwMD///9ra2tj"
        "a3Ntc3Rzc2tzc3N7c3N7e3N7e3taa4Rre4x7hISEhISMjIyElJyUlJSUnJyclJScnJyE"
        "lKWEnK2EnLWUnKWcnKWcpaWcpa2Upb2Urb2crbWlnJylpZytpZy1pZy1rZy9rZylpaWl"
        "pa2traWlrbWlrb2trbWssbOttbW1raUYPkMYPoIFDb4AAFQS5LgYUQsFDb4AAFQS5LgY"
        "UKcFEOyctcaltcalvc6ttca1vcatxta1xta1zt69zt7GtZzGtaXGta3Gva3GvbXGvb3G"
        "xr3GxsbGxs7Ozs7Gzt7O1tbWzs7W1s7W1tbe1tbe3tbe3t7n597n5+fn7+/v7+/v9//3"
        "7+/39/f///9pQHAAAAEAAAAS4VQS4mwS6mDUOQrWmvj////RRQDRbshpI9AAAA0AAgjR"
        "btgAAABpI9AAAAAAAAEAAAAAAAES4lzRxrAAAADUG/sAAAAAAADRxrACA7YS4hTRxtEA"
        "AAAAAH8AAAES4hgUAAD4RKgAAAgUCAgUAAAWNaAS4fC6q80S5Dj5iPD0OHD////4RKj0"
        "fXD0ijoAADRQLAAAAACdAAC+cjAS4ij0oyMS5HD5iPD0OHD////4RKj0fXD0ijrl4ZcA"
        "AA4AAQTUF90S41zUOQrWm2j////ROzPRWywAAADRxrACA7YAAH8AAAEAAAAAAAAAAAAS"
        "+fAS+fAS4szRX3PRxrACA7YAAH8AAAEAAAAAAAES4uzUIPLRxrACA7YAAH8AAAEAAAAS"
        "+fAS4wj2gksAAADRWCvRU35tA/4AABQBC9EAAAAAAAAYPFoYPEcBEKTUEBjUEBgAAAIY"
        "Ou0YNg8BENrUEBjUEBgAAAIBEKQS46zUER+dksjUR7CdksjUR8ABEKQS46weK/KLAAAE"
        "K0lEQVR42gEgBN/7AL+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/AL8EBAEE"
        "BL8vGBgvBAQvLy+/vxgvBAQBBAQBBAQEBC+/AL8EBAEEBAS/LxgYLy8vL7+/vxgYLwQE"
        "AQQBBAQELy+/AL8BBAQBBAQEvy8YGC8vvwQEvy8YGC8EBAEEBAQvLy+/AL8EAQEBBAQE"
        "BL8vGC+/BAQEBL8vGBgvBAQEBC8vL7+/AL8EAQQEBAQEBL+/L78EBAQEBAS/LxgYLwQE"
        "Ly8vv7+/AL8BAQQEBAQELy+/vwQEBAQEBAQEvy8YGC8vLy+/v7+/AL8EBAQEBAQvLy+/"
        "BAQBAQQEBAQEBL8vGBgvL78EBL+/AL8EBAQEBC8vL78EBAEEBAQEBAQEBAS/LxgvvwQE"
        "BAS/AL8EBAQELy8vvy8EBAEBAQEBBAQEBAS/vy+/BAQEBAS/AL8vBAQvLy+/vxgvBAQE"
        "BAQBBAQEBC8vv78EBAQEBAS/AL8YLy8vL7+/vxgYLwQEAQEYBAQELy8vvwQEBAEEBAS/"
        "AL8YGC8vvwQEvy8YGC8EBAQEBAQvLy+/BAQEBAEEBAS/AL8vGC+/BAQEBL8vGBgvBAQE"
        "BC8vL78vBAQBAQEBAQS/AL+/L78EBAQEBAS/LxgYLwQELy8vv78YLwQEBAEEBAS/AL+/"
        "vwQEAQEYBAQEvy8YGC8vLy+/v78YGC8EBAEEBAS/AL+/BAQBBAQBAQQEBL8vGBgvL78E"
        "BL8vGBgvBAQEBAS/AL8EBAQBBAEEAQQEBAS/LxgvvwQEBAS/LxgYLwQEBAS/AL8EBAQY"
        "AQQEBAQEBAS/vy+/BAQEBAQEvy8YGC8EBC+/AL8vBAQEAQEEBAQEBC8vv78EBAQBBAQE"
        "BL8vGBgvLy+/AL8YLwQEBAQEBAQELy8vvwQEGAEBBAQEBAS/LxgYLy+/AL8YGC8EBAQE"
        "BAQvLy+/BAQEAQQBBAEEBAQEvy8YL7+/AL8vGBgvBAQEBC8vL78vBAQEAQQBBAEEBAQE"
        "v78vvwS/AL+/LxgYLwQELy8vv78YLwQEBAQBARgEBAQvL7+/BBi/AL8Evy8YGC8vLy+/"
        "v78YGC8EBAQBBAQEBC8vL78EGBi/AL8YBL8vGBgvL78EBL8vGBgvBAQEBAQELy8vvwQY"
        "GBi/AL8YGAS/LxgvvwQYGAS/LxgYLwQEBAQvLy+/LwQYGBi/AL8YGBi/vy+/BBgYGBgE"
        "vy8YGC8EBC8vL7+/GC8EGBi/AL8YGC8vv78EGBgYGBgYBL8vGBgvLy8vv7+/GBgvBBi/"
        "AL8YLy8vvwQYGBgYGBgYGAS/LxgYLy+/BAS/LxgYLwS/AL8vLy+/BBgYGBgYGBgYGBgE"
        "vy8YL78EGBgEvy8YGC+/AL+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/0ODx"
        "b7QO4zQAAAAASUVORK5CYII="
    ),
    description = (
        "Adds Multitapper actions."
    ),
)

from threading import Timer

#===============================================================================
class Key(eg.ActionClass):
    class text:
        labelEventName = "Event name:"
        genSuffix = 'Generate as event suffix'
        genPayload = 'Generate as payload'
        labelKeys = "First set of characters (Caps Lock OFF):"
        labelKeys2 = "Second set of characters (Caps Lock ON):"
        labelKeys3 = '(For the mode "Numpad" is significant only the first character.)'
        labelTimeout1 = "Timeout:"
        labelTimeout2 = "(0 = never timeout)"
        accumulate = "Accumulate keys"
        labelMode = "Mode of Multitapper:"
        string = "SMS like string"
        numpad = "Numpad (numerical string)"
        singleKey = "Single Key"

    def __call__(self,mode,evtName,formatEvent,keys,timeout):
        return self.plugin.Multitapper(keys,timeout,formatEvent,evtName,mode)

    def GetLabel(self,mode,evtName,formatEvent,keys,timeout):
        if formatEvent:
            sep = ' '
        else:
            sep = '.'
        return evtName+sep+keys[0]

    def Configure(self, mode = 0, evtName = '', formatEvent = 0,keys = ['',''], timeout=0.0):
        text = self.text
        panel = eg.ConfigPanel(self)
        lblEventName = wx.StaticText(panel, -1, text.labelEventName)
        ctrlEventName = wx.TextCtrl(panel, -1, evtName, style=wx.TE_NOHIDESEL)
        choiceMode = wx.Choice(
            panel,
            -1,
            choices=(text.string, text.numpad, text.singleKey)
        )
        lblMode = wx.StaticText(panel, -1, text.labelMode)
        choiceMode.SetSelection(mode)
        rb0 = panel.RadioButton(not formatEvent,text.genSuffix, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(formatEvent,text.genPayload)
        lblKeys = wx.StaticText(panel, -1, text.labelKeys)
        lblKeys2 = wx.StaticText(panel, -1, text.labelKeys2)
        ctrlKeys = wx.TextCtrl(panel, -1, keys[0], style=wx.TE_NOHIDESEL)
        ctrlKeys2 = wx.TextCtrl(panel, -1, keys[1], style=wx.TE_NOHIDESEL)
        lblKeys3 = wx.StaticText(panel, -1, text.labelKeys3)
        lblKeys3.Enable(False)
        lblTimeout1 = wx.StaticText(panel, -1, text.labelTimeout1)
        lblTimeout2 = wx.StaticText(panel, -1, text.labelTimeout2)
        ctrlTimeout = eg.SpinNumCtrl(
            panel,
            -1,
            timeout,
            integerWidth = 2,
            fractionWidth = 2,
            allowNegative = False,
            min = 0.0,
        )
        ctrlAccumulate = wx.CheckBox(panel, -1, text.accumulate)
        ctrlAccumulate.Enable(False)
    #Sizers
        rbSizer = wx.BoxSizer(wx.VERTICAL)
        rbSizer.Add(rb0,0,wx.TOP,3)
        rbSizer.Add(rb1,0,wx.TOP,3)
        topSizer = wx.FlexGridSizer(4,0,2,15)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(lblMode)
        topSizer.Add(lblEventName)
        topSizer.Add(choiceMode)
        topSizer.Add(ctrlEventName)
        topSizer.Add(ctrlAccumulate,0,wx.TOP,3)
        topSizer.Add(rbSizer,0,wx.TOP|wx.EXPAND)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        keysSizer = wx.BoxSizer(wx.HORIZONTAL)
        keysSizer.Add(ctrlKeys,0,wx.RIGHT,8)
        keysSizer.Add(lblKeys3,0,wx.TOP,4)
        timeoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeoutSizer.Add(lblTimeout1,0,wx.TOP,4)
        timeoutSizer.Add(ctrlTimeout,0,wx.LEFT|wx.RIGHT,8)
        timeoutSizer.Add(lblTimeout2,0,wx.TOP,4)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer,0,wx.EXPAND)
        mainSizer.Add(nameSizer)
        mainSizer.Add(lblKeys,0,wx.TOP,4)
        mainSizer.Add(keysSizer,0,wx.TOP,3)
        mainSizer.Add(lblKeys2,0,wx.TOP,8)
        mainSizer.Add(ctrlKeys2,0,wx.TOP,3)
        mainSizer.Add(timeoutSizer,0,wx.TOP,12)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)

        def onChoiceMode(event=None):
            mode = choiceMode.GetSelection()
            if mode == 0:
                ctrlKeys2.Enable(True)
                lblKeys2.Enable(True)
                ctrlAccumulate.SetValue(True)
            elif mode == 1:
                ctrlKeys2.Enable(False)
                lblKeys2.Enable(False)
                ctrlAccumulate.SetValue(True)
                ctrlKeys2.SetValue('')
            else:
                ctrlKeys2.Enable(False)
                lblKeys2.Enable(False)
                ctrlAccumulate.SetValue(False)
                ctrlKeys2.SetValue('')
            if event:
                event.Skip()
        choiceMode.Bind(wx.EVT_CHOICE,onChoiceMode)
        onChoiceMode()

        while panel.Affirmed():
            panel.SetResult(
                choiceMode.GetSelection(),
                ctrlEventName.GetValue(),
                rb1.GetValue(),
                [ctrlKeys.GetValue(),ctrlKeys2.GetValue()],
                ctrlTimeout.GetValue(),
            )
#===============================================================================

class Enter(eg.ActionClass):

    def __call__(self):
        self.plugin.OnEnter()
#===============================================================================

class Cancel(eg.ActionClass):

    def __call__(self):
        self.plugin.mode=3
#===============================================================================

class Shift(eg.ActionClass):

    def __call__(self):
        self.plugin.OnShift()
#===============================================================================

ACTIONS = (
    (Key, 'Key', 'Key', 'Key.', None),
    (Enter, 'Enter', 'Enter', 'Enter.', None),
    (Cancel, 'Cancel', 'Cancel', 'Cancel.', None),
    (Shift, 'Shift', 'Caps Lock', 'Caps Lock.', None),
)
#===============================================================================
class Multitap(eg.PluginClass):

    def __init__(self):
        self.evtString = ''
        self.oldKeys = ''
        self.indx = 0
        self.timeout = 0
        self.timer = Timer(0.0, self.OnTimeout)
        self.AddActionsFromList(ACTIONS)
        self.formatEvent = False
        self.evtName = ''
        self.shift = False
        self.mode = 3 #3 .. idle, 0 .. string, 1 .. number, 2 .. "SingleKey"
                      #4 .. if SMS mode starts by Shift


    def Multitapper(self,keys,timeout,formatEvent,evtName, mode):
        self.timer.cancel()
        if self.mode > 2: #3 = idle, 4 = Shift after idle
            self.evtString = ''
            self.oldKeys = ''
            self.timeout=timeout
            self.formatEvent = formatEvent
            self.evtName = evtName
            self.shift = False if self.mode == 3 else True
            self.mode = mode
        if self.mode==0:
            set = int(self.shift)
            if self.oldKeys == '':
                self.oldKeys = keys[set]
                self.indx = -1
            if keys[set] != self.oldKeys:
                self.evtString+=self.oldKeys[self.indx]
                self.oldKeys = keys[set]
                self.indx=0
            else:
                self.indx+=1
                if self.indx > len(keys[set])-1:
                    self.indx=0
        elif self.mode==1:
            self.timer.cancel()
            if self.timeout==0:
                self.timeout=timeout
                self.evtName = evtName
            self.evtString += keys[0]
        else:       # mode Single Key = "Without accumulate"
            if self.oldKeys == '':
                self.oldKeys = keys[0]
                self.indx = -1
            if keys[0] != self.oldKeys: #ERROR or "Enter"?  -> meantime Error
                self.mode = 3
                self.evtString = ''
                self.oldKeys = ''
                self.indx = 0
                self.timeout = 0
                return #without timer start
            else:
                self.indx+=1
                if self.indx > len(keys[0])-1:
                    self.indx=0
        if self.timeout>0:
            self.timer = Timer(self.timeout, self.OnTimeout)
            self.timer.start()
        return self.evtString


    def OnShift(self):
        self.timer.cancel()
        if self.mode == 3:
            self.mode = 4
        elif self.mode == 4:
            self.mode = 3
        elif self.mode == 0:
            self.shift = not self.shift #toggle shift
            if self.oldKeys != '':
                self.evtString+=self.oldKeys[self.indx]
            self.oldKeys = ''


    def OnTimeout(self):
        if self.mode==2:     #SingleKey mode
            self.evtString=self.oldKeys[self.indx]
            self.GenerateEvent()
        elif self.mode == 1: #Numpad mode
            self.GenerateEvent()
        else:                #String mode
            self.evtString+=self.oldKeys[self.indx]
        self.oldKeys = ''


    def OnEnter(self):
        self.timer.cancel()
        if self.oldKeys != '':
            self.evtString+=self.oldKeys[self.indx]
        self.GenerateEvent()


    def GenerateEvent(self):
        if self.evtString != '':
            if self.formatEvent:
                self.TriggerEvent(self.evtName, self.evtString)
            else:
                self.TriggerEvent(self.evtName+'.'+self.evtString if self.evtName !='' else self.evtString)
        self.mode = 3 #Cleaning
#===============================================================================


