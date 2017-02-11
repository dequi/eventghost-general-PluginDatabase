# This file is part of EventGhost.
# Copyright (C) 2007
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-11-29 $
# $LastChangedRevision: 04 $
# $LastChangedBy: nightrader $
import eg
from threading import Event, Thread

eg.RegisterPlugin(
    name = "SageTVEvents",
    author = "Nightrader",
    version = "0.0.1." + "$LastChangedRevision: 6 $".split()[1],
    kind = "other",
    description = (
            'Adds Events from the <a href="http://www.sagetv.com/">'
            'SageTV Media Center</a>.<br>'
            '<br>'
            'Adds the following events:<br>'
            '<UL>     <li>NowPlaying</li>'
            '     <li>RecordingStart</li>'
            '     <li>RecordingStop</li></ul>'
            '<br><br>'
            'note: '
            'requires the GetStatus plugin for SageTV, <br>located '
            '<a href="http://tools.assembla.com/sageplugins/wiki/GetStatusPlugin#preview">'
            'here</a>.<br>'
        ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1wMXEAcEHYti"
        "bwAAABd0RVh0U29mdHdhcmUAR0xEUE5HIHZlciAzLjRxhaThAAAACHRwTkdHTEQzAAAA"
        "AEqAKR8AAAAEZ0FNQQAAsY8L/GEFAAACx0lEQVR4nH2TbUhTYRTH9+Z0u3POu93t7u5F"
        "J5ovEWVvJlEaWhIRiSaCZmpSfSor8oNCX4QikqCQzPpQERqUsC8hmh/UQNEoN5thapRa"
        "JoLMFywni/x37iWlNDvwg/vA+f/POc95rky2QcQ4o7YSFUQlsWejvHVhjGSNsdGue07B"
        "9t3MGsFFsqDvYExU9DOXw2n7r1inZdQOwfbczluREBuHspJSnD19BlsSkyBwZlAnPYaI"
        "CP2GBiajsZCqIWXHTni9XqzE8NAwMtLTYbfwsHDcpQ0NBIulyUqVnjQ0Ym10trfDaRVA"
        "HXb8U6zVaFOibLYpm9mCfo93ncHczAziXDGg8QICz//dRTijc9B841aTGbnHsvGguw6P"
        "3tXh/ewAxr8FcevlEKqb+1BefgFRggCXwwGLiStYNaDDDbH1k4UnsLS4hJ7JTpS2HMfl"
        "xlwUV12H62oz6rtHpE7u1NZCzHVYhUEdw2hkKqVKTYc30XYHXvX2rrbc5+9DfdVR1KRt"
        "h9v7EcEfQSwsLGBsbAx7U1Ol9bIGwz6ZQqGw2Hj+i7iqiYkJSbz82+TrzXMYLEhE0D+F"
        "ab8fIyMj8Hg8OJyVBT2jQ0S4Pl8ml8s5wcIP2OmGX7S2SsJAIIDFn8v43FAD38UjGB0d"
        "Rf9bH7q6uuB2u7E5IREGvR5qtfqgeAUaNsLwWLz9A/vT4PP5MD8/h+mZWbS5n+J+dSVe"
        "01Y6OjokcW5OjlSdDD7J5DLpZSqUCkU2jTFpZk1Iik/AqZISFBcVYVNcPDgzj0OZmcjP"
        "y8P25GSEMwyMhkiEqtVXSKtcWYRdpVJVmFjjB45lpQoilLhsYtmgKGLCNJKYnvIsie+G"
        "qEKSqbBixUB0SiLKaK46nVbbQjSrQ0Juk/E1TZimidFq20JDQx+S5jzlbVMqlZq1j1FO"
        "iDOJv24WkUHsJnYR6UQmkUI4/mz9FwoIacGNmDGLAAAAAElFTkSuQmCC"
    ),
)

import socket

class Text:
    host = "Host Address:"
    port = "TCP/IP Port:"
    poll_interval = "Polling Interval (sec):"
    NowPlaying = "Enable NowPlaying event"
    ExtraEvents = "Enable Expanded NowPlaying Events"
    Recording = "Enable Recording events"
    

# Events Supported
#  NowPlaying
#  RecordingStart 
#  RecordingStop  

class Playing:
    type      = "none"
    show      = "none"
    episode   = "none"
    artist    = "none"
    channel   = "none"
    starttime = "none"
    endtime   = "none"
    currpos   = "none"
    state     = "none"

    
class SageTVDevice:
    devname = "none"
    show    = "none"
    episode = "none"
    channel = "none"
    starttime = "none"
    endtime   = "none"
    index     = 0

class SageTVEvents(eg.PluginClass):
    canMultiLoad = True
    text = Text

    lastDevices = []
    lastPlaying = Playing()

    def __init__(self):
        eg.PluginClass.__init__(self)
        eg.globals.SageTVEventsPayload = ""
        class Action(SageTVEventsAction):
            Server = self
        Action.__name__ = "Poll Server"
        self.AddAction(Action)
    def __close__(self):
        self.stopThreadEvent.set()

    def __start__(self,
                  port=1024,
                  host="127.0.0.1",
                  pollinterval=5.0,
                  nowPlaying = True,
                  enableExtraEvents = False,
                  Recording = True):
        eg.globals.SageTVEventsPayload = ""
        self.lastPlaying.state = ""
        self.lastDevices = []
        self.stopThreadEvent = Event()
        self.port = port
        self.host = host
        self.pollinterval = pollinterval
        self.nowPlaying = nowPlaying
        self.enableExtraEvents = enableExtraEvents
        self.Recording = Recording

        if self.pollinterval > 0:
          thread = Thread(target=self.ThreadWorker, args=(self.stopThreadEvent,))
          thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            self.pollServer(self)
            stopThreadEvent.wait(self.pollinterval)

    def pollServer(self, payload=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(2.0)
        connected = False
        try:
            sock.connect((self.host, self.port))
            buffer = sock.recv(8192)
            sock.close
        except:
            if eg.debugLevel:
                eg.PrintTraceback()
            sock.close()
            errorString = self.host + ":" + str(self.port)
            self.PrintError("SageTV server [" + errorString + "] is not responding")
            return None

        lines = buffer.splitlines()
        
        if self.nowPlaying:
            self.proccessNowPlaying(lines[:9])
        if self.Recording:
            self.proccessDevices(lines[9:])


    def proccessNowPlaying(self, nowplaying):
        if self.lastPlaying.state.strip() == "":
            #First Run
            self.lastPlaying.type      = nowplaying[0].partition(":")[2].strip()
            self.lastPlaying.show      = nowplaying[1].partition(":")[2].strip()
            self.lastPlaying.episode   = nowplaying[2].partition(":")[2].strip()
            self.lastPlaying.artist    = nowplaying[3].partition(":")[2].strip()
            self.lastPlaying.channel   = nowplaying[4].partition(":")[2].strip()
            self.lastPlaying.starttime = nowplaying[5].partition(":")[2].strip()
            self.lastPlaying.endtime   = nowplaying[6].partition(":")[2].strip()
            self.lastPlaying.currpos   = nowplaying[7].partition(":")[2].strip()
            self.lastPlaying.state     = nowplaying[8].partition(":")[2].strip()
        else:
            hasChanged = False

            if len(nowplaying[8].partition(":")[2].strip()) != len(self.lastPlaying.state):
                hasChanged = True
            elif len(nowplaying[1].partition(":")[2].strip()) != len(self.lastPlaying.show):
                hasChanged = True
            elif len(nowplaying[0].partition(":")[2].strip()) != len(self.lastPlaying.type):
                hasChanged = True
            elif len(nowplaying[3].partition(":")[2].strip()) != len(self.lastPlaying.artist):
                hasChanged = True

            if hasChanged:
                self.lastPlaying.type      = nowplaying[0].partition(":")[2].strip()
                self.lastPlaying.show      = nowplaying[1].partition(":")[2].strip()
                self.lastPlaying.episode   = nowplaying[2].partition(":")[2].strip()
                self.lastPlaying.artist    = nowplaying[3].partition(":")[2].strip()
                self.lastPlaying.channel   = nowplaying[4].partition(":")[2].strip()
                self.lastPlaying.starttime = nowplaying[5].partition(":")[2].strip()
                self.lastPlaying.endtime   = nowplaying[6].partition(":")[2].strip()
                self.lastPlaying.currpos   = nowplaying[7].partition(":")[2].strip()
                self.lastPlaying.state     = nowplaying[8].partition(":")[2].strip()

                payload = "Type:" + self.lastPlaying.type + ", Show:" + self.lastPlaying.show
                payload = payload + ", State:" + self.lastPlaying.state
                payload = payload + ", Episode:" + self.lastPlaying.episode
                payload = payload + ", Artist:" + self.lastPlaying.artist
                payload = payload + ", Channel:" + self.lastPlaying.channel
                payload = payload + ", StartTime:" + self.lastPlaying.starttime
                payload = payload + ", EndTime:" + self.lastPlaying.endtime
                payload = payload + ", Currpos:" + self.lastPlaying.currpos

                eg.globals.SageTVEventsPayload = payload
                if not self.enableExtraEvents:
                    self.TriggerEvent("NowPlaying", (payload))
                else:

                #Break out Stet Events
                #Stopped, Paused and Play
                    if self.lastPlaying.state == "play":
                        self.TriggerEvent("NowPlaying.Play",(payload))
                    elif self.lastPlaying.state == "paused":
                        self.TriggerEvent("NowPlaying.Paused",(payload))
                    elif self.lastPlaying.state == "stopped":
                        self.TriggerEvent("NowPlaying.Stopped",(payload))

    def proccessDevices(self, devices):

        if len(self.lastDevices) == 0:
            #First Run
            devCnt = int(devices[0].partition(":")[2])
            Cnt = 0
            while devCnt > 0:
                devCnt -= 1
                aDev = SageTVDevice()
                aDev.devname   = devices[1 + (Cnt * 6)].partition(":")[2]
                aDev.show      = devices[2 + (Cnt * 6)].partition(":")[2]
                aDev.episode   = devices[3 + (Cnt * 6)].partition(":")[2]
                aDev.channel   = devices[4 + (Cnt * 6)].partition(":")[2]
                aDev.starttime = devices[5 + (Cnt * 6)].partition(":")[2]
                aDev.endtime   = devices[6 + (Cnt * 6)].partition(":")[2]
                aDev.index     = Cnt
                self.lastDevices.append(aDev)
                Cnt += 1
        else:
            devCnt = int(devices[0].partition(":")[2])
            for aDev in self.lastDevices:
                hasChanged = False
                if (2 + (aDev.index * 6)) < len(devices):
                    if len(aDev.show) != len(devices[2 + (aDev.index * 6)].partition(":")[2]):
                        hasChanged = True
                    elif len(aDev.episode) != len(devices[3 + (aDev.index * 6)].partition(":")[2]):
                        hasChanged = True
                else:
                    Cnt = len(self.lastDevices)
                    aDev = SageTVDevice()
                    aDev.devname   = devices[1 + (Cnt * 6)].partition(":")[2]
                    aDev.show      = devices[2 + (Cnt * 6)].partition(":")[2]
                    aDev.episode   = devices[3 + (Cnt * 6)].partition(":")[2]
                    aDev.channel   = devices[4 + (Cnt * 6)].partition(":")[2]
                    aDev.starttime = devices[5 + (Cnt * 6)].partition(":")[2]
                    aDev.endtime   = devices[6 + (Cnt * 6)].partition(":")[2]
                    aDev.index     = Cnt
                    self.lastDevices.append(aDev)

                if hasChanged:
                    #something has changed
                    #could be lastDev is blank and devices has a show
                        #Fire RecordStarted
                    #could be lastDev has a show and devices is blank
                        #Fire RecordStop
                    #could be lastDev has a show and devices has diffrent show
                        #Fire RecordStop
                        #Fire RecordStart
                    if (aDev.show.strip() == "") and (devices[2 + (aDev.index * 6)].partition(":")[2].strip() != ""):
                        #Fire RecordStart
                        payload = "Device:" + devices[1 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Show:" + devices[2 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Episode" + devices[3 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Channel" + devices[4 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Starttime" + devices[5 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Endtime" + devices[6 + (aDev.index * 6)].partition(":")[2]

                        eg.globals.SageTVEventsPayload = payload
                        self.TriggerEvent("RecordStart", (payload))

                    if (aDev.show.strip() != "") and (devices[2 + (aDev.index * 6)].partition(":")[2].strip() == ""):
                        #Fire RecordStop
                        payload = "Devices:" + aDev.devname
                        payload = payload + ", Show:" + aDev.show
                        payload = payload + ", Episode:" + aDev.episode
                        payload = payload + ", Channel:" + aDev.channel
                        payload = payload + ", Starttime:" + aDev.starttime
                        payload = payload + ", Endtime:" + aDev.endtime

                        eg.globals.SageTVEventsPayload = payload
                        self.TriggerEvent("RecordStop", (payload))

                    if (aDev.show.strip() != "") and (devices[2 + (aDev.index * 6)].partition(":")[2].strip() != ""):
                        #Fire RecordStop
                        payload = "Devices:" + aDev.devname
                        payload = payload + ", Show:" + aDev.show
                        payload = payload + ", Episode:" + aDev.episode
                        payload = payload + ", Channel:" + aDev.channel
                        payload = payload + ", Starttime:" + aDev.starttime
                        payload = payload + ", Endtime:" + aDev.endtime

                        eg.globals.SageTVEventsPayload = payload
                        self.TriggerEvent("RecordStop", (payload))
                        #Fire RecordStart
                        payload = "Device:" + devices[1 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Show:" + devices[2 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Episode" + devices[3 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Channel" + devices[4 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Starttime" + devices[5 + (aDev.index * 6)].partition(":")[2]
                        payload = payload + ", Endtime" + devices[6 + (aDev.index * 6)].partition(":")[2]

                        eg.globals.SageTVEventsPayload = payload
                        self.TriggerEvent("RecordStart", (payload))

                    #update lastDevices
                    aDev.show      = devices[2 + (aDev.index * 6)].partition(":")[2]
                    aDev.episode   = devices[3 + (aDev.index * 6)].partition(":")[2]
                    aDev.channel   = devices[4 + (aDev.index * 6)].partition(":")[2]
                    aDev.starttime = devices[5 + (aDev.index * 6)].partition(":")[2]
                    aDev.endtime   = devices[6 + (aDev.index * 6)].partition(":")[2]

                    return self
    def Configure(self,
                  port=1024,
                  host="127.0.0.1",
                  pollinterval=5,
                  enableNowPlaying = True,
                  enableExtraEvents = True,
                  enableRecording = True
                  ):

        panel = eg.ConfigPanel(self)
        
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        hostCtrl = panel.TextCtrl(host)
        intrvlCtrl = panel.SpinIntCtrl(pollinterval, max=600)
        nowPlayingCtrl = panel.CheckBox(enableNowPlaying)
        extraEventsCtrl = panel.CheckBox(enableExtraEvents)
        recordingCtrl  = panel.CheckBox(enableRecording)
        
        panel.AddLine(self.text.port, portCtrl)
        panel.AddLine(self.text.host, hostCtrl)
        panel.AddLine(self.text.poll_interval, intrvlCtrl)
        panel.AddLine(self.text.NowPlaying, nowPlayingCtrl)
        panel.AddLine(self.text.ExtraEvents, extraEventsCtrl)
        panel.AddLine(self.text.Recording, recordingCtrl)
        
        while panel.Affirmed():
            return (
                portCtrl.GetValue(),
                hostCtrl.GetValue(),
                intrvlCtrl.GetValue(),
                nowPlayingCtrl.GetValue(),
                extraEventsCtrl.GetValue(),
                recordingCtrl.GetValue()
            )

class SageTVEventsAction(eg.ActionClass):
    def __call__(self):
        self.Server.pollServer
        return self
