version="0.0.1"

# plugins/LogRedirector/__init__.py
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
# -----------------
# 0.0.0 by Pako 2010-10-20 14:56 GMT+1
#     - initial version
# 0.0.1 by Pako 2010-10-24 17:57 GMT+1
#     - added check file size feature
#===============================================================================

eg.RegisterPlugin(
    name = "Log redirector",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{E34BB200-A001-410B-B5F2-16B479AF2046}",
    description = ur'''<rst>This plugin is designed to easily redirection of
EventGhost log to text file.''',
    createMacrosOnAdd = False,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2740",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUA////AAD/fHz/"
        "jIz/vb3/TU3/p6f/aGj/mpr/srL/x8f/2dn/0NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAABub2l0QgZzZVliYVRlZHIAAAJCVAdvdHR0QgUEb050ZmVUA2h4AnBkaVdL"
        "AmhpZUgCdGhhQwdvaXRCBQZvTm5iYVRlZHIAAQJCVAdvdHR0QgUEa090ZmUDALgCcG9p"
        "VwUCaHRlSAZ0aGdDBxlpdHAFBm5PbnRhVAhkck8CAnJUBwB0dHVCCW5hQ25sZWNmZUwB"
        "CANwb1RXBXhodGRIBktoZ2kHGQJ0cGEGbm9udEJjbmFUCGxyT2ICcmUFAABpZEVkRQhw"
        "bklMBHQCdGZvVAMFPgJ0ZGkA6QNpZUgCdGhhVAhkck8EAnJUBgBlbmFuUAZwZVNmZUwD"
        "DAICcG9pVwUDaHRIBgBoZ2kKAgJldmV0dU8GB3JvTnZDBWVyb2xsYwdjYWxhUBB0bmVr"
        "Y2F1b3IICGRPYmFyZWQAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAAB5utwAAAAAAAAAAAAA"
        "AAAAAAMAAAA3BI8AAAAAAAAAAAAAAAAAAAMAAQEAAQAAAAAAAAAAAABhFgh5urQAEHAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAJhFgh5veQAEBBGzxB5PdhxxNgAAAAAAAgAAGAAAAB5QBhgKuLGAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAIRJREFUeNql01kOgCAMBNCW"
        "VZD7n9cYY8PSOkb7V3xBOyARLp7L+fAMzvIIcESg28MADEFCICPAC7jaDQF6DbwB3N2W"
        "vzkEACQmA/QHDh6rIAYVENWofMKQwy5N1QH5NYYpSWXOEShbjCtN2qIDyjKrAeoyyPxS"
        "ySIbIMlCQ1es//++1wFodAMcT/AbEgAAAABJRU5ErkJggg=="
    ),
)
#===============================================================================

from os import path, fsync
from datetime import datetime as dt
from codecs import open as openFile
from threading import Thread, Event
from winsound import PlaySound, SND_ASYNC
from win32gui import MessageBox
from Queue import Queue
#===============================================================================

class Text:
    commitLabel = "File commit interval (minutes):"
    logMode = "Logging mode"
    modes = (
        "Only standard EventGhost log",
        "Standard EventGhost log and selected text file",
        "Only selected text file",
    )
    boxTitle = 'Folder "%s" is incorrect'
    toolTipFile = "Press button and browse to select a logfile ..."
    browseFile = 'Select the logfile'
    label = "Log file:"
    size_1 = "Once the file reaches the size of"
    size_2 = "MiB, leave only the last"
    size_3 = "MiB"
    exceeded = "MaxSizeExceeded"
    truncated = "Truncated"
    mess = """In the folder "%s"
is name "Log.txt" reserved for system logfile of EventGhost.

Change the file name or folder !"""
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):

    def __init__(self,*args,**kwargs):
        if 'defaultFile' in kwargs:
            self.defaultFile = kwargs['defaultFile']
            del kwargs['defaultFile']
        else:
            self.defaultFile = ""
        eg.FileBrowseButton.__init__(self, *args, **kwargs)


    def GetValue(self):
        if self.textControl.GetValue():
            res = self.textControl.GetValue()
        else:
            res = "%s\\%s" % (self.startDirectory, self.defaultFile)
        return res


    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================
class FileCommitThread(Thread):

    def __init__(
        self,
        file,
        plugin,
        period,
        maxSize,
        minSize,
        check
    ):
        self.abort = False
        self.threadFlag = Event()
        self.file = file
        self.plugin = plugin
        self.period = period
        self.check = check
        self.maxSize = maxSize
        self.minSize = minSize
        Thread.__init__(self, name = 'LogCommit_Thread')


    def run(self):
        while not self.abort:
            self.file.flush()
            fsync(self.file.fileno())
            if self.check:
                fn = self.file.name
                sz = path.getsize(fn)
                if sz > self.maxSize*1048576:
                    eg.TriggerEvent(self.plugin.text.exceeded, prefix="LogRedirector.LogFile", payload = sz)
                    self.plugin.SetFlag(False)
                    self.file.close()
                    tmpf = open(fn, 'rb+')
                    tmpf.seek(-1048576*self.minSize,2)
                    data = tmpf.read()
                    pos = data.find("\r\n")
                    tmpf.seek(0)
                    tmpf.write(data[pos+2:])
                    tmpf.truncate()
                    tmpf.close()
                    self.file = self.plugin.OpenFile(fn)
                    eg.TriggerEvent(self.plugin.text.truncated, prefix="LogRedirector.LogFile", payload = path.getsize(fn))
                    self.plugin.SetFlag(True)
            if self.abort:
                break
            self.threadFlag.wait(self.period)
            self.threadFlag.clear()


    def AbortThread(self):
        self.abort = True
        self.threadFlag.set()
#===============================================================================

class LogRedirector(eg.PluginBase):

    text = Text
    default = None
    ioFile = None
    commitThread = None

    def OpenFile(self, logfile):
        self.ioFile = openFile(logfile, encoding = 'utf-8', mode = 'a')
        return self.ioFile
    
    def SetFlag(self, val):
        self.flag = val


    def __start__(
        self,
        mode = 0,
        logfile = None,
        interval = 1,
        maxSize = 20,
        minSize = 10,
        check = False
    ):
        if check:
            self.q = Queue()
            self.flag = True
        self.default = eg.Log._WriteLine
        self.check = check
        
        def WriteLine2File(when, indent, wRef, line):
            wref = wRef.__repr__().split(" ") if wRef else ""
            if len(wref) == 1:
                wref = "EVENT: "
            elif len(wref) == 7:
                wref = wref[4][1:-5].upper()+": "
            wref = wref if wref != "PLUGIN: " else ""
            if self.check:
                self.q.put("%s  %s%s%s\r\n" % (str(dt.fromtimestamp(when))[:19],indent*3*" ",wref,line.strip()))
                if self.flag:
                    while not self.q.empty():
                        self.ioFile.write(self.q.get())
            else:
                self.ioFile.write("%s  %s%s%s\r\n" % (str(dt.fromtimestamp(when))[:19],indent*3*" ",wref,line.strip()))
        
        if mode == 0:
            def extWriteLine(self, line, icon, wRef, when, indent):
                self.ctrl.WriteLine(line, icon, wRef, when, indent)
            self.ioFile = None
        else:
            self.OpenFile(logfile)
            fct = FileCommitThread(
                self.ioFile,
                self,
                60 * interval,
                maxSize,
                minSize,
                check
            )
            fct.start()
            self.commitThread = fct
        if mode == 1:
            def extWriteLine(self, line, icon, wRef, when, indent):
                self.ctrl.WriteLine(line, icon, wRef, when, indent)
                WriteLine2File(when, indent, wRef, line)
        if mode == 2:
            def extWriteLine(self, line, icon, wRef, when, indent):
                WriteLine2File(when, indent, wRef, line)
        eg.Log._WriteLine = extWriteLine


    def __stop__(self):
        if self.commitThread:
            fct = self.commitThread
            if fct.isAlive():
                fct.AbortThread()
            del self.commitThread
        self.commitThread = None
        eg.Log._WriteLine = self.default
        if self.ioFile:
            if self.check:
                while not self.q.empty():
                    self.ioFile.write(self.q.get())
            self.ioFile.close()
            self.ioFile = None


    def Configure(
        self,
        mode = 0,
        logfile = None,
        interval = 1,
        maxSize = 20,
        minSize = 10,
        check = False
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        self.logfile = logfile
        logFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.configDir,
            defaultFile = "EventGhost_Log.txt"
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logLabel = wx.StaticText(panel, -1, text.label)
        radioBox = wx.RadioBox(
            panel, 
            -1, 
            text.logMode, 
            choices = text.modes, 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(mode)
        commitLabel = wx.StaticText(panel, -1, text.commitLabel)
        commitCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            interval,
            min=1,
            max=99,
        )
        sizeCheck = wx.CheckBox(panel, -1, "")
        sizeCheck.SetValue(check)
        sizeLabel_1 = wx.StaticText(panel, -1, text.size_1)
        sizeCtrl_1 = eg.SpinIntCtrl(
            panel,
            -1,
            maxSize,
            min=2,
            max=50,
        )
        sizeLabel_2 = wx.StaticText(panel, -1, text.size_2)
        sizeCtrl_2 = eg.SpinIntCtrl(
            panel,
            -1,
            minSize,
            min=1,
            max=49,
        )
        sizeLabel_3 = wx.StaticText(panel, -1, text.size_3)
        commitSizer = wx.BoxSizer(wx.HORIZONTAL)
        commitSizer.Add(commitLabel, 0, wx.TOP, 3)
        commitSizer.Add(commitCtrl, 0, wx.LEFT, 8)
        sizeSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizeSizer.Add(sizeCheck, 0, wx.TOP|wx.RIGHT, 3)
        sizeSizer.Add(sizeLabel_1, 0, wx.TOP, 3)
        sizeSizer.Add(sizeCtrl_1, 0, wx.LEFT|wx.RIGHT, 5)
        sizeSizer.Add(sizeLabel_2, 0, wx.TOP, 3)
        sizeSizer.Add(sizeCtrl_2, 0, wx.LEFT|wx.RIGHT, 5)
        sizeSizer.Add(sizeLabel_3, 0, wx.TOP, 3)
        sizerAdd = panel.sizer.Add
        sizerAdd(radioBox, 0, wx.TOP | wx.EXPAND, 2)
        sizerAdd(logLabel, 0, wx.TOP, 15)
        sizerAdd(logFileCtrl, 0, wx.TOP | wx.EXPAND, 2)
        sizerAdd(commitSizer, 0, wx.TOP | wx.EXPAND, 15)
        sizerAdd(sizeSizer, 0, wx.TOP | wx.EXPAND, 15)


        def DummyHandle(evt):
            pass
        sizeCtrl_1.Bind(wx.EVT_TEXT, DummyHandle)
        sizeCtrl_2.Bind(wx.EVT_TEXT, DummyHandle)


        def Validation(event = None):
            flg_1 = len(self.logfile) > 0
            val = bool(radioBox.GetSelection())
            flg_2 = not val or (val and self.logfile is not None)
            flg_3 = sizeCtrl_1.GetValue() > sizeCtrl_2.GetValue()
            flg = flg_1 and flg_2 and flg_3
            panel.dialog.buttonRow.okButton.Enable(flg)
            panel.dialog.buttonRow.applyButton.Enable(flg)
        sizeCtrl_1.Bind(eg.EVT_VALUE_CHANGED, Validation)
        sizeCtrl_2.Bind(eg.EVT_VALUE_CHANGED, Validation)


        def logFileChange(event):
            val = logFileCtrl.GetTextCtrl().GetValue()
            if val.lower() == u"%s\\log.txt" % unicode(eg.configDir).lower():
                PlaySound('SystemExclamation', SND_ASYNC)
                MessageBox(
                    panel.GetHandle(),
                    text.mess % unicode(eg.configDir),
                    "EventGhost - Log redirector",
                    48
                    )
                logFileCtrl.GetTextCtrl().SetValue(self.logfile)
                return
            self.logfile = val
            Validation()
        logFileCtrl.Bind(wx.EVT_TEXT, logFileChange)


        def onSizeCheck(event = None):
            val=sizeCheck.GetValue()
            sizeLabel_1.Enable(val)
            sizeCtrl_1.Enable(val)
            sizeLabel_2.Enable(val)
            sizeCtrl_2.Enable(val)
            sizeLabel_3.Enable(val)            
        sizeCheck.Bind(wx.EVT_CHECKBOX, onSizeCheck)
        onSizeCheck()


        def onRadioBox(event = None):
            val = bool(radioBox.GetSelection())
            if not val or self.logfile is None:
                logFileCtrl.GetTextCtrl().ChangeValue("")
            else:
                logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)
            logLabel.Enable(val)
            logFileCtrl.Enable(val)
            commitLabel.Enable(val)
            commitCtrl.Enable(val)
            sizeCheck.Enable(val)
            if val:
                val=sizeCheck.GetValue()
            sizeCheck.SetValue(val)
            onSizeCheck()
        radioBox.Bind(wx.EVT_RADIOBOX, onRadioBox)
        onRadioBox()

        while panel.Affirmed():
            val = bool(radioBox.GetSelection())
            panel.SetResult(
                val,
                logFileCtrl.GetTextCtrl().GetValue() if val else self.logfile,
                commitCtrl.GetValue(),
                sizeCtrl_1.GetValue(),
                sizeCtrl_2.GetValue(),                
                sizeCheck.GetValue()
            )

