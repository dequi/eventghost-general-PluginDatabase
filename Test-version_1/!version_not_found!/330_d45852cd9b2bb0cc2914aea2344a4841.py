version = "0.0.0"

eg.RegisterPlugin(
    name = "Test-version_1",
    author = "krambriw",
    version = version,
    kind = "program",
    guid = "{64B7D9E6-D36E-4377-9C38-B34430463F09}",
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
    def OnTagChoice(self, event = None):         # "event = None" is used when opening the dialog
        itemCtrl = self.itemCtrl
        tagCtrl = self.tagCtrl
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
        return choice               # For future use ???


    def OnItemChoice(self, event):  # For future use ???
        choice = event.GetSelection()
        event.Skip()
        return choice


    def OnDataChoice(self, event):  # For future use ???
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        tag = "",
        item = "",
        data = ""
        ):
           
        panel = eg.ConfigPanel(self)
        self.item = item
        self.data_type = ''

        # Create a dropdown to select tag
        tagCtrl = self.tagCtrl = wx.Choice(parent=panel, pos=(10,10))
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
        tagCtrl.Bind(wx.EVT_CHOICE, self.OnTagChoice)

        # Create a dropdown to select item
        itemCtrl = self.itemCtrl = wx.Choice(parent=panel, pos=(10,10))
        self.OnTagChoice()                                # This is used when opening the dialog
        i_list = itemCtrl.GetStrings()
        if item in i_list:
            itemCtrl.SetStringSelection(item)
            if(
                item == 'a'
                or item == 'b'
                or item == 'c'
                or item == 'd'
            ):
                self.data_type = 'bool'

            if(
                item == 'e'
                or item == 'f'
                or item == 'g'
            ):
                self.data_type = 'string'


        #item = itemCtrl.GetStringSelection()
       
        staticBox = wx.StaticBox(panel, -1, "Select Item")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(itemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        itemCtrl.Bind(wx.EVT_CHOICE, self.OnItemChoice)
     

        # Create a control to select the data
        dataCtrl = self.dataCtrl = None

        # Create a field for available data
        if self.data_type == 'string' :
            dataCtrl = wx.TextCtrl(panel, -1, data)

        if self.data_type == 'bool':
            dataCtrl = wx.Choice(parent=panel, pos=(10,10)) 
            list = [
                'True', 'False'
            ]
            dataCtrl.AppendItems(strings=list) 
            if list.count(data)==0:
                dataCtrl.Select(n=0)
            else:
                dataCtrl.SetSelection(int(list.index(data)))

        staticBox = wx.StaticBox(panel, -1, "Select Data")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(dataCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        dataCtrl.Bind(wx.EVT_CHOICE, self.OnDataChoice)


        while panel.Affirmed():
            if self.data_type == 'bool': 
               data = dataCtrl.GetStringSelection()
            else:
               data = dataCtrl.GetValue()
            panel.SetResult(
                tagCtrl.GetStringSelection(),
                itemCtrl.GetStringSelection(),
                data               
            )