# -*- coding: utf-8 -*-
#
# plugins/MarantzTCP/__init__.py
#
# This file is a plugin for EventGhost designed to control supported Marantz (and probably Denon) AV Receivers via TCP/IP.
# Copyright (C) 2012 Sam West <samwest.spam@gmail.com>
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1  by SamWest 2012-12-07 19:00 UTC+10
#      - initial version 
#===============================================================================

import eg, socket, sys, telnetlib, threading, traceback
import new
from telnetlib import Telnet

eg.RegisterPlugin(
    name = "Marantz TCP",
    author = "Daniel Eriksson <daniel@clearminds.se>",
    original_author = "Sam West",
    version = "0.0.2",
    kind = "external",
    description = "Controls Marantz Receivers over a TCP/IP connection.  Currently provides convenience methods for setting absolute volume, and sending arbitrary text commands."+
                  "See included MarantzVolumeSync.xml for example usage. " 
                  "<p>See <a href=http://us.marantz.com/DocumentMaster/US/Marantz_AV_SR_NR_PROTOCOL_V01.xls>here</a> for a full list of supported commands. "+
                  "<p>Supported Marantz models include: AV7005, SR7005, SR6006, SR6005, SR5006, NR1602 (and probably others with an ethernet connection). "+
                  "<p>Might also support (untested) Denon models: AVR-3808, AVC-3808, command list <a href=http://usa.denon.com/US/Downloads/Pages/InstructionManual.aspx?FileName=DocumentMaster/US/AVR-3808CISerialProtocol_Ver5.2.0a.pdf>here</a>.",
    createMacrosOnAdd=False
)

# Define commands
# (name, title, description (same as title if None), command)
commandsList = (
    ('Power',
        (
            ('PowerOn', 'Power on', None, '/power on', 'PWON'),
            ('PowerOff', 'Power off', None, '/power off', 'PWSTANDBY'),
        )
    ),

    ('Input',
        (
            ('InputPhono', 'Select Phono input', None, '/input phono', 'SIPHONO'),
            ('InputCD', 'Select CD input', None, '/input cd', 'SICD'),
            ('InputDVD', 'Select DVD input', None, '/input dvd', 'SIDVD'),
            ('InputBD', 'Select BD input', None, '/input bd', 'SIBD'),
            ('InputTV', 'Select TV input', None, '/input tv', 'SITV'),        
            ('InputSAT/CBL', 'Select SAT/CBL input', None, '/input sat/cbl', 'SISAT/CBL'),
            ('InputSAT', 'Select SAT input', None, '/input sat', 'SISAT'),
            ('InputVCR', 'Select VCR input', None, '/input vcr', 'SIVCR'),
            ('InputGame', 'Select Game input', None, '/input game', 'SIGAME'),
            ('InputV.Aux', 'Select V.Aux input', None, '/input v.aux', 'SIV.AUX'),
            ('InputTuner', 'Select Tuner input', None, '/input tuner', 'SITUNER'),
            ('InputCDR', 'Select CDR input', None, '/input cdr', 'SICDR'),
            ('Input AUX1', 'Select AUX1 input', None, '/input aux1', 'SIAUX1'),
            ('Input AUX2', 'Select AUX2 input', None, '/input aux2', 'SIAUX2'),
            ('Input NET/USB', 'Select NET/USB input', None, '/input net/usb', 'SINET/USB'),
            ('Input M-XPORT', 'Select M-XPORT input', None, '/input m-xport', 'SIM-XPORT'),
            ('Input USB/IPOD', 'Select USB/IPOD input', None, '/input usb/ipod', 'SIUSB/IPOD'),
        )
    ),

    ('Input mode',
        (
            ('InputmodeAuto', 'Inputmode auto', 'Sets inputmode to auto', '/inputmode auto', 'SDAUTO'),
            ('InputmodeAnalog', 'Inputmode analog', 'Sets inputmode to analog', '/inputmode analog', 'SDANALOG'),
            ('InputmodeHdmi', 'Inputmode HDMI', 'Sets inputmode to HDMI', '/inputmode hdmi', 'SDHDMI'),
            ('InputmodeDigital', 'Inputmode digital', 'Sets inputmode to digital', '/inputmode digital', 'SDDIGITAL')
        )
    ),

    ('Surround mode',
        (
            ('SurroundAuto', 'Select Auto surround mode', None, '/surround auto', 'MSAUTO'),
            ('SurroundStereo', 'Select Stereo surround mode', None, '/surround stereo', 'MSSTEREO'),
            ('SurroundMulti', 'Select Multi Channel Stereo surround mode', None, '/surround multi', 'MSMCH STEREO'),
            ('SurroundVirtual', 'Select Virtual surround mode', None, '/surround virtual', 'MSVIRTUAL'),
            ('SurroundDirect', 'Select Pure Direct surround mode', None, '/surround direct', 'MSDIRECT'),
            ('SurroundDolby', 'Select Dolby surround mode', None, '/surround dolby', 'MSDOLBY DIGITAL'),
            ('SurroundDolbyDigitalEx', 'Select Dolby Digital EX surround mode', None, '/surround ddex', 'MSDOLBY DIGITAL'),
            ('SurroundDolbyProLogic', 'Select Dolby ProLogic surround mode', None, '/surround dpl', 'MSDOLBY PRO LOGIC'),
            ('SurroundDTS', 'Select DTS surround mode', None, '/surround dts', 'MSDTS SURROUND'),
            ('SurroundDTSES', 'Select DTS ES surround mode', None, '/surround dtses', 'MSDTS SURROUND'),
        )
    ),

    ('HDMI Out',
        (
            ('HDMIMonitorOut-1', 'Sets Monitor to HDMI 1', None, '/hdmi out-1', 'VSMON1'),
            ('HDMIMonitorOut-2', 'Sets Monitor to HDMI 2', None, '/hdmi out-2', 'VSMON2'),
            ('HDMIMonitorOut-Auto', 'Sets Monitor to Auto', None, '/hdmi auto', 'VSMONAUTO'),
        )
    ),

    ('HDMI Audio Decode',
        (
            ('HDMIAudioDecodeAmp', 'Audo to AMP', 'Sets the HDMI Audio to the AMP', '/audio amp', 'VSAUDIOAMP'),
            ('HDMIAudioDecodeTV', 'Audo to TV', 'Sets the HDMI Audio to the TV', '/audio tv', 'VSAUDIOTV'),
        )
    ),

    ('Mute',
        (
            ('MuteOn', 'Mute on', None, '/mute on', 'MUON'),
            ('MuteOff', 'Mute off', None, '/mute off', 'MUOFF'),
        )
    ),

)


class SetVolumeAbsolute(eg.ActionBase):
    name='Set absolute volume'
    description='Sets the absolute volume'

    def __call__(self, volume):
        return self.plugin.setVolumeAbsolute(volume)
        
    def GetLabel(self, volume):
        return "Set Absolute Volume to %d" % volume
        
    def Configure(self, volume=25):
        panel = eg.ConfigPanel(self)
        
        valueCtrl = eg.SmartSpinIntCtrl(panel, -1, 0, min=0)
        panel.AddLine("Set absolute volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class MarantzAction(eg.ActionClass):
    
    def __call__(self):
        self.plugin.sendCommand(self.cmd)
            
''' Sends a raw text command to the receiver.  See http://us.marantz.com/DocumentMaster/US/Marantz_AV_SR_NR_PROTOCOL_V01.xls for details '''
class SendCommandText(eg.ActionBase):
    name='Send Text Command'
    description='Sets the absolute volume'

    def __call__(self, cmd):
        print 'Sending command: '+cmd
        return self.plugin.sendCommand(str(cmd))
        
    def GetLabel(self, cmd):
        return "Send Command '%s'" % cmd
        
    def Configure(self, volume=25):
        panel = eg.ConfigPanel(self)
        
        cmdCtrl = wx.TextCtrl(panel,-1, '')
        desc = wx.StaticText(panel,-1, 'See http://us.marantz.com/DocumentMaster/US/Marantz_AV_SR_NR_PROTOCOL_V01.xls for a list of commands')
        
        panel.AddLine(desc)
        panel.AddLine("Send Command: ", cmdCtrl)
        while panel.Affirmed():
            panel.SetResult(cmdCtrl.GetValue())
            
            
''' The EventGhost plugin class. '''
class MarantzTCPPlugin(eg.PluginBase):
   
    telnet=None
    reader=None
    host=None
    port=None
    timeout=None
    maxDb=12
    disabled=True
    
    
    def __init__(self):
        for groupname, list in commandsList:
            group = self.AddGroup(groupname)
            for classname, title, desc, app, cmd in list:
                if desc is None:
                    desc = title
                clsAttributes = dict(name=title, description=desc, appcmd=app, cmd=cmd)
                cls = new.classobj(classname, (MarantzAction,), clsAttributes)
                group.AddAction(cls)

        group = self.AddGroup('Volume')
        group.AddAction(SetVolumeAbsolute)
        self.AddAction(SendCommandText)
        
    def __start__(self, host, port, timeout, maxDb):
        self.host=host
        self.port=port
        self.timeout=timeout
        self.maxDb=maxDb
        self.disabled = False
        print "MarantzTCPPlugin started"

    def __stop__(self):
        self.closeTelnetSession()
        self.disabled = True
        print "MarantzTCPPlugin stopped."

    def __close__(self):
        print "MarantzTCPPlugin closing."
        self.closeTelnetSession()
        self.disabled = True
        print "MarantzTCPPlugin closed."        
        
    ''' Lazily create a new SocketSender '''
    def getTelnet(self):
        if (self.telnet == None):
            self.telnet = Telnet(self.host, self.port, self.timeout)
            print 'Successfully created connection to '+self.host+':'+str(self.port)+' with send-timeout: '+str(self.timeout)
            self.reader = ReadClass(self)
            self.reader.setTelnet(self.telnet)
            self.reader.start()
        return self.telnet
    
    def closeTelnetSession(self):
        try:
            if (self.reader!=None):
                self.reader.close()
                self.reader=None
                
            if (self.telnet != None):
                self.telnet.close()
                self.telnet = None
                
        except Exception:
            print 'Exception while closing telnet connection. ', sys.exc_info()[0]
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)        

    def roundTo(self, n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n/precision+correction)*precision
    
    ''' Rounds n to nearest 0.5 '''
    def roundToHalf(self, n):
        return self.roundTo(n, 0.5)            
        
    '''Converts a percentage volume (0,100) to a MV code to set the receiver to that volume'''
    def volumePercentToMV(self, perc):
        if (self.disabled == True):
            return
        if (perc < 0.0 or perc > 100.0): 
            print 'perc must be a float in range [0,100]'
            return None
    
        maxMV = self.maxDb + 80
        mvNum = self.roundToHalf((perc/100.0)*maxMV)
        sys.stdout.write('Setting receiver volume to {0}dB '.format(mvNum-80))
        
        #Build the correct MVXX or MVXXX string to set the volume.
        if (mvNum<10):
            cmd = 'MV' + ('%2.1f' % mvNum)
            cmd=cmd.replace('MV','MV0')
            cmd=cmd.replace('.', '')
        else:
            cmd = 'MV' + str(mvNum).replace('.5', '5').replace('.', '')
            
        if (cmd.endswith('0')): cmd=cmd[0:4]
        
        if (len(cmd) < 4): cmd = cmd + '0'
        return cmd
   
    def sendCommand(self, cmd):
        if (self.disabled == True):
            return
        
        try:
            self.getTelnet().write(cmd+'\r')
        except socket.error, e:
            eg.PrintError("Error sending data: %s" % e)
            self.closeTelnetSession()
    
    def setVolumeAbsolute(self, percentage):
        if (self.disabled == True):
            return
        
        cmd = self.volumePercentToMV(percentage)
        print '('+str(percentage)+"%), command="+cmd
        self.sendCommand(cmd)
        
    def Configure(self, host="192.168.66.60", rport=23, timeout=2, maxDb=12):
        text = self.text
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        
        hostCtrl = wx.TextCtrl(panel,-1, host)
        rportCtrl = eg.SpinIntCtrl(panel, -1, rport, max=65535)
        timeoutCtrl = eg.SpinIntCtrl(panel, -1, timeout, min=1, max=10)
        maxDbCtrl = eg.SpinIntCtrl(panel, -1, maxDb, min=-80, max=12)
  
        panel.AddLine("Marantz Receiver IP Address:", hostCtrl)
        panel.AddLine("Marantz Receiver TCP Port:  ", rportCtrl)        
        panel.AddLine("Send Timeout (s):           ", timeoutCtrl)
        panel.AddLine("Max Allowed Volume (dB):    ", maxDbCtrl)
        
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                rportCtrl.GetValue(),  
                timeoutCtrl.GetValue(),
                maxDbCtrl.GetValue()
            )
        
''' A class that just listens for incoming lines from the telnet client, and creates events from this text.
    Event generation is pretty basic, and could be easily improved to parse and add payloads etc. '''        
class ReadClass(threading.Thread):
    stop = 0
    telnet = None
    plugin = None
    
    def __init__(self, marantzTCPPlugin):
        super(ReadClass, self).__init__()
        self.stop=0
        self.plugin=marantzTCPPlugin
    
    def setTelnet(self, telnet):
        self.telnet = telnet
        
    def close(self):
        self.stop=1
    
    def run(self):
        while(self.stop==0):
            try:
                response = self.telnet.read_until('\r')
                self.plugin.TriggerEvent(response)
            except socket.error, e:
                if (self.stop!=1):
                    eg.PrintError("Error receiving data: %s" % e)
                return
            except:
                if (self.stop!=1):
                    e = sys.exc_info()[0]
                    eg.PrintError("Error in read thread: %s" % e)
                    ex_type, ex, tb = sys.exc_info()
                    traceback.print_tb(tb) 
                return
            

