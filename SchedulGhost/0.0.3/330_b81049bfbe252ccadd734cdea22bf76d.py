version="0.0.3"

# plugins/SchedulGhost/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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
# changelog:

# 0.0.0 by Pako 2010-08-28 13:07 GMT+1
#     - initial version
# 0.0.1 by Pako 2010-08-29 13:21 GMT+1
#     - forum URL settings
# 0.0.2 by Pako 2010-09-02 18:52 GMT+1
#     - bugfix: Egg timer - popup window is opened (blank), although it has been disabled
# 0.0.3 by Pako 2010-09-11 19:07 GMT+1
#     - added action "Start egg timer" (without the possibility of adjust of time to elapse)
#===============================================================================

eg.RegisterPlugin(
    name = "SchedulGhost",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{39EFE2FF-6CA9-4450-B0E3-1AA125420B37}",
    description = ur'''<rst>This plugin is designed to easily schedule events to
 be trigger at any time of the day or night. Events can be scheduled to trigger 
 periodically, once, daily, weekly, monthly or yearly.''',
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2740",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAMAAAC5zwKfAAADAFBMVEX////AwMCAgIBA"
        "QEAAAACqqqpWVlYCDgECGgEEKAIENAMGQgMHTgMJXQUKaQUKagUKXgQIUAQHRAQGNgMF"
        "KgIDGwICDwEENgIJbQURpQgaygogxQsmwA0tvA8uvxAvwA8yxBAzxhE0yBI2yRI3yxM5"
        "zhM60BM01RIu2hIo3hAcswwOdAcHOwQFSAMKjwUVyQgevgsmswwntQ0quA0rug470hM8"
        "1BU91RU/2BU03hMn5BESnAkKTwUKjgQUxggbugojrwslsQxA2hZB3Bc14RMp5RASnAoK"
        "UAUHagQM1AYWvgcgqgohrAtC3hZD3xcv5RMd6w4PdwgERwIIjAQSwwcWtAgdpwlD4Rg4"
        "5RUq6RIUngkKUAYGaQMK0AQSuQcaowgbpQlF4xhG5Rgz6hMd7A8QeAgFaQMOvgYSrgYY"
        "oAdI5xg66RYt7BMGaAMOtAUUmgYWngZI6BlJ6ho07RUReQgFaAINsgUSmAVK7Bo27xQQ"
        "eQkFZwMLsAQQlQVL7ho18BYReQkEZwMKuAQOkwRL7xsw8BQReggDRQIHzQQLpAQ/8Bgg"
        "8g8MUgYGiAMIrQQMkQRN8Bs38hUXogwEZgIItgMJjQRN8hsx8xURewkGywIIoANA8xkh"
        "9BEMUwYFhwIGqQIIiwNP8xw49RcYpAwCRAIGswIGiAJO9Rwy9hUNUwYEhgIFnAJB9hkY"
        "owsCMwEEsAIFhQJQ9hwz9RQJPgUEZQEDmQFC9hgSfAoEkwACggBQ9xwlwREBDQEDrAA1"
        "+BcDEAIBGAECnQA++BkFHgMBJQEBjgBH+RsHLQQCMAEAgABQ+R0JOwUCPAEMSgYCRwEO"
        "WAcDVAEQZwgDXwESdQkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8PnYuAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAl5JREFUeNpjYBjagJGJmQUN"
        "MDMxUtE0CszEaRp5ZrKysRAEbKxUNY4UI5mIMw4EmKjoPGIdSYLziHIkpnnsHJxc3Dy8"
        "fPwCgkLCIqJipJmIbp64hKSUtIysnLyCopKyiqqauoamlrYO8Saimaerp29gaGRsgjDQ"
        "1MzcwtLK2oZIE1HN07W1s3dwxDTQydnF1c2dGBNRzfPw9PL2wW6gr59/QCBhE1HMCwoO"
        "CQ3DbWB4RGRUNAETWZHlY2Lj4hPwGZiYlJySiqwDMz0ip+e09IxMQgZmZecgm8iGz8O5"
        "efkFhA0sLCouwe1pZA+XlpUTZ2BFZRVOTyN5uLqmllgD6+obcHgayYGNTc3EG9jS2obd"
        "iQgHtnd0kmJgV3cPNicyIqzp7esnxcAJEych9DJiieLJU6aSZuC06TOwRDS8PmqfOYtU"
        "A2fPmQvTzYzp43nzF5Bq4MJFizH8DPfxkqXLSDdw+YqV6H6G+3jVanIMXLMWzc9wH69b"
        "v4EcAzdu2ozqZ7iPt2wlz8Bt21H9DPfxjp3kGbhrN6qfYbw9e8k1cN9+mBkoBh44SK6B"
        "hw5jNfDIUXINPHYcq4EnTpJr4KnTWA08Q76BZ7EaeI58A89jNfAC+QZexGrgJfINvEwf"
        "A6nuZapHCtWTDdUTNtWzHtULB6oVX1QvYKleBVC9kqJ6NUr9ip7qTRGqN5ao35yjeoOT"
        "6k1i6jfaqd6toH7Hh+pdM+p3HqnfvaV6B5z6QwTUH8Sg/jAL9QeCqD9URf3BNOoP95Hm"
        "SGIGJElwJJVHYUkwDgSoPOyM30zqDrZTYNogAQBaQepgoGvj8QAAAABJRU5ErkJggg=="
    )
,
)
#===============================================================================

import os
import wx.lib.masked as maskedlib
import wx.calendar as wxCal
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from eg.WinApi.Dynamic import BringWindowToTop
from calendar import day_name, month_name, monthrange
from datetime import datetime as dt
from datetime import timedelta as td
from time import mktime, strptime, localtime, sleep
from copy import deepcopy as cpy
from xml.dom import minidom as miniDom
from win32gui import MessageBox, GetWindowPlacement
from codecs import lookup
from codecs import open as openFile
from winsound import PlaySound, SND_ASYNC

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class Text:
    Suspend = "System session suspend."
    Resume = "System session resume."
    SessionLock = "System session lock."
    SessionUnlock =  "System session unlock."
    soundProblem = 'There was a problem opening or playing the file "%s"'
    label2 = "SchedulGhost.xml folder:"
    prefLabel = "Default event prefix:"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    toolTipFile = "Press button and browse to select logfile ..."
    browseFile = 'Select the logfile'
    logLabel = "Log scheduler events to following logfile:"
    nextRun = "Next run: %s"
    none = "None"
    execut = 'Schedule "%s" - Start event triggered. Next time: %s.'
    execStop = 'Schedule "%s" - Stop event triggered.'
    cancAndDel = 'Schedule "%s" canceled and deleted.'
    cancAndDis = 'Schedule "%s" canceled (disabled).'
    newSched = 'Schedule "%s" scheduled. Next time: %s.'
    re_Sched = 'Schedule "%s" re-scheduled. New next time: %s.'
    start = 'SchedulGhost plugin started. All valid schedules will be scheduled:'
    stop = 'SchedulGhost plugin stoped. All scheduled schedules and egg timers will be canceled:'
    canc = 'Schedule "%s" canceled.'
    holidButton = "Public holidays ..."
    fixBoxLabel = "Fix public holidays:"
    varBoxLabel = "Variable public holidays:"
    ok = "OK"
    cancel = "Cancel"
    add = "Add"
    delete = "Delete"
    first_day = "The first day of the week:"
    xmlComment = "SchedulGhost configuration file. Updated at %s."
    eggStart = 'Egg timer "%s.%s" (%s) started.'
    eggElaps = 'Egg timer "%s.%s" - time %s has elapsed.'
    eggCancel = 'Egg timer "%s.%s" (%s) canceled.'
    popupTitle = 'Egg Timer Popup Window'
    popupTip1 = 'Right click to close window\nTime elapsed at %s'
    popupTip2 = 'Drag-and-move to setup of window position'
    mess = """In the folder "%s"
is name "Log.txt" reserved for system logfile of EventGhost.

Change the file name or folder !"""
#===============================================================================

def Ticks2Delta(start, end):
    delta = td(microseconds = 1000000 * (end - start)).seconds
    hh = delta / 3600
    mm = (delta - 3600 * hh) / 60
    ss = delta - 3600 * hh - 60 * mm
    return '%02d:%02d:%02d' % (hh, mm, ss)
#===============================================================================

def FindMonthDay(year, month, weekday, index):
    """weekday = what day of the week looking for (numbered 0-6, 0 = monday)
    index = how many occurrence of looking for (numbered 0-4 and 5 for the last day)
    Returns the day of the month (date) or 0 (if no such date exists)"""
    first_wd, length = monthrange(year, month)
    day = 1 + weekday - first_wd
    if day < 1:
        day += 7
    if index == 5:
        index = 4 if day <= length % 7 else 3
    day += 7 * index
    if day > length:
        day = 0
    return day
#===============================================================================

class MyTimeCtrl(maskedlib.TimeCtrl):

    def _TimeCtrl__OnSetToNow(self, evt):
        return False
#===============================================================================

class MySpinIntCtrl(eg.SpinIntCtrl):

    def SetNumCtrlId(self, id):
        self.numCtrl.SetId(id)
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):

    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):

    def __init__(self,*args,**kwargs):
        if 'defaultFile' in kwargs:
            self.defaultFile = kwargs['defaultFile']
            del kwargs['defaultFile']
        else:
            self.defaultFile = ""
        eg.FileBrowseButton.__init__(self, *args, **kwargs)


    def GetValue(self):
        if self.textControl.GetValue():
            res = self.textControl.GetValue()
        else:
            res = "%s\\%s" % (self.startDirectory, self.defaultFile)
        return res


    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

newEVT_UPDATE_DIALOG = wx.NewEventType()
EVT_UPDATE_DIALOG = wx.PyEventBinder(newEVT_UPDATE_DIALOG, 1)
#===============================================================================

newEVT_CHECKLISTCTRL = wx.NewEventType()
EVT_CHECKLISTCTRL = wx.PyEventBinder(newEVT_CHECKLISTCTRL, 1)


class Evt_ChecklistCtrl(wx.PyCommandEvent):

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None


    def SetValue(self, val):
        self.myVal = val


    def GetValue(self):
        return self.myVal
#===============================================================================

newEVT_BUTTON_AFTER = wx.NewEventType()
EVT_BUTTON_AFTER = wx.PyEventBinder(newEVT_BUTTON_AFTER, 1)


class EventAfter(wx.PyCommandEvent):

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None


    def SetValue(self, val):
        self.myVal = val


    def GetValue(self):
        return self.myVal
#===============================================================================

class extColourSelectButton(eg.ColourSelectButton):

    def __init__(self,*args,**kwargs):
        eg.ColourSelectButton.__init__(self, *args)
        self.title = kwargs['title']


    def OnButton(self, event):
        colourData = wx.ColourData()
        colourData.SetChooseFull(True)
        colourData.SetColour(self.value)
        for i, colour in enumerate(eg.config.colourPickerCustomColours):
            colourData.SetCustomColour(i, colour)
        dialog = wx.ColourDialog(self.GetParent(), colourData)
        dialog.SetTitle(self.title)
        if dialog.ShowModal() == wx.ID_OK:
            colourData = dialog.GetColourData()
            self.SetValue(colourData.GetColour().Get())
            event.Skip()
        eg.config.colourPickerCustomColours = [
            colourData.GetCustomColour(i).Get() for i in range(16)
        ]
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
#===============================================================================

class extFontSelectButton(eg.FontSelectButton):

    def OnButton(self, event):
        fontData = wx.FontData()
        if self.value is not None:
            font = wx.FontFromNativeInfoString(self.value)
            fontData.SetInitialFont(font)
            fontData.EnableEffects(False)
        else:
            fontData.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dialog = wx.FontDialog(self.GetParent(), fontData)
        if dialog.ShowModal() == wx.ID_OK:
            fontData = dialog.GetFontData()
            font = fontData.GetChosenFont()
            self.value = font.GetNativeFontInfo().ToString()
            event.Skip()
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
#===============================================================================

class HolidaysFrame(wx.Frame):
    fixWin = None
    varWin = None
    fixHolidays = []
    varHolidays = []

    def __init__(self, parent, plugin):
        self.plugin = plugin
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.CAPTION,
            name = self.plugin.text.holidButton
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.fixHolidays, self.varHolidays = cpy(self.panel.holidays)
        self.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)


    def ShowHolidaysFrame(self):
        text = self.plugin.text
        self.SetTitle(text.holidButton)
        self.fixWin = CalendarPopup(self, False, self.plugin.first_day)
        self.varWin = CalendarPopup(self, True, self.plugin.first_day)
        calW, calH = self.fixWin.GetWinSize()
        fixLbl = wx.StaticText(self, -1, text.fixBoxLabel)
        variableLbl = wx.StaticText(self, -1, text.varBoxLabel)
        widthList = [self.GetTextExtent("30. %s 2000" % month)[0] +
            SYS_VSCROLL_X for month in list(month_name)]
        widthList.append(fixLbl.GetSize()[0])
        widthList.append(variableLbl.GetSize()[0])
        w = max(widthList) + 5
        self.SetMinSize((w + calW + 30, 2 * calH + 128))
        self.fixListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.fix_add_Btn = wx.Button(self, -1, text.add)
        self.fix_del_Btn = wx.Button(self, -1, text.delete)
        self.fix_del_Btn.Enable(False)
        self.varListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.var_add_Btn = wx.Button(self, -1, text.add)
        self.var_del_Btn = wx.Button(self, -1, text.delete)
        self.var_del_Btn.Enable(False)
        line = wx.StaticLine(self, -1, style = wx.LI_HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        fixSizer = wx.GridBagSizer(2, 8)
        fixSizer.SetMinSize((w + 8 + calW, -1))
        varSizer = wx.GridBagSizer(2, 8)
        varSizer.SetMinSize((w + 8 + calW, -1))
        fixSizer.Add(fixLbl, (0, 0))
        fixSizer.Add(self.fixListBox, (1, 0), (3, 1))
        fixSizer.Add(self.fix_add_Btn, (1, 1))
        fixSizer.Add((-1, 15), (2, 1))
        fixSizer.Add(self.fix_del_Btn, (3, 1))
        varSizer.Add(variableLbl, (0, 0))
        varSizer.Add(self.varListBox, (1, 0), (3,1))
        varSizer.Add(self.var_add_Btn, (1, 1))
        varSizer.Add((-1, 15), (2, 1))
        varSizer.Add(self.var_del_Btn, (3, 1))
        sizer.Add(fixSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((-1, 12))
        sizer.Add(varSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((1, 16))
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND)
        sizer.Add((1,5))
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sz = self.GetMinSize()
        self.SetSize(sz)
        self.fixListBox.Reset(self.fixHolidays)
        self.varListBox.Reset(self.varHolidays)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        btn2.Bind(wx.EVT_BUTTON, self.onCancel)
        btn1.Bind(wx.EVT_BUTTON, self.onOK)
        self.fix_add_Btn.Bind(wx.EVT_BUTTON, self.onFixAddBtn)
        self.var_add_Btn.Bind(wx.EVT_BUTTON, self.onVarAddBtn)
        self.fix_del_Btn.Bind(wx.EVT_BUTTON, self.onFixDelBtn)
        self.var_del_Btn.Bind(wx.EVT_BUTTON, self.onVarDelBtn)
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)
        sizer.Layout()
        self.SetSizer(sizer)
        self.MakeModal(True)
        self.Show(True)


    def onClose(self, evt):
        self.MakeModal(False)
        self.GetParent().GetParent().Raise()
        self.Destroy()


    def onCancel(self, evt):
        self.Close()


    def onOK(self, evt):
        self.panel.holidays = (self.fixHolidays, self.varHolidays)
        self.Close()


    def onHolBoxSel(self, evt):
        if  evt.GetId() == self.fixListBox.GetId():
            self.fix_del_Btn.Enable(True)
        else:
            self.var_del_Btn.Enable(True)
        evt.Skip()


    def onFixAddBtn(self, evt):
        pos = self.ClientToScreen(self.fix_add_Btn.GetPosition())
        self.fixWin.PopUp(pos, self.fixHolidays)


    def onVarAddBtn(self, evt):
        pos = self.ClientToScreen(self.var_add_Btn.GetPosition())
        self.varWin.PopUp(pos, self.varHolidays)


    def onFixDelBtn(self, evt):
        self.fixHolidays.pop(self.fixListBox.GetSelection())
        if self.fixListBox.Reset(self.fixHolidays):
            self.fix_del_Btn.Enable(False)


    def onVarDelBtn(self, evt):
        self.varHolidays.pop(self.varListBox.GetSelection())
        if self.varListBox.Reset(self.varHolidays):
            self.var_del_Btn.Enable(False)


    def OnChangeDay(self, evt):
        if evt.GetId() == self.fixWin.GetCalId():
            self.fixListBox.Reset(self.fixHolidays)
        else:
            self.varListBox.Reset(self.varHolidays)
        evt.Skip()
#===============================================================================

class HolidaysBox(wx.ListBox):

    def __init__ (self, parent, id, size, style):
        wx.ListBox.__init__(
            self,
            parent = parent,
            id = id,
            size = size,
            style = style
        )
        self.sel = -1
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)


    def Reset(self, list):
        tmpList = []
        for item in list:
            day = item[-1]
            day = "  %i" % day if day < 10 else "%i" % day
            if len(item) == 2:
                tmpList.append("%s. %s" % (day, month_name[item[0]]))
            else:
                tmpList.append("%s. %s %i" % (day, month_name[item[1]], item[0]))
        self.Set(tmpList)
        if self.sel > -1 and self.sel < self.GetCount():
            self.SetSelection(self.sel)
            return False
        else:
            return True


    def  onHolBoxSel(self, evt):
        self.sel = evt.GetSelection()
        evt.Skip()
#===============================================================================

class CalendarPopup(wx.PopupWindow):
    yearChange = True

    def __init__(self, parent, yearChange, first_day):
        self.yearChange = yearChange
        wx.PopupWindow.__init__(self, parent)
        startDate = wx.DateTime()
        startDate.Set(1, 0)
        self.cal = wxCal.CalendarCtrl(
            self,
            -1,
            startDate,
            style = (wxCal.CAL_MONDAY_FIRST, wxCal.CAL_SUNDAY_FIRST)[first_day]
                | wxCal.CAL_SHOW_HOLIDAYS
                | wxCal.CAL_SEQUENTIAL_MONTH_SELECTION
                | wxCal.CAL_SHOW_SURROUNDING_WEEKS 
        )
        self.cal.EnableYearChange(yearChange)
        sz = self.cal.GetBestSize()
        self.SetSize(sz)
        self.cal.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)
        self.cal.Bind(wxCal.EVT_CALENDAR_MONTH, self.OnChangeMonth)
        self.cal.Bind(wxCal.EVT_CALENDAR_YEAR, self.OnChangeMonth)
        self.cal.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)


    def OnLeaveWindow(self, evt):
        self.PopDown()
        evt.Skip()


    def GetCalId(self):
        return self.cal.GetId()


    def GetWinSize(self):
        return self.GetSize()


    def OnChangeDay(self, evt):
        date = evt.GetDate()
        day, month, year = date.GetDay(), 1 + date.GetMonth(), date.GetYear()
        newHoliday = (year, month, day) if self.yearChange else (month, day)
        if not newHoliday in self.holidays:
            self.holidays.append(newHoliday)
            self.holidays.sort()
        date = self.cal.GetDate()
        self.cal.SetHoliday(day)
        date.AddDS(wx.DateSpan.Day())
        self.cal.SetDate(date)
        self.Refresh()
        evt.Skip()


    def OnChangeMonth(self, evt = None):
        date = self.cal.GetDate()
        cur_month = date.GetMonth() + 1   # convert wx.DateTime 0-11 => 1-12
        if self.yearChange:
            cur_year = date.GetYear()
            for year, month, day in self.holidays:
                if year == cur_year and month == cur_month:
                    self.cal.SetHoliday(day)
        else:
            for month, day in self.holidays:
                if month == cur_month:
                    self.cal.SetHoliday(day)


    def PopUp(self, position, holidays):
        self.cal.EnableHolidayDisplay(False)
        self.cal.EnableHolidayDisplay(True)
        self.SetPosition(position)
        self.holidays = holidays
        self.OnChangeMonth()
        self.Show(True)


    def PopDown(self):
        self.Show(False)
        self.Close()
#===============================================================================

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, text, width):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            size = (width, 164),
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        for i in range(len(text.header)):
            self.InsertColumn(i, text.header[i])
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(
            1,
            width - self.GetColumnWidth(0) - 2 * 116 - SYS_VSCROLL_X - self.GetWindowBorderSize()[0]
        )
        self.SetColumnWidth(2, 116)
        self.SetColumnWidth(3, 116)
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)


    def OnItemSelected(self, evt):
        self.SelRow(evt.m_itemIndex)
        evt.Skip()


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = Evt_ChecklistCtrl(newEVT_CHECKLISTCTRL, self.GetId())
        evt.SetValue((index, flag))
        self.GetEventHandler().ProcessEvent(evt)


    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def AppendRow(self):
        ix = self.GetItemCount()
        self.InsertStringItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
#===============================================================================

class schedulerDialog(wx.Dialog):
    lastRow = -1
    data = []

    def __init__(self, text, plugin):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            text.dialogTitle,
            style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX|wx.CLOSE_BOX,
        )

    #    import locale as l
    #    l.setlocale(l.LC_ALL, "us") # only for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        bttns = []
        self.ctrls = []
        self.plugin = plugin
        self.plugin.dialog = self
        self.tmpData = self.plugin.tmpData = cpy(self.plugin.data)
        self.text = text

        def fillDynamicSizer(type, data = None, old_type = 255):
            flag = old_type != type
            if flag:
                dynamicSizer.Clear(True)
                self.ctrls = []
                self.ctrls.append(wx.NewId())
                self.ctrls.append(wx.NewId())
            if type == -1:
                return
            if type != 1 and flag:
                topSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseDay),
                    wx.HORIZONTAL
                )
            if type == 0:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp,0,wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    yearlyCtrl = wx.CheckBox(self, self.ctrls[3], self.text.yearly)
                    topSizer.Add(yearlyCtrl, 0, wx.EXPAND|wx.LEFT, 30)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                    yearlyCtrl = wx.FindWindowById(self.ctrls[3])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7]) - 1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
                    yearlyCtrl.SetValue(data[3])
            elif type == 2:
                if flag:
                    if self.plugin.first_day:
                        choices = list(day_name)[:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = choices,
                        size=((-1,110)),
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_2 = wx.CheckBox(
                        self,
                        self.ctrls[3],
                        self.text.holidCheck_2
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[4],
                        self.text.holidCheck_1
                    )
                    topSizer.Add((40,1), 0, wx.ALIGN_CENTER)
                    topSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.theEvery
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.RIGHT, 10
                    )
                    topSizer.Add(weekdayCtrl, 0, wx.TOP)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                    dynamicSizer.Add(holidCheck_2, 0, wx.TOP, 2)
                else:
                    weekdayCtrl = wx.FindWindowById(self.ctrls[2])
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[4])
                val = 127 if not data else data[2]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                check = 0 if (not data or not enable) else data[4]
                holidCheck_1.SetValue(check)
                enable = val & 96 and not val & 31
                holidCheck_2.Enable(enable)
                check = 0 if (not data or not enable) else data[3]
                holidCheck_2.SetValue(check)
            elif type == 3: # Monthly/weekday ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.the
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    self.ctrls.append(wx.NewId())
                    serialCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = self.text.serial_num,
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(serialCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    if self.plugin.first_day:
                        choices = list(day_name)[0:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = choices,
                        size = ((-1, 110)),
                    )
                    dateSizer.Add(weekdayCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.in_
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.LEFT, 10
                    )
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[6],
                        self.text.holidCheck_1
                    )
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                else:
                    serialCtrl = wx.FindWindowById(self.ctrls[2])
                    weekdayCtrl = wx.FindWindowById(self.ctrls[3])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[4])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[5])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[6])
                val = 0 if not data else data[2]
                for i in range(6):
                    serialCtrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                val = 63 if not data else data[4]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[5]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
                check = 0 if (not data or not enable) else data[6]
                holidCheck_1.SetValue(check)
            elif type == 4: # Monthly/day ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                    self.ctrls.append(wx.NewId())
                    q_1_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = [str(i) + '.' for i in range(1, 9)],
                        size = ((40, 125)),
                    )
                    dateSizer.Add(q_1_Ctrl, 0, wx.LEFT, 5)
                    self.ctrls.append(wx.NewId())
                    q_2_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = [str(i) + '.' for i in range(9, 17)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_2_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_3_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = [str(i) + '.' for i in range(17, 25)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_3_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_4_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = [str(i) + '.' for i in range(25, 32)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_4_Ctrl, 0, wx.LEFT, -1)
                    dateSizer.Add((-1, 1), 1, wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[6],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[7],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    dateSizer.Add((5, 1), 0)
                else:
                    q_1_Ctrl = wx.FindWindowById(self.ctrls[2])
                    q_2_Ctrl = wx.FindWindowById(self.ctrls[3])
                    q_3_Ctrl = wx.FindWindowById(self.ctrls[4])
                    q_4_Ctrl = wx.FindWindowById(self.ctrls[5])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[6])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[7])
                val = 0 if not data else data[2]
                for i in range(8):
                    q_1_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                for i in range(8):
                    q_2_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[4]
                for i in range(8):
                    q_3_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[5]
                for i in range(7):
                    q_4_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[6]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[7]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
            elif type == 5:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7])-1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
            #elif type == 1: # daily
            #    pass
            if flag:
                timeSizer = wx.GridBagSizer(0, 0)
                bottomSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseTime),
                    wx.HORIZONTAL
                )
                dynamicSizer.Add(bottomSizer, 0, wx.EXPAND | wx.TOP, 16)
                bottomSizer.Add(timeSizer, 0, wx.EXPAND)
                timeSizer.Add(
                    wx.StaticText(
                        self, 
                        -1,
                        self.text.start
                    ),
                    (0, 0),
                    (1, 2)
                )
                durLabel = wx.StaticText(self, -1, self.text.length)
                timeSizer.Add(durLabel, (0, 3), (1, 2))
                spinBtn = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                initTime = wx.DateTime_Now()
                initTime.SetSecond(0)
                initTime.AddTS(wx.TimeSpan.Minute())
                val = data[0] if data and data[0] else initTime
                timeCtrl = maskedlib.TimeCtrl(
                    self, 
                    self.ctrls[0],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn
                )
                timeSizer.Add(timeCtrl, (1, 0), (1, 1))
                timeSizer.Add(spinBtn, (1, 1), (1, 1))
                timeSizer.Add((40, -1), (1, 2), (1, 1))
                spinBtn2 = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                val = data[1] if data and data[1] else "00:00:00"
                lenCtrl = MyTimeCtrl(
                    self,
                    self.ctrls[1],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn2
                )
                timeSizer.Add(lenCtrl, (1, 3), (1, 1))
                timeSizer.Add(spinBtn2, (1, 4), (1, 1))
                bottomSizer.Add((-1,-1), 1, wx.EXPAND)
                testBttn = wx.Button(
                    self,
                    -1 if len(bttns) == 0 else bttns[-1],
                    self.text.testButton
                )
                bottomSizer.Add(testBttn, 0, wx.EXPAND | wx.RIGHT)
            else:
                timeCtrl = wx.FindWindowById(self.ctrls[0])
                val = data[0] if data and data[0] else wx.DateTime_Now()
                timeCtrl.SetValue(val)
                lenCtrl = wx.FindWindowById(self.ctrls[1])
                val = data[1] if data and data[1] else "00:00:00"
                lenCtrl.SetValue(val)
                OnTimeChange() #enable / disable handle for duplicate
            if type == 5: #periodically
                if flag:
                    bottomSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.choosePeriod),
                        wx.HORIZONTAL
                    )
                    self.ctrls.append(wx.NewId())
                    numCtrl = MySpinIntCtrl(self, -1, value = 1, min = 1)
                    numCtrl.SetNumCtrlId(self.ctrls[3])
                    bottomSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.andThenEvery
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    bottomSizer.Add(numCtrl, 0, wx.LEFT, 4)
                    self.ctrls.append(wx.NewId())
                    unitCtrl = wx.Choice(
                        self,
                        self.ctrls[4],
                        choices = self.text.units
                    )
                    bottomSizer.Add(unitCtrl, 0, wx.LEFT, 8)
                    dynamicSizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 16)
                    dynamicSizer.Layout()
                else:
                    numCtrl = wx.FindWindowById(self.ctrls[3])
                    unitCtrl = wx.FindWindowById(self.ctrls[4])
                if data:
                    numCtrl.SetValue(str(data[3]))
                    unitCtrl.SetSelection(data[4])
            elif flag:
                dynamicSizer.Layout()
            return dynamicSizer.GetMinSize()[0]


        def Diff():
            applyBttn = wx.FindWindowById(bttns[5])
            flg = self.tmpData != self.plugin.data
            applyBttn.Enable(flg)


        def onCheckListBox(evt):
            id = evt.GetId()
            sel = evt.GetSelection()
            box = self.FindWindowById(id)
            ix = self.ctrls.index(id)
            type = self.tmpData[self.lastRow][2]
            cond = (type == 2 and ix == 2) or (type == 3 and ix == 3)
            if cond and self.plugin.first_day:
                exp = (6, 0, 1, 2, 3, 4, 5)[sel]
            else:
                exp = sel
            if box.IsChecked(sel):
                self.tmpData[self.lastRow][3][ix] |= 2 ** exp
            else:
                self.tmpData[self.lastRow][3][ix] &= 255 - 2 ** exp
            if cond:
                holidCheck_1 = wx.FindWindowById(self.ctrls[-1])
                val = self.tmpData[self.lastRow][3][ix]
                flg = val & 31 and not val & 96
                holidCheck_1.Enable(flg)
                if not flg:
                    holidCheck_1.SetValue(0)
                    self.tmpData[self.lastRow][3][-1] = 0
                if type == 2:
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    val = self.tmpData[self.lastRow][3][2]
                    flg = val & 96 and not val & 31
                    holidCheck_2.Enable(flg)
                    if not flg:
                        holidCheck_2.SetValue(0)
                        self.tmpData[self.lastRow][3][3] = 0
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnTimeChange(evt = None):
            if evt:
                ix = self.ctrls.index(evt.GetId())
                self.tmpData[self.lastRow][3][ix] = evt.GetValue()
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
            else:
                ix = 1
            if ix == 1:
                enable = self.tmpData[self.lastRow][3][1] != "00:00:00"
                stopLabel.Enable(enable)
                stopCtrl.Enable(enable)
                stopTxt = self.tmpData[self.lastRow][7] if enable else ""
                stopCtrl.ChangeValue(stopTxt)
            Diff()


        def onPeriodUnit(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[4]:
                self.tmpData[self.lastRow][3][4] = evt.GetSelection()
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
            else:
                evt.Skip()
            Diff()


        def onDatePicker(evt):
            val = str(dt.fromtimestamp(evt.GetDate().GetTicks()))[:10]
            self.tmpData[self.lastRow][3][2] = val
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def onCheckBox(evt):
            val = evt.IsChecked()
            ix = self.ctrls.index(evt.GetId())
            if self.tmpData[self.lastRow][2] == 2 and ix == 3:
                self.tmpData[self.lastRow][3][3] = int(val)
            else:
                self.tmpData[self.lastRow][3][-1] = int(val)
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnUpdateDialog(evt):
            if self.lastRow == evt.GetId():
                OpenSchedule()


        def OnSelectCell(evt):
            self.lastRow = evt.m_itemIndex
            OpenSchedule()
            Diff()
            evt.Skip() # necessary !!!


        def enableBttns(value):
            for i in (1, 2):
                bttn = self.FindWindowById(bttns[i])
                bttn.Enable(value)
                if not value:
                    bttn = self.FindWindowById(bttns[5])
                    bttn.Enable(False)


        def FindNewTitle(title):
            tmpLst = []
            for item in self.tmpData:
                if item[1].startswith(title + " ("):
                    tmpLst.append(item[1][2 + len(title):])
            if len(tmpLst) == 0:
                return "%s (1)" % title
            tmpLst2 = []
            for item in tmpLst:
                if item[-1] == ")":
                    try:
                        tmpLst2.append(int(item[:-1]))
                    except:
                        pass
            if len(tmpLst2) == 0:
                return "%s (1)" % title
            else:
                return "%s (%i)" % (title, 1 + max(tmpLst2))


        def testValidity(data, test):
            mssgs = []
            if test:
                data = [data, ]
            tempDict = dict([(item[1].strip(), item[2]) for item in data])
            if "" in tempDict:
                mssgs.append(self.text.boxTexts[0])
            if not test and len(tempDict) < len(data):
                mssgs.append(self.text.boxTexts[1])
            if "" in [item[5].strip() for item in data]:
                mssgs.append(self.text.boxTexts[3])
            if -1 in [item[2] for item in data]:
                mssgs.append(self.text.boxTexts[2])
            for item in data:
                if item[2] == 5 and item[3][4] < 4:
                    period = item[3][3] * (1, 60, 3600, 86400)[item[3][4]]
                    span =  int(item[3][1][6:]) + 60 * int(item[3][1][3:5]) + 3600 * int(item[3][1][:2])
                    if period <= span:
                        if self.text.boxTexts[4] not in mssgs:
                            mssgs.append(self.text.boxTexts[4])
                            break
            res = len(mssgs)
            if res:
                PlaySound('SystemExclamation', SND_ASYNC)
                MessageBox(
                    self.GetHandle(),
                    "\n".join(mssgs),
                    self.text.boxTitle,
                    48
                    )
            return res


        def onButton(evt):
            id = evt.GetId()
            lngth = len(self.tmpData)
            if id == bttns[0]:   # Add new
                empty = [1, "", -1, [], "", self.plugin.prefix, "", "", ""]
                self.lastRow = lngth
                self.tmpData.append(empty)
                if lngth == 0:
                    enableBttns(True)
                else:
                    Tidy()
                grid.AppendRow()
                prefixCtrl.ChangeValue(self.plugin.prefix)
                grid.SelRow(self.lastRow)
                EnableCtrls(True)
            elif id == bttns[1]: # Duplicate
                item = cpy(self.tmpData[self.lastRow])
                item[4] = ""
                self.lastRow = lngth
                self.tmpData.append(item)
                newTitle = FindNewTitle(self.tmpData[lngth][1])
                self.tmpData[lngth][1] = newTitle
                grid.AppendRow()
                grid.SelRow(lngth)
                grid.SetStringItem(lngth, 1, newTitle)
                OpenSchedule()
            elif id == bttns[2]: # Delete
                self.tmpData.pop(self.lastRow)
                grid.DeleteItem(self.lastRow)
                if len(self.tmpData) > 0:
                    if self.lastRow == len(self.tmpData):
                        self.lastRow -= 1
                    OpenSchedule()
                    grid.SelRow(self.lastRow)
                else:
                    self.lastRow = -1
                    Tidy()
                    EnableCtrls(False)
                    enableBttns(False)
            elif id == bttns[3]: # OK
                if testValidity(self.tmpData, False):
                    return
                self.plugin.data = cpy(self.tmpData)
                self.tmpData = []
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
                self.Close()
            elif id == bttns[4]: # Cancel
                self.tmpData = []
                self.Close()
            elif id == bttns[5]: # Apply
                applyBttn = wx.FindWindowById(bttns[5])
                applyBttn.Enable(False)
                if testValidity(self.tmpData, False):
                    return
                for i in range(len(self.tmpData)):
                    next = self.plugin.NextRun(
                        self.tmpData[i][2],
                        self.tmpData[i][3]
                    )
                    grid.SetStringItem(i, 3, next)
                self.plugin.data = cpy(self.tmpData)
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()


        def EnableCtrls(value):
            typeChoice.Enable(value)
            schedulerName.Enable(value)
            name_label.Enable(value)
            type_label.Enable(value)
            prefixCtrl.Enable(value)
            prefixLabel.Enable(value)
            startCtrl.Enable(value)
            startLabel.Enable(value)
            payloadCtrl.Enable(value)
            payloadLabel.Enable(value)
            if not value:
                stopCtrl.Enable(False)
                stopLabel.Enable(False)


        def OpenSchedule():
            schedulerName.ChangeValue(self.tmpData[self.lastRow][1])
            prefixCtrl.ChangeValue(self.tmpData[self.lastRow][5])
            startCtrl.ChangeValue(self.tmpData[self.lastRow][6])
            stopCtrl.ChangeValue(self.tmpData[self.lastRow][7])
            payloadCtrl.ChangeValue(self.tmpData[self.lastRow][8])
            type = self.tmpData[self.lastRow][2]
            fillDynamicSizer(
                type,
                self.tmpData[self.lastRow][3],
                typeChoice.GetSelection()
            )
            typeChoice.SetSelection(type)


        def Tidy():
            typeChoice.SetSelection(-1)
            schedulerName.ChangeValue("")
            fillDynamicSizer(-1)
            prefixCtrl.ChangeValue("")
            startCtrl.ChangeValue("")
            stopCtrl.ChangeValue("")
            payloadCtrl.ChangeValue("")


        def onCheckListCtrl(evt):
            index, flag = evt.GetValue()
            if self.tmpData[index][0] != int(flag):
                self.tmpData[index][0] = int(flag)
                Diff()


        def onSchedulerTitle(evt):
            txt = evt.GetString()
            grid.SetStringItem(self.lastRow, 1, txt)
            self.tmpData[self.lastRow][1] = txt
            Diff()


        def onTypeChoice(evt):
            type = evt.GetSelection()
            if self.tmpData[self.lastRow][2] != type:
                empty_data = [
                    ["", "", 0, 0],
                    ["", ""],
                    ["", "", 127, 0, 0],
                    ["", "", 0, 0, 63, 63, 0],
                    ["", "", 0, 0, 0, 0, 63, 63],
                    ["", "", 0, 1, 0]
                ]
                self.tmpData[self.lastRow][2] = type
                data = empty_data[self.tmpData[self.lastRow][2]]
                self.tmpData[self.lastRow][3] = data
                fillDynamicSizer(type, data)
            Diff()


        def onPeriodNumber(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[3]:
                self.tmpData[self.lastRow][3][3] = int(evt.GetString())
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
                Diff()
            else:
                evt.Skip()


        def onPrefix(evt):
            self.tmpData[self.lastRow][5] = evt.GetString()
            Diff()
            evt.Skip()


        def onStart(evt):
            self.tmpData[self.lastRow][6] = evt.GetString()
            Diff()
            evt.Skip()


        def onStop(evt):
            self.tmpData[self.lastRow][7] = evt.GetString()
            Diff()
            evt.Skip()


        def onPayload(evt):
            self.tmpData[self.lastRow][8] = evt.GetString()
            Diff()
            evt.Skip()


        def onTestButton(evt):
            data = self.tmpData[self.lastRow]
            if testValidity(data, True):
                return
            ticks = mktime(localtime())
            next = self.plugin.Execute(data, False, ticks)
            next = next[:19] if next else self.plugin.text.none
            self.plugin.updateLogFile(self.text.testRun % (data[1], next))

        dynamicSizer = wx.BoxSizer(wx.VERTICAL)
        wDynamic = fillDynamicSizer(3)
        fillDynamicSizer(-1)
        self.SetSize(wx.Size(wDynamic + 37, 632))
        grid = self.grid = CheckListCtrl(self, text, wDynamic + 20)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.ALL, 5)
        prefixLabel = wx.StaticText(self, -1, self.text.evtPrefix)
        prefixCtrl = wx.TextCtrl(self, -1, "")
        startLabel = wx.StaticText(self, -1, self.text.startSuffix)
        startCtrl = wx.TextCtrl(self, -1, "")
        stopLabel = wx.StaticText(self, -1, self.text.stopSuffix)
        stopCtrl = wx.TextCtrl(self, -1, "")
        payloadLabel = wx.StaticText(self, -1, self.text.evtPayload)
        payloadCtrl = wx.TextCtrl(self, -1, "")
        bttnSizer = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer.Add((5, -1))
        i = 0
        for bttn in self.text.buttons:
            id = wx.NewId()
            bttns.append(id)
            b = wx.Button(self, id, bttn)
            bttnSizer.Add(b,1)
            if i in (1, 2, 5):
                b.Enable(False)
            if i == 3:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton, id = id)
            bttnSizer.Add((5, -1))
            i += 1
        sizer.Add(bttnSizer,0,wx.EXPAND)
        schedulerName = wx.TextCtrl(self, -1, "")
        typeChoice = wx.Choice(self, -1, choices = self.text.sched_type)
        id = wx.NewId() #testBttn
        bttns.append(id)
        self.Bind(wx.EVT_BUTTON, onTestButton, id = id)
        wx.EVT_CHECKLISTBOX(self, -1, onCheckListBox)
        maskedlib.EVT_TIMEUPDATE(self, -1, OnTimeChange)
        wx.EVT_TEXT(self, -1, onPeriodNumber)
        wx.EVT_CHOICE(self, -1, onPeriodUnit)
        wx.EVT_DATE_CHANGED(self, -1, onDatePicker)
        wx.EVT_CHECKBOX(self, -1, onCheckBox)
        self.Bind(EVT_UPDATE_DIALOG, OnUpdateDialog)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSelectCell)
        typeChoice.Bind(wx.EVT_CHOICE, onTypeChoice)
        schedulerName.Bind(wx.EVT_TEXT, onSchedulerTitle)
        prefixCtrl.Bind(wx.EVT_TEXT, onPrefix)
        startCtrl.Bind(wx.EVT_TEXT, onStart)
        stopCtrl.Bind(wx.EVT_TEXT, onStop)
        payloadCtrl.Bind(wx.EVT_TEXT, onPayload)
        self.Bind(EVT_CHECKLISTCTRL, onCheckListCtrl)

        nameSizer = wx.FlexGridSizer(2, 0, 0, 20)
        nameSizer.AddGrowableCol(0,1)
        name_label = wx.StaticText(self, -1, self.text.header[1] + ":")
        nameSizer.Add(name_label)
        type_label = wx.StaticText(self, -1, self.text.type_label)
        nameSizer.Add(type_label)
        nameSizer.Add(schedulerName, 0, wx.EXPAND)
        nameSizer.Add(typeChoice)
        typeSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, ""),
            wx.VERTICAL
        )
        dynamicSizer.SetMinSize((-1, 226))
        typeSizer.Add(nameSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        typeSizer.Add(dynamicSizer, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(typeSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        eventSizer = wx.FlexGridSizer(4, 2, 8, 3)
        eventSizer.AddGrowableCol(1)
        eventSizer.Add(prefixLabel, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        eventSizer.Add(prefixCtrl, 0)
        eventSizer.Add(startLabel,0, wx.ALIGN_RIGHT | wx.TOP, 4)
        eventSizer.Add(startCtrl, 0)
        eventSizer.Add(stopLabel, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        eventSizer.Add(stopCtrl, 0)
        eventSizer.Add(payloadLabel, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        eventSizer.Add(payloadCtrl, 1, wx.EXPAND)        
        sizer.Add(eventSizer, 0, wx.ALL | wx.EXPAND, 5)
        rows = len(self.tmpData)
        if rows > 0:
            for row in range(rows):
                grid.InsertStringItem(row, "")
                if self.tmpData[row][0]:
                    grid.CheckItem(row)
                grid.SetStringItem(row, 1, self.tmpData[row][1])
                grid.SetStringItem(row, 2, self.tmpData[row][4])
                next = self.plugin.NextRun(self.tmpData[row][2], self.tmpData[row][3])
                grid.SetStringItem(row, 3, next)
            self.lastRow = 0
            grid.SelRow(0)
            OpenSchedule()
            enableBttns(True)
        else:
            EnableCtrls(False)
            grid.DeleteItem(0)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetSizer(sizer)
        sizer.Layout()
        if self.plugin.pos:
            self.SetPosition(self.plugin.pos)
        else:
            self.Center()
        self.Show(True)


    def EnableAll(self, flag):
        for ix in range(len(self.tmpData)):
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)


    def EnableSchedule(self, schedule, flag):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)


    def DeleteSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                self.grid.DeleteItem(ix)
                self.grid.Refresh()
            self.tmpData.pop(ix)


    def AddSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule[1] in tmpList:
            ix = tmpList.index(schedule[1])
            self.tmpData[ix] = schedule
            if not self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                return
        else:
            ix = len(self.tmpData)
            self.tmpData.append(schedule)
            self.grid.InsertStringItem(ix, "")
        if schedule[0]:
            self.grid.CheckItem(ix)
        elif self.grid.IsChecked(ix):
            self.grid.ToggleItem(ix)
        self.grid.SetStringItem(ix, 1, schedule[1])
        next = self.plugin.NextRun(schedule[2], schedule[3])
        self.grid.SetStringItem(ix, 3, next)
        if self.lastRow == ix:
            evt = wx.PyCommandEvent(newEVT_UPDATE_DIALOG, ix)
            self.GetEventHandler().ProcessEvent(evt)


    def RefreshGrid(self, ix, last, next):
        if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
            self.grid.SetStringItem(ix, 2, last)
            self.grid.SetStringItem(ix, 3, next)


    def onClose(self, evt):
        hwnd = self.GetHandle()
        wp = GetWindowPlacement(hwnd)
        self.plugin.pos = (wp[4][0], wp[4][1])
        #Note: GetPosition() return (-32000, -32000), if window is minimized !!!
        self.Show(False)
        self.plugin.dialog = None
        self.Destroy()
        evt.Skip()
#===============================================================================

class SchedulGhost(eg.PluginBase):

    text = Text
    xmlpath = None
    data = []
    tmpData = []
    dialog = None
    pos = None
    eggTimer = None
    eggTimers = {}
    eggPos = None

    def __init__(self):
        text=Text
        self.AddActionsFromList(Actions)


    def __start__(
        self,
        xmlpath = None,
        logfile = None,
        prefix = "SchedulGhost",
        holidays = [[], []],
        first_day = 0
    ):
        self.holidays = holidays
        self.logfile = logfile
        self.prefix = prefix
        self.first_day = first_day
        self.data = []
        self.tmpData = []
        if xmlpath:
            self.xmlpath = u"%s\\SchedulGhost.xml" % xmlpath
            if os.path.exists(self.xmlpath):
                self.data = self.xmlToData()
            if logfile:
                 self.updateLogFile(self.text.start, True)
            self.UpdateEGscheduler()
        eg.Bind("System.Suspend", self.OnSystemMessage)
        eg.Bind("System.Resume", self.OnSystemMessage)
        eg.Bind("System.SessionLock", self.OnSystemMessage)
        eg.Bind("System.SessionUnlock", self.OnSystemMessage)


    def __stop__(self):
        sched_list = eg.scheduler.__dict__['heap']
        tmpLst = []
        self.updateLogFile(self.text.stop, True)
        for sched in sched_list:
            if sched[1] == self.SchedulGhostScheduleRun:
                tmpLst.append(sched)
        if len(tmpLst) > 0:
            for sched in tmpLst:
                eg.scheduler.CancelTask(sched)
                self.updateLogFile(self.text.canc % sched[2][0])
        self.AbortEggTimers()
        self.dataToXml()
        eg.Unbind("System.Suspend", self.OnSystemMessage)
        eg.Unbind("System.Resume", self.OnSystemMessage)
        eg.Unbind("System.SessionLock", self.OnSystemMessage)
        eg.Unbind("System.SessionUnlock", self.OnSystemMessage)
        if self.dialog:
            self.dialog.Close()
        if self.eggTimer:
            self.eggTimer.Close()


    def Configure(
        self,
        xmlpath = "",
        logfile = "",
        prefix = "SchedulGhost",
        holidays = [[], []],
        first_day = 0
    ):
        panel = eg.ConfigPanel(self)
        panel.holidays = cpy(holidays)
        del holidays
        self.logfile = logfile
        self.first_day = first_day
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        xmlPathCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        xmlPathCtrl.GetTextCtrl().SetEditable(False)
        if xmlpath:
            self.xmlpath = u"%s\\SchedulGhost.xml" % xmlpath
            xmlPathCtrl.GetTextCtrl().ChangeValue(xmlpath)
        else:
            xmlPathCtrl.startDirectory = eg.configDir
        logFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.configDir,
            defaultFile = "Sched_Log.txt"
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logCheckBox = wx.CheckBox(panel, -1, self.text.logLabel)
        defaultPrefLabel = wx.StaticText(panel, -1, self.text.prefLabel)
        firstDayLabel = wx.StaticText(panel, -1, self.text.first_day)
        firstDayCtrl = wx.Choice(
            panel,
            -1,
            choices = (
                day_name[0],
                day_name[6]
            ),
            size = (firstDayLabel.GetSize()[0], -1)
        )
        firstDayCtrl.SetSelection(first_day)
        defaultPrefCtrl  = wx.TextCtrl(panel, -1, prefix)
        panel.holidButton = wx.Button(panel, -1, self.text.holidButton)

        def onHolidButton(evt):
            dlg = HolidaysFrame(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowHolidaysFrame)
            evt.Skip()

        panel.holidButton.Bind(wx.EVT_BUTTON, onHolidButton)
        bottomSizer = wx.FlexGridSizer(2, 5, 2, 2)
        bottomSizer.AddGrowableCol(3)
        val = self.logfile != ""
        logCheckBox.SetValue(val)
        logFileCtrl.Enable(val)
        logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)
        sizerAdd = panel.sizer.Add
        sizerAdd(label2Text, 0, wx.TOP, 15)
        sizerAdd(xmlPathCtrl,0,wx.TOP | wx.EXPAND, 2)
        sizerAdd(logCheckBox, 0, wx.TOP, 15)
        sizerAdd(logFileCtrl, 0, wx.TOP | wx.EXPAND, 2)
        bottomSizer.Add(defaultPrefLabel)
        bottomSizer.Add((10, 1))
        bottomSizer.Add(firstDayLabel)
        bottomSizer.Add((-1, 1), 1, wx.EXPAND)
        bottomSizer.Add((1, 1))
        bottomSizer.Add(defaultPrefCtrl, 0)
        bottomSizer.Add((10, 1))
        bottomSizer.Add(firstDayCtrl,0)
        bottomSizer.Add((-1, 1), 1, wx.EXPAND)
        bottomSizer.Add(panel.holidButton, 0, wx.TOP | wx.ALIGN_RIGHT, -2)
        sizerAdd(bottomSizer, 0, wx.TOP | wx.EXPAND, 15)

        def Validation():
            flag1 = os.path.exists(xmlPathCtrl.GetValue())
            flag2 = False
            if not logCheckBox.IsChecked():
                flag2 = True
            else:
                logFile = logFileCtrl.GetTextCtrl().GetValue()
                egLog = u"%s\\Log.txt" % unicode(eg.configDir)
                if logFile.lower() == egLog.lower():
                    PlaySound('SystemExclamation', SND_ASYNC)
                    MessageBox(
                        panel.GetHandle(),
                        self.text.mess % unicode(eg.configDir),
                        "SchedulGhost",
                        48
                        )
                elif logFile != "":
                    flag2 = True
            flag3 = defaultPrefCtrl.GetValue() != ""
            flag = flag1 and flag2 and flag3
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)


        def onXmlPathChange(event):
            xmlpath = xmlPathCtrl.GetValue()
            if xmlpath:
                self.xmlpath = u"%s\\SchedulGhost.xml" % xmlpath
            Validation()
            event.Skip()
        xmlPathCtrl.Bind(wx.EVT_TEXT, onXmlPathChange)


        def logFileChange(event):
            self.logfile = logFileCtrl.GetTextCtrl().GetValue()
            Validation()
            event.Skip()
        logFileCtrl.Bind(wx.EVT_TEXT, logFileChange)


        def ontPrefCtrl(event):
            Validation()
            event.Skip()
        defaultPrefCtrl.Bind(wx.EVT_TEXT, ontPrefCtrl)


        def onLogCheckBox(evt):
            val = evt.IsChecked()
            logFileCtrl.Enable(val)
            if not val:
                logFileCtrl.SetValue("")
            else:
                Validation()
            evt.Skip()

        logCheckBox.Bind(wx.EVT_CHECKBOX, onLogCheckBox)
        Validation()       
        while panel.Affirmed():
            panel.SetResult(
                xmlPathCtrl.GetValue(),
                logFileCtrl.GetTextCtrl().GetValue(),
                defaultPrefCtrl.GetValue(),
                panel.holidays,
                firstDayCtrl.GetSelection()
            )


    def NextRun(self, type, data):

        def FindRunDateTime(runList, cond):
            runList.sort()
            runDateTime = ""
            if len(runList) > 0:
                if not cond:
                    return runList[0]
                found = False
                for item in runList:
                    if item.weekday() > 4:
                        found = True
                        break
                    else:
                        if (item.month, item.day) in self.holidays[0]:
                            pass
                        elif (item.year, item.month, item.day) in self.holidays[1]:
                            pass
                        else:
                            found = True
                            break
                if found:
                    runDateTime = item
            return runDateTime

        now = dt.now()
        now = now.replace(microsecond = 999999)

        for i in range(5):
            if i>0:
                print "Retry nbr: ", i
                try:
                    runTime = dt.strptime(data[0], "%H:%M:%S").time()
                    break
                except ImportError:
                    print "ImportError, trying again..."
                    sleep(0.2)

        if type == 0: # once or yearly
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif not data[3]:
                return ""
            else:
                if runDateTime.replace(year = now.year) < now:
                    return str(runDateTime.replace(year = now.year + 1))
                else:
                    return str(runDateTime.replace(year = now.year))
        elif type == 1: # daily
            runDateTime = dt.combine(now.date(), runTime)
            if now.time() > runTime:
                runDateTime += td(days = 1)
            return str(runDateTime)
        elif type == 2: # weekly
            if not data[2]:
                return ""
            runDateTime = dt.combine(now.date(), runTime)
            weekdaysLower = []
            weekdaysLarger = []
            nowDay = now.weekday()
            for weekday in range(7):
                if 2**weekday & data[2]:
                    if weekday < nowDay or (weekday == nowDay and now.time() > runTime):
                        weekdaysLower.append(weekday)
                    else:
                        weekdaysLarger.append(weekday)
            if not data[4] and not data[3]: # without holiday check
                if len(weekdaysLarger) > 0:
                    delta = weekdaysLarger[0] - nowDay
                    return str(runDateTime + td(days = delta))
                delta = 7 + weekdaysLower[0] - nowDay
                return str(runDateTime + td(days = delta))
            elif data[4]: # holiday check
                found = False
                shift = 0
                while True:
                    for day in weekdaysLarger:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                    shift += 7
                    for day in weekdaysLower:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                return str(tmpRunDT)
            else: # holiday_2 check
                if len(weekdaysLarger) > 0:
                    Delta = weekdaysLarger[0] - nowDay
                else:
                    Delta = 7 + weekdaysLower[0] - nowDay
                start = 0 if now.time() < runTime else 1
                found = False
                for delta in range(start, Delta):
                    tmpRunDT = runDateTime + td(days = delta)
                    if tmpRunDT.weekday() < 5:
                        if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                            found = True
                            break
                        elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                            found = True
                            break
                return str(tmpRunDT if found else runDateTime + td(days = Delta))
        elif type == 3: # monthly/weekday
            if data[2] == 0 or data[3] == 0 or (data[4] + data[5]) == 0:
                return ""
            currMonth = now.month
            currYear = now.year
            monthsInt = data[4] + (data[5] << 6)
            months = []
            for month in range(1,13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                runList = []
                for ix in range(6):
                    if 2 ** ix & data[2]:
                        for weekday in range(7):
                            if 2 ** weekday & data[3]:
                                day = FindMonthDay(currYear, currMonth, weekday, ix)
                                if day:
                                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                                    if now < runDateTime:
                                        runList.append(runDateTime)
                tmpRunDT = FindRunDateTime(runList, data[6])
                if tmpRunDT:
                    return str(tmpRunDT)
            lower = []
            larger = []
            for month in months:
                if month > currMonth:
                    larger.append(month)
                else: #month <= currMonth:
                    lower.append(month)
            year = currYear
            tmpRunDT = None
            while True:
                for month in larger:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day = FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
                year += 1
                for month in lower:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day=FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
            return str(tmpRunDT)
        elif type == 4: #monthly/day
            if (data[2] + data[3] + data[4] + data[5]) == 0 or (data[6] + data[7]) == 0:
                return ""
            runList = []
            currMonth = now.month
            currYear = now.year
            monthsInt = data[6] + (data[7] << 6)
            daysInt = data[2] + (data[3] << 8) + (data[4] << 16) + (data[5] << 24)
            days = []
            for day in range(1, 32):
                if 2 ** (day - 1) & daysInt:
                    days.append(day)
            months = []
            for month in range(1, 13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                for day in days:
                    if day > monthrange(currYear, currMonth)[1]:
                        break
                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                    if now < runDateTime:
                        runList.append(runDateTime)
            if len(runList) == 0:
                lower = []
                larger = []
                nextMonth = None
                for month in months:
                    if month > currMonth:
                        larger.append(month)
                    else: #month<=currMonth:
                        lower.append(month)
                if len(larger) > 0:
                    nextYear = currYear
                    for month in larger:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
                if len(runList) == 0 and len(lower) > 0:
                    nextYear = currYear + 1
                    for month in lower:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
            if len(runList) > 0:
                return str(min(runList))
            else:
                return ""
        else: # 5 = periodically
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif data[4] < 3: #unit =  second, minute, hour
                period = data[3] * (1, 60, 3600)[data[4]]
                if period < 86400 and not 86400 % period:
                    if now.time() > runTime:
                        date = now.date()
                    else:
                        date = now.date() - td(days = 1)
                    runDateTime = dt.combine(date, runTime)
                delta = now - runDateTime
                delta = delta.seconds + 86400 * delta.days
                share = delta / period
                share += 1
                delta = td(seconds = share * period)
                return str(runDateTime + delta)
            elif data[4] == 3 or data[4] == 4: #unit = day or week
                period = data[3] if data[4] == 3 else 7 * data[3]
                delta = (now - runDateTime).days
                share = delta / period
                if not delta % period:
                    if now.time() < runTime:
                        return str(dt.combine(now.date(), runTime))
                share += 1
                delta = td(days = share * period)
                return str(runDateTime + delta)
            elif data[4] == 5: #unit = month
                period = data[3]
                month = runDateTime.month
                year = runDateTime.year
                while now > runDateTime:
                    year += period / 12
                    m = month+period % 12
                    if m > 12:
                        year += 1
                        month = m % 12
                    else:
                        month = m
                    runDateTime = runDateTime.replace(year = year).replace(month = month)
                return str(runDateTime)
            else: # data[4] == 6: #unit = year
                period = data[3]
                year = runDateTime.year
                while now > runDateTime:
                    year += period
                    runDateTime = runDateTime.replace(year = year)
                return str(runDateTime)


    def updateLogFile(self, line, blank = False):
        if not self.logfile:
            return
        f = openFile(self.logfile, encoding = 'utf-8', mode = 'a')
        if blank:
            f.write("\r\n")
        f.write("%s  %s\r\n" % (str(dt.now())[:19], line))
        f.close()


    def OnSystemMessage(self, event):
        self.updateLogFile(self.text.__dict__[event.suffix], True)


    def Execute(self, params, stopEvent, ticks):
        if not stopEvent:
            span = params[3][1]
            if span != "00:00:00":
                stopTicks = ticks + int(span[6:]) + 60 * int(span[3:5]) + 3600 * int(span[:2])
                eg.scheduler.AddTaskAbsolute(
                    stopTicks,
                    self.SchedulGhostScheduleRun,
                    params[1],
                    True
                )
            next = self.NextRun(params[2], params[3])
            if next: # new schedule, if valid next run time
                startTicks = mktime(strptime(next, "%Y-%m-%d %H:%M:%S"))
                eg.scheduler.AddTaskAbsolute(
                    startTicks,
                    self.SchedulGhostScheduleRun,
                    params[1],
                    False,
                    startTicks
                )
            suffix = params[6]
        else:
            suffix = params[7]
            next = ""
        if params[8]:
            payload = next if params[8] == "{Next run}" else eg.ParseString(params[8])
            eg.TriggerEvent(
                eg.ParseString(suffix),
                prefix = eg.ParseString(params[5]),
                payload = payload
            )
        else:
            eg.TriggerEvent(
                eg.ParseString(suffix),
                prefix = eg.ParseString(params[5])
            )
        return next


    def SchedulGhostScheduleRun(self, schedule, stopEvent, ticks = 0):
        data = self.data
        ix = [item[1] for item in data].index(schedule)
        next = self.Execute(data[ix], stopEvent, ticks)
        if stopEvent:
            self.updateLogFile(self.text.execStop % data[ix][1])            
        else:
            last = str(dt.now())[:19]
            self.data[ix][4] = last
            if self.dialog:
                tmpList = [item[1] for item in self.tmpData]
                if schedule in tmpList:
                    ixTmp = tmpList.index(schedule)
                    self.tmpData[ixTmp][4] = last
                self.dialog.RefreshGrid(ixTmp, last, next)
            nxt = next[:19] if next else self.text.none        
            self.updateLogFile(self.text.execut % (data[ix][1], nxt))


    def UpdateEGscheduler(self):
        data = self.data
        tmpList = []
        sched_list = eg.scheduler.__dict__['heap']
        for sched in sched_list:
            if sched[1] == self.SchedulGhostScheduleRun:
                if sched[2][0] in [item[1] for item in data]:
                    tmpList.append(sched)
                else:
                    self.updateLogFile(self.text.cancAndDel % sched[2][0])
                    eg.scheduler.CancelTask(sched)
        sched_list = tmpList
        for schedule in data:
            startMoment = self.NextRun(schedule[2], schedule[3])
            if not startMoment:
                continue
            startTicks = mktime(strptime(startMoment, "%Y-%m-%d %H:%M:%S"))
            nameList = [item[2][0] for item in sched_list]
            if schedule[1] in nameList:
                sched = sched_list[nameList.index(schedule[1])]
                if not schedule[0]: # schedule is disabled !
                    eg.scheduler.CancelTask(sched)
                    self.updateLogFile(self.text.cancAndDis % schedule[1])
                elif not sched[2][1] and sched[0] != startTicks:
                    self.updateLogFile(self.text.re_Sched % (schedule[1], startMoment))
                    eg.scheduler.CancelTask(sched)
                    eg.scheduler.AddTaskAbsolute(
                        startTicks,
                        self.SchedulGhostScheduleRun, 
                        schedule[1],
                        False,
                        startTicks
                    )
            elif schedule[0]:
                    eg.scheduler.AddTaskAbsolute(
                        startTicks,
                        self.SchedulGhostScheduleRun,
                        schedule[1],
                        False,
                        startTicks
                    )
                    self.updateLogFile(self.text.newSched % (schedule[1], startMoment))


    def dataToXml(self):
        data = self.data
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Document', None)
        root = dom.documentElement
        commentNode = dom.createComment(self.text.xmlComment % str(dt.now())[:19])
        dom.insertBefore(commentNode, root)
        for item in data:
            schedNode = dom.createElement(u'Schedule')
            schedNode.setAttribute(u'Name', unicode(item[1]))
            schedNode.setAttribute(u'Type', unicode(item[2]))
            enableNode = dom.createElement(u'Enable')
            enableText = dom.createTextNode(unicode(item[0]))
            enableNode.appendChild(enableText)
            schedNode.appendChild(enableNode)
            last_runNode = dom.createElement(u'Last_run')
            last_runText = dom.createTextNode(unicode(item[4]))
            last_runNode.appendChild(last_runText)
            schedNode.appendChild(last_runNode)
            prefixNode = dom.createElement(u'Prefix')
            prefixText = dom.createTextNode(unicode(item[5]))
            prefixNode.appendChild(prefixText)
            schedNode.appendChild(prefixNode)
            startNode = dom.createElement(u'Start')
            startText = dom.createTextNode(unicode(item[6]))
            startNode.appendChild(startText)
            schedNode.appendChild(startNode)
            stopNode = dom.createElement(u'Stop')
            stopText = dom.createTextNode(unicode(item[7]))
            stopNode.appendChild(stopText)
            schedNode.appendChild(stopNode)
            payloadNode = dom.createElement(u'Payload')
            payloadText = dom.createTextNode(unicode(item[8]))
            payloadNode.appendChild(payloadText)
            schedNode.appendChild(payloadNode)
            dateTimeNode = dom.createElement(u'Datetime')
            start_timeNode = dom.createElement(u'Start_time')
            start_timeText = dom.createTextNode(unicode(item[3][0]))
            start_timeNode.appendChild(start_timeText)
            dateTimeNode.appendChild(start_timeNode)
            durationNode = dom.createElement(u'Duration')
            durationText = dom.createTextNode(unicode(item[3][1]))
            durationNode.appendChild(durationText)
            dateTimeNode.appendChild(durationNode)
            if item[2] == 0:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                yearlyNode = dom.createElement(u'Yearly')
                yearlyText = dom.createTextNode(unicode(item[3][3]))
                yearlyNode.appendChild(yearlyText)
                dateTimeNode.appendChild(yearlyNode)
            if item[2] == 2:
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][2]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][4]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
                holiday2Node = dom.createElement(u'HolidayCheck_2')
                holiday2Text = dom.createTextNode(unicode(item[3][3]))
                holiday2Node.appendChild(holiday2Text)
                dateTimeNode.appendChild(holiday2Node)
            if item[2] == 3:
                orderNode = dom.createElement(u'Order')
                orderText = dom.createTextNode(unicode(item[3][2]))
                orderNode.appendChild(orderText)
                dateTimeNode.appendChild(orderNode)
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][3]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][4]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][5]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][6]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
            if item[2] == 4:
                q_1_Node = dom.createElement(u'Q_1')
                q_1_Text = dom.createTextNode(unicode(item[3][2]))
                q_1_Node.appendChild(q_1_Text)
                dateTimeNode.appendChild(q_1_Node)
                q_2_Node = dom.createElement(u'Q_2')
                q_2_Text = dom.createTextNode(unicode(item[3][3]))
                q_2_Node.appendChild(q_2_Text)
                dateTimeNode.appendChild(q_2_Node)
                q_3_Node = dom.createElement(u'Q_3')
                q_3_Text = dom.createTextNode(unicode(item[3][4]))
                q_3_Node.appendChild(q_3_Text)
                dateTimeNode.appendChild(q_3_Node)
                q_4_Node = dom.createElement(u'Q_4')
                q_4_Text = dom.createTextNode(unicode(item[3][5]))
                q_4_Node.appendChild(q_4_Text)
                dateTimeNode.appendChild(q_4_Node)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][6]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][7]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
            if item[2] == 5:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                numberNode = dom.createElement(u'Number')
                numberText = dom.createTextNode(unicode(item[3][3]))
                numberNode.appendChild(numberText)
                dateTimeNode.appendChild(numberNode)
                unitNode = dom.createElement(u'Unit')
                unitText = dom.createTextNode(unicode(item[3][4]))
                unitNode.appendChild(unitText)
                dateTimeNode.appendChild(unitNode)
            schedNode.appendChild(dateTimeNode)
            root.appendChild(schedNode)
        f = file(self.xmlpath, 'wb')
        writer = lookup('utf-8')[3](f)
        dom.writexml(writer, encoding = 'utf-8')
        f.close()


    def xmlToData(self):
        data = []
        xmlfile = self.xmlpath
        xmldoc = miniDom.parse(xmlfile)
        document = xmldoc.getElementsByTagName('Document')[0]
        schedules = document.getElementsByTagName('Schedule')
        for schedule in schedules:
            dataItem = []
            enable = int(schedule.getElementsByTagName('Enable')[0].firstChild.data)
            dataItem.append(enable)
            name = schedule.attributes["Name"].value
            dataItem.append(name)
            type = int(schedule.attributes["Type"].value)
            dataItem.append(type)
            dateTime = schedule.getElementsByTagName('Datetime')[0]
            params = []
            start_time = dateTime.getElementsByTagName('Start_time')[0].firstChild.data
            params.append(start_time)
            duration = dateTime.getElementsByTagName('Duration')[0].firstChild.data
            params.append(duration)
            if type == 0:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                date = int(dateTime.getElementsByTagName('Yearly')[0].firstChild.data)
                params.append(date)
            if type == 2:
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                holiday2 = int(dateTime.getElementsByTagName('HolidayCheck_2')[0].firstChild.data)
                params.append(holiday2)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if type == 3:
                order = int(dateTime.getElementsByTagName('Order')[0].firstChild.data)
                params.append(order)
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if type == 4:
                q_1 = int(dateTime.getElementsByTagName('Q_1')[0].firstChild.data)
                params.append(q_1)
                q_2 = int(dateTime.getElementsByTagName('Q_2')[0].firstChild.data)
                params.append(q_2)
                q_3 = int(dateTime.getElementsByTagName('Q_3')[0].firstChild.data)
                params.append(q_3)
                q_4 = int(dateTime.getElementsByTagName('Q_4')[0].firstChild.data)
                params.append(q_4)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
            if type == 5:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                number = int(dateTime.getElementsByTagName('Number')[0].firstChild.data)
                params.append(number)
                unit = int(dateTime.getElementsByTagName('Unit')[0].firstChild.data)
                params.append(unit)
            dataItem.append(params)
            last_run = schedule.getElementsByTagName('Last_run')[0].firstChild
            last_run = last_run.data if last_run else ""
            dataItem.append(last_run)
            prefix = schedule.getElementsByTagName('Prefix')[0].firstChild
            prefix = prefix.data if prefix else ""
            dataItem.append(prefix)
            start = schedule.getElementsByTagName('Start')[0].firstChild
            start = start.data if start else ""
            dataItem.append(start)
            stop = schedule.getElementsByTagName('Stop')[0].firstChild
            stop = stop.data if stop else ""
            dataItem.append(stop)
            payload = schedule.getElementsByTagName('Payload')[0].firstChild
            payload = payload.data if payload else ""
            dataItem.append(payload)
            data.append(dataItem)
        return data


    def SchedulGhost_EggFunction(self, key):
        args = self.eggTimers[key]
        now = mktime(localtime())
        delta = Ticks2Delta(key, now)
        self.updateLogFile(self.text.eggElaps % (args[1], args[2], delta))
        eg.TriggerEvent(args[2], prefix = args[1])
        if len(args[4]) > 0:
            wx.CallAfter(
                PopupText,
                None,
                self,
                args[4:],
                None
            )
        if len(args[3]) > 0:
            sound = wx.Sound(args[3])
            if os.path.isfile(args[3]) and sound.IsOk():
                sound.Play(wx.SOUND_ASYNC)
            else:
                self.PrintError(self.text.soundProblem % args[3])
                PlaySound('SystemExclamation', SND_ASYNC)
        del self.eggTimers[key]


    def AddEggTimer(self, val, args):
        self.updateLogFile(self.text.eggStart % (args[1], args[2], val))
        val =  int(val[6:]) + 60 * int(val[3:5]) + 3600 * int(val[:2])
        now = mktime(localtime())
        self.eggTimers[now] = args
        eg.scheduler.AddTask(val, self.SchedulGhost_EggFunction, now)


    def AbortEggTimers(self):
        egg_list = eg.scheduler.__dict__['heap']
        tmpLst = []
        for egg in egg_list:
            if egg[1] == self.SchedulGhost_EggFunction:
                tmpLst.append(egg)
        if len(tmpLst) > 0:
            for egg in tmpLst:
                args = self.eggTimers[egg[2][0]]
                delta = Ticks2Delta(egg[2][0], egg[0])
                self.updateLogFile(self.text.eggCancel % (args[1], args[2], delta))
                eg.scheduler.CancelTask(egg)
#===============================================================================
#cls types for Actions list:
#===============================================================================

class ShowSchedulGhost(eg.ActionBase):

    class text:
        dialogTitle = "SchedulGhost"
        header = (
            "Enabled",
            "Schedule title",
            "Last run",
            "Next run",
        )
        sched_type = (
            "Only once (or yearly)",
            "Daily",
            "Weekly",
            "Monthly / weekday",
            "Monthly / day",
            "Periodically",
        )
        serial_num = (
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "last"
        )
        the = "The"
        in_ = "in"
        buttons = (
            "Add new",
            "Duplicate",
            "Delete",
            "OK",
            "Cancel",
            "Apply"
        )
        type_label = "Schedule type:"
        chooseDay = "Choose day"
        theEvery = "The every"
        yearly = "Every year on the same day"
        chooseTime = "Choose start event time and span"
        choosePeriod = "Choose period"
        andThenEvery = "And then every"
        units = (
            "seconds",
            "minutes",
            "hours",
            "days",
            "weeks",
            "months",
            "years",
        )
        start = "Start event time:"
        length = "Span (00:00:00 = only start event):"
        boxTitle = "Your setup is wrong !"
        boxTexts = (
            "Schedule title must not be an empty string !",
            "Schedule title must be unique !",
            'Must be chosen Schedule type !',
            'Event prefix must not be an empty string !',
            "Period can not be shorter than the span !",
        )
        testButton = "Test now"
        testRun = 'Schedule "%s" - TEST execution. Possible next time: %s'
        evtPrefix = "Event prefix:"
        evtPayload = "Event payload:"
        startSuffix = "Start event suffix:"
        stopSuffix = "Stop event suffix:"
        holidCheck_1 = "If some marked work day falls on holiday, it's like when he is not marked"
        holidCheck_2 = "If some not-marked work day falls on holiday, it's like when he is marked"

    def __call__(self):
        if not self.plugin.dialog:
            wx.CallAfter(schedulerDialog, self.text, self.plugin)
        else:
            wx.CallAfter(self.plugin.dialog.Raise)
#===============================================================================

class HideSchedulGhost(eg.ActionBase):

    def __call__(self):
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.Close)
#===============================================================================

class EnableSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            if self.value > -1:
                data[ix][0] = self.value
                self.plugin.UpdateEGscheduler()
                if self.plugin.dialog:
                    wx.CallAfter(self.plugin.dialog.EnableSchedule, schedule, self.value)
            return data[tmpLst.index(schedule)]
        else:
            self.PrintError(self.text.notFound % schedule)
            return self.text.notFound % schedule


    def Configure(self, schedule = ""):
        panel = eg.ConfigPanel()
        data = self.plugin.data
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300, -1), choices = choices)
        panel.sizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.scheduleTitle
            ),
            0,
            wx.LEFT | wx.TOP,
            10
        )
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class EnableAll(eg.ActionBase):

    def __call__(self):
        data = self.plugin.data
        for schedule in data:
            schedule[0] = self.value
        self.plugin.UpdateEGscheduler()
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.EnableAll, self.value)
#===============================================================================

class DeleteSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            data.pop(ix)
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.DeleteSchedule, schedule)
        else:
            self.PrintError(self.text.notFound % schedule)
            return self.text.notFound % schedule


    def Configure(self, schedule = ""):
        panel = eg.ConfigPanel()
        data = self.plugin.data
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300, -1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.scheduleTitle), 0, wx.LEFT | wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class AddSchedule(eg.ActionBase):

    class text:
        python_expr = "Python expression:"
        descr = u'''<rst>**Add schedule**.

In the edit box, enter a python expression with the parameters of the plan.
This may be for example *eg.result*, *eg.event.payload* or the entire list
(in the same format, what you get as a result of actions **"GetSchedule"**).

This action works in two ways (depending on the title of the schedule):

1. If the schedule with the same title already exists, its parameters are overwritten by new ones.
2. If the title does not exist yet, the schedule is added to the list as new.'''

    def __call__(self, expr = ""):
        schedule = eg.ParseString(expr)
        schedule = eval(schedule)
        if len(schedule) == 9 and isinstance(schedule[1], unicode):
            data = self.plugin.data
            tmpLst = [item[1] for item in data]
            if schedule[1] in tmpLst:
                data[tmpLst.index(schedule[1])] = schedule
            else:
                data.append(schedule)
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.AddSchedule, schedule)


    def Configure(self, expr = ""):
        panel = eg.ConfigPanel(resizable = True)
        textControl = wx.TextCtrl(panel, -1, expr, size = (300,-1), style = wx.TE_MULTILINE )
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.python_expr), 0,wx.LEFT | wx.TOP, 10)
        panel.sizer.Add(textControl, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class PopupText(wx.Frame):

    def __init__(
        self,
        parent,
        plugin,
        args,
        panel
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            '',
            size = (120, 60),
            style = wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        self.delta = (0,0)
        self.args = args
        self.panel = panel
        self.SetTitle(plugin.text.popupTitle)
        label = self.label = wx.StaticText(self, -1, "")
        if panel:
            panel.popupFrame = self
            tip = plugin.text.popupTip2
        else:
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            label.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            tip = plugin.text.popupTip1 % str(dt.now())[:19]
        label.SetToolTipString(tip)
        self.SetColor(fore = self.args[2], back = self.args[1])
        self.UpdateText(txt = self.args[0], font = wx.FontFromNativeInfoString(self.args[3]))
        self.SetPosition(self.args[4])
        self.Show(True)
        BringWindowToTop(self.GetHandle())
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)      
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        label.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        label.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)        
        label.Bind(wx.EVT_MOTION, self.OnMouseMove)        


    def OnCloseWindow(self, event):
        self.Destroy()
        event.Skip()


    def OnRightClick(self, evt):
        self.Show(False)
        self.Close()


    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            if self.panel:
                self.panel.SetIsDirty(True)


    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)


    def UpdateText(self, txt = None, font = None):
        border = 10
        if font:
            self.label.SetFont(font)
        if txt is not None:
            self.label.SetLabel(txt)
        sz = self.label.GetSize()
        self.SetClientSize((border + sz[0], border + sz[1]))
        self.label.SetPosition((border / 2, border / 2))


    def SetColor(self, fore = None, back = None):
        if back:
            self.SetBackgroundColour(back)
        if fore:
            self.label.SetForegroundColour(fore)
        self.Refresh()
#===============================================================================

class EggTimerFrame(wx.Frame):

    def __init__(self, text, plugin, args):
        self.plugin = plugin
        wx.Frame.__init__(
            self,
            None,
            -1,
            args[4] if args[4] else text.title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.TAB_TRAVERSAL ,
            name = text.title
        )
        self.plugin.eggTimer = self
        self.text = text
        self.args = args
        self.val = args[0]
        self.SetBackgroundColour(wx.NullColour)
        durLabel = wx.StaticText(self, -1, text.timeLbl)
        initTime = wx.DateTime_Now()
        initTime.SetSecond(0)
        initTime.AddTS(wx.TimeSpan.Minute())
        timeCtrl = MyTimeCtrl(self, -1, self.val, fmt24hr = True, style = wx.BORDER_SUNKEN)
        fnt = timeCtrl.GetFont()
        fnt.SetPointSize(4 * fnt.GetPointSize())
        timeCtrl.SetFont(fnt)
        h = timeCtrl.GetSize()[1]
        spinBtn = wx.SpinButton(self, -1, (-1, -1), (h / 2, h), wx.SP_VERTICAL)
        timeCtrl.BindSpinButton(spinBtn)
        self.startBtn = wx.Button(self, -1, text.startBtn)
        self.startBtn.SetDefault()
        fnt = self.startBtn.GetFont()
        fnt.SetPointSize(2 * fnt.GetPointSize())
        self.startBtn.SetFont(fnt)
        mainSizer = wx.GridBagSizer(2, 2)
        mainSizer.Add(durLabel, (0, 0))
        mainSizer.Add(timeCtrl, (1, 0))
        mainSizer.Add(spinBtn, (1, 1))
        mainSizer.Add((-1, 1), (2, 0))
        mainSizer.Add(self.startBtn, (3, 0), (1,2), flag = wx.EXPAND)
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(mainSizer, 0, wx.ALL, 5)
        self.SetSizer(Sizer)
        Sizer.Layout()
        self.SetClientSize(Sizer.GetMinSize())
        if self.plugin.eggPos:
            self.SetPosition(self.plugin.eggPos)
        else:
            self.Center()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.startBtn.Bind(wx.EVT_BUTTON, self.onStart)
        timeCtrl.Bind(maskedlib.EVT_TIMEUPDATE, self.OnTimeChange)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        self.MakeModal(True)
        self.Show(True)
        self.startBtn.Show(self.val != "00:00:00")
        timeCtrl.SetSelection(3, 5)


    def onFrameCharHook(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            evt.Skip()


    def OnTimeChange(self, evt):
        self.val = evt.GetValue()
        self.startBtn.Show(self.val != "00:00:00")
        evt.Skip()


    def onStart(self, evt):
        self.plugin.AddEggTimer(self.val, self.args)
        self.Close()
        evt.Skip()
 

    def onClose(self, evt):
        self.MakeModal(False)
        self.plugin.eggPos = self.GetPosition()
        self.Show(False)
        self.plugin.eggTimer = None
        self.Destroy()
        evt.Skip()
#===============================================================================

class SetEggTimer(eg.ActionBase):

    class text:
        title = "SchedulGhost - egg timer"
        timeLbl = "Set time to elapse (HH:MM:SS):"
        prefLbl = "Event prefix:"
        suffLbl = "Event suffix:"
        wavLbl = "Play this wav file:"
        popLbl = "Show pop-up window with this text:"
        foreColour = 'Text colour'
        backColour = 'Background colour'
        fontBtn = "Pop-up font:"
        startBtn = "Start now"
        toolTipFile = "Press button and browse to select wav file ..."
        browseFile = 'Select the wav file'
        playWav = "Wav file test"
        defaultPopup = "Wake up, eggs are cooked !!!"
        defaultTime = ("Default time:", "Time to elapse:")
        treeLabel = "%s: %s.%s: %s"

    def __call__(self, args = [
        "00:03:00",
        "SchedulGhost",
        "EggTimer",
        "",
        "",
        (191, 191, 255),
        (64, 0, 128),
        "",
        (10, 10)
    ]):
        if self.value:
            self.plugin.AddEggTimer(args[0], args)         
        else:
            if not self.plugin.eggTimer:
                wx.CallAfter(EggTimerFrame, self.text, self.plugin, args)


    def GetLabel(self, args):
        return self.text.treeLabel % (self.name, args[1], args[2], args[4])


    def Configure(self, args = [
        "00:03:00",
        "SchedulGhost",
        "EggTimer",
        "",
        "",
        (191, 191, 255),
        (64, 0, 128),
        "",
        (10, 10)
    ]):
        panel = self.panel = eg.ConfigPanel()
        self.panel.popupFrame = None
        if not args[1]:
            args[1] = self.plugin.prefix
        spinBtn = wx.SpinButton(
            panel,
            -1,
            wx.DefaultPosition,
            (-1, 22),
            wx.SP_VERTICAL
        )
        defTime = MyTimeCtrl(
            panel,
            -1,
            args[0],
            fmt24hr = True,
            spinButton = spinBtn
        )
        defTime.SetFocus()
        defTime.SetSelection(3, 5)
        prefCtrl = wx.TextCtrl(panel, -1, args[1], size = (100, -1))
        suffCtrl = wx.TextCtrl(panel, -1, args[2], size = (100, -1))
        topSizer = wx.GridBagSizer(1,1)
        topSizer.AddGrowableCol(2,1)
        topSizer.AddGrowableCol(4,1)
        topSizer.Add(wx.StaticText(panel, -1, self.text.defaultTime[self.value]), (0, 0),(1,3))
        topSizer.Add(wx.StaticText(panel, -1, self.text.prefLbl), (0, 3),(1,2))
        topSizer.Add(wx.StaticText(panel, -1, self.text.suffLbl), (0, 5))
        topSizer.Add(defTime, (1, 0))
        topSizer.Add(spinBtn, (1, 1))
        topSizer.Add(prefCtrl, (1, 3))
        topSizer.Add(suffCtrl, (1, 5))
        sizerAdd = panel.sizer.Add
        sizerAdd(topSizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        sizerAdd((-1,10))
        wavCheckBox = wx.CheckBox(panel, -1, self.text.wavLbl)
        sizerAdd(wavCheckBox, 0, wx.LEFT| wx.TOP, 10)
        wavFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Music,
            fileMask = "*.wav",
        )
        wavFileCtrl.GetTextCtrl().SetEditable(False)
        wavFileCtrl.GetTextCtrl().SetValue(args[3])
        flg = len(args[3]) != 0
        wavCheckBox.SetValue(flg)
        wavFileCtrl.Enable(flg)
        panel.dialog.buttonRow.testButton.SetLabel(self.text.playWav)
        panel.dialog.buttonRow.testButton.Enable(flg)
        sizerAdd(wavFileCtrl, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        popCheckBox = wx.CheckBox(panel, -1, self.text.popLbl)
        popTxtCtrl = wx.TextCtrl(panel, -1, args[4])
        backColorLbl = wx.StaticText(panel, -1, self.text.backColour + ":")
        foreColorLbl = wx.StaticText(panel, -1, self.text.foreColour + ":")
        fontLbl = wx.StaticText(panel, -1, self.text.fontBtn)
        backColorBtn = extColourSelectButton(
            panel,
            args[5],
            title = self.text.backColour
        )
        foreColorBtn = extColourSelectButton(
            panel,
            args[6],
            title = self.text.foreColour
        )
        fontInfo = args[7]
        if fontInfo == "":
            font = fontLbl.GetFont()
            font.SetPointSize(42)
            fontInfo = font.GetNativeFontInfoDesc()
        fontBtn = extFontSelectButton(panel, value = fontInfo)
        popSizer = wx.FlexGridSizer(2,5,0,0)
        popSizer.AddGrowableCol(1,1)
        popSizer.AddGrowableCol(3,1)
        popSizer.Add(fontLbl)
        popSizer.Add((-1,1))
        popSizer.Add(foreColorLbl)
        popSizer.Add((-1,1))
        popSizer.Add(backColorLbl)
        popSizer.Add(fontBtn)
        popSizer.Add((-1,1))
        popSizer.Add(foreColorBtn)
        popSizer.Add((-1,1))
        popSizer.Add(backColorBtn)
        sizerAdd((-1,8))
        sizerAdd(popCheckBox, 0, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        sizerAdd((-1,1))
        sizerAdd(popTxtCtrl, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizerAdd((-1,8))
        sizerAdd(popSizer, 0, wx.EXPAND |wx.LEFT| wx.RIGHT, 10)
        panel.sizer.Layout()

        def EnablePopUp(enable):
            popTxtCtrl.Enable(enable)
            fontLbl.Enable(enable)
            fontBtn.Enable(enable)
            foreColorLbl.Enable(enable)
            foreColorBtn.Enable(enable)
            backColorLbl.Enable(enable)
            backColorBtn.Enable(enable)

        val = len(args[4]) != 0
        popCheckBox.SetValue(val)
        EnablePopUp(val)
        if val:
            wx.CallAfter(
                PopupText,
                None,
                self.plugin,
                args[4:],
                self.panel,
            )

        def onPopCheckBox(evt):
            val = evt.IsChecked()
            EnablePopUp(val)
            if val:
                popTxtCtrl.ChangeValue(self.text.defaultPopup)
                wx.CallAfter(
                    PopupText,
                    None,
                    self.plugin,
                    (   popTxtCtrl.GetValue(),
                        backColorBtn.GetValue(),
                        foreColorBtn.GetValue(),
                        fontBtn.GetValue(),
                        args[8]),
                    self.panel,
                )
            else:
                popTxtCtrl.ChangeValue("")
                self.panel.popupFrame.Close()
            evt.Skip()
        popCheckBox.Bind(wx.EVT_CHECKBOX, onPopCheckBox)


        def OnPopTxtChange(evt):
            if self.panel.popupFrame:
                self.panel.popupFrame.UpdateText(txt = evt.GetString())
            evt.Skip()
        popTxtCtrl.Bind(wx.EVT_TEXT, OnPopTxtChange)


        def onWavCheckBox(evt):
            val = evt.IsChecked()
            wavFileCtrl.Enable(val)
            if not val:
                wavFileCtrl.GetTextCtrl().ChangeValue("")
                panel.dialog.buttonRow.testButton.Enable(False)
            evt.Skip()
        wavCheckBox.Bind(wx.EVT_CHECKBOX, onWavCheckBox)
        

        def OnWavFile(evt):
            val = evt.GetString() != ""
            panel.dialog.buttonRow.testButton.Enable(val)
            evt.Skip()
        wavFileCtrl.Bind(wx.EVT_TEXT, OnWavFile)


        def OnFontBtn(evt):
            if self.panel.popupFrame:
                font = wx.FontFromNativeInfoString(evt.GetValue())
                self.panel.popupFrame.UpdateText(font = font)
            evt.Skip()
        fontBtn.Bind(EVT_BUTTON_AFTER, OnFontBtn)


        def OnColourBtn(evt):
            if self.panel.popupFrame:
                id = evt.GetId()
                value = evt.GetValue()
                if id == foreColorBtn.GetId():
                    self.panel.popupFrame.SetColor(fore = value)
                else:
                    self.panel.popupFrame.SetColor(back = value)
            evt.Skip()
        foreColorBtn.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColorBtn.Bind(EVT_BUTTON_AFTER, OnColourBtn)


        def OnCancelBtn(evt):
            if self.panel.popupFrame:
                self.panel.popupFrame.Close()
                self.panel.popupFrame = None
            evt.Skip()
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, OnCancelBtn)


        def OnApplyBtn(evt):
            panel.dialog.buttonRow.applyButton.Enable(False)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyBtn)


        def OnTestBtn(evt):
            file = wavFileCtrl.GetTextCtrl().GetValue()
            sound = wx.Sound(file)
            if os.path.isfile(file) and sound.IsOk():
                sound.Play(wx.SOUND_ASYNC)
            else:
                self.PrintError(self.plugin.text.soundProblem % file)
                PlaySound('SystemExclamation', SND_ASYNC)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestBtn)


        def OnCloseBox(evt):
            if self.panel.popupFrame:
                self.panel.popupFrame.Close()
                self.panel.popupFrame = None
            evt.Skip()
        panel.dialog.Bind(wx.EVT_CLOSE, OnCloseBox)
        

        while panel.Affirmed():
            if self.panel.popupFrame:
                popPos = self.panel.popupFrame.GetPosition()
                self.panel.popupFrame.Close()
                self.panel.popupFrame = None
            else:
                popPos = args[8]
            panel.SetResult((
                defTime.GetValue(),
                prefCtrl.GetValue(),
                suffCtrl.GetValue(),
                wavFileCtrl.GetTextCtrl().GetValue(),
                popTxtCtrl.GetValue(),
                backColorBtn.GetValue(),
                foreColorBtn.GetValue(),
                fontBtn.GetValue(),
                popPos
            ),)
#===============================================================================

class AbortEggTimers(eg.ActionBase):

    def __call__(self):
        self.plugin.AbortEggTimers()
#===============================================================================

Actions = (
    (SetEggTimer, "SetEggTimer", "Adjust and start egg timer", "Adjust and start egg timer.", 0),
    (SetEggTimer, "StartEggTimer", "Start egg timer", "Start egg timer immediately (without the possibility of adjust of time to elapse).", 1),
    (AbortEggTimers, "AbortEggTimers", "Abort egg timer(s)", "Abort egg timer(s).", None),
    (ShowSchedulGhost, "ShowSchedulGhost", "Show SchedulGhost", "Show SchedulGhost manager.", None),
    (HideSchedulGhost, "HideSchedulGhost", "Hide SchedulGhost", "Hide SchedulGhost manager.", None),
    (EnableSchedule, "EnableSchedule", "Enable schedule", "Enable schedule.", 1),
    (EnableSchedule, "DisableSchedule", "Disable schedule", "Disable schedule.", 0),
    (EnableAll, "EnableAll", "Enable all schedules", "Enable all schedules.", 1),
    (EnableAll, "DisableAll", "Disable all schedules", "Disable all schedules.", 0),
    (EnableSchedule, "GetSchedule", "Get schedule", "Get schedule.", -1),
    (AddSchedule, "AddSchedule", "Add schedule", AddSchedule.text.descr, None),
    (DeleteSchedule, "DeleteSchedule", "Delete schedule", "Delete schedule.", None),
)