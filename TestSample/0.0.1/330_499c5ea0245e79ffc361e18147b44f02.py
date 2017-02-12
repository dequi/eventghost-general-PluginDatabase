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
        self.OkButtonClicked = False
        self.ConfigChanged = True


    def __start__(
        self,
        var1
    ):
        self.var1 = var1
        if self.ConfigChanged:
            self.ConfigChanged = False
        if self.OkButtonClicked:
            pass
        if self.init:        
            self.StartThread()
            self.init = False        
        self.started = True


    def __stop__(self):
        self.started = False


    def __close__(self):
        self.started = False

            
    def StartThread(self):
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


    def SetConfig(self, prm):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        #print args
        for i in prm:
            arg = prm[i]
            args[int(i)] = arg
        trItem.SetArguments(args) #automatically __stop__ / __start__      
        eg.document.SetIsDirty()
        eg.document.Save()
        print 'Configuration changed', prm


    def PollingThread(self):
        while not self.started:
            self.finished.wait(0.5)
        print 'threadStarted'
        var1_old = self.var1
        while not self.finished.isSet():
            if self.var1 <> var1_old:
                #print 'var1_old', var1_old, self.var1
                var1_old = self.var1
                if self.OkButtonClicked:
                    self.OkButtonClicked = False
                    self.finished.wait(0.5)
                else:
                    prm = {'0':self.var1}
                    self.ConfigChanged = True
                    self.SetConfig(prm)
            self.finished.wait(0.5)
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
            self.OkButtonClicked = True

           
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            var1 = var1Ctrl.GetValue()
            panel.SetResult(
                var1
            )