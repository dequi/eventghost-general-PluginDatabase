version = "0.0.0"

eg.RegisterPlugin(
    name = "Test",
    author = "krambriw",
    version = version,
    kind = "program",
    description = "Testing",
)
import wx.lib

#===============================================================================
class Test(eg.PluginClass):
    
    def __init__(self):
        self.AddAction(MyAction)

class MyAction(eg.ActionClass):
    class text:
        txtMyValue = "My value"

        
    def __call__(self, tag, item):
        print tag
        print item
        
                
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        tag = "",
        item = ""
        ):
            
        panel = eg.ConfigPanel(self)

        # Create a dropdown to select tag
        tagCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        t_list = ['a','b','c','d']
        tagCtrl.AppendItems(strings=t_list) 
        if t_list.count(tag)==0:
            tagCtrl.Select(n=0)
        else:
            tagCtrl.SetSelection(int(t_list.index(tag)))
        tag = tagCtrl.GetStringSelection()
        
        staticBox = wx.StaticBox(panel, -1, "Select Tag")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(tagCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        tagCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown to select item
        itemCtrl = wx.Choice(parent=panel, pos=(10,10)) 

        if tag == "a":
            i_list = ['a','b','c','d']
        elif tag == "b":
            i_list = ['b','c','d','e']
        elif tag == "c":
            i_list = ['c','d','e','f']
        elif tag == "d":
            i_list = ['d','e','f','g']

        itemCtrl.AppendItems(strings=i_list) 
        if i_list.count(item)==0:
            itemCtrl.Select(n=0)
        else:
            itemCtrl.SetSelection(int(i_list.index(item)))
        item = itemCtrl.GetStringSelection()
        
        staticBox = wx.StaticBox(panel, -1, "Select Item")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(itemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        itemCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
     
        while panel.Affirmed():
            panel.SetResult(
                tagCtrl.GetStringSelection(),
                itemCtrl.GetStringSelection()
            )