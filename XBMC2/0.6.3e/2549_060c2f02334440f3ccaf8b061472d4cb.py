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
import urllib
import json
import ast
import xml.dom.minidom
from xml.dom.minidom import Node

from threading import Event, Thread
import re

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "XBMC2",
    author = "Joni Boren",
    version = "0.6.3e",
    kind = "program",
    guid = "{8C8B850C-773F-4583-AAD9-A568262B7933}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=10&t=1562",
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
    ("MyMovies", "Show Movies Screen", "Show Movies screen.", "Activatewindow(MyVideoLibrary,movietitles,return)"),
    ("MyTVShows", "Show TV Shows Screen", "Show TV Shows screen.", "Activatewindow(MyVideoLibrary,tvshowtitles,return)"),
    ("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "Activatewindow(ShutdownMenu)"),
    ("Home", "Home", "WINDOW_HOME", "Activatewindow(Home)"),
    ("Programs", "Programs", "WINDOW_PROGRAMS", "Activatewindow(Programs)"),
    ("Pictures", "Pictures", "WINDOW_PICTURES", "Activatewindow(Pictures)"),
    ("Files", "Files", "WINDOW_FILES\nbackward compat", "Activatewindow(Files)"),
    ("Settings", "Settings", "WINDOW_SETTINGS_MENU", "Activatewindow(Settings)"),
    ("Music", "Music", "WINDOW_MUSIC", "Activatewindow(Music)"),
    ("Musicfiles", "Musicfiles", "WINDOW_MUSIC_FILES", "Activatewindow(Musicfiles)"),
    ("Musiclibrary", "Musiclibrary", "WINDOW_MUSIC_NAV", "Activatewindow(Musiclibrary)"),
    ("Musicplaylist", "Musicplaylist", "WINDOW_MUSIC_PLAYLIST", "Activatewindow(Musicplaylist)"),
    ("Musicplaylisteditor", "Musicplaylisteditor", "WINDOW_MUSIC_PLAYLIST_EDITOR", "Activatewindow(Musicplaylisteditor)"),
    ("Musicinformation", "Musicinformation", "WINDOW_DIALOG_MUSIC_INFO", "Activatewindow(Musicinformation)"),
    ("Video", "Video", "WINDOW_VIDEOS", "Activatewindow(Video)"),
    ("Videofiles", "Videofiles", "WINDOW_VIDEO_FILES", "Activatewindow(Videofiles)"),
    ("Videolibrary", "Videolibrary", "WINDOW_VIDEO_NAV", "Activatewindow(Videolibrary)"),
    ("Videoplaylist", "Videoplaylist", "WINDOW_VIDEO_PLAYLIST", "Activatewindow(Videoplaylist)"),
    ("Systeminfo", "Systeminfo", "WINDOW_SYSTEM_INFORMATION", "Activatewindow(Systeminfo)"),
    ("Guicalibration", "Guicalibration", "WINDOW_SCREEN_CALIBRATION\nbackward compat", "Activatewindow(Guicalibration)"),
    ("Screencalibration", "Screencalibration", "WINDOW_SCREEN_CALIBRATION", "Activatewindow(Screencalibration)"),
    ("Picturessettings", "Picturessettings", "WINDOW_SETTINGS_MYPICTURES", "Activatewindow(Picturessettings)"),
    ("Programssettings", "Programssettings", "WINDOW_SETTINGS_MYPROGRAMS", "Activatewindow(Programssettings)"),
    ("Weathersettings", "Weathersettings", "WINDOW_SETTINGS_MYWEATHER", "Activatewindow(Weathersettings)"),
    ("Musicsettings", "Musicsettings", "WINDOW_SETTINGS_MYMUSIC", "Activatewindow(Musicsettings)"),
    ("Systemsettings", "Systemsettings", "WINDOW_SETTINGS_SYSTEM", "Activatewindow(Systemsettings)"),
    ("Videossettings", "Videossettings", "WINDOW_SETTINGS_MYVIDEOS", "Activatewindow(Videossettings)"),
    ("Networksettings", "Networksettings", "WINDOW_SETTINGS_NETWORK", "Activatewindow(Networksettings)"),
    ("Appearancesettings", "Appearancesettings", "WINDOW_SETTINGS_APPEARANCE", "Activatewindow(Appearancesettings)"),
    ("Scripts", "Scripts", "WINDOW_PROGRAMS\nbackward compat", "Activatewindow(Scripts)"),
    ("Gamesaves", "Gamesaves", "Gamesaves", "Activatewindow(Gamesaves)"),
    ("Profiles", "Profiles", "WINDOW_SETTINGS_PROFILES", "Activatewindow(Profiles)"),
    ("Virtualkeyboard", "Virtualkeyboard", "WINDOW_DIALOG_KEYBOARD", "Activatewindow(Virtualkeyboard)"),
    ("Volumebar", "Volumebar", "WINDOW_DIALOG_VOLUME_BAR", "Activatewindow(Volumebar)"),
    ("Favourites", "Favourites", "WINDOW_DIALOG_FAVOURITES", "Activatewindow(Favourites)"),
    ("Musicosd", "Musicosd", "WINDOW_DIALOG_MUSIC_OSD", "Activatewindow(Musicosd)"),
    ("Visualisationsettings", "Visualisationsettings", "WINDOW_DIALOG_ADDON_SETTINGS\nbackward compat", "Activatewindow(Visualisationsettings)"),
    ("Visualisationpresetlist", "Visualisationpresetlist", "WINDOW_DIALOG_VIS_PRESET_LIST", "Activatewindow(Visualisationpresetlist)"),
    ("Osdvideosettings", "Osdvideosettings", "WINDOW_DIALOG_VIDEO_OSD_SETTINGS", "Activatewindow(Osdvideosettings)"),
    ("Osdaudiosettings", "Osdaudiosettings", "WINDOW_DIALOG_AUDIO_OSD_SETTINGS", "Activatewindow(Osdaudiosettings)"),
    ("Videobookmarks", "Videobookmarks", "WINDOW_DIALOG_VIDEO_BOOKMARKS", "Activatewindow(Videobookmarks)"),
    ("Profilesettings", "Profilesettings", "WINDOW_DIALOG_PROFILE_SETTINGS", "Activatewindow(Profilesettings)"),
    ("Locksettings", "Locksettings", "WINDOW_DIALOG_LOCK_SETTINGS", "Activatewindow(Locksettings)"),
    ("Contentsettings", "Contentsettings", "WINDOW_DIALOG_CONTENT_SETTINGS", "Activatewindow(Contentsettings)"),
    ("Networksetup", "Networksetup", "WINDOW_DIALOG_NETWORK_SETUP", "Activatewindow(Networksetup)"),
    ("Smartplaylisteditor", "Smartplaylisteditor", "WINDOW_DIALOG_SMART_PLAYLIST_EDITOR", "Activatewindow(Smartplaylisteditor)"),
    ("Smartplaylistrule", "Smartplaylistrule", "WINDOW_DIALOG_SMART_PLAYLIST_RULE", "Activatewindow(Smartplaylistrule)"),
    ("Movieinformation", "Movieinformation", "WINDOW_DIALOG_VIDEO_INFO", "Activatewindow(Movieinformation)"),
    ("Scriptsdebuginfo", "Scriptsdebuginfo", "Scriptsdebuginfo", "Activatewindow(Scriptsdebuginfo)"),
    ("Fullscreenvideo", "Fullscreenvideo", "WINDOW_FULLSCREEN_VIDEO", "Activatewindow(Fullscreenvideo)"),
    ("Visualisation", "Visualisation", "WINDOW_VISUALISATION", "Activatewindow(Visualisation)"),
    ("Slideshow", "Slideshow", "WINDOW_SLIDESHOW", "Activatewindow(Slideshow)"),
    ("Filestackingdialog", "Filestackingdialog", "WINDOW_DIALOG_FILESTACKING", "Activatewindow(Filestackingdialog)"),
    ("Weather", "Weather", "WINDOW_WEATHER", "Activatewindow(Weather)"),
    ("Screensaver", "Screensaver", "WINDOW_SCREENSAVER", "Activatewindow(Screensaver)"),
    ("Videoosd", "Videoosd", "WINDOW_DIALOG_VIDEO_OSD", "Activatewindow(Videoosd)"),
    ("Videomenu", "Videomenu", "WINDOW_VIDEO_MENU", "Activatewindow(Videomenu)"),
    ("Filebrowser", "Filebrowser", "WINDOW_DIALOG_FILE_BROWSER", "Activatewindow(Filebrowser)"),
    ("Startup", "Startup", "WINDOW_STARTUP_ANIM", "Activatewindow(Startup)"),
    ("Startwindow", "Startwindow", "WINDOW_START", "Activatewindow(Startwindow)"),
    ("Loginscreen", "Loginscreen", "WINDOW_LOGIN_SCREEN", "Activatewindow(Loginscreen)"),
    ("Musicoverlay", "Musicoverlay", "WINDOW_DIALOG_MUSIC_OVERLAY", "Activatewindow(Musicoverlay)"),
    ("Videooverlay", "Videooverlay", "WINDOW_DIALOG_VIDEO_OVERLAY", "Activatewindow(Videooverlay)"),
    ("Pictureinfo", "Pictureinfo", "WINDOW_DIALOG_PICTURE_INFO", "Activatewindow(Pictureinfo)"),
    ("Pluginsettings", "Pluginsettings", "Pluginsettings", "Activatewindow(Pluginsettings)"),
    ("Fullscreeninfo", "Fullscreeninfo", "WINDOW_DIALOG_FULLSCREEN_INFO", "Activatewindow(Fullscreeninfo)"),
    ("PlayerControls", "Player Controls", "WINDOW_DIALOG_PLAYER_CONTROLS", "Activatewindow(Playercontrols)"),
)),
)
# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC

GENERAL_ACTIONS = (
(eg.ActionGroup, "General", "General", None, (
    ("Left", "Left", "Move left off a control.", "left"),
    ("Right", "Right", "Move right off a control.", "right"),
    ("Up", "Up", "Move up off a control.", "up"),
    ("Down", "Down", "Move down off a control.", "down"),
    ("PageUp", "PageUp", "Scroll up on page in a list, thumb, or text view.", "pageup"),
    ("PageDown", "PageDown", "Scroll down on page in a list, thumb, or text view.", "pagedown"),
    ("Select", "Select", "Select a button, or an item from a list of thumb view.", "select"),
    ("Highlight", "Highlight", "Highlight an item in a list or thumb view.", "highlight"),
    ('Parentfolder', 'Parentfolder', 'Go up a folder to the parent folder.', 'parentfolder'),
    ('Back', 'Back', '', 'back'),
    ("ParentDir", "ParentDir", "Go up a folder to the parent folder.\n// backward compatibility", "parentdir"),
    ("PreviousMenu", "PreviousMenu", "Go back to the previous menu screen.", "previousmenu"),
    ("Info", "Info", "Show the information about the currently highlighted item, or currently playing item.", "info"),
    ("Screenshot", "Screenshot", "Take a screenshot of the current screen.", "screenshot"),
    ("PowerOff", "PowerOff", "Shutdown and power off.", "poweroff"),
    ("VolumeUp", "VolumeUp", "Increase the volume of playback.", "volumeup"),
    ("VolumeDown", "VolumeDown", "Decrease the volume of playback.", "volumedown"),
    ("Mute", "Mute", "Mute the volume.", "mute"),
    ("ContextMenu", "ContextMenu", "Pops up a contextual menu", "contextmenu"),
    ("ScrollUp", "ScrollUp", "Variable speed scroll up for analog keys (stick or triggers)", "scrollup"),
    ("ScrollDown", "ScrollDown", "Variable speed scroll down for analog keys (stick or triggers)", "scrolldown"),
    ("Close", "Close", "Used to close a dialog", "close"),
    ("Number0", "Number0", "Used to input the number 0", "number0"),
    ("Number1", "Number1", "Used to input the number 1", "number1"),
    ("Number2", "Number2", "Used to input the number 2", "number2"),
    ("Number3", "Number3", "Used to input the number 3", "number3"),
    ("Number4", "Number4", "Used to input the number 4", "number4"),
    ("Number5", "Number5", "Used to input the number 5", "number5"),
    ("Number6", "Number6", "Used to input the number 6", "number6"),
    ("Number7", "Number7", "Used to input the number 7", "number7"),
    ("Number8", "Number8", "Used to input the number 8", "number8"),
    ("Number9", "Number9", "Used to input the number 9", "number9"),
)),
)

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_while_video_or_music_are_playing

MEDIA_PLAYING_ACTIONS = (
(eg.ActionGroup, "MediaPlaying", "Media playing", None, (
    ("Play", "Play", "Play the selected item (or folder of items), or unpause a paused item.", "play"),
    ("Pause", "Pause", "Pause the currently playing item.", "pause"),
    ("Stop", "Stop", "Stop the currently playing item.", "stop"),
    ("FastForward", "FastForward", "Toggle the fastforward speed between normal play, 2x, 4x, 8x, 16x, and 32x.", "fastforward"),
    ("Rewind", "Rewind", "Toggle the rewind speed between normal play, 2x, 4x, 8x, 16x, and 32x.", "rewind"),
    ("SkipNext", "SkipNext", "Skip to the next item in a playlist or scene in a video.", "skipnext"),
    ("SkipPrevious", "SkipPrevious", "Skip to the previous item in a playlist or scene in a video.", "skipprevious"),
    ("FullScreen", "FullScreen", "Toggles fullscreen modes (either visualisation or video playback)", "fullscreen"),
    ("CodecInfo", "CodecInfo", "Show codec information about the currently playing item (during video or visualisation playback)", "codecinfo"),
    ("AnalogSeekForward", "AnalogSeekForward", "Variable speed seeking for analog keys (stick or triggers)", "analogseekforward"),
    ("AnalogSeekBack", "AnalogSeekBack", "Variable speed seeking for analog keys (stick or triggers)", "analogseekback"),
    ("AnalogFastForward", "AnalogFastForward", "Variable speed fast forward for analog keys (stick or triggers)", "analogfastforward"),
    ("AnalogRewind", "AnalogRewind", "Variable speed rewind for analog keys (stick or triggers)", "analogrewind"),
    ("PartyMode", "Party Mode", "Party mode.", "playercontrol(partymode)"),
    ("Random", "Random", "Toggles random playback", "playercontrol(Random,Notify)"),
    ("Repeat", "Repeat", "Cycles through the repeat modes", "playercontrol(Repeat,Notify)"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "updatelibrary(video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "updatelibrary(music)"),
    ("IncreaseRating", "IncreaseRating", "Unused.", "increaserating"),
    ("DecreaseRating", "DecreaseRating", "Unused .", "decreaserating"),
    ("EjectTray", "EjectTray", "Close or open the DVD tray", "EjectTray"),
    ("Record", "Record", "Starts recording.", "record"),
    ("PlayDVD", "PlayDVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive!", "PlayDVD"),
    ("LastFMLove", "LastFM.Love", "Add the current playing last.fm radio track to the last.fm loved tracks", "LastFM.Love"),
    ("LastFMBan", "LastFM.Ban", "Ban the current playing last.fm radio track", "LastFM.Ban"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Music_and_Videos_windows_only

PLAYLIST_ACTIONS = (
(eg.ActionGroup, "Playlist", "Playlist", None, (
    ("Playlist", "Playlist", "Toggle to playlist view from My Music or My Videos", "playlist"),
    ("Queue", "Queue", "Queue the item to the current playlist", "queue"),
    ("MoveItemUp", "MoveItemUp", "Used to rearrange playlists", "moveitemup"),
    ("MoveItemDown", "MoveItemDown", "Used to rearrange playlists", "moveitemdown"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Full_Screen_Video

FULLSCREEN_VIDEO_ACTIONS = (
(eg.ActionGroup, "FullscreenVideo", "FullScreen Video", None, (
    ("StepForward", "StepForward", "Step forward 1% in the movie.", "stepforward"),
    ("StepBack", "StepBack", "Step back 1% in the movie.", "stepback"),
    ("BigStepForward", "BigStepForward", "Step forward 10% in the movie.", "bigstepforward"),
    ("BigStepBack", "BigStepBack", "Step back 10% in the movie.", "bigstepback"),
    ("SmallStepBack", "SmallStepBack", "Step back 7 seconds in the current video.", "smallstepback"),
    ("OSD", "OSD", "Toggles the OSD while playing an item.", "osd"),
    ("AspectRatio", "AspectRatio", "Toggle through the various aspect ratio modes (Normal is the preferred option).", "aspectratio"),
    ("ShowSubtitles", "ShowSubtitles", "Toggles whether subtitles are shown or not.", "showsubtitles"),
    ("NextSubtitle", "NextSubtitle", "Change to the next subtitle language, if there is more than one.", "nextsubtitle"),
    ('Subtitledelay', 'SubtitleDelay', 'Show subtitle delay slider', 'subtitledelay'),
    ("SubtitleDelayMinus", "SubtitleDelayMinus", "Decrease the delay amount of subtitles (use if subtitles are displaying too late)", "subtitledelayminus"),
    ("SubtitleDelayPlus", "SubtitleDelayPlus", "Increase the delay amount of subtitles (use if subtitles are displaying too early)", "subtitledelayplus"),
    ('Audiodelay', 'AudioDelay', 'Show audio delay slider', 'audiodelay'),
    ("AudioDelayMinus", "AudioDelayMinus", "Decrease the delay amount of audio (use if audio is being heard too early)", "audiodelayminus"),
    ("AudioDelayPlus", "AudioDelayPlus", "Increase the delay amount of audio (use if audio is being heard too late)", "audiodelayplus"),
    ("AudioNextLanguage", "AudioNextLanguage", "Change to the next audio track in a video with multiple audio tracks.", "audionextlanguage"),
    ("mplayerosd", "MplayerOSD", "Show Mplayer's OSD", "mplayerosd"),
    ("ShowTime", "ShowTime", "Used to show the current play time in music + video playback", "showtime"),
    ("ShowVideoMenu", "ShowVideoMenu", "Go to the DVD Video menu when playing a DVD.", "showvideomenu"),
    ('Increasepar', 'IncreasePAR', 'Used in video fullscreen to increase the pixel aspect ratio (stretch).', 'increasepar'),
    ('Decreasepar', 'DecreasePAR', 'Used in video fullscreen to decrease the pixel aspect ratio (stretch).', 'decreasepar'),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_picture_slideshow

SLIDESHOW_ACTIONS = (
(eg.ActionGroup, "PictureSlideshow", "Picture slideshow", None, (
    ("NextPicture", "NextPicture", "Move to the next picture in a slideshow.", "nextpicture"),
    ("PreviousPicture", "PreviousPicture", "Move to the previous picture in a slideshow.", "previouspicture"),
    ("ZoomOut", "ZoomOut", "Used in picture, slideshow or video fullscreen to zoom out of the current image/video.", "zoomout"),
    ("ZoomIn", "ZoomIn", "Used in picture, slideshow or video fullscreen to zoom in to the current image/video.", "zoomin"),
    ("ZoomNormal", "ZoomNormal", "Normal (fullscreen) viewing in My Pictures", "zoomnormal"),
    ("ZoomLevel1", "ZoomLevel1", "Zoom to 120% in My Pictures", "zoomlevel1"),
    ("ZoomLevel2", "ZoomLevel2", "Zoom to 150% in My Pictures", "zoomlevel2"),
    ("ZoomLevel3", "ZoomLevel3", "Zoom to 200% in My Pictures", "zoomlevel3"),
    ("ZoomLevel4", "ZoomLevel4", "Zoom to 280% in My Pictures", "zoomlevel4"),
    ("ZoomLevel5", "ZoomLevel5", "Zoom to 400% in My Pictures", "zoomlevel5"),
    ("ZoomLevel6", "ZoomLevel6", "Zoom to 600% in My Pictures", "zoomlevel6"),
    ("ZoomLevel7", "ZoomLevel7", "Zoom to 900% in My Pictures", "zoomlevel7"),
    ("ZoomLevel8", "ZoomLevel8", "Zoom to 1350% in My Pictures", "zoomlevel8"),
    ("ZoomLevel9", "ZoomLevel9", "Zoom to 2000% in My Pictures", "zoomlevel9"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures.", "analogmove"),
    ("Rotate", "Rotate", "Rotate a picture in My Pictures", "rotate"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_screen_calibration

CALIBRATION_ACTIONS = (
(eg.ActionGroup, "ScreenCalibration", "Screen calibration", None, (
    ("NextCalibration", "NextCalibration", "Used in Video + GUI calibration", "nextcalibration"),
    ("ResetCalibration", "ResetCalibration", "Used in Video + GUI calibration", "resetcalibration"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures.", "analogmove"),
    ("NextResolution", "NextResolution", "Used in Video calibration", "nextresolution"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_File_Manager

FILEMANAGER_ACTIONS = (
(eg.ActionGroup, "FileManager", "File Manager", None, (
    ("Delete", "Delete", "Used in My Files to delete a file.", "delete"),
    ("Copy", "Copy", "Used in My Files to copy a file.", "copy"),
    ("Move", "Move", "Used in My Files to move a file.", "move"),
    ("Rename", "Rename", "Used in My Files to rename a file.", "rename"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_on-screen_keyboard

ON_SCREEN_KEYBOARD_ACTIONS = (
(eg.ActionGroup, "On-screenKeyboard", "On-screen keyboard", None, (
    ("BackSpace", "BackSpace", "Used in the virtual keyboards to delete one letter.", "backspace"),
    ("Shift", "Shift", "Used in Virtual Keyboard to switch to upper or lower case letters", "shift"),
    ("Symbols", "Symbols", "Used in Virtual Keyboard to switch to or from symbols mode", "symbols"),
    ("CursorLeft", "CursorLeft", "Used in Virtual Keyboard to move the current cursor point to the left", "cursorleft"),
    ("CursorRight", "CursorRight", "Used in Virtual Keyboard to move the current cursor point to the right", "cursorright"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_music_visualisation

VISUALISATION_ACTIONS = (
(eg.ActionGroup, "MusicVisualisation", "Music visualisation", None, (
    ("OSD", "OSD", "Toggles the OSD while playing an item.", "osd"),
    ("ShowPreset", "ShowPreset", "Shows the current visualisation preset (milkdrop/spectrum)", "showpreset"),
    ("PresetList", "PresetList", "Pops up the visualisation preset list (milkdrop/spectrum)", "presetlist"),
    ("NextPreset", "NextPreset", "Next visualisation preset", "nextpreset"),
    ("PreviousPreset", "PreviousPreset", "Previous visualisation preset", "previouspreset"),
    ("LockPreset", "LockPreset", "Lock the current visualisation preset", "lockpreset"),
    ("RandomPreset", "RandomPreset", "Switch to a new random preset", "randompreset"),
    ("increasevisrating", "IncreaseVisRating", "", "increasevisrating"),
    ("decreasevisrating", "DecreaseVisRating", "", "decreasevisrating"),
)),
)

SHUTDOWN_ACTIONS = (
(eg.ActionGroup, "ShutdownRelated", "Shutdown related", None, (
    ("Quit", "Quit", "Quit XBMC", "Quit"),
    ("RestartApp", "RestartApp", "Restart XBMC", "RestartApp"),
    ("Reset", "Reset Computer", "Reset the computer.", "reset"),
    ("Shutdown", "Shutdown Computer", "Trigger default Shutdown action defined in System Settings, Default Quit on Windows.", "shutdown"),
    ("Powerdown", "Powerdown", "Powerdown system", "Powerdown"),
    ("Suspend", "Suspend", "Suspends the system", "Suspend"),
    ("Hibernate", "Hibernate", "Hibernates the system", "Hibernate"),
    ("Reboot", "Reboot Computer", "Cold reboots the system (power cycle).", "reboot"),
    ("Restart", "Restart Computer", "Cold reboots the system (power cycle).", "restart"),
)),
)

UNCATEGORIZED_ACTIONS = (
(eg.ActionGroup, "UncategorizedActions", "Uncategorized actions", None, (
    ("JumpSMS2", "JumpSMS2", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms2"),
    ("JumpSMS3", "JumpSMS3", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms3"),
    ("JumpSMS4", "JumpSMS4", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms4"),
    ("JumpSMS5", "JumpSMS5", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms5"),
    ("JumpSMS6", "JumpSMS6", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms6"),
    ("JumpSMS7", "JumpSMS7", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms7"),
    ("JumpSMS8", "JumpSMS8", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms8"),
    ("JumpSMS9", "JumpSMS9", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms9"),
    ("FilterClear", "FilterClear", "", "filterclear"),
    ("FilterSMS2", "FilterSMS2", "Filter a list in music or videos using SMS-style input.", "filtersms2"),
    ("FilterSMS3", "FilterSMS3", "Filter a list in music or videos using SMS-style input.", "filtersms3"),
    ("FilterSMS4", "FilterSMS4", "Filter a list in music or videos using SMS-style input.", "filtersms4"),
    ("FilterSMS5", "FilterSMS5", "Filter a list in music or videos using SMS-style input.", "filtersms5"),
    ("FilterSMS6", "FilterSMS6", "Filter a list in music or videos using SMS-style input.", "filtersms6"),
    ("FilterSMS7", "FilterSMS7", "Filter a list in music or videos using SMS-style input.", "filtersms7"),
    ("FilterSMS8", "FilterSMS8", "Filter a list in music or videos using SMS-style input.", "filtersms8"),
    ("FilterSMS9", "FilterSMS9", "Filter a list in music or videos using SMS-style input.", "filtersms9"),
    ("FirstPage", "FirstPage", "", "firstpage"),
    ("LastPage", "LastPage", "", "lastpage"),

    ("HideSubMenu", "HideSubMenu", "<depreciated>", "hidesubmenu"),

    ("ToggleSource", "ToggleSource", "", "togglesource"),
    ("Remove", "Remove", "", "remove"),

    ("AudioToggleDigital", "AudioToggleDigital", "", "audiotoggledigital"),

    ("OSDLeft", "OSDLeft", "", "osdleft"),
    ("OSDRight", "OSDRight", "", "osdright"),
    ("OSDUp", "OSDUp", "", "osdup"),
    ("OSDDown", "OSDDown", "", "osddown"),
    ("OSDSelect", "OSDSelect", "", "osdselect"),
    ("OSDValuePlus", "OSDValuePlus", "", "osdvalueplus"),
    ("OSDValueMinus", "OSDValueMinus", "", "osdvalueminus"),

    ("ToggleWatched", "ToggleWatched", "Toggles watched/unwatched status for Videos", "togglewatched"),
    ("ScanItem", "ScanItem", "", "scanitem"),

    ("Enter", "Enter", "", "enter"),
    ("IncreaseRating", "IncreaseRating", "Unused", "increaserating"),
    ("DecreaseRating", "DecreaseRating", "Unused", "decreaserating"),
    ("ToggleFullScreen", "ToggleFullScreen", "", "togglefullscreen"),
    ("NextScene", "NextScene", "", "nextscene"),
    ("PreviousScene", "PreviousScene", "", "previousscene"),
    ("NextLetter", "NextLetter", "Move to the next letter in a list or thumb panel.  Note that SHIFT-B on the keyboard will take you to the B's.", "nextletter"),
    ("PrevLetter", "PrevLetter", "Move to the previous letter in a list or thumb panel.  Note that SHIFT-Z on the keyboard will take you to the Z's.", "prevletter"),

    ('Verticalshiftup', 'VerticalShiftUp', '', 'verticalshiftup'),
    ('Verticalshiftdown', 'VerticalShiftDown', '', 'verticalshiftdown'),
    ('Playpause', 'PlayPause', '', 'playpause'),
    ('Reloadkeymaps', 'ReloadKeymaps', '', 'reloadkeymaps'),
    ('Guiprofile', 'GuiProfile', '', 'guiprofile'),
    ('Red', 'Red', '', 'red'),
    ('Green', 'Green', '', 'green'),
    ('Yellow', 'Yellow', '', 'yellow'),
    ('Blue', 'Blue', '', 'blue'),

    ('Subtitleshiftup', 'Subtitleshiftup', '', 'subtitleshiftup'),
    ('Subtitleshiftdown', 'Subtitleshiftdown', '', 'subtitleshiftdown'),
    ('Subtitlealign', 'Subtitlealign', '', 'subtitlealign'),
    ('Help', 'Help', 'This help message', 'Help'),
    ('Minimize', 'Minimize', 'Minimize XBMC', 'Minimize'),
    ('Mastermode', 'Mastermode', 'Control master mode', 'Mastermode'),
    ('TakeScreenshot', 'TakeScreenshot', 'Takes a Screenshot', 'TakeScreenshot'),
    ('ReloadSkin', 'ReloadSkin', "Reload XBMC's skin", 'ReloadSkin'),
    ('UnloadSkin', 'UnloadSkin', "Unload XBMC's skin", 'UnloadSkin'),
    ('RefreshRSS', 'RefreshRSS', 'Reload RSS feeds from RSSFeeds.xml', 'RefreshRSS'),
    ('Playlist.Clear', 'Playlist.Clear', 'Clear the current playlist', 'Playlist.Clear'),
    ('RipCD', 'RipCD', 'Rip the currently inserted audio CD', 'RipCD'),
    ('Skin.ResetSettings', 'Skin.ResetSettings', 'Resets all skin settings', 'Skin.ResetSettings'),
    ('System.LogOff', 'System.LogOff', 'Log off current user', 'System.LogOff'),
    ('Container.Refresh', 'Container.Refresh', 'Refresh current listing', 'Container.Refresh'),
    ('Container.Update', 'Container.Update', 'Update current listing. Send Container.Update(path,replace) to reset the path history', 'Container.Update'),
    ('Container.NextViewMode', 'Container.NextViewMode', 'Move to the next view type (and refresh the listing)', 'Container.NextViewMode'),
    ('Container.PreviousViewMode', 'Container.PreviousViewMode', 'Move to the previous view type (and refresh the listing)', 'Container.PreviousViewMode'),
    ('Container.NextSortMethod', 'Container.NextSortMethod', 'Change to the next sort method', 'Container.NextSortMethod'),
    ('Container.PreviousSortMethod', 'Container.PreviousSortMethod', 'Change to the previous sort method', 'Container.PreviousSortMethod'),
    ('Container.SortDirection', 'Container.SortDirection', 'Toggle the sort direction', 'Container.SortDirection'),
    ('UpdateAddonRepos', 'UpdateAddonRepos', 'Check add-on repositories for updates', 'UpdateAddonRepos'),
    ('UpdateLocalAddons', 'UpdateLocalAddons', 'Check for local add-on changes', 'UpdateLocalAddons'),
    ('ToggleDPMS', 'ToggleDPMS', 'Toggle DPMS mode manually', 'ToggleDPMS'),
    ('Weather.Refresh', 'Weather.Refresh', 'Force weather data refresh', 'Weather.Refresh'),
    ('Weather.LocationNext', 'Weather.LocationNext', 'Switch to next weather location', 'Weather.LocationNext'),
    ('Weather.LocationPrevious', 'Weather.LocationPrevious', 'Switch to previous weather location', 'Weather.LocationPrevious'),
    ('LIRC.Stop', 'LIRC.Stop', 'Removes XBMC as LIRC client', 'LIRC.Stop'),
    ('LIRC.Start', 'LIRC.Start', 'Adds XBMC as LIRC client', 'LIRC.Start'),
    ('LCD.Suspend', 'LCD.Suspend', 'Suspends LCDproc', 'LCD.Suspend'),
    ('LCD.Resume', 'LCD.Resume', 'Resumes LCDproc', 'LCD.Resume'),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://wiki.xbmc.org/?title=Keymap.xml#Remote_Section

REMOTE_BUTTONS = (
(eg.ActionGroup, "Remote", "Remote", None, (
    ("RemoteLeft", "Left", "", "left"),
    ("RemoteRight", "Right", "", "right"),
    ("RemoteUp", "Up", "", "up"),
    ("RemoteDown", "Down", "", "down"),
    ("RemoteSelect", "Select", "", "select"),
    ("RemoteBack", "Back", "", "back"),
    ("RemoteMenu", "Menu", "", "menu"),
    ("RemoteInfo", "Info", "", "info"),
    ("RemoteDisplay", "Display", "", "display"),
    ("RemoteTitle", "Title", "", "title"),
    ("RemotePlay", "Play", "", "play"),
    ("RemotePause", "Pause", "", "pause"),
    ("RemoteReverse", "Reverse", "", "reverse"),
    ("RemoteForward", "Forward", "", "forward"),
    ("RemoteSkipPlus", "Skip +", "", "skipplus"),
    ("RemoteSkipMinus", "Skip -", "", "skipminus"),
    ("RemoteStop", "Stop", "", "stop"),
    ("Remote0", "0", "", "zero"),
    ("Remote1", "1", "", "one"),
    ("Remote2", "2", "", "two"),
    ("Remote3", "3", "", "three"),
    ("Remote4", "4", "", "four"),
    ("Remote5", "5", "", "five"),
    ("Remote6", "6", "", "six"),
    ("Remote7", "7", "", "seven"),
    ("Remote8", "8", "", "eight"),
    ("Remote9", "9", "", "nine"),
    ("RemotePower", "Power", "", "power"),
    ("RemoteMyTV", "My TV", "", "mytv"),
    ("RemoteMyMusic", "My Music", "", "mymusic"),
    ("RemoteMyPictures", "My Pictures", "", "mypictures"),
    ("RemoteMyVideo", "My Video", "", "myvideo"),
    ("RemoteRecord", "Record", "", "record"),
    ("RemoteStart", "Start", "", "start"),
    ("RemoteVolPlus", "Vol +", "", "volumeplus"),
    ("RemoteVolMinus", "Vol -", "", "volumeminus"),
    ("Remotechannelplus", "CH +", "", "channelplus"),
    ("Remotechannelminus", "CH -", "", "channelminus"),
    ("Remotepageplus", "PG +", "", "pageplus"),
    ("Remotepageminus", "PG -", "", "pageminus"),
    ("RemoteMute", "Mute", "", "mute"),
    ("RemoteRecordedTV", "Recorded TV", "", "recordedtv"),
    ("RemoteLiveTV", "Live TV", "", "livetv"),
    ("RemoteStar", "*", "", "star"),
    ("Remote#", "#", "", "hash"),
    ("RemoteClear", "Clear", "", "clear"),
    ("Remoteguide", "Guide", "", "guide"),
    ("Remoteenter", "Enter", "", "enter"),
    ("Remotexbox", "Xbox", "", "xbox"),
    ("Remoteteletext", "Teletext", "", "teletext"),
    ("Remotered", "Red", "", "red"),
    ("Remotegreen", "Green", "", "green"),
    ("Remoteyellow", "Yellow", "", "yellow"),
    ("Remoteblue", "Blue", "", "blue"),
    ("Remotesubtitle", "Subtitle", "", "subtitle"),
    ("Remotelanguage", "Language", "", "language"),
)),
)
# Remote buttons handled by XBMC.  For a list of all buttons see: http://wiki.xbmc.org/?title=Keymap.xml#Gamepad_Section

GAMEPAD_BUTTONS = (
(eg.ActionGroup, "Gamepad", "Gamepad", None, (
    ("GamepadA", "A", "", "a"),
    ("GamepadB", "B", "", "b"),
    ("GamepadX", "X", "", "x"),
    ("GamepadY", "Y", "", "y"),
    ("GamepadWhite", "White", "", "white"),
    ("GamepadBlack", "Black", "", "black"),
    ("GamepadStart", "Start", "", "start"),
    ("GamepadBack", "Back", "", "back"),
    ("GamepadLeftThumbButton", "LeftThumbButton", "", "leftthumbbutton"),
    ("GamepadRightThumbButton", "RightThumbButton", "", "rightthumbbutton"),
    ("GamepadLeftThumbStick", "LeftThumbStick", "", "leftthumbstick"),
    ("GamepadLeftThumbStickUp", "LeftThumbStickUp", "", "leftthumbstickup"),
    ("GamepadLeftThumbStickDown", "LeftThumbStickDown", "", "leftthumbstickdown"),
    ("GamepadLeftThumbStickLeft", "LeftThumbStickLeft", "", "leftthumbstickleft"),
    ("GamepadLeftThumbStickRight", "LeftThumbStickRight", "", "leftthumbstickright"),
    ("GamepadRightThumbStick", "RightThumbStick", "", "rightthumbstick"),
    ("GamepadRightThumbStickUp", "RightThumbStickUp", "", "rightthumbstickup"),
    ("GamepadRightThumbStickDown", "RightThumbStickDown", "", "rightthumbstickdown"),
    ("GamepadRightThumbStickLeft", "RightThumbStickLeft", "", "rightthumbstickleft"),
    ("GamepadRightThumbStickRight", "RightThumbStickRight", "", "rightthumbstickright"),
    ("GamepadLeftTrigger", "LeftTrigger", "", "lefttrigger"),
    ("GamepadRightTrigger", "RightTrigger", "", "righttrigger"),
    ("GamepadLeftAnalogTrigger", "LeftAnalogTrigger", "", "leftanalogtrigger"),
    ("GamepadRightAnalogTrigger", "RightAnalogTrigger", "", "rightanalogtrigger"),
    ("GamepadDpadLeft", "DpadLeft", "", "dpadleft"),
    ("GamepadDpadRight", "DpadRight", "", "dpadright"),
    ("GamepadDpadUp", "DpadUp", "", "dpadup"),
    ("GamepadDpadDown", "DpadDown", "", "dpaddown"),
)),
)

# Keyboard keys handled by XBMC.  For a list of all keys see: http://wiki.xbmc.org/index.php?title=List_of_XBMC_keynames

KEYBOARD_KEYS = (
(eg.ActionGroup, "Keyboard", "Keyboard", None, (
    ("KeyboardBackspace", "Backspace", "", "backspace"),
    ("KeyboardEnter", "Enter", "", "enter"),
    ("KeyboardTab", "Tab", "", "tab"),
)),
)

# Support functions
def ParseString2(text, filterFunc=None):
	start = 0
	chunks = []
	last = len(text) - 1
	while 1:
		pos = text.find('{{', start)
		if pos < 0:
			break
		if pos == last:
			break
		chunks.append(text[start:pos])
		start = pos + 2
		end = text.find('}}', start)
		if end == -1:
			raise SyntaxError("unmatched bracket")
		word = text[start:end]
		res = None
		if filterFunc:
			res = filterFunc(word)
		if res is None:
			res = eval(word, {}, eg.globals.__dict__)
		chunks.append(unicode(res))
		start = end + 2
	chunks.append(text[start:])
	return "".join(chunks)


class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_action(self.value, ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC
"""
CONFIGURABLE_ACTIONS = (
(eg.ActionGroup, "General", "General", None, (
    ("UpdateLibrary", "UpdateLibrary", "UpdateLibrary", "UpdateLibrary(Video)"),
)),
)
"""
class UpdateLibrary(eg.ActionBase):
    def __call__(self, libraryType="Video", updatePath=""):
        try:
            self.plugin.xbmc.send_action("UpdateLibrary("+libraryType+","+updatePath+")", ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

    def Configure(self, libraryType="Video", updatePath="" ):
        panel = eg.ConfigPanel()
        textControl1 = wx.TextCtrl(panel, -1, libraryType)
        textControl2 = wx.TextCtrl(panel, -1, updatePath)
        panel.sizer.Add(textControl1, 1, wx.EXPAND)
        panel.sizer.Add(textControl2, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl1.GetValue())
            panel.SetResult(textControl2.GetValue())

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

class KeyboardPrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("KB"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class XBMC_HTTP_API:

	def __init__(self):
		self.ip = "127.0.0.1"
		self.port = "80"
		return

	def connect(self, ip=None, port=None):
		if ip: self.ip = ip
		if port: self.port = port
		print 'HTTP API connected'

	def send(self, method, params = ""):
		try:
			responce = urllib.urlopen('http://'+self.ip+':'+self.port+'/xbmcCmds/xbmcHttp?command='+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')').readlines()
		except IOError:
#			print 'HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')'
			eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')')
		else:
			if (''.join(responce).find('<html>') != -1):
				responce2 = {}
				for lines in responce:
					if (lines.find('<html>') != -1): lines = lines[lines.find('<html>')+6:]
					if (lines.find('</html>') != -1): lines = lines[:lines.find('</html>')]
					if (lines.find('<li>') != -1):
						if (lines.find('OK') != -1):
							responce2 = 'OK'
						elif (lines.find('ERROR') != -1):
							responce2 = lines[4:].rstrip('\n').split(':', 1)
						elif (lines.find(':') != -1):
							lines = lines[4:].rstrip('\n').split(':', 1)
							responce2[lines[0]] = lines[1]
						else:
							responce2 = lines[4:].rstrip('\n')
					else:
						if (lines.rstrip('\n') != ''):
							responce2 = lines.rstrip('\n')
				return responce2

	def close(self):
		print 'HTTP API connection closed'

class XBMC_JSON_RPC:

	def __init__(self):
		self.jsoninit = {'jsonrpc':'2.0', 'id':1}
		self.ip = "127.0.0.1"
		self.port = "80"
		return

	def connect(self, ip=None, port=None):
		if ip: self.ip = ip
		if port: self.port = port
		print 'JSON-RPC connected'

	def send(self, method, params = None):
		self.jsoninit['method'] = method
		if params:
			self.jsoninit['params'] = params
		else:
			if self.jsoninit.has_key('params'):
				del self.jsoninit['params']
		try:
			responce = urllib.urlopen('http://'+self.ip+':'+self.port+'/jsonrpc', json.dumps(self.jsoninit)).read()
		except IOError:
#			print 'JSON-RPC connection error:'+' http://'+self.ip+':'+self.port+'\n'+json.dumps(self.jsoninit)
			eg.PrintError('JSON-RPC connection error:'+' http://'+self.ip+':'+self.port+'\n'+json.dumps(self.jsoninit))
		else:
#			print responce
			return json.loads(responce)

	def close(self):
		print 'JSON-RPC connection closed'

class GetCurrentlyPlayingFilename(eg.ActionClass):
  description = "Get filename of currently playing file"

  def __call__(self):
		responce = self.plugin.JSON_RPC.send('Player.GetActivePlayers')
		if (responce != None):
			Method = None
			if (responce['result']['picture']): Method = 'Picture'
			elif (responce['result']['video']): Method = 'Video'
			elif (responce['result']['audio']): Method = 'Audio'
			if Method:
				print 'Method: ', Method
				if (Method != 'Picture'):
					responce = self.plugin.JSON_RPC.send(Method+'Playlist.GetItems')
#					print 'eg.result: ', responce['items'][responce['current']]['file']
					return responce['result']['items'][responce['result']['current']]['file']
				else:
					responce = self.plugin.HTTP_API.send('getcurrentlyplaying')
					if responce:
						if (responce['result']['Filename'] == ''):
							print 'No file playing'
						return responce['result']['Filename']
					else:
						raise self.Exceptions.ProgramNotRunning
			else:
				print 'No file playing'
		else:
			responce = self.plugin.HTTP_API.send('getcurrentlyplaying')
			if responce:
				if (responce['Filename'] == ''):
					print 'No file playing'
				return responce['Filename']
			else:
				raise self.Exceptions.ProgramNotRunning

class SendNotification(eg.ActionClass):
	description = "Send a notification to the connected XBMC"

	def __call__(self, title, message):
		try:
			self.plugin.xbmc.send_notification(str(eg.ParseString(title)), str(eg.ParseString(message)))
		except UnicodeEncodeError:
#			print "Error: ascii charecters only."
			eg.PrintError("Error: ascii charecters only.")
		except:
			raise self.Exceptions.ProgramNotRunning
	def Configure(self, title='Hello', message='world'):
		panel = eg.ConfigPanel()
		Title = wx.TextCtrl(panel, -1, value=title)
		Message = wx.TextCtrl(panel, -1, value=message)
		panel.sizer.Add(wx.StaticText(panel, -1, "Title"))
		panel.sizer.Add(Title)
		panel.sizer.Add(wx.StaticText(panel, -1, "Message"))
		panel.sizer.Add(Message)
		while panel.Affirmed():
			panel.SetResult(Title.GetValue(), Message.GetValue())

class HTTPAPI(eg.ActionClass):
	description = "Run any <a href='http://wiki.xbmc.org/index.php?title=Web_Server_HTTP_API'>XBMC HTTP API</a> command."

	def __call__(self, command, param, category, log):
		if param:
			responce = self.plugin.HTTP_API.send(command, param)
		else:
			responce = self.plugin.HTTP_API.send(command)
		if responce != None:
#			print 'Result:\n', responce
			if log:
				import pprint
				print 'Result:'
				pprint.PrettyPrinter(indent=2).pprint(responce)
			return responce
		else:
			raise self.Exceptions.ProgramNotRunning

	def Configure(self, command="GetCurrentPlaylist", param="", category=0, log=True):
		class record:
			pass
		httpapi = record()
		httpapi.Headers = []
		httpapi.Commands = []
		OldCategory = category

		def OnUpdate(event):
			UpdateCommands()
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'rb') as f:
					import pickle
					httpapi.Headers, httpapi.Commands = pickle.load(f)
			except IOError:
#				print 'Failed to open: httpapi.dat'
				eg.PrintError('Failed to open: httpapi.dat')
			else:
				category = OldCategory
				HBoxControl.Clear()
				for i in httpapi.Headers:
					HBoxControl.Append(i)
				HBoxControl.SetValue(httpapi.Headers[category])
				UpdateCommandCtrl(HBoxControl.GetSelection())
		def OnCommandChange(event):
			if event.GetEventObject() == comboBoxControl:
				syntax.SetLabel(httpapi.Commands[HBoxControl.GetSelection()][1][event.GetSelection()])
				description.SetLabel(httpapi.Commands[HBoxControl.GetSelection()][2][event.GetSelection()])
				description.Wrap(480)
			else:
				UpdateCommandCtrl(event.GetSelection())
		def UpdateCommandCtrl(Selection):
			value = comboBoxControl.GetValue()
			comboBoxControl.Clear()
			for i in httpapi.Commands[Selection][0]:
				comboBoxControl.Append(i)
			comboBoxControl.SetValue(value)

		def GetText(nodes):
			Text = ''
			for node in nodes.childNodes:
				if node.nodeType == Node.TEXT_NODE: Text += node.data
				else: Text += GetText(node)
			return Text
		def UpdateCommands():
			httpapi.Headers = [];httpapi.Commands = []
			doc = xml.dom.minidom.parse(urllib.urlopen('http://wiki.xbmc.org/index.php?title=Web_Server_HTTP_API'))
			for h3 in doc.getElementsByTagName("h3")[10:-1]:
				for span in h3.getElementsByTagName("span"):
					httpapi.Headers.append(span.childNodes[0].data)
			Header = 0
			for node in doc.getElementsByTagName("table")[3:9]:
				for node2 in node.getElementsByTagName("tr")[1:]:
					httpapi.Commands.append([[],[],[]])
					node3 = node2.getElementsByTagName("td")[0]
					for node4 in node3.childNodes:
						if node4.nodeType == Node.TEXT_NODE:
							Text = node4.data.strip()
							httpapi.Commands[Header][1].append(Text)
							Pos = Text.find('(')
							if (Pos != -1):
								httpapi.Commands[Header][0].append(Text[:Pos])
							else:
								httpapi.Commands[Header][0].append(Text)
						else:
							print '<'+node4.tagName+'>'
					httpapi.Commands[Header][2].append(GetText(node2.getElementsByTagName("td")[1]).strip())
				Header += 1
#			import os
			if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
				os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))

			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'wb') as f:
				import pickle
				pickle.dump((httpapi.Headers, httpapi.Commands), f, 1)

		import os
		try:
			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'rb') as f:
				import pickle
				httpapi.Headers, httpapi.Commands = pickle.load(f)
		except IOError:
			category = 0
			httpapi.Headers = ['No categorys']
			httpapi.Commands = [[['No commands'],[''],['']]]
		panel = eg.ConfigPanel()
		HBoxControl = wx.ComboBox(panel, -1, value=httpapi.Headers[category], choices=httpapi.Headers, style=wx.CB_READONLY)
		comboBoxControl = wx.ComboBox(panel, -1, value=command, choices=httpapi.Commands[category][0])
		comboBoxControl.SetStringSelection(command)
		textControl1 = wx.TextCtrl(panel, -1, param, size=(500, -1))
		Category = wx.BoxSizer(wx.HORIZONTAL)
		Category.Add(wx.StaticText(panel, -1, "Category"))
		Category.Add(HBoxControl)
		Category.Add(wx.StaticText(panel, -1, "Command"))
		Category.Add(comboBoxControl)
		panel.sizer.Add(wx.StaticText(panel, -1, "Choose or type in a HTTP API command and add parameter(s)"))
		panel.sizer.Add(Category)
		panel.sizer.Add(textControl1)
		panel.sizer.Add(wx.StaticText(panel, -1, "Command syntax:"))
		if (comboBoxControl.GetSelection() != -1):
			syntax = wx.TextCtrl(panel, -1, httpapi.Commands[category][1][comboBoxControl.GetSelection()], (1, 70), size=(500,-1), style=wx.TE_READONLY)
		else:
			syntax = wx.TextCtrl(panel, -1, '', (1, 70), size=(500,-1), style=wx.TE_READONLY)
		panel.sizer.Add(syntax)
		panel.sizer.Add(wx.StaticBox(panel, -1, 'Command description:', size=(500, 150)))
		if (comboBoxControl.GetSelection() != -1):
			description = wx.StaticText(panel, -1, httpapi.Commands[category][2][comboBoxControl.GetSelection()], (5, 105), style=wx.ALIGN_LEFT)
		else:
			description = wx.StaticText(panel, -1, '', (5, 105), style=wx.ALIGN_LEFT)
		description.Wrap(480)
		CheckBox = wx.CheckBox(panel, -1, 'Show result in the log')
		CheckBox.SetValue(log)
		UpdateButton = wx.Button(panel, -1, 'Update')
		UpdateButton.Bind(wx.EVT_BUTTON, OnUpdate)
		Bottom = wx.BoxSizer(wx.HORIZONTAL)
		Bottom.Add(CheckBox)
		Bottom.Add(UpdateButton,0,wx.LEFT,280)
		panel.sizer.Add(Bottom)
		panel.Bind(wx.EVT_COMBOBOX, OnCommandChange)
		while panel.Affirmed():
			panel.SetResult(comboBoxControl.GetValue(), textControl1.GetValue(), HBoxControl.GetSelection(), CheckBox.GetValue())

class JSONRPC(eg.ActionClass):
	description = "Run any <a href='http://wiki.xbmc.org/index.php?title=JSON_RPC'>XBMC JSON-RPC</a> method"

	def __call__(self, method="JSONRPC.Introspect", param="", log=True):
		if param:
			responce = self.plugin.JSON_RPC.send(method, ast.literal_eval(ParseString2(param)))
		else:
			responce = self.plugin.JSON_RPC.send(method)
		if responce != None:
			if responce.has_key('result'):
				if log:
					print 'Result:\n', json.dumps(responce['result'], sort_keys=True, indent=2)
				return responce['result']
			elif responce.has_key('error'):
#				print 'Error:\n', json.dumps(responce['error'], sort_keys=True, indent=2)
				eg.PrintError('Error:\n', json.dumps(responce['error'], sort_keys=True, indent=2))
			else:
#				print 'Got bad JSON-RPC responce', responce
				eg.PrintError('Got bad JSON-RPC responce', responce)
		else:
			raise self.Exceptions.ProgramNotRunning

	def Configure(self, method="JSONRPC.Introspect", param="", log=True):
		import os
		import pickle
		class record:
			Namespaces = ['No namespaces']
			Methods = {'No namespaces':['No methods']}
			Descriptions = {'No namespaces':['']}
		jsonrpc = record()
		def OnUpdate(event):
			UpdateMethods()
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'rb') as f:
					jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = pickle.load(f)
			except IOError:
#				print 'Error opening: jsonrpc.dat'
				eg.PrintError('Error opening: jsonrpc.dat')
			else:
				HBoxControl.Clear()
				for i in jsonrpc.Namespaces:
					HBoxControl.Append(i)
				HBoxControl.SetValue(method[:method.find('.')])
				UpdateMethodCtrl(HBoxControl.GetSelection())

		def UpdateMethods():
			responce = self.plugin.JSON_RPC.send('JSONRPC.Version')
			if responce:
				jsonrpc.Namespaces = []
				jsonrpc.Methods = {}
				jsonrpc.Descriptions = {}
				if responce['result']['version'] > 2:
					responce = self.plugin.JSON_RPC.send('JSONRPC.Introspect', json.loads('{"filterbytransport": false}'))
					if responce != None:
						if responce.has_key('result'):
							for method in responce['result']['methods']:
								namespace = method[:method.find('.')]
								if namespace not in jsonrpc.Namespaces:
									jsonrpc.Namespaces.append(namespace)
									jsonrpc.Methods[namespace] = []
									jsonrpc.Descriptions[namespace] = []
								jsonrpc.Methods[namespace].append(method[method.find('.')+1:])
								if responce['result']['methods'][method].has_key('description'):
									jsonrpc.Descriptions[namespace].append(responce['result']['methods'][method]['description'])
								else:
									jsonrpc.Descriptions[namespace].append('')
							if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
								os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))
							with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'wb') as f:
								pickle.dump((jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions), f, 1)
							return False
						elif responce.has_key('error'):
#					print 'Error', responce['error']
							eg.PrintError('Error', responce['error'])
							return responce['error']
						else:
#					print 'Got bad JSON-RPC responce', responce
							eg.PrintError('Got bad JSON-RPC responce', responce)
							return False
					else:
						return False
				else:
					responce = self.plugin.JSON_RPC.send('JSONRPC.Introspect', json.loads('{"getdescriptions": true, "getpermissions": false}'))
					if responce != None:
						if responce.has_key('result'):
							for method in responce['result']['commands']:
								namespace = method['command'][:method['command'].find('.')]
								if namespace not in jsonrpc.Namespaces:
									jsonrpc.Namespaces.append(namespace)
									jsonrpc.Methods[namespace] = []
									jsonrpc.Descriptions[namespace] = []
								jsonrpc.Methods[namespace].append(method['command'][method['command'].find('.')+1:])
								jsonrpc.Descriptions[namespace].append(method['description'])
							if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
								os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))
							with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'wb') as f:
								pickle.dump((jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions), f, 1)
							return False
						elif responce.has_key('error'):
#					print 'Error', responce['error']
							eg.PrintError('Error', responce['error'])
							return responce['error']
						else:
#					print 'Got bad JSON-RPC responce', responce
							eg.PrintError('Got bad JSON-RPC responce', responce)
							return False
					else:
						return False

		def UpdateMethodCtrl(Selection):
			comboBoxControl.Clear()
			for i in jsonrpc.Methods[jsonrpc.Namespaces[Selection]]:
				comboBoxControl.Append(i)
			comboBoxControl.SetValue(method[method.find('.')+1:])
		def OnMethodChange(event):
			if event.GetEventObject() == comboBoxControl:
				description.SetLabel(jsonrpc.Descriptions[jsonrpc.Namespaces[HBoxControl.GetSelection()]][event.GetSelection()])
				description.Wrap(480)
			else:
				UpdateMethodCtrl(event.GetSelection())
#				comboBoxControl.Clear()
#				for i in jsonrpc.Methods[jsonrpc.Namespaces[event.GetSelection()]]:
#					comboBoxControl.Append(i)

		panel = eg.ConfigPanel()
		try:
			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'rb') as f:
				jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = pickle.load(f)
		except IOError:
#			print 'Error opening: jsonrpc.dat'
			eg.PrintError('Error opening: jsonrpc.dat')
		HBoxControl = wx.ComboBox(panel, -1, value=method[:method.find('.')], choices=jsonrpc.Namespaces, style=wx.CB_READONLY)
		comboBoxControl = wx.ComboBox(panel, -1, value=method[method.find('.')+1:], choices=jsonrpc.Methods[jsonrpc.Namespaces[HBoxControl.GetSelection()]] , style=wx.CB_READONLY)
		textControl2 = wx.TextCtrl(panel, -1, param, size=(500, -1))
		Category = wx.BoxSizer(wx.HORIZONTAL)
		Category.Add(wx.StaticText(panel, -1, "Namespace"))
		Category.Add(HBoxControl)
		Category.Add(wx.StaticText(panel, -1, "Method"))
		Category.Add(comboBoxControl)
		panel.sizer.Add(wx.StaticText(panel, -1, "Choose a JSON-RPC Method and add any parameter(s)"))
		panel.sizer.Add(Category)
		panel.sizer.Add(textControl2)
		panel.sizer.Add(wx.StaticBox(panel, -1, 'Method description:', size=(500, 150)))
		if (comboBoxControl.GetSelection() != -1):
			description = wx.StaticText(panel, -1, jsonrpc.Descriptions[jsonrpc.Namespaces[HBoxControl.GetSelection()]][comboBoxControl.GetSelection()], (5, 70), style=wx.ALIGN_LEFT)
		else:
			description = wx.StaticText(panel, -1, '', (5, 70), style=wx.ALIGN_LEFT)
		description.Wrap(480)
		Bottom = wx.BoxSizer(wx.HORIZONTAL)
		CheckBox = wx.CheckBox(panel, -1, 'Show result in the log')
		CheckBox.SetValue(log)
		Bottom.Add(CheckBox)
		UpdateButton = wx.Button(panel, -1, 'Update')
		UpdateButton.Bind(wx.EVT_BUTTON, OnUpdate)
		Bottom.Add(UpdateButton,0,wx.LEFT,280)
		panel.sizer.Add(Bottom)
		panel.Bind(wx.EVT_COMBOBOX, OnMethodChange)
		while panel.Affirmed():
			panel.SetResult(HBoxControl.GetValue()+'.'+comboBoxControl.GetValue(), textControl2.GetValue(), CheckBox.GetValue())

class JSONRPCEventsConnect(eg.ActionClass):
	description = "Connect to XBMC to recieve JSON-RPC events"

	def __call__(self):
		self.plugin.stopJSONRPCEvents.clear()
		try:
			if not self.plugin.JSONRPCEventsThread.isAlive():
				self.plugin.JSONRPCEventsThread = Thread(target=self.plugin.JSONRPCEvents, args=(self.plugin.stopJSONRPCEvents,))
				self.plugin.JSONRPCEventsThread.start()
			else:
				print "Already connecting."
		except AttributeError:
			self.plugin.JSONRPCEventsThread = Thread(target=self.plugin.JSONRPCEvents, args=(self.plugin.stopJSONRPCEvents,))
			self.plugin.JSONRPCEventsThread.start()

class JSONRPCEventsDisconnect(eg.ActionClass):
	description = "Stop reciving JSON-RPC events from XBMC"

	def __call__(self):
		self.plugin.stopJSONRPCEvents.set()

#class StopRepeating(eg.ActionClass):
#    name = "Stop Repeating"
#    description = "Stops a button repeating."

#    def __call__(self):
#        try:
#            self.plugin.xbmc.release_button()
#        except:
#            raise self.Exceptions.ProgramNotRunning


# And now we define the actual plugin:

class XBMC2(eg.PluginClass):
    def __init__(self):
#        self.ip = "127.0.0.1"
#        self.port = port
        ButtonsGroup = self.AddGroup("Buttons", "Button actions to send to XBMC")
        ButtonsGroup.AddActionsFromList(REMOTE_BUTTONS, ButtonPrototype)
        ButtonsGroup.AddActionsFromList(GAMEPAD_BUTTONS, GamepadPrototype)
        ButtonsGroup.AddActionsFromList(KEYBOARD_KEYS, KeyboardPrototype)
        ActionsGroup = self.AddGroup("Actions", "Actions to send to XBMC")
        ActionsGroup.AddActionsFromList(GENERAL_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(MEDIA_PLAYING_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(PLAYLIST_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(FULLSCREEN_VIDEO_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(SLIDESHOW_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(CALIBRATION_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(FILEMANAGER_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(ON_SCREEN_KEYBOARD_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(VISUALISATION_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(SHUTDOWN_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(UNCATEGORIZED_ACTIONS, ActionPrototype)
#        ConfigurableGroup = ActionsGroup.AddGroup("Configurable", "Actions that have configurable settings")
#        ConfigurableGroup.AddAction(UpdateLibrary)
        self.AddActionsFromList(WINDOWS, ActionPrototype)

        TestGroup = self.AddGroup("Experimental", "Experimental")
        TestGroup.AddAction(JSONRPC)
        TestGroup.AddAction(HTTPAPI)
        TestGroup.AddAction(GetCurrentlyPlayingFilename)
        TestGroup.AddAction(SendNotification)
        TestGroup.AddAction(JSONRPCEventsConnect)
        TestGroup.AddAction(JSONRPCEventsDisconnect)

#        self.AddAction(StopRepeating)
        self.xbmc = XBMCClient("EventGhost")
        self.JSON_RPC = XBMC_JSON_RPC()
        self.HTTP_API = XBMC_HTTP_API()

    def Configure(self, ip="127.0.0.1", port="80", eventsConfig={}):
#    def Configure(self, ip="127.0.0.1", IPs = ['127.0.0.1', '192.168.0.100']):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, ip)
        textControl2 = wx.TextCtrl(panel, -1, port)
        try:
					eventsConfig['JSONRPC']['Port']
					eventsConfig['JSONRPC']['Retrys']
					eventsConfig['JSONRPC']['RetryTime']
					eventsConfig['Broadcast']['Enable']
					eventsConfig['Broadcast']['Port']
					eventsConfig['Broadcast']['Workaround']
					eventsConfig['LogRawEvents']
        except:
					eventsConfig = {'JSONRPC':{'Port': 9090, 'Retrys': 5, 'RetryTime': 5}, 'Broadcast':{'Enable':False, 'Port': 8278, 'Workaround': False}, 'LogRawEvents': False}
					eg.PrintError("JSON-RPC event settings reset, please check.")

        JSONRPCNotificationPort = wx.TextCtrl(panel, -1, str(eventsConfig['JSONRPC']['Port']))
        JSONRPCNotificationRetrys = wx.TextCtrl(panel, -1, str(eventsConfig['JSONRPC']['Retrys']))
        JSONRPCNotificationRetryTime = wx.TextCtrl(panel, -1, str(eventsConfig['JSONRPC']['RetryTime']))
        BroadcastEnable = wx.CheckBox(panel, -1, 'Enable broadcast events.')
        BroadcastEnable.SetValue(eventsConfig['Broadcast']['Enable'])
        BroadcastPort = wx.TextCtrl(panel, -1, str(eventsConfig['Broadcast']['Port']))
        BroadcastWorkaround = wx.CheckBox(panel, -1, 'Broadcast event workaround.')
        BroadcastWorkaround.SetValue(eventsConfig['Broadcast']['Workaround'])
        LogRawEvents = wx.CheckBox(panel, -1, 'Log raw events from XBMC.')
        LogRawEvents.SetValue(eventsConfig['LogRawEvents'])
#        textControl = panel.ComboBox(
#            ip,
#            IPs,
#            style=wx.CB_DROPDOWN,
#            validator=eg.DigitOnlyValidator()
#        )
        panel.sizer.Add(wx.StaticText(panel, -1, "IP address of XBMC ( 127.0.0.1 is this computer )"))
#        panel.sizer.Add(textControl, 1, wx.EXPAND)
        panel.sizer.Add(textControl)
        panel.sizer.Add(textControl2)
        panel.sizer.Add(wx.StaticText(panel, -1, "JSON-RPC notification port"))
        panel.sizer.Add(JSONRPCNotificationPort)
        panel.sizer.Add(JSONRPCNotificationRetrys)
        panel.sizer.Add(JSONRPCNotificationRetryTime)
        panel.sizer.Add(BroadcastEnable)
        panel.sizer.Add(wx.StaticText(panel, -1, "Broadcast port"))
        panel.sizer.Add(BroadcastPort)
        panel.sizer.Add(BroadcastWorkaround)
        panel.sizer.Add(LogRawEvents)
        while panel.Affirmed():
					eventsConfig['JSONRPC']['Port'] = int(JSONRPCNotificationPort.GetValue())
					eventsConfig['JSONRPC']['Retrys'] = int(JSONRPCNotificationRetrys.GetValue())
					eventsConfig['JSONRPC']['RetryTime'] = int(JSONRPCNotificationRetryTime.GetValue())
					eventsConfig['Broadcast']['Enable'] = BroadcastEnable.GetValue()
					eventsConfig['Broadcast']['Port'] = int(BroadcastPort.GetValue())
					eventsConfig['Broadcast']['Workaround'] = BroadcastWorkaround.GetValue()
					eventsConfig['LogRawEvents'] = LogRawEvents.GetValue()
					panel.SetResult(textControl.GetValue(), textControl2.GetValue(), eventsConfig)

    def __start__(self, ip='127.0.0.1', port='80', eventsConfig={}):
        self.ip = ip
        self.port = port
        try:
					eventsConfig['JSONRPC']['Port']
					eventsConfig['JSONRPC']['Retrys']
					eventsConfig['JSONRPC']['RetryTime']
					eventsConfig['Broadcast']['Enable']
					eventsConfig['Broadcast']['Port']
					eventsConfig['Broadcast']['Workaround']
					eventsConfig['LogRawEvents']
        except:
					eventsConfig = {'JSONRPC':{'Port': 9090, 'Retrys': 5, 'RetryTime': 5}, 'Broadcast':{'Enable':False, 'Port': 8278, 'Workaround': False}, 'LogRawEvents': False}
					eg.PrintError("JSON-RPC event settings reset, please check.")
        self.eventsConfig = eventsConfig
        try:
            self.xbmc.connect(ip=ip)
#            self.xbmc.connect()
#            self.xbmc.connect(ip="192.168.0.100")
						#	self.stopThreadEvent = Event()
        except:
            raise self.Exceptions.ProgramNotRunning
        self.JSON_RPC.connect(ip=ip, port=port)
        self.HTTP_API.connect(ip=ip, port=port)
       	self.stopJSONRPCEvents = Event()
       	if self.eventsConfig['Broadcast']['Enable']:
					self.stopBroadcastEvents = Event()
					BroadcastEventsThread = Thread(target=self.BroadcastEvents, args=(self.stopBroadcastEvents,))
					BroadcastEventsThread.start()

    def __stop__(self):
        try:
            #self.stopJSONRPCEvents.set()
            if self.eventsConfig['Broadcast']['Enable']:
							self.stopBroadcastEvents.set()
            self.xbmc.close()
        except:
            pass

    def __close__(self):
        pass

#    def ThreadWorker(self, stopThreadEvent):
#        while not stopThreadEvent.isSet():
#            self.TriggerEvent("MyTimerEvent")
#            stopThreadEvent.wait(10.0)

    def JSONRPCEvents(self, stopJSONRPCEvents):
			retrys = self.eventsConfig['JSONRPC']['Retrys']
			retryTime = self.eventsConfig['JSONRPC']['RetryTime']

			try:
				retry = retrys
				while retry:
					print 'try # ' + str(retrys + 1 - retry)
					try:
						import socket
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((self.ip, self.eventsConfig['JSONRPC']['Port']))
					except socket.error:
						retry -= 1
						import time
						time.sleep(retryTime)
					else:
						break
				if not retry:
					eg.PrintError("Can't connect via JSON-RPC to XBMC")
					return
			except:
				import sys
				eg.PrintError('JSON-RPC connect error: ' + str(sys.exc_info()))
				return
			print 'Listening for XBMC JSON-RPC events'
			while not stopJSONRPCEvents.isSet():
				try:
					message = s.recv(4096)
					if not message:
						break
					message = json.loads(message)
					if self.eventsConfig['LogRawEvents']:
						print "Raw event: %s" % repr(message)
					event = message['method']
					payload = message['params']['data']
					if payload:
						event += '.' + payload['item']['type']
						del payload['item']['type']
						if not payload['item']:
							del payload['item']
				except socket.error:
					import sys
					eg.PrintError('JSON socket.error: ' + str(sys.exc_info()[1]))
					break
				except:
					import sys
					eg.PrintError('Error: JSON-RPC event ' + str(sys.exc_info()))
					break
				if not stopJSONRPCEvents.isSet():
					#self.TriggerEvent('JSONRPC.' + event, payload)
					self.TriggerEvent(event, payload)
			s.close()
			print 'Not listening for XBMC JSON-RPC events'

    def BroadcastEvents(self, stopBroadcastEvents):
			ActionList = {
# actions that we have defined...
'0':'ACTION_NONE',
'1':'ACTION_MOVE_LEFT',
'2':'ACTION_MOVE_RIGHT',
'3':'ACTION_MOVE_UP',
'4':'ACTION_MOVE_DOWN',
'5':'ACTION_PAGE_UP',
'6':'ACTION_PAGE_DOWN',
'7':'ACTION_SELECT_ITEM',
'8':'ACTION_HIGHLIGHT_ITEM',
'9':'ACTION_PARENT_DIR',
'10':'ACTION_PREVIOUS_MENU',
'11':'ACTION_SHOW_INFO',

'12':'ACTION_PAUSE',
'13':'ACTION_STOP',
'14':'ACTION_NEXT_ITEM',
'15':'ACTION_PREV_ITEM',
'16':'ACTION_FORWARD', # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*
'17':'ACTION_REWIND', # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*

'18':'ACTION_SHOW_GUI', # toggle between GUI and movie or GUI and visualisation.
'19':'ACTION_ASPECT_RATIO', # toggle quick-access zoom modes. Can b used in videoFullScreen.zml window id=2005
'20':'ACTION_STEP_FORWARD', # seek +1% in the movie. Can b used in videoFullScreen.xml window id=2005
'21':'ACTION_STEP_BACK', # seek -1% in the movie. Can b used in videoFullScreen.xml window id=2005
'22':'ACTION_BIG_STEP_FORWARD', # seek +10% in the movie. Can b used in videoFullScreen.xml window id=2005
'23':'ACTION_BIG_STEP_BACK', # seek -10% in the movie. Can b used in videoFullScreen.xml window id=2005
'24':'ACTION_SHOW_OSD', # show/hide OSD. Can b used in videoFullScreen.xml window id=2005
'25':'ACTION_SHOW_SUBTITLES', # turn subtitles on/off. Can b used in videoFullScreen.xml window id=2005
'26':'ACTION_NEXT_SUBTITLE', # switch to next subtitle of movie. Can b used in videoFullScreen.xml window id=2005
'27':'ACTION_SHOW_CODEC', # show information about file. Can b used in videoFullScreen.xml window id=2005 and in slideshow.xml window id=2007
'28':'ACTION_NEXT_PICTURE', # show next picture of slideshow. Can b used in slideshow.xml window id=2007
'29':'ACTION_PREV_PICTURE', # show previous picture of slideshow. Can b used in slideshow.xml window id=2007
'30':'ACTION_ZOOM_OUT', # zoom in picture during slideshow. Can b used in slideshow.xml window id=2007
'31':'ACTION_ZOOM_IN', # zoom out picture during slideshow. Can b used in slideshow.xml window id=2007
'32':'ACTION_TOGGLE_SOURCE_DEST', # used to toggle between source view and destination view. Can be used in myfiles.xml window id=3
'33':'ACTION_SHOW_PLAYLIST', # used to toggle between current view and playlist view. Can b used in all mymusic xml files
'34':'ACTION_QUEUE_ITEM', # used to queue a item to the playlist. Can b used in all mymusic xml files
'35':'ACTION_REMOVE_ITEM', # not used anymore
'36':'ACTION_SHOW_FULLSCREEN', # not used anymore
'37':'ACTION_ZOOM_LEVEL_NORMAL', # zoom 1x picture during slideshow. Can b used in slideshow.xml window id=2007
'38':'ACTION_ZOOM_LEVEL_1', # zoom 2x picture during slideshow. Can b used in slideshow.xml window id=2007
'39':'ACTION_ZOOM_LEVEL_2', # zoom 3x picture during slideshow. Can b used in slideshow.xml window id=2007
'40':'ACTION_ZOOM_LEVEL_3', # zoom 4x picture during slideshow. Can b used in slideshow.xml window id=2007
'41':'ACTION_ZOOM_LEVEL_4', # zoom 5x picture during slideshow. Can b used in slideshow.xml window id=2007
'42':'ACTION_ZOOM_LEVEL_5', # zoom 6x picture during slideshow. Can b used in slideshow.xml window id=2007
'43':'ACTION_ZOOM_LEVEL_6', # zoom 7x picture during slideshow. Can b used in slideshow.xml window id=2007
'44':'ACTION_ZOOM_LEVEL_7', # zoom 8x picture during slideshow. Can b used in slideshow.xml window id=2007
'45':'ACTION_ZOOM_LEVEL_8', # zoom 9x picture during slideshow. Can b used in slideshow.xml window id=2007
'46':'ACTION_ZOOM_LEVEL_9', # zoom 10x picture during slideshow. Can b used in slideshow.xml window id=2007

'47':'ACTION_CALIBRATE_SWAP_ARROWS', # select next arrow. Can b used in: settingsScreenCalibration.xml windowid=11
'48':'ACTION_CALIBRATE_RESET', # reset calibration to defaults. Can b used in: settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
'49':'ACTION_ANALOG_MOVE', # analog thumbstick move. Can b used in: slideshow.xml window id=2007/settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
'50':'ACTION_ROTATE_PICTURE', # rotate current picture during slideshow. Can b used in slideshow.xml window id=2007

'52':'ACTION_SUBTITLE_DELAY_MIN', # Decrease subtitle/movie Delay. Can b used in videoFullScreen.xml window id=2005
'53':'ACTION_SUBTITLE_DELAY_PLUS', # Increase subtitle/movie Delay. Can b used in videoFullScreen.xml window id=2005
'54':'ACTION_AUDIO_DELAY_MIN', # Increase avsync delay. Can b used in videoFullScreen.xml window id=2005
'55':'ACTION_AUDIO_DELAY_PLUS', # Decrease avsync delay. Can b used in videoFullScreen.xml window id=2005
'56':'ACTION_AUDIO_NEXT_LANGUAGE', # Select next language in movie. Can b used in videoFullScreen.xml window id=2005
'57':'ACTION_CHANGE_RESOLUTION', # switch 2 next resolution. Can b used during screen calibration settingsScreenCalibration.xml windowid=11

'58':'REMOTE_0', # remote keys 0-9. are used by multiple windows
'59':'REMOTE_1', # for example in videoFullScreen.xml window id=2005 you can
'60':'REMOTE_2', # enter time (mmss) to jump to particular point in the movie
'61':'REMOTE_3',
'62':'REMOTE_4', # with spincontrols you can enter 3digit number to quickly set
'63':'REMOTE_5', # spincontrol to desired value
'64':'REMOTE_6',
'65':'REMOTE_7',
'66':'REMOTE_8',
'67':'REMOTE_9',

'68':'ACTION_PLAY', # Unused at the moment
'69':'ACTION_OSD_SHOW_LEFT', # Move left in OSD. Can b used in videoFullScreen.xml window id=2005
'70':'ACTION_OSD_SHOW_RIGHT', # Move right in OSD. Can b used in videoFullScreen.xml window id=2005
'71':'ACTION_OSD_SHOW_UP', # Move up in OSD. Can b used in videoFullScreen.xml window id=2005
'72':'ACTION_OSD_SHOW_DOWN', # Move down in OSD. Can b used in videoFullScreen.xml window id=2005
'73':'ACTION_OSD_SHOW_SELECT', # toggle/select option in OSD. Can b used in videoFullScreen.xml window id=2005
'74':'ACTION_OSD_SHOW_VALUE_PLUS', # increase value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
'75':'ACTION_OSD_SHOW_VALUE_MIN', # decrease value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
'76':'ACTION_SMALL_STEP_BACK', # jumps a few seconds back during playback of movie. Can b used in videoFullScreen.xml window id=2005

'77':'ACTION_PLAYER_FORWARD', # FF in current file played. global action, can be used anywhere
'78':'ACTION_PLAYER_REWIND', # RW in current file played. global action, can be used anywhere
'79':'ACTION_PLAYER_PLAY', # Play current song. Unpauses song and sets playspeed to 1x. global action, can be used anywhere

'80':'ACTION_DELETE_ITEM', # delete current selected item. Can be used in myfiles.xml window id=3 and in myvideoTitle.xml window id=25
'81':'ACTION_COPY_ITEM', # copy current selected item. Can be used in myfiles.xml window id=3
'82':'ACTION_MOVE_ITEM', # move current selected item. Can be used in myfiles.xml window id=3
'83':'ACTION_SHOW_MPLAYER_OSD', # toggles mplayers OSD. Can be used in videofullscreen.xml window id=2005
'84':'ACTION_OSD_HIDESUBMENU', # removes an OSD sub menu. Can be used in videoOSD.xml window id=2901
'85':'ACTION_TAKE_SCREENSHOT', # take a screenshot
'87':'ACTION_RENAME_ITEM', # rename item

'88':'ACTION_VOLUME_UP',
'89':'ACTION_VOLUME_DOWN',
'91':'ACTION_MUTE',
'92':'ACTION_NAV_BACK',

'100':'ACTION_MOUSE_START',
'100':'ACTION_MOUSE_LEFT_CLICK',
'101':'ACTION_MOUSE_RIGHT_CLICK',
'102':'ACTION_MOUSE_MIDDLE_CLICK',
'103':'ACTION_MOUSE_DOUBLE_CLICK',
'104':'ACTION_MOUSE_WHEEL_UP',
'105':'ACTION_MOUSE_WHEEL_DOWN',
'106':'ACTION_MOUSE_DRAG',
'107':'ACTION_MOUSE_MOVE',
'109':'ACTION_MOUSE_END',

'110':'ACTION_BACKSPACE',
'111':'ACTION_SCROLL_UP',
'112':'ACTION_SCROLL_DOWN',
'113':'ACTION_ANALOG_FORWARD',
'114':'ACTION_ANALOG_REWIND',

'115':'ACTION_MOVE_ITEM_UP', # move item up in playlist
'116':'ACTION_MOVE_ITEM_DOWN', # move item down in playlist
'117':'ACTION_CONTEXT_MENU', # pops up the context menu


# stuff for virtual keyboard shortcuts
'118':'ACTION_SHIFT',
'119':'ACTION_SYMBOLS',
'120':'ACTION_CURSOR_LEFT',
'121':'ACTION_CURSOR_RIGHT',

'122':'ACTION_BUILT_IN_FUNCTION',

'123':'ACTION_SHOW_OSD_TIME', # displays current time, can be used in videoFullScreen.xml window id=2005
'124':'ACTION_ANALOG_SEEK_FORWARD', # seeks forward, and displays the seek bar.
'125':'ACTION_ANALOG_SEEK_BACK', # seeks backward, and displays the seek bar.

'126':'ACTION_VIS_PRESET_SHOW',
'127':'ACTION_VIS_PRESET_LIST',
'128':'ACTION_VIS_PRESET_NEXT',
'129':'ACTION_VIS_PRESET_PREV',
'130':'ACTION_VIS_PRESET_LOCK',
'131':'ACTION_VIS_PRESET_RANDOM',
'132':'ACTION_VIS_RATE_PRESET_PLUS',
'133':'ACTION_VIS_RATE_PRESET_MINUS',

'134':'ACTION_SHOW_VIDEOMENU',
'135':'ACTION_ENTER',

'136':'ACTION_INCREASE_RATING',
'137':'ACTION_DECREASE_RATING',

'138':'ACTION_NEXT_SCENE', # switch to next scene/cutpoint in movie
'139':'ACTION_PREV_SCENE', # switch to previous scene/cutpoint in movie

'140':'ACTION_NEXT_LETTER', # jump through a list or container by letter
'141':'ACTION_PREV_LETTER',

'142':'ACTION_JUMP_SMS2', # jump direct to a particular letter using SMS-style input
'143':'ACTION_JUMP_SMS3',
'144':'ACTION_JUMP_SMS4',
'145':'ACTION_JUMP_SMS5',
'146':'ACTION_JUMP_SMS6',
'147':'ACTION_JUMP_SMS7',
'148':'ACTION_JUMP_SMS8',
'149':'ACTION_JUMP_SMS9',

'150':'ACTION_FILTER_CLEAR',
'151':'ACTION_FILTER_SMS2',
'152':'ACTION_FILTER_SMS3',
'153':'ACTION_FILTER_SMS4',
'154':'ACTION_FILTER_SMS5',
'155':'ACTION_FILTER_SMS6',
'156':'ACTION_FILTER_SMS7',
'157':'ACTION_FILTER_SMS8',
'158':'ACTION_FILTER_SMS9',

'159':'ACTION_FIRST_PAGE',
'160':'ACTION_LAST_PAGE',

'161':'ACTION_AUDIO_DELAY',
'162':'ACTION_SUBTITLE_DELAY',

'180':'ACTION_PASTE',
'181':'ACTION_NEXT_CONTROL',
'182':'ACTION_PREV_CONTROL',
'183':'ACTION_CHANNEL_SWITCH',

'199':'ACTION_TOGGLE_FULLSCREEN', # switch 2 desktop resolution
'200':'ACTION_TOGGLE_WATCHED', # Toggle watched status (videos)
'201':'ACTION_SCAN_ITEM', # scan item
'202':'ACTION_TOGGLE_DIGITAL_ANALOG', # switch digital <-> analog
'203':'ACTION_RELOAD_KEYMAPS', # reloads CButtonTranslator's keymaps
'204':'ACTION_GUIPROFILE_BEGIN', # start the GUIControlProfiler running

'215':'ACTION_TELETEXT_RED', # Teletext Color buttons to control TopText
'216':'ACTION_TELETEXT_GREEN', # " " " " " "
'217':'ACTION_TELETEXT_YELLOW', # " " " " " "
'218':'ACTION_TELETEXT_BLUE', # " " " " " "

'219':'ACTION_INCREASE_PAR',
'220':'ACTION_DECREASE_PAR',

'221':'ACTION_GESTURE_NOTIFY',
'222':'ACTION_GESTURE_BEGIN',
'223':'ACTION_GESTURE_ZOOM', #sendaction with point and currentPinchScale (fingers together < 1.0 -> fingers apart > 1.0)
'224':'ACTION_GESTURE_ROTATE',
'225':'ACTION_GESTURE_PAN',
'226':'ACTION_GESTURE_END',
'227':'ACTION_VSHIFT_UP', # shift up video image in DVDPlayer
'228':'ACTION_VSHIFT_DOWN', # shift down video image in DVDPlayer

'229':'ACTION_PLAYER_PLAYPAUSE', # Play/pause. If playing it pauses, if paused it plays.

# The NOOP action can be specified to disable an input event. This is
# useful in user keyboard.xml etc to disable actions specified in the
# system mappings.
'999':'ACTION_NOOP',

'230':'ACTION_SUBTITLE_VSHIFT_UP', # shift up subtitles in DVDPlayer
'231':'ACTION_SUBTITLE_VSHIFT_DOWN', # shift down subtitles in DVDPlayer
'232':'ACTION_SUBTITLE_ALIGN', # toggle vertical alignment of subtitles

# Window ID defines to make the code a bit more readable
'9999':'WINDOW_INVALID',
'10000':'WINDOW_HOME',
'10001':'WINDOW_PROGRAMS',
'10002':'WINDOW_PICTURES',
'10003':'WINDOW_FILES',
'10004':'WINDOW_SETTINGS_MENU',
'10005':'WINDOW_MUSIC', # virtual window to return the music start window.
'10006':'WINDOW_VIDEOS',
'10007':'WINDOW_SYSTEM_INFORMATION',
'10008':'WINDOW_TEST_PATTERN',
'10011':'WINDOW_SCREEN_CALIBRATION',

'10012':'WINDOW_SETTINGS_MYPICTURES',
'10013':'WINDOW_SETTINGS_MYPROGRAMS',
'10014':'WINDOW_SETTINGS_MYWEATHER',
'10015':'WINDOW_SETTINGS_MYMUSIC',
'10016':'WINDOW_SETTINGS_SYSTEM',
'10017':'WINDOW_SETTINGS_MYVIDEOS',
'10018':'WINDOW_SETTINGS_NETWORK',
'10019':'WINDOW_SETTINGS_APPEARANCE',

'10020':'WINDOW_SCRIPTS', # virtual window for backward compatibility

'10024':'WINDOW_VIDEO_FILES',
'10025':'WINDOW_VIDEO_NAV',
'10028':'WINDOW_VIDEO_PLAYLIST',

'10029':'WINDOW_LOGIN_SCREEN',
'10034':'WINDOW_SETTINGS_PROFILES',

'10040':'WINDOW_ADDON_BROWSER',

'10099':'WINDOW_DIALOG_POINTER',
'10100':'WINDOW_DIALOG_YES_NO',
'10101':'WINDOW_DIALOG_PROGRESS',
'10103':'WINDOW_DIALOG_KEYBOARD',
'10104':'WINDOW_DIALOG_VOLUME_BAR',
'10105':'WINDOW_DIALOG_SUB_MENU',
'10106':'WINDOW_DIALOG_CONTEXT_MENU',
'10107':'WINDOW_DIALOG_KAI_TOAST',
'10109':'WINDOW_DIALOG_NUMERIC',
'10110':'WINDOW_DIALOG_GAMEPAD',
'10111':'WINDOW_DIALOG_BUTTON_MENU',
'10112':'WINDOW_DIALOG_MUSIC_SCAN',
'10113':'WINDOW_DIALOG_MUTE_BUG',
'10114':'WINDOW_DIALOG_PLAYER_CONTROLS',
'10115':'WINDOW_DIALOG_SEEK_BAR',
'10120':'WINDOW_DIALOG_MUSIC_OSD',
'10121':'WINDOW_DIALOG_VIS_SETTINGS',
'10122':'WINDOW_DIALOG_VIS_PRESET_LIST',
'10123':'WINDOW_DIALOG_VIDEO_OSD_SETTINGS',
'10124':'WINDOW_DIALOG_AUDIO_OSD_SETTINGS',
'10125':'WINDOW_DIALOG_VIDEO_BOOKMARKS',
'10126':'WINDOW_DIALOG_FILE_BROWSER',
'10128':'WINDOW_DIALOG_NETWORK_SETUP',
'10129':'WINDOW_DIALOG_MEDIA_SOURCE',
'10130':'WINDOW_DIALOG_PROFILE_SETTINGS',
'10131':'WINDOW_DIALOG_LOCK_SETTINGS',
'10132':'WINDOW_DIALOG_CONTENT_SETTINGS',
'10133':'WINDOW_DIALOG_VIDEO_SCAN',
'10134':'WINDOW_DIALOG_FAVOURITES',
'10135':'WINDOW_DIALOG_SONG_INFO',
'10136':'WINDOW_DIALOG_SMART_PLAYLIST_EDITOR',
'10137':'WINDOW_DIALOG_SMART_PLAYLIST_RULE',
'10138':'WINDOW_DIALOG_BUSY',
'10139':'WINDOW_DIALOG_PICTURE_INFO',
'10140':'WINDOW_DIALOG_ADDON_SETTINGS',
'10141':'WINDOW_DIALOG_ACCESS_POINTS',
'10142':'WINDOW_DIALOG_FULLSCREEN_INFO',
'10143':'WINDOW_DIALOG_KARAOKE_SONGSELECT',
'10144':'WINDOW_DIALOG_KARAOKE_SELECTOR',
'10145':'WINDOW_DIALOG_SLIDER',
'10146':'WINDOW_DIALOG_ADDON_INFO',
'10147':'WINDOW_DIALOG_TEXT_VIEWER',
'10148':'WINDOW_DIALOG_PLAY_EJECT',
'10149':'WINDOW_DIALOG_PERIPHERAL_MANAGER',
'10150':'WINDOW_DIALOG_PERIPHERAL_SETTINGS',

'10500':'WINDOW_MUSIC_PLAYLIST',
'10501':'WINDOW_MUSIC_FILES',
'10502':'WINDOW_MUSIC_NAV',
'10503':'WINDOW_MUSIC_PLAYLIST_EDITOR',

'10600':'WINDOW_DIALOG_OSD_TELETEXT',

#'11000':'WINDOW_VIRTUAL_KEYBOARD',
'12000':'WINDOW_DIALOG_SELECT',
'12001':'WINDOW_DIALOG_MUSIC_INFO',
'12002':'WINDOW_DIALOG_OK',
'12003':'WINDOW_DIALOG_VIDEO_INFO',
'12005':'WINDOW_FULLSCREEN_VIDEO',
'12006':'WINDOW_VISUALISATION',
'12007':'WINDOW_SLIDESHOW',
'12008':'WINDOW_DIALOG_FILESTACKING',
'12009':'WINDOW_KARAOKELYRICS',
'12600':'WINDOW_WEATHER',
'12900':'WINDOW_SCREENSAVER',
'12901':'WINDOW_DIALOG_VIDEO_OSD',

'12902':'WINDOW_VIDEO_MENU',
'12903':'WINDOW_DIALOG_MUSIC_OVERLAY',
'12904':'WINDOW_DIALOG_VIDEO_OVERLAY',
'12905':'WINDOW_VIDEO_TIME_SEEK', # virtual window for time seeking during fullscreen video

'12998':'WINDOW_START', # first window to load
'12999':'WINDOW_STARTUP_ANIM', # for startup animations

# WINDOW_ID's from 13000 to 13099 reserved for Python

'13000':'WINDOW_PYTHON_START',
'13099':'WINDOW_PYTHON_END',
}
			import socket
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			s.bind(('', self.eventsConfig['Broadcast']['Port']))
			print 'Listening for XBMC broadcast events'
			while not stopBroadcastEvents.isSet():
				s.settimeout(None)
				message = ''
				addr = ''
				try:
					message, addr = s.recvfrom(4096)
				except socket.error:
					import sys
					eg.PrintError('socket.error: ' + str(sys.exc_info()[1]))
					continue
				except:
					import sys
					eg.PrintError('Error: get1: ' + str(sys.exc_info()))
					continue
				if self.eventsConfig['LogRawEvents']:
					print "Raw event: %s %s" % (repr(message), repr(addr))
				if self.ip != addr[0]:
					if self.ip == '127.0.0.1':
						if not addr[0] in socket.gethostbyname_ex('')[2]: continue
					else:
						continue
				if self.eventsConfig['Broadcast']['Workaround']:
					s.settimeout(0)
					try:
						message2 = ''
						addr2 = ''
						if self.eventsConfig['LogRawEvents']:
							message2, addr2 = s.recvfrom(4096)
							print "Raw event2: %s %s" % (repr(message2), repr(addr2))
						else:
							s.recvfrom(4096)
					except:
						eg.PrintError('Error: get2')
					try:
						message2 = ''
						addr2 = ''
						if self.eventsConfig['LogRawEvents']:
							message2, addr2 = s.recvfrom(4096)
							print "Raw event3: %s %s" % (repr(message2), repr(addr2))
						else:
							s.recvfrom(4096)
					except:
						eg.PrintError('Error: get3')
				parts = re.sub('<[^<]+?>', '', message).split(';', 1)
				try:
					event, payload = parts[0].split(':', 1)
					if event != 'OnAction':
						event += '.' + payload.split(':', 1)[0]
					else:
						try:
							event += '.' + ActionList[payload.split(':', 1)[0]]
						except:
							event += '.' + payload.split(':', 1)[0]
					try:
						payload = unicode(payload.split(':', 1)[1], 'UTF8')
					except:
						payload = None
				except:
					event = parts[0].split(':', 1)[0]
					payload = None
				if not stopBroadcastEvents.isSet():
					self.TriggerEvent('Broadcast.' + event, payload)

			s.close()
			print 'Not listening for XBMC broadcast events'