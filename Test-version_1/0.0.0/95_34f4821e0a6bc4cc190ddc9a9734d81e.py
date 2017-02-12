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
        txtMyValue = "My value"   # For future use ???????????????????????????????????????????????????????
        boolChoices = (
            "True",
            "False"
        )
        selItem = "Select Item"
        selTag  = "Select Tag"
        selData = "Select Data"       


    def __call__(self, tag, item, data):
        print tag
        print item
        print data
       
               
    # Get the choice from dropdown and perform some action
    def OnTagChoice(self, event = None):
        itemCtrl = self.itemCtrl
        tagCtrl = self.tagCtrl
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
        #if i_list.count(tag)==0:
        #    sel = 0
        #else:
        #    sel = int(i_list.index(tag))
        #itemCtrl.SetSelection(sel)
        itemCtrl.SetStringSelection(tag if event else self.item)
        self.OnItemChoice()
        if event:
            event.Skip()
        return tagCtrl.GetSelection()  # For future use ???????????????????????????????????????????????????????


    def OnItemChoice(self, event = None):
        itemCtrl = self.itemCtrl
        data = self.data
        item = itemCtrl.GetStringSelection()
        panel = itemCtrl.GetParent()
        staticBoxSizer = panel.sizer.GetItem(2).GetSizer()
        if len(staticBoxSizer.GetChildren()):
            dynamicSizer = staticBoxSizer.GetItem(0).GetSizer()
            dynamicSizer.Clear(True)
            staticBoxSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()

        if item in itemCtrl.GetStrings():
            itemCtrl.SetStringSelection(item)
            if item in ('a', 'b', 'c', 'd'):
                dataCtrl = wx.Choice(parent=panel, pos=(10,10))
                list = self.text.boolChoices
                dataCtrl.AppendItems(strings=list) 
                #if list.count(data)==0:
                #    dataCtrl.Select(n=0)
                #else:
                #    dataCtrl.SetSelection(int(list.index(data)))
                choices = dataCtrl.GetStrings()
                data = data if data in choices else choices[0]
                dataCtrl.SetStringSelection(data)
            elif item in ('e', 'f', 'g'):
                dataCtrl = wx.TextCtrl(panel, -1, "")
                if not event:
                    dataCtrl.ChangeValue(data)
        self.dataCtrl = dataCtrl
        dynamicSizer = wx.BoxSizer(wx.HORIZONTAL)
        dynamicSizer.Add(dataCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(dynamicSizer, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Layout()
        if event:
            event.Skip()
        #dataCtrl.Bind(wx.EVT_CHOICE, self.OnDataChoice)
        #return choice


    #def OnDataChoice(self, event):  # For future use ???
    #    choice = event.GetSelection()
    #    event.Skip()
    #    return choice


    def Configure(
        self,
        tag = "",
        item = "",
        data = ""
        ):
           
        panel = eg.ConfigPanel(self)
        self.item = item
        self.data = data

        # Create a dropdown to select tag
        tagCtrl = self.tagCtrl = wx.Choice(parent=panel, pos=(10,10))
        t_list = ['a','b','c','d']
        tagCtrl.AppendItems(strings=t_list)
        #if t_list.count(tag)==0:
        #    tagCtrl.Select(n=0)
        #else:
        #    tagCtrl.SetSelection(int(t_list.index(tag)))
        tagCtrl.SetStringSelection(tag if tag in t_list else t_list[0])
        staticBox = wx.StaticBox(panel, -1, self.text.selTag)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(tagCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        tagCtrl.Bind(wx.EVT_CHOICE, self.OnTagChoice)

        # Create a dropdown to select item
        itemCtrl = self.itemCtrl = wx.Choice(parent=panel, pos=(10,10))
        staticBox = wx.StaticBox(panel, -1, self.text.selItem)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(itemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        itemCtrl.Bind(wx.EVT_CHOICE, self.OnItemChoice)

        # Create a field for available data
        staticBox = wx.StaticBox(panel, -1, self.text.selData)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        self.OnTagChoice()

        while panel.Affirmed():
            dataCtrl = self.dataCtrl
            item = itemCtrl.GetStringSelection()
            if item in ('a', 'b', 'c', 'd'):
                data = dataCtrl.GetStringSelection()
            elif item in ('e', 'f', 'g'):
                data = dataCtrl.GetValue()
            panel.SetResult(
                tagCtrl.GetStringSelection(),
                item,
                data               
            )