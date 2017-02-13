import eg
import time
from threading import Thread, Event

eg.RegisterPlugin()

class SmoothVolPlugin(eg.PluginBase):

    def __init__(self):
        self.AddAction(SetVolSmooth)
        self.AddAction(SmoothMute)
        self.AddAction(SmoothUnMute)
        self.AddAction(SmoothToggleMute)

        self.mythread = None 
        self.Muted = False

    def __start__(self, muteVol=0.0,delay=5.0,step=5.0):
        self.muteVol= muteVol
        self.delay = delay
        self.step = step
        
    def PrepareThread(self):
        print 'prepare...'
        if self.mythread and self.mythread.isAlive():
            self.mythread.KillThread()  #ask the active thread to abort
            self.mythread.join() #wait for it to abort
            #it should now be safe to create a new thread that fades the volume

    def doMute(self):
        self.RestoreVolume = int(eg.plugins.System.ChangeMasterVolumeBy(0.0, 0))
        self.PrepareThread()
        self.mythread=SetVolThread('MuteThread',self.muteVol,self.delay,self.step)  
        self.mythread.start()        
        self.Muted = True

    def doUnMute(self):
        self.PrepareThread()
        self.mythread=SetVolThread('MuteThread',self.RestoreVolume,self.delay,self.step)  
        self.mythread.start()        
        self.Muted = False
    
    #configure universal plugin settings for mute/unmute    
    def Configure(self, muteVol=0.0,delay=5.0,step=5.0):
        panel = eg.ConfigPanel(self)
        muteVolCtrl = eg.SpinNumCtrl( panel,-1,muteVol, max=100.0,fractionWidth=0 )
        delayCtrl = eg.SpinIntCtrl( panel,-1,delay,min=1, max=50 )
        stepCtrl = eg.SpinIntCtrl( panel,-1,step,min=1, max=10 )
        panel.AddLabel("Volume Level to set for mute (default 0):")
        panel.AddCtrl(muteVolCtrl)
        panel.AddLabel("delay per step (milliseconds) on Mute/Unmute")
        panel.AddCtrl(delayCtrl)
        panel.AddLabel("step size on mute/unmute")
        panel.AddCtrl(stepCtrl)
        while panel.Affirmed():
            panel.SetResult(muteVolCtrl.GetValue(),delayCtrl.GetValue(),stepCtrl.GetValue())

    
    
class SmoothMute(eg.ActionBase):
    name = "Smooth Mute"

    def __call__(self):
        if  not self.plugin.Muted:
            self.plugin.doMute()
            
        else:
            return 'already muted'
            
class SmoothUnMute(eg.ActionBase):
    name = "Smooth UnMute"

    def __call__(self):
        if  self.plugin.Muted:
            self.plugin.doUnMute()
        else:
            return 'not muted'
      
class SmoothToggleMute(eg.ActionBase):
    name = "Smooth Toggle Mute"

    def __call__(self):
        if  self.plugin.Muted:
            self.plugin.doUnMute()
            
        else:
            self.plugin.doMute()
        
      
class SetVolSmooth(eg.ActionBase):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%) from 0 to 100 using a smooth transition"
    
    def __call__(self,targetVol=50.0,delay=5,step=5):  
        
        if self.plugin.mythread and self.plugin.mythread.isAlive():
            self.plugin.mythread.KillThread()  #ask the active thread to abort
            self.plugin.mythread.join() #wait for it to abort
        
        #it should now be safe to create a new thread that fades the volume
        currentVol=int(eg.plugins.System.ChangeMasterVolumeBy(0.0, 0))
        self.plugin.mythread=SetVolThread('theSetVolThread',targetVol,delay,step)  
        self.plugin.mythread.start()
        self.plugin.Muted=False
        self.plugin.RestoreVolume = targetVol
        
    def Configure(self, targetVol=50.0,delay=5.0,step=5.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl( panel,-1,targetVol, max=100.0,fractionWidth=0 )
        delayCtrl = eg.SpinIntCtrl( panel,-1,delay,min=1, max=50 )
        stepCtrl = eg.SpinIntCtrl( panel,-1,step,min=1, max=10 )
        panel.AddLabel("Volume to set when applying *mute*")
        panel.AddCtrl(volumeCtrl)
        panel.AddLabel("delay per step (milliseconds) for mute/unmute")
        panel.AddCtrl(delayCtrl)
        panel.AddLabel("step size for mute/unmute")
        panel.AddCtrl(stepCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue(),delayCtrl.GetValue(),stepCtrl.GetValue())
            

    class text:
        label_conf="Volume Level:"

class SetVolThread(Thread):
    def __init__(self,name,toVol,delay,step):
        self.kill = False
        self.fromVol=int(eg.plugins.System.ChangeMasterVolumeBy(0.0, 0))
        self.toVol=toVol
        self.delay = 0.01*delay
        self.step = step
        self.threadFlag = Event()
        Thread.__init__(self, name=name)
        
    def run(self):
        #are we raising or lowering volume?
        if  self.toVol> self.fromVol:
            stepVolBy = self.step #raising vol
        else:
            stepVolBy =-self.step #lowering vol
        tempVol=self.fromVol    
        while abs(self.toVol-tempVol)>self.step:
            tempVol+=stepVolBy
            eg.plugins.System.SetMasterVolume(tempVol)
            self.threadFlag.wait(self.delay)
            if self.threadFlag.isSet():
                break
                
        #finally set it to the requested value
        eg.plugins.System.SetMasterVolume(self.toVol)
        #finished fading volume
        
    def KillThread(self):
        self.threadFlag.set()