eg.RegisterPlugin(
    name = "xPL",
    author = "doghouselabs.com", 
    version = "0.2.2",
    canMultiLoad = False,
    description = "send and receive xPL messages.",
)

##############################################################################
# Revision history:
#
# 2009-07-17 Walter Kraembring: Added action for catching xPL messages,
#            changed version to 0.2.2
##############################################################################
    
import sys, string, select, re
from socket import *
import wx
from threading import Event, Thread

class Text:
    name = "send xPL Message"
    description = "sends an xPL message"
    textBoxLabel = "xPL Msg Type"
    textBoxLabel0 = "xPL Schema"
    textBoxLabel1 = "xPL Target"
    textBoxLabel2 = "xPL Message"
    
    class catchxPL:    
        name = "catch an xPL Message"
        description = "catch an xPL message from a specified sender and creates a named EG event"
        textBoxLabel3 = "Name"
        textBoxLabel4 = "xPL Sender"
        textBoxLabel5 = "xPL Message"
        textBoxLabel6 = "EG Event"


#
# core xPL code is from John Bent's python xPL monitor
#
class xPL(eg.PluginClass):
    
  # Define maximum xPL message size
    buff = 1500
    def __init__(self):
        self.LocalIP=gethostbyname(gethostname())
        self.hostname="doghouse-eg."+str(gethostname())
        # add class to send messages              
        self.AddAction(sendxPL)
        self.AddAction(catchxPL)
              
    def __start__(self):
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)
        # Initialise the socket
        self.port = 50000
        bound = 0
        while bound == 0 :
            bound = 1
            try :
                addr = ('0.0.0.0',self.port)
                self.UDPSock.bind(addr)
            except :
                bound = 0
                self.port += 1
                
        print "xPL plugin, bound to port " + str(self.port)

        print "xPL is started"
        # start the heartbeat thread
        self.hbThreadEvent = Event()
        hbThread = Thread(target=self.SendHeartbeat, args=(self.hbThreadEvent,))
        hbThread.start()
        # start the main thread that scans for incoming xPL msgs
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()

    def __stop__(self):
        self.hbThreadEvent.set()
        self.mainThreadEvent.set()
        hbSock = socket(AF_INET,SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        msg = "xpl-stat\n{\nhop=1\nsource="+str(self.hostname)+"\ntarget=*\n}\nhbeat.end\n{\ninterval=5\nport="
        msg = msg + str(self.port) + "\nremote-ip=" + str(self.LocalIP) + "\nversion=1.2\n}\n"
        hbSock.sendto(msg,("255.255.255.255",3865))
        hbSock.sendto(msg,("255.255.255.255",self.port))
        self.UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def __close__(self):
        print "XPL is closed."
  
# Sub routine for sending a heartbeat
    def SendHeartbeat(self,hbThreadEvent) :
        hbSock = socket(AF_INET,SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        while not hbThreadEvent.isSet():
            msg = "xpl-stat\n{\nhop=1\nsource="+str(self.hostname)+"\ntarget=*\n}\nhbeat.app\n{\ninterval=5\nport="
            msg = msg + str(self.port) + "\nremote-ip=" + str(self.LocalIP) + "\nversion=1.2\n}\n"
            hbSock.sendto(msg,("255.255.255.255",3865))
            hbThreadEvent.wait(5*60.0)
            
# Main Loop
    def main(self,mainThreadEvent):
        while not mainThreadEvent.isSet():
            readable, writeable, errored = select.select([self.UDPSock],[],[],60)
            if len(readable) == 1 :
                data,addr = self.UDPSock.recvfrom(1500)
                message = str(data)
                message = message.splitlines()
                xpltype = message[0]
                
                msgheader = message[2:5]
                xplsource = message[3].rsplit("=")[1]
                xpltarget = message[4].rsplit("=")[1]
                
                msgschema = message[6]
                xplschema = msgschema.rsplit(".")
                
                msgbody = message[8:-1]
                msgbody2 = ""
                # ignore heartbeat messages and messages from myself
                if msgschema <> "hbeat.app" :
                    if xplsource <> self.hostname:
                        for element in msgbody:
                            msgbody2 = msgbody2 + element + ","
                        self.TriggerEvent(xpltype+":"+msgschema+":"+xplsource+":"+xpltarget+":"+msgbody2)
     
      
      
class sendxPL(eg.ActionClass):
    text = Text

    def __call__(self, xPLType, xPLSchema, xPLTarget, xPLMsg1):
        xPLMessage=re.compile('\r')
        xPLMessage.sub('',xPLMsg1)
        xPLMessage=re.compile('\n ')
        xPLMessage.sub('\n',xPLMsg1)
        msg = xPLType + "\n{\nhop=1\nsource="+self.plugin.hostname+"\ntarget="+xPLTarget+"\n}\n" + str(xPLSchema) + "\n{\n" + xPLMsg1 + "\n}\n"
        addr = ("255.255.255.255",3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        self.plugin.UDPSock.sendto(msg,addr)
        
    def Configure(
        self, 
        xPLType="",
        xPLSchema="",
        xPLTarget="",
        xPLMsg1=""
        ):
        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        
        #type box.  as an example, you would put this in the box: xpl-cmnd
        textType = wx.TextCtrl(panel, -1, xPLType)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizerz = wx.BoxSizer(wx.HORIZONTAL)
        sizerz.Add(textType, 1, wx.EXPAND)
        staticBoxSizer.Add(sizerz, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        #schema box.  as an example, you would put this in the box: osd.basic
        textSchema = wx.TextCtrl(panel, -1, xPLSchema)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel0)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textSchema, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        #target box.  ex: *
        textTarget = wx.TextCtrl(panel, -1, xPLTarget)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(textTarget, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        

        # body of message, you would enter into this box:
        # command=write
        # delay=30
        # text=hello world
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel2)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        
        textMsg1 = wx.TextCtrl(panel, -1, xPLMsg1, style=wx.TE_MULTILINE)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(textMsg1, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                textType.GetValue(), 
                textSchema.GetValue(), 
                textTarget.GetValue(), 
                textMsg1.GetValue(), 
            )      
      
      
      
class catchxPL(eg.ActionClass):
    text = Text.catchxPL
    
        
    def __call__(self, xPLName, xPLSender, xPLMessage, egEvent):
        if eg.event.suffix.find(xPLSender) != -1:
            # split up the event components
            xPLSplit = eg.event.suffix.split(':')
            
            # make the pieces easy to remember
            xPLType = xPLSplit[0]
            xPLSchema = xPLSplit[1]
            xPLSource = xPLSplit[2]
            xPLTarget = xPLSplit[3]
            xPLBody = xPLSplit[4]
            
            # we only want xpl-trig messages
            if xPLType == "xpl-trig":
                # only want messages from blabber
                if re.search('doghouse-blabber',xPLSource):
                    bodySplit = xPLBody.split(',')
                    # extract the components of the message body
                    for i in range(3):
                        if re.search('device',bodySplit[i]):
                            senderSplit = bodySplit[i].split('=')
                        elif re.search('type',bodySplit[i]):
                            typeSplit = bodySplit[i].split('=')
                        elif re.search('current',bodySplit[i]):
                            currentSplit = bodySplit[i].split('=')
                    # we only want messages from defined sender
                    if senderSplit[1].find(xPLSender) != -1:
                        if typeSplit[1] == "message" and currentSplit[1]==xPLMessage:
                            # if we get the correct message we'll reply back to the sender
                            # that we got his message
                            returnMsg = "device="+senderSplit[1]+"\n"+\
                            "current=EG got your message: " + xPLMessage
                            eg.plugins.xPL.sendxPL(u'xpl-cmnd', u'control.basic', \
                            xPLSource, returnMsg)
                            # then we create the eg event
                            eg.TriggerEvent(xPLName+"."+egEvent)
             

    def Configure(
        self,
        xPLName = "give me a name" ,
        xPLSender = "my.daddy@home.net",
        xPLMessage = "message",
        egEvent = "EG event to be created"
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        
        #name box
        textName = wx.TextCtrl(panel, -1, xPLName)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel3)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizerz = wx.BoxSizer(wx.HORIZONTAL)
        sizerz.Add(textName, 1, wx.EXPAND)
        staticBoxSizer.Add(sizerz, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        #sender box
        textSender = wx.TextCtrl(panel, -1, xPLSender)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel4)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizerz = wx.BoxSizer(wx.HORIZONTAL)
        sizerz.Add(textSender, 1, wx.EXPAND)
        staticBoxSizer.Add(sizerz, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        #message box
        textMessage = wx.TextCtrl(panel, -1, xPLMessage)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel5)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textMessage, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        #eg event box
        textEvent = wx.TextCtrl(panel, -1, egEvent)           
        staticBox = wx.StaticBox(panel, -1, text.textBoxLabel6)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(textEvent, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 10)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                textName.GetValue(),
                textSender.GetValue(), 
                textMessage.GetValue(), 
                textEvent.GetValue()
            )      
      
