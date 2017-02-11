import httplib
import urllib
import re
from time import sleep
import socket #<added 0.2>
import wx.lib
import eg
from xml.dom.minidom import parse, parseString
from threading import Thread

# You're welcome to add more features to this plugin, just make sure to post it
# back to the EG forum thread for this plugin (see the url= parameter of the
# RegisterPlugin method below.  This plugin currently only sends "keypress"
# and "launch" commands to the Roku device.  It does not make use of the keydown and keyup commands
# (which could enable pressing and holding a key in order to repeat a command).
# The plugin only makes use of the launch command to launch a channel (numeric values only).
# It does not launch streaming video URL's in your own app.
# If you want to be SUPER fancy, you could use the
# query/icon command to get the icon for those channels too!

#<added 0.2>
# When the plugin starts, it will search for Roku devices on the network automatically
# When you select an action you will be prompted to select which Roku the command
# will be sent to. Each command is stored against the SN of the Roku device not the IP
# address. This mean if the IP address changes and EG restarts, the commands will still 
# work as long as the plugin finds the same Roku on the network. 
#
# The port number should always be 8060, per the Roku External Control Guide.
PORT = "8060"

#<added 0.2>
#examples of SSDP search and response
'''
M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
Man: "ssdp:discover"
ST: roku:ecp
'''
'''
HTTP/1.1 200 OK
Cache-Control: max-age=300
ST: roku:ecp
Location: http://192.168.1.134:8060/
USN: uuid:roku:ecp:P0A070000007
'''
# EventGhost Constants
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02

globalRokuDict = {}

eg.RegisterPlugin(
    name = "RokuNet",
    author = "barnabas1969",
    version = "0.2",
    kind = "external",
    createMacrosOnAdd = False,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5995",
    description = "Allows control of a Roku player over Ethernet or WiFi.",
)

def HtmlSplit(data=""): #<added 0.2>
    header = {}
    header['body'] = ""
    headerstring = data.split("\r\n\r\n")[0]
    try:
        header['body'] = data.split("\r\n\r\n")[1]
    except:
        pass
    headerlist = headerstring.split("\r\n")
    try:
        header['status-type'] = headerlist[0].split(" ",2)[0]
        header['status-code'] = headerlist[0].split(" ",2)[1]
        header['status'] = headerlist[0].split(" ",2)[2]
        headerlist = headerlist[1:]
    except:
        header['status-type'] = "Unknown"
        header['status-code'] = "NA"
        header['status'] = "Response Error, Status Code not found (HtmlSplit)"
    for s in headerlist:
        variable = s.split(":",1)[0]
        try:
            value = s.split(":",1)[1].strip() #remove white space, there is usually a space after :
        except:
            value = ""
        header[variable] = value
    return header  

    
def get_lan_ip():
    """
    Attempts to open a socket connection to Google's DNS
    servers in order to determine the local IP address
    of this computer. Eg, 192.168.1.100
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def get_network_prefix():
    """
    Returns the network prefix, which is the local IP address
    without the last segment, Eg: 192.168.1.100 -> 192.168.1
    """
    lan_ip = get_lan_ip()
    return lan_ip[:lan_ip.rfind('.')]
    
def create_ip_range(range_start, range_end):
    """
    Given a start ip, eg 192.168.1.1, and an end ip, eg 192.168.1.254,
    generate a list of all of the ips within that range, including
    the start and end ips.
    """
    ip_range = []
    start = int(range_start[range_start.rfind('.')+1:])
    end = int(range_end[range_end.rfind('.')+1:])
    for i in range(start, end+1):
        ip = range_start[:range_start.rfind('.')+1] + str(i)
        ip_range.append(ip)
    return ip_range

def auto_detect_ip_threaded(self):
    """
    Blasts the network with requests, attempting to find any and all yamaha receivers
    on the local network. First it detects the user's local ip address, eg 192.168.1.100.
    Then, it converts that to the network prefix, eg 192.168.1, and then sends a request
    to every ip on that subnet, eg 192.168.1.1 -> 192.168.1.254. It does each request on
    a separate thread in order to avoid waiting for the timeout for every 254 requests
    one by one.
    """
    devices = []
    print "this is rList"
    print self.rList
    # Get network prefix (eg 192.168.1)
    net_prefix = get_network_prefix()
    print net_prefix
    ip_range = create_ip_range(net_prefix + '.1', net_prefix + '.254')
    print ip_range
    threads = []
    for ip in ip_range:
        t = Thread(target=try_connect, kwargs={'self':self,'ip':ip})
        t.daemon = True
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    
    if devices is not None:
        pass
    else:
        eg.PrintError("No Roku Was Not Found!")
    
def try_connect(self, ip):
    """
    Used with the auto-detect-ip functions, determines if a Roku is
    waiting at the other end of the given ip address.
    """
    #ip = "192.168.1.171"
    lastnum = ip[ip.rfind('.'):]
    recvsock = int(lastnum[1:]) + 65500
    bindsock = int(lastnum[1:]) + 5000
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)#very important if useing while loop to receive all responses,if this is removed, loop occurs
        s.bind(('', bindsock))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nST: roku:ecp\r\n\r\n'
        s.sendto(data, (ip, 1900))
        data, srv_sock = s.recvfrom(recvsock)              
        if data.find("ST: roku:ecp") > 0: #verify it's roku
            srv_addr = srv_sock[0]
            html = HtmlSplit(data)
            #USN: uuid:roku:ecp:P0A070000007
            sn = html["USN"].split(":")[-1]
            location = html["LOCATION"]
            #print html
            self.rList[sn] = {}
            self.rList[sn]['ip'] = srv_addr
            self.rList[sn]['location'] = location
    except:
        pass
    
def SearchForRoku(self): #<added 0.2>
    self.rList = {} #need to make zp class now. 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)#very important if useing while loop to receive all responses,if this is removed, loop occurs
        s.bind(('', 5001))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nST: roku:ecp\r\n\r\n'
        s.sendto(data, ('239.255.255.250', 1900))
        print "Searching for Rokus on network..."
        while True:#look until timeout # this is to capture all responses
            data, srv_sock = s.recvfrom(65565)              
            if not data: break
            if data.find("ST: roku:ecp") > 0: #verify it's roku
                srv_addr = srv_sock[0]
                html = HtmlSplit(data)
                #USN: uuid:roku:ecp:P0A070000007
                sn = html["USN"].split(":")[-1]
                location = html["LOCATION"]
                #print html
                self.rList[sn] = {}
                self.rList[sn]['ip'] = srv_addr
                self.rList[sn]['location'] = location
    except Exception, e:
        if str(e) == "timed out":
            print "Roku search complete"
        else:
            print "RokuNet ERROR %s - %s" % (Exception, e)
        
    
    print "trying full ip network search"
    auto_detect_ip_threaded(self)
    s.close
    return self.rList    


class WindowRokuSelect(): #<added 0.2>
    def __init__(self, roku="", title="Select a Roku Player from the list below..."):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextRokuSelect = wx.StaticText(panel, -1, title)
        
        ChoiceList = []
        if globalRokuDict:
            for sn, v in globalRokuDict.iteritems():
                ChoiceList.append(v['ip'] + "-" + sn)
            ChoiceList.sort()
            RokuDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No Roku players found on network"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalRokuDict[roku]['ip'] + "-" + roku)
            RokuDropDown.SetSelection(p)
        except: #ValueError:
            RokuDropDown.SetSelection(0)
        mySizer.Add(TextRokuSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(RokuDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        while panel.Affirmed():
            FinalChoice = RokuDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[1], #save only the Roku SN from the list.
            )  
            

def GetRokuChIDs(ip):#<added 0.2>    
    IDs = {}
    print "getting Roku Channels"
    print "%s:8060/squery/apps" % ip 
    conn = httplib.HTTPConnection(ip,8060)
    try:
        conn.request("GET", "/query/apps")
        r = conn.getresponse()
        #print r.status, r.reason
        data = r.read()
        #print data
        conn.close()
        try:
            xml = parseString(data)
            idList = xml.getElementsByTagName('app')
            for id in idList:
                IDs[id.getAttribute('id')] = id.firstChild.nodeValue
        except:
            print "XML Parsing Error"
    except Exception, e:
        print "ERROR %s" % e
        conn.close()  
    return IDs

class WindowRokuSelecttwo(): #<added 0.2>  
  
    def UpdateIDDropDown(self):
        ChoiceList = []
        if self.IDs:
            for d, ch in self.IDs.iteritems():
                ChoiceList.append(ch + "-" + d)
            ChoiceList.sort()
            #self.IDDropDown =  wx.Choice(self.panel, -1, choices=ChoiceList)
            try:
                for ch in ChoiceList:
                    self.IDDropDown.Append(ch)
            except:
                self.IDDropDown =  wx.Choice(self.panel, -1, choices=ChoiceList)
        else:
            print "!! No Channel IDs found on Roku"
            #return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(self.IDs[self.id] + "-" + self.id)
            self.IDDropDown.SetSelection(p)
        except: #ValueError:
            self.IDDropDown.SetSelection(0)
   
    def OnSearchButton(self, event):
        self.IDs = GetRokuChIDs(globalRokuDict[self.roku]["ip"])
        self.IDDropDown.Clear()
        self.UpdateIDDropDown()
    
    def __init__(self, roku="", id = '', title="Select a Zone Player and item from the list below...", text1="", text2=""):
        self.panel = eg.ConfigPanel()
        self.id = id
        self.IDs = {"Netflix":"12"}
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        self.panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextRokuSelect = wx.StaticText(self.panel, -1, title)
        TextIDSelect = wx.StaticText(self.panel, -1, text1)
        TextNote = wx.StaticText(self.panel, -1, text2)
        #searchButton = wx.Button(self.panel, -1, "Refresh Channel ID list")
        #============ dropdown ==============
        ChoiceList = []
        if globalRokuDict:
            for sn, v in globalRokuDict.iteritems():
                ChoiceList.append(v['ip'] + "-" + sn)
            ChoiceList.sort()
            RokuDropDown =  wx.Choice(self.panel, -1, choices=ChoiceList)
        else:
            print "!! - No Roku players found on network"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalRokuDict[roku]['ip'] + "-" + roku)
            self.roku = roku
            RokuDropDown.SetSelection(p)
        except: #ValueError:
            RokuDropDown.SetSelection(0)
            self.roku = ChoiceList[0].split("-")[1]
        #============ end dropdown ==============
        #get channel IDs based on Roku selected in drop down list.
        if not self.roku == "":
            self.IDs = GetRokuChIDs(globalRokuDict[self.roku]["ip"])
        #============ dropdown ==============
        self.UpdateIDDropDown()
        #============ end dropdown ==============
        mySizer.Add(TextRokuSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(RokuDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextIDSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(self.IDDropDown, (3,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextNote, (4,0), flag = wx.EXPAND)
        #mySizer.Add(searchButton, (5,0), flag = wx.ALIGN_RIGHT)
        RokuDropDown.Bind(wx.EVT_CHOICE, self.OnSearchButton)
        #searchButton.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        while self.panel.Affirmed():
            FinalChoice = RokuDropDown.GetStringSelection()
            FinalID = self.IDDropDown.GetStringSelection()
            self.panel.SetResult(
                FinalChoice.split("-")[1], #save only the SN from the list.
                FinalID.split("-")[1] #save only the ID from the list.
            )

class ChannelAction(eg.ActionBase): #<added 0.2>
    name = "Select Roku Channel"
    description = "Open installed channel on selected Roku player"

    def __call__(self, roku="", id=""):
        if roku == "":
            print "Please select a Roku player to send command to."
            return
        if roku not in globalRokuDict:
            print "!!! Roku player no longer in globalRokuDict (not found on network) !!!"
            return
        try:
            return self.plugin.roku.send_action(roku, id, ACTION_BUTTON)
        except Exception, e:
            print "ch error: %s" % e
            raise self.Exceptions.ProgramNotRunning
            
    def Configure(self, roku="", id=""):
        title = "Select a Roku Player from the list below..."
        text1 = '''Select a Channel from the list below'''
        text2 = '''The Channel ID list will automatically update\nwhen you change Roku Players'''
        winSelectGUI = WindowRokuSelecttwo(roku, id, title, text1, text2)

            
class RokuAction(eg.ActionClass):
    def __call__(self, roku=""):
        if roku == "":
            print "Please select a Roku player to send command to."
            return
        if roku not in globalRokuDict:
            print "!!! Roku player no longer in globalRokuDict (not found on network) !!!"
            return
        try:
            return self.plugin.roku.send_action(roku, self.value, ACTION_BUTTON)
        except Exception, e:
            print "action error: %s" % e
            raise self.Exceptions.ProgramNotRunning
            
    def Configure(self, roku=""):
        winSelectGUI = WindowRokuSelect(roku)   

class RokuNet(eg.PluginBase):
    def __init__(self):
        group1 = self.AddGroup("RemoteControl","Send commands as if pushing buttons on the IR/RF remote control.")
        group1.AddActionsFromList(REMOTE_ACTIONS, RokuAction)
        group2 = self.AddGroup("ChannelDirect", "Actions that directly start a channel.")
        group2.AddActionsFromList(CHANNEL_ACTIONS, RokuAction)
        group3 = self.AddGroup("Keyboard", "Send any key from a keyboard.  Use this to type a string into a search box, etc.")
        group3.AddActionsFromList(KEYBOARD_ACTIONS, RokuAction)
        
    def __start__(self):    
        global globalRokuDict
        globalRokuDict = SearchForRoku(self)
        if not globalRokuDict:  #if nothing found, try one more time. 
            globalRokuDict = SearchForRoku(self)
        if globalRokuDict:
            for sn, roku in globalRokuDict.iteritems():
                print "Roku found: %s - %s - %s" % (sn, roku['ip'],roku['location'])          
        else:
            print "no rokus found on network"
            raise self.Exceptions.ProgramNotRunning
        self.roku = RokuNetClient()
    
    def __stop__(self):
        pass
        
    def __close__(self):
        pass

def send_key(keycmd, roku):
    global globalRokuDict
    print "Sending Key command: %s - %s" % (keycmd, globalRokuDict[roku]['ip'] )
    conn = httplib.HTTPConnection("%s:%s" % ( globalRokuDict[roku]['ip'], PORT ))
    headers = { "Content-type": "text/html" }
    try:
        conn.request("POST", "/keypress/" + keycmd, "", headers)
        conn.close()
    except:
        #if the IP address has changed, search the network to update the IP address and try again.
        print "Roku send_key connection error:"
        globalRokuDict = SearchForRoku()
        conn.request("POST", "/keypress/" + keycmd, "", headers)
        conn.close()

def launch_channel(appid, roku):
    global globalRokuDict
    print "Sending Channel number: %s - %s" % (appid, globalRokuDict[roku]['ip'] )
    conn = httplib.HTTPConnection("%s:%s" % ( globalRokuDict[roku]['ip'], PORT ))
    headers = { "Content-type": "text/html" }
    try:
        conn.request("POST", "/launch/" + appid, "", headers)
        conn.close()
    except:
        #if the IP address has changed, search the network to update the IP address and try again.
        print "Roku launch_channel connection error:"
        globalRokuDict = SearchForRoku()
        conn.request("POST", "/launch/" + appid, "", headers)
        conn.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class RokuNetClient:
    def __init__(self):
        print "Init"

    def send_action(self, roku, msg = '', type = ACTION_EXECBUILTIN):
        if is_number(msg) == True:
            launch_channel(msg, roku)
        else:
            send_key(msg, roku)
            sleep(0.1)

# The action lists below consist of the following structure:
#   ("class", "Command Name", "Command Description", "parameter"),
#
# Parameter values below may be any of the "Valid Keys", per the documentation at:
# http://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide
#
# The parameter may also be "Lit_X" where X is a single keyboard key.  Special keys
# must be URL-encoded.  FYI, "Lit_" means "Literal string".
#
# Finally, the parameter may be a numeric app id, as found by going to:
# http://<your_roku_IP_address>:8060/query/apps
REMOTE_ACTIONS = (   
    ("Home", "Home", "Go to the home screen.", "home"),
    ("Back", "Back", "Go back to the previous screen", "back"),
    ("Left", "Left", "Move left", "left"),
    ("Right", "Right", "Move right", "right"),
    ("Down", "Down", "Move down", "down"),
    ("Up", "Up", "Move up", "up"),
    ("OK", "OK", "Select the currently highlighted channel or whatever.", "select"),
    ("Rewind", "Rewind", "Rewind the currently playing video.", "rev"),
    ("FastFwd", "Fast Forward", "Fast forward the currently playing video.", "fwd"),
    ("PlayPause", "PlayPause", "Play or Pause the currently playing video.", "play"),
    ("InstantReplay", "Instant Replay", "Skip back a few seconds", "instantreplay"),
    ("Option", "Option", "Sends the asterisk (*) key.", "Lit_*"),
    ("Info", "Info", "See more info?", "info"),
    ("Search", "Search", "Open a search dialog. See actions under Keyboard to enter text in the search box.", "search"),
)    

CHANNEL_ACTIONS = (
    (ChannelAction, "ChannelSelect", "ChannelSelect", "Select and Start the Channel.", None), #<added 0.2>
    ("Netflix", "Netflix", "Start the Netflix channel.", "12"),
    ("Amazon", "Amazon Instant Video", "Start the Amazon Instant Video channel.", "13"),
    ("HuluPlus", "Hulu Plus", "Start the Hulu Plus channel.", "2285"),
    ("Crackle", "Crackle", "Start the Crackle channel.", "2016"),
    ("Pandora", "Pandora", "Start the Pandora channel.", "28"),
)    

KEYBOARD_ACTIONS = (   
    ("Enter", "Enter", "Sends the enter key after typing in a string in a search box.", "enter"),
    ("Backspace", "Backspace", "Sends a backspace keyboard key.", "backspace"),
    ("Space", "Space", "Sends a space keyboard key.", "Lit_+"),
    ("A", "A", "Letter a", "Lit_a"),
    ("B", "B", "Letter b", "Lit_b"),
    ("C", "C", "Letter c", "Lit_c"),
    ("D", "D", "Letter d", "Lit_d"),
    ("E", "E", "Letter e", "Lit_e"),
    ("F", "F", "Letter f", "Lit_f"),
    ("G", "G", "Letter g", "Lit_g"),
    ("H", "H", "Letter h", "Lit_h"),
    ("I", "I", "Letter i", "Lit_i"),
    ("J", "J", "Letter j", "Lit_j"),
    ("K", "K", "Letter k", "Lit_k"),
    ("L", "L", "Letter l", "Lit_l"),
    ("M", "M", "Letter m", "Lit_m"),
    ("N", "N", "Letter n", "Lit_n"),
    ("O", "O", "Letter o", "Lit_o"),
    ("P", "P", "Letter p", "Lit_p"),
    ("Q", "Q", "Letter q", "Lit_q"),
    ("R", "R", "Letter r", "Lit_r"),
    ("S", "S", "Letter s", "Lit_s"),
    ("T", "T", "Letter t", "Lit_t"),
    ("U", "U", "Letter u", "Lit_u"),
    ("V", "V", "Letter v", "Lit_v"),
    ("W", "W", "Letter w", "Lit_w"),
    ("X", "X", "Letter x", "Lit_x"),
    ("Y", "Y", "Letter y", "Lit_y"),
    ("Z", "Z", "Letter z", "Lit_z"),
    ("0", "0", "Number 0", "Lit_0"),
    ("1", "1", "Number 1", "Lit_1"),
    ("2", "2", "Number 2", "Lit_2"),
    ("3", "3", "Number 3", "Lit_3"),
    ("4", "4", "Number 4", "Lit_4"),
    ("5", "5", "Number 5", "Lit_5"),
    ("6", "6", "Number 6", "Lit_6"),
    ("7", "7", "Number 7", "Lit_7"),
    ("8", "8", "Number 8", "Lit_8"),
    ("9", "9", "Number 9", "Lit_9"),
    ("Plus", "Plus", "Character +", "Lit_%2B"),
    ("Minus", "Minus", "Character -", "Lit_-"),
    ("Slash", "Slash", "Character /", "Lit_%2F"),
    ("Asterisk", "Asterisk", "Character *", "Lit_*"),
)    
