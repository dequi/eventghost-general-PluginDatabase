version = "0.0.0"

eg.RegisterPlugin(
    name = "TestSample",
    author = "krambriw",
    version = version,
    kind = "program",
    guid = "{EDD0D4A2-0D44-46AB-9C8C-904A6B95E498}",
    description = "Testing",
)


#===============================================================================

class MyPlugin(eg.PluginClass):
    
    def __init__(self):
        pass


    def __start__(
        self,
        var1
    ):
        self.var1 = var1
        print 'var1: ', self.var1
            
            
    def __stop__(self):
        pass 


    def __close__(self):
        pass 


    def Configure(
        self,
        var1 = False
        ):
           
        panel = eg.ConfigPanel(self)

        staticBox = wx.StaticBox(panel, -1, "Variabel 1")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        var1Ctrl = wx.CheckBox(panel, -1, 'Variabel 1')
        var1Ctrl.SetValue(var1)
        sizer1.Add(var1Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
     
        while panel.Affirmed():
            var1 = var1Ctrl.GetValue()
            panel.SetResult(
                var1
            )