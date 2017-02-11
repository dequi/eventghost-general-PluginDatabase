
# Copyright (C) 2008 Chris Longo <cal@chrislongo.net> and Tobias Arrskog (topfs2)
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

from xbmcclient import *

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "XBMC",
    author = "Chris Longo",
    version = "0.2." + "$LastChangedRevision: 570 $".split()[1],
    kind = "program",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1005",
    description = "Adds actions to control <a href='http://www.xbmc.org/'>XBMC</a>.",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsRAAALEQF/ZF+RAAAA"
        "BGdBTUEAALGeYUxB9wAAACBjSFJNAAB6fAAAfosAAPoBAACHPAAAbUoAAPFDAAA2IAAAHlNX4WK7"
        "AAACYElEQVR42tTTPW8ScQDH8d/9n44HESgFKQjFWku1rUYdTEAT0sGHSU10cHZz0piYjqYxbia6"
        "+hB3Y0w3kzq0scaojdZqYiMp1dQWAlLg4A7ugbvzRXTy8wK+21dyXRe7QbBLuw6wG3ceJnJnLuTL"
        "279DrutySBIhEnUopSbjtMsYVzkXLSFEU5Y9dY/XW5Nlr207DpRWE+zzp6VHxWLpstpWKaEA5RT9"
        "XgCcC/jDDihjOpWI6vF4WkLweigULgdD4R/p4ZH30X1Dr6XhbK4i/OH43qSKVikJLhhGz26AEo61"
        "+Qz0roWR8RDWixtIJKP4/mUVA5EgkvvjOHEy/1FKj+XnwpHMxdipIhJH29C2o0hMVmH1KJQyxWTw"
        "FuKhKYCbaDUVOI4LwzKxOD8PAvkrMazOW1uSUH43ilCqgUYphvJyBitzKUyfLiCVBe7PPkVzp4l7"
        "dx9g+lwB5T9bePPqJTIjB4v0uqmVi4cHbx67UkFteRjRAx30mgEcym9iZz2NpRcyfAM6Om0Nruui"
        "sr2F8SNZuIQjEhl6Lj0LAY8Hcwtq6nwhStuQJB8sWOh3fTClBgIDOhj1wDAtcEFRq/5FW+shPRRF"
        "diyTYJNe4Kr1bfaJHiv0qAtBKTgX4D6CAJXAbQIhaYhyG16iIxvpwEfW0BITM75YrsJm3Ah6SnfB"
        "kCtzWmLikmabYLYAIRxO34Zp6nAs9VdX6xSVRn2lb7QWe2b3w9RxplwLy2AL8AOMIa5s3vb6gzUm"
        "+5mh1XXL0Lq2pVRVQ2z66J6fpLdaMqu6KjwUXo8XnFH0+w6k/3+mfwMAzwT87LI0qNEAAAAASUVO"
        "RK5CYII="
    ),
)

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs

ACTIONS = (
(eg.ActionGroup, "Actions", "Actions", None, (
		("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "ActivateWindow(ShutdownMenu)"),
    ("ShowSubtitles", "Show Subtitles", "Toggle subtitles on or off.", "ShowSubtitles"),
    ("AudioDelayMinus", "AudioDelayMinus", "Audio Delay Minus.", "audiodelayminus"),
    ("AudioDelayPlus", "AudioDelayPlus", "Audio Delay Plus.", "audiodelayplus"),
    ("TakeScreenShot", "Take Screen Shot", "Takes a screen shot.", "TakeScreenshot"),
    ("EjectTray", "Eject Tray", "Close or open the DVD tray.", "EjectTray"),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://xbmc.org/wiki/?title=Keymap.xml#Remote_Buttons

REMOTE_BUTTONS = (
(eg.ActionGroup, "Remote", "Remote", None, (
		("Left", "Left", "", "left"),
		("Right", "Right", "", "right"),
		("Up", "Up", "", "up"),
		("Down", "Down", "", "down"),
		("Select", "Select", "", "select"),
		("Back", "Back", "", "back"),
		("Menu", "Menu", "", "menu"),
		("Info", "Info", "", "info"),
		("Display", "Display", "", "display"),
		("Title", "Title", "", "title"),
		("Play", "Play", "", "play"),
		("Pause", "Pause", "", "pause"),
		("Reverse", "Reverse", "", "reverse"),
		("Forward", "Forward", "", "forward"),
		("Skip +", "Skip +", "", "skipplus"),
		("Skip -", "Skip -", "", "skipminus"),
		("Stop", "Stop", "", "stop"),
		("0", "0", "", "zero"),
		("1", "1", "", "one"),
		("2", "2", "", "two"),
		("3", "3", "", "three"),
		("4", "4", "", "four"),
		("5", "5", "", "five"),
		("6", "6", "", "six"),
		("7", "7", "", "seven"),
		("8", "8", "", "eight"),
		("9", "9", "", "nine"),
		("Power", "Power", "", "power"),
		("My TV", "My TV", "", "myTV"),
		("My Music", "My Music", "", "mymusic"),
		("My Pictures", "My Pictures", "", "mypictures"),
		("My Video", "My Video", "", "myvideo"),
		("Record", "Record", "", "record"),
		("Start", "Start", "", "start"),
		("Vol +", "Vol +", "", "volumeplus"),
		("Vol -", "Vol -", "", "volumeminus"),
		("channelplus", "channelplus", "", "channelplus"),
		("channelminus", "channelminus", "", "channelminus"),
		("pageplus", "pageplus", "", "pageplus"),
		("pageminus", "pageminus", "", "pageminus"),
		("Mute", "Mute", "", "mute"),
		("Recorded TV", "Recorded TV", "", "recordedtv"),
		("Live TV", "Live TV", "", "livetv"),
		("*", "*", "", "star"),
		("#", "#", "", "hash"),
		("Clear", "Clear", "", "clear"),
)),
)

class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_action(self.value, ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

class ButtonPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_remote_button(self.value)
        except:
            raise self.Exceptions.ProgramNotRunning

# And now we define the actual plugin:

class XBMC(eg.PluginClass):
    def __init__(self):
        self.AddActionsFromList(REMOTE_BUTTONS, ButtonPrototype)
        self.AddActionsFromList(ACTIONS, ActionPrototype)
        self.xbmc = XBMCClient("EventGhost")

    def __start__(self):
        try:
            self.xbmc.connect()
        except:
            raise self.Exceptions.ProgramNotRunning

    def __stop__(self):
        try:
            self.xbmc.close()
        except:
            pass

    def __close__(self):
        pass