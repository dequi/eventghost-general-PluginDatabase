version="0.0.1"
# Plugins/XMPlay/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
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
#
# Revision history:
# =================
# 0.0.1 by Pako 2010-10-05 17:56 GMT+1
#     - initial version

eg.RegisterPlugin(
    name = "XMPlay",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{E7DB64B9-6C0D-4F38-A4CA-9FE2868AEA49}",
    description = (
        'Adds actions to control the <a href="http://www.un4seen.com/">XMPlay</a> audio player. \n\n<p>'
    ),
    createMacrosOnAdd = True,    
#    url = "http://www.eventghost.org/forum/viewtopic.php?.....",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABQElEQVR4nGNgQAXRM88x"
        "4AWMDAwMySW9h3asuH3lNLKGpelGDAwMMkqaNm6hEBFuHv65PcWM+M1emm4ko6Spa+rA"
        "LyjKwMCwYkYTE0QpLpdEzzz35N51BgaGj+9fQ52UXNL77PEdBgYGKVkVBgYGOBvC2L5y"
        "Olyzqo7p7SunGTzDM////////3+IKISNLJhc0ouiBpmPqRPCRWYz/VB1lJJVYWSE+h7O"
        "QGN7RWQxMDB4hmcycdze/+zxHWSD0fwNEUH2DMLdcDZcHcS1cGWe4ZlMEKsZGRmlZFWS"
        "S3ohbIgbkkt64a5NLun1isiSklVhZGBgiMioO7JrNSS8ccUgHDBBKF1TB4iT8Ktemm4E"
        "1QCJeRklTUgSwqoUIsXCwMDAzcP/9ctHfkFRXVMHBliyQ0uFqjqmxjaeK2Y04bEfu38A"
        "SgS6R4+k12sAAAAASUVORK5CYII="
    ),
)

from os import path, remove
import _winreg
import win32ui
import dde
from subprocess import Popen
from win32gui import GetWindowText
from threading import Thread, Event
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

def HandleXMP():

    FindXMP = eg.WindowMatcher(
                u'xmplay.exe',
                None,
                u'XMPLAY-MAIN',
                None,
                None,
                None,
                True,
                0.0,
                0
            )
    hwnds = FindXMP()
    if len(hwnds) > 0:
        return hwnds[0]
    return None
#===============================================================================

class ObservationThread(Thread):

    def __init__(
        self,
        period,
        evtName,
    ):
        self.abort = False
        self.oldData = ""
        self.threadFlag = Event()

        self.period = period
        self.evtName = evtName
        Thread.__init__(self, name = self.evtName.encode('unicode_escape')+'_Thread')


    def run(self):
        while 1:
            hwnd = HandleXMP()
            if hwnd:
                data = GetWindowText(hwnd).decode(eg.systemEncoding)
                if data != self.oldData and data != "XMPlay":
                    self.oldData = data
                    eg.TriggerEvent(self.evtName, payload = data, prefix = "XMPlay")
            if self.abort:
                break
            self.threadFlag.wait(self.period)
            self.threadFlag.clear()


    def AbortObservation(self):
        self.abort = True
        self.threadFlag.set()
#===============================================================================

class Text:
    error1 = "Cannot connect to XMPlay"
    error2 = "XMPlay is not running !"
    label1 = "XMPlay installation folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    browseTitle = "Selected folder:"
    events = "Trigger events with suffix"
    label2 = "when changing tracks"
    intervalLabel = "Refresh period of titlebar reading:"
    suffix = "Track_Changed"
#===============================================================================

class XMPlay(eg.PluginBase):

    text=Text

    def __init__(self):
        self.observThread = None
        self.AddActionsFromList(ACTIONS)


    def __start__(self, path = None, suffix = "", period = 1.0):
        self.xmpPath = path
        self.xmpServer = dde.CreateServer()
        self.xmpConversation = None
        if suffix:
            self.observThread = ObservationThread(
                period,
                suffix,
            )
            self.observThread.start()


    def __stop__(self):
        if self.observThread:
            if self.observThread.isAlive():
                self.observThread.AbortObservation()
            del self.observThread
        self.observThread = None
        if self.xmpConversation:
            self.xmpServer.Shutdown()
            self.xmpConversation = None
        self.xmpServer = None


    def Configure(self, path = None, suffix = "", period = 1.0):
        self.xmpPath = path
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        xmpPathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        if self.xmpPath is None:
            self.xmpPath = self.XMPlayPath()
        xmpPathCtrl.startDirectory = self.xmpPath
        xmpPathCtrl.GetTextCtrl().SetEditable(False)
        xmpPathCtrl.GetTextCtrl().SetValue(self.xmpPath)
        evtCheckBox = wx.CheckBox(panel, -1, self.text.events)
        evtCheckBox.SetValue(suffix != "")
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        suffixCtrl = wx.TextCtrl(panel, -1, suffix, size = (100, -1))
        periodNumCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        intervalLbl = wx.StaticText(panel, -1, self.text.intervalLabel)
        val = suffix != ""
        suffixCtrl.Enable(val)
        intervalLbl.Enable(val)
        periodNumCtrl.Enable(val)
        suffixSizer = wx.BoxSizer(wx.HORIZONTAL)
        suffixSizer.Add(evtCheckBox, 0, wx.TOP, 2)
        suffixSizer.Add(suffixCtrl, 0, wx.LEFT|wx.RIGHT, 5)
        suffixSizer.Add(label2Text, 0, wx.TOP, 2)
        periodSizer = wx.BoxSizer(wx.HORIZONTAL)
        periodSizer.Add(intervalLbl, 0, wx.TOP, 2)
        periodSizer.Add(periodNumCtrl, 0, wx.LEFT, 5 )
        panelAdd = panel.sizer.Add
        panelAdd(label1Text, 0, wx.TOP, 15)
        panelAdd(xmpPathCtrl, 0, wx.TOP, 2)
        panelAdd(suffixSizer, 0, wx.TOP, 20)
        panelAdd(periodSizer, 0, wx.TOP, 20)

        def OnCheckBox(evt):
            val = evt.IsChecked()
            suffixCtrl.Enable(val)
            intervalLbl.Enable(val)
            periodNumCtrl.Enable(val)
            suffixCtrl.ChangeValue("" if not val else self.text.suffix)
            if evt:
                evt.Skip()
        evtCheckBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():
            panel.SetResult(
                xmpPathCtrl.GetValue(),
                suffixCtrl.GetValue(),
                periodNumCtrl.GetValue()
            )


    def XMPconversation(self):
        xmpc = None    
        try:
            self.xmpServer.Create("EGclient")
            xmpc = dde.CreateConversation(self.xmpServer)
            xmpc.ConnectTo("XMPlay","XMPlay")
            if not xmpc.Connected():
                self.xmpServer.Shutdown()
        except:
            pass
        return xmpc
            

    def Exec(self, key):
        if HandleXMP() is None:
            eg.PrintError(self.text.error2)
            return
        if not (self.xmpConversation and self.xmpConversation.Connected()):
            self.xmpConversation = self.XMPconversation()
            if self.xmpConversation is None:
                eg.PrintError(self.text.error1)
                return
        self.xmpConversation.Exec(key)


    def XMPlayPath(self):
        """
        Get the path of XMPlay's installation directory through querying 
        the Windows registry.
        """
        XMPlayPath = ""
        try:
            xmp = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER,
                "Software\\Classes\\XMPlay\\shell\\Open\\command"
            )
            try:
                XMPlayPath = path.split(_winreg.EnumValue(xmp, 0)[1])[0][1:]
            except:
                pass
            _winreg.CloseKey(xmp)
        except:
            pass
        return XMPlayPath
#===============================================================================

class Run(eg.ActionBase):

    def __call__(self):
        if HandleXMP() is None:
            xmp = '%s\\xmplay.exe' % self.plugin.xmpPath
            if path.isfile(xmp):
                Popen([xmp])
#===============================================================================

class Exec(eg.ActionBase):

    def __call__(self):
        self.plugin.Exec("key%i" % self.value)
#===============================================================================

class OpenFileFolder(eg.ActionBase):

    class text:
        label1 = "List of audio files, playlists and folders:"
        toolTipList = """If some row is marked (selected),
the new item(s) is (are) inserted in its position.
Otherwise a new entry is inserted at the end of the list.
Row can be selected with the left mouse button
and unselected with the right mouse button.
In addition to audio files, playlists and folders,
you can also insert Python expression such as {eg.result}.
Then you can use for example OSE plugin to play
the selected directory!"""
        elements = (
            '',
            'File(s) or playlist(s)',
            'Folder',
            'Python expression "{eg.result}"',
            'Python expression "{eg.event.payload}"',
            'Other Python expression'
        )
        clear = "Clear all"
        delete = "Delete item"
        wildcards = """
            XMPlay-able or playlists|*.ogg;*.mp3;*.mp2;*.mp1;*.wma;*.wav;*.aac;*.mp4;*.m4a;*.m4b;*.cda;*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx;*.pls;*.m3u;*.asx;*.wax|
            XMPlay-able|*.ogg;*.mp3;*.mp2;*.mp1;*.wma;*.wav;*.aac;*.mp4;*.m4a;*.m4b;*.cda;*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx|
            Playlists (pls/m3u/asx/wax)|*.pls;*.m3u;*.asx;*.wax|
            Modules (mo3/it/xm/s3m/mtm/mod/umx)|*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx|
            Ogg Vorbis (ogg)|*.ogg|
            MPEG (mp3/mp2/mp1)|*.mp3;*.mp2;*.mp1|
            WAVE (wav)|*.wav|
            Advanced Audio Coding (aac/mp4/m4a/m4b)|*.aac;*.mp4;*.m4a;*.m4b|
            CD audio (cda)|*.cda|
            Windows Media Audio (wma)|*.wma|
            All files (*.*)|*.*
        """
        radioboxtitle = "Action with selected files"
        modes = (
            "Replace current playlist",
            "Add to current playlist"
        )
        choiceLbl = "Choose item (file, playlist, folder ...) to insert"
        caption = "Please enter text"
        message = 'Python expression - for example {eg.event.suffix} :'
        

    def __call__(self, filepath, mode):
        fp = eg.ParseString(filepath[0])
        if path.isfile(fp) or path.isdir(fp):
            self.plugin.Exec("[%s(%s)]" % (("open","list")[mode], fp))
        if len(filepath) > 1:
            for fp in filepath[1:]:
                fp = eg.ParseString(fp)
                if path.isfile(fp) or path.isdir(fp):
                    self.plugin.Exec("[%s(%s)]" % ("list", fp))                


    def Configure(self, filepath = [], mode=0):
        if filepath == []:
            self.startDir = eg.folderPath.Music
        else:
            self.startDir = path.split(filepath[0])[0]
        text = self.text
        panel = eg.ConfigPanel(resizable=True)      
        radioBox = wx.RadioBox(
            panel, 
            -1, 
            text.radioboxtitle, 
            choices = text.modes, 
            style=wx.RA_SPECIFY_COLS
        )
        radioBox.SetSelection(mode)
        label1Text = wx.StaticText(panel, -1, text.label1)
        pathCtrl = wx.ListBox(
            panel,
            -1,
            choices = filepath,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        pathCtrl.SetToolTipString(text.toolTipList)
        buttonSizer = wx.GridBagSizer(2,10)
        buttonSizer.AddGrowableCol(1)
        buttonSizer.AddGrowableCol(3)
        elemCtrl = wx.Choice(panel, -1, choices=text.elements)
        clearButton = wx.Button(panel, -1, text.clear)
        deleteButton = wx.Button(panel, -1, text.delete)
        choiceLabel = wx.StaticText(panel, -1, text.choiceLbl)
        buttonSizer.Add(choiceLabel,(0,0))
        buttonSizer.Add(elemCtrl,(1,0),flag = wx.EXPAND)
        buttonSizer.Add(deleteButton,(1,2))
        buttonSizer.Add(clearButton,(1,4))
        panel.sizer.Add(label1Text, 0)
        panel.sizer.Add(pathCtrl,1,wx.TOP|wx.EXPAND)
        panel.sizer.Add(buttonSizer,0,wx.TOP|wx.EXPAND,10)
        panel.sizer.Add(radioBox,0,wx.EXPAND|wx.TOP,10)


        def EnableButtons():
            if pathCtrl.GetSelection() > -1:
                deleteButton.Enable(True)
            else:
                deleteButton.Enable(False)
            if pathCtrl.GetCount() == 0:
                clearButton.Enable(False)
            else:
                clearButton.Enable(True)

        EnableButtons()

        def OnPathCtrl(event):
            EnableButtons()
            event.Skip()
        pathCtrl.Bind(wx.EVT_LISTBOX, OnPathCtrl)


        def OnPathCtrlRightClick(event):
            pathCtrl.SetSelection(-1)
            EnableButtons()
            event.Skip()
        pathCtrl.Bind(wx.EVT_RIGHT_DOWN, OnPathCtrlRightClick)


        def OnElemCtrl(event):
            pos = pathCtrl.GetSelection()
            if pos == -1:
                sel = pathCtrl.GetCount()
            else:
                sel = pos
            ix = event.GetSelection()
            if ix == 1:
                fileDialog = wx.FileDialog(
                    panel,
                    message=text.elements[1],
                    wildcard=text.wildcards,
                    defaultDir = self.startDir,
                    style=wx.OPEN|wx.FD_MULTIPLE 
                )
                try:
                    if fileDialog.ShowModal() == wx.ID_OK:
                        val = fileDialog.GetPaths()
                        self.startDir = path.split(val[0])[0]
                        pathCtrl.InsertItems(val, sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                finally:
                    fileDialog.Destroy()
            elif ix == 2:
                folderDialog = wx.DirDialog(
                    panel,
                    message="",
                    defaultPath = self.startDir,
                    style=wx.DD_DIR_MUST_EXIST
                )
                try:
                    if folderDialog.ShowModal() == wx.ID_OK:
                        val = folderDialog.GetPath()
                        pathCtrl.InsertItems([val,], sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                        self.startDir = val
                finally:
                    folderDialog.Destroy()
            elif ix in (3, 4):
                item = text.elements[ix]
                pathCtrl.InsertItems([item[item.find('"')+1:-1],], sel)
                if pos > -1:
                    pathCtrl.SetSelection(sel)
            elif ix == 5:
                dlg = wx.TextEntryDialog(
                    panel,
                    text.message,
                    text.caption,
                    "",
                    wx.OK | wx.CANCEL | wx.CENTRE,
                    wx.DefaultPosition
                )
                if dlg.ShowModal() == wx.ID_OK:
                    val = dlg.GetValue()
                    if val:
                        if val[0] != "{":
                            val = "{" + val
                        if val[-1] != "}":
                            val = val + "}"
                        pathCtrl.InsertItems([val,], sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                dlg.Destroy()
            elemCtrl.SetSelection(0)
            EnableButtons()
            event.Skip()
        elemCtrl.Bind(wx.EVT_CHOICE, OnElemCtrl)


        def OnDeleteButton(event):
            sel = pathCtrl.GetSelection()
            if sel > -1:
                pathCtrl.Delete(sel)
                length = pathCtrl.GetCount()
                if length == sel:
                    sel -= 1
                if sel > -1:
                    pathCtrl.SetSelection(sel)
            EnableButtons()
            event.Skip()
        deleteButton.Bind(wx.EVT_BUTTON, OnDeleteButton)


        def OnClearButton(event):
            pathCtrl.Set([])
            EnableButtons()
            event.Skip()
        clearButton.Bind(wx.EVT_BUTTON, OnClearButton)


        while panel.Affirmed():
            panel.SetResult(
                pathCtrl.GetStrings(), radioBox.GetSelection()
            )
#===============================================================================

class OpenUrl(eg.ActionBase):

    class text:
        label1 = "Radio station url:"


    def __call__(self, url):
        url = eg.ParseString(url)
        filePath = eg.folderPath.TemporaryFiles+"\\!_EG_temp_url_!.pls"
        pls = file(filePath,'w')
        pls.write("[playlist]\nnumberofentries=1\nfile1=%s\ntitle1=Dummy title\n" % url)
        pls.close()
        self.plugin.Exec("[open(%s)]" % filePath)
        remove(filePath)


    def Configure(self, url = ""):
        text = self.text
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, text.label1)
        urlCtrl = wx.TextCtrl(
            panel,
            -1,
            url,
            size=(410,-1),
        )
        panel.sizer.Add(label1Text, 0, wx.TOP,15)
        panel.sizer.Add(urlCtrl,0,wx.TOP,2)
        while panel.Affirmed():
            panel.SetResult(
                urlCtrl.GetValue(),
            )
#===============================================================================

class GetTitle(eg.ActionBase):

    def __call__(self):
        hwnd = HandleXMP()
        if hwnd:
            return GetWindowText(hwnd).decode(eg.systemEncoding)
#===============================================================================

ACTIONS = (
    ( eg.ActionGroup, 'Main', 'Main', 'Adds actions to main control XMPlay',(
        (Run,"Run","Run","Run foobar with its default settings.", None),
        (Exec,"Close","Close","Close",10),
        (Exec,"Close_with_position_saved","Close with position saved","Close with position saved",11),
        (Exec,"Current_track_-_Play/pause","Current track - Play/pause","Current track - Play/pause",80),
        (Exec,"Current_track_-_Stop","Current track - Stop","Current track - Stop",81),
        (Exec,"Current_track_-_Restart","Current track - Restart","Current track - Restart",84),
        (Exec,"Change_track_-_Next","Change track - Next","Change track - Next",128),
        (Exec,"Change_track_-_Previous","Change track - Previous","Change track - Previous",129),
        (Exec,"Change_track_-_Random","Change track - Random","Change track - Random",130),
        (Exec,"Current_track_-_Forward","Current track - Forward","Current track - Forward",82),
        (Exec,"Current_track_-_Back","Current track - Back","Current track - Back",83),
        (OpenFileFolder,"Open_file_folder","Open/Add file(s) or folder","Open or add file(s), playlist(s) or folder(s)",None),
        (OpenUrl,"OpenUrl","Open URL (Internet radio)","Open URL (Internet radio)",None),
        (Exec,"Volume_up","Volume up","Volume up",512),
        (Exec,"Volume_down","Volume down","Volume down",513),
        (Exec,"Toggle_random_play_order","Toggle random play order","Toggle random play order",313),
        (GetTitle,"GetTitle","Get playing song","Get playing song",None),
        (Exec,"Bookmark_-_Set","Bookmark - Set","Bookmark - Set",640),
        (Exec,"Bookmark_-_Resume","Bookmark - Resume","Bookmark - Resume",641),
    )),
        ( eg.ActionGroup, 'Extras', 'Extras', 'Adds extra actions to control XMPlay',(
        (Exec,"Toggle_mini_mode","Toggle mini mode","Toggle mini mode",1),
        (Exec,"Minimize","Toggle minimize","Toggle minimize",2),
        (Exec,"Minimize_to_tray","Toggle minimize to tray","Toggle minimize to tray",3),
        (Exec,"Reload_skin","Reload skin","Reload skin",4),
        (Exec,"Current_track_-_Prev_subsong","Current track - Prev subsong","Current track - Prev subsong",85),
        (Exec,"Current_track_-_Next_subsong","Current track - Next subsong","Current track - Next subsong",86),
        (Exec,"Current_track_-_Plugin_info","Current track - Plugin info","Current track - Plugin info",87),
        (Exec,"Current_track_-_Tray_title_bubble","Current track - Tray title bubble","Current track - Tray title bubble",88),
        (Exec,"Current_track_-_Plugin_info","Current track - Plugin info","Current track - Plugin info",89),
        (Exec,"Toggle_on-top","Toggle on-top","Toggle on-top",7),
        (Exec,"Toggle_time_display","Toggle time display","Toggle time display",8),
        (Exec,"Toggle_looping","Toggle looping","Toggle looping",9),
        (Exec,"DSP_-_Amplification_up","DSP - Amplification up","DSP - Amplification up",514),
        (Exec,"DSP_-_Amplification_down","DSP - Amplification down","DSP - Amplification down",515),
        (Exec,"DSP_-_Equalizer_on/off","DSP - Equalizer on/off","DSP - Equalizer on/off",516),
        (Exec,"DSP_-_Reverb_on/off","DSP - Reverb on/off","DSP - Reverb on/off",517),
        (Exec,"Info_-_Open/close_window","Info - Open/close window","Info - Open/close window",256),
        (Exec,"Info_-_General","Info - General","Info - General",257),
        (Exec,"Info_-_Message","Info - Message","Info - Message",258),
        (Exec,"Info_-_Samples","Info - Samples","Info - Samples",259),
        (Exec,"Info_-_Library","Info - Library","Info - Library",608),
        (Exec,"Info_-_Visuals","Info - Visuals","Info - Visuals",260),
        (Exec,"Info_-_Extended_list","Info - Extended list","Info - Extended list",261),
        (Exec,"Info_-_Scroll_up","Info - Scroll up","Info - Scroll up",262),
        (Exec,"Info_-_Scroll_down","Info - Scroll down","Info - Scroll down",263),
        (Exec,"Info_-_Copy_to_clipboard","Info - Copy to clipboard","Info - Copy to clipboard",264),
        (Exec,"MOD_pattern_-_Scroll_mode","MOD pattern - Scroll mode","MOD pattern - Scroll mode",288),
        (Exec,"MOD_pattern_-_Prev_channel","MOD pattern - Prev channel","MOD pattern - Prev channel",289),
        (Exec,"MOD_pattern_-_Next_channel","MOD pattern - Next channel","MOD pattern - Next channel",290),
        (Exec,"MOD_pattern_-_Mute_channel","MOD pattern - Mute channel","MOD pattern - Mute channel",291),
        (Exec,"MOD_pattern_-_Unmute_all","MOD pattern - Unmute all","MOD pattern - Unmute all",292),
        (Exec,"MOD_pattern_-_Invert_all","MOD pattern - Invert all","MOD pattern - Invert all",293),
        (Exec,"Toggle_MOD_playback_mode","Toggle MOD playback mode","Toggle MOD playback mode",296),
        (Exec,"List_nav_-_Up","List nav - Up","List nav - Up",336),
        (Exec,"List_nav_-_Down","List nav - Down","List nav - Down",337),
        (Exec,"List_nav_-_Page_up","List nav - Page up","List nav - Page up",338),
        (Exec,"List_nav_-_Page_down","List nav - Page down","List nav - Page down",339),
        (Exec,"List_nav_-_Jump_to_current","List nav - Jump to current","List nav - Jump to current",340),
        (Exec,"List_nav_-_Select_all","List nav - Select all","List nav - Select all",341),
        (Exec,"List_nav_-_Invert_selection","List nav - Invert selection","List nav - Invert selection",342),
        (Exec,"List_nav_-_Find_next","List nav - Find next","List nav - Find next",353),
        (Exec,"List_nav_-_Find_previous","List nav - Find previous","List nav - Find previous",354),
        (Exec,"List_nav_-_Find_all","List nav - Find all","List nav - Find all",355),
        (Exec,"List_sort_-_Shuffle","List sort - Shuffle","List sort - Shuffle",320),
        (Exec,"List_sort_-_Title","List sort - Title","List sort - Title",321),
        (Exec,"List_sort_-_Filename","List sort - Filename","List sort - Filename",322),
        (Exec,"List_sort_-_Extension","List sort - Extension","List sort - Extension",323),
        (Exec,"List_sort_-_Reverse","List sort - Reverse","List sort - Reverse",324),
        (Exec,"List_sort_-_Selected_to_top","List sort - Selected to top","List sort - Selected to top",325),
        (Exec,"List_nav_-_Select_dead","List nav - Select dead","List nav - Select dead",343),
        (Exec,"List_-_Remove","List - Remove","List - Remove",370),
        (Exec,"List_-_Remove_&_delete_file","List - Remove & delete file","List - Remove & delete file",371),
        (Exec,"List_-_Play","List - Play","List - Play",372),
        (Exec,"List_-_Toggle_skipping","List - Toggle skipping","List - Toggle skipping",373),
        (Exec,"List_-_Toggle_queuing","List - Toggle queuing","List - Toggle queuing",374),
        (Exec,"List_-_Clear_queue","List - Clear queue","List - Clear queue",375),
        (Exec,"List_-_Plugin_info","List - Plugin info","List - Plugin info",376),
        (Exec,"List_-_Filenames_in_ext._list","List - Toggle filenames in ext. list","List - Toggle filenames in ext. list",377),
        (Exec,"List_-_Show_queue_in_list","List - Show queue in list","List - Show queue in list",379),
        (Exec,"List_-_Auto_advance","List - Auto advance","List - Auto advance",380),
        (Exec,"List_track_-_Add_to/from_library","List track - Add to/from library","List track - Add to/from library",384),
        (Exec,"List_track_-_Plugin_info","List track - Plugin info","List track - Plugin info",385),
        (Exec,"List_-_Undo","List - Undo","List - Undo",400),
        (Exec,"Saved_settings_-_Load_current","Saved settings - Load current","Saved settings - Load current",593),
    )),
)