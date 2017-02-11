version="0.1.0" 
# plugins/WriteTextToFile/__init__.py
#
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
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

eg.RegisterPlugin(
    name = "Write text to file",
    author = "Pako",
    version = version,
    kind = "other",
    createMacrosOnAdd = False,
    description = (
        'Write text to selected file. Text is for instance "{eg.result}".'
        '<BR>'
        'Plugin can write date and time too (logger).'
    ),
    #url = "http://www.eventghost.org/forum/viewtopic.php",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEX4/PjgtGjIlFDI"
        "kEjYsFjYqFDYpGjw4Mj44MjIlEDYvJDguCjw1KD44MDw2LjIkFD47MD44KjYrGjwzKDI"
        "mFj49LDw2GjwzGjQnFjYqHDw3GDw1ED47IjgtFjYjDi4kCC4iCDw5LjgyLDIqGCQbBj4"
        "5NCwfDDAmDDYxGjInEjAgDDoqGDomEDAZBCoYBCwdChYQBDozKjAiEiYaCDYwJAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVBa15AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAGdJREFUeNpjYMADGJmYWZD5"
        "rGzsHJxcCD43Dy8HBx8/gi8gKCQszCeC4IuKiUtIMiPxpaRlZOVw8eXR+AqKaHwlZRS+"
        "CruqmrqGphbcASoc2jq6evoIFxpICBsaIfEZDAyM9U3weBkAHOgJw4bE4b0AAAAASUVO"
        "RK5CYII="
    ),
)

import os
import time

class WriteTextToFile(eg.PluginClass):
    def __init__(self):
        self.AddAction(Write)


class Write(eg.ActionClass):
    name = "Write text to file"
    description = "Writes text to selected file."
    class text:
        TreeLabel = "Write %s to file: %s"
        FilePath = "Path to file:"
        browseFileDialogTitle = "Choose the file"
        txtMode = "Mode of write"
        overwrite = "File overwrite"
        append = "Append to file"
        newLine = "Append to file with new line"
        writeToLog = "Write to EventGhost Log too"
        error = "Could not open file %s"
        systemPage = "System code page"
        pageChoice = "Manual choice"
        hex = "HEX"
        txtCoding = "Output code page"
        codePage = "Code page:"
        String = "Text to write:"
        logTimes = "Log Times"
    
    def __call__(self, string = "", fileName = '', mode = 0, log = False, times = False, coding = 0, page = ""):
        string = eg.ParseString(string)
        fileName = eg.ParseString(fileName)
        modeStr='w' if mode==0 else 'a'
        if coding == 2:
            result = string.encode('hex').upper()
        else:
            result=string.encode(page if coding==0 else eg.systemEncoding)
        if log:
            print result
        try:
            file = open(fileName, modeStr)
            if mode == 2:
                file.write("\x0A")
            if times:
                currentTime = time.time()
                file.write(time.strftime("%c", time.localtime(currentTime))+"  ")                
            file.write(result)
            file.close()
        except:
            self.PrintError(self.text.error % fileName)
            
    
    def GetLabel(self, string, fileName, mode, log, times, coding, page):
        return self.text.TreeLabel % (string, os.path.split(fileName)[1])


    def Configure(self, string="", fileName='', mode=0, log=False, times = False, coding=0, page=""):
        panel = eg.ConfigPanel(self)
        text = self.text
        stringText = wx.StaticText(panel, -1, text.String)
        stringCtrl = wx.TextCtrl(panel, -1, string)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            -1, 
            size=(320,-1),
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        radioBoxMode = wx.RadioBox(
            panel, 
            -1, 
            text.txtMode,
            (0,0),
            (200,80),
            choices=[text.overwrite, text.append, text.newLine],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        radioBoxCoding = wx.RadioBox(
            panel, 
            -1, 
            text.txtCoding,
            (0,0),
            (200,80),
            choices=[text.pageChoice, text.systemPage, text.hex],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxCoding.SetSelection(coding)
        writeToLogCheckBox = wx.CheckBox(panel, -1, text.writeToLog)
        writeToLogCheckBox.SetValue(log)
        timesCheckBox = wx.CheckBox(panel, -1, text.logTimes)
        timesCheckBox.SetValue(times)

        mySizer = wx.FlexGridSizer(2,2)
        Add = mySizer.Add
        panel.sizer.Add(stringText)
        panel.sizer.Add(stringCtrl, 0, wx.EXPAND)
        panel.sizer.Add(fileText,0,wx.TOP,5)
        panel.sizer.Add(filepathCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mySizer)
        Add(radioBoxMode,0,wx.TOP,5)
        
        chkBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        chkBoxSizer.Add(writeToLogCheckBox,0,wx.TOP|wx.LEFT,12)        
        chkBoxSizer.Add(timesCheckBox,0,wx.TOP|wx.LEFT,12)
        
        Add(chkBoxSizer)
        Add(radioBoxCoding,0,wx.TOP,5)
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        Add(pageSizer, 0, wx.TOP|wx.LEFT,10)
        labelCtrl = panel.StaticText(text.codePage)
        pageCtrl = wx.TextCtrl(panel,-1,page)
        pageSizer.Add(labelCtrl, 0, wx.TOP,-2)
        pageSizer.Add(pageCtrl, 0, wx.TOP,2)
        
        
        

        def onCodingChange(event=None):
            if radioBoxCoding.GetSelection()==0:
                if ((pageCtrl.GetValue()=='System code page') | (pageCtrl.GetValue()=='HEX')):
                   pageCtrl.SetValue('') 
                labelCtrl.Enable(True)
                pageCtrl.Enable(True)
            else:
                pageCtrl.SetValue('System code page' if radioBoxCoding.GetSelection()==1 else 'HEX')
                labelCtrl.Enable(False)
                pageCtrl.Enable(False)
            if event:
                event.Skip()
        radioBoxCoding.Bind(wx.EVT_RADIOBOX, onCodingChange)
        onCodingChange()

        
        while panel.Affirmed():
            panel.SetResult(
                stringCtrl.GetValue(),
                filepathCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                writeToLogCheckBox.IsChecked(),
                timesCheckBox.IsChecked(),
                radioBoxCoding.GetSelection(),
                pageCtrl.GetValue(),
            )        
