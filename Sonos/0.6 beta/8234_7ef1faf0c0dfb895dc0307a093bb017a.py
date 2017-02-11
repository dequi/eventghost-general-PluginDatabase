# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2014-2020 Chase Whitten <shocktherapysb10@gmail.com>
#
# No Code here on out within this file may be used accept with EventGhost.
# Permission by myself (Chase Whitten) must be granted by me to use this code
# or part of this code in any other program.
#
######################################## Register ############################################
eg.RegisterPlugin(
    name = "Sonos",
    author = "Chase Whitten (Techoguy)",
    version = "0.6 beta",
    kind = "program",
    canMultiLoad = False,
    description = "This plugin allows you to control your SONOS zone players. This works with grouped zones or stereo pairs. This plugin will search your network for Zone Players during startup, and if any SONOS ZP is added or removed from the network the plugin will automatically update itself. Each ZP is unique based on the MAC address. This means even if the name of a ZP is changed it won't affect your actions. If you have to replace a ZP, then all actions that use that ZP will have to be updated. Many more comands will be added soon.",
    createMacrosOnAdd = True
    #createMacrosOnAdd = False    
)
###################################### Import ###############################################
import eg
from xml.dom.minidom import parse, parseString
import httplib
import wx.lib
#from socket import *
import time
import asyncore, socket
from xml.dom.minidom import parse, parseString
import os
import linecache # for PrintException()
import sys # for PrintException()
if os.name != "nt":
    import fcntl
    import struct
#for debugging and knowing which functions called another
import inspect

###################################### Globals ############################################### 
globalZPList = {} #dict to store ZP objects.
globalServiceList = {} #dict to store service/subscription objects
localip = ""
globalDebug = 0
###################################### Functions #############################################

### example of calling the speech plugin: eg.plugins.Speech.TextToSpeech(u'Microsoft Hazel Desktop - English (Great Britain)', 1, u'Today is a beutiful day. the temperature is 87 degrees outside at {TIME} ', 0, 100)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    #filename = f.f_code.co_filename
    #linecache.checkcache(filename)
    #line = linecache.getline(filename, lineno, f.f_globals)
    #print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print 'EXCEPTION AT LINE: %s = %s' % (lineno, exc_obj)

    
def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def HtmlSplit(data=""):
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

    
class AsyncRequesting(asyncore.dispatcher):    
    
    def __init__(self, HOSTzp, PORTzp, data, callback):
        self.HOSTzp = HOSTzp
        self.PORTzp = PORTzp
        self.data = data
        self.contentLength = 0
        self.connectionClose = ''
        self.callback = callback
        self.start_connection()
        
    def start_connection(self):
        self.connectionMade = "NO"
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect((self.HOSTzp, self.PORTzp))
            self.portused = self.getsockname()[1]
        except socket.error, e:
            print "Connection to %s on port %s failed: %s" % (self.HOSTzp, self.PORTzp, e)
        self.buffer = self.data
        
    def handle_connect(self):
        if globalDebug >= 2:
            print "%s handle_connect" % self.portused
        self.connectionMade = "CONNECTED"
        pass

    def handle_close(self):
        if globalDebug >= 2:
            print str(self.portused) + " -- CLOSED handle close, %s" % self.connectionMade
        if self.connectionMade == "CONNECTED": #connection made but then closed, so retry.
            self.close() #close current socket, 
            if globalDebug >= 1:
                print "%s socket closed before reading, RETRYING connection" % self.portused
            self.start_connection() #retry sending.
        elif self.connectionMade == "READ":
            self.close()
        else: #everything else and "NO"
            if globalDebug >= 1:
                print "No response from %s:%s" % (self.HOSTzp, self.PORTzp)
            self.close()
            data = "No Response from %s:%s" % (self.HOSTzp, self.PORTzp)
            response = {'body':"",'ERROR':data}
            self.callback(response)

    def handle_read(self):
        if globalDebug >= 2:
            print "%s handle_read" % self.portused
        self.connectionMade = "READ"
        data = self.recv(1024)
        if globalDebug >= 2:
            print "%s-Data:\r\n%s\r\n------" % (self.portused, data)        
        try:
            self.response #if it doesn't exist, it's the first read
            if data != '':
                self.response['body'] = self.response['body'] + data
                if self.contentLength <= len(self.response['body']):
                    if self.connectionClose == 'close':
                        self.close()
                    self.callback(self.response)
            else: # data empty before content length reached
               print "%s Response ERROR: Connection closed before reaching content length " % self.portused
               print "%s Current-Length:%s  SB: %s \n%s" % (self.portused,len(self.response['body']), self.contentLength, self.response)
               self.callback(self.response)
        except AttributeError: #if first read
            self.response = HtmlSplit(data)
            if data != '':
                try:
                    self.contentLength = int(self.response['CONTENT-LENGTH'])
                except:
                    self.contentLength = 0
                try:
                    self.connectionClose = self.response['Connection']
                except:
                    self.connectionClose = ''
                if self.contentLength <= len(self.response['body']):
                    if self.connectionClose == 'close':
                        self.close()
                    self.callback(self.response)
            else:
                if globalDebug >= 1:
                    print "%s ---- Response empty ----- " % self.portused
                self.callback(self.response)
               
    def writable(self):
        if globalDebug >= 2:
            print "writable"
        return (len(self.buffer) > 0)

    def handle_write(self):
        if globalDebug >= 2:
            print "%s handle_write" % self.portused
        try:
            sent = self.send(self.buffer)
        except:
            sent = self.send(self.buffer.encode("utf-8"))
        self.buffer = self.buffer[sent:]

    def handle_expt(self):
        print "handle_expt : %s:%s" % (self.HOSTzp, self.PORTzp)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, AsyncRequesting: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_error(self):
        print "handle_error : %s:%s" % (self.HOSTzp, self.PORTzp)
        try:
            self.close()
        except:
            pass
        PrintException()
        raise #Exception("ERROR, AsyncRequesting: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_connect_expt(self,expt):
        print "connection error: %s \r\n..... %s:%s" % (expt,self.HOSTzp, self.PORTzp)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, AsyncRequesting: %s:%s" % (self.HOSTzp, self.PORTzp))


class Service():

    def __init__(self, zp, url, EventCallBack, eventport):
        self.zp = zp
        self.url = url
        self.EventCallBack = EventCallBack
        self.eventport = eventport
        self.subsTimeout = 3600
        self.Subscribe()

    def ServiceErrorHandler(self, data):
        if "ERROR" in data.keys():
            if data['ERROR'].find("No Response") >= 0:
                self.UnsubResponse(data)
                del globalZPList[self.zp.uuid] #delete zp from list
                #trigger eg event....
                if globalDebug >= 1:
                    print "deleted ZP from List: %s" % self.zp.uuid
                trigger = "%s.%s" % (self.zp.uuid, "DELETED")
                eg.TriggerEvent(trigger, prefix='SONOS', payload=self.zp.uuid.name)
                if self.url.find("ZoneGroupTopology")>0: #if true, subscribe to a different ZP.
                    try:
                        uuid = globalZPList.keys()[0] #select random ZP to get grouptopology from
                        tempservice = Service(globalZPList[uuid], "/ZoneGroupTopology/Event",               ZoneGroupTopologyEvent)             
                    except:#if there are no more ZPs, through error
                        raise Exception("ERROR: Can't connect to SONOS Zone Players")
            else: #unhandled error
                raise Exception(data['ERROR'])
        return data 
    
    def RenewResponse(self, data):
        #might not need. 
        #store timeout 
        #schedule, renew function call
        #remember to store this so it can be cancelled later. 
        if globalDebug >= 1:
            print "renew Response received..."
        pass
    
    def Renew(self):
        if globalDebug >= 1:
            print "sending renew request...."
        port = 1400
        data = "SUBSCRIBE " + self.url + " HTTP/1.1\r\nSID: " + self.SID + "\r\nTIMEOUT: Second-"+str(self.subsTimeout)+"\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nContent-Length: 0\r\n\r\n"
        self.renrequest = AsyncRequesting(self.zp.ip, port, data, self.SubResponse)
        #restart loop to include the new socket object
        # this is needed because this is created after the first call to RestartAsyncore
        eg.RestartAsyncore() 
        if globalDebug >= 1:
            print "*************************************"
            print "%s renew request sent" % globalZPList[self.zp.uuid].name
            print "*************************************"
    
    def UnsubResponse(self, data):
        # Unsubscribe response
        # check to make sure 200 OK is recieved 
        # trigger eg event....
        #HTTP/1.1 200 OK
        #Server: Linux UPnP/1.0 Sonos/24.0-71060 (ZP120)
        #Connection: close
        global globalServiceList
        global globalZPList
        if globalDebug >= 2:
            print "%s Unsubscribed response %s - %s" % (self.unsubrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        del globalServiceList[self.SID]
        globalZPList[self.zp.uuid].services[self.url.split("/")[-2]] = ""
        if globalDebug >= 2:
            print "UnsubResponse Data: %s" % data
        try:
            self.unsubrequest.close()
        except Exception, e:
            print " Service Unsubscribe Response Error: %s" % e
            PrintException()
        
    def Unsubscribe(self):
        #cancel the scheduled task for the renew
        #send cancel request
        if globalDebug >= 2:
            print "sending unsubscribe request to %s" % (self.zp.ip)
        try:
            eg.scheduler.CancelTask(self.renewCallBack) # cancel renew callback
        except Exception, e:
            if globalDebug >= 2:
                print "can't Cancel Task renewCallBack in Unsubscribed %s" % str(e)
            pass
        try:
            self.renrequest.close()
        except Exception, e:
            pass
        try:
            self.subrequest.close()
        except Exception, e:
            pass
        try:
            self.unsubrequest.close()
        except Exception, e:
            pass
        port = 1400
        data = "UNSUBSCRIBE " + self.url + " HTTP/1.1\r\nUSER-AGENT: Linux UPnP/1.0 Sonos/24.0-69180m (WDCR:Microsoft Windows NT 6.2.9200.0)\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nSID: " + self.SID + "\r\n\r\n"
        if globalDebug >= 2:
            print "sending unsubscribe request: %s - %s" % (globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        self.unsubrequest = AsyncRequesting(self.zp.ip, port, data, self.UnsubResponse)      
    
    def SubResponse(self, data):
        global globalServiceList
        global globalZPList
        #print "subscribe response: %s - %s" % (globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        try:
            response = self.ServiceErrorHandler(data)
            try:
                eg.scheduler.CancelTask(self.renewCallBack)#restart if needed.
            except:
                pass
            self.subsTimeout = int(response['TIMEOUT'].split("-")[1]) #ex: TIMEOUT: Seconds-3200
            if globalDebug >= 2:
                print response['SID']
            self.SID = response['SID']
            globalServiceList[self.SID] = self # store service object in global dict
            # store SID info in ZP object
            globalZPList[self.zp.uuid].services[self.url.split("/")[-2]] = self.SID  
            if globalZPList[self.zp.uuid].name == "":
                globalZPList[self.zp.uuid].name = self.zp.ip
            if globalDebug >= 2:
                print "Subscribed to %s on %s" % (self.url.split("/")[-2],globalZPList[self.zp.uuid].name)
            if globalDebug >= 2:
                print "%s subscribed response %s - %s" % (self.subrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
            self.renewCallBack = eg.scheduler.AddTask(self.subsTimeout/2, self.Renew)
        except Exception, e:
            print " Service Subscribe Response Error: %s" % e
            PrintException()
        
    def Subscribe(self):
        global globalZPList
        port = 1400
        data = "SUBSCRIBE " + self.url + " HTTP/1.1\r\nNT: upnp:event\r\nTIMEOUT: Second-"+str(self.subsTimeout)+"\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nCALLBACK: <http://" + localip + ":" + str(self.eventport) + "/events>\r\nContent-Length: 0\r\n\r\n"
        self.subrequest = AsyncRequesting(self.zp.ip, port, data, self.SubResponse)
        if globalZPList[self.zp.uuid].name == "":
            globalZPList[self.zp.uuid].name = self.zp.ip
        if globalDebug >= 2:
            print "%s sending subscribe request: %s - %s" % (self.subrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
    
    def Event(self, data):
        #define how the event response is handled, unique for each service
        self.EventCallBack(self.zp.uuid, data)

              
def UpdateTransportStates(uuid, transportstate):
    #updated all Zone Players within a group.
    for key in globalZPList:
        if not globalZPList[key].invisible:
            if globalZPList[key].coordinator == uuid:
                globalZPList[key].TransportState(transportstate)
        
        
def AVTransportEvent(uuid, data):
    global globalZPList
    try:
        #print "AVTransportEvent received from %s" % globalZPList[uuid].name
        xml = parseString(data)
        xmlLastChange = xml.getElementsByTagName('LastChange')[0].firstChild.nodeValue
        xml = parseString(xmlLastChange.encode('utf-8'))    
        if globalDebug >= 2:
            print xml.toxml()
        transportstate = xml.getElementsByTagName("TransportState")[0].attributes['val'].value
        #check to see if avTransportURI exists, if it doesn't update transportstate (only occurs when starting)
        try:
            globalZPList[uuid].avTransportURI
        except:
            UpdateTransportStates(uuid, transportstate)
            
        try:
            globalZPList[uuid].avTransportURI = xml.getElementsByTagName("AVTransportURI")[0].attributes['val'].value
            if globalDebug >= 1:
                print "%s AVTransportURI: %s" % (globalZPList[uuid].name, globalZPList[uuid].avTransportURI)
        except: 
            #if AVTransportURI is present, this means the stream is updating so transportstate 'STOPPED' should be ignored.
            UpdateTransportStates(uuid, transportstate)
        try:
            globalZPList[uuid].currentPlayMode = xml.getElementsByTagName("CurrentPlayMode")[0].attributes['val'].value
            if globalDebug >= 1:
                print "%s currentPlayMode: %s" % (globalZPList[uuid].name, globalZPList[uuid].currentPlayMode)
        except: pass
        try:
            globalZPList[uuid].playbackStorageMedium = xml.getElementsByTagName("PlaybackStorageMedium")[0].attributes['val'].value
            if globalDebug >= 1:
                print "%s playbackStorageMedium: %s" % (globalZPList[uuid].name, globalZPList[uuid].playbackStorageMedium)
        except: pass
        
        #AVTransportURIMetaData (streaming station info)
        try:
            avtransportURIMetaData = xml.getElementsByTagName("AVTransportURIMetaData")[0].attributes['val'].value
            if avtransportURIMetaData == "":
                if globalDebug >= 1:
                    print "%s avtransportURIMetaData: <empty>" % globalZPList[uuid].name
            else:
                tempxml = parseString(avtransportURIMetaData)
                #print tempxml.toxml()
                title = tempxml.getElementsByTagName("dc:title")[0].firstChild.nodeValue 
                if globalDebug >= 1:
                    print "%s Stream Title: %s" % (globalZPList[uuid].name, title)
        except Exception, e:
            if globalDebug >= 2:
                print "failed %s" % str(e)
            
        #CurrentTrackMetaData information (sub xml)
        try:
            currenttrackmetadata = xml.getElementsByTagName("CurrentTrackMetaData")[0].attributes['val'].value
            tempxml = parseString(currenttrackmetadata.encode('utf-8'))
            #print tempxml.toxml()
            albumartlink = tempxml.getElementsByTagName("upnp:albumArtURI")[0].firstChild.nodeValue 
            #print "http://" + globalZPList[uuid].ip + ":1400" + albumartlink
            #to get high resolution pics: 
            #http://www.albumartexchange.com/covers.php?sort=7&q=Scary+Monsters+and+Nice&fltr=2&bgc=&page=&sng=1
            #this returns: html, which has a <a href="/gallery/images/public/..." taht has the picture. 
            #if it can't find anything it response with "There are no images to display."  
        except Exception, e:
            if globalDebug >= 2:
                print "failed %s" % str(e)
            pass
        try:
            title = tempxml.getElementsByTagName("dc:title")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Track: " + title
        except:
            pass
        try:
            artist = tempxml.getElementsByTagName("dc:creator")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Artist: " + artist
        except:
            pass
        try:
            album = tempxml.getElementsByTagName("upnp:album")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Album: " + album
            #high resolution artwork search based on alum name:
            album = album.replace(" ","+")
            #print "http://www.albumartexchange.com/covers.php?sort=7&q=" + album + "&fltr=2&bgc=&page=&sng=1"
        except:
            pass
    except Exception, e:
        print "XML error: %s" % e
        
        
def ZoneGroupTopologyEvent(uuid, data):
    global globalZPList
    try:
        #print data
        xml = parseString(data)
        xmlstring = xml.getElementsByTagName('ZoneGroupState')[0].firstChild.nodeValue
        #print xmlstring
        xml = parseString(xmlstring)
        grouplist = xml.getElementsByTagName('ZoneGroup')
        #print grouplist
        #loop through group info and update zpList
        zpInfo = {} #temp.
        subscribeList = []
        unsubscribeList = []
        for zg in grouplist:
            #print zg.attributes['Coordinator'].value
            coordinator = zg.attributes['Coordinator'].value
            zplist = zg.getElementsByTagName('ZoneGroupMember')
            for zp in zplist:
                attrlist = dict(zp.attributes.items())
                uuid = attrlist['UUID']
                #add ZP to dict if new
                ip = attrlist['Location'].split("/")[2].split(":")[0]
                xmllocation = attrlist['Location']
                if uuid not in globalZPList:
                    globalZPList[uuid] = ZonePlayer(uuid, ip, xmllocation)
                #globalZPList[uuid].uuid = uuid
                globalZPList[uuid].ip = ip
                globalZPList[uuid].name = attrlist['ZoneName']
                globalZPList[uuid].coordinator = coordinator
                #subscribe to AVTransport (all that are coordinators)
                if coordinator == uuid: #if true, ZP is coordinator 
                    stringflagco = " :coordinator -%s-" % globalZPList[uuid].services["AVTransport"]
                    if globalZPList[uuid].services["AVTransport"] == "": # no SID
                        if globalDebug >= 2:
                            print "    Subscribing to %s" % globalZPList[uuid].name
                        subscribeList.append(uuid)
                    else:
                        pass
                        if globalDebug >= 2:
                            print "    AVTransport already subscribed to %s" % globalZPList[uuid].name
                else:
                    stringflagco = " -%s-" % globalZPList[uuid].services["AVTransport"]
                    if not globalZPList[uuid].services["AVTransport"] == "": #SID present
                        unsubscribeList.append(uuid)
                        if globalDebug >= 2:
                            print "    Unsubscribing to %s" % globalZPList[uuid].name
                        #globalServiceList[globalZPList[uuid].services["AVTransport"]].Unsubscribe()
                    else:
                        if globalDebug >= 2:
                            print "    AVTransport already unsubscribed to %s" % globalZPList[uuid].name
                if "Invisible" in attrlist:
                    globalZPList[uuid].invisible = 1
                    if globalDebug >= 1:
                        print '{0: <27}'.format(uuid) + '{0: <17}'.format(ip) + attrlist['ZoneName'] + " (Invisible)" + stringflagco
                else:
                    globalZPList[uuid].invisible = 0
                    if globalDebug >= 1:
                        print '{0: <27}'.format(uuid) + '{0: <17}'.format(ip) + attrlist['ZoneName'] + stringflagco
        for zp in subscribeList:
            if globalDebug >= 1:
                print "Subscribing to %s" % globalZPList[zp].name
            #globalZPList[zp].services["AVTransport"] = "testing"
            tempservice = Service(globalZPList[zp], "/MediaRenderer/AVTransport/Event", AVTransportEvent, serverPort)
        for zp in unsubscribeList:
            if globalDebug >= 1:
                print "Unsubscribing to %s" % globalZPList[zp].name
            #globalZPList[zp].services["AVTransport"] = ""
            globalServiceList[globalZPList[zp].services["AVTransport"]].Unsubscribe()
    except Exception, e:
        print "XML error: %s" % e


class EventChannel(asyncore.dispatcher):
    contentlength = 0
    eventdata = ""
    def handle_write(self):
        pass
    
    def handle_close(self):
        pass
        
    def handle_read(self):
        data = self.recv(8192)
        try:
            if self.contentlength == 0:
                self.eventdata = HtmlSplit(data)
                self.contentlength = int(self.eventdata['CONTENT-LENGTH'])
                if self.eventdata['NT'] != 'upnp:event': #check to make sure it's an event
                    raise Exception("ERROR, expected to receive event")
            else:
                self.eventdata['body'] = self.eventdata['body'] + data
            
            if self.contentlength <= len(self.eventdata['body']):
                self.send('HTTP/1.1 200 OK\r\nContent-Length: 0')
                self.close()
                #print self.eventdata['body']
                SID = self.eventdata['SID']
                if SID in globalServiceList:
                    servicename = globalServiceList[SID].url.split("/")[-2]
                    zpevent = globalZPList[globalServiceList[SID].zp.uuid].name
                    if globalDebug >= 1:
                        print "--- EVENT Received --- %s from %s" % (servicename, zpevent)
                    globalServiceList[SID].Event(self.eventdata['body'])
                self.contentlength = 0
                self.eventdata = ""
        except Exception, e:
            print "event receive error: %s - %s" % (Exception, e)
            #self.send('HTTP/1.1 500 Internal Server ERROR\r\nContent-Length: 0')
            self.close()

class EventServer(asyncore.dispatcher):

    def __init__(self, port=0):#leaving the port assigned to 0 will allow the OS to pick an available port. 
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        ''' other plugins place the RestartAsyncore here but it doesn't help me '''
        #eg.RestartAsyncore() #this used instead of asyncore.loop for EG.
        self.bind(("", self.port))
        self.port = self.getsockname()[1] #gets assigned port number
        self.listen(5)
        print "SONOS Event Server listening on port", self.port

    def handle_accept(self):
        channel, addr = self.accept()
        if globalDebug >= 2:
            print " connected to channel: " + str(channel)
        if globalDebug >= 2:
            print " connected to addr: " + str(addr)
        EventChannel(channel)

class ZonePlayer():
    household = ""
    COMMANDPORT = 1400
    def __init__(self, uuid, ip, xmllocation):
        if globalDebug >= 2:
            print "New ZonePlayer Added: %s : %s" % (uuid, ip)
        prename = "%s-%s" % (ip, uuid)
        eg.TriggerEvent("NewZonePlayerAdded", prefix='SONOS', payload=prename)
        self.uuid = uuid
        self.ip = ip
        self.xmllocation = xmllocation
        self.name = ""
        self.coordinator = uuid
        self.transportState = ""
        self.favPlayList = {}
        #services:
        services = {
                    'ZoneGroupTopology':"", #only one ZP 
                    'ContentDirectory':"", #none right now, otherwise all ZPs (bridge?)
                    'AVTransport':"", #Play etc. only the coordinators
                    'AlarmClock':"", #only one ZP
                    'RenderingControl':"" #vol etc. All ZPs except if invisible (sub, or stereo pair)
                    }
        self. services = services   
        
    def TransportState(self, transportstate):
        # Transport States from SONOS ZP (transportstate): 
        #    STOPPED, PAUSED_PLAYBACK, TRANSITIONING, PLAYING
        # Transport States for EG and Triggering Events (globalZPList[uuid].transportstate):
        #    Stopped, Playing
        # should only be called when AVTransportURI is present (updated) in AVTransport Event
        trigger = ""
        if globalDebug >= 1:
            print "%s Transport State: %s" % (self.name,transportstate)
        if self.transportState == "":
            if transportstate == "TRANSITIONING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "PAUSED_PLAYBACK":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "STOPPED":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "PLAYING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        elif self.transportState == "Playing":
            if transportstate == "PAUSED_PLAYBACK":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "STOPPED":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        elif self.transportState == "Stopped":
            if transportstate == "PLAYING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "TRANSITIONING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        if trigger != "":
            eg.TriggerEvent(trigger, prefix='SONOS', payload=self.name)
    
    #------------- Standard functions for commands -----------------------
    def CommandPacketForm(self, path, hostport, xml, service, command):
        datalist = [
            'POST %s HTTP/1.1\r\n' % path,
            'Accept-Encoding: gzip\r\n',
            'CONNECTION: close\r\n',
            'HOST: %s\r\n' % hostport,
            'CONTENT-TYPE: text/xml; charset="utf-8"\r\n',
            'CONTENT-LENGTH: %s\r\n' % len(xml),
            'SOAPACTION: "urn:schemas-upnp-org:service:%s:1#%s"\r\n' % (service, command),
            '\r\n',
            xml.decode('utf-8'),#encode added
            '\r\n',
            '\r\n'
        ]
        return "".join(datalist)
    
    def XMLDataForm(self, service, command, variables={} ):
        try:
            xmldoc = '''<?xml version="1.0" encoding="utf-8"?>
            <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body>
                </s:Body>
            </s:Envelope>'''
            xml = parseString(xmldoc)
            body = xml.getElementsByTagName('s:Body')[0]
            cmdnode = xml.createElement("u:"+command)
            urn = "urn:schemas-upnp-org:service:%s:1" % service
            cmdnode.setAttribute("xmlns:u",urn) 
            for var, value in variables.iteritems():
                newnode = xml.createElement(var)
                newnode.appendChild(xml.createTextNode(value))
                cmdnode.appendChild(newnode)
            body.appendChild(cmdnode)
            xmlstr = xml.toxml(encoding="utf-8")
            xmlstr = xmlstr.replace("\r","").replace("\n","").replace("    ","") #compress
            return xmlstr
        except Exception, e:
            print "XMLDataForm Error %s" % (e) 
    
    #---------- generic command send (can use to send commands for something that is not hard coded.        
    def SendCommand(self, service, command, device = '', variables={'InstanceID':'0'}, responseCallBack = 'StandardCmdRes'):
        try:
            callBackFunction = getattr(self, responseCallBack)
        except:
            if globalDebug >= 1:
                print "SendCommand responseCallBack function not found, setting to StandardCmdRes"
            callBackFunction = getattr(self, 'StandardCmdRes')
            
        try:
            command = command[0].upper() + command[1:] #make sure first character is capitalized
            if globalDebug >= 1:
                print "Sending %s to %s" % (command, self.name)
            if device == "":
                path = "/%s/Control" % (service)
            else:
                path = "/%s/%s/Control" % (device, service)
            hostport = self.ip + ":" + str(self.COMMANDPORT)
            xml = self.XMLDataForm(service, command, variables)
            data = self.CommandPacketForm(path, hostport, xml, service, command)
            if globalDebug >= 2:
                print data
            self.socketSendCmd = AsyncRequesting(self.ip, self.COMMANDPORT, data, callBackFunction)
            eg.RestartAsyncore()
            if globalDebug >= 1:
                print "%s Sending %s to %s" % (self.socketSendCmd.portused, command, self.name)
        except Exception, e:
            print "ERROR Handled: Sending %s to %s Failed - %s" % ( command, self.name, e)
        
    def SendCommandPrint(service, command, device = '', variables={'InstanceID':'0'}):
        self.SendCommand(service, command, device, variables, 'StandardCmdResPrint')
        
    #------------- AVTransport Commands -------------------------------------------------
    def SendPlay(self):
        self.SendCommand( "AVTransport", "Play", "MediaRenderer", variables={'InstanceID':'0', 'Speed':'1'})
    
    def SendPause(self):
        self.SendCommand( "AVTransport", "Pause", "MediaRenderer")
        
    def SendStop(self):
        self.SendCommand( "AVTransport", "Stop", "MediaRenderer")
        
    def SendNext(self):
        self.SendCommand( "AVTransport", "Next", "MediaRenderer")
    
    def SendPrevious(self):
        self.SendCommand( "AVTransport", "Previous", "MediaRenderer")
        
    def SendSeek(self, unit, target):
        variables = {'InstanceID':'0', 'Unit':unit, 'Target':target}
        self.SendCommand( "AVTransport", "Play", "MediaRenderer", variables)
    
    def SendGetPositionInfo(self, callback=None):
        variables = {'InstanceID':'0'}
        self.GetPositionInfoCallback = callback
        self.SendCommand( "AVTransport", "MediaRenderer", "GetPositionInfo", variables, 'ResponseGetPositionInfo')
    
    def SendGetMediaInfo(self, callback=None):
        variables = {'InstanceID':'0'}
        self.GetMediaInfoCallback = callback
        self.SendCommand( "AVTransport", "GetMediaInfo", "MediaRenderer", variables, 'ResponseGetMediaInfo')
    
    def SendSetAVTransportURI(self, uri, urimetadata=''):
        variables = {'InstanceID':'0', 'CurrentURI':uri, 'CurrentURIMetaData':urimetadata}
        self.SendCommand( "AVTransport", "SetAVTransportURI", "MediaRenderer", variables)
        
    def SendAddURIToQueue(self, uri, urimetadata):
        variables = {'InstanceID':'0', 
                     'EnqueuedURI':uri, 
                     'EnqueuedURIMetaData':urimetadata,
                     'DesiredFirstTrackNumberEnqueued':'0',
                     'EnqueueAsNext':'0'
                    }
        self.SendCommand( "AVTransport", "AddURIToQueue", "MediaRenderer", variables)
    
    def SendSetPlayMode(self, playmode):
        variables = {'InstanceID':'0', 'NewPlayMode':playmode}
        self.SendCommand( "AVTransport", "SetPlayMode", "MediaRenderer", variables)
    
    def SendRemoveAllTracksFromQueue(self):
        variables = {'InstanceID':'0'}
        self.SendCommand( "AVTransport", "RemoveAllTracksFromQueue", "MediaRenderer", variables)
    
    #------------- Rendering Commands -------------------------------------------------    
    #NOTE: sending volume commands should not be sent to invisible ZPs. 
    def SendRelVolume(self, incvol):
        variables = {'InstanceID':'0', 'Channel':'Master', 'Adjustment':incvol}
        self.SendCommand( "RenderingControl", "SetRelativeVolume", "MediaRenderer", variables)

    def SendSetVolume(self, setvol):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredVolume':setvol}
        self.SendCommand( "RenderingControl", "SetVolume", "MediaRenderer", variables)

    def SendMuteOn(self):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredMute':'1'}
        self.SendCommand( "RenderingControl", "SetMute", "MediaRenderer", variables)
    
    def SendMuteOff(self):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredMute':'0'}
        self.SendCommand( "RenderingControl", "SetMute", "MediaRenderer", variables)

    #------------- Media Server Commands ------------------------------------------------- 
    def SendGetFavPlayList(self, callback=None):    
        variables = {
                     'ObjectID':'FV:2',
                     'BrowseFlag':'BrowseDirectChildren',
                     'Filter':'dc:title,res,dc:creator,upnp:artist,upnp:album,upnp:albumArtURI',
                     'StartingIndex':'0',
                     'RequestedCount':'100',
                     'SortCriteria':''
                    }
        self.GetFavPlayListCallback = callback
        self.SendCommand( "ContentDirectory", "Browse", "MediaServer", variables, 'ResponseGetFavPlayList')
    
    #------------- Response Callback Functions  ------------------------------------------   
    def StandardCmdResPrint(self, response):
        try:
            if response['status'] == "OK":
                print "%s Standard Response: \r\n%s" % (self.name, response['body'])
                pass
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
        except:
            print "**Response HTML Error from %s" % (self.name)
    
    def StandardCmdRes(self, response):
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s Standard Response: \r\n%s" % (self.name, response['body'])
                pass
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
        except:
            print "**Response HTML Error from %s" % (self.name)
            print response
            
    def ResponseGetPositionInfo(self, response):
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s GetPositionInfo Response: \r\n%s" % (self.name, response['body'])
                xmlstr = response['body']
                xml = parseString(xmlstr.encode('utf-8'))
                self.track = xml.getElementsByTagName('Track')[0].childNodes[0].nodeValue
                self.trackuri = xml.getElementsByTagName('TrackURI')[0].childNodes[0].nodeValue
                self.trackmetadata = xml.getElementsByTagName('TrackMetaData')[0].childNodes[0].nodeValue
                self.reltime = xml.getElementsByTagName('RelTime')[0].childNodes[0].nodeValue
                #call callback function if present 
                try: 
                    self.GetPositionInfoCallback() 
                    self.GetPositionInfoCallback = None
                except: 
                    pass
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
        except:
            print "**Response HTML Error from %s" % (self.name) 
     
    def ResponseGetMediaInfo(self, response):
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s GetPositionInfo Response %s" % (self.name, response['body'])
                xmlstr = response['body']
                xml = parseString(xmlstr.encode('utf-8'))
                self.track = xml.getElementsByTagName('Track')[0].childNodes[0].nodeValue
                self.trackuri = xml.getElementsByTagName('TrackURI')[0].childNodes[0].nodeValue
                self.trackmetadata = xml.getElementsByTagName('TrackMetaData')[0].childNodes[0].nodeValue
                self.reltime = xml.getElementsByTagName('RelTime')[0].childNodes[0].nodeValue
                #call callback function if present 
                try: 
                    self.GetMediaInfoCallback() 
                    self.GetMediaInfoCallback = None
                except: 
                    pass 
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
        except:
            print "**Response HTML Error from %s" % (self.name)
     
    def ResponseGetFavPlayList(self, response):
        #try:
        if response['status'] == "OK":
            if globalDebug >= 1:
                print "%s GetFavPlayList Response \n%s" % (self.name, response['body'])
            xmlstr = response['body']
            xml = parseString(xmlstr)
            xmlplayliststring = xml.getElementsByTagName('Result')[0].firstChild.nodeValue
            xml = parseString(xmlplayliststring.encode('utf-8'))
            #print xml.toxml()
            self.favPlayList={} #clear dict
            for item in xml.getElementsByTagName('item'):
                tempdescription = item.getElementsByTagName('r:description')[0].firstChild.nodeValue.replace(" Station","")
                temptitle = item.getElementsByTagName('dc:title')[0].firstChild.nodeValue
                tempuri = item.getElementsByTagName('res')[0].firstChild.nodeValue
                subxmlstr = item.getElementsByTagName('r:resMD')[0].firstChild.nodeValue
                subxml = parseString(subxmlstr.encode('utf-8'))
                tempurimetadata = subxml.getElementsByTagName('DIDL-Lite')[0].toxml()
                tempupnpclass = subxml.getElementsByTagName('upnp:class')[0].firstChild.nodeValue
                if tempupnpclass.find("playlistContainer") > 0: #is this a streaming station or a playlist
                    tempisplaylist = True
                else:
                    tempisplaylist = False
                self.favPlayList[temptitle]={} #clear/create dict
                self.favPlayList[temptitle]['description'] = tempdescription
                self.favPlayList[temptitle]['uri'] = tempuri
                self.favPlayList[temptitle]['urimetadata'] = tempurimetadata
                self.favPlayList[temptitle]['upnpclass'] = tempupnpclass
                self.favPlayList[temptitle]['isplaylist'] = tempisplaylist
            
            #call callback function if present 
            try: 
                self.GetFavPlayListCallback() 
                self.GetFavPlayListCallback = None
            except: 
                print "Error No GetFavPlayListCallback executed..."
        else:
            print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
        #except Exception, e:
        #    print "**Response HTML Error from %s %s response:\n%s" % (self.name, e, response)    
            
            
def searchforsonos():
    try:
        zpList = {} #need to make zp class now. 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1.5)#very important if useing while loop to receive all responses,if this is removed, loop occurs
        s.bind(('', 5001))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 3\r\nST: urn:schemas-upnp-org:device:ZonePlayer:1\r\n\r\n'
        s.sendto(data, ('239.255.255.250', 1900))
        print "Searching for SONOS ZonePlayers on network..."
        while True:#look until timeout # this is to capture all responses
            data, srv_sock = s.recvfrom(65565)              
            if not data: break
            if data.find("ST: urn:schemas-upnp-org:device:ZonePlayer:1") > 0: #verify it's SONOS
                srv_addr = srv_sock[0]
                html = HtmlSplit(data)
                uuid = html["USN"].split("::")[0].split(":")[1]
                household = html["X-RINCON-HOUSEHOLD"]
                location = html["LOCATION"]
                zpList[uuid] = ZonePlayer(uuid, srv_addr, location)
                zpList[uuid].household = household
                #print "USN: %s IP: %s" % (zpList[uuid].uuid, zpList[uuid].ip)
                #print "Household HHID: %s" % zpList[uuid].household
                #print "XML info: %s" % location
                #print data
    except Exception, e:
        if str(e) == "timed out":
            print "MSEARCH socket closed"
        else:
            print "ERROR %s" % e
        s.close
    return zpList 

    
def connerror(self, status, reason):
    if not int(status) == 200:
        print "ERROR: " + str(status) + " - " + reason  

        
def httpRequest(self, host, port, path, type, headers, data=""):
    hostport = host + ":" + str(port)
    conn = httplib.HTTPConnection(host,port)
    conn.request(type, path, data, headers)
    res = conn.getresponse() #res.read() #res.getheader(name) #res.getheaders() list #
    connerror(self, res.status, res.reason)
    return res  


################################################################################################  
###################################### Plugin Base #############################################
################################################################################################
class Sonos(eg.PluginBase):

    def __init__(self):
        print "initializing SONOS plugin..."
        self.AddActionsFromList(ACTIONS)
    
    def __start__(self, debugLvL=0):
        print "SONOS plugin starting..."
        global globalZPList
        global globalServiceList
        global localip
        global serverPort
        global globalDebug 
        globalDebug = debugLvL
        localip = get_lan_ip()
        if globalDebug >= 1:
            print localip        
        globalServiceList = {}
        try:
            globalZPList = searchforsonos()
            if not globalZPList:  #if nothing found, try one more time. 
                globalZPList = searchforsonos()
            #need to get the XML files here of all ZPs to get model info. 
            self.server = EventServer() #start listening for events as long as plugin is active (creates a listening socket)
            serverPort = self.server.port
            uuid = globalZPList.keys()[0] #select random ZP to get grouptopology from 
            #send request using asyncore
            tempservice = Service(globalZPList[uuid], "/ZoneGroupTopology/Event", ZoneGroupTopologyEvent, serverPort)   
            #asyncore.loop(5)
            eg.RestartAsyncore() #this used instead of asyncore.loop for EG.
        except Exception,e: 
            print "error while executing..."
            print str(e)
            PrintException()
            print "calling closesockets due to exception..."
            self.closesockets()
            
    def __stop__(self):
        print "SONOS plugin stopping..."
        self.closesockets()
        
    def __close__(self):
        print "SONOS plugin closing..."
        #self.closesockets()

    def closesockets(self):
        #print group topology state one last time. 
        print "\r\nSONOS Plugin SHUTTING DOWN..."
        if globalDebug >= 1:
            print 'caller name:', inspect.stack()[1][3]

        for uuid in globalZPList:
            if globalZPList[uuid].coordinator == uuid:
                coordinator = "Coordinator"
            else:
                coordinator = ""
            if globalDebug >= 1:
                print uuid + " = " + globalZPList[uuid].name + " : " + coordinator + " SID:" + globalZPList[uuid].services['AVTransport']
        try:
            if globalDebug >= 1:
                print "unsubscribing to all services..." 
            #replace with loop that cycles through globalServiceList
            for k, service in globalServiceList.iteritems():
                #print "SID Exists..."
                service.Unsubscribe()
        except AttributeError,e:
            if globalDebug >= 1:
                print "nothing to unsubscribe from : %s" % str(e)
            pass
        self.server.close()
        print "SONOS Event Server has been Shut down, the end."        
    
    def Configure(self, debugLvL=0):
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        text1 = '''
                0 - Debug Off, only screen print when errors occur
                1 - Print general comments within functions
                2 - Print Asyncore Socket messages and everything else
                '''
        TextZPSelect = wx.StaticText(panel, -1, "Select Debug Level...")
        TextSelect = wx.StaticText(panel, -1, text1)
        TextNote = wx.StaticText(panel, -1, "")
        try:
            DropDown = wx.SpinCtrl(panel, -1, debugLvL, (0,0), (100,20))
            DropDown.SetRange(0,2)
        except:
            DropDown = wx.SpinCtrl(panel, -1, '0', (0,0), (100,20))
            DropDown.SetRange(0,2)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(DropDown, (1,0), (1,2), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        mySizer.Add(TextSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextNote, (4,0), (1,2), flag = wx.EXPAND)
        while panel.Affirmed():
            Final = DropDown.GetValue()
            panel.SetResult(
                Final
            )

########################################## Window Panels ########################################
class WindowUUIDSelectList():
    def __init__(self, uuid="", item = '', title="Select a Zone Player and item from the list below...", list=[], text1="", text2=""):
                
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextPMSelect = wx.StaticText(panel, -1, text1)
        TextPMNote = wx.StaticText(panel, -1, text2)
        #============ dropdown ==============
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                if v.invisible == 0:
                    ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                    #ChoiceList.append(k)
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        
        #============ dropdown ==============
        ChoiceList = list
        PMDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(item)
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
                FinalPM                
            )


class WindowUUIDSelectRange():
    def __init__(self, uuid="", value=0, title="Select a Zone Player and Value from the list below...", range="0:100", text1="", text2=""):
                
        try:
            rangeMin = int(range.split(":")[0])
            rangeMax = int(range.split(":")[1])
        except:
            print "Range for Window set incorrectly sb: 'min:max' "
            rangeMin = 0
            rangeMax = 10
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextVolSelect = wx.StaticText(panel, -1, text1)
        TextVolNote = wx.StaticText(panel, -1, text2)
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        try:
            VolDropDown = wx.SpinCtrl(panel, -1, value, (0,0), (100,20))
            VolDropDown.SetRange(rangeMin,rangeMax)
        except:
            VolDropDown = wx.SpinCtrl(panel, -1, '3', (0,0), (100,20))
            VolDropDown.SetRange(rangeMin,rangeMax)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), (1,2), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextVolSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextVolNote, (4,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(VolDropDown, (3,1), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalVol = VolDropDown.GetValue()
            panel.SetResult(
                FinalChoice.split("-")[1], #save only the uuid from the list.
                str(FinalVol) 
            )


class WindowUUIDSelect():
    def __init__(self, uuid="", title="Select a Zone Player from the list below..."):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            ChoiceList.sort()
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[1], #save only the uuid from the list.
            )         
        
################################################ Actions ########################################

class Play(eg.ActionBase):
    name = "Send SONOS PLay"
    description = "sends the play command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPlay()
    
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)       
            
            
class Pause(eg.ActionBase):
    name = "Send SONOS Pause"
    description = "sends the pause command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPause()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class Stop(eg.ActionBase):
    name = "Send SONOS Stop (NOTE: in most cases Paused should be used instead of Stop)"
    description = "sends the stop command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendStop()
       
    def Configure(self, uuid=""):
        text1 = '''Select a Zone Player from the list below...\n(NOTE: in most cases Paused should be used instead of Stop)'''
        winSelectGUI = WindowUUIDSelect(uuid, text1) 

class Next(eg.ActionBase):
    name = "Send SONOS Next"
    description = "sends the next command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendNext()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)        

class Previous(eg.ActionBase):
    name = "Send SONOS Previous"
    description = "sends the previous command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPrevious()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)         
 
class VolumeAdjust(eg.ActionBase):
    name = "Send SONOS VolumeAdjust"
    description = "sends command to adjust the volume by a relative amount. "

    def __call__(self, uuid="", incvol="3"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendRelVolume(incvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "adjusted volume by " + str(incvol) + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", incvol="3"):
        title = "Select a Zone Player and Step Value from the list below..."
        range1 = "-10:10"
        text1 = '''Select incremental percentage to adjust volume\nrelative to current value.\nVol. Up def.= 3\nVol. Dwn def.= -3'''
        text2 = '''- Select positive number to adjust volume up\n - Select negative to adjust volume down.\n'''
        winSelectGUI = WindowUUIDSelectRange(uuid, incvol, title, range1, text1, text2)

class VolumeSet(eg.ActionBase):
    name = "Send SONOS VolumeSet"
    description = "sends command to set volume to specific value. "

    def __call__(self, uuid="", setvol="20"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendSetVolume(setvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "set volume to "+ str(setvol) + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", setvol="20"):
        title = "Select a Zone Player and Step Value from the list below..."
        range1 = "0:100"
        text1 = '''Select Volume level (0-100%)'''
        text2 = ''''''
        winSelectGUI = WindowUUIDSelectRange(uuid, setvol, title, range1, text1, text2)

class MuteOn(eg.ActionBase):
    name = "Send SONOS Mute On"
    description = "sends command to activate Mute."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendMuteOn()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class MuteOff(eg.ActionBase):
    name = "Send SONOS Mute Off"
    description = "sends command to disable Mute."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendMuteOff()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class SetPlayMode(eg.ActionBase):
    name = "Send SONOS PlayMode, like shuffle and repeat"
    description = "sends command to set play mode. "

    def __call__(self, uuid="", playmode="NORMAL"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendSetPlayMode(playmode)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "set playmode to "+ playmode + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", playmode="NORMAL"):
        title = "Select a Zone Player and Play Mode from the list below..."
        list1 = ["NORMAL", "REPEAT_ALL", "SHUFFLE_NOREPEAT", "SHUFFLE"]
        text1 = '''Select Play Mode.'''
        text2 = '''NOTE: Streaming stations like Pandora don't support PlayMode.\n\tFor this reason if this is sent while listening\n\tto streaming station, it will return a 500 error.'''
        winSelectGUI = WindowUUIDSelectList(uuid, playmode, title, list1, text1, text2)


class StartPlayList(eg.ActionBase):
    name = "Start a playlist from the SONOS Favorites list"
    description = "sends command to start playlist. "

    def __call__(self, uuid="", title="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        if isplaylist:
            globalZPList[coordinator].SendRemoveAllTracksFromQueue()
            globalZPList[coordinator].SendAddURIToQueue(uri, urimetadata)
            globalZPList[coordinator].SendSetAVTransportURI("x-rincon-queue:"+coordinator+"#0", "")
            if globalDebug >= 1:
                print "Starting Playlist "+ title + " in " + globalZPList[uuid].name
        else:
            globalZPList[coordinator].SendSetAVTransportURI(uri, urimetadata)
            if globalDebug >= 1:
                print "Starting Station " + title + " in " + globalZPList[uuid].name
        globalZPList[coordinator].SendPlay()
       
    def ResponseReceived(self):
        if globalDebug >= 1:
            print "getFavPlayList Socket ResponseReceived callback Success"
        self.favPlayListReceived = True
        
    def Configure(self, uuid="", title="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        try:
            panel = eg.ConfigPanel()
            #get SONOS Favorites...(make sure not to select a bridge by ignoring invisible zps)
            if globalDebug >= 1:
                print "looking for ZP that is not invisible..."
            self.favPlayListReceived = False
            for k, v in globalZPList.iteritems():
                    if v.invisible == 0: #find the first non invisible ZP
                        tempuuid = k
                        break
            if globalDebug >= 1:
                print "Getting Favorites List from %s at %s" % (globalZPList[tempuuid].name,globalZPList[tempuuid].ip)
            globalZPList[tempuuid].SendGetFavPlayList(self.ResponseReceived)
            if globalDebug >= 1:
                print "Waiting for SendGetFavPlayList response..."
            #wait for socket to be created..
            while True:
                time.sleep(0.1)#small delay to allow socket to be created and wait between reads
                try:
                    #check to see if socket is still alive, if it's not break. This is to avoid hanging in the loop. 
                    noread = globalZPList[tempuuid].socketSendCmd.getsockname()
                    if globalDebug >= 1:
                        print "getFavPlayList Socket created..."
                    break
                except:
                    pass
            #wait for socket to be closed or callback function called..
            while True:
                #if self.favPlayListReceived:
                #    break
                time.sleep(0.1)#small delay to allow socket to be created and wait between reads
                try:
                    #check to see if socket is still alive, if it's not break. This is to avoid hanging in the loop. 
                    noread = globalZPList[tempuuid].socketSendCmd.getsockname()
                except:
                    if globalDebug >= 1:
                        print "getFavPlayList Socket closed before ResponseReceived callback"
                    break
            try: 
                presets = globalZPList[tempuuid].favPlayList
            except:
                print "ERROR getting favPlayLists..."
                return
            
            mySizer = wx.GridBagSizer(5, 1)
            mySizer.AddGrowableRow(4)
            mySizer.AddGrowableCol(0)
            
            panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
            
            TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
            TextPLSelect = wx.StaticText(panel, -1, "Select a Playlist or Station from your SONOS Favorites list...")
            TextPLNote = wx.StaticText(panel, -1, '''Make sure to add any station you want to select to the SONOS favorites list before opening this dialogue.\nAlso note when the action is triggered, if it's a playlist it will replace the current queue''')
            #============ dropdown ==============
            ChoiceList = []
            if globalZPList:
                for k, v in globalZPList.iteritems():
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                        #ChoiceList.append(k)
                ChoiceList.sort()
                ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
            else:
                print "!! - No SONOS ZPs, search network again"
                return
            #Identify the device and set dropdown to correct position
            p = 0
            try:
                p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
                ZPDropDown.SetSelection(p)
            except: #ValueError:
                ZPDropDown.SetSelection(0)
            #============ end dropdown ==============
            
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
                    FinalPL,
                    presets[FinalPL]['description'],
                    presets[FinalPL]['uri'],
                    presets[FinalPL]['urimetadata'],
                    presets[FinalPL]['upnpclass'],
                    presets[FinalPL]['isplaylist']                
                ) 
        except Exception, e:
            print "something went wrong %s" % e

#class TestCmd(eg.ActionBase):
#    name = "Send SONOS TestCmd"
#    description = "sends command to test."
#
#    def __call__(self, uuid=""):
#        if uuid == "":
#            print "Please select a ZP to send command to."
#            return
#        if uuid not in globalZPList:
#            print "!!! zone player no longer in globalZPList (not found on network) !!!"
#            return
#        globalZPList[uuid].SendGetFavPlayList(self.ResponseReceived)
#    
#    def ResponseReceived():
#        print "TestCmd Response Received" 
#        
#    def Configure(self, uuid=""):
#        winSelectGUI = WindowUUIDSelect(uuid)            
#           
ACTIONS = (
    #(SearchForSonosZPs,"SearchForSonosZPs","SearchForSonosZPs","SearchForSonosZPs.", None),
    (Play,"Play","Play","Send Play to ZonePlayer.", None),
    (Pause,"Pause","Pause","Send Pause to ZonePlayer.", None),
    (Stop,"Stop","Stop","Send Stop to ZonePlayer.", None),
    (Next,"Next","Next","Send Next to ZonePlayer.", None),
    (Previous,"Previous","Previous","Send Previous to ZonePlayer.", None),
    (VolumeAdjust,"VolumeAdjust","VolumeAdjust","VolumeAdjust Sonos.", None),
    (VolumeSet,"VolumeSet","VolumeSet","VolumeSet Sonos.", None),
    (MuteOn,"MuteOn","MuteOn","MuteOn Sonos.", None),
    (MuteOff,"MuteOff","MuteOff","MuteOff Sonos.", None),
    (StartPlayList, "StartPlayList","StartPlayList","Start Playlist", None),
    (SetPlayMode, "SetPlayMode", "SetPlayMode", "Set Play Mode", None)
    #(TestCmd, "TestCmd", "TestCmd", "TestCmd", None)
    #(WhatstheWeather, "WhatstheWeather", "WhatstheWeather", "Play current weather forecast over SONOS", None)
)