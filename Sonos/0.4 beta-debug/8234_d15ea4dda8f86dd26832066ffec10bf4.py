######################################## Register ############################################
eg.RegisterPlugin(
    name = "Sonos",
    author = "Chase Whitten (Techoguy)",
    version = "0.4 beta/debug",
    kind = "program",
    canMultiLoad = False,
    description = "This plugin allows you to control your SONOS zone players. This works with grouped zones or stereo pairs. NOTE: all Zone Players should have static IP addresses within the router. This plugin will search your network for Zone Players during startup, but if any are added or removed, it will not know this. Many more comands will be added soon.",
    createMacrosOnAdd = True,    
)
###################################### Import ###############################################
import eg
from xml.dom.minidom import parse, parseString
import httplib
import wx.lib
from socket import *
import time

zpList = {} #dict to store ZP and information about them. 

###################################### Functions ###########################################

### example of calling the speech plugin: eg.plugins.Speech.TextToSpeech(u'Microsoft Hazel Desktop - English (Great Britain)', 1, u'Today is a beutiful day. the temperature is 87 degrees outside at {TIME} ', 0, 100)


def entityencode(self, string):
    #string.replace('&','&amp;')
    string = string.replace('&','&amp;').replace(">",'&gt;').replace("<",'&lt;').replace('"','&quot;')
    return string

def entitydecode(self, string):
    return string

def connerror(self, status, reason):
    if not int(status) == 200:
        print "ERROR: " + str(status) + " - " + reason        

### weather call: http://xml.weather.yahoo.com/forecastrss/92081.xml
def getweatherforcast(self, zip):
    print "requesting weather from yahoo for zip code: " + zip
    path = "/forecastrss/" + zip + ".xml HTTP/1.1"
    host = "xml.weather.yahoo.com"
    port = 80
    hostport = host + ":" + str(port)
    conn = httplib.HTTPConnection(host,port)
    conn.request("GET", path, body="", headers = {
        "Host": hostport,
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": 0
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xmlstring = res.read()
    xml = parseString(xmlstring)
    forecast = {} #temp,text, todayshigh, todayslow, todaystext
    #x[i].getAttribute('category')
    forecast['temp'] = xml.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
    forecast['text'] = xml.getElementsByTagName('yweather:condition')[0].getAttribute('text')
    forecast['todayshigh'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('high')
    forecast['todayslow'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('low')
    forecast['todaystext'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('text')
    return forecast
        
def sendSetPlayMode(self, ip, playmode):
    print "Setting Play Mode to " + playmode
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:SetPlayMode xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
             <NewPlayMode>''' + playmode + '''</NewPlayMode>
          </u:SetPlayMode>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#SetPlayMode"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

def RemoveAllTracksFromQueue(self, ip):
    print "Removing All Tracks From Queue"
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <s:Body>
        <u:RemoveAllTracksFromQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
          <InstanceID>0</InstanceID>
        </u:RemoveAllTracksFromQueue>
      </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#RemoveAllTracksFromQueue"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

    
def AddURIToQueue(self, ip, uri, urimetadata):
    print "Add URI To Queue"
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    uri = entityencode(self, uri)
    urimetadata = entityencode(self, urimetadata)
    #print "  uri:   " + uri
    #print "  metadata:   " + urimetadata
    xml = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <s:Body>
        <u:AddURIToQueue xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
          <InstanceID>0</InstanceID>
          <EnqueuedURI>''' + uri + '''</EnqueuedURI>
          <EnqueuedURIMetaData>''' + urimetadata + '''</EnqueuedURIMetaData>
          <DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued>
          <EnqueueAsNext>0</EnqueueAsNext>
        </u:AddURIToQueue>
      </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#AddURIToQueue"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

def SetAVTransportURI(self, ip, uri, urimetadata=""):
    print "Set AV Transport URI"
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    uri = entityencode(self, uri)
    urimetadata = entityencode(self, urimetadata)
    #print "  uri:   " + uri
    #print "  metadata:   " + urimetadata
    xml ='''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <s:Body>
        <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
          <InstanceID>0</InstanceID>
          <CurrentURI>''' + uri + '''</CurrentURI>
          <CurrentURIMetaData>''' + urimetadata + '''</CurrentURIMetaData>
        </u:SetAVTransportURI>
      </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    conn.close()
    
def getfavlist(self, ip):
    path = "/MediaServer/ContentDirectory/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
          <s:Body>
             <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
                 <ObjectID>FV:2</ObjectID>
                 <BrowseFlag>BrowseDirectChildren</BrowseFlag>
                 <Filter>dc:title,res,dc:creator,upnp:artist,upnp:album,upnp:albumArtURI</Filter>
                 <StartingIndex>0</StartingIndex>
                 <RequestedCount>100</RequestedCount>
                 <SortCriteria></SortCriteria>
             </u:Browse>
          </s:Body>
        </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:ContentDirectory:1#Browse"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xmlstring = res.read()
    xml = parseString(xmlstring)
    xmlplayliststring = xml.getElementsByTagName('Result')[0].firstChild.nodeValue  
    xmlplayliststring = xmlplayliststring.replace('&gt;',">").replace('&lt;',"<").replace('&quot;','"')#.replace('&amp;','&') #& cant be in XML. 
    xml = parseString(xmlplayliststring)
    presets = {}
    for item in xml.getElementsByTagName('item'):
        #each item node has it's own item node with title which is captured in items. To determine which one i'm looking at, i look at # of children present 
        if len(item.childNodes) > 3: #if greater than 3, than it's the parent item node, else it's the child. 
            tempdescription = item.getElementsByTagName('r:description')[0].firstChild.nodeValue.replace(" Station","")
            temptitle = item.getElementsByTagName('dc:title')[0].firstChild.nodeValue
            tempurimetadata = item.getElementsByTagName('DIDL-Lite')[0].toxml().replace('&amp;','&')
            tempuri = item.getElementsByTagName('res')[0].firstChild.nodeValue
            tempupnpclass = item.getElementsByTagName('upnp:class')[1].firstChild.nodeValue
            if tempupnpclass.find("playlistContainer") > 0: #is this a streaming station or a playlist
                tempisplaylist = True
            else:
                tempisplaylist = False
            presets[temptitle]={}
            presets[temptitle]['description'] = tempdescription
            presets[temptitle]['uri'] = tempuri
            presets[temptitle]['urimetadata'] = tempurimetadata
            presets[temptitle]['upnpclass'] = tempupnpclass
            presets[temptitle]['isplaylist'] = tempisplaylist
    return presets
    
def sendrelvolume(self, ip, incvol):
    path = "/MediaRenderer/RenderingControl/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:SetRelativeVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
             <InstanceID>0</InstanceID>
             <Channel>Master</Channel>
             <Adjustment>''' + str(incvol) +'''</Adjustment>
          </u:SetRelativeVolume>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:RenderingControl:1#SetRelativeVolume"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

def sendsetvolume(self, ip, setvol):
    path = "/MediaRenderer/RenderingControl/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
       <u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
          <InstanceID>0</InstanceID>
          <Channel>Master</Channel>
          <DesiredVolume>''' + str(setvol) +'''</DesiredVolume>
       </u:SetVolume>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:RenderingControl:1#SetVolume"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

def Seek(self, ip, unit, target):
    print "sending Seek..."
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Seek xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
             <Unit>''' + unit + '''</Unit>
             <Target>''' + target + '''</Target>
          </u:Seek>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Seek"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)


def sendplay(self, ip):
    print "sending Play..."
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
             <Speed>1</Speed>
          </u:Play>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Play"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)

def sendpause(self, ip):
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:Pause>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Pause"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)    
    
def sendstop(self, ip):
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Stop xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:Stop>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Stop"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)    

def sendnext(self, ip):
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Next xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:Next>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Next"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)    

def sendprevious(self, ip):
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:Previous xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:Previous>
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#Previous"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)    
   
   
def getzonegrouptopology(self, ip):
    xml=""
    print "requsting group info..."
    path = "/ZoneGroupTopology/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:GetZoneGroupState xmlns:u="urn:schemas-upnp-org:service:ZoneGroupTopology:1" />
       </s:Body>
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:ZoneGroupTopology:1#GetZoneGroupState"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xml = res.read()
    return xml

def GetTransportInfo(self, ip):
    CurrentTransportState = ""
    print "getting Transport Info.."
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:GetTransportInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:GetTransportInfo>
       </s:Body>    
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#GetTransportInfo"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xml = res.read()
    dom = parseString(xml)
    #print xml
    CurrentTransportState = dom.getElementsByTagName('CurrentTransportState')[0].childNodes[0].nodeValue
    return CurrentTransportState    

def GetPositionInfo(self, ip):
    positionInfo = {}
    print "getting PositionInfo.."
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:GetPositionInfo>
       </s:Body>    
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xml = res.read()
    dom = parseString(xml)
    #print xml
    positionInfo['track'] = dom.getElementsByTagName('Track')[0].childNodes[0].nodeValue
    positionInfo['trackuri'] = dom.getElementsByTagName('TrackURI')[0].childNodes[0].nodeValue
    positionInfo['trackmetadata'] = dom.getElementsByTagName('TrackMetaData')[0].childNodes[0].nodeValue
    positionInfo['reltime'] = dom.getElementsByTagName('RelTime')[0].childNodes[0].nodeValue
    return positionInfo
    
def getmediainfo(self, ip):
    MediaInfo = {}
    print "getting MediaInfo.."
    path = "/MediaRenderer/AVTransport/Control HTTP/1.1"
    host = ip
    port = 1400
    hostport = host + ":" + str(port)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Body>
          <u:GetMediaInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
             <InstanceID>0</InstanceID>
          </u:GetMediaInfo>
       </s:Body>    
    </s:Envelope>'''
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", path, body=xml, headers = {
        "Host": hostport,
        "SOAPACTION": '''"urn:schemas-upnp-org:service:AVTransport:1#GetMediaInfo"''',
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(xml)
    })
    res = conn.getresponse()
    connerror(self, res.status, res.reason)
    xml = res.read()
    dom = parseString(xml)
    #print xml
    MediaInfo['uri'] = dom.getElementsByTagName('CurrentURI')[0].childNodes[0].nodeValue
    try:# if metadata is empty, the line below fails, so made an exception
        MediaInfo['urimetadata'] = dom.getElementsByTagName('CurrentURIMetaData')[0].childNodes[0].nodeValue
    except:
        MediaInfo['urimetadata'] = ""
    MediaInfo['nrtracks'] = dom.getElementsByTagName('NrTracks')[0].childNodes[0].nodeValue
    return MediaInfo

def getcoordinator(self, ip, uuid):
    uri = getmediainfo(self, ip)['uri']
    if uri.find("x-rincon:RINCON_") == 0:
        coordinator = uri.split(":")[1]
        print "coordinator of " + uuid + "is " + coordinator
    else:
        coordinator = uuid
        #print "current zp is coordinator"
    return coordinator
    
def searchforsonos(self):
    try:
        zpInfo = {}
        s = socket(AF_INET, SOCK_DGRAM)
        s.settimeout(2)#very important if useing while loop to receive all responses,if this is removed, loop occurs
        s.bind(('', 5001))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        data = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 3\r\nST: urn:schemas-upnp-org:device:ZonePlayer:1\r\n\r\n'
        s.sendto(data, ('239.255.255.250', 1900))
        print "Searching for SONOS ZonePlayers on network..."
        time.sleep(1)
        #if i do a full search, i can get the zp type it's the only thing in ( )
        data, srv_sock = s.recvfrom(65565) #only need to catch one ZP response, will get rest from zonegrouptopology
        #while True:#look until timeout # this is to capture all responses
        #    data, srv_sock = s.recvfrom(65565)              
        #    if not data: break
        #    srv_addr = srv_sock[0]
        #    usn_id = ""
        #    print "USN: %s IP: %s" % (usn_id, srv_addr)
        s.close
        #print "MSEARCH socket closed"
        xmlstring = getzonegrouptopology(self, srv_sock[0])
        #for some reason the encoding isn't working, need to figure this out, for now this works
        xmlstring = xmlstring.replace('&gt;',">").replace('&lt;',"<").replace('&quot;','"')
        #print xmlstring
        xml = parseString(xmlstring)
        grouplist = xml.getElementsByTagName('ZoneGroup')
        print "SONOS ZonePlayers found:"
        for zg in grouplist:
            #print zg.attributes['Coordinator'].value
            coordinator = zg.attributes['Coordinator'].value
            zplist = zg.getElementsByTagName('ZoneGroupMember')
            for zp in zplist:
                #print "" + zp.attributes['UUID'].value
                #print "   " + zp.attributes['Location'].value.split("/")[2].split(":")[0]
                #print "   Coordinator - " + coordinator
                attrlist = dict(zp.attributes.items())
                #for attr, value in attrlist:
                #    print "     " + attr + "= " + value
                #print attrlist['UUID'] + " (" + attrlist['ZoneName'] + ") " + attrlist['Location'].split("/")[2].split(":")[0]
                #print "     coordinator: " + coordinator
                uuid = attrlist['UUID']
                if uuid not in zpInfo:
                    zpInfo[uuid] = {}
                zpInfo[uuid]['ip'] = attrlist['Location'].split("/")[2].split(":")[0]
                #zpInfo[uuid]['coordinator'] = coordinator
                zpInfo[uuid]['name'] = attrlist['ZoneName']
                if "Invisible" in attrlist:
                    #print "    " + "ZP is invisible"
                    zpInfo[uuid]['invisible'] = 1
                    print '{0: <27}'.format(uuid) + '{0: <17}'.format(zpInfo[uuid]['ip']) + zpInfo[uuid]['name'] + " (Invisible)"
                else:
                    #print "    " + "ZP is visible"
                    zpInfo[uuid]['invisible'] = 0
                    #print uuid + " " + zpInfo[uuid]['ip'] + "  " + zpInfo[uuid]['name']
                    print '{0: <27}'.format(uuid) + '{0: <17}'.format(zpInfo[uuid]['ip']) + zpInfo[uuid]['name']
                #if uuid == zpInfo[uuid]['coordinator']:
                #    print "    Coordinator"
                #else:
                #    print "    Slave"
        return zpInfo
                
    except Exception, e:
        print "error occurred"
        print e
    
###################################### Plugin Base #########################################
class Sonos(eg.PluginBase):

        
########## Config box
    #def Configure(self, ZP_l={}):
    #    IPinput = "Insert the IP of the Sonos device you want to control."
    #    panel = eg.ConfigPanel()
    #    IPLabel = wx.StaticText(panel, -1, IPinput)
    #    textControl = wx.TextCtrl(panel, -1, IP, size=(200, -1))
    #    panel.sizer.Add(IPLabel,0,wx.TOP,15)
    #    panel.sizer.Add(textControl, 0, wx.TOP,1)
    #    while panel.Affirmed():
    #        panel.SetResult(textControl.GetValue())

########## init self
    def __init__(self):
        print "initializing SONOS plugin..."
        self.AddActionsFromList(ACTIONS
        )

########## start self       
    def __start__(self):
        print "SONOS plugin starting..."
        global zpList
        zpList = searchforsonos(self)
        if not zpList:  #if nothing found, try one more time. 
            zpList = searchforsonos(self)
        

################################################ Actions ########################################

class SearchForSonosZPs(eg.ActionBase):
    name = "SearchForSonosZPs"
    description = "Search for SONOS equipment on the network, use to refresh list."

    def __call__(self):
        global zpList
        zpList = searchforsonos(self)

class Play(eg.ActionBase):
    name = "Send SONOS PLay"
    description = "sends the play command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid, zp_name):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        #print "sending Play..."
        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendplay(self, zpList[coordinator]['ip'])
        print "sent PLAY to ", zpList[coordinator]['name'] #host
       
    def Configure(self, uuid="", zp_name=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...", (12,15), (100,20))
        
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)

        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        #print ZPDropDown.GetCurrentSelection()
        while panel.Affirmed():
            #FinalChoice = ZPDropDown.GetCurrentSelection()
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0]
            )

class Pause(eg.ActionBase):
    name = "Send SONOS Pause"
    description = "sends the pause command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid, zp_name):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        print "sending Pause..."
        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendpause(self, zpList[coordinator]['ip'])
        print "sent Pause to ", zpList[coordinator]['name'] #host
       
    def Configure(self, uuid="", zp_name=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...", (12,15), (100,20))
        
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)

        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        #print ZPDropDown.GetCurrentSelection()
        while panel.Affirmed():
            #FinalChoice = ZPDropDown.GetCurrentSelection()
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0]
            )

class Stop(eg.ActionBase):
    name = "Send SONOS Stop"
    description = "sends the stop command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid, zp_name):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        #print "sending stop..."
        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendstop(self, zpList[coordinator]['ip'])
        print "sent STOP to ", zpList[coordinator]['name'] #host
       
    def Configure(self, uuid="", zp_name=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...", (12,15), (100,20))
        
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)

        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        #print ZPDropDown.GetCurrentSelection()
        while panel.Affirmed():
            #FinalChoice = ZPDropDown.GetCurrentSelection()
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0]
            )

class Next(eg.ActionBase):
    name = "Send SONOS Next"
    description = "sends the next command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid, zp_name):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        #print "sending Next..."
        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendnext(self, zpList[coordinator]['ip'])
        print "sent Next to ", zpList[coordinator]['name'] #host
       
    def Configure(self, uuid="", zp_name=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...", (12,15), (100,20))
        
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)

        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        #print ZPDropDown.GetCurrentSelection()
        while panel.Affirmed():
            #FinalChoice = ZPDropDown.GetCurrentSelection()
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0]
            )

class Previous(eg.ActionBase):
    name = "Send SONOS Previous"
    description = "sends the Previous command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid, zp_name):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        #print "sending Previous..."
        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendprevious(self, zpList[coordinator]['ip'])
        print "sent Previous to ", zpList[coordinator]['name'] #host
       
    def Configure(self, uuid="", zp_name=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...", (12,15), (100,20))
        
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)

        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        #print ZPDropDown.GetCurrentSelection()
        while panel.Affirmed():
            #FinalChoice = ZPDropDown.GetCurrentSelection()
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0]
            )

class VolumeAdjust(eg.ActionBase):
    name = "Send SONOS VolumeAdjust"
    description = "sends relative volume adjustment command. "

    def __call__(self, uuid, zp_name, incvol):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        #print "sending relative Volume adjustment..."
        sendrelvolume(self, zpList[uuid]['ip'], incvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        print "adjusted volume by " + str(incvol) + " in " + zpList[uuid]['name']
        
       
    def Configure(self, uuid="", zp_name="", incvol="3"):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
        TextVolSelect = wx.StaticText(panel, -1, '''Select incremental percentage to adjust volume\nrelative to current value.\nVol. Up def.= 3\nVol. Dwn def.= -3''')
        TextVolNote = wx.StaticText(panel, -1, " - Select positive number to adjust volume up\n - Select negative to adjust volume down.\n")
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        try:
            VolDropDown = wx.SpinCtrl(panel, -1, incvol, (0,0), (100,20))
            VolDropDown.SetRange(-10,10)
        except:
            VolDropDown = wx.SpinCtrl(panel, -1, '3', (0,0), (100,20))
            VolDropDown.SetRange(-10,10)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), (1,2), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextVolSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextVolNote, (4,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(VolDropDown, (3,1), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            #FinalVol = VolDropDown.GetStringSelection()
            FinalVol = VolDropDown.GetValue()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0],
                str(FinalVol)
                
            )

class VolumeSet(eg.ActionBase):
    name = "Send SONOS VolumeSet"
    description = "sends command to set volume to specific value. "

    def __call__(self, uuid="", zp_name="", setvol=""):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        if uuid == "" :
            print "**please configure action**"
            return
        sendsetvolume(self, zpList[uuid]['ip'], setvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. 
        print "set volume to "+ str(setvol) + " in " + zpList[uuid]['name']
       
    def Configure(self, uuid="", zp_name="", setvol="20"):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(1)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
        TextVolSelect = wx.StaticText(panel, -1, '''Select Volume level (0-100%):  ''')
        TextVolNote = wx.StaticText(panel, -1, "")
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
               
        try:
            VolDropDown = wx.SpinCtrl(panel, -1, setvol, (0,0), (100,20))
            VolDropDown.SetRange(0,100)
        except:
            VolDropDown = wx.SpinCtrl(panel, -1, '20', (0,0), (100,20))
            VolDropDown.SetRange(0,100)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), (1,2), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextVolSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextVolNote, (4,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(VolDropDown, (3,1), flag = (wx.ALIGN_TOP | wx.ALIGN_RIGHT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            #FinalVol = VolDropDown.GetStringSelection()
            FinalVol = VolDropDown.GetValue()
            panel.SetResult(
                #FinalChoice,
                #zpList[FinalChoice]['name']
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0],
                str(FinalVol)
                
            )

class StartPlayList(eg.ActionBase):
    name = "StartPlayList"
    description = "starts playing specific playlist or station on the selected Zone Player"

    def __call__(self, uuid="", zp_name="", title="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        print "starting playlist: " + dscr + " - " + title + " in " + zpList[uuid]['name']
        #print dscr + " - " + title
        #print "   " + uri
        #print "   " + urimetadata
        #print "   " + upnpclass
        #print "   " + str(isplaylist)

        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        if isplaylist:
            RemoveAllTracksFromQueue(self, zpList[coordinator]['ip'])
            AddURIToQueue(self, zpList[coordinator]['ip'], uri, urimetadata)
            SetAVTransportURI(self, zpList[coordinator]['ip'], "x-rincon-queue:"+coordinator+"#0", "")
        else:
            SetAVTransportURI(self, zpList[coordinator]['ip'], uri, urimetadata)
        sendplay(self, zpList[coordinator]['ip'])

       
    def Configure(self, uuid="", zp_name="", title="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(5, 1)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
        TextPLSelect = wx.StaticText(panel, -1, "Select a Playlist or Station from your SONOS Favorites list...")
        TextPLNote = wx.StaticText(panel, -1, '''Make sure to add any station you want to select to the SONOS favorites list before opening this dialogue.\nAlso note when the action is triggered, if it's a playlist it will replace the current queue''')
        #============ dropdown ==============
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        
        #get SONOS Favorites...(make sure not to select a bridge by ignoring invisible zps)
        for k, v in zpList.iteritems():
                if v['invisible'] == 0: #find the first non invisible ZP
                    tempuuid = k
                    break
        print "Getting Favorites List from %s at %s" % (zpList[tempuuid]['name'],zpList[tempuuid]['ip'])
        presets = getfavlist(self, zpList[tempuuid]['ip'])
        #============ dropdown ==============
        ChoiceList = []
        for k, v in presets.iteritems():
            ChoiceList.append(v['description'] + ": " + k)
        PLDropDown =  wx.Choice(panel, -1, choices=ChoiceList) # (0,0), (60,20)
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(dscr + ": " + title)
            PLDropDown.SetSelection(p)
        except: #ValueError:
            PLDropDown.SetSelection(0)
        #============ end dropdown ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPLSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(TextPLNote, (3,0), flag = wx.EXPAND)
        mySizer.Add(PLDropDown, (4,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalPL = PLDropDown.GetStringSelection().split(": ")[1]
            panel.SetResult(
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0],
                FinalPL,
                presets[FinalPL]['description'],
                presets[FinalPL]['uri'],
                presets[FinalPL]['urimetadata'],
                presets[FinalPL]['upnpclass'],
                presets[FinalPL]['isplaylist']                
            )
            
class SetPlayMode(eg.ActionBase):
    name = "SetPlayMode"
    description = "sets play mode to normal, shuffle, shuffle w/ no repeat, or repeat all "

    def __call__(self, uuid="", zp_name="", playmode=""):
        if uuid not in zpList:
            print "!!! zone player no longer in zpList (not found on network) !!!"
        print "set playmode to " + playmode + " in " + zpList[uuid]['name']

        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
        sendSetPlayMode(self, zpList[coordinator]['ip'], playmode)

       
    def Configure(self, uuid="", zp_name="", playmode=""):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        
        TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
        TextPMSelect = wx.StaticText(panel, -1, "Select Play Mode.")
        TextPMNote = wx.StaticText(panel, -1, "NOTE: Streaming stations like Pandora don't support PlayMode.\n\tFor this reason if this is sent while listening\n\tto streaming station, it will return a 500 error.")
        #============ dropdown ==============
        ChoiceList = []
        if zpList:
            for k, v in zpList.iteritems():
                if v['invisible'] == 0:
                    ChoiceList.append(v['name'] + "-" + k + "-" + v['ip'])
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(zpList[uuid]['name'] + "-" + uuid + "-" + zpList[uuid]['ip'])
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        
        #============ dropdown ==============
        ChoiceList = ["NORMAL", "REPEAT_ALL", "SHUFFLE_NOREPEAT", "SHUFFLE"]
        PMDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(playmode)
            PMDropDown.SetSelection(p)
        except: #ValueError:
            PMDropDown.SetSelection(0)
        #============ end dropdown ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPMSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(PMDropDown, (3,0), flag = (wx.ALIGN_TOP | wx.ALIGN_LEFT))
        mySizer.Add(TextPMNote, (4,0), flag = (wx.ALIGN_BOTTOM | wx.ALIGN_LEFT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalPM = PMDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[1], #save only the uuid from the list.
                FinalChoice.split("-")[0],
                FinalPM                
            )

#class WhatstheWeather(eg.ActionBase):
#    name = "WhatstheWeather"
#    description = "Gets the current weather conditions from Yahoo and uses text to speech to play it over the SONOS system"
#    
#    def SetAVTransportURIPlay(self, ip, uri, urimetadata="", trnum="", trtime="", playing=""):
#        SetAVTransportURI(self, ip, uri, urimetadata)
#        if trnum != "":
#           Seek(self, ip, "TRACK_NR", trnum)
#           Seek(self, ip, "REL_TIME", trtime)
#        if playing: #if music was playing, start music again. 
#            sendplay(self, ip)
#        
#    #need zp to send notifications too (check boxes)(currently supporting one zp)
#    #         will need to make list and have it loop through the list for all ZP selected
#    #need Aux input to use
#    #need delay for text to speech
#    #need speech variables
#    #need string 
#    def __call__(self, uuid="", zip="92081"):
#        trtime = ""
#        trnum = ""
#        playing = False
#        conditions = getweatherforcast(self, zip)
#        current = u".It is currently " + conditions['text'] + " and " + conditions['temp'] + " degrees outside."
#        today = u".Today will be " + conditions['todaystext'] + " with a high of " + conditions['todayshigh'] + " and a low of " + conditions['todayslow']
#        print current
#        print today
#
#        uuid = "RINCON_000E58D9A55E01400"
#        auxUID = "RINCON_000E58A3465201400"
#        coordinator = getcoordinator(self, zpList[uuid]['ip'], uuid)
#        mediainfo = getmediainfo(self, zpList[coordinator]['ip'])
#        uri = mediainfo['uri']
#        currentTransportState = GetTransportInfo(self, zpList[coordinator]['ip']) #need to see if zp is currently playing ("CurrentTransportState" = "PLAYING")
#        if currentTransportState == "PLAYING":
#            playing = True
#        if uri.find("x-rincon-queue:") == 0:#is it playing from the queue?
#            #playing from the queue
#            print "playing from queue"
#            positionInfo = GetPositionInfo(self, zpList[coordinator]['ip'])
#            trnum = positionInfo['track'] 
#            trtime = positionInfo['reltime']
#        SetAVTransportURI(self, zpList[coordinator]['ip'], "x-rincon-stream:"+auxUID, "")
#        sendplay(self, zpList[coordinator]['ip'])
#        eg.plugins.Speech.TextToSpeech(u'Microsoft Hazel Desktop - English (Great Britain)', 1, current, 0, 100)
#        eg.plugins.Speech.TextToSpeech(u'Microsoft Hazel Desktop - English (Great Britain)', 1, today, 0, 100)
#        #start playing SONOS after set time:
#        eg.globals.taskSonosPlay = eg.scheduler.AddTask(8.5, self.SetAVTransportURIPlay, zpList[coordinator]['ip'], uri, mediainfo['urimetadata'], trnum, trtime, playing) 
#      
        
########################################### Auto add Actions #####################################

ACTIONS = (
    (SearchForSonosZPs,"SearchForSonosZPs","SearchForSonosZPs","SearchForSonosZPs.", None),
    (Play,"Play","Play","Send Play to ZonePlayer.", None),
    (Pause,"Pause","Pause","Send Pause to ZonePlayer.", None),
    (Stop,"Stop","Stop","Send Stop to ZonePlayer.", None),
    (Next,"Next","Next","Send Next to ZonePlayer.", None),
    (Previous,"Previous","Previous","Send Previous to ZonePlayer.", None),
    (VolumeAdjust,"VolumeAdjust","VolumeAdjust","VolumeAdjust Sonos.", None),
    (VolumeSet,"VolumeSet","VolumeSet","VolumeSet Sonos.", None),
    (StartPlayList, "StartPlayList","StartPlayList","Start Playlist", None),
    (SetPlayMode, "SetPlayMode", "SetPlayMode", "Set Play Mode", None)
    #(WhatstheWeather, "WhatstheWeather", "WhatstheWeather", "Play current weather forecast over SONOS", None)
)