version="0.7" 

# Plugins/JRMC/__init__.py
#Changelog
#  Version 0.3 - Added new support for several JRMC COM/Automation methods:
#           SetActiveZone
#           SetPlaylist
#           SyncZones
#  Version 0.4 - Modified WindowMatcher to work for (at least) version 12 and 13 of JRMC,
#                so there aren't two different versions.
#  Version 0.5 - Updated actions to match the HotKeys (plus Up/Down/etc)
#                from the J River wiki
#  Version 0.6 - Fixed a bug in my COM handling.  comInstance was not set to None unless
#                a command was sent when JRMC was not running.  However, if JRMC was stopped 
#                and restarted without any commands, the old (and invalid) comInstance would
#                be used, which would cause a silent exception.  Now the exception is caught,
#                the comInstance is reset, and the command is tried again.
#  Version 0.7 - Fixed a bug that could create 2nd worker thread and delay shutdown.  Changed 
#                queries (Zones and Playlists) so the COM interfaces are retrieved each time and
#                not stored.  Fixed the WindowMatcher function so it works when other zones are
#                enabled.  Changed VolumeUp/Down {Ctrl++} didn't work, {Ctrl+Add} does.

eg.RegisterPlugin(
    name = "J River Media Center",
    author = "Brett Stottlemyer",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control J River Media Center.'
    ),
    createMacrosOnAdd = False,
    icon = (
        "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"
    )
)

from win32gui import SendMessage, PostMessage
from win32com.client import GetActiveObject, WithEvents, Dispatch
from win32com.client.gencache import EnsureModule, EnsureDispatch
from functools import partial

FindJRMC = eg.WindowMatcher(None,u'Media Center{*}',u'MJFrame',None, None, 1, False, 0.0, 0)
#jrmc=EnsureModule('{03457D73-676C-4BB0-A275-D12D30ADB89A}', lcid=0, major=1, minor=0)
            
class JRMCConfigureThreadWorker(eg.ThreadWorker):
    comInstance = None
    
    def Setup(self):
        self.comInstance = EnsureDispatch("MediaJukebox Application")
        
    def Finish(self):
        if self.comInstance:
            del self.comInstance
            
    def GetZoneInfo(self):
        zonesInstance = self.comInstance.GetZones()
        nZones = zonesInstance.GetNumberZones();
        names = []
        for i in range(nZones):
            names.append(zonesInstance.GetZoneName(i))
        return nZones,names
        
    def GetPlaylistInfo(self):
        playlistsInstance = self.comInstance.GetPlaylists()
        nPlaylists = playlistsInstance.GetNumberPlaylists();
        names = []
        paths = []
        ids = []
        for i in range(nPlaylists):
            pl = playlistsInstance.GetPlaylist(i)
            paths.append(pl.Path)
            names.append(pl.Name)
            ids.append(pl.GetID())
            #print "ID =",pl.GetID(),"Name =",pl.Name,"Path =",pl.Path
        groups = []
        playlistsByGroup = {}
        playlistsByGroup["All"] = []
        for i in range(nPlaylists):
            if len(paths[i]) > 0:
                fullpath = paths[i] + "\\" + names[i]
            else:
                fullpath = names[i]
            if fullpath in paths:
                groups.append(fullpath)
                playlistsByGroup[fullpath] = []
        for i in range(nPlaylists):
            if len(paths[i]) > 0:
                fullpath = paths[i] + "\\" + names[i]
            else:
                fullpath = names[i]
            if fullpath not in paths:
                if len(paths[i]) > 0:
                    playlistsByGroup[paths[i]].append(names[i])
                playlistsByGroup["All"].append(names[i])
        return playlistsByGroup, names, ids

class wmAction(eg.ActionClass):    
    def __call__(self):
        hwnds = FindJRMC()
        if len(hwnds) != 0:
            PostMessage(hwnds[0], 793, 0, self.value)
            print self.value
        else:
            self.PrintError("J River Media Center is not running.")
            return

class hotKeys(eg.ActionClass):    
    def __call__(self):
        hwnds = FindJRMC()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, False)
        else:
            self.PrintError("J River Media Center is not running.")
            return
			            
class SetActiveZone(eg.ActionClass):
    def __call__(self, whichZone):
        if self.plugin.ComActive():
            try:
                self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SetActiveZone,whichZone-1))
            except:
                #This should mean that JRMC was active, then shutdown and restarted.  
                #The COM instance is from the old thread, so restart
                self.plugin.workerThread.Stop(1)
                self.plugin.workerThread = None
                if self.plugin.ComActive():
                    self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SetActiveZone,whichZone-1))

    def Configure(self, whichZone=1):
        panel = eg.ConfigPanel()
        configThread = JRMCConfigureThreadWorker()
        configThread.Start(10)
        nZones, names = configThread.CallWait(configThread.GetZoneInfo)
        configThread.Stop(1)
        labelCtrl = panel.StaticText("Select which zone to make active from the pulldown below:")
        labelCtrl.SetSize(labelCtrl.GetBestSize())
        panel.sizer.Add(labelCtrl, 0, wx.EXPAND)
        panel.sizer.Add((5, 5))
        zoneCtrl = panel.Choice(whichZone-1, names)
        panel.sizer.Add(zoneCtrl, 0, wx.EXPAND)
        zoneCtrl.SetFocus()
        while panel.Affirmed():
            panel.SetResult(zoneCtrl.GetValue()+1)
            
class SyncZones(eg.ActionClass):
    def __call__(self, srcZone, dstZone):
        if self.plugin.ComActive():
            try:
                self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SyncZones,srcZone-1,dstZone-1))
            except:
                #This should mean that JRMC was active, then shutdown and restarted.  
                #The COM instance is from the old thread, so restart
                self.plugin.workerThread.Stop(1)
                self.plugin.workerThread = None
                if self.plugin.ComActive():
                    self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SyncZones,srcZone-1,dstZone-1))
   
    def Configure(self, srcZone=1,dstZone=2):
        panel = eg.ConfigPanel()
        configThread = JRMCConfigureThreadWorker()
        configThread.Start(10)
        nZones, names = configThread.CallWait(configThread.GetZoneInfo)
        configThread.Stop(1)
        labelCtrl = panel.StaticText("Select source and destination zones from the pulldown menus:")
        labelCtrl.SetSize(labelCtrl.GetBestSize())
        panel.sizer.Add(labelCtrl, 0, wx.EXPAND)
        panel.sizer.Add((5, 5))
        srcZoneCtrl = panel.Choice(srcZone-1, names)
        panel.sizer.Add(srcZoneCtrl, 0, wx.EXPAND)
        dstZoneCtrl = panel.Choice(dstZone-1, names)
        panel.sizer.Add(dstZoneCtrl, 0, wx.EXPAND)
        srcZoneCtrl.SetFocus()
        while panel.Affirmed():
            panel.SetResult(srcZoneCtrl.GetValue()+1, dstZoneCtrl.GetValue()+1)

     
class SetPlaylist(eg.ActionBase):

    def __call__(self, myString):
        if self.plugin.ComActive():
            try:
                self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SetPlaylist,myString))
            except:
                #This should mean that JRMC was active, then shutdown and restarted.  
                #The COM instance is from the old thread, so restart
                self.plugin.workerThread.Stop(1)
                self.plugin.workerThread = None
                if self.plugin.ComActive():
                    self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.SetPlaylist,myString))

    def Configure(self, myString=""):

        configThread = JRMCConfigureThreadWorker()
        configThread.Start(10)
        groups, names, ids = configThread.CallWait(configThread.GetPlaylistInfo)
        try:
            myIndex = groups["All"].index(myString)
        except:
            myIndex = 0
        configThread.Stop(1)
        panel = eg.ConfigPanel()
        labelCtrl = panel.StaticText("Select a playlist from the pulldown:")
        panel.sizer.Add(labelCtrl,1,wx.EXPAND)
        playlistCtrl = panel.Choice(myIndex,groups["All"])
        panel.sizer.Add(playlistCtrl, 1, wx.EXPAND)
        playlistCtrl.SetFocus()
        while panel.Affirmed():
            ind = playlistCtrl.GetValue()
            plIndex = names.index(groups["All"][ind])
            name = names[plIndex]
            panel.SetResult(name)
            
class JRMCEvents():
    def OnFireMJEvent(self, string1, string2, string3):
        if string2 == "MCC: NOTIFY_TRACK_CHANGE":
            playlist = self.comInstance.GetCurPlaylist()
            pos = playlist.Position
            if pos < 0: #Playback stopped?
                self.plugin.TriggerEvent("TrackChanged")
                return
            file = playlist.GetFile(pos)
            Payload = {}
            Payload["name"] = file.Name
            Payload["artist"] = file.Artist
            Payload["album"] = file.Album
            Payload["zone"] = string3
            self.plugin.TriggerEvent("TrackChanged",Payload)
                                    
class JRMCThreadWorker(eg.ThreadWorker):
    comInstance = None
    plugin = None
    eventHandler = None
    
    def Setup(self, plugin, eventHandler):
        self.plugin = plugin
        self.eventHandler = eventHandler
        try:
            self.comInstance = GetActiveObject("MediaJukebox Application")
            WithEvents(self.comInstance,self.eventHandler)
            self.eventHandler.comInstance = self.comInstance
        except:
            pass
        
    def Finish(self):
        if self.comInstance:
            del self.comInstance
            
    def SetActiveZone(self, whichZone):
        zonesInstance = self.comInstance.GetZones()
        nZones = zonesInstance.GetNumberZones();
        if whichZone > nZones or whichZone < 0:
            eg.PrintError("Invalid zone requested", whichZone)
            return
        zonesInstance.SetActiveZone(whichZone);
        Payload = {}
        Payload["zone"] = zonesInstance.GetZoneName(whichZone)
        self.plugin.TriggerEvent("ZoneChanged",Payload)
        
    def SyncZones(self, srcZone, dstZone):
        zonesInstance = self.comInstance.GetZones()
        nZones = zonesInstance.GetNumberZones();
        if srcZone > nZones or srcZone < 0:
            eg.PrintError("Invalid zone requested", srcZone)
            return
        if dstZone > nZones or dstZone < 0:
            eg.PrintError("Invalid zone requested", dstZone)
            return
        zonesInstance.SynchronizeZones(srcZone,dstZone);
        Payload = {}
        Payload["source zone"] = zonesInstance.GetZoneName(srcZone)
        Payload["destination zone"] = zonesInstance.GetZoneName(dstZone)
        self.plugin.TriggerEvent("ZonesSynchronized",Payload)


    def SetPlaylist(self, plistName):
        playlistsInstance = self.comInstance.GetPlaylists()
        nPlaylists = playlistsInstance.GetNumberPlaylists();
        for i in range(nPlaylists):
            plist = playlistsInstance.GetPlaylist(i)
            if plistName == plist.Name:
                break
        else:
            plist = None
        #Don't want to pass in ID, rather find playlist by name to make config easier
        #plist = self.comInstance.GetPlaylistByID(plistID)
        if plist == None:
            eg.PrintError("Invalid playlist requested: ","Name =",plistName)
            return
        files = plist.GetFiles()
        n = files.GetNumberFiles()
        if n < 1:
            eg.PrintNotice("Requested Playlist has no songs.","Name =",plistName,"ID =",plistID)
            return
        current = self.comInstance.GetCurPlaylist()
        current.RemoveAllFiles()
        i = 0
        while i < n:
            file = files.GetFile(i)
            current.AddFile(file.Filename,i)
            #print "Adding",file.Filename,str(i)
            i = i + 1
        if (current.Shuffle):
            current.ReShuffleFiles()
        current.Position = 0
        playback = self.comInstance.GetPlayback().Play()
        
class JRMC(eg.PluginClass):
    workerThread = None
    def __init__(self):
        self.windowMatch = FindJRMC
        self.AddActionsFromList(ACTIONS)

    def StartThread(self):        
        class SubJRMCEvents(JRMCEvents):
            plugin = self
        self.workerThread = JRMCThreadWorker(self, SubJRMCEvents)
        try:
            self.workerThread.Start(20)
        except:
            raise self.Exception("Error starting JRMC worker thread")
    
    def ComActive(self):
        hwnds = FindJRMC()
        if len(hwnds) != 0:
            if not self.workerThread:
                self.StartThread()
            return True
        elif self.workerThread:
            self.workerThread.Stop(1)
            self.workerThread = None
        eg.PrintNotice("JRMC is not running")
        return False

    def __start__(self):
        if not self.ComActive():
            self.StartThread()        

    def __stop__(self):
        if self.workerThread:
            self.workerThread.Stop(1)
            self.workerThread = None
            
       
ACTIONS = (
  (hotKeys,"Play","Play","Play/Pause", u'{Ctrl+P}'),
  (hotKeys,"Pause","Pause","Play/Pause", u'{Ctrl+P}'),
  (hotKeys,"Stop","Stop","Stop", u'{Ctrl+S}'),
  (hotKeys,"Previous","Previous Track","Previous Track", u'{Ctrl+L}'),
  (hotKeys,"Next","Next Track","Next Track", u'{Ctrl+N}'),
  (hotKeys,"Up", "Up", "Up", u'{Up}'),
  (hotKeys,"Down", "Down", "Down", u'{Down}'),
  (hotKeys,"Left", "Left", "Left", u'{Left}'),
  (hotKeys,"Right", "Right", "Right", u'{Right}'),
  (hotKeys,"Select", "Select", "Select", u'{Enter}'),
  (hotKeys,"Mute","Mute","Mute", u'{Ctrl+M}'),
  (hotKeys,"VolumeUp","Volume Up","Volume Up", u'{Ctrl+Add}'),
  (hotKeys,"VolumeDown","Volume Down","Volume Down", u'{Ctrl+Subtract}'),
  (hotKeys,"PageUp", "Page Up", "Page Up", u'{PgUp}'),
  (hotKeys,"PageDown", "Page Down", "Page Down", u'{PgDown}'),
  (hotKeys,"Rewind","Rewind","Rewind", u'{Ctrl+Left}'),
  (hotKeys,"Forward","Fast-Forward","Fast-Forward", u'{Ctrl+Right}'),
  (hotKeys,"Reshuffle","Reshuffle All","Reshuffle All songs in Playing Now", u'{Ctrl+R}'),
  (hotKeys,"ShuffleRemaining","Reshuffle Remaining","Reshuffle remaining songs in Playing Now", u'{Ctrl+Shift+R}'),
  (SetPlaylist, "Set Playlist", "Set Playlist", "Set Playlist", None),
  (SetActiveZone, "Set Zone", "Set Zone", "Sets the active JRMC Zone", None),
  (SyncZones, "Sync Zones", "Sync Zones", "Synchronize music playing between multiple zones", None),
  (hotKeys,"SwitchZones","Switch zones","Switch between zones", u'{Ctrl+T}'),
  (hotKeys,"Rating0","Change rating to 0","Change rating of currently playing file to 0", u'{Shift+Ctrl+0}'),
  (hotKeys,"Rating1","Change rating to 1","Change rating of currently playing file to 1", u'{Shift+Ctrl+1}'),
  (hotKeys,"Rating2","Change rating to 2","Change rating of currently playing file to 2", u'{Shift+Ctrl+2}'),
  (hotKeys,"Rating3","Change rating to 3","Change rating of currently playing file to 3", u'{Shift+Ctrl+3}'),
  (hotKeys,"Rating4","Change rating to 4","Change rating of currently playing file to 4", u'{Shift+Ctrl+4}'),
  (hotKeys,"Rating5","Change rating to 5","Change rating of currently playing file to 5", u'{Shift+Ctrl+5}'),
  (hotKeys,"TogglePlayback","Toggle Playback Settings","Toggle between Main and Alternate Playback Settings", u'{Alt+1}'),
  (hotKeys,"MoveFocus","Move Keyboard Focus","Move Keyboard Focus", u'{Tab}'),
  (hotKeys,"ToggleViews","Toggle views","Toggle between all Full Screen, Theater and Standard views", u'{F11}'),
  (hotKeys,"StandardMode","Return to Standard Mode","Return to Standard Mode from Full Screen or Theater View", u'{Escape}'),
  (hotKeys,"StandardView","Standard View","Standard View", u'{Ctrl+1}'),
  (hotKeys,"MiniView","Mini View","Mini View", u'{Ctrl+2}'),
  (hotKeys,"WindowedView","Windowed View","Windowed View", u'{Ctrl+3}'),
  (hotKeys,"FullScreen","Full Screen View","Full Screen View", u'{Ctrl+4}'),
  (hotKeys,"TheaterView","Theater View","Theater View", u'{Ctrl+5}'),
  (hotKeys,"PlayingNow","Playing Now","Playing Now", u'{Alt+2}'),
  (hotKeys,"Playlists","Playlists","Playlists", u'{Alt+4}'),
  (hotKeys,"Exit","Exit","Exit JRMC", u'{Alt+F4}'),
  (eg.ActionGroup, 'Keyboard Commands', 'Probably not useful for IR Remotes', 'Probably not useful for IR Remotes',(
    (hotKeys,"Start","Start (in tree)","Start (in tree)", u'{Alt+1}'),
    (hotKeys,"LastOpenMedia","Last Open Media Mode in Tree","Last Open Media Mode in Tree", u'{Alt+3}'),
    (hotKeys,"DrivesDevices","Drives and Devices","Drives and Devices", u'{Alt+5}'),
    (hotKeys,"MyComputer","My Computer","My Computer", u'{Alt+6}'),
    (hotKeys,"TVTuner","TV Tuner","TV Tuner", u'{Alt+7}'),
    (hotKeys,"WebMedia","Web Media","Web Media", u'{Alt+8}'),
    (hotKeys,"Plugins","Plug-ins","Plug-ins", u'{Alt+9}'),
    (hotKeys,"Search","Find (Search)","Find (Search)", u'{Ctrl+F}'),
    (hotKeys,"Refresh","Refresh","Refresh", u'{F5}'),
    (hotKeys,"NavigateBackward","Navigate Backward","Navigate Backward", u'{Alt+Left}'),
    (hotKeys,"NavigateForward","Navigate Forward","Navigate Forward", u'{Alt+Right}'),
    (hotKeys,"ToggleStyle","Toggle List Style","Toggle List Style (focus must be in bottom list pane)", u'{Ctrl+U}'),
    (hotKeys,"AutomaticListStyle","Automatic List Style","Automatic List Style (focus must be in bottom list pane)", u'{Ctrl+Shift+U}'),
    (hotKeys,"DetailsListStyle","Details List Style","Details List Style (focus must be in bottom list pane)", u'{Ctrl+Shift+I}'),
    (hotKeys,"ViewThumbnails","View Thumbnails","View Thumbnails (focus must be in bottom list pane)", u'{Ctrl+Shift+O}'),
    (hotKeys,"ViewAlbumThumbnails","View Album Thumbnails","View Album Thumbnails (focus must be in bottom list pane)", u'{Ctrl+Shift+P}'),
    (hotKeys,"CollapseAll","Collapse All in Tree","Collapse All in Tree", u'{Ctrl+G}'),
    (hotKeys,"SelectAll","Select All","Select All", u'{Ctrl+A}'),
    (hotKeys,"TaggingMode","Tagging Mode","Tagging Mode", u'{F4}'),
    (hotKeys,"InvertSelectAll","Invert Select All","Invert Select All", u'{Ctrl+Shift+A}'),
    (hotKeys,"Copy","Copy","Copy", u'{Ctrl+C}'),
    (hotKeys,"Paste","Paste","Paste", u'{Ctrl+V}'),
    (hotKeys,"Delete","Delete","Delete", u'{Del}'),
    (hotKeys,"Delete files.","Delete files.","Delete files from the database and the currently selected playlist.", u'{Shift+Del}'),
    (hotKeys,"Rename","Rename","Rename", u'{F2}'),
    (hotKeys,"Redo","Redo","Redo", u'{Ctrl+Y}'),
    (hotKeys,"Undo","Undo","Undo", u'{Ctrl+Z}'),
    (hotKeys,"QuickSearch","Quick Search","Quick Search in a list", u'{Ctrl+Q}'),
    (hotKeys,"AddPlaylist","Add Playlist","Add Playlist", u'{F8}'),
    (hotKeys,"AddSmartlist","Add Smartlist","Add Smartlist", u'{F9}'),
    (hotKeys,"AddPlaylist Group","Add Playlist Group","Add Playlist Group", u'{F10}'),
    (hotKeys,"Properties","Properties","Properties", u'{Alt+Enter}'),
    (hotKeys,"ShowFileMenu","Show File Menu","Show File Menu", u'{Alt+F}'),
    (hotKeys,"ShowEditMenu","Show Edit Menu","Show Edit Menu", u'{Alt+E}'),
    (hotKeys,"ShowViewMenu","Show View Menu","Show View Menu", u'{Alt+V}'),
    (hotKeys,"ShowPlayerMenu","Show Player Menu","Show Player Menu", u'{Alt+P}'),
    (hotKeys,"ShowToolsMenu","Show Tools Menu","Show Tools Menu", u'{Alt+T}'),
    (hotKeys,"ShowHelpMenu","Show Help Menu","Show Help Menu", u'{Alt+H}'),
    (hotKeys,"Options","Options","Options", u'{Ctrl+O}'),
    (hotKeys,"TVTunerChannels","TV Tuner Channels","TV Tuner Channels", u'{F7}'),
    (hotKeys,"Help","Help","Help", u'{F1}'),
    (hotKeys,"CheckForUpdates","Check for Updates","Check for Updates", u'{Ctrl+J}'),
  )),
)       