
eg.RegisterPlugin(
    name = "Dummy",
    author = "Walter Kraembring",
    version = "1.0",
    description = (
        "Just a dummy framework"
    ),
    url = "http://www.eventghost.org/forum",
)

from threading import Thread, Event
import time


class Text:
   
    stopped = "Plugin stopped"
    schedulerFinished = "Scheduler finished"
    listhl = "Currently active Schedulers:"
    colLabels = (
            "Scheduler Name",
            "Label 1",
            "Label 2"
            )


    class SchedulerAction:
        name = "Start new or control running scheduler"
        description = "Allows starting, stopping or resetting dummy schedulers"
        schedulerName = "Scheduler name:"
        labelStart = ' "%s"'


class SchedulerThread(Thread):
    def __init__(self,
        name,
        variable
    ):

        # Thread.__init__(self, name = name)
        Thread.__init__(self, name="SchedulerThread")
        self.name = name
        self.t_variable = variable
        self.finished = Event()
        self.abort = False
        self.restart = False
   
    def run(self):
        while (self.abort == False):
            self.finished.wait(5)
            self.finished.clear()
            if self.abort:
                break
            eg.TriggerEvent(str(self.t_variable))
            self.t_variable += 1
            self.variable = self.t_variable
        
    def AbortScheduler(self):
        self.abort = True
        self.finished.set()
       
  

class Scheduler(eg.PluginClass):
    text = Text
    started = False
    
    def __init__(self):
        self.AddAction(SchedulerAction)
        self.AddAction(GetContentsOfVariable)
        self.schedulerNames = []
        self.lastSchedulerName = ""
        self.schedulerThreads = {}
        self.variable = 0


    def __start__(self):
        self.started = True


    def __stop__(self):
        self.started = False
        self.AbortAllSchedulers()


    def __close__(self):
        self.AbortAllSchedulers()


    #methods to Control schedulers
    def StartScheduler(self,
        schedulerName,
        variable
    ):

        if self.schedulerThreads.has_key(schedulerName):
            t = self.schedulerThreads[schedulerName]
            if t.isAlive():
                t.AbortScheduler()
            del self.schedulerThreads[schedulerName]
        t = SchedulerThread(
            schedulerName,
            variable
            )
        self.schedulerThreads[schedulerName] = t
        t.start()


    def AbortScheduler(self, scheduler):
        if self.schedulerThreads.has_key(scheduler):
            t = self.schedulerThreads[scheduler]
            t.AbortScheduler()
            del self.schedulerThreads[scheduler]


    def AbortAllSchedulers(self):
        for i, item in enumerate(self.schedulerThreads):
            t = self.schedulerThreads[item]
            t.AbortScheduler()
            del t
        self.schedulerThreads = {}


    def Configure(self, *args):
        panel = eg.ConfigPanel(self)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
       
        schedulerListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
       
        for i, colLabel in enumerate(self.text.colLabels):
            schedulerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        #insert date to get Size
        schedulerListCtrl.InsertStringItem(0, "Test EventName")
        schedulerListCtrl.SetStringItem(0, 1, time.strftime("%c"))

        size = 0
        for i in range(2):
            schedulerListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER) #wx.LIST_AUTOSIZE
            size += schedulerListCtrl.GetColumnWidth(i)
       
        schedulerListCtrl.SetMinSize((size, -1))
       
        mySizer.Add(schedulerListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, "Abort")
        mySizer.Add(abortButton, (1,0))
       
        abortAllButton = wx.Button(panel, -1, "Abort all")
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
       
        refreshButton = wx.Button(panel, -1, "Refresh")
        mySizer.Add(refreshButton, (1,4), flag = wx.ALIGN_RIGHT)
       
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
       
        def PopulateList (event):
            schedulerListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.schedulerThreads):
                t = self.schedulerThreads[item]
                if t.isAlive():
                    schedulerListCtrl.InsertStringItem(row, t.name)
                    schedulerListCtrl.SetStringItem(row,
                        1, "Info 1")
                    schedulerListCtrl.SetStringItem(row,
                        2, "Info 2")
                    row += 1
            ListSelection(wx.CommandEvent())

        def OnAbortButton(event):
            item = schedulerListCtrl.GetFirstSelected()
            while item != -1:
                name = schedulerListCtrl.GetItemText(item)
                self.AbortScheduler(name)
                item = schedulerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnAbortAllButton(event):
            self.AbortAllSchedulers()
            PopulateList(wx.CommandEvent())
            event.Skip()

        def ListSelection(event):
            flag = schedulerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()
           
        def OnSize(event):
            schedulerListCtrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER) #wx.LIST_AUTOSIZE
            event.Skip()

        PopulateList(wx.CommandEvent())

       
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        schedulerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        schedulerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)

        while panel.Affirmed():
            panel.SetResult(*args)

    #function to fill the scheduler name Combobox
    def GetSchedulerNames(self):
        self.schedulerNames.sort(lambda a,b: cmp(a.lower(), b.lower()) )
        return self.schedulerNames

    #function to collect scheduler names for Combobox
    def AddSchedulerName(self, schedulerName):
        if not schedulerName in self.schedulerNames:
            self.schedulerNames.append(schedulerName)



class SchedulerAction(eg.ActionClass):

    def __call__(self,
            schedulerName,
            variable
            ):

        if not self.plugin.started:
            self.PrintError(self.plugin.text.stopped)
            return False

        self.plugin.StartScheduler(
                schedulerName,
                variable
                )


    def GetLabel(self,
            schedulerName,
            variable
            ):
        self.plugin.AddSchedulerName(schedulerName)
        return self.text.labelStart % (schedulerName)


    def Configure(self,
        schedulerName = "",
        variable = 0
    ):
        text = self.text
        plugin = self.plugin
        panel = eg.ConfigPanel(self)

        #name
        schedulerNameCtrl = wx.TextCtrl(panel, -1, schedulerName)
        panel.AddLine("Scheduler name:", schedulerNameCtrl)
      
        #variable
        variableCtrl = panel.SpinIntCtrl(variable, 0, 5)
        variableCtrl.SetInitialSize((50,-1))
        panel.AddLine("Variable:", variableCtrl)


        while panel.Affirmed():
            schedulerName = schedulerNameCtrl.GetValue()
            plugin.lastSchedulerName = schedulerName
            plugin.AddSchedulerName(schedulerName)
            variable = variableCtrl.GetValue()
    
            panel.SetResult(
                schedulerName,
                variable
             )
             

class GetContentsOfVariable( eg.ActionClass ) :

    def __call__( self ) :
        print self.plugin.variable
        return self.plugin.variable