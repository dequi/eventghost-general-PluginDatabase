# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2007-11-19 20:33:24 +0100 (Mon, 19 Nov 2007) $
# $LastChangedRevision: 277 $
# $LastChangedBy: bitmonster $

import eg
import wx

eg.RegisterPlugin(
    name = "ffdshow",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision: 277 $".split()[1],
    kind = "program",
    description = (
        'Adds actions to control the '
        '<a href="http://ffdshow-tryout.sourceforge.net/">'
        'ffdshow DirectShow filter</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADMElEQVR42nVSXUiTYRR+"
        "v+/bn6hbapqoTEf400R3YWmQ6E2gIoIk02Y3BZoadVEIGsxCZAkpSZB6YUiDdlFmNAzC"
        "QeDUFGXI7GcmBlEauh+dujnWtm/receMbjrwcF7Oe87zPue8hxkfHyccxxGlUkkYhiEy"
        "mYwcm9/vJy6XizgcDqJQKEhSUlI0TvN8Ph/Z2NggzNjYGCMQCEhRUVE5z/MyqVTKsywb"
        "AWk4FAqxu7u7n7e2tpjs7GxVcnIyUvhIYmJi+OjoiAXBHON0OoUIBt1u95fMzExlJBIh"
        "gUAgqspms5GBgQFTf3+/F3eXwuFwVAF9fXNzk/T09HgYyORQlLG/v/8eLytqa2s/HRwc"
        "mNPS0khKSkry9vb29Pz8/GO0caKtrW1nYWHhFZTQtmTp6elSZnFxkfZaXVZW9m5mZoYf"
        "HBx8X1xc/EQul7MNDQ3G5eXlczU1NWar1SrWarWvU1NTn2VlZQmGhoaM0XmAkROJRNqC"
        "goL7tO+9vT0uIyODzM7OksnJyZsoEkkkkkdCoTBweHgoosrMZjOZm/vwwOFw3mNQQCdt"
        "ycnJKTEYDL6VlRUuPj7+CNLDdru9Va/Xq9GKZnR0NDA9PR3EbwUwPMHq6uqNYDBgYND7"
        "FY/H04ciRWtr61OoGcRre83NzaH19XV3fX29XwxraWlxVVZWKjs7O8P5+fmMTqdz5ebm"
        "EWZpaclWWlqaBx/u6OiYgtyGpqYmUlhYSKCgWqPRvMBrcY2NjYb29vZrw8PDJCEhgajV"
        "akKHyfT29r2sqChXm0wmMjExcR3THe/u7hbX1dX5sTDdXq9Xh1nQu1sgHFGpVMK1tbXf"
        "+DEmagKBCHvEXeT5UHowGNRjsBEoIpg+wfeyVVVVGovFIh4ZGZlF+jcsFenq6mKRF12K"
        "6BYi8SouJWB9i7MSRIm42wZclBC/Q1fwLM6LAIsaC/wZQEkJ4nC4Cwyg+Db8RxAdoKgE"
        "5wIUihE3ImaFv4zYDrwbPhcwUQIRDg+BKVoA/ADkgAD4DpwHvlK1wC/AC9yJ5T+PtgC7"
        "AJwC3gCnAQlgp/JjvZ6MkRtjdzTnJyU7Jji2v8P5j3EA/2/gD9tgef0euQO8AAAAAElF"
        "TkSuQmCC"
    ),
)



##define FFDSHOW_REMOTE_MESSAGE "ffdshow_remote_message"
##define FFDSHOW_REMOTE_CLASS "ffdshow_remote_class"
#
#//lParam - parameter id to be used by WPRM_PUTPARAM, WPRM_GETPARAM and COPY_PUTPARAMSTR
##define WPRM_SETPARAM_ID 0
#
#//lParam - new value of parameter
#//returns TRUE or FALSE
##define WPRM_PUTPARAM    1
#
#//lParam - unused
#//return the value of parameter
##define WPRM_GETPARAM    2
#
#//lParam - parameter id
##define WPRM_GETPARAM2   3
#
##define WPRM_STOP        4
##define WPRM_RUN         5
#
#//returns playback status
#// -1 - if not available
#//  0 - stopped
#//  1 - paused
#//  2 - running
##define WPRM_GETSTATE    6
#
#//returns movie duration in seconds
##define WPRM_GETDURATION 7
#//returns current position in seconds
##define WPRM_GETCURTIME  8
#
##define WPRM_PREVPRESET 11
##define WPRM_NEXTPRESET 12 
#
#//Set current time in seconds
##define WPRM_SETCURTIME 13
#
#
#
#
#//WM_COPYDATA 
#//COPYDATASTRUCT.dwData=
##define COPY_PUTPARAMSTR        9 // lpData points to new param value
##define COPY_SETACTIVEPRESET   10 // lpData points to new preset name
##define COPY_AVAILABLESUBTITLE_FIRST 11 // lpData points to buffer where first file name will be stored  - if no subtitle file is available, lpData will contain empty string
##define COPY_AVAILABLESUBTITLE_NEXT  12 // lpData points to buffer where next file name will be stored  - if no subtitle file is available, lpData will contain empty string
##define COPY_GETPARAMSTR       13 // lpData points to buffer where param value will be stored
##define COPY_GET_PRESETLIST		14 //Get the list of presets (array of strings)
##define COPY_GET_SOURCEFILE		15 //Get the filename currently played

import sys
import win32gui
import win32con
import ctypes
from ctypes.wintypes import DWORD

class COPYDATASTRUCT(ctypes.Structure):
    """This is a mapping to the Win32 COPYDATASTRUCT.
    
    typedef struct tagCOPYDATASTRUCT {
        ULONG_PTR dwData;
        DWORD cbData;
        PVOID lpData;
    } COPYDATASTRUCT, *PCOPYDATASTRUCT;
    """
    _fields_ = [ 
        ('dwData', DWORD), #I think this is right
        ('cbData', DWORD),
        ('lpData', ctypes.c_char_p)
    ]

PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)


WPRM_SETPARAM_ID = 0
WPRM_PUTPARAM = 1
WPRM_GETPARAM = 2
WPRM_GETPARAM2 = 3
WPRM_STOP = 4
WPRM_RUN = 5
WPRM_PREVPRESET = 11
WPRM_NEXTPRESET = 12 

COPY_SETACTIVEPRESET = 10
COPY_GET_PRESETLIST = 14
COPY_GET_SOURCEFILE = 15


class WParamAction(eg.ActionClass):
    
    def __call__(self):
        return self.plugin.SendFfdshowMessage(self.value)
    
    
    
class GetIntAction(eg.ActionClass):
    
    def __call__(self):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning

        return win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)
    
    
    
class SetIntAction(eg.ActionClass):
    parameterDescription = "Set to:"
    
    def __call__(self, value=0):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning

        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, value)
    
    
    def Configure(self, value=0):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(
            value, 
            min = -sys.maxint - 1, 
            max = sys.maxint, 
        )
        panel.AddLine(self.parameterDescription, valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())
    
    
    
class ChangeIntAction(SetIntAction):
    parameterDescription = "Change by:"
    
    def __call__(self, value=0):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning

        oldValue = win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)
        newValue = oldValue + value
        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, newValue)
        return newValue


class ToggleAction(eg.ActionClass):
    
    def __call__(self, action):
        #0: disable, 1: enable, 2: toggle, 3: getStatus
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning
            
        if action == 0 or action == 1:
            win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
            win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, action)
            return action
            
        oldValue = win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)
        
        if action == 2:
            if oldValue:
                newValue = 0
            else:
                newValue = 1
            win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
            win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, newValue)
            return newValue
            
        if action == 3:
            return oldValue
            
    
    def GetLabel(self, action):
        labels = (
            "Disable %s",
            "Enable %s",
            "Toggle %s",
            "Get Status of %s"
        )
        return labels[action] % self.name
    

    def Configure(self, action = 2):
        panel = eg.ConfigPanel(self)
        panel.AddLabel(self.description);
        
        radioButtons = (
            wx.RadioButton(panel, -1, "Disable", style = wx.RB_GROUP),
            wx.RadioButton(panel, -1, "Enable"),
            wx.RadioButton(panel, -1, "Toggle"),
            wx.RadioButton(panel, -1, "Get status")
        )

        radioButtons[action].SetValue(True)
        for rb in radioButtons:
            panel.AddCtrl(rb)
        
        while panel.Affirmed():
            for i in range(len(radioButtons)):
                if radioButtons[i].GetValue():
                    action = i
                    break
            panel.SetResult(action)




class IntegerAction(eg.ActionClass):
    
    def __call__(self, action, value):
        #0: set to, 1: change by, 2: get value
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning            

        if action == 2:
            return win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)    
            
        if action == 1:
            value += win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)      
        
        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        win32gui.SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, value)
        return value
            
    
    def GetLabel(self, action, value):
        labels = (
            "Set %s to %i",
            "Change %s by %i",
        )
        if action < 2:
            return labels[action] % (self.name, value)
        else:
            return "Get Value of %s" % self.name
    
    
    def Configure(self, action = 0, value = 0):
        panel = eg.ConfigPanel(self)
        panel.AddLabel(self.description);
        
        radioButtons = (
            wx.RadioButton(panel, -1, "Set to value", style = wx.RB_GROUP),
            wx.RadioButton(panel, -1, "Change by value"),
            wx.RadioButton(panel, -1, "Get current value")
        )

        valueCtrl = panel.SpinIntCtrl(
            value, 
            min = -sys.maxint - 1, 
            max = sys.maxint, 
        )

        radioButtons[action].SetValue(True)
        for rb in radioButtons:
            panel.AddCtrl(rb)
        
        panel.AddCtrl(valueCtrl)
        
        while panel.Affirmed():
            for i in range(len(radioButtons)):
                if radioButtons[i].GetValue():
                    action = i
                    break
                    panel = eg.ConfigPanel(self)
            panel.SetResult(action, valueCtrl.GetValue())


#Name, internalName, description, filterXXX, isXXX, showXXX, orderXXX, fullXXX, halfXXX
FILTERS = (
    ("Avisynth", "Avisynth", None, 1250, 1251, 1260, 1252, 1253, None), 
    ("Bitmap overlay", "Bitmap", None, 1650, 1651, 1652, 1653, 1654, None),
    ("Blur & NR", "Blur", None, 900, 901, 936, 903, 905, None),
    ("Crop", "CropNzoom", None, 747, 712, 752, 754, 765, None),
    ("DCT", "DCT", None, 450, 451, 462, 452, 453, 463),
    ("DeBand", "GradFun", None, 1150, 1151, 1152, 1153, 1154, 1155),
    ("Deinterlacing", "Deinterlace", None, 1400, 1401, 1418, 1424, 1402 , None),
    ("DScaler filter", "DScaler", None, 2200, 2201, 2206, 2202, 2203, 2207),
    ("Grab", "Grab", None, 2000, 2001, 2013, 2002, 2003, None),
    ("Levels", "Levels", None, 1600, 1601, 1611, 1602, 1603, 1612),
    ("Logoaway", "Logoaway", None, 1450, 1451, 1452, 1453, 1454, None),
    ("Noise", "Noise", None, 500, 501, 512, 506, 507, 513),
    ("Offset & flip", "Offset", None, 1100, 1101, 1110, 1102, 1109, 1111),
    ("OSD", "OSD", "Actions to control ffdshow's OSD", None, 1501, None, None, None, None),
    ("Perspective correction", "Perspective", None, 2300, 2301, 2314, 2302, 2303, 2315),
    ("Picture properties", "PictProp", None, 200, 205, 217, 207, 213, 218),
    ("Postprocessing", "Postproc", None, 100, 106, 120, 109, 111, 121),
    ("Presets", "Presets", "Actions to control ffdshow presets", None, None, None, None, None, None),
    ("Resize & aspect", "Resize", None, 700, 701, 751, 722, 723, None),
    ("Sharpen", "Sharpen", None, 400, 401, 427, 407, 408, 428),
    ("Subtitles", "Subtitles", None, 800, 801, 828, 815, 817, None),
    ("Visualizations", "Vis", None, 1200, 1201, 1206, 1202, None, None),
    ("Warpsharp", "Warpsharp", None, 430, 431, 442, 432, 433, 443),
    ("deprecated Actions", "deprecated", "Actions for compatibility reasons. Do not use", None, None, None, None, None, None),
)

#aType, aGroup, aClsName, aName, aDescription, aValue
CMDS = (
    (WParamAction, None, "Run", "Run", None, 5),
    (WParamAction, None, "Stop", "Stop", None, 4),
    (GetIntAction, "deprecated", "GetSubtitleDelay", "Get Subtitle Delay", None, 812),
    (SetIntAction, "deprecated", "SetSubtitleDelay", "Set Subtitle Delay", None, 812),
    (ChangeIntAction, "deprecated", "ChangeSubtitleDelay", "Change Subtitle Delay", None, 812),
    (WParamAction, "Presets", "PreviousPreset", "Previous Preset", None, 11),
    (WParamAction, "Presets", "NextPreset", "Next Preset", None, 12),

    #subtitle actions
    (IntegerAction, "Subtitles", "SubtitleDelay", "Subtitle: Delay", None, 812),
    
    #CropNzoom
    (IntegerAction, "CropNzoom", "CropNzoomMagnificationX", "Crop: Magnification X", None, 714),
    (IntegerAction, "CropNzoom", "CropNzoomMagnificationY", "Crop: Magnification Y", None, 720),
    (ToggleAction, "CropNzoom", "CropNzoomMagnificationLock", "Crop: Magnification Lock", None, 721),
)


class Ffdshow(eg.PluginClass):
    
    def __init__(self):
        groups = {}
        for filterName, internalName, description, filterId, isId, showId, orderId, fullId, halfId in FILTERS:
            if not description:
                description = "Actions to control the %s filter within ffdshow" % filterName
            group = self.AddGroup(filterName, description)
            groups[internalName] = group
            
            #enable/disable filter
            if isId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter"
                    description = "Sets or retrieves the status of the %s filter" % filterName
                    value = isId
                tmpAction.__name__ = internalName + "Toggle"
                group.AddAction(tmpAction)
            
            if showId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter visibility"
                    description = "Sets or retrieves the visibility of the %s filter" % filterName
                    value = showId
                tmpAction.__name__ = internalName + "Visibility"
                group.AddAction(tmpAction)

            if fullId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter \"Process whole image\" property"
                    description = "Sets or retrieves the \"Process whole image\" property of the %s filter" % filterName
                    value = fullId
                tmpAction.__name__ = internalName + "ProcessWholeImage"
                group.AddAction(tmpAction)

            if halfId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter \"Only right half\" property"
                    description = "Sets or retrieves the \"Only right half\" property of the %s filter" % filterName
                    value = halfId
                tmpAction.__name__ = internalName + "ProcessRightHalf"
                group.AddAction(tmpAction)

            if orderId:
                class tmpAction(IntegerAction):
                    name = filterName + " order"
                    description = "Sets or retrieves the position of the %s filter" % filterName
                    value = orderId
                tmpAction.__name__ = internalName + "Order"
                group.AddAction(tmpAction)


        #add commands
        for aType, aGroup, aClsName, aName, aDescription, aValue in CMDS:
            class tmpAction(aType):
                name = aName
                description = aDescription
                value = aValue
            tmpAction.__name__ = aClsName
            if not aGroup:
                self.AddAction(tmpAction)
            else:
                group = groups[aGroup]
                group.AddAction(tmpAction)
        
        group = groups["Presets"]
        group.AddAction(GetPresets)
        group.AddAction(SetPreset)
        
        
    def __start__(self):
        self.mesg = win32gui.RegisterWindowMessage("ffdshow_remote_message")
        eg.messageReceiver.AddHandler(win32con.WM_COPYDATA, self.Handler)
        
        
    @eg.LogIt
    def Handler(self, hwnd, mesg, wParam, lParam):
        cdsPointer = ctypes.cast(lParam, PCOPYDATASTRUCT)
        #print repr(cdsPointer.contents.lpData)
        return True


    def SendFfdshowMessage(self, wParam, lParam=0):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning
            
        return win32gui.SendMessage(hwnd, self.mesg, wParam, lParam)



class SetPreset(eg.ActionWithStringParameter):
    class text:
        name = "Set Preset"
        parameterDescription = "Preset Name:"
        
    def __call__(self, preset):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning
            
        cds = COPYDATASTRUCT()
        cds.dwData = COPY_SETACTIVEPRESET
        cds.lpData = ctypes.c_char_p(preset)
        cds.cbData = len(preset) + 1
        win32gui.SendMessage(
            hwnd, 
            win32con.WM_COPYDATA, 
            eg.messageReceiver.hwnd, 
            ctypes.addressof(cds)
        )
        
        
    
class GetPresets(eg.ActionClass):
    
    def __call__(self):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            raise self.Exceptions.ProgramNotRunning
        
        cds = COPYDATASTRUCT()
        cds.dwData = COPY_GET_PRESETLIST
        win32gui.SendMessage(
            hwnd, 
            win32con.WM_COPYDATA, 
            eg.messageReceiver.hwnd, 
            ctypes.addressof(cds)
        )
        