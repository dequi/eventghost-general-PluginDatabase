#
# plugins/KMK_5I8O/__init__.py
#
# Copyright (C) 2009
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2009-11-08  The first stumbling version
##############################################################################

eg.RegisterPlugin(
    name = "KMK_5I8O",
    author = "Walter Kraembring",
    version = "0.0.3",
    canMultiLoad = True,
    kind = "external",
    url = "http://www.kmk.com.hk/ProductShop/USB5I8O.htm",
    description = (
        '<p>Plugin to control the KMK USB 5I8O Board</p>'
        '\n\n<p><a href="http://www.kmk.com.hk/ProductShop/USB5I8O.htm">Product details...</a></p>'
        '<center><img src="USB5I8O.PNG" /></center>'
    ),
)
import win32com.client
import sys, os, pickle, time
import pythoncom
from threading import Event, Thread

class Text:

    txt_BoardSerial = "Board Serial Number "
    txt_ThreadWaitTime = "Thread wait time (x.y s)"
    
    txt_DigitalIn_1 = "Digital In_1 Value for event (0-1)"
    txt_DigitalIn_2 = "Digital In_2 Value for event (0-1)"
    txt_DigitalIn_3 = "Digital In_3 Value for event (0-1)"
    txt_DigitalIn_4 = "Digital In_4 Value for event (0-1)"
    txt_DigitalIn_5 = "Digital In_5 Value for event (0-1)"
    
    txt_Initiated = "KMK USB 5I8O is initiated"
    txt_OCX_CannotBeFound_T = "KMKUSB5I8OOCX.KMKUSB cannot be found by the thread"
    txt_OCX_Found_T = "OCX is found by the thread"
    txt_IsStopped = " is stopped"
    txt_IsDeleted = " is deleted"
    txt_Polling = "The polling thread has stopped"

    txt_DI = " DI:"
    txt_State = " State:"
    
    class SetDigitalOut:
        name = "Set Digital Output ON"
        description = "Turns on a digital output on the KMK USB 5I8O"
        txt_ConfSetDO = "Digital Output (1-8)"
        
    class ClearDigitalOut:
        name = "Set Digital Output OFF"
        description = "Turns off a digital output on the KMK USB 5I8O"
        txt_ConfClrDO = "Digital Output (1-8)"
       


class KMK5I8O(eg.PluginClass):
    
    text = Text

    def Configure(
        self,
        board_serial = "KMSHF43V",
        tw = 0.1,
        el_1 = 1,
        el_2 = 1,
        el_3 = 1,
        el_4 = 1,
        el_5 = 1,
        di_event_trigger = [0]*5,
        di_event_memory = [0]*5
     ):
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)

        board_serialCtrl = wx.TextCtrl(panel, -1, board_serial)
        board_serialCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_BoardSerial), (0,0))
        mySizer_1.Add(board_serialCtrl, (0,1))

        thread_wait = panel.SpinNumCtrl(
            tw,
            decimalChar = '.',
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.1,
            max = 5.0
        )
        thread_wait.SetInitialSize((60,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_ThreadWaitTime), (1,0))
        mySizer_1.Add(thread_wait, (1,1))

        #Digital event trigger levels
        di_1_level = panel.SpinIntCtrl(el_1, 0, 1)
        di_1_level.SetInitialSize((40,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txt_DigitalIn_1), (2,0))
        mySizer_2.Add(di_1_level, (2,1))
        
        di_2_level = panel.SpinIntCtrl(el_2, 0, 1)
        di_2_level.SetInitialSize((40,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txt_DigitalIn_2), (3,0))
        mySizer_2.Add(di_2_level, (3,1))
        
        di_3_level = panel.SpinIntCtrl(el_3, 0, 1)
        di_3_level.SetInitialSize((40,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txt_DigitalIn_3), (4,0))
        mySizer_2.Add(di_3_level, (4,1))
        
        di_4_level = panel.SpinIntCtrl(el_4, 0, 1)
        di_4_level.SetInitialSize((40,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txt_DigitalIn_4), (5,0))
        mySizer_2.Add(di_4_level, (5,1))
        
        di_5_level = panel.SpinIntCtrl(el_5, 0, 1)
        di_5_level.SetInitialSize((40,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txt_DigitalIn_5), (6,0))
        mySizer_2.Add(di_5_level, (6,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            board_serial = board_serialCtrl.GetValue()
            tw = thread_wait.GetValue()
            el_1 = di_1_level.GetValue()
            del di_event_trigger[0]
            di_event_trigger.insert(0, el_1)
            el_2 = di_2_level.GetValue()
            del di_event_trigger[1]
            di_event_trigger.insert(1, el_2)
            el_3 = di_3_level.GetValue()
            del di_event_trigger[2]
            di_event_trigger.insert(2, el_3)
            el_4 = di_4_level.GetValue()
            del di_event_trigger[3]
            di_event_trigger.insert(3, el_4)
            el_5 = di_5_level.GetValue()
            del di_event_trigger[4]
            di_event_trigger.insert(4, el_5)
            
            panel.SetResult(
                board_serial,
                tw,
                el_1,
                el_2,
                el_3,
                el_4,
                el_5,
                di_event_trigger,
                di_event_memory
            )


    def __init__(self):
        self.AddAction(SetDigitalOut)
        self.AddAction(ClearDigitalOut)
   
        
    def __start__(
        self,
        board_serial,
        tw,
        el_1,
        el_2,
        el_3,
        el_4,
        el_5,
        di_event_trigger,
        di_event_memory
    ):
        self.di_event_trigger = di_event_trigger
        self.di_event_memory = di_event_memory
        self.do_state_memory = [0]*8
        self.do_state_trigger = [0]*8
        self.b_nbr = board_serial
        self.thread_wait = tw

        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
 
        #Get persistent output status data if it exists
        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData+'/EventGhost/KMK_5I8O data')and not os.path.isdir(progData+'/EventGhost/KMK_5I8O data'):
                os.makedirs(progData+'/EventGhost/KMK_5I8O data')
            else:
                print "Reading KMK_5I8O configuration data from file..."
                f = open (progData+'/EventGhost/KMK_5I8O data/KMK_5I8O_p_'+str(self.b_nbr), 'r')
                self.do_state_memory = pickle.load(f)
                f.close()
        else:
            if not os.path.exists('KMK_5I8O data') and not os.path.isdir('KMK_5I8O data'):
                os.mkdir('KMK_5I8O data')
            else:
                print "Reading KMK_5I8O configuration data from file..."
                f = open ('KMK_5I8O data/KMK_5I8O_p_'+str(self.b_nbr), 'r')
                self.do_state_memory = pickle.load(f)
                f.close()

        self.do_state_trigger = self.do_state_memory
        
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()
   
        
    def __stop__(self):
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
 
        #Make current output status data persistent
        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData+'/EventGhost/KMK_5I8O data')and not os.path.isdir(progData+'/EventGhost/KMK_5I8O data'):
                os.makedirs(progData+'/EventGhost/KMK_5I8O data')
            print "Writing KMK_5I8O configuration data to file..."
            f = open (progData+'/EventGhost/KMK_5I8O data/KMK_5I8O_p_'+str(self.b_nbr), 'w')
            pickle.dump(self.do_state_memory, f)
            f.close()
        else:
            if not os.path.exists('KMK_5I8O data') and not os.path.isdir('KMK_5I8O data'):
                os.mkdir('KMK_5I8O data')
            print "Writing KMK_5I8O configuration data to file..."
            f = open ('KMK_5I8O data/KMK_5I8O_p_'+str(self.b_nbr), 'w')
            pickle.dump(self.do_state_memory, f)
            f.close()

        self.stopThreadEvent.set()
        print (
            self.text.txt_BoardSerial+str(self.b_nbr)+
            self.text.txt_IsStopped
        )    
    

    def __close__(self):
        self.stopThreadEvent.set()
        print (
            self.text.txt_BoardSerial+str(self.b_nbr)+
            self.text.txt_IsDeleted
        )
 
                
    def ThreadWorker(self, stopThreadEvent):
        pythoncom.CoInitialize()        
        
        #Attach interface to the OCX
        AxkmkusbT = None
        try:
            AxkmkusbT = win32com.client.Dispatch("KMKUSB5I8OOCX.KMKUSB")
        except: 
            raise eg.Exception(self.text.txt_OCX_CannotBeFound_T)
        if AxkmkusbT != None:
            print self.text.txt_OCX_Found_T
        
        #Address the board...
        AxkmkusbT.device = self.b_nbr
        print self.text.txt_Initiated
       
        #Set outputs to last known states
        kmkSum = (
            self.do_state_memory[0]
            + self.do_state_memory[1]
            + self.do_state_memory[2]
            + self.do_state_memory[3]
            + self.do_state_memory[4]
            + self.do_state_memory[5]
            + self.do_state_memory[6]
            + self.do_state_memory[7]
        )
        
        AxkmkusbT.port_open_close = 1
        ########################################## input #############################################
        time.sleep(0.1)
        ########################################## input #############################################
        #AxkmkusbT.port_open_close = 0
        AxkmkusbT.out = str(kmkSum)

        while not stopThreadEvent.isSet():
            #AxkmkusbT.port_open_close = 1
            inputs = str(AxkmkusbT.binary)
            #AxkmkusbT.out = str(kmkSum)
            ########################################## input #############################################
            time.sleep(0.1)
            ########################################## input #############################################
            #AxkmkusbT.port_open_close = 0
            inputList = []
            
            for i in range(0, len(inputs)):
                inputList.insert(i, inputs[i])
        
            for i in range (0, len(inputs)):
                ret = int(inputList[i])
        
                if ret != self.di_event_trigger[i]:
                    if self.di_event_memory[i] != ret:
                        self.TriggerEvent(
                            self.text.txt_DI+str(i+1)+
                            self.text.txt_State+str(ret)
                        )
                        del self.di_event_memory[i]
                        self.di_event_memory.insert(i, ret)
                        
                if self.di_event_memory[i] != ret:
                    self.TriggerEvent(
                        self.text.txt_DI+str(i+1)+
                        self.text.txt_State+str(ret)
                    )
                    del self.di_event_memory[i]
                    self.di_event_memory.insert(i, ret)

            if self.do_state_memory <> self.do_state_trigger:
                kmkSum = (
                    self.do_state_trigger[0]
                    + self.do_state_trigger[1]
                    + self.do_state_trigger[2]
                    + self.do_state_trigger[3]
                    + self.do_state_trigger[4]
                    + self.do_state_trigger[5]
                    + self.do_state_trigger[6]
                    + self.do_state_trigger[7]
                )
                AxkmkusbT.out = str(kmkSum)
                self.do_state_memory = self.do_state_trigger

#            print self.di_event_trigger
#            print self.di_event_memory
            print self.do_state_memory
            #Test to se what gets sent.
            print "Output set to: ", str(kmkSum)
            stopThreadEvent.wait(self.thread_wait)

        AxkmkusbT.port_open_close = 0
        pythoncom.CoUninitialize()
        print self.text.txt_Polling



class SetDigitalOut(eg.ActionClass):
    iconFile = "digital-out-on"

    def __call__(self, do):

        if self.plugin.do_state_trigger[do-1]==0:
            del self.plugin.do_state_trigger[do-1]
            self.plugin.do_state_trigger.insert(do-1, 2**(do-1))
    
    #Digital outputs on the board, 8 in total
    def Configure(self, do = 1):
        panel = eg.ConfigPanel(self)
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfSetDO, digitalOut_ctrl)
        while panel.Affirmed():
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                do
            )



class ClearDigitalOut(eg.ActionClass):
    iconFile = "digital-out-off"

    def __call__(self, do):

        if self.plugin.do_state_trigger[do-1]==2**(do-1):
            del self.plugin.do_state_trigger[do-1]
            self.plugin.do_state_trigger.insert(do-1, 0)

    #Digital outputs on the board, 8 in total
    def Configure(self, do = 1):
        panel = eg.ConfigPanel(self)
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfClrDO, digitalOut_ctrl)
        while panel.Affirmed():
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                do
            )




        