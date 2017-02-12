import eg

eg.RegisterPlugin(
    name="Test Variable",
    description = "Test variable/procedure access",
    guid = "{0FC35A7F-F0DD-440D-8E24-F747D2CF7377}",
    createMacrosOnAdd = True,
    version = 0.0,
    author = "TEST",
    )



class TestVariable(eg.PluginBase):

    def __init__(self):
        self.strVariable = ''
        self.AddAction(GetHelloWorld)
        self.AddAction(SetHelloWorld)
   
    def __start__(self):
        print "Test variable: Started"

    def myProcedure(self):
        print self.strVariable

    def __stop__(self):
        print "Test variable: Stopped"
       
    def __close__(self):
        print "Test variable: Closed"



class GetHelloWorld(eg.ActionBase):

    def __call__(self):
        return self.plugin.strVariable


class SetHelloWorld(eg.ActionBase):

    def __call__(self, strVariable = ''):
        self.plugin.strVariable = strVariable

    def Configure(self, strVariable = ''):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, strVariable)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())        