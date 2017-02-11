# Copyright (c) 2009, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

eg.RegisterPlugin(
    name = "Spotify",
    author = "Walter Kraembring",
    version = "1.0.5",
    kind = "program",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org",
    description = (
        'Adds actions to control <a href="http://www.spotify.com/">Spotify</a>.'
    ),
)

##############################################################################
# Revision history:
#
# 2009-12-18  Tried to improve reliabilty when using SendKeys 
# 2009-12-14  Added new actions for extended control
#             - Go to playlists tree view
#             - Select next playlist
#             - Select previous playlist
#             - Show and start playing
#             Changed printout "Spotify Window was not found" to event instead
# 2009-12-09  Added new actions due to request
#             - Play
#             - Stop
#             - Minimize and stop playing
#             - Terminate Spotify
# 2009-09-09  Improved the error handling
# 2009-09-03  Introduced a thread to monitor Spotify status
# 2009-08-05  First version, thanks to Bjoerge Naess for pytify.py
##############################################################################

import win32gui, win32api, win32com.client
from eg.WinApi.Utils import BringHwndToFront, CloseHwnd
from pytify import Spotify
from threading import Event, Thread


 
class MySpotify(eg.PluginClass):

    class text:
        infoGroupName = "Information actions"
        infoGroupDescription = "Actions to query Spotify for information"
        infoSpotifyObject = "Spotify object created"
        infoPlugin = "Spotify plugin stopped" 
        infoStatus = "Spotify is not found running"
        infoNoWindow = "Spotify Window was not found"
        infoThread = "Spotify monitor thread has stopped"

    
    def __init__(self):
            self.bFound = False
            self.bSpotifyObjectCreated = False
            self.iDelay = 0.2
            self._hwnd = None
            self.spotify = None
            self.bTerminated = False
            self.bToggle = True
            
            self.AddAction(Play)
            self.AddAction(Stop)
            self.AddAction(PlayPause)
            self.AddAction(Mute)
            self.AddAction(VolumeDown)
            self.AddAction(VolumeUp)
            self.AddAction(PreviousTrack)
            self.AddAction(NextTrack)
            self.AddAction(MinimizeSpotify)
            self.AddAction(ShowSpotify)
            self.AddAction(TerminateSpotify)
            self.AddAction(GoToPlayList)
            self.AddAction(NextPlayList)
            self.AddAction(PreviousPlayList)
            
            group = self.AddGroup(
                self.text.infoGroupName, 
                self.text.infoGroupDescription
            )
            group.AddAction(GetCurrentTrack)
            group.AddAction(GetCurrentArtist)
            group.AddAction(GetStatus)


    def __start__(self):
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()


    def __stop__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        print self.text.infoPlugin

      
    def __close__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()


    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            stopThreadEvent.wait(self.iDelay)
            if self.bFound and not self.bSpotifyObjectCreated:
                self.createSpotifyObject()
            self.findSpotifyWindow()
        print self.text.infoThread


    def findSpotifyWindow(self):
        try:
            self._hwnd = win32gui.FindWindow("SpotifyMainWindow", None)
            self.bFound = True
        except:
       	    self.bFound = False

        if self.bFound:
           self.iDelay = 2.0
           self.bToggle = True
           #print "Spotify Window was found" #used when "debugging"
        else:
     	   self.iDelay = 10.0
     	   if self.bTerminated:
         	   self.iDelay = 2.0
     	   self.bSpotifyObjectCreated = False
     	   self.spotify = None
     	   if not self.bTerminated and self.bToggle:
               self.TriggerEvent(self.text.infoNoWindow)
               self.bToggle = False


    def createSpotifyObject(self):
        try:
            self.spotify = Spotify()
            self.bSpotifyObjectCreated = True
            print self.text.infoSpotifyObject
            self.bTerminated = False
        except:
            self.bFound = False
       	    self.iDelay = 10.0
            print self.text.infoStatus

            

class PlayPause(eg.ActionClass):
    name = "Play/Pause"
    description = "Toggles the pause button"

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            if self.plugin.spotify.isPlaying():
                # Play current track
                self.plugin.spotify.playpause()
                res = self.GetPlayingStatus()
                print res
                return
            else:
                # Pause current track
                self.plugin.spotify.playpause()
                res = self.GetPlayingStatus()
                print res
                return
        else:
            print self.plugin.text.infoStatus


    def GetPlayingStatus(self):
		if self.plugin.spotify.isPlaying():
			nowplaying = (
			    "Now playing " 
			    + self.plugin.spotify.getCurrentArtist() 
			    + " - " 
			    + self.plugin.spotify.getCurrentTrack()
			)
		else:
			nowplaying = "Not playing anything..."
		return "Spotify running! " + nowplaying



class Play(eg.ActionClass):
    name = "Play"
    description = "Starts playing"

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            if not self.plugin.spotify.isPlaying():
                self.plugin.spotify.playpause()
                res = self.GetPlayingStatus()
                print res
                return
        else:
            print self.plugin.text.infoStatus


    def GetPlayingStatus(self):
		if self.plugin.spotify.isPlaying():
			nowplaying = (
			    "Now playing " 
			    + self.plugin.spotify.getCurrentArtist() 
			    + " - " 
			    + self.plugin.spotify.getCurrentTrack()
			)
		else:
			nowplaying = "Not playing anything..."
		return "Spotify running! " + nowplaying



class Stop(eg.ActionClass):
    name = "Stop"
    description = "Stops playing"

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            if self.plugin.spotify.isPlaying():
                # Plays currently a track 
                self.plugin.spotify.stop()
                res = self.GetPlayingStatus()
                print res
                return
        else:
            print self.plugin.text.infoStatus


    def GetPlayingStatus(self):
		if self.plugin.spotify.isPlaying():
			nowplaying = (
			    "Now playing " 
			    + self.plugin.spotify.getCurrentArtist() 
			    + " - " 
			    + self.plugin.spotify.getCurrentTrack()
			)
		else:
			nowplaying = "Not playing anything..."
		return "Spotify running! " + nowplaying



class Mute(eg.ActionClass):
    name = "Mute"
    description = "Toggles the mute button."

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            self.plugin.spotify.mute()
            return
        else:
            print self.plugin.text.infoStatus



class VolumeDown(eg.ActionClass):
    name = "Volume Down"
    description = "Lowers the volume."

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            self.plugin.spotify.volumeDown()
            return
        else:
            print self.plugin.text.infoStatus



class VolumeUp(eg.ActionClass):
    name = "Volume Up"
    description = "Raises the volume."

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            self.plugin.spotify.volumeUp()
            return
        else:
            print self.plugin.text.infoStatus



class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Play the previous track."

    
    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            self.plugin.spotify.previous()
            return
        else:
            print self.plugin.text.infoStatus



class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Play the next track."


    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            self.plugin.spotify.next()
            return
        else:
            print self.plugin.text.infoStatus



class GetCurrentTrack(eg.ActionClass):
    name = "Get current Song Title"
    description = "Gets the Song Title currently beeing played."


    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            res = self.plugin.spotify.getCurrentTrack()
            print str(res)
            return res
        else:
            print self.plugin.text.infoStatus



class GetCurrentArtist(eg.ActionClass):
    name = "Get current Artist"
    description = "Gets the Artist currently beeing played."


    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
            res = self.plugin.spotify.getCurrentArtist()
            print str(res)
            return res
        else:
            print self.plugin.text.infoStatus



class GetStatus(eg.ActionClass):
    name = "Get current Status"
    description = "Gets the Status of Spotify."


    def __call__(self):
        if self.plugin.bSpotifyObjectCreated:
    		if self.plugin.spotify.isPlaying():
    			nowplaying = (
    			    "Now playing " 
    			    + self.plugin.spotify.getCurrentArtist() 
    			    + " - " 
    			    + self.plugin.spotify.getCurrentTrack()
    			)
    		else:
    			nowplaying = "Not playing anything..."
    		print "Spotify running! " + nowplaying
    		return "Spotify running! " + nowplaying
        else:
            print self.plugin.text.infoStatus
	
		
		
class MinimizeSpotify(eg.ActionClass):
    name = "Minimize and stop playing"
    description = "Stops playing and minimizes Spotify to the system tray"


    def __call__(self):
        try:
            BringHwndToFront(self.plugin._hwnd)
            self.plugin.spotify.stop()
            CloseHwnd(self.plugin._hwnd)
        except:
            raise self.Exceptions.ProgramNotRunning



class ShowSpotify(eg.ActionClass):
    name = "Show and start playing"
    description = "Brings Spotify up from tray and starts playing"


    def __call__(self):
        try:
            BringHwndToFront(self.plugin._hwnd)
            win32api.Sleep(100)
        except:
            raise self.Exceptions.ProgramNotRunning

        if self.plugin.bSpotifyObjectCreated:
            if not self.plugin.spotify.isPlaying():
                self.plugin.spotify.playpause()
                res = self.GetPlayingStatus()
                print res
                return
        else:
            print self.plugin.text.infoStatus


    def GetPlayingStatus(self):
		if self.plugin.spotify.isPlaying():
			nowplaying = (
			    "Now playing " 
			    + self.plugin.spotify.getCurrentArtist() 
			    + " - " 
			    + self.plugin.spotify.getCurrentTrack()
			)
		else:
			nowplaying = "Not playing anything..."
		return "Spotify running! " + nowplaying



class TerminateSpotify(eg.ActionClass):
    name = "Terminate Spotify"
    description = "Terminates Spotify"


    def __call__(self):
        sh = win32com.client.Dispatch("WScript.Shell")
        win32api.Sleep(100)
        if self.plugin.bSpotifyObjectCreated:
            hWnd = win32gui.FindWindow("SpotifyMainWindow", None)
            BringHwndToFront(hWnd)
            win32api.Sleep(200)
            sh.AppActivate("spotify")
            win32api.Sleep(100)
            sh.SendKeys("%")
            win32api.Sleep(10)
            sh.SendKeys("xxx")
            del hWnd
        self.plugin.bTerminated = True
        del sh
        return



class GoToPlayList(eg.ActionClass):
    name = "Go to playlists tree view and start playing the last one"
    description = "Go to Playlist tree view and start playing"


    def __call__(self):
        sh = win32com.client.Dispatch("WScript.Shell")
        win32api.Sleep(100)
        if self.plugin.bSpotifyObjectCreated:
            hWnd = win32gui.FindWindow("SpotifyMainWindow", None)
            BringHwndToFront(hWnd)
            win32api.Sleep(200)
            sh.AppActivate("spotify")
            win32api.Sleep(100)
            sh.SendKeys("{TAB}")
            win32api.Sleep(50)
            sh.SendKeys("{TAB}")
            win32api.Sleep(50)
            sh.SendKeys("{TAB}")
            win32api.Sleep(50)
            sh.SendKeys("{END}")
            win32api.Sleep(10)
            sh.SendKeys("~~~~")
            del hWnd
        del sh
        return



class NextPlayList(eg.ActionClass):
    name = "Select next playlist"
    description = "Selects next playlist"


    def __call__(self):
        sh = win32com.client.Dispatch("WScript.Shell")
        win32api.Sleep(100)
        if self.plugin.bSpotifyObjectCreated:
            hWnd = win32gui.FindWindow("SpotifyMainWindow", None)
            BringHwndToFront(hWnd)
            win32api.Sleep(200)
            sh.AppActivate("spotify")
            win32api.Sleep(100)
            sh.SendKeys("{DOWN}")
            win32api.Sleep(10)
            sh.SendKeys("~~~~")
            del hWnd
        del sh
        return



class PreviousPlayList(eg.ActionClass):
    name = "Select previous playlist"
    description = "Selects previous playlist"


    def __call__(self):
        sh = win32com.client.Dispatch("WScript.Shell")
        win32api.Sleep(100)
        if self.plugin.bSpotifyObjectCreated:
            hWnd = win32gui.FindWindow("SpotifyMainWindow", None)
            BringHwndToFront(hWnd)
            win32api.Sleep(200)
            sh.AppActivate("spotify")
            win32api.Sleep(100)
            sh.SendKeys("{UP}")
            win32api.Sleep(10)
            sh.SendKeys("~~~~")
            del hWnd
        del sh
        return

    