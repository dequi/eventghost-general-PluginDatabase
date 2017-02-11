# -*- coding: utf-8 -*-
#
# plugins/AudioEndpoint/__init__.py
# 
# This file is a plugin for EventGhost.

import eg

eg.RegisterPlugin(
    name = "AudioEndpoint",
    guid = "{31DE576B-5938-4C0B-A0E2-64F9ADF02BF8}",
    author = "Sem;colon & Johann Boehme",
    version = "1.5",
    kind = "other",
    canMultiLoad = False,
    description = "This plugin can set the default audio render device and generates events when an audio endpoint changes!",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6213",
)

import subprocess
from threading import Event, Thread, Lock

class AudioEndpoint(eg.PluginBase):
  
    def __init__(self):
        self.stopThreadEvent = Event()
        self.AddAction(SetRender, "SetRender", "Set Default Audio Render", "Sets the default audio render device.(by id)")
        self.AddAction(GetRender, "GetRender", "Get Default Audio Render", "Returns the ID of the current Default Audio Render")
        self.AddAction(NextRender, "NextRender", "Next Default Audio Render", "Selects the next available Default Audio Render")
        self.AddAction(PreviousRender, "PreviousRender", "Previous Default Audio Render", "Selects previous available Default Audio Render")

        
    def __start__(self):
        self.activeAudioEndpoint=""
        if self.init():
            print "Audio Endpoint plugin started."
            self.stopThreadEvent = Event()
            thread = Thread(
                target=self.check,
                args=(self.stopThreadEvent, )
            )
            thread.start()


    def __stop__(self):
        print "Audio Endpoint plugin stopped."
        if not self.stopThreadEvent.isSet():
            self.stopThreadEvent.set()
            self.prog.terminate()

    def __close__(self):
        print "Audio Endpoint plugin closed."
        self.stopThreadEvent.set()

    
    def init(self):
        self.audioEndpointIDToNameDict={}
        self.audioEndpointNames=[]
        self.audioEndpointIDs=[]
        command=[self.info.path+'\\EndPointController\\EndPointControllerModified.exe','-g']
        ret, data = self.popen(command)
        if not ret:
            data=data.split("\r\n")[:-1]
            for currData in data:
                currDataArray=unicode(currData.decode(eg.systemEncoding)).split(";;")
                self.audioEndpointIDToNameDict[currDataArray[3]]=currDataArray[0]
                if currDataArray[1]=="1":
                    self.audioEndpointNames.append(currDataArray[0])
                    self.audioEndpointIDs.append(currDataArray[3])
                if currDataArray[2]=="1" and self.activeAudioEndpoint!=currDataArray[3]:
                    self.activeAudioEndpoint=currDataArray[3]
                    self.TriggerEvent("Default.Render.Console."+currDataArray[0], [currDataArray[3]])
                    self.TriggerEvent("Default.Render.Multimedia."+currDataArray[0], [currDataArray[3]])
            return True
        else:
            eg.PrintError("AudioEndpoint: ERROR calling "+str(command)+": "+str(ret))
            return False
    
      
    def popen(self, cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.STDOUT,startupinfo=startupinfo,shell=False)
        data = proc.communicate()[0]
        return (proc.returncode, data)
            
    
    def check(self, stopThreadEvent):
        lock=Lock()
        command=[self.info.path+'\\CMMNotificationClient.exe']
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        self.prog = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, stderr=None,startupinfo=startupinfo)
        while not stopThreadEvent.isSet():
            if self.prog.poll():
                self.prog = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, stderr=None,startupinfo=startupinfo)
            else:
                output = self.prog.stdout.readline()
                lock.acquire()
                if output:
                    output=unicode(output.replace("\r\n","").decode(eg.systemEncoding)).split(";;")
                    if output[2]=="defaultDeviceChanged":
                        if output[3]=="Render" and  output[4]=="Console":
                            self.activeAudioEndpoint=output[1]
                        self.TriggerEvent("Default."+output[3]+"."+output[4]+"."+output[0],[output[1]])
                    elif output[2]=="deviceStateChanged":
                        self.TriggerEvent("State."+output[3]+"."+output[0],[output[1]])
                    #elif output[2]=="devicePropertyChanged":
                        #self.TriggerEvent("Property."+output[3]+"."+output[0],[output[1],output[4]])
                    elif not output[2]=="devicePropertyChanged":
                        self.TriggerEvent(output[2]+"."+output[0],[output[1]])
                stopThreadEvent.wait(0.1)
                lock.release()
        self.prog.terminate()

        
class SetRender(eg.ActionBase):

    setTo = "Set default to:"
    
    def __call__(self,target):
        command=[self.plugin.info.path+'\\EndPointController\\EndPointControllerModified.exe','-s']
        if target in self.plugin.audioEndpointIDs or (self.plugin.init() and target in self.plugin.audioEndpointIDs):
            ret, data = self.plugin.popen(command+[str(target)])
            if not ret:
                return True
        eg.PrintError("AudioEndpoint SetRender: Device not found! "+str(target))
        return False
    
    def GetLabel(self, target=""):
        if target in self.plugin.audioEndpointIDToNameDict:
            target = self.plugin.audioEndpointIDToNameDict[target]
        else:
            target = "???"
        return target
        
    def Configure(self,target=""):
        self.plugin.init()
        if target in self.plugin.audioEndpointIDs:
            target = self.plugin.audioEndpointIDs.index(target)
        else:
            target = 0
        panel = eg.ConfigPanel(self)
        wx_setTo = wx.Choice(panel, -1, choices=self.plugin.audioEndpointNames)
        wx_setTo.SetSelection(target)
        st_setTo = panel.StaticText(self.setTo)
        
        panel.AddLine(st_setTo,wx_setTo)

        while panel.Affirmed():
            panel.SetResult(self.plugin.audioEndpointIDs[wx_setTo.GetCurrentSelection()])


class GetRender(eg.ActionBase):
    
    def __call__(self):
        return self.plugin.activeAudioEndpoint        

        
class NextRender(eg.ActionBase):
    
    def __call__(self):
        self.plugin.init()
        command=[self.plugin.info.path+'\\EndPointController\\EndPointControllerModified.exe','-s']
        oldIndex = self.plugin.audioEndpointIDs.index(self.plugin.activeAudioEndpoint)
        i=oldIndex+1
        while i!=oldIndex:
            if i<len(self.plugin.audioEndpointIDs):
                target = self.plugin.audioEndpointIDs[i]
                ret, data = self.plugin.popen(command+[str(target)])
                if not ret:
                    return True
            if i>=len(self.plugin.audioEndpointIDs):
                i=0
            else:
                i+=1
        eg.PrintError("AudioEndpoint NextRender: No (other) selectable Render!")
        return False
    
    
class PreviousRender(eg.ActionBase):
    
    def __call__(self):
        self.plugin.init()
        command=[self.plugin.info.path+'\\EndPointController\\EndPointControllerModified.exe','-s']
        oldIndex = self.plugin.audioEndpointIDs.index(self.plugin.activeAudioEndpoint)
        i=oldIndex-1
        while i!=oldIndex:
            if i>=0:
                target = self.plugin.audioEndpointIDs[i]
                ret, data = self.plugin.popen(command+[str(target)])
                if not ret:
                    return True
            if i<=0:
                i=len(self.plugin.audioEndpointIDs)-1
            else:
                i-=1
        eg.PrintError("AudioEndpoint PreviousRender: No (other) selectable Render!")
        return False