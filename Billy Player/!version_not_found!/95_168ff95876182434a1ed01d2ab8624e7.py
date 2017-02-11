version="0.1.0" 

# Plugins/Billy/__init__.py
#
# Copyright (C)  2007 Pako  (lubos.ruckl@quick.cz)
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


# Every EventGhost plugin should start with the import of 'eg' and the 
# definition of an eg.PluginInfo subclass.
import eg

class Text:
    filemask = "Billy.exe|Billy.exe|All-Files (*.*)|*.*"
    label = "Path to Billy.exe:"
    title = "Written by Pako, based on MonsterMagnet's plugin for foobar2000"
    version = "Version: "
    text1="Hot Key >>"
    text2="<< is not defined inside of file Billy.ini!"
    text3="File Billy.ini not found!"
    class Run:
        text4="Billy not found!"
        
class Constants:
    VK_LWIN=91
    VK_CONTROL=17
    VK_MENU=18
    VK_SHIFT=16
    KEYEVENTF_KEYUP=2
        
        
eg.RegisterPlugin(
    name = "Billy Player",
    author = "MonsterMagnet+Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.sheepfriends.com/?page=billy">'
        'Billy</a> audio player. \n\n<p>'
        '<BR><B>ATTENTION !<BR>Only works for beta version 1.04b of Billy !</B>'
        '<BR>The plugin will not work with older versions of Billy!</p>'
        '<BR><BR>First You have to configure Hot Keys of Billy<BR>(Options - Settings - Global hotkeys).'
    ),
    createMacrosOnAdd = True,    
    icon = (
        "R0lGODlhEAAQAPcAAAQCBMz+tPz+/AAAABkEFSEAAAAAAAAAAGECDR4AAAAAAAAAAAAADQAAABUA"
        "AAAAAA0AyAAAHgAAEAAAagAAXQIABAAAhQAAAwAAFwMAAAAAAAAAAIgBAeIAABIAAAAAAOkaGeUA"
        "AIEAAHwAAAAAEQAAAAEAAAAAAFYA0QAAOQAAJQAAW5AVhOEAABIAAAAAAHMViAAAFgAAKAAAW7AN"
        "FeIAABIAAAAAABgNTe4AAJAAAHwAAHDIlQUeOZEQJXxqW/9dYP8EQP+FOP8DAG0X/gUAEZEAHnwA"
        "AIUBUOcAQIEAOHwAAAAZ2wAAGhUAJQAAW1gR/AMA8gAAEgAAAHABEIUA9xkARQAAAIgHhEIAABUA"
        "AAAAAAAI/gAAEQAAHgAAAH4JhAAAAAAAAMAAAAAiAAAcAAABAACSAP8ATf8AAP8Awf8AAP+IBP/j"
        "AP8SAP8AAADQ4gA8BAAlAABbAABIcQBB1QA4NgAAfgBNAAAAABUAAAAAAMDBYOIAnhIAgAAAfNJI"
        "+ObkVIESFnwAAIhGAELQABUmAABbAEpIB+NBAIE4AHwAAMAFAHYAAFAAAAAAAIj+AEIRUAEeFgAA"
        "AGtQAABAAAA4AAAAAPyJAOFaABIAAAAAAADYAADjAAASAAAAAPiFAPcrABKDAAB8ABgAaO4AnpAA"
        "gHwAfHAA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pIAW3AJGSAHx8AEr4IPRUAIAWAHwAAAA0SABk"
        "6xWDEgB8AAD//wD//wD//wD//4gAAEIAABUAAAAAAAC8BAHj5QASEgAAAAA0vgBkOwCDTAB8AFf4"
        "5PT35IASEnwAAOgYd+PuEBKQTwB8AIgAGEK35RWSEgB8ABH/NAD/ZAD/gwD/fAT4qABU5QAWEgAA"
        "AAM03gBk/wCD/wB8fwAAiADl5QASEgAAAADn+ABkVACDFgB8AASINABkZACDgwB8fAMB+AAAVAAA"
        "FgAAAAAxiQAAWgAAAAAAAAAAAAAAAAAAAAAAAAoA6QAAzgAARwAAACH5BAEAAAIALAAAAAAQABAA"
        "BwhEAAUIHEiwoMGDBgEoXMhQIUEAASJKnAjg4cSLASoOhIhRokaBHDtmtChy5MaSJkGi/CggZEeW"
        "LjHCXPmwoU2EOHMeDAgAOw=="
    ),
)

# Since we also have to do some GUI stuff, we also need 'wx'
import wx

# Now import some other modules that are needed for the special purpose of
# this plugin.
import os
from ConfigParser import SafeConfigParser
import win32api

fnList = (
    (
        "Play",
        "Play", 
        "Simulate a press on the play button.", 
        "0"
    ), 
    (
        "PlayPause", 
        "Toggle Play/Pause", 
        "Simulate a press on the PlayPause button.", 
        "1"
    ), 
    (
        "Stop",
        "Stop", 
        "Simulate a press on the stop button.", 
        "2"
    ), 
    (
        "NextTrack", 
        "Next Track", 
        "Simulate a press on the next track button.", 
        "3"
    ), 
    (
        "PreviousTrack",
        "Previous Track", 
        "Simulate a press on the previous track button.", 
        "4"
    ), 
    (
        "VolumeUp",
        "Volume Up", 
        "Simulate a press on the volume up button.", 
        "5"
    ), 
    (
        "VolumeDown",
        "Volume Down", 
        "Simulate a press on the volume down button.", 
        "6"
    ), 
    (
        "SoftMute",
        "Soft Mute", 
        "Simulate a press on the soft mute button.", 
        "7"
    ), 
    (
        "FocusBilly",
        "Focus Billy", 
        "Simulate a press on the focus Billy button.", 
        "8"
    ), 
    (
        "ExitBilly",
        "Exit Billy", 
        "Simulate a press on the exit Billy button.", 
        "9"
    ), 
    (
        "FindBox",
        "Find Box", 
        "Simulate a press on the find box button.", 
        "10"
    ), 
    (
        "OpenDirBox",
        "Open Dir Box", 
        "Simulate a press on the open dir box button.", 
        "11"
    ), 
    (
        "CopyPlayingTitle", 
        "Copy Playing Title", 
        "Simulate a press on the copy playing title button.", 
        "12"
    ),
)


# Now we can start to define the plugin by subclassing eg.PluginClass
class Billy(eg.PluginClass):
    text=Text
    BillyPath = None
    
    def __init__(self):
        self.AddAction(Run)
        BillyPath = ""

        # And now begins the tricky part. We will loop through every tuple in
        # our list to get the needed values.
        for tmpClassName, tmpName, tmpDescription, tmpHotKey in fnList:
            # Then we will create a subclass of eg.ActionClass on every
            # iteration and assign the values to the class-variables.
            class tmpActionClass(eg.ActionClass):
                name = tmpName
                description = tmpDescription
                HotKey = tmpHotKey
                # Every action needs a workhorse.
                def __call__(self):
                    cp = SafeConfigParser()
                    if os.access(os.path.dirname(self.plugin.BillyPath)+"//Billy.ini",os.F_OK):
                        cp.read(os.path.dirname(self.plugin.BillyPath)+"//Billy.ini")
                        try:
                            HotKey=cp.get('Global hotkeys', self.HotKey)
                            if HotKey[0]=="1":
                                win32api.keybd_event(Constants.VK_LWIN,0,0,0)
                            if HotKey[1]=="1":
                                win32api.keybd_event(Constants.VK_CONTROL,0,0,0)
                            if HotKey[2]=="1":
                                win32api.keybd_event(Constants.VK_MENU,0,0,0)
                            if HotKey[3]=="1":
                                win32api.keybd_event(Constants.VK_SHIFT,0,0,0)
                            win32api.keybd_event(int(HotKey[5:]),0,0,0)
                            win32api.keybd_event(int(HotKey[5:]),0,Constants.KEYEVENTF_KEYUP,0)
                            if HotKey[3]=="1":
                                win32api.keybd_event(Constants.VK_SHIFT,0,Constants.KEYEVENTF_KEYUP,0)
                            if HotKey[2]=="1":
                                win32api.keybd_event(Constants.VK_MENU,0,Constants.KEYEVENTF_KEYUP,0)
                            if HotKey[1]=="1":
                                win32api.keybd_event(Constants.VK_CONTROL,0,Constants.KEYEVENTF_KEYUP,0)
                            if HotKey[0]=="1":
                                win32api.keybd_event(Constants.VK_LWIN,0,Constants.KEYEVENTF_KEYUP,0)
                            return
                        except:
                            self.PrintError(self.plugin.text.text1+self.name+self.plugin.text.text2)
                    else:
                        # Some error-checking is always fine.
                        self.PrintError(self.plugin.text.text3)

            # We also have to change the classname of the action to a unique
            # value, otherwise we would overwrite our newly created action
            # on the next iteration.
            tmpActionClass.__name__ = tmpClassName
            # Finally we cann add the new ActionClass to our plugin
            self.AddAction(tmpActionClass)

    def __start__(self, BillyPath=None):
        self.BillyPath = BillyPath
                
    def Configure(self, BillyPath=None):
        if BillyPath is None:
            BillyPath = os.path.join(
                eg.PROGRAMFILES, 
                "Billy", 
                "Billy.exe"
            )
        dialog = eg.ConfigurationDialog(self)
        TitleText = wx.StaticText(dialog, -1, self.text.title, style=wx.ALIGN_LEFT)
        VersionText = wx.StaticText(dialog, -1, self.text.version+version, style=wx.ALIGN_LEFT)
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            size=(320,-1),
            initialValue=BillyPath, 
            startDirectory=eg.PROGRAMFILES,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
        dialog.sizer.Add(TitleText, 0, wx.EXPAND)
        dialog.sizer.Add(VersionText, 0, wx.EXPAND)
        dialog.sizer.Add((5, 20))
        dialog.AddLabel(self.text.label)
        dialog.AddCtrl(filepathCtrl)
        
        if dialog.AffirmedShowModal():
            return (filepathCtrl.GetValue(), )

class Run(eg.ActionClass):
    name = "Run"
    description = "Run Billy with its default settings."
    
    def __call__(self):
        try:
            head, tail = os.path.split(self.plugin.BillyPath)
            return win32api.ShellExecute(
                0, 
                None, 
                tail,
                None, 
                head, 
                1
            )
        except:
            # Some error-checking is always fine.
            self.PrintError(self.text.text4)
         
