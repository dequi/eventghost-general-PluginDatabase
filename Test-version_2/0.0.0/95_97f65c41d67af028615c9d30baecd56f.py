version = "0.0.0"

eg.RegisterPlugin(
    name = "Test-version_2",
    author = "krambriw",
    version = version,
    kind = "program",
    guid = "{F9D81883-5DB9-4795-A904-F12C38FE154F}",
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


    def OnItemChoice(self, event): # For future use ???
        choice = event.GetSelection()
        event.Skip()
        return choice

               
    def Configure(
        self,
        tag = "",
        item = ""
        ):
           
        panel = eg.ConfigPanel(self)
        self.item = item

        # Create a dropdown to select tag
        tagCtrl = wx.Choice(parent=panel, pos=(10,10))
        t_list = ['a','b','c','d']
        tagCtrl.AppendItems(strings=t_list)
        if t_list.count(tag)==0:
            tagCtrl.Select(n=0)
        else:
            tagCtrl.SetSelection(int(t_list.index(tag)))
        #tag = tagCtrl.GetStringSelection()
       
        staticBox = wx.StaticBox(panel, -1, "Select Tag")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(tagCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown to select item
        itemCtrl = wx.Choice(parent=panel, pos=(10,10))

    # Get the choice from dropdown and perform some action
        def OnChoice(event = None):                # "event = None" is used when opening the dialog
            choice = tagCtrl.GetSelection()
            tag = tagCtrl.GetStringSelection()
            if tag == "a":
                i_list = ['a','b','c','d']
            elif tag == "b":
                i_list = ['b','c','d','e']
            elif tag == "c":
                i_list = ['c','d','e','f']
            elif tag == "d":
                i_list = ['d','e','f','g']
            itemCtrl.Clear()
            itemCtrl.AppendItems(strings=i_list)
    #        if i_list.count(self.item)==0:
            if i_list.count(tag)==0:                 # Note: I do not know how it actually has to work
                sel = 0
            else:
    #            sel = int(i_list.index(self.item))
                sel = int(i_list.index(tag))         # Note: I do not know how it actually has to work
            itemCtrl.SetSelection(sel)
            if event:
                event.Skip()
            return choice                            # For future use ???
        tagCtrl.Bind(wx.EVT_CHOICE, OnChoice)
        OnChoice()                                   # This is used when opening the dialog

        #item = itemCtrl.GetStringSelection()
       
        staticBox = wx.StaticBox(panel, -1, "Select Item")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(itemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        itemCtrl.Bind(wx.EVT_CHOICE, self.OnItemChoice)
     
        while panel.Affirmed():
            panel.SetResult(
                tagCtrl.GetStringSelection(),
                itemCtrl.GetStringSelection()
            )