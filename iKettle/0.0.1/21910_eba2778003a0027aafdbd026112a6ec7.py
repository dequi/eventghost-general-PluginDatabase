import eg
import socket
from threading import Event, Thread

eg.RegisterPlugin(
    name = "iKettle",
    author = "K-RAD",
    version = "0.0.1",
    kind = "other",
    description = "This is an EventGhost plugin for the Smarter WiFi Kettle (iKettle)."
)

class iKettle(eg.PluginBase):

    def __init__(self):
        self.kettleconnected = 0
        
        self.AddAction(Connect)
        group1 = self.AddGroup(
            "Buttons",
            "iKettle Buttons"
        )
        group1.AddAction(TurnOn)
        group1.AddAction(TurnOff)
        group1.AddAction(Boil100)
        group1.AddAction(Boil95)
        group1.AddAction(Boil80)
        group1.AddAction(Boil65)
        group1.AddAction(Warm)
        group1.AddAction(SetWarm20)
        group1.AddAction(SetWarm10)
        group1.AddAction(SetWarm5)
        
    def Configure(self, bridge=""):
        panel = eg.ConfigPanel()
        helpString = "Configure to connect to your iKettle."
        helpLabel=panel.StaticText(helpString)
        
        bridgeHostEdit=panel.TextCtrl(bridge)
        
        panel.AddLine(helpLabel)
        panel.AddLine("iKettle IP address : ",bridgeHostEdit)
       
        while panel.Affirmed():
            panel.SetResult(bridgeHostEdit.GetValue())
            
    def __start__(self, bridge):
        print "iKettle Plugin started. Connecting to: " + bridge
        self.bridge = bridge
        
        self.kettleconnect()
        
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.catchEvents,
            args=(self.stopThreadEvent, )
        )
        thread.start()
            
    def kettleconnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.bridge,2000))
            self.sock.send("HELLOKETTLE\n")
        except:
            print "Failed to connect to iKettle. Check the IP address."
            
    def kettlesend(self, data):
        self.sock.send(data+"\n")
        
            
    def catchEvents(self, stopThreadEvent):
        
        while not stopThreadEvent.isSet():
            
            line = self.sock.recv(4096)
            if not len(line):  # "Connection closed."
                self.kettleconnect()
                return False
            else:
                for myline in line.splitlines():
#                     print "got a line: " + myline
                    if (myline.startswith("HELLOAPP")):
                        self.kettleconnected = 1
                        print "Connected."
                        self.sock.send("get sys status\n")
                    if (myline.startswith("sys status key=")):
                        if (len(myline)<16):
                            key = 0
                        else:
                            key = ord(myline[15]) & 0x3f
                        self.setbutton(self.b100,key&0x20)
                        self.setbutton(self.b95,key&0x10)
                        self.setbutton(self.b80,key&0x8)
                        self.setbutton(self.b65,key&0x4)
                        self.setbutton(self.bwarm,key&0x2)
                        self.bboil.handler_block_by_func(self.clickboil)
                        self.bboil.set_active(key&0x1)
                        self.bboil.handler_unblock_by_func(self.clickboil)
                    if (myline == "sys status 0x100"):
                        self.TriggerEvent("iKettle.Boil100")
                    elif (myline == "sys status 0x95"):
                        self.TriggerEvent("iKettle.Boil95")
                    elif (myline == "sys status 0x80"):
                        self.TriggerEvent("iKettle.Boil80")
                    elif (myline == "sys status 0x65"):
                        self.TriggerEvent("iKettle.Boil65")
                    elif (myline == "sys status 0x11"):
                        self.TriggerEvent("iKettle.Warm")
                    elif (myline == "sys status 0x10"):
                        self.TriggerEvent("iKettle.WarmEnded")
                    elif (myline == "sys status 0x5"):
                        self.TriggerEvent("iKettle.On")
                    elif (myline == "sys status 0x0"):
                        self.TriggerEvent("iKettle.Off")
                    elif (myline == "sys status 0x3"):
                        self.TriggerEvent("iKettle.Completed")
                    elif (myline == "sys status 0x2"):
                        self.TriggerEvent("iKettle.NoWater")
                    elif (myline == "sys status 0x1"):
                        self.TriggerEvent("iKettle.Removed")

            stopThreadEvent.wait(1.0)
            return True

        # Maybe should be used for some kind of timeout?
        def check_connected(self):
            if (self.kettleconnected == 0):
                try:
                    self.sock.close()
                except:
                    pass
                print "Failed to connect to kettle"
                
        def __stop__(self):
            if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
            
            print "Closing"
            try:
                self.sock.close()
            except:
                pass
            print "iKettle is stopped."
            
        def __close__(self):
            if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
            
            try:
                self.sock.close()
            except:
                pass

class Connect(eg.ActionBase):
    name = "Connect"
    description = "Connect to iKettle. Is it necesarry?"
    
    def __call__(self):
        print "Connecting...."
        self.plugin.kettleconnect()

class TurnOn(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x4")
    
class TurnOff(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x0")
    
class Boil100(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x80")
    
class Boil95(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x2")
    
class Boil80(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x4000")
    
class Boil65(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x200")
    
class Warm(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8")
    
class SetWarm5(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8005")
    
class SetWarm10(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8010")
    
class SetWarm20(eg.ActionBase):
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8020")
    
    
            