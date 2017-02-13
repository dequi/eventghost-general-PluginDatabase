version="0.1.0" 
# Plugins/VirtualNumpad/__init__.py
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

eg.RegisterPlugin(
    name = "Virtual Numpad",
    author = "Pako",
    version = version,
    kind = "other",
    description = (
        'Virtual Numpad'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/xxxxx",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABsAAAAgCAMAAADUt/MJAAADAFBMVEX///8AAAAQEBAR"
        "EREDAwPZ2dmYmJgEBARaWloBAQEGBgYaGhpvb2/V1dXNzc3JyckODg7Pz8/Hx8fKysrM"
        "zMynp6dSUlJ4eHhZWVkFBQWzs7MYGBiMjIy+vr7S0tJzc3O4uLhYWFiEhIRMTEw7Ozt7"
        "e3uwsLDGxsbLy8sJCQkKCgoICAhnZ2diYmInJycMDAy7u7u8vLwhISEWFhYCAgKsrKx/"
        "f392dnZjY2O3t7fd3d08PDzOzs4qKiqNjY1JSUmAgIDg4OC5ubmjo6OmpqYAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADLlYDLjZQAADQA"
        "AADJ/BzJ/BwAACQAAAAAAAAAAAAAAAAAAAAAAGgAABNBmXQAAAAAAADJ/FDJ/FAAAMAA"
        "AAAAAAAAAAAAEAAAAAAAAADJ/HTJ/HQAAJwAAADJ/ITJ/IQAAIwAAAAAAAAAAAAAAAAA"
        "AAAAAADJ+9jJ+WgAAGgAAADJ/LjJ/LgAAFgAAABAAAAAAAAAAAAAAAAAAADJ+3DLk0QA"
        "ADQAAADJ/OzJ/OwAACQAAAAAAAgAAAAAAAAAAAAAATgAABNBmXQAAAAAAADJ/SDJ/SAA"
        "ACQAAAAAAAAAAACAAAAAAAAAAWwAABNBmXQAAAAAAADJ/VTJ/VQAAVwAAAAAAAAAAAAA"
        "AAAAAAAAAADJ/XjJ/XgAATgAAADJ/YjJ/YgAACQAAAAAAAAAAAAAAAAAAAAAADQAABNB"
        "mXQAAAAAAADJ/bzJ/bwAAPQAAAAAAAAAAAAAAAAAQAAAAADJ+gTH4JQAANAAAADJ/fDJ"
        "/fAAACQAAAAAAAAAAAAAAAAAAAAAADQAABNBmXQAAAAAAADJ/iTJ/iQAAIzetFnHAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAN5JREFUeNqFktcWgjAQREHF"
        "2FHsvYsde+/6/99kMAlZQnGfMrlMzu4OkvSnZLeyswBEQR9fiCDFxxd28yHCIlRGIYsR"
        "Fvfpk6mElLQqpVKWNtsIyBmf0fFRy6o5iPKMFdihaLESuyrzRiqUVd26rAkbs+2l7p0C"
        "ma/BZbPV5qJjwm6PiD58BVkB4iwGOjkMxXCdm0Ajb+blG+Np0MRk09ncAGFC30J4Y8nk"
        "Cn63hraNvMVix8fd6wchd0vZ/pfjj53ctnmmnV2c6MpnMoSMbnBg5Q5MD8c+nq/3B5fG"
        "b74jbAz6WoeoZQAAAABJRU5ErkJggg=="
    ),
)

#====================================================================
#cls types for ACTIONS list:       
class StartDirect(eg.ActionClass):
    class Text:
        dirLabel = ">> Direct mode <<"

    def __call__(self):
        if self.plugin.event is None:
            self.plugin.mode = 'direct'
            self.plugin.event = self.Text.dirLabel
            self.plugin.number=''
            self.plugin.ShowNumLabel()
            
        
#======================================================================            
class StartPayload(eg.ActionClass):
    class Text:
        label = "Event suffix:"
        noSuffix = "NoSuffix!!!"

    def __call__(self,event=None):
        if self.plugin.event is None:
            self.plugin.mode = 'payload'
            if event is not None:
                self.plugin.event = event
            else:
                self.plugin.event=self.Text.noSuffix
            self.plugin.number=''
            self.plugin.ShowNumLabel()
            
    def Configure(self,event=''):
        panel = eg.ConfigPanel(self)
        labelText = wx.StaticText(panel, -1, self.Text.label)
        eventNameCtrl = wx.TextCtrl(panel, -1, event, size = (200,-1), style=wx.TE_NOHIDESEL)
        panel.sizer.Add(labelText,0,wx.TOP,50)
        panel.sizer.Add(eventNameCtrl,0,wx.TOP,5)
        
        while panel.Affirmed():
            panel.SetResult(
                eventNameCtrl.GetValue(),
            )  
        
#======================================================================            
class DigitAction(eg.ActionClass):

    def __call__(self):
        if self.plugin.event is not None:
            self.plugin.number+=self.value
            self.plugin.ShowNumLabel()
#======================================================================            
class Enter(eg.ActionClass):

    def __call__(self):
        if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
            self.plugin.SendEvent()
            self.plugin.event = None
                
#======================================================================
class Backspace(eg.ActionClass):

    def __call__(self):
        if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
                self.plugin.number = self.plugin.number[:-1]
                if len(self.plugin.number) == 0:
                    self.plugin.numDialog.Destroy()
                    self.plugin.numDialog = None
                    self.plugin.event = None
                else:
                    self.plugin.ShowNumLabel()

#======================================================================
class Cancel(eg.ActionClass):

    def __call__(self):
        if self.plugin.numDialog is not None:
            self.plugin.number = ''
            self.plugin.numDialog.Destroy()
            self.plugin.numDialog = None
            self.plugin.event = None

#======================================================================
ACTIONS = (
    ( eg.ActionGroup, 'StartInput', 'Start input', 'Start input.',(
        (StartDirect, 'StartDirect', 'Start input - direct', 'Start input - direct.', None ),
        (StartPayload, 'StartPayload', 'Start input - payload', 'Start input - payload.', None ),
    ),),
    (DigitAction, 'Digit0', 'Digit 0', 'Type Digit 0', '0' ),
    (DigitAction, 'Digit1', 'Digit 1', 'Type Digit 1', '1' ),
    (DigitAction, 'Digit2', 'Digit 2', 'Type Digit 2', '2' ),
    (DigitAction, 'Digit3', 'Digit 3', 'Type Digit 3', '3' ),
    (DigitAction, 'Digit4', 'Digit 4', 'Type Digit 4', '4' ),
    (DigitAction, 'Digit5', 'Digit 5', 'Type Digit 5', '5' ),
    (DigitAction, 'Digit6', 'Digit 6', 'Type Digit 6', '6' ),
    (DigitAction, 'Digit7', 'Digit 7', 'Type Digit 7', '7' ),
    (DigitAction, 'Digit8', 'Digit 8', 'Type Digit 8', '8' ),
    (DigitAction, 'Digit9', 'Digit 9', 'Type Digit 9', '9' ),
    (Enter, 'Enter', 'Enter', 'Enter - Goto slide.', None),
    (Backspace, 'Backspace', 'Backspace', 'Backspace (delete last digit).', None),
    (Cancel, 'Cancel', 'Cancel', 'Cancel - Do not goto a slide.', None),
) 

#====================================================================
class VirtualNumpad(eg.PluginClass):
        
    numDialog = None
    number = ''
    event = None
    mode = ''

    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        
        
    def SendEvent(self):
        if self.mode == 'direct':
            self.TriggerEvent(str(self.number))
        else:
            self.TriggerEvent(self.event, str(self.number))
        self.number = ''
        self.numDialog.Destroy()
        self.numDialog = None


    def ShowNumLabel(self):
        if self.numDialog is not None:
            statTextNum = self.numDialog.GetSizer().GetChildren()[1].GetWindow()
            statTextNum.SetLabel(self.number)
        else:
            self.numDialog = wx.Frame(
                None, -1, 'VirtualNumpad', 
                style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER   
            )
            statTextEvent=wx.StaticText(
                self.numDialog,
                -1,
                self.event,
                style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
            )
            statTextNum=wx.StaticText(
                self.numDialog,
                -1,
                self.number,
                style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
            )
            fontEvent = statTextEvent.GetFont()
            fontNum = statTextNum.GetFont()
            fontEvent.SetPointSize(32)
            fontNum.SetPointSize(64)
            fontNum.SetWeight(wx.BOLD)
            statTextEvent.SetFont(fontEvent)
            statTextNum.SetFont(fontNum)
            self.numDialog.SetBackgroundColour(wx.Colour(100,149,237))
            statTextNum.SetForegroundColour(wx.Colour(238, 238, 0))
            statTextNum.SetBackgroundColour(wx.Colour(0, 0, 128))
            w1,h1 = statTextEvent.GetTextExtent(self.event)
            w2,h2 = statTextNum.GetTextExtent('88888')
            w=max(w1,w2)
            self.numDialog.SetSize((w+16,h1+h2+16))
            statTextEvent.SetPosition((7,7))
            statTextNum.SetPosition((7,7+h1))
            statTextEvent.SetSize((w,h1))
            statTextNum.SetSize((w,h2))
            mainSizer =wx.BoxSizer(wx.VERTICAL)
            self.numDialog.SetSizer(mainSizer)
            mainSizer.Add(statTextEvent, 0, wx.EXPAND)
            mainSizer.Add(statTextNum, 0, wx.EXPAND)
            self.numDialog.Centre()
            self.numDialog.Show()        
#====================================================================

