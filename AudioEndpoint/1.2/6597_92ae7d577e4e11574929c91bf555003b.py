# -*- coding: utf-8 -*-
#
# plugins/AudioEndpoint/__init__.py
# 
# This file is a plugin for EventGhost.

import eg

eg.RegisterPlugin(
    name = "AudioEndpoint",
    author = "Sem;colon & Johann Boehme",
    version = "1.2",
    kind = "other",
    canMultiLoad = False,
    description = "This plugin can set the default audio render device and generates events when an audio endpoint changed!",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6213",
)

import subprocess
from threading import Event, Thread, Lock

class AudioEndpoint(eg.PluginBase):
  
  def __init__(self):
    self.stopThreadEvent = Event()
    self.AddAction(SetRender, "SetRender", "Set Default Audio Render", "Sets the default audio render device.(by id)")

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
            currDataArray=currData.split(";;")
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
        print "ERROR calling "+str(command)+": "+str(ret)
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
          output=output.replace("\r\n","").split(";;")
          if output[2]=="defaultDeviceChanged":
            self.TriggerEvent("Default."+output[3]+"."+output[4]+"."+output[0],[output[1]])
          elif output[2]=="deviceStateChanged":
            self.TriggerEvent("State."+output[3]+"."+output[0],[output[1]])
          elif output[2]=="devicePropertyChanged":
            self.TriggerEvent("Property."+output[3]+"."+output[0],[output[1],output[4]])
          elif not output[2]=="devicePropertyChanged":
            self.TriggerEvent(output[2]+"."+output[0],[output[1]])
        stopThreadEvent.wait(0.1)
        lock.release()
    #prog.terminate()

class SetRender(eg.ActionBase):

  setTo = "Set default to:"
  
  def __call__(self,target):
    command=[self.plugin.info.path+'\\EndPointController\\EndPointControllerModified.exe','-s']
    if target in self.plugin.audioEndpointIDs or (self.plugin.init() and target in self.plugin.audioEndpointIDs):
        ret, data = self.plugin.popen(command+[str(target)])
        if not ret:
            return True
    print "AudioEndpoint SetRender ERROR: Device not found! "+str(target)
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
          
