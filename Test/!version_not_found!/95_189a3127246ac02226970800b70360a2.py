version = "0.0.0"
# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
    name = "Test",
    author = "krambriw",
    version = version,
    kind = "program",
    createMacrosOnAdd = False,
    description = "Testing.",
    help = "<i>SOS</i>",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABcAAAAiCAMAAACDQ7KMAAADAFBMVEXRpOgAAAD//wD/"
        "//+AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0sMcANLAAAMgAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAADHAACwx7xADwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADH0qzH0qwAAVwAAAEAAADH0Dj/CYkA"
        "AAAAAAAAAAAAAAMAAADYCo0AAAAAAAAAAAAAAAD///8AAQEAAQAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAQEAAAAAAADH02zH02wAAJwAAAAAAADH04DH04AAAIgAAAAAABQA"
        "ACtCZRgAAABE9RDH0VDCEnwAAAAAAAgAAGAAAADH07zH07wAAEwAAAAAAADXE2ZbAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAIZJREFUeNq1kcsWgCAIRAfj"
        "/785BTEeeXLTrOwCOkzAh0hVaBMhVAa9hmJFaZsCk8PtkRVIMHgI+ojHYkcLMiB8zbLj"
        "dkL4IjgPvov6e97zmvbrx1tjHEjcQsq47y048olR8EyD8i0zDaC0oxhUXvFmn5ySLzC/"
        "4ZjSiTb9ZP/71P+G/+T/Bo2CAlhdZWJTAAAAAElFTkSuQmCC"
    ),
)

#===============================================================================
class Text:
    A_label = " A_label"
    B_label = " B_label"
      

#===============================================================================
class Test(eg.PluginClass):
    text=Text
    
    #def __init__(self):
        #self.AddAction(ActionA)


    def __start__(self, A=False, B=False):
        if A:
            print "B is not True !!!"

                     
    def Configure(self, A=False, B=False):
        panel = eg.ConfigPanel(self)
        A_ctrl = wx.CheckBox(panel, -1, '  '+self.text.A_label)
        B_ctrl = wx.CheckBox(panel, -1, '  '+self.text.B_label)
        A_ctrl.SetValue(A)    
        B_ctrl.SetValue(B)    
        panel.AddCtrl(A_ctrl)
        panel.AddCtrl(B_ctrl)
        
        def On_B_CheckBox(event=None):
            flag = B_ctrl.GetValue()
            A_ctrl.Enable(not flag)
            if flag:
                A_ctrl.SetValue(False)
            if event is not None:
                event.Skip() #mandatory for "Apply button" functionality !!!
        B_ctrl.Bind(wx.EVT_CHECKBOX, On_B_CheckBox)
        
        On_B_CheckBox() #for initialisation after open dialog (panel)
        
        while panel.Affirmed():
            panel.SetResult(A_ctrl.GetValue(),B_ctrl.GetValue())
        
