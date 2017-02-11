version = "0.0.1"

eg.RegisterPlugin(
    name = "TestSample",
    author = "krambriw",
    version = version,
    kind = "program",
    guid = "{EDD0D4A2-0D44-46AB-9C8C-904A6B95E498}",
    description = "Testing how to update a plugin configuration from outside",
)

#===============================================================================
import eg
import time
from threading import Event, Thread



class MyPlugin(eg.PluginClass):
    
    def __init__(self):
        self.started = False
        self.init = True
        self.var1 = False        


    def __start__(
        self,
        var1
    ):
        self.var1 = var1
        if self.init:        
            self.startThread()
            self.init = False        


    def __stop__(self):
        pass


    def __close__(self):
        pass 

            
    def startThread(self):
        self.finished = Event()
        self.pollingThread = Thread(
            target=self.PollingThread,
            name="Polling_Thread"
        )
        if not self.finished.isSet():
            self.pollingThread.start()
            

    def StopThread(self):     
        self.finished.set()
        while self.started:
            time.sleep(0.1)
        print "Finished waiting for thread termination"


    def SetConfig(self, arg):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        args[0] = arg
        trItem.SetArguments(args) #automatically __stop__ / __start__      
        eg.document.SetIsDirty()
        eg.document.Save()
        print 'Configuration updated', 'var1: ', arg


    def PollingThread(self):
        print 'threadStarted'
        var1_old = self.var1
        self.started = True
        while not self.finished.isSet():
            if self.var1 <> var1_old:
                var1_old = self.var1
                self.SetConfig(self.var1)
            self.finished.wait(0.5)
        self.started = False
        print 'threadStopped'


    def Configure(self, var1 = False):
        panel = eg.ConfigPanel(self)
        staticBox = wx.StaticBox(panel, -1, "Variabel 1")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        var1Ctrl = wx.CheckBox(panel, -1, 'Variabel 1')
        var1Ctrl.SetValue(var1)
        sizer1.Add(var1Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
     
        def OnOkButton(event): 
            event.Skip()
            if self.started:
                self.StopThread()
                while self.started:
                    time.sleep(0.1)
            self.startThread()
           
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            var1 = var1Ctrl.GetValue()
            panel.SetResult(
                var1
            )