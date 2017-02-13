import eg
import time
from threading import Thread, Event

eg.RegisterPlugin()

class SmoothVolPlugin(eg.PluginBase):

    def __init__(self):
        self.AddAction(SetVolSmooth)
        self.mythread = None        

class SetVolSmooth(eg.ActionBase):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%) from 0 to 100 using a smooth transition"
    
    def __call__(self,targetVol=50.0,delay=5,step=5):  
        
        if self.plugin.mythread and self.plugin.mythread.isAlive():
            self.plugin.mythread.KillThread()  #ask the active thread to abort
            self.plugin.mythread.join() #wait for it to abort
        
        #it should now be safe to create a new thread that fades the volume
        currentVol=int(eg.plugins.System.ChangeMasterVolumeBy(0.0, 0))
        #self.plugin.threadFlag = Event()
        self.plugin.mythread=SetVolThread('theSetVolThread',currentVol,targetVol,delay,step)  
        self.plugin.mythread.start()
        
    def Configure(self, targetVol=50.0,delay=5.0,step=5.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl( panel,-1,targetVol, max=100.0,fractionWidth=0 )
        delayCtrl = eg.SpinIntCtrl( panel,-1,delay,min=1, max=50 )
        stepCtrl = eg.SpinIntCtrl( panel,-1,step,min=1, max=10 )
        panel.AddLabel("Volume Level:")
        panel.AddCtrl(volumeCtrl)
        panel.AddLabel("delay per step (milliseconds)")
        panel.AddCtrl(delayCtrl)
        panel.AddLabel("step (adjust vol by this much on each loop)")
        panel.AddCtrl(stepCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue(),delayCtrl.GetValue(),stepCtrl.GetValue())
            

    class text:
        label_conf="Volume Level:"

class SetVolThread(Thread):
    def __init__(self,name,fromVol,toVol,delay,step):
        self.kill = False
        self.fromVol=fromVol
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
                #print self.name,' has been killed'
                raise SystemExit()
                
        #finally set it to the requested value
        eg.plugins.System.SetMasterVolume(self.toVol)
        #finished fading volume
        
    def KillThread(self):
        self.threadFlag.set()