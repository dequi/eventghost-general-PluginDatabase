version="0.1.10"

# Plugins/MediaMonkeyTest/__init__.py
#
# Copyright (C)  2007 Pako  <lubos.ruckl@quick.cz>
#
# This file is part of EventGhost.
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
#Last change: 2008-10-21 22:27

eg.RegisterPlugin(
    name = "MMTestWithoutThread",
    author = "Pako",
    version = version,
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control '
        '<a href="http://www.MediaMonkey.com/">MediaMonkey</a>. \n\n<P>'
        '<BR><B>Note:</B><BR>'
        'To make functional event triggering from MediaMonkey, you must install'
        '<BR>file "EventGhost.vbs" to MediaMonkey/Scripts/Auto folder.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=563",
    icon = (
        "R0lGODlhEAAQAPcAADQyNLyaTHRmRJSWlPzGNFxOPGxqbFROVKSGRJyWfOzSlOTCdGRmZ"
        "HReRERCPIRyTNy2dIyCbPzSZMSylExOTFxaXOTe5HxyVOS2ROzCTFxWPIx+ZKSajDw6PP"
        "zinExGTPTSfHR2dFRWVKSOVLyibGxiTExKRISKjNy+lIx6VPzOVKyaZLSqnFRSRJyGTNT"
        "GrOzKfERCRJR6RNS2fPzWdGRiXIx2VMyqXGxWPEQ+RDw2PMSiRIRuVJyenPzKRHRydFRS"
        "VLSedNS6hHx2ZGRaTIR2TKSSdPzWbMS6pFxeXPzy1IRyVPzKTGRWPKSSXLymhEQ+PPzqt"
        "PzahHx+fFxWVLymfHRiTJyShMzCpPzSXFxSRKSKTOzWtExGRNy2fMSqZH4HhAAAAAAAAM"
        "AAAAAIEgAACgAAEwAAAP8JhP8AAP8AAP8AAP8yAP8HAP+RAP98AACreAAGAACRTQB8AAA"
        "wBADqAAASAAAAAADQ4gA8BBUlAABbAGAIYOlAnhI4gAAAfNJ4IOYARYEAH3wAAMhNAMUA"
        "ABwAAAAAAErwB+PqAIESAHwAAKBGAHfQAFAmAABbAMgIAMVAQAE4HwAAAGsFAAAAAAAAA"
        "AAAAJxuAOi9ABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4AnpAAgHwAfH"
        "AA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pKgW3AJGSAHx8AEogKvRFAIAfAHwAAAA0WAB"
        "k8RWDEgB8AAD//wD//wD//wD//8gAAMUAABwAAAAAAABcpAHq6wASEgAAAAA09gBkOACD"
        "TAB8AFcIhPT864ASEnwAAIgYd+ruEBKQTwB8AMgAuMW36xySEgB8AKD/NAD/ZAD/gwD/f"
        "B8gWgBF7AAfEgAAABE01ABk/wCD/wB8fwSgMADr7AASEgAAAAPnIABkRQCDHwB8AACINA"
        "BkZACDgwB8fAABIAAARQAAHwAAAAQxbgAAvQAwAAAAAAMBAAAAAAAAAAAAAAAajQAA4gA"
        "ARwAAACH5BAEAABYALAAAAAAQABAABwjtAC0IFNjDgMEfPQYqtDCAAY8gECCQ4FFjwMIQ"
        "ViBIOcLxiAcUVgwMPGFlAY0jErJIkBBFCRcrJwQyIIEyywoDI2AoUfLiiQgLIT58OZIlA"
        "BAKQK5wqFABSJcpXSLQkKACQYyrMRzEeJDCRJcYQ1Ay2dFFqwMtGFReceAASokiBWIAuN"
        "olg48sRy7o6NJCRwetFBx0IEKACd4UHX7YUIAFCYUOOhwU8KFCgpQlIk2gUMLir2AZlY9"
        "AiCGzxAQAHbZsASBAwhEYApIMNFHCyIwbAHSMkAKhBJSFSRwsqYKjQJUHUH4ulAmgOQAG"
        "CwMCADs="
    ),
)



from win32com.client import Dispatch

#====================================================================

class MMTestWithoutThread(eg.PluginClass):
    MM = None
    
    def __init__(self):
        self.AddAction(Play)
        self.AddAction(Pause)
        
    def DispMM(self):
        if not self.MM:
            self.MM = Dispatch("SongsDB.SDBApplication")
            self.MM.ShutdownAfterDisconnect = False
        return self.MM

    def __stop__(self):
        if self.MM:
            del self.MM
            self.MM = None

#====================================================================
class Play(eg.ActionClass):
    name = "Play"
    description = "Play."

    def __call__(self):
        print "Command Play"        
        self.plugin.DispMM().Player.Play()

#====================================================================
class Pause(eg.ActionClass):
    name = "Pause"
    description = "Pause."

    def __call__(self):
        print "Command Pause"
        self.plugin.DispMM().Player.Pause()

#====================================================================
