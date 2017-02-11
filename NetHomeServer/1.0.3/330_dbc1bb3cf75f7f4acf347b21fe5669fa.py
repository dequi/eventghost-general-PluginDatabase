#
# plugins/NetHomeServer/__init__.py
#
# Copyright (C) 2009
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2010-01-05  Added support for UPM Wind and Rain gauges
# 2010-01-04  Added action to send pronto code to NetHomeServer
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-05  First published version
# 2009-11-19  Improved control of received data 
# 2009-10-27  Small modification of the logging function
# 2009-10-17  The first alpha version
##############################################################################

eg.RegisterPlugin(
    name = "NetHomeServer",
    guid = '{7B2DF95B-DC3E-4D56-9785-0E13365C568F}',
    author = "Walter Kraembring",
    version = "1.0.3",
    canMultiLoad = False,
    kind = "other",
    url = "http://wiki.nethome.nu/doku.php/start",
    description = (
        '<p>Plugin to receive messages from NetHomeServer</p>'
        '\n\n<p><a href="http://wiki.nethome.nu/doku.php/start">Product details...</a></p>'
        '<center><img src="nethomeserver.png" /></center>'
    ),
)

import telnetlib, socket, time, os, sys, winsound, re, math
from threading import Event, Thread



class Text:
    started = "Plugin started"
    listhl = "Currently active threads:"
    hostName = "Host name or ip:"
    portNumber = "Port number:"
    windSpeed = "Check if windspeed shall be presented in m/s:"
    colLabels = (
        "Action Name",
        "    ",
        "    "
    )
    subscribe = "Request to Subscribe: "
    connection_etablished = "Connection established: "
    connection_error = "Connection error: "
    unsubscribe = "Request to Unsubscribe: "
    read_error = "Read error: "
    
    #Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_restartAll = "Restart All"
    b_refresh = "Refresh"

    #Threads
    n_loggerThread = "loggerThread"
    thr_abort = "Thread is terminating: "
    
    class loggerAction:
        name = "Start new or control a running logger"
        description = (
            "Allows starting, stopping or resetting loggers, which "+
            "monitors events from NetHomeServer"
        )
        loggerName = "Logger name:"
        soundOnEvent = "Beep on events:"
        repeats = "Allow repeated events:"
        delay = "Delay of repeats:"
        delay_u = " s (seconds)"
        labelStart = ' "%s"'
        logToFile = "Log events to file:"
        debug = "Turn debug ON:"
        txtBattLow = "Battery low"

    class prontoCmd:
        deviceName = (
            "This is a device that can be controlled via NetHomeServer "+
            "using pronto codes"
        )
        pronto = "Paste the pronto code to be transmitted for this action"


   
class loggerThread(Thread):
    text = Text

    def __init__(
        self,
        name,
        hostName,
        portNbr,
        bSound,
        bRepeats,
        delayRepeat,
        bLogToFile,
        bDebug,
        bSpeed_ms,
        plugin
    ):
        Thread.__init__(self, name=self.text.n_loggerThread)
        self.name = name
        self.hostName = hostName
        self.portNbr = portNbr
        self.bSound = bSound
        self.bRepeats = bRepeats
        self.delayRepeat = delayRepeat
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.bSpeed_ms = bSpeed_ms
        self.finished = Event()
        self.abort = False
        self.bTaskAdded = False
        self.plugin = plugin
        self.wDirection = [
            'N',
            'NNE',
            'NE',
            'ENE',
            'E',
            'ESE',
            'SE',
            'SSE',
            'S',
            'SSW',
            'SW',
            'WSW',
            'W',
            'WNW',
            'NW',
            'NNW'
        ]

   
    def run(self):
        event_Old = []
       
        while (self.abort == False):
            self.finished.wait(0.2)
            self.finished.clear()

            if self.abort:
                self.finished.wait(1)
                break

            lst = []
            
            if eg.event:
                lst = self.plugin.event_NHS.split(',')

            if (
                len(lst) > 9
                and lst.count("NetHomeServer") > 0
                and (not self.bTaskAdded
                or event_Old != lst)
            ):
                event_Old = lst

                if len(lst) > 9:
                    s_lst = ""
                    for X in range (4,len(lst)):
                        s_lst += str(lst[X])

                        if X < len(lst):
                            s_lst += "|"
                    
                    if lst.count("UPM_Message") == 0:
                        eg.TriggerEvent(self.name+"|"+s_lst)
                        
                    else:
                        # split up the event components
                        UPMsplit = s_lst.split('|')
                    
                        if (
                            len(UPMsplit[1]) > 0
                            and len(UPMsplit[2]) > 0
                            and len(UPMsplit[3]) > 0
                            and len(UPMsplit[4]) > 0
                            and len(UPMsplit[5]) > 0
                            and len(UPMsplit[6]) > 0
                            and len(UPMsplit[7]) > 0
                            and len(UPMsplit[8]) > 0
                            and len(UPMsplit[9]) > 0
                            and len(UPMsplit[10]) > 0
                            and UPMsplit[10] != " "
                        ):
                            upmHumidity = int(UPMsplit[6])
                            upmBattery = UPMsplit[8]
                            upmTemperature = float(UPMsplit[10])
                            upmDevice = UPMsplit[2]
                            upmHouse = UPMsplit[4]
 
                            # Calculate values from the sensor readings
                            if int(upmHouse) != 10:
                                upmHumidity = upmHumidity / 2
                                upmTemperature = (
                                    (upmTemperature * 0.0625) - 50.0
                                )
                                s_lst = (
                                    self.name+"|"+
                                    str(UPMsplit[3])+"|"+
                                    str(upmHouse)+"|"+
                                    str(UPMsplit[1])+"|"+
                                    str(upmDevice)+"|"+
                                    str(UPMsplit[7])+"|"+
                                    str(upmBattery)+"|"
                                )
                                    
                                p_lod = (    
                                    str(UPMsplit[5])+"|"+
                                    str(upmHumidity)+"|"+
                                    str(UPMsplit[9])+"|"+
                                    str(upmTemperature)+"|"
                                 )

                            else:
                                # House/Device codes 10/2 are reserved
                                # for wind gauges
                                if int(upmDevice) == 2:
                                    if int(upmHumidity) <= 15:
                                        wdLabel = (
                                            self.wDirection[int(upmHumidity)]
                                        )
                                        upmHumidity = wdLabel
                                    else:
                                        print (
                                            "Wind direction out of range:",
                                            upmHumidity
                                        )
                                        upmHumidity = "Out of range"
                                    
                                    if self.plugin.bSpeed_ms:
                                        upmTemperature = (
                                            (upmTemperature*1000)/3600
                                        )
                                    s_lst = (
                                        self.name+"|"+
                                        str(UPMsplit[3])+"|"+
                                        str(upmHouse)+"|"+
                                        str(UPMsplit[1])+"|"+
                                        str(upmDevice)+"|"+
                                        str(UPMsplit[7])+"|"+
                                        str(upmBattery)+"|"
                                    )
                                        
                                    p_lod = (    
                                        "UPM.WindDirection|"+
                                        str(upmHumidity)+"|"+
                                        "UPM.WindSpeed|"+
                                        str(upmTemperature)+"|"
                                     )
                                # House/Device codes 10/3 are reserved
                                # for rain gauges
                                if int(upmDevice) == 3:
                                    upmTemperature = upmTemperature * 0.7
                                    s_lst = (
                                        self.name+"|"+
                                        str(UPMsplit[3])+"|"+
                                        str(upmHouse)+"|"+
                                        str(UPMsplit[1])+"|"+
                                        str(upmDevice)+"|"+
                                        str(UPMsplit[7])+"|"+
                                        str(upmBattery)+"|"
                                    )
                                        
                                    p_lod = (    
                                        "UPM.Rain|"+
                                        str(upmHumidity)+"|"+
                                        "UPM.Level|"+
                                        str(upmTemperature)+"|"
                                     )

                            eg.TriggerEvent(s_lst, p_lod)

                            if upmBattery == 1:
                                # Create the eg battery low event
                                eg.TriggerEvent(
                                    s_lst+"|"
                                    +self.text.loggerAction.txtBattLow
                                )
                                    
                                if self.bLogToFile:
                                    logStr = (
                                        s_lst+"|"
                                        +self.text.loggerAction.txtBattLow
                                    )
                                    self.LogToFile(logStr)

                    if self.bLogToFile:
                        if lst.count("UPM_Message") == 0:
                            self.LogToFile(s_lst)
                        else:
                            self.LogToFile(s_lst+p_lod)

                    if self.bDebug:
                        self.debugLogToFile(
                            self.name
                            +"|"
                            +str(lst)
                        )

                    if self.bSound:                        
                        winsound.Beep(1000, 200)                

                    if self.bRepeats:

                        if not self.bTaskAdded:
                            eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.ClearBuffer
                            )
                            self.bTaskAdded = True


    def ClearBuffer(self):
        self.plugin.event_NHS = "NIL"
        self.bTaskAdded = False
        #print self.plugin.event_NHS, self.bTaskAdded


    def Abortlogger(self):
        time.sleep(1.0)
        print self.text.thr_abort, self.text.n_loggerThread
        self.abort = True
        self.finished.set()

       
    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]

        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if (
                not os.path.exists(progData+"/EventGhost/Log")
                and not os.path.isdir(progData+"/EventGhost/Log")
            ):
                os.makedirs(progData+"/EventGhost/Log")
            fileHandle = open (
                progData+'/EventGhost/Log/'+fileDate+'Logger_'+
                self.name+'.html', 'a'
            )
            fileHandle.write ( logStr )
            fileHandle.close ()
            
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
            fileHandle = open ( 'Log/'+fileDate+'Logger_'+self.name+'.html', 'a' )
            fileHandle.write ( logStr )
            fileHandle.close ()


    def debugLogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]

        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if (
                not os.path.exists(progData+"/EventGhost/Log")
                and not os.path.isdir(progData+"/EventGhost/Log")
            ):
                os.makedirs(progData+"/EventGhost/Log")
            fileHandle = open (
                progData+'/EventGhost/Log/'+fileDate+'Logger_debug'+
                self.name+'.html', 'a'
            )
            fileHandle.write ( logStr )
            fileHandle.close ()
            
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
            fileHandle = open ( 'Log/'+fileDate+'Logger_debug'+self.name+'.html', 'a' )
            fileHandle.write ( logStr )
            fileHandle.close ()
               


class NetHome(eg.PluginClass):
    text = Text
        
    def __init__(self):
        self.AddAction(loggerAction)
        self.AddAction(prontoCmd)
        self.AllloggerNames = []
        self.AllSound = []
        self.AllRepeats = []
        self.AllRepeatDelay = []
        self.AllLogToFile = []
        self.AllDebug = []
        self.lastloggerName = ""
        self.loggerThreads = {}
        self.counters = {}
        self.OkButtonClicked = False
        self.started = False


    def __start__(
        self,
        hostName,
        portNbr,
        bSpeed_ms
    ):
        print self.text.started
        self.hostName = hostName
        self.portNbr = portNbr
        self.bSpeed_ms = bSpeed_ms
        self.started = True
        self.event_NHS = ""
        
        if self.OkButtonClicked:
            self.OkButtonClicked = False
            self.RestartAllLoggers()

        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if (
                not os.path.exists(progData+"/EventGhost/Log")
                and not os.path.isdir(progData+"/EventGhost/Log")
            ):
                os.makedirs(progData+"/EventGhost/Log")
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')

        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()
        self.AbortAllLoggers()
        self.started = False


    def __close__(self):
        self.mainThreadEvent.set()
        self.AbortAllLoggers()
        self.started = False


    def main(self,mainThreadEvent):
        connectionError = True
        try:
            self.tn = telnetlib.Telnet(self.hostName, self.portNbr)
            self.tn.write("subscribe\r")
            rsp = self.tn.read_until("\n", 0.9)
            print self.text.subscribe, rsp

            if rsp.find("ok") != -1:
                print self.text.connection_etablished, self.tn
                connectionError = False

        except socket.error, e:
            print self.text.connection_error, e
            connectionError = True
            time.sleep(5.0)
            self.main(mainThreadEvent)

        while not mainThreadEvent.isSet():
            time.sleep(0.2)
            try:
                tst = self.tn.read_until("\n", 1.0)

            except EOFError:
                print self.text.read_error, EOFError
                connectionError = True

            tst = tst.strip('\n\r')

            if len(tst) > 9:
                self.event_NHS = "NetHomeServer"+","+tst

            if connectionError:
                time.sleep(5.0)
                self.main(mainThreadEvent)

        time.sleep(1.0)
        print self.text.unsubscribe+"Main-"+self.text.thr_abort
        self.tn.write("quit\r")
        self.tn.close()


    #methods to Control loggers
    def Startlogger(
        self,
        loggerName,
        hostName,
        portNbr,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        if self.loggerThreads.has_key(loggerName):
            t = self.loggerThreads[loggerName]
            if t.isAlive():
                t.Abortlogger()
            del self.loggerThreads[loggerName]
        t = loggerThread(
            loggerName,
            self.hostName,
            self.portNbr,
            bSound,
            bRepeats,
            repeatDelay,
            bLogToFile,
            bDebug,
            self.bSpeed_ms,
            self
        )
        self.loggerThreads[loggerName] = t
        t.start()


    def Abortlogger(self, logger):
        print logger
        if self.loggerThreads.has_key(logger):
            t = self.loggerThreads[logger]
            t.Abortlogger()
            del self.loggerThreads[logger]


    def AbortAllLoggers(self):
        for i, item in enumerate(self.loggerThreads):
            t = self.loggerThreads[item]
            t.Abortlogger()
            del t
        self.loggerThreads = {}


    def RestartAllLoggers(self, startNewIfNotAlive = True):
        for i, item in enumerate(self.GetAllLoggerNames()):
            if startNewIfNotAlive:
                self.Startlogger(
                    self.GetAllLoggerNames()[i],
                    self.hostName,
                    self.portNbr,
                    self.GetAllSound()[i],
                    self.GetAllRepeats()[i],
                    self.GetAllRepeatDelay()[i],
                    self.GetAllLogToFile()[i],
                    self.GetAllDebug()[i],
                    self.bSpeed_ms
                )


    def Configure(
        self,
        hostName = "192.168.10.254",
        portNbr = 8005,
        bSpeed_ms = True,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
       
        netHomeServerListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )
       
        for i, colLabel in enumerate(self.text.colLabels):
            netHomeServerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        netHomeServerListCtrl.InsertStringItem(0, "Test NetHome Name                     ")
        netHomeServerListCtrl.SetStringItem(0, 1, "  ")
        netHomeServerListCtrl.SetStringItem(0, 2, "  ")

        size = 0
        for i in range(3):
            netHomeServerListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            ) #wx.LIST_AUTOSIZE
            size += netHomeServerListCtrl.GetColumnWidth(i)
       
        netHomeServerListCtrl.SetMinSize((size, -1))
        
        mySizer.Add(netHomeServerListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        hostNameCtrl = wx.TextCtrl(panel, -1, hostName)
        hostNameCtrl.SetInitialSize((250,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.hostName), (1,0))
        mySizer.Add(hostNameCtrl, (1,1))
    
        portCtrl = panel.SpinIntCtrl(portNbr, 0, 9000)
        portCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNumber), (2,0))
        mySizer.Add(portCtrl, (2,1))

        speedCtrl = panel.CheckBox(bSpeed_ms, "")
        speedCtrl.SetValue(bSpeed_ms)
        mySizer.Add(wx.StaticText(panel, -1, self.text.windSpeed), (3,0))
        mySizer.Add(speedCtrl, (3,1))

        #buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer.Add(abortButton, (4,0))
       
        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer.Add(abortAllButton, (4,1), flag = wx.ALIGN_RIGHT)
       
        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer.Add(restartAllButton, (4,2), flag = wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer.Add(refreshButton, (4,4), flag = wx.ALIGN_RIGHT)
       
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

       
        def PopulateList (event):
            netHomeServerListCtrl.DeleteAllItems()
            row = 0
            for j, item in enumerate(self.loggerThreads):
                t = self.loggerThreads[item]
                if t.isAlive():
                    netHomeServerListCtrl.InsertStringItem(row, t.name)
                    row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = netHomeServerListCtrl.GetFirstSelected()
            while item != -1:
                name = netHomeServerListCtrl.GetItemText(item)
                self.Abortlogger(name)
                item = netHomeServerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.AbortAllLoggers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = netHomeServerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()

           
        def OnSize(event):
            netHomeServerListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            ) #wx.LIST_AUTOSIZE
            event.Skip()


        def OnApplyButton(event): 
            event.Skip()
            self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event): 
            event.Skip()
            self.OkButtonClicked = True
#            if not self.started:    
#                self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())
        
        PopulateList(wx.CommandEvent())
       
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        netHomeServerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        netHomeServerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            hostName = hostNameCtrl.GetValue()
            portNbr = portCtrl.GetValue()
            bSpeed_ms = speedCtrl.GetValue()

            panel.SetResult(
                        hostName,
                        portNbr,
                        bSpeed_ms,
                        *args
            )


    def GetAllLoggerNames(self):
        return self.AllloggerNames


    def GetAllSound(self):
        return self.AllSound


    def GetAllRepeats(self):
        return self.AllRepeats


    def GetAllRepeatDelay(self):
        return self.AllRepeatDelay


    def GetAllLogToFile(self):
        return self.AllLogToFile


    def GetAllDebug(self):
        return self.AllDebug


    def AddloggerName(self, loggerName):
        if not loggerName in self.AllloggerNames:
            self.AllloggerNames.append(loggerName)
        return self.AllloggerNames.index(loggerName)


    def AddSound(self, bSound, indx):
        try:
            del self.AllSound[indx]
        except IndexError:
            i = -1 # no match
        self.AllSound.insert(indx, bSound)


    def AddDebug(self, bDebug, indx):
        try:
            del self.AllDebug[indx]
        except IndexError:
            i = -1 # no match
        self.AllDebug.insert(indx, bDebug)


    def AddLogToFile(self, bLogToFile, indx):
        try:
            del self.AllLogToFile[indx]
        except IndexError:
            i = -1 # no match
        self.AllLogToFile.insert(indx, bLogToFile)


    def AddRepeats(self, bRepeats, indx):
        try:
            del self.AllRepeats[indx]
        except IndexError:
            i = -1 # no match
        self.AllRepeats.insert(indx, bRepeats)


    def AddRepeatDelay(self, repeatDelay, indx):
        try:
            del self.AllRepeatDelay[indx]
        except IndexError:
            i = -1 # no match
        self.AllRepeatDelay.insert(indx, repeatDelay)


             
class loggerAction(eg.ActionClass):
    text = Text.loggerAction
    
    def __call__(
        self,
        loggerName,
        hostName,
        portNbr,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        self.plugin.Startlogger(
            loggerName,
            hostName,
            portNbr,
            bSound,
            bRepeats,
            repeatDelay,
            bLogToFile,
            bDebug,
            bSpeed_ms
        )


    def GetLabel(
        self,
        loggerName,
        hostName,
        portNbr,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        indx = self.plugin.AddloggerName(loggerName)
        self.plugin.AddSound(bSound, indx)
        self.plugin.AddRepeatDelay(repeatDelay, indx)
        self.plugin.AddRepeats(bRepeats, indx)
        self.plugin.AddLogToFile(bLogToFile, indx)
        self.plugin.AddDebug(bDebug, indx)
        
        return self.text.labelStart % (loggerName)


    def Configure(
        self,
        loggerName = "Give this logger a name",
        hostName = "name",
        portNbr = 0,
        bSound = False,
        bRepeats = True,
        repeatDelay = 5.0,
        bLogToFile = True,
        bDebug = False,
        bSpeed_ms = True
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(10, 10)

        #name
        loggerNameCtrl = wx.TextCtrl(panel, -1, loggerName)
        loggerNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.loggerName), (0,0))
        mySizer_1.Add(loggerNameCtrl, (0,1))

        bRepeatsCtrl = wx.CheckBox(panel, -1, "")
        bRepeatsCtrl.SetValue(bRepeats)
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.repeats), (1,0))
        mySizer_1.Add(bRepeatsCtrl, (1,1))

        repeatDelayCtrl = panel.SpinNumCtrl(
            repeatDelay,
            decimalChar = '.', # by default, use '.' for decimal point
            groupChar = ',',   # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 999.9,
            increment = 0.5
        )
        repeatDelayCtrl.SetInitialSize((60,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.delay), (2,1))
        mySizer_2.Add(repeatDelayCtrl, (2,2))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.delay_u), (2,3))

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.logToFile), (3,0))
        mySizer_3.Add(bLogToFileCtrl, (3,1))

        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(bSound)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.soundOnEvent), (4,0))
        mySizer_3.Add(bSoundCtrl, (4,1))

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.debug), (5,0))
        mySizer_3.Add(bDebugCtrl, (5,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)


        def OnButton(event): 
            # re-assign the OK button
            event.Skip()
            
            loggerName = loggerNameCtrl.GetValue()
            plugin.lastloggerName = loggerName
            indx = plugin.AddloggerName(loggerName)
            hostName = self.plugin.hostName
            portNbr = self.plugin.portNbr
            bSound = bSoundCtrl.GetValue()
            plugin.AddSound(bSound, indx)
            bRepeats = bRepeatsCtrl.GetValue()
            plugin.AddRepeats(bRepeats, indx)
            repeatDelay = repeatDelayCtrl.GetValue()
            plugin.AddRepeatDelay(repeatDelay, indx)
            bLogToFile = bLogToFileCtrl.GetValue()
            plugin.AddLogToFile(bLogToFile, indx)
            bDebug = bDebugCtrl.GetValue()
            plugin.AddDebug(bDebug, indx)
            bSpeed_ms = self.plugin.bSpeed_ms

            self.plugin.RestartAllLoggers()

        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            loggerName = loggerNameCtrl.GetValue()
            plugin.lastloggerName = loggerName
            indx = plugin.AddloggerName(loggerName)
            hostName = self.plugin.hostName
            portNbr = self.plugin.portNbr
            bSound = bSoundCtrl.GetValue()
            plugin.AddSound(bSound, indx)
            bRepeats = bRepeatsCtrl.GetValue()
            plugin.AddRepeats(bRepeats, indx)
            repeatDelay = repeatDelayCtrl.GetValue()
            plugin.AddRepeatDelay(repeatDelay, indx)
            bLogToFile = bLogToFileCtrl.GetValue()
            plugin.AddLogToFile(bLogToFile, indx)
            bDebug = bDebugCtrl.GetValue()
            plugin.AddDebug(bDebug, indx)
            bSpeed_ms = self.plugin.bSpeed_ms
            
            panel.SetResult(
                loggerName,
                hostName,
                portNbr,
                bSound,
                bRepeats,
                repeatDelay,
                bLogToFile,
                bDebug,
                bSpeed_ms
            )



class prontoCmd(eg.ActionClass):
    text = Text.prontoCmd
    
    def __call__(
        self,
        deviceName,
        pronto
    ):
    	header = "event,Pronto_Message,Direction,Out,Pronto.Message,"
        connectionError = True
        try:
            self.tn = telnetlib.Telnet(self.plugin.hostName, self.plugin.portNbr)
            self.tn.write("dir\r")
            rsp = self.tn.read_until("\n", 0.1)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            print self.plugin.text.connection_error, e
            connectionError = True
            
        s = header+str(pronto)+"\r"
        time.sleep(0.1)
        self.tn.write(s)
        time.sleep(0.1)
        self.tn.write("quit\r")
        self.tn.close()


    def Configure(
        self,
        deviceName = "Give the device a name",
        pronto = (
            "0000 0073 0000 0019 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a "+
            "000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 002a 000e "+
            "000e 002a 002a 000e 000e 002a 002a 000e 000e 0199"
        )
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        #name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.deviceName), (0,0))
        mySizer_1.Add(deviceNameCtrl, (1,0))

        #pronto
        prontoCtrl = wx.TextCtrl(panel, -1, pronto, style=wx.TE_MULTILINE)
        prontoCtrl.SetInitialSize((400,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.pronto), (1,0))
        mySizer_2.Add(prontoCtrl, (2,0))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            pronto = prontoCtrl.GetValue()
            panel.SetResult(
                deviceName,
                pronto
            )

