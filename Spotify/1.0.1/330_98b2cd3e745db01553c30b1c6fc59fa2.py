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
    version = "1.0.1",
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
# 2009-09-03  Introduced a thread to monitor Spotify status
# 2009-08-05  First version, thanks to Bjoerge Naess for pytify.py
##############################################################################

import win32gui
from pytify import Spotify
from threading import Event, Thread


 
class MySpotify(eg.PluginClass):
    class text:
        infoGroupName = "Information actions"
        infoGroupDescription = "Actions to query Spotify for information"
        infoPlugin = "Spotify plugin stopped" 
        infoStatus = "Spotify is not found running"
        infoThread = "Spotify monitor thread has stopped"

    bFound = False
    iDelay = 2.0
    _hwnd = None
    spotify = None

    
    def __init__(self):
            self.AddAction(PlayPause)
            self.AddAction(Mute)
            self.AddAction(VolumeDown)
            self.AddAction(VolumeUp)
            self.AddAction(PreviousTrack)
            self.AddAction(NextTrack)
            
            group = self.AddGroup(
                self.text.infoGroupName, 
                self.text.infoGroupDescription
            )
            group.AddAction(GetCurrentTrack)
            group.AddAction(GetCurrentArtist)


    def __start__(self):
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()
 

    def __stop__(self):
        self.stopThreadEvent.set()
        print self.text.infoPlugin

      
    def __close__(self):
        self.stopThreadEvent.set()


    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            stopThreadEvent.wait(self.iDelay)
            if self.bFound == False:
                self.createSpotifyObject()
            self.findSpotifyWindow()
        print self.text.infoThread


    def findSpotifyWindow(self):
        try:
            self._hwnd = win32gui.FindWindow("SpotifyMainWindow", None)
            self.bFound = True
        except:
       	    self.bFound = False
       	    self.iDelay = 10.0


    def createSpotifyObject(self):
        try:
            self.spotify = Spotify()
            self.bFound = True
       	    self.iDelay = 2.0
        except:
            self.bFound = False
       	    self.iDelay = 10.0
            print self.text.infoStatus
            


class PlayPause(eg.ActionClass):
    name = "Play/Pause"
    description = "Toggles the pause button"

    
    def __call__(self):
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


    def GetPlayingStatus(self):
		if self.plugin.spotify.isPlaying():
			nowplaying = "Now playing " + self.plugin.spotify.getCurrentArtist() + " - " + self.plugin.spotify.getCurrentTrack()
		else:
			nowplaying = "Not playing anything..."
		return "Spotify running! " + nowplaying



class Mute(eg.ActionClass):
    name = "Mute"
    description = "Toggles the mute button."

    
    def __call__(self):
        self.plugin.spotify.mute()
        return



class VolumeDown(eg.ActionClass):
    name = "Volume Down"
    description = "Lowers the volume."

    
    def __call__(self):
        self.plugin.spotify.volumeDown()
        return



class VolumeUp(eg.ActionClass):
    name = "Volume Up"
    description = "Raises the volume."

    
    def __call__(self):
        self.plugin.spotify.volumeUp()
        return



class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Play the previous track."

    
    def __call__(self):
        self.plugin.spotify.previous()
        return



class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Play the next track."


    def __call__(self):
        self.plugin.spotify.next()
        return



class GetCurrentTrack(eg.ActionClass):
    name = "Get current Song Title"
    description = "Gets the Song Title currently beeing played."


    def __call__(self):
        res = self.plugin.spotify.getCurrentTrack()
        print str(res)
        return res



class GetCurrentArtist(eg.ActionClass):
    name = "Get current Artist"
    description = "Gets the Artist currently beeing played."


    def __call__(self):
        res = self.plugin.spotify.getCurrentArtist()
        print str(res)
        return res

