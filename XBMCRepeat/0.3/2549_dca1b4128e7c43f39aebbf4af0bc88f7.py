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
    name = "XBMCRepeat",
    author = "Joni Boren",
    version = "0.3",
    kind = "program",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1005",
    description = "Adds actions buttons to control <a href='http://www.xbmc.org/'>XBMC</a>.",
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

# from threading import Event, Thread

# Windows availible in XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Window_IDs
"""
"""

WINDOWS = (
(eg.ActionGroup, "Windows", "Windows", None, (
    ("MyMovies", "Show Movies Screen", "Show Movies screen.", "ActivateWindow(MyVideoLibrary,movietitles,return)"),
    ("MyTVShows", "Show TV Shows Screen", "Show TV Shows screen.", "ActivateWindow(MyVideoLibrary,tvshowtitles,return)"),
    ("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "ActivateWindow(ShutdownMenu)"),
    ("Home", "Home", "Home", "Activatewindow(Home)"),
    ("Programs", "Programs", "Programs", "Activatewindow(Programs)"),
    ("Pictures", "Pictures", "Pictures", "Activatewindow(Pictures)"),
    ("Files", "Files", "Files", "Activatewindow(Files)"),
    ("Settings", "Settings", "Settings", "Activatewindow(Settings)"),
    ("Music", "Music", "Music", "Activatewindow(Music)"),
    ("Musicfiles", "Musicfiles", "Musicfiles", "Activatewindow(Musicfiles)"),
    ("Musiclibrary", "Musiclibrary", "Musiclibrary", "Activatewindow(Musiclibrary)"),
    ("Musicplaylist", "Musicplaylist", "Musicplaylist", "Activatewindow(Musicplaylist)"),
    ("Musicplaylisteditor", "Musicplaylisteditor", "Musicplaylisteditor", "Activatewindow(Musicplaylisteditor)"),
    ("Musicinformation", "Musicinformation", "Musicinformation", "Activatewindow(Musicinformation)"),
    ("Video", "Video", "Video", "Activatewindow(Video)"),
    ("Videofiles", "Videofiles", "Videofiles", "Activatewindow(Videofiles)"),
    ("Videolibrary", "Videolibrary", "Videolibrary", "Activatewindow(Videolibrary)"),
    ("Videoplaylist", "Videoplaylist", "Videoplaylist", "Activatewindow(Videoplaylist)"),
    ("Systeminfo", "Systeminfo", "Systeminfo", "Activatewindow(Systeminfo)"),
    ("Guicalibration", "Guicalibration", "Guicalibration", "Activatewindow(Guicalibration)"),
    ("Screencalibration", "Screencalibration", "Screencalibration", "Activatewindow(Screencalibration)"),
    ("Picturessettings", "Picturessettings", "Picturessettings", "Activatewindow(Picturessettings)"),
    ("Programssettings", "Programssettings", "Programssettings", "Activatewindow(Programssettings)"),
    ("Weathersettings", "Weathersettings", "Weathersettings", "Activatewindow(Weathersettings)"),
    ("Musicsettings", "Musicsettings", "Musicsettings", "Activatewindow(Musicsettings)"),
    ("Systemsettings", "Systemsettings", "Systemsettings", "Activatewindow(Systemsettings)"),
    ("Videossettings", "Videossettings", "Videossettings", "Activatewindow(Videossettings)"),
    ("Networksettings", "Networksettings", "Networksettings", "Activatewindow(Networksettings)"),
    ("Appearancesettings", "Appearancesettings", "Appearancesettings", "Activatewindow(Appearancesettings)"),
    ("Scripts", "Scripts", "Scripts", "Activatewindow(Scripts)"),
    ("Gamesaves", "Gamesaves", "Gamesaves", "Activatewindow(Gamesaves)"),
    ("Profiles", "Profiles", "Profiles", "Activatewindow(Profiles)"),
    ("Virtualkeyboard", "Virtualkeyboard", "Virtualkeyboard", "Activatewindow(Virtualkeyboard)"),
    ("Volumebar", "Volumebar", "Volumebar", "Activatewindow(Volumebar)"),
    ("Favourites", "Favourites", "Favourites", "Activatewindow(Favourites)"),
    ("Musicosd", "Musicosd", "Musicosd", "Activatewindow(Musicosd)"),
    ("Visualisationsettings", "Visualisationsettings", "Visualisationsettings", "Activatewindow(Visualisationsettings)"),
    ("Visualisationpresetlist", "Visualisationpresetlist", "Visualisationpresetlist", "Activatewindow(Visualisationpresetlist)"),
    ("Osdvideosettings", "Osdvideosettings", "Osdvideosettings", "Activatewindow(Osdvideosettings)"),
    ("Osdaudiosettings", "Osdaudiosettings", "Osdaudiosettings", "Activatewindow(Osdaudiosettings)"),
    ("Videobookmarks", "Videobookmarks", "Videobookmarks", "Activatewindow(Videobookmarks)"),
    ("Profilesettings", "Profilesettings", "Profilesettings", "Activatewindow(Profilesettings)"),
    ("Locksettings", "Locksettings", "Locksettings", "Activatewindow(Locksettings)"),
    ("Contentsettings", "Contentsettings", "Contentsettings", "Activatewindow(Contentsettings)"),
    ("Networksetup", "Networksetup", "Networksetup", "Activatewindow(Networksetup)"),
    ("Smartplaylisteditor", "Smartplaylisteditor", "Smartplaylisteditor", "Activatewindow(Smartplaylisteditor)"),
    ("Smartplaylistrule", "Smartplaylistrule", "Smartplaylistrule", "Activatewindow(Smartplaylistrule)"),
    ("Movieinformation", "Movieinformation", "Movieinformation", "Activatewindow(Movieinformation)"),
    ("Scriptsdebuginfo", "Scriptsdebuginfo", "Scriptsdebuginfo", "Activatewindow(Scriptsdebuginfo)"),
    ("Fullscreenvideo", "Fullscreenvideo", "Fullscreenvideo", "Activatewindow(Fullscreenvideo)"),
    ("Visualisation", "Visualisation", "Visualisation", "Activatewindow(Visualisation)"),
    ("Slideshow", "Slideshow", "Slideshow", "Activatewindow(Slideshow)"),
    ("Filestackingdialog", "Filestackingdialog", "Filestackingdialog", "Activatewindow(Filestackingdialog)"),
    ("Weather", "Weather", "Weather", "Activatewindow(Weather)"),
    ("Screensaver", "Screensaver", "Screensaver", "Activatewindow(Screensaver)"),
    ("Videoosd", "Videoosd", "Videoosd", "Activatewindow(Videoosd)"),
    ("Videomenu", "Videomenu", "Videomenu", "Activatewindow(Videomenu)"),
    ("Filebrowser", "Filebrowser", "Filebrowser", "Activatewindow(Filebrowser)"),
    ("Startup", "Startup", "Startup", "Activatewindow(Startup)"),
    ("Startwindow", "Startwindow", "Startwindow", "Activatewindow(Startwindow)"),
    ("Loginscreen", "Loginscreen", "Loginscreen", "Activatewindow(Loginscreen)"),
    ("Musicoverlay", "Musicoverlay", "Musicoverlay", "Activatewindow(Musicoverlay)"),
    ("Videooverlay", "Videooverlay", "Videooverlay", "Activatewindow(Videooverlay)"),
    ("Pictureinfo", "Pictureinfo", "Pictureinfo", "Activatewindow(Pictureinfo)"),
    ("Pluginsettings", "Pluginsettings", "Pluginsettings", "Activatewindow(Pluginsettings)"),
    ("Fullscreeninfo", "Fullscreeninfo", "Fullscreeninfo", "Activatewindow(Fullscreeninfo)"),
)),
)
# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC

GENERAL_ACTIONS = (
(eg.ActionGroup, "General actions", "General actions", None, (
    ("Left", "Left", "Move left off a control.", "Left"),
    ("Right", "Right", "Move right off a control.", "Right"),
    ("Up", "Up", "Move up off a control.", "Up"),
    ("Down", "Down", "Move down off a control.", "Down"),
    ("PageUp", "Page Up", "Scroll up on page in a list, thumb, or text view.", "PageUp"),
    ("PageDown", "Page Down", "Scroll down on page in a list, thumb, or text view.", "PageDown"),
    ("Select", "Select", "Select a button, or an item from a list of thumb view.", "Select"),
    ("Highlight", "Highlight", "Highlight an item in a list or thumb view.", "highlight"),
    ("ParentDir", "ParentDir", "Go up a folder to the parent folder.", "parentdir"),
    ("PreviousMenu", "PreviousMenu", "Go back to the previous menu screen.", "previousmenu"),
    ("Info", "Info", "Show the information about the currently highlighted item, or currently playing item.", "info"),
    ("Screenshot", "Screenshot", "Take a screenshot of the current screen..", "Screenshot"),
    ("PowerOff", "PowerOff", "Shutdown and power off.", "PowerOff"),
    ("VolumeUp", "VolumeUp", "Increase the volume of playback..", "VolumeUp"),
    ("VolumeDown", "VolumeDown", "Decrease the volume of playback..", "VolumeDown"),
    ("Mute", "Mute", "Mute the volume..", "Mute"),
    ("ContextMenu", "ContextMenu", "Pops up a contextual menu.", "ContextMenu"),
    ("ScrollUp", "ScrollUp", "Variable speed scroll up for analog keys (stick or triggers).", "ScrollUp"),
    ("ScrollDown", "ScrollDown", "Variable speed scroll down for analog keys (stick or triggers).", "ScrollDown"),
    ("Close", "Close", "Used to close a dialog.", "Close"),
    ("Number0", "Number0", "Used to input the number 0.", "Number0"),
    ("Number1", "Number1", "Used to input the number 1.", "Number1"),
    ("Number2", "Number2", "Used to input the number 2.", "Number2"),
    ("Number3", "Number3", "Used to input the number 3.", "Number3"),
    ("Number4", "Number4", "Used to input the number 4.", "Number4"),
    ("Number5", "Number5", "Used to input the number 5.", "Number5"),
    ("Number6", "Number6", "Used to input the number 6.", "Number6"),
    ("Number7", "Number7", "Used to input the number 7.", "Number7"),
    ("Number8", "Number8", "Used to input the number 8.", "Number8"),
    ("Number9", "Number9", "Used to input the number 9.", "Number9"),
)),
)

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_while_video_or_music_are_playing

MEDIA_PLAYING_ACTIONS = (
(eg.ActionGroup, "Media plying actions", "Media plying actions", None, (
    ("Play", "Play", "Play the selected item (or folder of items), or unpause a paused item..", "Play"),
    ("Pause", "Pause", " Pause the currently playing item. .", "Pause"),
    ("Stop", "Stop", " Stop the currently playing item. .", "Stop"),
    ("FastForward", "FastForward", "Toggle the fastforward speed between normal play, 2x, 4x, 8x, 16x, and 32x..", "FastForward"),
    ("Rewind", "Rewind", "Toggle the rewind speed between normal play, 2x, 4x, 8x, 16x, and 32x..", "Rewind"),
    ("SkipNext", "SkipNext", "Skip to the next item in a playlist..", "SkipNext"),
    ("SkipPrevious", "SkipPrevious", "Skip to the previous item in a playlist..", "SkipPrevious"),
    ("FullScreen", "FullScreen", "Toggles fullscreen modes (either visualisation or video playback).", "FullScreen"),
    ("CodecInfo", "CodecInfo", "Show codec information about the currently playing item (during video or visualisation playback).", "CodecInfo"),
    ("AnalogSeekForward", "AnalogSeekForward", "Variable speed seeking for analog keys (stick or triggers).", "AnalogSeekForward"),
    ("AnalogSeekBack", "AnalogSeekBack", "Variable speed seeking for analog keys (stick or triggers).", "AnalogSeekBack"),
    ("AnalogFastForward", "AnalogFastForward", "Variable speed fast forward for analog keys (stick or triggers).", "AnalogFastForward"),
    ("AnalogRewind", "AnalogRewind", "Variable speed rewind for analog keys (stick or triggers).", "AnalogRewind"),
    ("PartyMode", "Party Mode", "Party mode.", "PlayerControl(PartyMode)"),
    ("Random", "Random", "Random.", "PlayerControl(Random)"),
    ("Repeat", "Repeat", "Repeat.", "PlayerControl(Repeat)"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "UpdateLibrary(Video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "UpdateLibrary(Music)"),
    ("IncreaseRating", "IncreaseRating", "Unused.", "IncreaseRating"),
    ("DecreaseRating", "DecreaseRating", "Unused .", "DecreaseRating"),
    ("EjectTray", "Eject Tray", "Close or open the DVD tray.", "EjectTray"),
    ("Record", "Record", "Starts recording.", "Record"),
    ("PlayDVD", "Play DVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive.", "PlayDVD"),
    ("LastFMLove", "Last FM Love", "Add the current playing last.fm radio track to the last.fm loved tracks.", "LastFM.Love"),
    ("LastFMBan", "Last FM Ban", "Ban the current playing last.fm radio track.", "LastFM.Ban"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Music_and_Videos_windows_only

PLAYLIST_ACTIONS = (
(eg.ActionGroup, "Playlist actions", "Playlist actions", None, (
    ("Playlist", "Playlist", "Toggle to playlist view from My Music or My Videos.", "Playlist"),
    ("Queue", "Queue", "Queue the item to the current playlist.", "Queue"),
    ("MoveItemUp", "MoveItemUp", "Used to rearrange playlists.", "MoveItemUp"),
    ("MoveItemDown", "MoveItemDown", "Used to rearrange playlists.", "MoveItemDown"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Full_Screen_Video

FULLSCREEN_VIDEO_ACTIONS = (
(eg.ActionGroup, "Fullscreen video actions", "Actions available only in Full Screen Video", None, (
    ("StepForward", "StepForward", "Step forward 1% in the movie..", "StepForward"),
    ("StepBack", "StepBack", "Step back 1% in the movie..", "StepBack"),
    ("BigStepForward", "BigStepForward", "Step forward 10% in the movie..", "BigStepForward"),
    ("BigStepBack", "BigStepBack", "Step back 10% in the movie..", "BigStepBack"),
    ("SmallStepBack", "SmallStepBack", "Step back 7 seconds in the current video..", "SmallStepBack"),
    ("OSD", "OSD", "Toggles the OSD while playing an item..", "OSD"),
    ("AspectRatio", "AspectRatio", "Toggle through the various aspect ratio modes (Normal is the preferred option)..", "AspectRatio"),
    ("ShowSubtitles", "ShowSubtitles", "Toggles whether subtitles are shown or not..", "ShowSubtitles"),
    ("NextSubtitle", "NextSubtitle", "Change to the next subtitle language, if there is more than one..", "NextSubtitle"),
    ("SubtitleDelayMinus", "SubtitleDelayMinus", "Decrease the delay amount of subtitles (use if subtitles are displaying too late).", "SubtitleDelayMinus"),
    ("SubtitleDelayPlus", "SubtitleDelayPlus", "Increase the delay amount of subtitles (use if subtitles are displaying too early).", "SubtitleDelayPlus"),
    ("AudioDelayMinus", "AudioDelayMinus", "Decrease the delay amount of audio (use if audio is being heard too early).", "AudioDelayMinus"),
    ("AudioDelayPlus", "AudioDelayPlus", "Increase the delay amount of audio (use if audio is being heard too late).", "AudioDelayPlus"),
    ("AudioNextLanguage", "AudioNextLanguage", "Change to the next audio track in a video with multiple audio tracks..", "AudioNextLanguage"),
    ("mplayerosd", "mplayerosd", "Show Mplayer's OSD.", "mplayerosd"),
    ("ShowTime", "ShowTime", "Used to show the current play time in music + video playback.", "ShowTime"),
    ("ShowVideoMenu", "ShowVideoMenu", "Go to the DVD Video menu when playing a DVD..", "ShowVideoMenu"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_picture_slideshow

SLIDESHOW_ACTIONS = (
(eg.ActionGroup, "Picture slideshow actions", "Picture slideshow actions", None, (
    ("NextPicture", "NextPicture", "Move to the next picture in a slideshow..", "NextPicture"),
    ("PreviousPicture", "PreviousPicture", "Move to the previous picture in a slideshow..", "PreviousPicture"),
    ("ZoomOut", "ZoomOut", "Used in picture or slideshow to zoom out of the current image..", "ZoomOut"),
    ("ZoomIn", "ZoomIn", "Used in picture or slideshow to zoom in to the current image..", "ZoomIn"),
    ("ZoomNormal", "ZoomNormal", "Normal (fullscreen) viewing in My Pictures.", "ZoomNormal"),
    ("ZoomLevel1", "ZoomLevel1", "Zoom to 120% in My Pictures.", "ZoomLevel1"),
    ("ZoomLevel2", "ZoomLevel2", "Zoom to 150% in My Pictures.", "ZoomLevel2"),
    ("ZoomLevel3", "ZoomLevel3", "Zoom to 200% in My Pictures.", "ZoomLevel3"),
    ("ZoomLevel4", "ZoomLevel4", "Zoom to 280% in My Pictures.", "ZoomLevel4"),
    ("ZoomLevel5", "ZoomLevel5", "Zoom to 400% in My Pictures.", "ZoomLevel5"),
    ("ZoomLevel6", "ZoomLevel6", "Zoom to 600% in My Pictures.", "ZoomLevel6"),
    ("ZoomLevel7", "ZoomLevel7", "Zoom to 900% in My Pictures.", "ZoomLevel7"),
    ("ZoomLevel8", "ZoomLevel8", "Zoom to 1350% in My Pictures.", "ZoomLevel8"),
    ("ZoomLevel9", "ZoomLevel9", "Zoom to 2000% in My Pictures.", "ZoomLevel9"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures..", "AnalogMove"),
    ("Rotate", "Rotate", "Rotate a picture in My Pictures.", "Rotate"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_screen_calibration

CALIBRATION_ACTIONS = (
(eg.ActionGroup, "Screen calibration actions", "Screen calibration actions", None, (
    ("NextCalibration", "NextCalibration", "Used in Video + GUI calibration.", "NextCalibration"),
    ("ResetCalibration", "ResetCalibration", "Used in Video + GUI calibration.", "ResetCalibration"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures..", "AnalogMove"),
    ("NextResolution", "NextResolution", "Used in Video calibration.", "NextResolution"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_File_Manager

FILEMANAGER_ACTIONS = (
(eg.ActionGroup, "File Manager actions", "File Manager actions", None, (
    ("Delete", "Delete", "Used in My Files to delete a file..", "Delete"),
    ("Copy", "Copy", "Used in My Files to copy a file..", "Copy"),
    ("Move", "Move", "Used in My Files to move a file..", "Move"),
    ("Rename", "Rename", "Used in My Files to rename a file..", "Rename"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_on-screen_keyboard

ON_SCREEN_KEYBOARD_ACTIONS = (
(eg.ActionGroup, "On-screen keyboard actions", "On-screen keyboard actions", None, (
    ("BackSpace", "BackSpace", "Used in the virtual keyboards to delete one letter..", "BackSpace"),
    ("Shift", "Shift", "Used in Virtual Keyboard to switch to upper or lower case letters.", "Shift"),
    ("Symbols", "Symbols", "Used in Virtual Keyboard to switch to or from symbols mode.", "Symbols"),
    ("CursorLeft", "CursorLeft", "Used in Virtual Keyboard to move the current cursor point to the left.", "CursorLeft"),
    ("CursorRight", "CursorRight", "Used in Virtual Keyboard to move the current cursor point to the right.", "CursorRight"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_music_visualisation

VISUALISATION_ACTIONS = (
(eg.ActionGroup, "Music visualisation actions", "Music visualisation actions", None, (
    ("OSD", "OSD", "Toggles the OSD while playing an item..", "OSD"),
    ("ShowPreset", "ShowPreset", "Shows the current visualisation preset (milkdrop/spectrum).", "ShowPreset"),
    ("PresetList", "PresetList", "Pops up the visualisation preset list (milkdrop/spectrum).", "PresetList"),
    ("NextPreset", "NextPreset", "Next visualisation preset.", "NextPreset"),
    ("PreviousPreset", "PreviousPreset", "Previous visualisation preset.", "PreviousPreset"),
    ("LockPreset", "LockPreset", "Lock the current visualisation preset.", "LockPreset"),
    ("RandomPreset", "RandomPreset", "Switch to a new random preset.", "RandomPreset"),
    ("increasevisrating", "increasevisrating", "increasevisrating.", "increasevisrating"),
    ("decreasevisrating", "decreasevisrating", "decreasevisrating.", "decreasevisrating"),
)),
)

SHUTDOWN_ACTIONS = (
(eg.ActionGroup, "Shutdown related actions", "Shutdown related actions", None, (
    ("Quit", "Quit XBMC", "Quit XBMC.", "Quit"),
    ("RestartApp", "Restart XBMC", "Restarts XBMC.", "RestartApp"),
    ("Reset", "Reset Computer", "Reset the computer.", "Reset"),
    ("Shutdown", "Shutdown Computer", "Trigger default Shutdown action defined in System Settings, Default Quit on Windows.", "Shutdown"),
    ("Powerdown", "Powerdown Computer", "Powerdown system.", "Powerdown"),
    ("Suspend", "Suspend Computer", "Suspends (S3 / S1 depending on bios setting) the System.", "Suspend"),
    ("Hibernate", "Hibernate Computer", "Hibernate (S5) the System.", "Hibernate"),
    ("Reboot", "Reboot Computer", "Cold reboots the system (power cycle).", "Reboot"),
    ("Restart", "Restart Computer", "Cold reboots the system (power cycle).", "Restart"),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://xbmc.org/wiki/?title=Keymap.xml#Remote_Buttons

REMOTE_BUTTONS = (
(eg.ActionGroup, "Remote", "Remote", None, (
    ("Left", "Left", "Move left off a control.", "left"),
    ("Right", "Right", "Move right off a control.", "right"),
    ("Up", "Up", "Move up off a control.", "up"),
    ("Down", "Down", "Move down off a control.", "down"),
    ("Select", "Select", "Select a button, or an item from a list of thumb view.", "select"),
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

# Remote buttons handled by XBMC.  For a list of all buttons see: http://xbmc.org/wiki/?title=Keymap.xml#Gamepad_Buttons

GAMEPAD_BUTTONS = (
(eg.ActionGroup, "Gamepad", "Gamepad", None, (
    ("a", "a", "a.", "a"),
    ("b", "b", "b.", "b"),
    ("x", "x", "x.", "x"),
    ("y", "y", "y.", "y"),
    ("white", "white", "white.", "white"),
    ("black", "black", "black.", "black"),
    ("start", "start", "start.", "start"),
    ("back", "back", "back.", "back"),
    ("leftthumbbutton", "leftthumbbutton", "leftthumbbutton.", "leftthumbbutton"),
    ("rightthumbbutton", "rightthumbbutton", "rightthumbbutton.", "rightthumbbutton"),
    ("leftthumbstick", "leftthumbstick", "leftthumbstick.", "leftthumbstick"),
    ("leftthumbstickup", "leftthumbstickup", "leftthumbstickup.", "leftthumbstickup"),
    ("leftthumbstickdown", "leftthumbstickdown", "leftthumbstickdown.", "leftthumbstickdown"),
    ("leftthumbstickleft", "leftthumbstickleft", "leftthumbstickleft.", "leftthumbstickleft"),
    ("leftthumbstickright", "leftthumbstickright", "leftthumbstickright.", "leftthumbstickright"),
    ("rightthumbstick", "rightthumbstick", "rightthumbstick.", "rightthumbstick"),
    ("rightthumbstickup", "rightthumbstickup", "rightthumbstickup.", "rightthumbstickup"),
    ("rightthumbstickdown", "rightthumbstickdown", "rightthumbstickdown.", "rightthumbstickdown"),
    ("rightthumbstickleft", "rightthumbstickleft", "rightthumbstickleft.", "rightthumbstickleft"),
    ("rightthumbstickright", "rightthumbstickright", "rightthumbstickright.", "rightthumbstickright"),
    ("lefttrigger", "lefttrigger", "lefttrigger.", "lefttrigger"),
    ("righttrigger", "righttrigger", "righttrigger.", "righttrigger"),
    ("leftanalogtrigger", "leftanalogtrigger", "leftanalogtrigger.", "leftanalogtrigger"),
    ("rightanalogtrigger", "rightanalogtrigger", "rightanalogtrigger.", "rightanalogtrigger"),
    ("dpadleft", "dpadleft", "dpadleft.", "dpadleft"),
    ("dpadright", "dpadright", "dpadright.", "dpadright"),
    ("dpadup", "dpadup", "dpadup.", "dpadup"),
    ("dpaddown", "dpaddown", "dpaddown.", "dpaddown"),
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
            packet = PacketBUTTON(map_name=str("R1"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class GamepadPrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("XG"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

#class StopRepeating(eg.ActionClass):
#    name = "Stop Repeating"
#    description = "Stops a button repeating."

#    def __call__(self):
#        try:
#            self.plugin.xbmc.release_button()
#        except:
#            raise self.Exceptions.ProgramNotRunning


# And now we define the actual plugin:

class XBMC(eg.PluginClass):
    def __init__(self):
        self.AddActionsFromList(REMOTE_BUTTONS, ButtonPrototype)
        self.AddActionsFromList(GAMEPAD_BUTTONS, GamepadPrototype)
        self.AddActionsFromList(WINDOWS, ActionPrototype)
        self.AddActionsFromList(GENERAL_ACTIONS, ActionPrototype)
        self.AddActionsFromList(MEDIA_PLAYING_ACTIONS, ActionPrototype)
        self.AddActionsFromList(PLAYLIST_ACTIONS, ActionPrototype)
        self.AddActionsFromList(FULLSCREEN_VIDEO_ACTIONS, ActionPrototype)
        self.AddActionsFromList(SLIDESHOW_ACTIONS, ActionPrototype)
        self.AddActionsFromList(CALIBRATION_ACTIONS, ActionPrototype)
        self.AddActionsFromList(FILEMANAGER_ACTIONS, ActionPrototype)
        self.AddActionsFromList(ON_SCREEN_KEYBOARD_ACTIONS, ActionPrototype)
        self.AddActionsFromList(VISUALISATION_ACTIONS, ActionPrototype)
        self.AddActionsFromList(SHUTDOWN_ACTIONS, ActionPrototype)
#        self.AddAction(StopRepeating)
        self.xbmc = XBMCClient("EventGhost")

    def __start__(self):
        try:
            self.xbmc.connect()
#            self.stopThreadEvent = Event()
#            thread = Thread(target=self.ThreadWorker, args=(self.stopThreadEvent,))
#            thread.start()
        except:
            raise self.Exceptions.ProgramNotRunning

    def __stop__(self):
        try:
#            self.stopThreadEvent.set()
            self.xbmc.close()
        except:
            pass

    def __close__(self):
        pass

#    def ThreadWorker(self, stopThreadEvent):
#        while not stopThreadEvent.isSet():
#            self.TriggerEvent("MyTimerEvent")
#            stopThreadEvent.wait(10.0)
