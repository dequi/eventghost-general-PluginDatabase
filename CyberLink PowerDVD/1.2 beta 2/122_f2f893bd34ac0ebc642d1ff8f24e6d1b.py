# -*- coding: utf-8 -*-
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

import eg

eg.RegisterPlugin(
    name="CyberLink PowerDVD",
    description="Adds actions to control CyberLink PowerDVD 7, 8 and 12. Note: Enabling BD-J keyboard support disables all CyberLink PowerDVD Blu-ray hotkeys.",
    kind="program",
    author="Bitmonster",
    guid="{4DBDFFA7-9E47-4782-B843-B196C74DE3EF}",
    version="1.2 beta 2",
    createMacrosOnAdd=True,
)

ACTIONS = [
#Navigation
    ("NavigationUp", "Navigation Up", "Navigates through disc menus.", "{Up}"),
    ("NavigationDown", "Navigation Down", "Navigates through disc menus.", "{Down}"),
    ("NavigationLeft", "Navigation Left", "Navigates through disc menus.", "{Left}"),
    ("NavigationRight", "Navigation Right", "Navigates through disc menus.", "{Right}"),
    ("NavigationEnter", "Navigation Enter", "Navigates through disc menus. (Has actually the same function as the Play action.)", "{Return}"),
    ("NextAudioStream", "Next audio stream", "Switches among available audio streams.", "h"),
    ("NextSubtitle", "Next subtitle", "Switches among available subtitles during playback.", "u"),
#Movie Disc Playback Controls 
    #("SelectSource", "Select source", "Click to view a pop-up list of the disc drives on your computer, or to open a disc folder on the hard drive.", "{LCtrl+O}"),
    ("Rewind", "Rewind", "Reverses through content at incremental speeds.", "b"),
    ("StepBackward", "Step backward", "Goes to previous frame.", "e"),
    ("PreviousChapter", "Previous chapter", "Returns to previous chapter.", "p"),
    ("Stop", "Stop", "Stops playback.", "s"),
    ("PlayPause", "Play/Pause", "Plays media or pauses playback.", "{Space}"),
    ("NextChapter", "Next chapter", "Jumps to next chapter.", "n"),
    ("FastForward", "Fast forward", "Fast forwards through the content at incremental speeds.", "f"),
    ("StepForward", "Step forward", "Goes to next frame.", "t"),
    ("Mute", "Mute", "Mute volume.", "q"),
    ("VolumeUp", "Volume up", "Increase volume.", "+"),
    ("VolumeDown", "Volume down", "Decrease volume.", "-"),
    ("Fullscreen", "Fullscreen", "Toggles between fullscreen and window mode.", "z"),
    ("EjectDisc", "Eject disc", "Ejects the disc in the selected disc drive.", "{LCtrl+E}"),
    ("PopupMenu", "PopupMenu", "During Blu-ray Disc playback, click this button to display the pop-up menu over the disc content.", "{Ctrl+P}"),
#Music Controls 
    #("MusicEqualizer", "Music equalizer", "When playing back music, click this button to access the equalizer presets used to enhance audio. The audio preset you should select, depends on the type audio or genre of music you are playing back.", "h"),
    ("Repeat", "Repeat", "Click this button during playback to repeat one or all of the songs in a folder/playlist.", "{Ctrl+R}"),
    ("Shuffle", "Shuffle", "Plays the music in a folder, playlist, or on a disc in random order.", "v"),
#Photo Tab Controls 
    #("RotateRight", "Rotate right", "Click to rotate the current photo 90 degrees in the clockwise direction.", "{Ctrl+.}"),
    ("RotateLeft", "Rotate left", "Click to rotate the current photo 90 degrees in the counterclockwise direction.", "{Ctrl+Decimal}"),
#Miscellaneous Hotkeys 
    #("SecondaryAudio", "Secondary Audio", "Enables/disables secondary audio.", "{LCtrl+D}"),
    #("PGtextST", "PG textST", "Enables/disables PG textST. When enabled, a BD-ROM player will present either a text subtitle stream or a presentation graphics subtitle stream, when available for a disc title.", "{LCtrl+G}"),
    ("Minimize", "Minimize", "Minimize CyberLink PowerDVD.", "{LCtrl+N}"),
    #("SecondarySubtitle", "Secondary Subtitle", "Enable/disable second subtitles.", "{LCtrl+U}"),
    #("SecondaryVideo", "Secondary Video", "Enable/disable secondary video.", "{LCtrl+V}"),
    #("ResumeVideo", "Resume Video", "When the video playback is paused, but the interactive menu is active, this will resume the video.", "{LCtrl+W}"),
    ("Close", "Close", "Close/shut down CyberLink PowerDVD program.", "{Ctrl+x}"),
    ("DolbyHeadphone", "Dolby Headphone", "Dolby Headphone.", "{Ctrl+q}"),
    #("PreviousScene", "Previous scene", "Previous scene (uses CyberLink Rich Video to detect scenes).", "{F6}"),
    #("SkipCommercial", "Skip commercial", "Skip commercial (uses CyberLink Rich Video to detect commercials).", "{F7}"),
    #("NextScene", "Next scene", "Next scene (uses CyberLink Rich Video to detect scenes).", "{F8}"),
    ("OSDDetails", "OSD Details", "Toggle OSD DVD playback details.", "d"),
    ("RootMenu", "Root menu", "Takes you to the DVD root menu.", "j"),
#Unknown
    ("MenuList", "Menu list", "Accesses all available DVD menus.", "l"),
    #("NextAngel", "Next angel", "Switches among available angles if any.", "a"),
    #("SayItAgain", "Say-It-Again", "Repeats the last dialog.", "w"),
    #("SeeItAll", "See-It-All", "Activates See-It-All function, refer to Blu-ray Disc Configuration.", "{LCtrl+S}"),
    #("CaptureFrame", "Capture frame", "Captures video content as bitmap image files. (Not supported during HD DVD and Blu-ray Disc playback.)", "c"),
]


gWindowMatcher = eg.WindowMatcher('PowerDVD{*}.exe')


class ActionPrototype(eg.ActionBase):

    def __call__(self):
        hwnds = gWindowMatcher()
        if hwnds:
            #eg.SendKeys(hwnds[0], self.value)
            eg.SendKeys(hwnds[0], self.value, "True")
        else:
            raise self.Exceptions.ProgramNotRunning



class PowerDvd(eg.PluginBase):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)

