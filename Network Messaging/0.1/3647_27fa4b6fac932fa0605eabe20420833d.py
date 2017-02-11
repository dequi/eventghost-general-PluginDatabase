import eg

eg.RegisterPlugin(
    name = "Network Messaging",
    version = "0.1",
    author = "Koke",
    description = (
        "Based on Network Sender."
    ),
)

import wx
import socket
from hashlib import md5
import time
import os
import copy


class Text:
    hostList = "Comma Delimited list of hosts:"
    port = "Port:"
    password = "Password:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    class SendMessage:
        parameterDescription = "Event name to send:"


class NetworkMessaging(eg.PluginBase):
    canMultiLoad = True
    text = Text

    def __init__(self):
        self.AddAction(SendMessage)
        self.AddAction(EventHandler)
        self.AddAction(SetStatus)
        self.AddAction(GetStatus)
        
        
    def __start__(self, hostList, port, password):
        self.hostList = hostList.upper().replace(' ', '').split(',')
        self.port = port
        self.password = password
        self.status = {}
        self.computerName = os.getenv('COMPUTERNAME').capitalize()
        self.pollTime = 30
        self.timeout = 65
        self.networkRouter = '1.1.1.1'
        self.statusFileName = '!Status.txt'
        self.PollTask = None

        
        if not os.path.exists(self.statusFileName):
            eg.plugins.FileOperations.Write(3, 'Offline', self.statusFileName, 0, 0, False, False, False, 'ascii')
        lastStatus = eg.plugins.FileOperations.Read(2, self.statusFileName, 0, 0, 'ascii', 1, False, 1)
        eg.plugins.FileOperations.Write(3, 'Online', self.statusFileName, 0, 0, False, False, False, 'ascii')
        
        #Status Checks
        if lastStatus == 'Online':
            statusMessage = 'Recovered'
        elif lastStatus.count('Info.') > 0:
            statusMessage = lastStatus
        else:
            statusMessage = 'Online'
        
        print ''.join(['My status: ', statusMessage.replace('Info.', '')])
        
        self.StartupRoutine(statusMessage)


    def Configure(self, host="127.0.0.1", port=1024, password=""):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        
        st1 = panel.StaticText(text.hostList)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.password)
        eg.EqualizeWidths((st1, st2, st3))
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st1, hostCtrl),
            (st2, portCtrl),
        )
        securityBox = panel.BoxedGroup(
            text.securityBox,
            (st3, passwordCtrl),
        )
        
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(securityBox, 0, wx.TOP|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                passwordCtrl.GetValue()
            )


    def Send(self, message, host, payload=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(2.0)
        try:
            sock.connect((host, self.port))
            sock.settimeout(1.0)
            # First wake up the server, for security reasons it does not
            # respond by it self it needs this string, why this odd word ?
            # well if someone is scanning ports "connect" would be very 
            # obvious this one you'd never guess :-) 

            sock.sendall("quintessence\n\r")

            # The server now returns a cookie, the protocol works like the
            # APOP protocol. The server gives you a cookie you add :<password>
            # calculate the md5 digest out of this and send it back
            # if the digests match you are in.
            # We do this so that no one can listen in on our password exchange
            # much safer then plain text.

            cookie = sock.recv(128)        

            # Trim all enters and whitespaces off
            cookie = cookie.strip()

            # Combine the token <cookie>:<password>
            token = cookie + ":" + self.password

            # Calculate the digest
            digest = md5(token).hexdigest()

            # add the enters
            digest = digest + "\n"
                    
            # Send it to the server        
            sock.sendall(digest)

            # Get the answer
            answer = sock.recv(512)

            # If the password was correct and you are allowed to connect
            # to the server, you'll get "accept"
            if (answer.strip() != "accept"):
                sock.close()
                return False

            # now just pipe those commands to the server
            if (payload is not None) and (len(payload) > 0):
                for pld in payload:
                    sock.sendall("payload %s\n" % pld.encode(eg.systemEncoding))
            
            if message != '':
                sock.sendall("payload withoutRelease\n")
                sock.sendall(''.join([self.computerName, '.', message]).encode(eg.systemEncoding) + "\n")
            
            #Leave recovered status alone
            if self.status[host] != 'Recovered':
                self.UpdateStatus(host, 'Online')
        #Failed to connect to Network Receiver
        except:
            if eg.debugLevel:
                eg.PrintTraceback()
            sock.close()
            
            #Update comptuer status
            if self.status[self.computerName] == 'Start' or self.status[host] == 'Offline':
                self.UpdateStatus(host, 'Offline')
            else:
                if self.status[host] != 'Offline':
                    self.UpdateStatus(host, time.time())
                else:
                    if time.time() - self.status[host] > self.timeout:
                        eg.TriggerEvent(''.join(['Network.',host, '.MIA']))
                        self.UpdateStatus(host, 'MIA')
                        eg.plugins.EventGhost.ShowOSD(''.join([host, ' - MIA']), u'0;-24;0;0;0;700;0;0;0;1;0;0;2;32;Arial', (255, 0, 0), (0, 0, 0), 3, (0, 25), 0, 5, True)

        
    def UpdateStatus(self, host, status):
        if self.status[self.computerName] == 'Start':
            print ''.join([host,' - ', status])
        
        self.status[host] = status
            
            
    def MapUp(self, sock):
        # tell the server that we are done nicely.
        sock.sendall("close\n")
        sock.close()
        
    
    def PollComputers(self):
        if self.status[self.computerName] != 'Offline':
            self.SendMessage('')
            self.DebugMessage('Poll Online')
            self.PollTask =  eg.scheduler.AddTask(self.pollTime, self.PollComputers)
        else:
            self.DebugMessage('Poll Offline')
            self.PollTask = eg.scheduler.AddTask(60, self.StartupRoutine)
        
        
    def SendMessage(self, message, to=None):
        #Set computers to send to
        if to == None:
            hostList = self.status.keys()
        else:
            hostList = to.replace(' ', '').split(',')
        hostList.sort()
        
        
        #Send message to only active computers unless we're just pinging them
        for host in hostList:
            host.capitalize()
            if host != self.computerName and ((self.status[host] != 'Offline' and self.status[host] != 'MIA') or message == ''):
                res = self.Send(eg.ParseString(message), host)
                
                if res:
                    eg.event.AddUpFunc(self.plugin.MapUp, res)

        
    def StartupRoutine(self, statusMessage='Online'):
        self.DebugMessage('Startup Routine')
        for host in self.hostList:
            self.status[host.capitalize()] = 'Offline'

        self.status[self.computerName] = 'Start'
        
        #wait for nics to initialize
        time.sleep(8)
        
        if self.OnNetwork():
            self.SendMessage('')
            self.status[self.computerName] = 'Online'
            self.SendMessage(statusMessage)
            self.PollTask = eg.scheduler.AddTask(self.pollTime, self.PollComputers)
        else:
            self.status[self.computerName] = 'Offline'
            self.PollTask = eg.scheduler.AddTask(60, self.PollComputers(statusMessage))
        
        
    def ShutdownRoutine(self):
        self.DebugMessage('Shutdown Routine')
        if self.status[self.computerName] != 'Offline':
            self.SendMessage('Offline')
            self.status[self.computerName] = 'Offline'
            try:
                eg.scheduler.CancelTask(self.PollTask)
            except:
                pass
            if eg.plugins.FileOperations.Read(2, self.statusFileName, 0, 0, 'ascii', 1, False, 1).lower().count('info.') == 0:
                eg.plugins.FileOperations.Write(3, 'Offline', self.statusFileName, 0, 0, False, False, False, 'ascii')
        
 
    def OnNetwork(self):
        for i in range(1, 5):
            if os.popen(''.join(['C:\Windows\system32\ping.exe ', self.networkRouter, ' -n 1 -w 5'])).read().count('Lost = 0') == 1:
                return True
            else:
                time.sleep(2)
        return False
        
        
    def DebugMessage(self, message):
        self.computerName = self.computerName
        #print ''.join([time.asctime(), ' - ', message])
        
        
class SendMessage(eg.ActionWithStringParameter):
    def __call__(self, message, to=None):
            self.plugin.SendMessage(message, to)
        
        
class EventHandler(eg.ActionClass):
    def __call__(self):
        message = eg.event.string.split('.', 2)

        #Local Events
        if message[0] == 'Main' or message[0] == 'System':
            if message[1] == ('Resume'):
                self.plugin.DebugMessage('Resume - call startup routine')
                self.plugin.StartupRoutine()
            else:
                self.plugin.DebugMessage('Shutdown - call shutdown routine')
                self.plugin.ShutdownRoutine()
                
        #Network Events
        else:
            #Computer online notice
            if message[2] == 'Online':
                eg.plugins.EventGhost.ShowOSD(''.join([message[1], ' - ', message[2]]), u'0;-24;0;0;0;700;0;0;0;1;0;0;2;32;Arial', (0, 255, 0), (0, 0, 0), 3, (0, 25), 0, 2, True)
                self.plugin.UpdateStatus(message[1], 'Online')

            #Computer offline notice
            elif message[2] == 'Offline':
                eg.plugins.EventGhost.ShowOSD(''.join([message[1], ' - ', message[2]]), u'0;-24;0;0;0;700;0;0;0;1;0;0;2;32;Arial', (255, 255, 0), (0, 0, 0), 3, (0, 25), 0, 2, True)
                self.plugin.UpdateStatus(message[1], 'Offline')

            #Computer recovery notice
            elif message[2] == 'Recovered':
                eg.plugins.EventGhost.ShowOSD(''.join([message[1], ' - ', message[2]]), u'0;-24;0;0;0;700;0;0;0;1;0;0;2;32;Arial', (255, 0, 0), (0, 0, 0), 3, (0, 25), 0, 10, True)
                self.plugin.UpdateStatus(message[1], 'Recovered')
            
            #Info message            
            elif message[2].find('Info.') == 0:
                eg.plugins.EventGhost.ShowOSD(''.join([message[1], ' - ', message[2].replace('Info.', '')]), u'0;-24;0;0;0;700;0;0;0;1;0;0;2;32;Arial', (0, 255, 255), (0, 0, 0), 3, (0, 25), 0, 2, True)

            #Computer status reqested
            elif message[2] == 'Requestsstatus':
                self.plugin.SendMessage(self.plugin.status[self.plugin.computerName], message[1])
                
            #System standby requested
            elif message[2] == ''.join([self.plugin.computerName, '.Standby']):
                self.plugin.ShutdownRoutine
                eg.plugins.System.Standby(False)
                
                
class SetStatus(eg.ActionClass):
    def __call__(self, status, computer=None):
        if computer == None:
            computer = self.plugin.computerName
        self.plugin.status[computer] = status
    
    
class GetStatus(eg.ActionClass):
    def __call__(self):
        statusList = copy.copy(self.plugin.status)
        
        #replace time stamps with MIA
        for host in statusList.keys():
            if isinstance(statusList[host], float):
                statusList[host] = 'MIA'
            if host == self.plugin.computerName:
                del statusList[host]

        return statusList