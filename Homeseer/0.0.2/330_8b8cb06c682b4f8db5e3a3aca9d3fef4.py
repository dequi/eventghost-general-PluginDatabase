import eg

eg.RegisterPlugin(
    name = "Homeseer",
    author = "Me. Modified 09/08/2010 by krambriw ",
    version = "0.0.2",
    kind = "other",
    description = "Homeseer plugin. More info on http://smart-living.geoblog.be/"
)

import win32com.client
HOMESEERINSTANCE = None



class Homeseer():
    hsi = win32com.client.Dispatch("HomeSeer2.application")
#    hs = win32com.client.Dispatch("Scheduler.hsapplication") # krambriw: not needed it seems???
    connected = False
    hostname = "localhost"
    username = "default"
    password = "default"


    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

		
    def connect(self):        
        print "Trying to connect to Homeseer-host " + self.hostname + " using user " + self.username + "."
        self.hsi.SetHost(self.hostname)
        rval = self.hsi.Connect(self.username, self.password)
        if rval == "":
            print "Successfully connected to Homeseer " + self.hostname + " using user " + self.username + "."
            self.connected = True
        else:
            print "Error: " + rval
            self.hsi.Disconnect
            self.connected = False

        if self.connected:
            #self.hs = self.hsi.GetHSRef
            self.hs = win32com.client.Dispatch("homeseer.application") # krambriw: Changed interface

    def disconnect(self):
        if self.connected:
            self.hsi.Disconnect
            print "Disconnected from Homeseer."
            self.connected = False

	
    def isConnected(self):
        return self.connected


    def doSpeak(self, speech):
        if self.connected:
            print "Speaking " + speech
            self.hs.Speak(speech)
        else:
            print "Not connected to Homeseer."


    def doOnOffCommand(self, deviceCode):
        if self.connected:
            if self.hs.DeviceExistsRef(deviceCode)>-1: # krambriw: Check if the device exists
                if self.hs.IsOn(deviceCode):
                    command = "Off"
                else:
                    command = "On"
    		
                print "Sending command " + command + " to " + deviceCode
                self.hs.ExecX10(deviceCode, command, 0, 0, False)
            else:
                print deviceCode + " does not exist in Homeseer configuration."			
        else:
            print "Not connected to Homeseer."



class HomeseerPlugin(eg.PluginBase):
    
    def __init__(self):
        self.AddAction(OnOffCommand)
        self.AddAction(Speak)

        
    def __start__(self, hostname, username, password):
        global HOMESEERINSTANCE
        HOMESEERINSTANCE = Homeseer(hostname, username, password)
        HOMESEERINSTANCE.connect()


    def __stop__(self):
        HOMESEERINSTANCE.disconnect()        


    def __close__(self):
        print "Homeseer plugin is now closed."

		
    def Configure(self, hostname="localhost", username="default", password="default"):
        panel = eg.ConfigPanel()
		
        hostnameTextControl = panel.TextCtrl(hostname)
        usernameTextControl = panel.TextCtrl(username)
        passwordTextControl = wx.TextCtrl(panel, -1, password, size=(175, -1), style=wx.TE_PASSWORD)

        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Homeseer Host: "))
        sizer.Add(hostnameTextControl)  
        sizer.Add(panel.StaticText("Homeseer Username: "))
        sizer.Add(usernameTextControl)
        sizer.Add(panel.StaticText("Homeseer Password: "))    # row2, col1
        sizer.Add(passwordTextControl)
        
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)
		
        while panel.Affirmed():
            panel.SetResult(
                hostnameTextControl.GetValue(),
                usernameTextControl.GetValue(),
                passwordTextControl.GetValue()
            )


			
class OnOffCommand(eg.ActionBase):
	
    def __call__(self, deviceCode):
        HOMESEERINSTANCE.doOnOffCommand(deviceCode)


    def Configure(self, devicecode=""):
        panel = eg.ConfigPanel()
		
        deviceCodeTextControl = panel.TextCtrl(devicecode)
        
        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Device Code: "))
        sizer.Add(deviceCodeTextControl)  
        
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)
		
        while panel.Affirmed():
            panel.SetResult(deviceCodeTextControl.GetValue())
		

		
class Speak(eg.ActionBase):

    def __call__(self, speech):
        HOMESEERINSTANCE.doSpeak(speech)


    def Configure(self, speech="Hello Homeseer World."):
        panel = eg.ConfigPanel()
		
        speechTextControl = panel.TextCtrl(speech)
        
        sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Speech: "))
        sizer.Add(speechTextControl)  
        
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)
		
        while panel.Affirmed():
            panel.SetResult(speechTextControl.GetValue())