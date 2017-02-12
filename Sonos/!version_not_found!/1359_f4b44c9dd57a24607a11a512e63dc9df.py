######################################## Register ############################################
eg.RegisterPlugin(
    name = "Sonos",
    author = ".",
    version = ".",
    kind = "program",
    canMultiLoad = True,
    description = "Adds actions to control Sonos",
    createMacrosOnAdd = True,    
)
###################################### Import ###############################################
import eg

###################################### Plugin Base #########################################
class Sonos(eg.PluginBase):
        
########## Config box
    def Configure(self, IP="Hello"):
        IPinput = "Insert the IP of the Sonos device you want to control."
        panel = eg.ConfigPanel()
        IPLabel = wx.StaticText(panel, -1, IPinput)
        textControl = wx.TextCtrl(panel, -1, IP, size=(200, -1))
        panel.sizer.Add(IPLabel,0,wx.TOP,15)
        panel.sizer.Add(textControl, 0, wx.TOP,1)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
########## init self
    def __init__(self):
        self.AddActionsFromList(ACTIONS
        )
########## start self       
    def __start__(self, IP=""):
        self.IP = IP
################################################ Actions ############################################
class Play(eg.ActionBase):

    def __call__(self, ActionIP):
        print "This is config from plugin setup: " + self.plugin.IP
        print "This is config from action setup: " + ActionIP

    def Configure(self, ActionIP="World"):
        IPActioninput = "Insert the IP of the Sonos device you want to control."
        panel = eg.ConfigPanel()
        IPActionLabel = wx.StaticText(panel, -1, IPActioninput)
        textControl = wx.TextCtrl(panel, -1, ActionIP, size=(200, -1))
        panel.sizer.Add(IPActionLabel,0,wx.TOP,15)
        panel.sizer.Add(textControl, 0, wx.TOP,1)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())

########################################### Auto add Actions #####################################

ACTIONS = (    
    (Play,"Play","Play","Play Sonos.", None),
)