# Plugins/Taskbar/__init__.py
#
# Copyright (C)  2010 Pako  <lubos.ruckl@quick.cz>
#
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


eg.RegisterPlugin(
    name = "Taskbar",
    author = "Pako",
    version = "1.0.0",
    kind = "other",
    guid = "{9E798FF1-ABFB-42F2-A292-0FF746309DBE}",
    createMacrosOnAdd = True,
    description = """ Tool for work with the windows taskbar""",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEX6+vrU6dJ3tHA4"
        "gDIWXBFzpG+02LBDkDsqeCI0fywLSghwnmxElT05ijFPm0RBkDgJQgZtmWl6unIvfyVT"
        "nkhJlUA1gC8KPgdpk2ZkrFtkqF0+jDY+jDREkzs4hzIORwtKeEVmjmRfqlUvgCUpdR9Q"
        "jkobaRVJl0BHlT4VVxBCcz5Vpk0xhydXpEtNmUIbYxU9dTcOVQlLmUEDMgJyumoxhykt"
        "fSMXWxIVSxFSf08KSwdFlTw8jDQCKgEQXAtNm0NCkTsFNgMIQgVAjjc2hC8BIgAMUgg9"
        "jDUDLwJknl8cXRcXWBE7ijMxgCoJPAYJLgdBZkAJSAY2hzECJwESUA4zgCwreyUHNgUj"
        "SyJPjEoZXRMtdyYFLQM+bTkLQQgHOAYvVy1/tHhZlVQTUg82fy8ufSYaXxUYRBVAaj41"
        "XzR6rnUQUAs5hDIJPgdSd093qHI7ijQ0hC4TUw8aRBfC0sJzom8GNwQiZhwLQwkbRxiV"
        "sJNvnGoJOAccTRlUe1IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAB3AAB3d3d3d3cAd3dTDwAdWRZ3ADF3d3cmSSUAAC5XGgAoWx8GCk5lNw13"
        "d3cAd3dVFAAjWRx3ADd3d3d2dnYAGEVZHAAqXCMjDVN3dip3d3cAHENXGAAhWRp3AEN3"
        "d3d3d3chd3dJACYLUAJ3L2BOM3chRR0NACpXFhQYUxF3GFN3d3d3d3d3d3deL3czYC53"
        "d3dSNXcAIwAaEU5bHyELTgJ3QGR3d3d3d3d3d3d3d3d3d3d3d3dTN3cAKAAdHFVTDSUd"
        "WRh3aXJ3d3d3d3d3d3d3d3d3d3d3d3dXOHcALwAAEUxVFgZcblt3d3d3d3d3d3d3d3d3"
        "d3d3d3d3d3dbOncAOgA6FE5yaT53d3d3d3d3d3cMsEgMsEgAADzscFpyUCBdBAPkAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAMVJREFUeNpjYAACRiZmFlYG"
        "BGBj5+Dk4kbwGXl4+fgFBBECQsIiomLiEgwMklIQAWkZWTl5BUUGJWUVVbCAmrqGphYD"
        "g7aOrp6+AUjA0IjfmIHBxNRMRNTcwhIoYGVtYwuSsLN3cARrcXJ2cQXRbhruHkDK08vb"
        "x9fPP4CBIZA/KBgkYRASGhYewcAQGWUTHQPWEhsXn8CQmJSckpqWDnFIRiYDQ1Z2jo9v"
        "bh7CufkCBYVFxSUIgdKy8orKKiQfV9fU1oHlAYjJITsbAU04AAAAAElFTkSuQmCC"
    ),
)
#===============================================================================


import ctypes
from ctypes import wintypes
from eg.WinApi.Dynamic import GetWindowLong, SetWindowPos

SHAppBarMessage     =  ctypes.windll.shell32.SHAppBarMessage
ABM_GETSTATE        =  0x00000004 # Retrieves the autohide and always-on-top states of the Windows taskbar
ABM_SETSTATE        =  0x0000000A # Sets the autohide and always-on-top states of the Windows taskbar.
ABS_AUTOHIDE        =  0x0000001
ABS_ALWAYSONTOP     =  0x0000002
TOGGLE_UNHIDEWINDOW =  0x40
TOGGLE_HIDEWINDOW   =  0x80
#===============================================================================


def isWindows7():
    '''Return True if current OS is Windows 7.'''
    from win32api import GetVersionEx
    VER_NT_WORKSTATION = 1
    format = 1
    version = GetVersionEx(format)
    if not version or len(version) < 9:
        return False
    return ((version[0] == 6) and (version[1] == 1) and (version[8] == VER_NT_WORKSTATION))

class Taskbar(eg.PluginBase):

    class APPBARDATA(ctypes.Structure):
        _fields_ = [
            ("cbSize",wintypes.DWORD),
            ("hWnd",wintypes.HWND),
            ("uCallbackMessage", ctypes.c_ulong),
            ("uEdge", ctypes.c_ulong),
            ("rc", wintypes.RECT),
            ("lParam",wintypes.LPARAM),
        ]

    def __init__(self):
        self.hTaskBar = ctypes.windll.user32.FindWindowA("Shell_TrayWnd", "")
        self.pAPPBARDATA = ctypes.POINTER(self.APPBARDATA)
        self.AddActionsFromList(ACTIONS)
        if not isWindows7():
            self.AddActionsFromList(ACTIONS2)

    def Appbardata(self):
        appbardata = self.APPBARDATA()
        appbardata.hWnd = self.hTaskBar
        appbardata.cbSize = wintypes.DWORD(ctypes.sizeof(appbardata))
        return appbardata
#===============================================================================


class HideUnhide(eg.ActionBase):

    def __call__(self):
        if self.value > 0:
            flag = self.value
        else:
            hide = GetWindowLong(self.plugin.hTaskBar,-16)&0x10000000
            flag = TOGGLE_HIDEWINDOW if hide else TOGGLE_UNHIDEWINDOW            
        SetWindowPos(self.plugin.hTaskBar, 0, 0, 0, 0, 0, flag)
#===============================================================================


class GetHide(eg.ActionBase):

    def __call__(self):
        hide = GetWindowLong(self.plugin.hTaskBar,-16)&0x10000000
        return hide != 0x10000000
#===============================================================================#===============================================================================        


class SetAutohide(eg.ActionBase):

    def __call__(self):
        Appbardata = self.plugin.Appbardata()
        pData = self.plugin.pAPPBARDATA(Appbardata)
        res = SHAppBarMessage(ABM_GETSTATE, pData)
        if self.value > -1:
            flag = self.value
        else:
            flag =  0 if res&1 else 1
        Appbardata.lParam = flag*ABS_AUTOHIDE + ABS_ALWAYSONTOP*int(res&2==2)
        res = SHAppBarMessage(ABM_SETSTATE, pData)
#===============================================================================        


class GetAutohide(eg.ActionBase):

    def __call__(self):
        Appbardata = self.plugin.Appbardata()
        pData = self.plugin.pAPPBARDATA(Appbardata)
        res = SHAppBarMessage(ABM_GETSTATE, pData)
        return res&1 == 1
#===============================================================================        


class SetAlwaysOnTop(eg.ActionBase):

    def __call__(self):
        Appbardata = self.plugin.Appbardata()
        pData = self.plugin.pAPPBARDATA(Appbardata)
        res = SHAppBarMessage(ABM_GETSTATE, pData)
        if self.value > -1:
            flag = self.value
        else:
            flag =  0 if res&2 else 1
        Appbardata.lParam = ABS_AUTOHIDE*int(res&1==1) + ABS_ALWAYSONTOP*flag
        res = SHAppBarMessage(ABM_SETSTATE, pData)

#===============================================================================        


class GetAlwaysOnTop(eg.ActionBase):

    def __call__(self):
        Appbardata = self.plugin.Appbardata()
        pData = self.plugin.pAPPBARDATA(Appbardata)
        res = SHAppBarMessage(ABM_GETSTATE, pData)
        return res&2 == 2
#===============================================================================        


ACTIONS = (
    (HideUnhide,"HideTaskBar","Hide","Hide or the taskbar.",TOGGLE_HIDEWINDOW),
    (HideUnhide,"UnhideTaskBar","Unhide","Unhide the taskbar.",TOGGLE_UNHIDEWINDOW),
    (HideUnhide,"ToggleTaskBar","Toggle the hide status","Toggles the hide status of taskbar.",0),
    (GetHide,"GetHide","Get hide status","Get hide status.",None),
    (SetAutohide,"SetAutohideOn","Set autohide ON","Sets autohide ON.",1),
    (SetAutohide,"SetAutohideOff","Set autohide OFF","Sets autohide OFF.",0),
    (SetAutohide,"ToggleAutohide","Toggle auto-hide","Toggles auto-hide.",-1),
    (GetAutohide,"GetAutohide","Get autohide","Get autohide.",None),
)
ACTIONS2 = (    
    (SetAlwaysOnTop,"SetAlwaysOnTopOn","Set Always On Top ON","Sets Always On Top ON.",1),
    (SetAlwaysOnTop,"SetAlwaysOnTopOff","Set Always On Top OFF","Sets Always On Top OFF.",0),
    (SetAlwaysOnTop,"ToggleAlwaysOnTop","Toggle Always On Top","Toggles Always On Top.",-1),
    (GetAlwaysOnTop,"GetAlwaysOnTop","Get Always On Top","Get Always On Top.",None),
)