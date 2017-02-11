# Plugins/Foobar2000COM/__init__.py
#
# Copyright (C) 2008 CHeitkamp
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


# Every EventGhost plugin should start with the definition of an
# eg.PluginInfo subclass.


eg.RegisterPlugin(
    name = "Foobar2000 (COM)",
    author = "CHeitkamp",
    version = "0.1." + "$LastChangedRevision: 0 $".split()[1],
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.foobar2000.org/">'
        'Foobar2000</a> audio player.'
        '\n'
        'This plugin requires Foobar v0.9 and <a href='
        '"http://foosion.foobar2000.org/">Foosion\'s COM Automation server</a>'
    ),
    createMacrosOnAdd = True,
    #url = "http://www.eventghost.org/forum/viewtopic.php?t=695",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC0UlEQVR42m1TO0hjURA9"
        "1/8nH+OPJdoYRIWgLgZhwUJsLFZUkG0iYiGCgnZpJKRQUDfEVhAsDWIRFSzURtlO0YiC"
        "pFAskxiiFnn5+Es0OzPw3GYHLu8+7sy5Z86ZqwDYaP2uq6v7YaYoKChAPp+XxXuOz89P"
        "KKVkfXx8IJlMZh8fH4N05FKUFBgZGfk1MDCA8vJySSoqKpK9pmkCRLh4f3/H29ub/L+8"
        "vODg4AC7u7v7qr6+Pup2u621tbXIZrOS2NzcjI6ODuzt7SGXy2FwcBCRSASXl5coKSlB"
        "cXExnp6e4PV6Y8pqtWrj4+OmsrIyocogTqcT7e3t2NzcRCqVwvT0NMLhMNbX14VBYWEh"
        "Xl9f+TypqqurE/39/WYG4GJihMXFRVRUVEgx91xVVSXgCwsLuLm5AecywPHxsaYqKysT"
        "nZ2dAsAFExMTcuP/Ymdnh2nDYDCIHtfX15qifhKNjY1m7qu0tBRzc3NoaGhAb2/vVyHr"
        "EAgEYLFYMD8/L/0zI9JFYxcSNTU1ZlbeZrOhp6cHPp8PJCyWlpZE1MnJSfj9fqyuruLo"
        "6AgnJyfiFgH9A2AGJpNJKE5NTSEejyMYDIp4ZDPsdju2t7cxNjaG+/t7YfAFQENkZvqZ"
        "TAazs7MYGhrC8vIyPB6PeL6xsSGM2FYWkmeEBadh0hRRT5CVZladFWfkra0tdHd3IxQK"
        "iQOkEU5PT0F2i43cLrsQi8U0RTcnWlpaeIpFMD5oa2vDysoKDg8PQS6JLjMzM4hGoyI0"
        "989s7+7uNGU0GjWHw2HiSdTfAdMeHh7G6OioJK6trYkeTF0Peg88mUlFlsW6urq+NTU1"
        "CTXdNr7J5XLh9vZWWuI50YMveXh4wMXFRVzR/35ra+vPvr4+cUF/dQxC7iCdTouVPL5c"
        "yPH8/Izz83OcnZ39YQA7LS89nu9UaGQ7GUBnwm3prXGw0BSZq6urEH09fwEfgnAhbyFf"
        "mQAAAABJRU5ErkJggg=="
    ),
)

# changelog:
# 0.0 by CHeitkamp
#     - initial prerelease version


# Now import some other modules that are needed for the special purpose of
# this plugin.
import win32com.client

# Base class for all Actions
class FoobarActionClass(eg.ActionClass):

    def getFb2kObj(self):
        try:
            return win32com.client.Dispatch("Foobar2000.Application.0.7")
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")
            raise

    def getPlaybackObj(self):
        fb2k = self.getFb2kObj()
        return fb2k.Playback

    def getPlaylistsObj(self):
        fb2k = self.getFb2kObj()
        return fb2k.Playlists


class Play(FoobarActionClass):
    name = "Play"
    description = "Simulate a press on the play button."

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                fb2kPlayback.Pause()
            else:
                fb2kPlayback.Start(1)
        except:
            return


class Pause(FoobarActionClass):
    name = "Pause"
    description = "Simulate a press on the pause button."

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                fb2kPlayback.Pause()
        except:
            return


class Stop(FoobarActionClass):
    name = "Stop"
    description = "Simulate a press on the stop button."

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            fb2kPlayback.Stop()
        except:
            return


class Forward(FoobarActionClass):
    name = "Forward"
    description = "Fast-forward x sec."

    def __call__(self,seconds=10):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                fb2kPlayback.SeekRelative(seconds)
        except:
            return

    def GetLabel(self, seconds):
        return "Forward: %d seconds" % seconds

    def Configure(self,seconds=10):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(seconds,min=0)
        panel.AddLine("Forward ", valueCtrl, " seconds.")
        while panel.Affirmed():
            panel.SetResult(int(valueCtrl.GetValue()))


class Rewind(FoobarActionClass):
    name = "Rewind"
    description = "Fast-rewind x sec."

    def __call__(self,seconds=10):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                fb2kPlayback.SeekRelative(-seconds)
        except:
            return

    def GetLabel(self, seconds):
        return "Rewind: %d seconds" % seconds

    def Configure(self,seconds=10):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(seconds,min=0)
        panel.AddLine("Rewind", valueCtrl, " seconds.")
        while panel.Affirmed():
            panel.SetResult(int(valueCtrl.GetValue()))


class Next(FoobarActionClass):
    name = "Next Track"
    description = "Simulate a press on the next track button."

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            fb2kPlayback.Next()
        except:
            return


class Previous(FoobarActionClass):
    name = "Previous Track"
    description = "Simulate a press on the previous track button."

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            fb2kPlayback.Previous()
        except:
            return


class GetFormatTitle(FoobarActionClass):
    name = "GetFormatTitle"
    description = "Get Formated Title"

    def __call__(self,titlestring="%artist% - %title%"):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                return fb2kPlayback.FormatTitle(titlestring).encode("unicode_escape")
            else:
                return ""
        except:
            return "ERROR"

    def GetLabel(self, titlestring):
        return "GetFormatTitle: '%s'" % titlestring

    def Configure(self,titlestring="%artist% - %title%"):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.TextCtrl(titlestring)
        panel.AddLine("Format", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class GetArtist(FoobarActionClass):
    name = "GetArtist"
    description = "Get Track Artist - or '' when not playing"

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                return fb2kPlayback.FormatTitle("%artist%").encode("unicode_escape")
            else:
                return ""
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")
            return "ERROR"


class GetTitle(FoobarActionClass):
    name = "GetTitle"
    description = "Get Track Title - or '' when not playing"

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                return fb2kPlayback.FormatTitle("%title%").encode("unicode_escape")
            else:
                return ""
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")
            return "ERROR"


class GetElapsed(FoobarActionClass):
    name = "GetElapsed"
    description = "Get Track elapsed Time - or 0 when not playing"

    def __call__(self):
        try:
            fb2kPlayback = self.getPlaybackObj()
            if fb2kPlayback.IsPlaying:
                return fb2kPlayback.Position
            else:
                return "0"
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")


class GetDuration(FoobarActionClass):
    name = "GetDuration"
    description = "Get Track length - or 0 when not playing"

    def __call__(self):
        try:
            if fb2kPlayback.IsPlaying:
                return fb2kPlayback.Length
            else:
                return "0"
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")


class ShowHide(FoobarActionClass):
    name = "Show / Hide"
    description = "Show / Hide program"

    def __call__(self):
        try:
            fb2k = self.getFb2kObj()
            fb2k.Minimized = not fb2k.Minimized
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")


class Playlist(FoobarActionClass):
    name = "Playlist"
    description = "Playlist"

    def __call__(self):
        try:
            fb2kPlaylists = self.getPlaylistsObj()
            for pls in fb2kPlaylists:
                self.PrintError("Playlist: [%s] %i Tracks" % (pls.Name, pls.GetTracks().Count))
            apls= fb2kPlaylists.ActivePlaylist
            self.PrintError("Aktive Playlist [%s]" % (apls.Name))
        except:
            self.PrintError("Error connecting to Foobar2000 COM-Server")


# Now we can start to define the plugin by subclassing eg.PluginClass
class Foobar2000COM(eg.PluginClass):

    def __init__(self):
        group= self.AddGroup("Playback Control", "Playback Control Functions\ne.g. Play/Pause")
        group.AddAction(Play)
        group.AddAction(Pause)
        group.AddAction(Stop)
        group.AddAction(Forward)
        group.AddAction(Rewind)
        group.AddAction(Next)
        group.AddAction(Previous)
        group= self.AddGroup("Info", "Status Informations")
        group.AddAction(GetFormatTitle)
        group.AddAction(GetArtist)
        group.AddAction(GetTitle)
        group.AddAction(GetElapsed)
        group.AddAction(GetDuration)
        group= self.AddGroup("Miscellaneous", "Miscellaneous Functions")
        group.AddAction(ShowHide)
        group.AddAction(Playlist)
